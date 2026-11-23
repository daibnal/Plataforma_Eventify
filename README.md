# Plataforma Eventify Global — Sistema Backend NoSQL 

> **Caso Semestral de Bases de Datos No Relacionales** | **Carrera:** Ingeniería en Informática (Duoc UC)
> **Autores:** Dairys Bernal, Amaru Burdiles, Florencia Soto

---

## 1. Resumen Ejecutivo del Proyecto
**Eventify Global** enfrentaba cuellos de botella críticos de rendimiento y bloqueos de concurrencia en su infraestructura relacional heredada al momento de enfrentar picos de tráfico masivo (conciertos de alta demanda y campañas de ventas). Este repositorio documenta la migración integral hacia una arquitectura orientada a documentos en **MongoDB**, redefiniendo el diseño de esquemas, validaciones estrictas y una batería completa de consultas analíticas avanzadas (*Aggregation Framework*).

---

# Plataforma Eventify: API + dashboard

Aplicación de referencia para analizar una plataforma de gestión y venta de entradas de eventos (**Eventify**) sobre **MongoDB Atlas**. La arquitectura separa totalmente la visualización del acceso a datos

`MongoDB Atlas <--> FastAPI (agregaciones y reglas de negocio) <--> Streamlit`

Streamlit no tiene dependencia de `pymongo`, URI ni credenciales de Atlas: solo consulta la API HTTP. De esta forma se puede reemplazar Streamlit por otra herramienta de BI sin modificar la capa de datos.

## Objetivo
Mostrar cómo diseñar APIs orientadas a analítica y operación sobre MongoDB, integrando operaciones CRUD, consultas de agregación avanzadas y un dashboard interactivo.

## Colecciones
- `usuarios`: datos de usuarios de la plataforma.
- `eventos`: datos de eventos, ubicaciones y tickets.
- `ordenes_compra`: datos de órdenes de compra de entradas.
- `review_evaluaciones`: datos de las reseñas y calificaciones de parte de los usuarios.

## Estructura del proyecto
```text
Plataforma_Eventify/
├── .env                   variables de entorno (no subir a Git)
├── .venv/                 entorno virtual (ignorado por Git)
├── api/
│   ├── controllers/
│   │   ├── dashboard_controller.py
│   │   ├── evento_controller.py
│   │   ├── orden_controller.py
│   │   ├── review_controller.py
│   │   └── usuario_controller.py
│   ├── models/
│   │   ├── evento.py
│   │   ├── orden_compra.py
│   │   ├── review_evaluacion.py
│   │   └── usuario.py
│   ├── services/
│   │   ├── dashboard_service.py
│   │   ├── evento_service.py
│   │   ├── orden_service.py
│   │   ├── review_service.py
│   │   └── usuario_service.py
│   ├── utils/
│   │   └── serializer.py
│   ├── app.py
│   └── database.py
├── Codigo_ver1/
│   ├── init.db.js
│   └── solucion.mongodb.js
├── dashboard/
│   └── app.py
├── Documentacion_ver1/
├── requirements.txt
└── README.md
```

## Inicio rápido
Se requiere Python 3.10 o superior.

1. Cree y active el entorno virtual:
```
  py -m venv .venv
  .\.venv\Scripts\Activate.ps1
```

2. Instale dependencias:
```
pip install -r requirements.txt
```

3. Cree el archivo .env en la raíz del proyecto y complete MONGO_URI y DATABASE_NAME. No suba ese archivo al repositorio:
```
MONGO_URI=mongodb+srv://<usuario>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority
DATABASE_NAME=<nombre_de_tu_base_de_datos>
```
4. Ejecute la API:
```
uvicorn api.app:app --reload --port 8000
```

5. En otra terminal (con el entorno virtual activo), ejecute el dashboard:
```
streamlit run dashboard/app.py
```

La documentación interactiva queda disponible en http://127.0.0.1:8000/docs y el dashboard en http://localhost:8501.

## Endpoints CRUD expuestos (/api/v1)

| Método | Ruta | Descripción |
| :--- | :--- | :--- |
| GET | /api/v1/eventos/ | Lista todos los eventos |
| GET | /api/v1/eventos/ciudad/{ciudad} | Filtra eventos por ciudad |
| GET | /api/v1/eventos/{codigo} | Busca un evento por su código |
| POST | /api/v1/eventos/ | Crea un nuevo evento |
| PUT | /api/v1/eventos/{codigo} | Actualiza un evento existente |
| DELETE | /api/v1/eventos/{codigo} | Elimina un evento por su código |

## Endpoints analíticos expuestos (/api/v1)

| Método | Ruta | Consulta / KPI |
| :--- | :--- | :--- |
| GET | /api/v1/kpis | Consolidado de los 3 KPIs de negocio |
| GET | /api/v1/consultas/compras-usuario/{run} | Consulta 1: detalle de compras de un usuario en una ciudad ($lookup + $unwind) |
| GET | /api/v1/consultas/gasto-por-ciudad | Consulta 1: gasto total por usuario y ciudad para visualización |
| GET | /api/v1/consultas/reporte-ventas | Consulta 2: recaudación, ocupación vs. stock inicial y clasificación ("Exitoso" / "Por Mejorar") |
| GET | /api/v1/consultas/eventos-futuros | Consulta 3: eventos futuros en una ciudad con tickets disponibles bajo un monto máximo |
| GET | /api/v1/consultas/calidad-precio | Consulta 4: consulta libre con $lookup (subpipeline), $addFields y $switch sobre precio promedio y calificación |

## Justificación de los 3 KPIs de negocio

| KPI | Justificación |
| :--- | :--- |
| Ocupación de eventos activos | Permite medir qué porcentaje del stock inicial de tickets ya se ha vendido en eventos activos para detectar oportunidades de venta o baja convocatoria |
| Gasto promedio por orden | Refleja el monto promedio gastado por orden de compra (junto al total recaudado) para evaluar el valor medio por transacción en la plataforma |
| Calificación promedio | Resume la satisfacción general de los asistentes a partir de las reseñas registradas como indicador de calidad del servicio |
