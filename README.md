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

## Inicio rápido
Se requiere Python 3.10 o superior.
 Cree y active el entorno virtual:Windows (PowerShell):PowerShellpy -m venv .venv
.\.venv\Scripts\Activate.ps1
Linux / macOS:Bashpython3 -m venv .venv
source .venv/bin/activate
Instale dependencias:Bashpip install -r requirements.txt
