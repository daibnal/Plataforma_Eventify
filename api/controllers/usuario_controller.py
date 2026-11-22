from fastapi import APIRouter, HTTPException
from api.services.usuario_service import listar_usuarios, buscar_por_run, agregar_usuario
from api.models.usuario import Usuario

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

@router.get("/")
def obtener_usuarios():
    return listar_usuarios()

@router.get("/{run}")
def filtro_por_run(run: str):
    resultado = buscar_por_run(run)
    if not resultado:
        raise HTTPException(
            status_code=404,
            detail=f"No existe un usuario con RUN {run}"
        )

    return resultado

@router.post("/")
def crear_usuario(u: Usuario):
    resultado = agregar_usuario(u)
    if not resultado:
        raise HTTPException(
            status_code=400,
            detail=f"Ya existe un usuario con RUN {u.run}"
        )

    return resultado