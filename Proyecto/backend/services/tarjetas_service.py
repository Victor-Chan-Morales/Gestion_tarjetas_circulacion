from datetime import date, datetime, timedelta
from backend.database.db_connection import execute_query, execute_modify

def listar_tarjetas():
    query = """
    SELECT 
      t.id_tarjeta, t.codigo_identificador, t.fecha_registro, t.fecha_emision, t.hora_emision, t.vigencia,
      json_build_object(
        'vin', v.vin, 'placa', v.placa, 'modelo', v.modelo, 'asientos', v.asientos, 'ejes', v.ejes, 'cilindros', v.cilindros, 'cc', v.cc, 'ton', v.ton, 'serie', v.serie, 'chasis', v.chasis, 'motor', v.motor,
        'linea', json_build_object('nombre_linea', l.nombre_linea, 'marca', json_build_object('nombre_marca', m.nombre_marca)),
        'tipo_vehiculo', json_build_object('nombre_tipo', tv.nombre_tipo),
        'color', json_build_object('nombre_color', c.nombre_color)
      ) as vehiculo,
      json_build_object('id_propietario', p.id_propietario, 'nombre', p.nombre, 'nit', p.nit, 'cui', p.cui) as propietario,
      json_build_object('id_uso', u.id_uso, 'nombre_uso', u.nombre_uso) as uso,
      json_build_object('id_estado', e.id_estado, 'nombre_estado', e.nombre_estado) as estado
    FROM tarjeta t
    JOIN vehiculo v ON t.vin = v.vin
    JOIN linea l ON v.id_linea = l.id_linea
    JOIN marca m ON l.id_marca = m.id_marca
    JOIN tipo_vehiculo tv ON v.id_tipo = tv.id_tipo
    JOIN color c ON v.id_color = c.id_color
    JOIN propietario p ON t.id_propietario = p.id_propietario
    JOIN uso u ON t.id_uso = u.id_uso
    JOIN estado e ON t.id_estado = e.id_estado
    ORDER BY t.id_tarjeta DESC;
    """
    return execute_query(query)

def catalogos():
    return {
        "marcas": execute_query("SELECT id_marca, nombre_marca FROM marca ORDER BY nombre_marca ASC"),
        "lineas": execute_query("SELECT id_linea, id_marca, nombre_linea FROM linea ORDER BY nombre_linea ASC"),
        "tipos": execute_query("SELECT id_tipo, nombre_tipo FROM tipo_vehiculo ORDER BY nombre_tipo ASC"),
        "colores": execute_query("SELECT id_color, nombre_color FROM color ORDER BY nombre_color ASC"),
        "usos": execute_query("SELECT id_uso, nombre_uso FROM uso ORDER BY nombre_uso ASC"),
        "estados": execute_query("SELECT id_estado, nombre_estado FROM estado ORDER BY nombre_estado ASC"),
        "propietarios": execute_query("SELECT id_propietario, nombre, nit, cui FROM propietario ORDER BY nombre ASC"),
    }

def _estado_id(nombre):
    rows = execute_query("SELECT id_estado FROM estado WHERE nombre_estado = %s", (nombre,))
    if not rows:
        raise ValueError(f"No existe el estado '{nombre}' en la tabla estado.")
    return rows[0]["id_estado"]

def _siguiente_codigo():
    year = date.today().year
    rows = execute_query(
        "SELECT codigo_identificador FROM tarjeta WHERE codigo_identificador LIKE %s ORDER BY id_tarjeta DESC LIMIT 1",
        (f"TC-{year}-%",)
    )
    if not rows:
        return f"TC-{year}-000001"
    numero = int(rows[0]["codigo_identificador"].split("-")[-1]) + 1
    return f"TC-{year}-{numero:06d}"

def _normalizar_placa(placa, id_uso):
    placa = str(placa).strip().upper().replace(" ", "")
    if placa.startswith(("P-", "C-")):
        return placa
    rows = execute_query("SELECT nombre_uso FROM uso WHERE id_uso = %s", (id_uso,))
    uso = rows[0] if rows else None
    prefijo = "C" if uso and uso.get("nombre_uso", "").lower() == "comercial" else "P"
    return f"{prefijo}-{placa}"

def _validar_creacion(data):
    vehiculo = data.get("vehiculo") or {}
    propietario = data.get("propietario") or {}

    requeridos_vehiculo = [
        "vin", "placa", "id_linea", "modelo", "id_tipo", "id_color",
        "asientos", "ejes", "cilindros", "cc", "motor",
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

def crear_tarjeta(data):
    _validar_creacion(data)
    propietario_id = data.get("id_propietario")

    if not propietario_id:
        rows = execute_query(
            "SELECT id_propietario FROM propietario WHERE nit = %s OR cui = %s LIMIT 1",
            (data['propietario']['nit'], data['propietario']['cui'])
        )
        if rows:
            propietario_id = rows[0]["id_propietario"]
        else:
            res = execute_modify(
                "INSERT INTO propietario (nombre, nit, cui) VALUES (%s, %s, %s) RETURNING id_propietario",
                (data["propietario"]["nombre"], data["propietario"]["nit"], data["propietario"]["cui"]),
                returning=True
            )
            propietario_id = res["id_propietario"]

    vehiculo = data["vehiculo"]
    vehiculo["placa"] = _normalizar_placa(vehiculo["placa"], data["id_uso"])
    
    if execute_query("SELECT vin FROM vehiculo WHERE vin = %s", (vehiculo['vin'],)):
        raise ValueError("Ya existe un vehiculo registrado con ese VIN.")
    if execute_query("SELECT placa FROM vehiculo WHERE placa = %s", (vehiculo['placa'],)):
        raise ValueError("Ya existe un vehiculo registrado con esa placa.")

    execute_modify(
        """INSERT INTO vehiculo (vin, placa, id_linea, modelo, id_tipo, id_color, asientos, ejes, cilindros, cc, ton, serie, chasis, motor)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        (
            vehiculo["vin"], vehiculo["placa"], vehiculo["id_linea"], vehiculo["modelo"],
            vehiculo["id_tipo"], vehiculo["id_color"], vehiculo["asientos"], vehiculo["ejes"],
            vehiculo["cilindros"], vehiculo["cc"], vehiculo.get("ton", 0), vehiculo.get("serie"),
            vehiculo.get("chasis"), vehiculo["motor"]
        )
    )

    now = datetime.now()
    fecha = now.date()
    codigo = data.get("codigo_identificador") or _siguiente_codigo()
    
    tarjeta = execute_modify(
        """INSERT INTO tarjeta (vin, id_propietario, id_uso, id_estado, codigo_identificador, fecha_registro, fecha_emision, hora_emision, vigencia)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *""",
        (
            vehiculo["vin"], propietario_id, data["id_uso"], _estado_id("Activa"),
            codigo, fecha.isoformat(), fecha.isoformat(), now.strftime("%H:%M:%S"),
            (fecha + timedelta(days=365)).isoformat()
        ),
        returning=True
    )
    return tarjeta

def actualizar_propietario(id_tarjeta, id_propietario, observaciones=""):
    actual = execute_query("SELECT id_propietario FROM tarjeta WHERE id_tarjeta = %s", (id_tarjeta,))
    if not actual:
        raise ValueError("Tarjeta no encontrada")
    
    execute_modify("UPDATE tarjeta SET id_propietario = %s WHERE id_tarjeta = %s", (id_propietario, id_tarjeta))
    return registrar_historial(id_tarjeta, "CAMBIO DUENO", actual[0]["id_propietario"], id_propietario, observaciones)

def actualizar_motor(vin, id_tarjeta, motor, cilindros, cc, observaciones=""):
    actual = execute_query("SELECT motor, cilindros, cc FROM vehiculo WHERE vin = %s", (vin,))
    if not actual:
        raise ValueError("Vehiculo no encontrado")
    
    execute_modify(
        "UPDATE vehiculo SET motor = %s, cilindros = %s, cc = %s WHERE vin = %s",
        (motor, cilindros, cc, vin)
    )
    anterior = f"{actual[0]['motor']} / {actual[0]['cilindros']} / {actual[0]['cc']}"
    nuevo = f"{motor} / {cilindros} / {cc}"
    return registrar_historial(id_tarjeta, "CAMBIO MOTOR", anterior, nuevo, observaciones)

def actualizar_color(vin, id_tarjeta, id_color, observaciones=""):
    actual = execute_query("SELECT id_color FROM vehiculo WHERE vin = %s", (vin,))
    if not actual:
        raise ValueError("Vehiculo no encontrado")
        
    execute_modify("UPDATE vehiculo SET id_color = %s WHERE vin = %s", (id_color, vin))
    return registrar_historial(id_tarjeta, "CAMBIO COLOR", actual[0]["id_color"], id_color, observaciones)

def desactivar_tarjeta(id_tarjeta, motivo, observaciones=""):
    estado_id = _estado_id("Inactiva")
    execute_modify("UPDATE tarjeta SET id_estado = %s WHERE id_tarjeta = %s", (estado_id, id_tarjeta))
    return registrar_historial(id_tarjeta, "DESACTIVACION", "Activa", motivo, observaciones)

def activar_tarjeta(id_tarjeta, observaciones=""):
    tarjeta = execute_query("SELECT id_estado FROM tarjeta WHERE id_tarjeta = %s", (id_tarjeta,))
    if not tarjeta:
        raise ValueError("No existe la tarjeta especificada.")

    estado_actual = execute_query("SELECT nombre_estado FROM estado WHERE id_estado = %s", (tarjeta[0]['id_estado'],))
    anterior = estado_actual[0]["nombre_estado"] if estado_actual else "Desconocido"
    if anterior.lower() == "activa":
        raise ValueError("La tarjeta ya se encuentra activa.")

    estado_id = _estado_id("Activa")
    execute_modify("UPDATE tarjeta SET id_estado = %s WHERE id_tarjeta = %s", (estado_id, id_tarjeta))
    return registrar_historial(id_tarjeta, "REACTIVACION", anterior, "Activa", observaciones)

def registrar_historial(id_tarjeta, tipo, anterior, nuevo, observaciones):
    return execute_modify(
        """INSERT INTO historial_cambios (id_tarjeta, tipo_cambio, valor_anterior, valor_actual, observaciones)
           VALUES (%s, %s, %s, %s, %s) RETURNING *""",
        (id_tarjeta, tipo, "" if anterior is None else str(anterior), "" if nuevo is None else str(nuevo), observaciones),
        returning=True
    )

def listar_historial():
    query = """
    SELECT 
      h.id_historial, h.tipo_cambio, h.valor_anterior, h.valor_actual, h.fecha_cambio, h.observaciones,
      json_build_object('codigo_identificador', t.codigo_identificador, 'vehiculo', json_build_object('vin', v.vin, 'placa', v.placa)) as tarjeta
    FROM historial_cambios h
    JOIN tarjeta t ON h.id_tarjeta = t.id_tarjeta
    JOIN vehiculo v ON t.vin = v.vin
    ORDER BY h.fecha_cambio DESC
    """
    return execute_query(query)

def eliminar_tarjeta(id_tarjeta):
    tarjeta = execute_query("SELECT vin FROM tarjeta WHERE id_tarjeta = %s", (id_tarjeta,))
    
    execute_modify("DELETE FROM historial_cambios WHERE id_tarjeta = %s", (id_tarjeta,))
    res = execute_modify("DELETE FROM tarjeta WHERE id_tarjeta = %s RETURNING *", (id_tarjeta,), returning=True)
    
    if tarjeta and tarjeta[0].get("vin"):
        execute_modify("DELETE FROM vehiculo WHERE vin = %s", (tarjeta[0]['vin'],))
    return res

def crear_marca(nombre):
    nombre = nombre.strip().title()
    if not nombre:
        raise ValueError("El nombre de la marca no puede estar vacio")
    return execute_modify("INSERT INTO marca (nombre_marca) VALUES (%s) RETURNING *", (nombre,), returning=True)

def crear_linea(id_marca, nombre):
    nombre = nombre.strip().title()
    if not nombre:
        raise ValueError("El nombre de la linea no puede estar vacio")
    if not id_marca:
        raise ValueError("Debe seleccionar una marca para agregar una linea")
    return execute_modify("INSERT INTO linea (id_marca, nombre_linea) VALUES (%s, %s) RETURNING *", (id_marca, nombre), returning=True)

def crear_tipo_vehiculo(nombre):
    nombre = nombre.strip().title()
    if not nombre:
        raise ValueError("El tipo de vehiculo no puede estar vacio")
    return execute_modify("INSERT INTO tipo_vehiculo (nombre_tipo) VALUES (%s) RETURNING *", (nombre,), returning=True)

def crear_color(nombre):
    nombre = nombre.strip().title()
    if not nombre:
        raise ValueError("El color no puede estar vacio")
    return execute_modify("INSERT INTO color (nombre_color) VALUES (%s) RETURNING *", (nombre,), returning=True)
