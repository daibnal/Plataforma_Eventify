from pydantic import BaseModel

class OrdenCompra(BaseModel):
    run: str
    dv: str
    codigo_evento: str
    total: int