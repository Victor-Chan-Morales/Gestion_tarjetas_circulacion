import json
import os
import urllib.error
import urllib.request
from datetime import date, timedelta


API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000/api").rstrip("/")


def _http(path, method="GET", payload=None):
    url = f"{API_BASE_URL}{path}"
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(
        url,
        data=body,
        method=method,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=3) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw) if raw else None
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8")
        try:
            parsed = json.loads(detail)
            message = parsed.get("detail", detail)
            if isinstance(message, str) and message.startswith("{"):
                nested = json.loads(message)
                message = nested.get("message") or nested.get("detail") or message
        except Exception:
            message = detail
        raise RuntimeError(message) from exc
    except Exception:
        raise


def obtener_tarjetas():
    try:
        return _http("/tarjetas")
    except Exception:
        return datos_demo()


def obtener_catalogos():
    try:
        return _http("/catalogos")
    except Exception:
        return catalogos_demo()


def crear_tarjeta(payload):
    return _http("/tarjetas", method="POST", payload=payload)


def registrar_cambio_dueno(payload):
    return _http("/mantenimiento/dueno", method="POST", payload=payload)


def registrar_cambio_motor(payload):
    return _http("/mantenimiento/motor", method="POST", payload=payload)


def registrar_cambio_color(payload):
    return _http("/mantenimiento/color", method="POST", payload=payload)


def reactivar_tarjeta(payload):
    return _http("/mantenimiento/activar", method="POST", payload=payload)


def desactivar_tarjeta(payload):
    return _http("/desactivaciones", method="POST", payload=payload)


def obtener_historial():
    try:
        return _http("/historial")
    except Exception:
        return historial_demo()


def eliminar_tarjeta(id_tarjeta):
    return _http(f"/tarjetas/{id_tarjeta}", method="DELETE")


def catalogos_demo():
    return {
        "marcas": [
            {"id_marca": 1, "nombre_marca": "Toyota"},
            {"id_marca": 2, "nombre_marca": "Honda"},
            {"id_marca": 3, "nombre_marca": "Nissan"},
            {"id_marca": 4, "nombre_marca": "Mazda"},
        ],
        "lineas": [
            {"id_linea": 1, "id_marca": 1, "nombre_linea": "Corolla"},
            {"id_linea": 2, "id_marca": 1, "nombre_linea": "Hilux"},
            {"id_linea": 3, "id_marca": 2, "nombre_linea": "Civic"},
            {"id_linea": 4, "id_marca": 3, "nombre_linea": "Sentra"},
            {"id_linea": 5, "id_marca": 4, "nombre_linea": "CX-5"},
        ],
        "tipos": [
            {"id_tipo": 1, "nombre_tipo": "Sedan"},
            {"id_tipo": 2, "nombre_tipo": "Pick Up"},
            {"id_tipo": 3, "nombre_tipo": "SUV"},
        ],
        "colores": [
            {"id_color": 1, "nombre_color": "Blanco"},
            {"id_color": 2, "nombre_color": "Negro"},
            {"id_color": 3, "nombre_color": "Gris"},
            {"id_color": 4, "nombre_color": "Rojo"},
            {"id_color": 5, "nombre_color": "Azul"},
        ],
        "usos": [
            {"id_uso": 1, "nombre_uso": "Particular"},
            {"id_uso": 2, "nombre_uso": "Comercial"},
        ],
        "estados": [
            {"id_estado": 1, "nombre_estado": "Activa"},
            {"id_estado": 2, "nombre_estado": "Inactiva"},
            {"id_estado": 3, "nombre_estado": "Suspendida"},
            {"id_estado": 4, "nombre_estado": "Vencida"},
        ],
        "propietarios": [
            {"id_propietario": 1, "nombre": "Juan Carlos Perez Lopez", "nit": "1234567-8", "cui": "1234567890101"},
            {"id_propietario": 2, "nombre": "Maria Elena Garcia Morales", "nit": "8765432-1", "cui": "8765432101234"},
            {"id_propietario": 3, "nombre": "Carlos Roberto Martinez", "nit": "5678901-2", "cui": "2345678901234"},
            {"id_propietario": 4, "nombre": "Ana Lucia Hernandez Ruiz", "nit": "9012345-6", "cui": "3456789012345"},
            {"id_propietario": 5, "nombre": "Pedro Antonio Ramirez", "nit": "3456789-0", "cui": "4567890123456"},
        ],
    }


def datos_demo():
    base = catalogos_demo()
    rows = [
        ("TC-2024-000001", "JTDKN3DU5A0123456", "P-123ABC", 1, 2022, 1, 1, 1, "MOT001", 1, 1, "2025-01-15"),
        ("TC-2024-000002", "8AJBA3CD9P0123456", "P-456DEF", 2, 2023, 2, 2, 2, "MOT002", 2, 1, "2025-02-20"),
        ("TC-2024-000003", "2HGFB2F59CH123456", "P-789GHI", 3, 2021, 1, 3, 3, "MOT003", 1, 2, "2025-03-10"),
        ("TC-2023-000045", "3N1AB7AP8HY123456", "P-012JKL", 4, 2020, 1, 4, 4, "MOT004", 1, 4, "2024-06-05"),
        ("TC-2024-000010", "JM3KE2CY0G0123456", "P-345MNO", 5, 2024, 3, 5, 1, "MOT005", 1, 1, "2025-04-12"),
    ]

    tarjetas = []
    for idx, row in enumerate(rows, start=1):
        codigo, vin, placa, id_linea, modelo, id_tipo, id_color, id_prop, motor, id_uso, id_estado, vigencia = row
        linea = next(x for x in base["lineas"] if x["id_linea"] == id_linea)
        marca = next(x for x in base["marcas"] if x["id_marca"] == linea["id_marca"])
        tipo = next(x for x in base["tipos"] if x["id_tipo"] == id_tipo)
        color = next(x for x in base["colores"] if x["id_color"] == id_color)
        propietario = next(x for x in base["propietarios"] if x["id_propietario"] == id_prop)
        uso = next(x for x in base["usos"] if x["id_uso"] == id_uso)
        estado = next(x for x in base["estados"] if x["id_estado"] == id_estado)

        tarjetas.append({
            "id_tarjeta": idx,
            "codigo_identificador": codigo,
            "fecha_registro": "2024-01-15",
            "fecha_emision": "2024-01-15",
            "hora_emision": "09:30:00",
            "vigencia": vigencia,
            "propietario": propietario,
            "uso": uso,
            "estado": estado,
            "vehiculo": {
                "vin": vin,
                "placa": placa,
                "modelo": modelo,
                "asientos": 5,
                "ejes": 2,
                "cilindros": 4,
                "cc": 1800,
                "ton": 0,
                "serie": f"SER{idx:03d}",
                "chasis": f"CHS{idx:03d}",
                "motor": motor,
                "linea": {"nombre_linea": linea["nombre_linea"], "marca": {"nombre_marca": marca["nombre_marca"]}},
                "tipo_vehiculo": {"nombre_tipo": tipo["nombre_tipo"]},
                "color": {"nombre_color": color["nombre_color"]},
            },
        })
    return tarjetas


def historial_demo():
    return [
        {
            "id_historial": 1,
            "fecha_cambio": "2024-03-15T10:20:00",
            "tipo_cambio": "CAMBIO COLOR",
            "valor_anterior": "Gris",
            "valor_actual": "Blanco",
            "observaciones": "Cambio de color autorizado",
            "tarjeta": {"codigo_identificador": "TC-2024-000001", "vehiculo": {"placa": "P-123ABC"}},
        },
        {
            "id_historial": 2,
            "fecha_cambio": "2024-04-20T12:10:00",
            "tipo_cambio": "CAMBIO MOTOR",
            "valor_anterior": "MOT-OLD-002",
            "valor_actual": "MOT002",
            "observaciones": "Reemplazo de motor por falla",
            "tarjeta": {"codigo_identificador": "TC-2024-000002", "vehiculo": {"placa": "P-456DEF"}},
        },
        {
            "id_historial": 3,
            "fecha_cambio": "2024-05-10T09:00:00",
            "tipo_cambio": "CAMBIO DUENO",
            "valor_anterior": "Carlos Martinez",
            "valor_actual": "Pedro Antonio Ramirez",
            "observaciones": "Traspaso de vehiculo",
            "tarjeta": {"codigo_identificador": "TC-2024-000010", "vehiculo": {"placa": "P-345MNO"}},
        },
    ]


def vigencia_un_anio():
    return (date.today() + timedelta(days=365)).isoformat()
