from datetime import datetime
from pydantic import BaseModel

class Ubicacion(BaseModel):
    pais: str
    ciudad: str
    calle: str
    n_calle: int
    coordenadas: list[float]

class Ticket(BaseModel):
    tipo: str
    precio: int
    stock_ini: int
    disponibles: int
    zona: str

class Evento(BaseModel):
    codigo: str
    titulo: str
    tipo: str
    descripcion: str
    capacidad: int
    fecha_hora_ini: datetime
    fecha_hora_fin: datetime
    activo: bool
    ubicacion: Ubicacion
    tickets: list[Ticket]

class EventoCambios(BaseModel):
    titulo: str
    capacidad: int