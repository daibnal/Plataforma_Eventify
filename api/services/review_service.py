from api.database import db
from api.models.review_evaluacion import ReviewEvaluacion
from api.utils.serializer import serializar_lista

def listar_reviews():
    return serializar_lista(db.review_evaluaciones.find())

def agregar_review(review: ReviewEvaluacion):
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
    return {"mensaje": "Reseña agregada correctamente"}