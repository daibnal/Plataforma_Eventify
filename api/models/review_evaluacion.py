from pydantic import BaseModel

class ReviewEvaluacion(BaseModel):
    run: str
    dv: str
    codigo_evento: str
    calificacion: int
    comentario: str