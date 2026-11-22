from api.database import db
from api.models.usuario import Usuario

from api.utils.serializer import serializar_lista, serializar_documento

def listar_usuarios():
    """
    Obtiene todos los usuarios
    """
    return serializar_lista(db.usuarios.find())

def buscar_por_run(run: str):
    """
    Obtiene un usuario por su RUN (sin puntos ni DV)
    """
    return serializar_documento(db.usuarios.find_one({"run": run}))

def agregar_usuario(usuario: Usuario):
    """
        Agrega un nuevo usuario
        params:
            usuario: datos a agregar
    """
    if db.usuarios.find_one({"run": usuario.run}):
        return None

    documento = {
        "run": usuario.run,
        "dv": usuario.dv,
        "nombre": usuario.nombre,
        "apellido": usuario.apellido,
        "correo": usuario.correo,
        "telefono": usuario.telefono,
        "fecha_nacimiento": usuario.fecha_nacimiento,
        "es_vip": usuario.es_vip
    }

    db.usuarios.insert_one(documento)

    return {
        "mensaje": "Usuario agregado correctamente"
    }