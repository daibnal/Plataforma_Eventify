<div align="center">

# 🎟️ Eventify Global — Plataforma NoSQL

<img src="https://img.shields.io/badge/Status-Completado-success?style=for-the-badge&logo=none" alt="Status">
<img src="https://img.shields.io/badge/Database-MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white" alt="MongoDB">
<img src="https://img.shields.io/badge/Backend-Spring%20Boot-6DB33F?style=for-the-badge&logo=springboot&logoColor=white" alt="Spring Boot">
<img src="https://img.shields.io/badge/Architecture-Microservices-blue?style=for-the-badge&logo=microservices&logoColor=white" alt="Architecture">

*Modernización de la infraestructura tecnológica para la venta masiva de entradas a eventos, migrando desde un modelo relacional hacia un diseño orientado a documentos en MongoDB[cite: 1, 2].*

</div>

---

## 📌 Contexto del Proyecto

**Eventify Global** experimentaba caídas de rendimiento críticas durante picos de demanda (como lanzamientos de artistas masivos o Cyber Days) debido al alto costo de los `JOINs` en su infraestructura relacional previa[cite: 2]. 

Para solucionar los problemas de concurrencia y bloqueos, se rediseñó la arquitectura de datos implementando **MongoDB**, permitiendo que la unidad de lectura coincida con la unidad de negocio: **la ficha completa de un evento se recupera en una sola lectura atómica**[cite: 2].

---

## 🏗️ Arquitectura y Modelo de Datos

La base de datos `no-sql-ev2` está compuesta por **4 colecciones** con reglas estrictas de validación mediante `$jsonSchema`[cite: 2]:

| Colección | Rol Principal | Patrón Aplicado |
| :--- | :--- | :--- |
| **`usuarios`** | Clientes y administradores del sistema[cite: 2] | Documento plano (Validación estricta de RUN, DV y Correo)[cite: 2, 3] |
| **`eventos`** | Catálogo central, recintos y configuración de entradas[cite: 2] | **Embebido** (Ubicación geográfica y tickets estructurados)[cite: 2, 4] |
| **`ordenes_compra`** | Registro transaccional de compras[cite: 2] | **Referenciado** (`usuario_id`, `evento_id` vía `ObjectId`)[cite: 2, 4] |
| **`review_evaluaciones`** | Calificaciones (0-5) y comentarios post-evento[cite: 2] | **Referenciado** (`usuario_id`, `evento_id` vía `ObjectId`)[cite: 2, 4] |

> **Regla de Diseño:** Se embebe lo que se lee junto, es acotado y cambia poco (ej. *ubicación y tickets de un evento*); se referencia lo que crece sin límite, se escribe masivamente y se consulta de forma independiente (ej. *órdenes de compra y reseñas*)[cite: 4, 5].

---

## 🔍 Batería de Consultas Analíticas

El proyecto incluye un conjunto robusto de consultas avanzadas de agregación (*Aggregation Framework*):

1. **Historial de Compras por Usuario:** Cruce de colecciones (`$lookup`, `$unwind`) para filtrar por RUN y ciudad, calculando el gasto total y desglosando las transacciones[cite: 5].
2. **Reporte de Ventas por Evento:** Procesamiento 100% interno sin uniones, calculando recaudación total, tickets vendidos, porcentaje de ocupación y etiquetado automático (*"Exitoso"* o *"Por Mejorar"*)[cite: 5, 6].
3. **Eventos Futuros con Oferta de Tickets:** Filtrado avanzado usando `$$NOW`, `$elemMatch` y `$filter` para localizar eventos próximos que cumplan con criterios específicos de precio y disponibilidad[cite: 6].
4. **Relación Precio-Satisfacción:** Cruce analítico que contrasta el precio promedio de los tickets (calculado mediante `$avg` directo sobre arreglos embebidos) frente a la calificación promedio de los usuarios[cite: 6, 7].

---

## ⚙️ Configuración y Ejecución

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/tu-usuario/Microservicio_sakura_agenda.git](https://github.com/tu-usuario/Microservicio_sakura_agenda.git)
