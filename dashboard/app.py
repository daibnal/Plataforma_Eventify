import os
from datetime import datetime, time
import pandas as pd
import plotly.express as px
import requests
import streamlit as st

st.set_page_config(
    page_title="Eventify | Analytics & Operaciones",
    page_icon="🎟️",
    layout="wide",
)

API_BASE_URL = os.getenv("EVENTIFY_API_URL", "http://127.0.0.1:8000/api/v1")

ENDPOINTS = {
    "kpis": f"{API_BASE_URL}/kpis",
    "gasto_ciudad": f"{API_BASE_URL}/consultas/gasto-por-ciudad",
    "compras_usuario": f"{API_BASE_URL}/consultas/compras-usuario",
    "reporte_ventas": f"{API_BASE_URL}/consultas/reporte-ventas",
    "eventos_futuros": f"{API_BASE_URL}/consultas/eventos-futuros",
    "calidad_precio": f"{API_BASE_URL}/consultas/calidad-precio",
    "eventos": f"{API_BASE_URL}/eventos/",
    "evento_item": f"{API_BASE_URL}/eventos",
}


@st.cache_data(ttl=15)
def api_get(url: str, params: dict | None = None):
    try:
        resp = requests.get(url, params=params, timeout=10)
        if resp.status_code == 404:
            detail = resp.json().get("detail", "No se encontraron registros.")
            return None, detail
        resp.raise_for_status()
        return resp.json(), None
    except requests.RequestException as exc:
        return None, f"Error de conexión con la API: {exc}"


def formato_clp(valor: float | int) -> str:
    return f"${valor:,.0f}".replace(",", ".")


# =========================================================
# ENCABEZADO Y BARRA LATERAL
# =========================================================
st.title("Eventify — Plataforma de Analítica y Gestión")
st.caption("Arquitectura desacoplada: Streamlit → FastAPI → MongoDB Atlas")

with st.sidebar:
    st.header("Control de Datos")
    if st.button("Refrescar datos desde API", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    st.markdown(f"**Endpoint base:** `{API_BASE_URL}`")

# =========================================================
# TARJETAS DE INDICADORES CLAVE DE NEGOCIO (KPI CARDS)
# =========================================================
st.subheader("1. Indicadores Clave de Negocio (KPIs)")
kpis, kpi_err = api_get(ENDPOINTS["kpis"])

col_k1, col_k2, col_k3 = st.columns(3)
if kpi_err or not isinstance(kpis, dict):
    st.error(kpi_err or "No fue posible obtener los KPIs desde la API.")
    col_k1.metric("Ocupación Eventos Activos", "—")
    col_k2.metric("Gasto Promedio por Orden", "—")
    col_k3.metric("Calificación Promedio", "—")
else:
    col_k1.metric(
        label="Ocupación Eventos Activos",
        value=f"{kpis.get('ocupacion_eventos_activos', 0)}%",
        help="Tickets vendidos sobre stock inicial en eventos activos",
    )
    col_k2.metric(
        label="Gasto Promedio por Orden",
        value=formato_clp(kpis.get("gasto_promedio_orden", 0)),
        delta=f"Recaudado: {formato_clp(kpis.get('total_recaudado', 0))}",
        delta_color="off",
    )
    col_k3.metric(
        label="Calificación Promedio Reseñas",
        value=f"{kpis.get('calificacion_promedio', 0)} / 5.0",
        help="Promedio general de review_evaluaciones",
    )

st.divider()

# =========================================================
# 2. SECCIÓN DE CONSULTAS ANALÍTICAS 
# =========================================================
st.subheader("2. Consultas Analíticas Avanzadas")

tab1, tab2, tab3, tab4 = st.tabs([
    "Consulta 1: Gasto por Usuario y Ciudad",
    "Consulta 2: Ventas y Ocupación",
    "Consulta 3: Eventos Futuros",
    "Consulta 4: Calidad vs. Precio",
])

# --- CONSULTA 1 ---
with tab1:
    st.markdown("#### Distribución del gasto total de usuarios por ciudad (`$lookup` + `$unwind`)")
    data_c1, err_c1 = api_get(ENDPOINTS["gasto_ciudad"])
    if err_c1:
        st.warning(err_c1)
    elif data_c1:
        df1 = pd.DataFrame(data_c1)
        fig1 = px.bar(
            df1,
            x="ciudad",
            y="gasto_total",
            color="nombre_usuario",
            barmode="group",
            text_auto=True,
            hover_data=["compras"],
            labels={
                "ciudad": "Ciudad",
                "gasto_total": "Gasto Total ($)",
                "nombre_usuario": "Usuario",
                "compras": "Cantidad de Compras",
            },
            title="Gasto Total por Usuario y Ciudad",
        )
        st.plotly_chart(fig1, use_container_width=True)
        st.dataframe(df1, use_container_width=True, hide_index=True)
    else:
        st.info("No hay registros de compras por ciudad.")

    with st.expander("Consultar detalle de compras por RUN de usuario"):
        c1_f1, c1_f2, c1_f3, c1_f4 = st.columns([2, 1, 2, 1])
        run_in = c1_f1.text_input("RUN (sin puntos ni guión)", placeholder="12345678")
        dv_in = c1_f2.text_input("DV", placeholder="9", max_chars=1)
        ciudad_in = c1_f3.text_input("Ciudad", value="Santiago", key="c1_ciudad")
        buscar_u = c1_f4.button("Buscar", use_container_width=True)

        if buscar_u and run_in and dv_in:
            res_u, err_u = api_get(
                f"{ENDPOINTS['compras_usuario']}/{run_in.strip()}",
                params={"dv": dv_in.strip(), "ciudad": ciudad_in.strip()},
            )
            if err_u:
                st.warning(err_u)
            elif res_u:
                info_u = res_u[0]
                st.success(
                    f"**{info_u['nombre_usuario']}** ({info_u['correo']}) — "
                    f"Gasto total en {info_u['ciudad']}: **{formato_clp(info_u['gasto_total'])}**"
                )
                st.dataframe(
                    pd.DataFrame(info_u.get("compras_desglosadas", [])),
                    use_container_width=True,
                    hide_index=True,
                )

# --- CONSULTA 2 ---
with tab2:
    st.markdown("#### Recaudación, ocupación y clasificación de rendimiento por evento")
    data_c2, err_c2 = api_get(ENDPOINTS["reporte_ventas"])
    if err_c2:
        st.warning(err_c2)
    elif data_c2:
        df2 = pd.DataFrame(data_c2)
        c2_g1, c2_g2 = st.columns(2)

        with c2_g1:
            fig2_rec = px.bar(
                df2,
                x="titulo",
                y="total_recaudado",
                color="rendimiento",
                color_discrete_map={"Exitoso": "#2ecc71", "Por Mejorar": "#e67e22"},
                hover_data=["codigo", "tipo", "tickets_vendidos", "stock_total"],
                labels={
                    "titulo": "Evento",
                    "total_recaudado": "Total Recaudado ($)",
                    "rendimiento": "Clasificación",
                },
                title="Recaudación Total por Evento",
            )
            st.plotly_chart(fig2_rec, use_container_width=True)

        with c2_g2:
            fig2_ocu = px.bar(
                df2,
                x="titulo",
                y="ptje_ocupacion",
                color="rendimiento",
                color_discrete_map={"Exitoso": "#2ecc71", "Por Mejorar": "#e67e22"},
                text="ptje_ocupacion",
                labels={
                    "titulo": "Evento",
                    "ptje_ocupacion": "Ocupación (%)",
                    "rendimiento": "Clasificación",
                },
                title="Porcentaje de Ocupación vs. Meta (60%)",
            )
            fig2_ocu.add_hline(y=60, line_dash="dash", line_color="gray", annotation_text="Umbral Exitoso (60%)")
            st.plotly_chart(fig2_ocu, use_container_width=True)

        st.dataframe(df2, use_container_width=True, hide_index=True)
    else:
        st.info("No hay datos de ventas disponibles.")

# --- CONSULTA 3 ---
with tab3:
    st.markdown("#### Disponibilidad de tickets en eventos futuros por ciudad y precio máximo")
    c3_col1, c3_col2 = st.columns(2)
    ciudad_c3 = c3_col1.text_input("Ciudad del evento", value="Santiago", key="c3_ciudad")
    monto_c3 = c3_col2.number_input(
        "Precio máximo del ticket ($)",
        min_value=1000,
        value=30000,
        step=1000,
    )

    data_c3, err_c3 = api_get(
        ENDPOINTS["eventos_futuros"],
        params={"ciudad": ciudad_c3.strip(), "monto": int(monto_c3)},
    )
    if err_c3:
        st.warning(err_c3)
    elif data_c3:
        df3 = pd.DataFrame(data_c3)
        st.dataframe(df3, use_container_width=True, hide_index=True)
        fig3 = px.bar(
            df3,
            x="titulo",
            y="disponibles",
            color="ticket",
            barmode="group",
            hover_data=["precio", "zona", "fecha_inicio"],
            labels={
                "titulo": "Evento",
                "disponibles": "Tickets Disponibles",
                "ticket": "Tipo de Ticket",
            },
            title=f"Tickets Disponibles en {ciudad_c3} bajo {formato_clp(monto_c3)}",
        )
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info(f"No hay eventos futuros en {ciudad_c3} con tickets menores a {formato_clp(monto_c3)}.")

# --- CONSULTA 4 ---
with tab4:
    st.markdown("#### Consulta Libre: Relación entre Precio Promedio y Calificación (`$lookup` + `$switch`)")
    precio_alto_in = st.slider(
        "Umbral de precio considerado alto ($)",
        min_value=5000,
        max_value=100000,
        value=20000,
        step=5000,
    )
    data_c4, err_c4 = api_get(
        ENDPOINTS["calidad_precio"],
        params={"precio_alto": int(precio_alto_in)},
    )
    if err_c4:
        st.warning(err_c4)
    elif data_c4:
        df4 = pd.DataFrame(data_c4)
        fig4 = px.scatter(
            df4,
            x="precio_promedio",
            y="calificacion_promedio",
            size="total_reviews",
            color="relacion",
            hover_name="titulo",
            hover_data=["codigo", "tipo", "total_reviews"],
            color_discrete_map={
                "Bien evaluado": "#2ecc71",
                "Regular": "#3498db",
                "Riesgo: caro y mal evaluado": "#e74c3c",
            },
            labels={
                "precio_promedio": "Precio Promedio Ticket ($)",
                "calificacion_promedio": "Calificación Promedio (1-5)",
                "relacion": "Diagnóstico",
                "total_reviews": "Total Reseñas",
            },
            title="Matriz Calidad vs. Precio por Evento",
        )
        fig4.update_yaxes(range=[0, 5.5])
        st.plotly_chart(fig4, use_container_width=True)
        st.dataframe(df4, use_container_width=True, hide_index=True)
    else:
        st.info("No hay eventos con reseñas para evaluar calidad vs. precio.")

st.divider()

# =========================================================
# 3. PANEL DE ADMINISTRACIÓN Y OPERACIONES (CRUD EVENTOS)
# =========================================================
st.subheader("3. Panel de Administración de Eventos (CRUD vía API)")

eventos_raw, eventos_err = api_get(ENDPOINTS["eventos"])
if eventos_err:
    st.warning(eventos_err)
    codigos_existentes = []
else:
    if eventos_raw:
        df_ev = pd.DataFrame(eventos_raw)
        cols_vista = [c for c in ["codigo", "titulo", "tipo", "capacidad", "fecha_hora_ini", "activo"] if c in df_ev.columns]
        if "ubicacion" in df_ev.columns:
            df_ev["ciudad"] = df_ev["ubicacion"].apply(lambda u: u.get("ciudad") if isinstance(u, dict) else "")
            cols_vista.append("ciudad")
        st.dataframe(df_ev[cols_vista], use_container_width=True, hide_index=True)
        codigos_existentes = df_ev["codigo"].tolist() if "codigo" in df_ev.columns else []
    else:
        st.info("No hay eventos registrados.")
        codigos_existentes = []

crud_post, crud_put, crud_delete = st.tabs([
    "➕ Registrar Nuevo Evento (POST)",
    "✏️ Actualizar Evento (PUT)",
    "🗑️ Eliminar Evento (DELETE)",
])

# --- POST ---
with crud_post:
    with st.form("form_crear_evento", clear_on_submit=True):
        st.markdown("**Datos Generales del Evento**")
        r1_c1, r1_c2, r1_c3 = st.columns(3)
        codigo = r1_c1.text_input("Código único*", placeholder="EVT-099")
        titulo = r1_c2.text_input("Título*", placeholder="Festival Indie Concepción")
        tipo = r1_c3.selectbox("Tipo*", ["Concierto", "Festival", "Teatro", "Conferencia", "Deportivo", "Otro"])

        descripcion = st.text_area("Descripción*", placeholder="Descripción breve del evento...")

        r2_c1, r2_c2, r2_c3, r2_c4 = st.columns(4)
        capacidad = r2_c1.number_input("Capacidad total*", min_value=1, value=200, step=10)
        fecha_ini = r2_c2.date_input("Fecha inicio*")
        hora_ini = r2_c3.time_input("Hora inicio*", value=time(20, 0))
        activo = r2_c4.checkbox("Evento activo", value=True)

        r3_c1, r3_c2 = st.columns(2)
        fecha_fin = r3_c1.date_input("Fecha término*")
        hora_fin = r3_c2.time_input("Hora término*", value=time(23, 30))

        st.markdown("**Ubicación**")
        u_c1, u_c2, u_c3, u_c4 = st.columns(4)
        pais = u_c1.text_input("País*", value="Chile")
        ciudad = u_c2.text_input("Ciudad*", value="Concepción")
        calle = u_c3.text_input("Calle*", placeholder="Av. O'Higgins")
        n_calle = u_c4.number_input("N° Calle*", min_value=1, value=100)

        coord_c1, coord_c2 = st.columns(2)
        lon = coord_c1.number_input("Longitud", value=-73.0498, format="%.4f")
        lat = coord_c2.number_input("Latitud", value=-36.8270, format="%.4f")

        st.markdown("**Ticket Inicial**")
        t_c1, t_c2, t_c3, t_c4 = st.columns(4)
        t_tipo = t_c1.text_input("Tipo ticket*", value="General")
        t_precio = t_c2.number_input("Precio ($)*", min_value=0, value=15000, step=1000)
        t_stock = t_c3.number_input("Stock inicial*", min_value=1, value=200, step=10)
        t_zona = t_c4.text_input("Zona*", value="Platea")

        submit_post = st.form_submit_button("Crear Evento")
        if submit_post:
            if not (codigo and titulo and descripcion and calle):
                st.error("Completa todos los campos obligatorios marcados con *.")
            else:
                dt_ini = datetime.combine(fecha_ini, hora_ini).isoformat()
                dt_fin = datetime.combine(fecha_fin, hora_fin).isoformat()
                payload = {
                    "codigo": codigo.strip(),
                    "titulo": titulo.strip(),
                    "tipo": tipo,
                    "descripcion": descripcion.strip(),
                    "capacidad": int(capacidad),
                    "fecha_hora_ini": dt_ini,
                    "fecha_hora_fin": dt_fin,
                    "activo": activo,
                    "ubicacion": {
                        "pais": pais.strip(),
                        "ciudad": ciudad.strip(),
                        "calle": calle.strip(),
                        "n_calle": int(n_calle),
                        "coordenadas": [float(lon), float(lat)],
                    },
                    "tickets": [
                        {
                            "tipo": t_tipo.strip(),
                            "precio": int(t_precio),
                            "stock_ini": int(t_stock),
                            "disponibles": int(t_stock),
                            "zona": t_zona.strip(),
                        }
                    ],
                }
                try:
                    res = requests.post(ENDPOINTS["eventos"], json=payload, timeout=10)
                    if res.status_code >= 400:
                        st.error(f"Error {res.status_code}: {res.json().get('detail', res.text)}")
                    else:
                        st.cache_data.clear()
                        st.success(f"Evento {codigo} creado exitosamente.")
                        st.rerun()
                except requests.RequestException as exc:
                    st.error(f"Error al conectar con la API: {exc}")

# --- PUT ---
with crud_put:
    with st.form("form_editar_evento"):
        if codigos_existentes:
            cod_put = st.selectbox("Selecciona código del evento", codigos_existentes)
        else:
            cod_put = st.text_input("Código del evento a modificar")

        nuevo_titulo = st.text_input("Nuevo título*")
        nueva_capacidad = st.number_input("Nueva capacidad*", min_value=1, value=250, step=10)
        submit_put = st.form_submit_button("Guardar Cambios")

        if submit_put:
            if not (cod_put and nuevo_titulo):
                st.error("Debes indicar el código y el nuevo título.")
            else:
                payload_put = {
                    "titulo": nuevo_titulo.strip(),
                    "capacidad": int(nueva_capacidad),
                }
                try:
                    res = requests.put(
                        f"{ENDPOINTS['evento_item']}/{cod_put.strip()}",
                        json=payload_put,
                        timeout=10,
                    )
                    if res.status_code >= 400:
                        st.error(f"Error {res.status_code}: {res.json().get('detail', res.text)}")
                    else:
                        st.cache_data.clear()
                        st.success(res.json().get("mensaje", "Evento actualizado."))
                        st.rerun()
                except requests.RequestException as exc:
                    st.error(f"Error al conectar con la API: {exc}")

# --- DELETE ---
with crud_delete:
    with st.form("form_eliminar_evento"):
        if codigos_existentes:
            cod_del = st.selectbox("Selecciona código del evento a eliminar", codigos_existentes, key="del_select")
        else:
            cod_del = st.text_input("Código del evento a eliminar", key="del_text")

        submit_del = st.form_submit_button("Eliminar Evento")

        if submit_del and cod_del:
            try:
                res = requests.delete(f"{ENDPOINTS['evento_item']}/{cod_del.strip()}", timeout=10)
                if res.status_code >= 400:
                    st.error(f"Error {res.status_code}: {res.json().get('detail', res.text)}")
                else:
                    st.cache_data.clear()
                    st.success(res.json().get("mensaje", "Evento eliminado."))
                    st.rerun()
            except requests.RequestException as exc:
                st.error(f"Error al conectar con la API: {exc}")