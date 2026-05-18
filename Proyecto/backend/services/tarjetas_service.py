from datetime import date, datetime, timedelta

from backend.database.supabase_client import first, request


TARJETA_SELECT = ",".join(
    [
        "id_tarjeta",
        "codigo_identificador",
        "fecha_registro",
        "fecha_emision",
        "hora_emision",
        "vigencia",
        "vehiculo:vin("
        "vin,placa,modelo,asientos,ejes,cilindros,cc,ton,serie,chasis,motor,"
        "linea:id_linea(nombre_linea,marca:id_marca(nombre_marca)),"
        "tipo_vehiculo:id_tipo(nombre_tipo),"
        "color:id_color(nombre_color)"
        ")",
        "propietario:id_propietario(id_propietario,nombre,nit,cui)",
        "uso:id_uso(id_uso,nombre_uso)",
        "estado:id_estado(id_estado,nombre_estado)",
    ]
)


def listar_tarjetas():
    return request("tarjeta", select=TARJETA_SELECT, filters={"order": "id_tarjeta.desc"})


def catalogos():
    return {
        "marcas": request("marca", select="id_marca,nombre_marca", filters={"order": "nombre_marca.asc"}),
        "lineas": request("linea", select="id_linea,id_marca,nombre_linea", filters={"order": "nombre_linea.asc"}),
        "tipos": request("tipo_vehiculo", select="id_tipo,nombre_tipo", filters={"order": "nombre_tipo.asc"}),
        "colores": request("color", select="id_color,nombre_color", filters={"order": "nombre_color.asc"}),
        "usos": request("uso", select="id_uso,nombre_uso", filters={"order": "nombre_uso.asc"}),
        "estados": request("estado", select="id_estado,nombre_estado", filters={"order": "nombre_estado.asc"}),
        "propietarios": request("propietario", select="id_propietario,nombre,nit,cui", filters={"order": "nombre.asc"}),
    }


def _estado_id(nombre):
    estado = first("estado", "id_estado,nombre_estado", {"nombre_estado": f"eq.{nombre}"})
    if not estado:
        raise ValueError(f"No existe el estado '{nombre}' en la tabla estado.")
    return estado["id_estado"]


def _siguiente_codigo():
    year = date.today().year
    filas = request(
        "tarjeta",
        select="id_tarjeta,codigo_identificador",
        filters={"codigo_identificador": f"like.TC-{year}-%", "order": "id_tarjeta.desc", "limit": "1"},
    )
    if not filas:
        return f"TC-{year}-000001"
    numero = int(filas[0]["codigo_identificador"].split("-")[-1]) + 1
    return f"TC-{year}-{numero:06d}"


def crear_tarjeta(data):
    _validar_creacion(data)
    propietario_id = data.get("id_propietario")

    if not propietario_id:
        existente = (
            first("propietario", "id_propietario,nombre,nit,cui", {"nit": f"eq.{data['propietario']['nit']}"})
            or first("propietario", "id_propietario,nombre,nit,cui", {"cui": f"eq.{data['propietario']['cui']}"})
        )
        if existente:
            propietario_id = existente["id_propietario"]
        else:
            propietario = request(
                "propietario",
                method="POST",
                payload={
                    "nombre": data["propietario"]["nombre"],
                    "nit": data["propietario"]["nit"],
                    "cui": data["propietario"]["cui"],
                },
            )[0]
            propietario_id = propietario["id_propietario"]

    vehiculo = data["vehiculo"]
    vehiculo["placa"] = _normalizar_placa(vehiculo["placa"], data["id_uso"])
    if first("vehiculo", "vin", {"vin": f"eq.{vehiculo['vin']}"}):
        raise ValueError("Ya existe un vehiculo registrado con ese VIN.")
    if first("vehiculo", "placa", {"placa": f"eq.{vehiculo['placa']}"}):
        raise ValueError("Ya existe un vehiculo registrado con esa placa.")

    request(
        "vehiculo",
        method="POST",
        payload={
            "vin": vehiculo["vin"],
            "placa": vehiculo["placa"],
            "id_linea": vehiculo["id_linea"],
            "modelo": vehiculo["modelo"],
            "id_tipo": vehiculo["id_tipo"],
            "id_color": vehiculo["id_color"],
            "asientos": vehiculo["asientos"],
            "ejes": vehiculo["ejes"],
            "cilindros": vehiculo["cilindros"],
            "cc": vehiculo["cc"],
            "ton": vehiculo.get("ton", 0),
            "serie": vehiculo.get("serie"),
            "chasis": vehiculo.get("chasis"),
            "motor": vehiculo["motor"],
        },
    )

    now = datetime.now()
    fecha = now.date()
    tarjeta = request(
        "tarjeta",
        method="POST",
        payload={
            "vin": vehiculo["vin"],
            "id_propietario": propietario_id,
            "id_uso": data["id_uso"],
            "id_estado": _estado_id("Activa"),
            "codigo_identificador": data.get("codigo_identificador") or _siguiente_codigo(),
            "fecha_registro": fecha.isoformat(),
            "fecha_emision": fecha.isoformat(),
            "hora_emision": now.strftime("%H:%M:%S"),
            "vigencia": (fecha + timedelta(days=365)).isoformat(),
        },
    )[0]
    return tarjeta


def _validar_creacion(data):
    vehiculo = data.get("vehiculo") or {}
    propietario = data.get("propietario") or {}

    requeridos_vehiculo = [
        "vin",
        "placa",
        "id_linea",
        "modelo",
        "id_tipo",
        "id_color",
        "asientos",
        "ejes",
        "cilindros",
        "cc",
        "motor",
    ]
    for campo in requeridos_vehiculo:
        if vehiculo.get(campo) in (None, ""):
            raise ValueError(f"Falta el campo del vehiculo: {campo}")

    if len(str(vehiculo["vin"]).strip()) != 17:
        raise ValueError("El VIN debe tener exactamente 17 caracteres.")

    if not data.get("id_propietario"):
        for campo in ["nombre", "nit", "cui"]:
            if propietario.get(campo) in (None, ""):
                raise ValueError(f"Falta el campo del propietario: {campo}")

    if not data.get("id_uso"):
        raise ValueError("Debe seleccionar el uso del vehiculo.")

    if int(vehiculo["modelo"]) < 1900 or int(vehiculo["modelo"]) > 2100:
        raise ValueError("El modelo debe estar entre 1900 y 2100.")

    for campo in ["asientos", "ejes", "cilindros", "cc"]:
        if int(vehiculo[campo]) <= 0:
            raise ValueError(f"El campo {campo} debe ser mayor que cero.")

    if float(vehiculo.get("ton") or 0) < 0:
        raise ValueError("El tonelaje no puede ser negativo.")


def _normalizar_placa(placa, id_uso):
    placa = str(placa).strip().upper().replace(" ", "")
    if placa.startswith(("P-", "C-")):
        return placa
    uso = first("uso", "nombre_uso", {"id_uso": f"eq.{id_uso}"})
    prefijo = "C" if uso and uso.get("nombre_uso", "").lower() == "comercial" else "P"
    return f"{prefijo}-{placa}"

def actualizar_propietario(id_tarjeta, id_propietario, observaciones=""):
    actual = first("tarjeta", "id_tarjeta,id_propietario", {"id_tarjeta": f"eq.{id_tarjeta}"})
    request("tarjeta", method="PATCH", filters={"id_tarjeta": f"eq.{id_tarjeta}"}, payload={"id_propietario": id_propietario})
    return registrar_historial(id_tarjeta, "CAMBIO DUENO", actual.get("id_propietario"), id_propietario, observaciones)


def actualizar_motor(vin, id_tarjeta, motor, cilindros, cc, observaciones=""):
    actual = first("vehiculo", "motor,cilindros,cc", {"vin": f"eq.{vin}"})
    request("vehiculo", method="PATCH", filters={"vin": f"eq.{vin}"}, payload={"motor": motor, "cilindros": cilindros, "cc": cc})
    anterior = f"{actual.get('motor')} / {actual.get('cilindros')} / {actual.get('cc')}"
    nuevo = f"{motor} / {cilindros} / {cc}"
    return registrar_historial(id_tarjeta, "CAMBIO MOTOR", anterior, nuevo, observaciones)


def actualizar_color(vin, id_tarjeta, id_color, observaciones=""):
    actual = first("vehiculo", "id_color", {"vin": f"eq.{vin}"})
    request("vehiculo", method="PATCH", filters={"vin": f"eq.{vin}"}, payload={"id_color": id_color})
    return registrar_historial(id_tarjeta, "CAMBIO COLOR", actual.get("id_color"), id_color, observaciones)


def desactivar_tarjeta(id_tarjeta, motivo, observaciones=""):
    estado_id = _estado_id("Inactiva")
    request("tarjeta", method="PATCH", filters={"id_tarjeta": f"eq.{id_tarjeta}"}, payload={"id_estado": estado_id})
    return registrar_historial(id_tarjeta, "DESACTIVACION", "Activa", motivo, observaciones)


def activar_tarjeta(id_tarjeta, observaciones=""):
    tarjeta = first("tarjeta", "id_estado", {"id_tarjeta": f"eq.{id_tarjeta}"})
    if not tarjeta:
        raise ValueError("No existe la tarjeta especificada.")

    estado_actual = first("estado", "nombre_estado", {"id_estado": f"eq.{tarjeta['id_estado']}"})
    anterior = estado_actual.get("nombre_estado") if estado_actual else "Desconocido"
    if anterior.lower() == "activa":
        raise ValueError("La tarjeta ya se encuentra activa.")

    estado_id = _estado_id("Activa")
    request("tarjeta", method="PATCH", filters={"id_tarjeta": f"eq.{id_tarjeta}"}, payload={"id_estado": estado_id})
    return registrar_historial(id_tarjeta, "REACTIVACION", anterior, "Activa", observaciones)


def registrar_historial(id_tarjeta, tipo, anterior, nuevo, observaciones):
    return request(
        "historial_cambios",
        method="POST",
        payload={
            "id_tarjeta": id_tarjeta,
            "tipo_cambio": tipo,
            "valor_anterior": "" if anterior is None else str(anterior),
            "valor_actual": "" if nuevo is None else str(nuevo),
            "observaciones": observaciones,
        },
    )[0]


def listar_historial():
    select = "id_historial,tipo_cambio,valor_anterior,valor_actual,fecha_cambio,observaciones,tarjeta:id_tarjeta(codigo_identificador,vehiculo:vin(placa))"
    return request("historial_cambios", select=select, filters={"order": "fecha_cambio.desc"})


def eliminar_tarjeta(id_tarjeta):
    tarjeta = first("tarjeta", "vin", {"id_tarjeta": f"eq.{id_tarjeta}"})
    
    # Eliminar historial asociado primero
    request("historial_cambios", method="DELETE", filters={"id_tarjeta": f"eq.{id_tarjeta}"})
    
    # Eliminar tarjeta
    res = request("tarjeta", method="DELETE", filters={"id_tarjeta": f"eq.{id_tarjeta}"})
    
    # Eliminar vehiculo
    if tarjeta and tarjeta.get("vin"):
        request("vehiculo", method="DELETE", filters={"vin": f"eq.{tarjeta['vin']}"})
    return res
