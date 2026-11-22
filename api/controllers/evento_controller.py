from fastapi import APIRouter, HTTPException
from api.services.evento_service import (
    listar_eventos, buscar_por_codigo, filtrar_por_ciudad,
    agregar_evento, actualizar_evento, eliminar_evento
)
from api.models.evento import Evento, EventoCambios

router = APIRouter(
    prefix="/eventos",
    tags=["Eventos"]
)

@router.get("/")
def obtener_eventos():
    return listar_eventos()

@router.get("/ciudad/{ciudad}")
def filtro_por_ciudad(ciudad: str):
    resultado = filtrar_por_ciudad(ciudad)
    if not resultado:
        raise HTTPException(
            status_code=404,
            detail=f"Sin eventos en {ciudad}"
        )

    return resultado

@router.get("/{codigo}")
def filtro_por_codigo(codigo: str):
    resultado = buscar_por_codigo(codigo)
    if not resultado:
        raise HTTPException(
            status_code=404,
            detail=f"No existe el evento {codigo}"
        )

    return resultado

@router.post("/")
def crear_evento(e: Evento):
    resultado = agregar_evento(e)
    if not resultado:
        raise HTTPException(
            status_code=400,
            detail=f"Ya existe un evento con codigo {e.codigo}"
        )

    return resultado

@router.put("/{codigo}")
def modificar_evento(codigo: str, cambios: EventoCambios):
    if actualizar_evento(codigo, cambios) == 0:
        raise HTTPException(
            status_code=404,
            detail=f"No existe el evento {codigo}"
        )

    return {"mensaje": "Evento actualizado correctamente"}

@router.delete("/{codigo}")
def borrar_evento(codigo: str):
    if eliminar_evento(codigo) == 0:
        raise HTTPException(
            status_code=404,
            detail=f"No existe el evento {codigo}"
        )

    return {"mensaje": "Evento eliminado correctamente"}