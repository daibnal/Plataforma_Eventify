from api.database import db
from api.models.evento import Evento, EventoCambios

from api.utils.serializer import serializar_lista, serializar_documento

def listar_eventos():
    """
    Obtiene todos los eventos
    """
    return serializar_lista(db.eventos.find())

def buscar_por_codigo(codigo: str):
    """
    Obtiene un evento por su codigo
    """
    return serializar_documento(db.eventos.find_one({"codigo": codigo}))

def filtrar_por_ciudad(ciudad: str):
    """
    Obtiene los eventos de una ciudad (campo del objeto embebido ubicacion)
    """
    return serializar_lista(db.eventos.find({"ubicacion.ciudad": ciudad}))

def agregar_evento(evento: Evento):
    """
        Agrega un nuevo evento
        params:
            evento: datos a agregar (incluye ubicacion y tickets embebidos)
    """
    if db.eventos.find_one({"codigo": evento.codigo}):
        return None

    db.eventos.insert_one(evento.model_dump())

    return {
        "mensaje": "Evento agregado correctamente"
    }

def actualizar_evento(codigo: str, cambios: EventoCambios):
    """
        Actualiza el titulo y la capacidad de un evento
        Retorna cuantos eventos coincidieron con el codigo (0 = no existe)
    """
    resultado = db.eventos.update_one(
        {"codigo": codigo},
        {"$set": {
            "titulo": cambios.titulo,
            "capacidad": cambios.capacidad
        }}
    )
    return resultado.matched_count

def eliminar_evento(codigo: str):
    """
        Elimina un evento por su codigo
        Retorna cuantos eventos se eliminaron (0 = no existe)
    """
    resultado = db.eventos.delete_one({"codigo": codigo})
    return resultado.deleted_count