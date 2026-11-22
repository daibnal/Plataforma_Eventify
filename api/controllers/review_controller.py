from fastapi import APIRouter, HTTPException
from api.models.review_evaluacion import ReviewEvaluacion
from api.services.review_service import listar_reviews, agregar_review

router = APIRouter(prefix="/reviews", tags=["Reseñas"])

@router.get("/")
def obtener_reviews():
    return listar_reviews()

@router.post("/")
def crear_review(review: ReviewEvaluacion):
    if review.calificacion < 0 or review.calificacion > 5:
        raise HTTPException(status_code=400, detail="La calificación debe estar entre 0 y 5")
    resultado = agregar_review(review)
    if not resultado:
        raise HTTPException(status_code=404, detail="Usuario o evento no encontrado")
    return resultado