from api.database import db
from api.models.review_evaluacion import ReviewEvaluacion

from api.utils.serializer import serializar_lista

def listar_reviews():
    """
    Obtiene todas las reseñas
    """
    return serializar_lista(db.review_evaluaciones.find())

def agregar_review(review: ReviewEvaluacion):
    """
        Agrega una nueva reseña
        Busca el _id del usuario por su RUN y el del evento por su codigo,
        igual que el seed con findOne()._id, y los guarda como referencia
    """
    usuario = db.usuarios.find_one({"run": review.run, "dv": review.dv})
    evento = db.eventos.find_one({"codigo": review.codigo_evento})

    if not usuario or not evento:
        return None

    documento = {
        "usuario_id": usuario["_id"],
        "evento_id": evento["_id"],
        "calificacion": review.calificacion,
        "comentario": review.comentario
    }

    db.review_evaluaciones.insert_one(documento)

    return {
        "mensaje": "Reseña agregada correctamente"
    }