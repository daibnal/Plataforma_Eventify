# Plataforma Eventify Global — Sistema Backend NoSQL 

> **Caso Semestral de Bases de Datos No Relacionales** | **Carrera:** Ingeniería en Informática (Duoc UC)
> **Autores:** Dairys Bernal, Amaru Burdiles, Florencia Soto

---

## 1. Resumen Ejecutivo del Proyecto
**Eventify Global** enfrentaba cuellos de botella críticos de rendimiento y bloqueos de concurrencia en su infraestructura relacional heredada al momento de enfrentar picos de tráfico masivo (conciertos de alta demanda y campañas de ventas). Este repositorio documenta la migración integral hacia una arquitectura orientada a documentos en **MongoDB**, redefiniendo el diseño de esquemas, validaciones estrictas y una batería completa de consultas analíticas avanzadas (*Aggregation Framework*).

---

## 2. Arquitectura de Datos y Decisiones de Modelado

Para optimizar los patrones de lectura y escritura bajo alta concurrencia, se estructuró la base de datos `no-sql-ev2` en **4 colecciones principales**:

### A. Colecciones y Estrategias de Almacenamiento
* **`usuarios`**: Almacena clientes y administradores bajo un **documento plano** con validación estricta de RUN, DV y correo electrónico.
* **`eventos`**: Colección central que implementa el **patrón de embebido** para *ubicación* y *tickets*. Esto permite que la ficha de un evento se recupere en **una sola lectura atómica**, eliminando `JOINs` costosos.
* **`ordenes_compra`**: Registro transaccional vinculado mediante **referencias (`ObjectId`)** hacia usuarios y eventos, garantizando escalabilidad ante escrituras masivas concurrentes.
* **`review_evaluaciones`**: Almacena calificaciones (0-5) y comentarios mediante **referencias (`ObjectId`)**, permitiendo análisis de satisfacción independientes.

### B. Principio de Diseño Aplicado
> *"Se embebe lo que se lee junto, es acotado y cambia poco. Se referencia lo que crece sin límite, se escribe constantemente y se consulta por sí mismo."*

---

## 3. Implementación de la Batería de Consultas Analíticas

El motor de agregación de MongoDB resuelve los requerimientos analíticos complejos del negocio de la siguiente manera:

1. **Consulta 1 — Detalle de Compras por Usuario:** 
   * *Mecanismo:* Uso de `$lookup` sucesivos y `$unwind` para cruzar la identidad del usuario con sus órdenes de compra y los eventos asociados, filtrando por ciudad y calculando el gasto total acumulado mediante `$group` y `$sum`.
2. **Consulta 2 — Reporte de Ventas por Evento:** 
   * *Mecanismo:* Procesamiento puramente interno sobre arreglos embebidos (`$addFields`, `$map`) sin requerir `JOINs`. Calcula el total recaudado, los tickets vendidos y el porcentaje de ocupación, asignando etiquetas automáticas de rendimiento (*"Exitoso"* o *"Por Mejorar"*) vía `$cond`.
3. **Consulta 3 — Eventos Futuros con Oferta de Tickets:** 
   * *Mecanismo:* Filtrado temporal estricto usando la variable del sistema `$$NOW`, validación geográfica y uso clave de `$elemMatch` para asegurar que un mismo tipo de ticket cumpla simultáneamente con stock disponible y precio bajo el umbral, proyectando solo los elementos filtrados con `$filter`.
4. **Consulta 4 — Relación Precio-Satisfacción (Elemento Diferenciador):** 
   * *Mecanismo:* Cruce analítico con `review_evaluaciones` para evaluar la percepción del cliente frente al costo. Emplea operadores `$avg` directos sobre subdocumentos y protege contra divisiones por cero con `$size` y `$cond`, devolviendo etiquetas semánticas claras (*"Sin evaluaciones"*).

---

## 4. Scripts de Inicialización y Carga (Seed Data)

El repositorio incluye la automatización completa para la creación de esquemas y población masiva de datos de prueba (más de 50 documentos validados por colección):

* **Definición de Esquemas y Validaciones (`$jsonSchema`):** `solucion.mongodb.js`
* **Generación de Datos de Prueba (Seed):** `init.db.js`

### Instrucciones de Ejecución en MongoDB Shell / Compass:
```javascript
// 1. Crear colecciones y reglas de validación estricta
load("solucion.mongodb.js");

// 2. Ejecutar la carga masiva de datos de prueba (Seed)
load("init.db.js");
