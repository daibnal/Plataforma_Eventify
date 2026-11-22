from datetime import datetime

from api.database import db
from api.models.orden_compra import OrdenCompra

from api.utils.serializer import serializar_lista

def listar_ordenes():
    """
    Obtiene todas las ordenes de compra
    """
    return serializar_lista(db.ordenes_compra.find())

def agregar_orden(orden: OrdenCompra):
    """
        Agrega una nueva orden de compra
        Busca el _id del usuario por su RUN y el del evento por su codigo,
        igual que el seed con findOne()._id, y los guarda como referencia
    """
    usuario = db.usuarios.find_one({"run": orden.run, "dv": orden.dv})
    evento = db.eventos.find_one({"codigo": orden.codigo_evento})

    if not usuario or not evento:
        return None

    documento = {
        "usuario_id": usuario["_id"],
        "evento_id": evento["_id"],
        "total": orden.total,
        "fecha": datetime.now()
    }

    db.ordenes_compra.insert_one(documento)

    return {
        "mensaje": "Orden agregada correctamente"
    }