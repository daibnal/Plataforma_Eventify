from fastapi import APIRouter, HTTPException, Query
from api.services.dashboard_service import DashboardService

router = APIRouter(tags=["Dashboard"])

@router.get("/kpis")
def get_kpis():
    """Retorna los 3 KPIs del negocio: ocupacion, gasto promedio y calificacion."""
    return DashboardService.get_kpis()

@router.get("/consultas/compras-usuario/{run}")
def get_compras_usuario(run: str, dv: str, ciudad: str = "Santiago"):
    """Consulta 1: detalle de compras de un usuario en una ciudad."""
    resultado = DashboardService.compras_usuario(run, dv, ciudad)
    if not resultado:
        raise HTTPException(
            status_code=404,
            detail=f"Sin compras del RUN {run} en {ciudad}"
        )

    return resultado

@router.get("/consultas/gasto-por-ciudad")
def get_gasto_por_ciudad():
    """Consulta 1 para el grafico: gasto de cada usuario por ciudad."""
    return DashboardService.gasto_usuarios_por_ciudad()

@router.get("/consultas/reporte-ventas")
def get_reporte_ventas():
    """Consulta 2: recaudacion, ocupacion y rendimiento por evento."""
    return DashboardService.reporte_ventas_eventos()

@router.get("/consultas/eventos-futuros")
def get_eventos_futuros(ciudad: str = "Santiago", monto: int = Query(10000, gt=0)):
    """Consulta 3: tickets disponibles en eventos futuros bajo un monto."""
    return DashboardService.eventos_futuros(ciudad, monto)

@router.get("/consultas/calidad-precio")
def get_calidad_precio(precio_alto: int = Query(20000, gt=0)):
    """Consulta 4: relacion entre precio promedio y calificacion por evento."""
    return DashboardService.calidad_vs_precio(precio_alto)