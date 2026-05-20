from fastapi import APIRouter, HTTPException

import psycopg2
from backend.services import tarjetas_service


router = APIRouter(prefix="/api", tags=["tarjetas"])


def handle(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except psycopg2.Error as exc:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: {str(exc)}") from exc


@router.get("/health")
def health():
    return {"ok": True}


@router.get("/catalogos")
def catalogos():
    return handle(tarjetas_service.catalogos)


@router.get("/tarjetas")
def tarjetas():
    return handle(tarjetas_service.listar_tarjetas)


@router.post("/tarjetas")
def crear_tarjeta(payload: dict):
    return handle(tarjetas_service.crear_tarjeta, payload)


@router.post("/mantenimiento/dueno")
def cambio_dueno(payload: dict):
    return handle(
        tarjetas_service.actualizar_propietario,
        payload["id_tarjeta"],
        payload["id_propietario"],
        payload.get("observaciones", ""),
    )


@router.post("/mantenimiento/motor")
def cambio_motor(payload: dict):
    return handle(
        tarjetas_service.actualizar_motor,
        payload["vin"],
        payload["id_tarjeta"],
        payload["motor"],
        payload["cilindros"],
        payload["cc"],
        payload.get("observaciones", ""),
    )


@router.post("/mantenimiento/color")
def cambio_color(payload: dict):
    return handle(
        tarjetas_service.actualizar_color,
        payload["vin"],
        payload["id_tarjeta"],
        payload["id_color"],
        payload.get("observaciones", ""),
    )


@router.post("/mantenimiento/activar")
def activar(payload: dict):
    return handle(
        tarjetas_service.activar_tarjeta,
        payload["id_tarjeta"],
        payload.get("observaciones", ""),
    )


@router.post("/desactivaciones")
def desactivar(payload: dict):
    return handle(
        tarjetas_service.desactivar_tarjeta,
        payload["id_tarjeta"],
        payload["motivo"],
        payload.get("observaciones", ""),
    )


@router.get("/historial")
def historial():
    return handle(tarjetas_service.listar_historial)


@router.delete("/tarjetas/{id_tarjeta}")
def eliminar_tarjeta(id_tarjeta: int):
    return handle(tarjetas_service.eliminar_tarjeta, id_tarjeta)


@router.post("/catalogos/marca")
def crear_marca(payload: dict):
    return handle(tarjetas_service.crear_marca, payload["nombre"])


@router.post("/catalogos/linea")
def crear_linea(payload: dict):
    return handle(tarjetas_service.crear_linea, payload["id_marca"], payload["nombre"])


@router.post("/catalogos/tipo")
def crear_tipo_vehiculo(payload: dict):
    return handle(tarjetas_service.crear_tipo_vehiculo, payload["nombre"])


@router.post("/catalogos/color")
def crear_color(payload: dict):
    return handle(tarjetas_service.crear_color, payload["nombre"])
