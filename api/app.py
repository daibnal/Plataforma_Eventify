from fastapi import FastAPI

from api.controllers import (
    usuario_controller, evento_controller,
    orden_controller, review_controller, dashboard_controller
)

tags_metadata = [
    {
        "name": "General",
        "description": "Operaciones generales de la API"
    },
    {
        "name": "Usuarios",
        "description": "Consulta y registro de usuarios"
    },
    {
        "name": "Eventos",
        "description": "CRUD de eventos"
    },
    {
        "name": "Órdenes de compra",
        "description": "Consulta y registro de órdenes de compra"
    },
    {
        "name": "Reseñas",
        "description": "Consulta y registro de reseñas"
    },
    {
        "name": "Dashboard",
        "description": "KPIs y consultas avanzadas de la Evaluación 2"
    }
]

app = FastAPI(
    title="API Eventify",
    version="1.0",
    openapi_tags=tags_metadata
)

API = "/api/v1"

app.include_router(usuario_controller.router, prefix=API)
app.include_router(evento_controller.router, prefix=API)
app.include_router(orden_controller.router, prefix=API)
app.include_router(review_controller.router, prefix=API)
app.include_router(dashboard_controller.router, prefix=API)

@app.get("/", tags=["General"])
def inicio():
    return {"mensaje": "API Eventify funcionando correctamente"}