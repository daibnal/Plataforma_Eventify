from datetime import datetime
from pydantic import BaseModel

class Usuario(BaseModel):
    run: str
    dv: str
    nombre: str
    apellido: str
    correo: str
    telefono: str
    fecha_nacimiento: datetime
    es_vip: bool