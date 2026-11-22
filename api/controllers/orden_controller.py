from fastapi import APIRouter, HTTPException
from api.models.orden_compra import OrdenCompra
from api.services.orden_service import listar_ordenes, agregar_orden

router = APIRouter(prefix="/ordenes", tags=["Órdenes de compra"])

@router.get("/")
def obtener_ordenes():
    return listar_ordenes()

@router.post("/")
def crear_orden(orden: OrdenCompra):
    resultado = agregar_orden(orden)
    if not resultado:
        raise HTTPException(status_code=404, detail="Usuario o evento no encontrado")
    return resultado