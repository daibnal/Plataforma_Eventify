/*=====================================
        Definición de colecciones
======================================*/

use("no-sql-ev2");

/* USUARIOS ------------------------
Almacena información de clientes. */
db.createCollection("usuarios", {
	validator: {
		$jsonSchema: {
			bsonType: "object",
			required: ["run", "dv", "nombre", "apellido", "correo", "telefono", "fecha_nacimiento", "es_vip"],
			properties: {
				run: {
					bsonType: "string",
					pattern: "^[1-9][0-9]{6,7}$",
					description: "'run' debe ser numérico sin puntos, de 7 a 8 dígitos y no iniciar con 0"
				},
				dv: {
					bsonType: "string",
					pattern: "^[0-9kK]$",
					description: "'dv' debe ser un solo carácter (0-9 o k/K)"
				},
				nombre: { bsonType: "string" },
				apellido: { bsonType: "string" },
				correo: {
					bsonType: "string",
					pattern: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
				},
				telefono: { bsonType: "string" },
				fecha_nacimiento: { bsonType: "date" },
				es_vip: { bsonType: "bool" }
			}
		}
	}
});

/* EVENTOS -------------------------------------------------------------
Almacena el catálogo de eventos, recintos y configuración de tickets. */
db.createCollection("eventos", {
	validator: {
		$jsonSchema: {
			bsonType: "object",
			required: ["codigo", "titulo", "tipo", "capacidad", "fecha_hora_ini", "fecha_hora_fin", "activo"],
			properties: {
				codigo: { bsonType: "string" },
				titulo: { bsonType: "string" },
				tipo: { bsonType: "string" },
				descripcion: { bsonType: "string" },
				capacidad: { bsonType: "int", minimum: 1 },
				fecha_hora_ini: { bsonType: "date" },
				fecha_hora_fin: { bsonType: "date" },
				activo: { bsonType: "bool" },

				// Tabla ubicación embebida
				ubicacion: {
					bsonType: "object",
					description: "'ubicacion' debe ser un objeto",
					required: ["pais", "ciudad", "calle", "n_calle", "coordenadas"],
					properties: {
						pais: { bsonType: "string" },
						ciudad: { bsonType: "string" },
						calle: { bsonType: "string" },
						n_calle: { bsonType: "int", minimum: 0 },
						coordenadas: {
							bsonType: "array",
							description: "'coordenadas' es un arreglo de 2 números (longitud, latitud)",
							minItems: 2,
							maxItems: 2,
							items: {
								bsonType: ["double", "int"]
							}
						},
						detalle: { bsonType: "string" }
					}
				},
				// Tabla ticket embebida
				tickets: {
					bsonType: "array",
					description: "'tickets' debe ser un arreglo de objetos",
					items: {
						bsonType: "object",
						required: ["tipo", "precio", "stock_ini", "disponibles"],
						properties: {
							tipo: { bsonType: "string" },
							precio: { bsonType: ["double", "int"], minimum: 0 },
							stock_ini: { bsonType: "int", minimum: 0 },
							disponibles: { bsonType: "int", minimum: 0 },
							zona: { bsonType: "string" }
						}
					}
				}
			}
		}
	}
});

/* ORDENES DE COMPRA -----------------------------------------
Almacena el registro de transacciones y compras realizadas. */
db.createCollection("ordenes_compra", {
	validator: {
		$jsonSchema: {
			bsonType: "object",
			required: ["usuario_id", "evento_id", "total", "fecha"],
			properties: {
				// Claves "foraneas" obligatorias
				usuario_id: { bsonType: ["objectId"] },
				evento_id: { bsonType: ["objectId"] },

				// Demás campos
				total: { bsonType: ["double", "int"], minimum: 0 },
				fecha: { bsonType: "date" }
			}
		}
	}
});

/* Reseñas y Evaluaciones ----------------------------------------------------------------
Almacena calificaciones y comentarios dejados por los asistentes a eventos finalizados. */
db.createCollection("review_evaluaciones", {
	validator: {
		$jsonSchema: {
			bsonType: "object",
			required: ["usuario_id", "evento_id", "calificacion"],
			properties: {
				// Claves "foraneas" obligatorias
				usuario_id: { bsonType: ["objectId"] },
				evento_id: { bsonType: ["objectId"] },

				// Demás campos
				calificacion: { bsonType: "int", minimum: 0, maximum: 5 },
				comentario: { bsonType: "string" }
			}
		}
	}
});

/*======================================
    Batería de consultas avanzadas
=======================================*/

/*-------------------------------------
    CONSULTA 1: $lookup + $unwind
---------------------------------------
Obtiene el detalle de compras de un usuario, uniendo datos de la orden con los datos del
evento correspondiente, desglosando los elementos comprados y proyectando el gasto total en
eventos de una ciudad especı́fica. */

/* INICIALIZACION PARAMETROS DE BUSQUEDA
Reemplace el run, dv y ciudad a filtrar */
const p_run_filtro = "21684030";
const p_dv_filtro = "5";
let p_ciudad_filtro = "Santiago";

use("no-sql-ev2");
db.usuarios.aggregate([
	{
		// Filtrar el usuario por su RUN
		$match: {
			run: p_run_filtro,
			dv: p_dv_filtro
		}
	},
	{
		// JOIN usuarios u -> ordenes_compra o ON(u._id = o.usuario_id)
		$lookup: {
			from: "ordenes_compra",
			localField: "_id",
			foreignField: "usuario_id",
			as: "ordenes"
		}
	},

	// Extrae cada orden individual de la lista ordenes en forma de objeto
	{ $unwind: "$ordenes" },
	{
		// JOIN ordenes_compra o -> eventos e ON(o.evento_id = e._id)
		$lookup: {
			from: "eventos",
			localField: "ordenes.evento_id",
			foreignField: "_id",
			as: "evento_info"
		}
	},

	// Extrae cada evento de la lista evento_info
	{ $unwind: "$evento_info" },
	{
		// Filtrar los eventos por ciudad
		$match: {
			"evento_info.ubicacion.ciudad": p_ciudad_filtro
		}
	},
	{
		// GROUPBY u._id, u.nombre ||" "|| u.apellido "nombre_usuario", u.correo, e.ciudad...
		$group: {
			_id: "$_id",
			nombre_usuario: { $first: { $concat: ["$nombre", " ", "$apellido"] } },
			correo: { $first: "$correo" },
			ciudad: { $first: "$evento_info.ubicacion.ciudad" },
			gasto_total: { $sum: "$ordenes.total" },
			compras_desglosadas: {
				$push: {
					orden_id: "$ordenes._id",
					evento: "$evento_info.titulo",
					codigo: "$evento_info.codigo",
					tipo: "$evento_info.tipo",
					fecha_compra: "$ordenes.fecha",
					monto: "$ordenes.total"
				}
			}
		}
	},
	{
		// SELECT u.nombre ||" "|| u.apellido "nombre_usuario", u.correo, e.ciudad...
		$project: {
			_id: 0,
			nombre_usuario: 1,
			correo: 1,
			ciudad: 1,
			gasto_total: 1,
			compras_desglosadas: 1
		}
	}
]);

/* ------------------------------------
    CONSULTA 2: Pipeline de reporte
---------------------------------------
Generar un reporte de ventas por evento que incluya: total recaudado, cantidad de
tickets vendidos, porcentaje de ocupación/venta respecto al stock inicial (embebido)
y una etiqueta proyectada ( "Exitoso" o "Por Mejorar" ) según el rendimiento. */
use("no-sql-ev2");
db.eventos.aggregate([
	{
		// Crea campos temporales para almacenar y reutilizar calculos
		$addFields: {
			stock_total: { $sum: "$tickets.stock_ini" },
			stock_restante: { $sum: "$tickets.disponibles" },

			// Recaudación por ticket -> (stock_ini - disponibles) * precio
			// lista de subtotales -> [1030, 46500, 70990, 35000...]
			subtotales_tickets: {
				$map: {
					// For t IN tickets LOOP...
					input: "$tickets",
					as: "t",
					in: {
						$multiply: [{ $subtract: ["$$t.stock_ini", "$$t.disponibles"] }, "$$t.precio"]
					}
				}
			}
		}
	},
	{
		// Calcula el total recaudado y la cantidad de tickets vendidos
		$addFields: {
			total_recaudado: { $sum: "$subtotales_tickets" },
			tickets_vendidos: { $subtract: ["$stock_total", "$stock_restante"] }
		}
	},
	{
		// Calcular el porcentaje de ocupación; (vendidos / total * 100)
		$addFields: {
			ptje_ocupacion: {
				$cond: {
					// Evita una posible division por cero
					if: { $gt: ["$stock_total", 0] },
					then: {
						$multiply: [{ $divide: ["$tickets_vendidos", "$stock_total"] }, 100]
					},
					else: 0
				}
			}
		}
	},
	{
		// SELECT
		$project: {
			_id: 0,
			codigo: 1,
			titulo: 1,
			tipo: 1,

			total_recaudado: 1,
			tickets_vendidos: 1,
			stock_total: 1,

			// --------------- round(ptje_ocupacion, 2)
			ptje_ocupacion: { $round: ["$ptje_ocupacion", 2] },
			rendimiento: {
				// Calcula el rendimiento
				$cond: {
					// WHEN ptje_ocupacion >= 60 THEN "Existoso"
					if: { $gte: ["$ptje_ocupacion", 60] },
					then: "Exitoso",
					else: "Por Mejorar"
				}
			}
		}
	}
]);

/* ---------------------------------------------------
    CONSULTA 3: Filtrado de Subdocumentos y Fechas
------------------------------------------------------
Buscar eventos futuros en una ciudad determinada que aún tengan disponible un tipo de ticket
con precio inferior a un monto, aplicando proyecciones para ocultar campos innecesarios */

/* INICIALIZACION PARAMETROS DE BUSQUEDA ---
Reemplace por la ciudad y monto a filtrar */
p_ciudad_filtro = "Santiago";
const p_monto_filtro = 10000;

use("no-sql-ev2");
db.eventos.aggregate([
	{
		// Filtra por fecha futura, ciudad y tickets
		$match: {
			$expr: {
				// fecha_evento > SYSDATE
				$gt: ["$fecha_hora_ini", "$$NOW"]
			},
			"ubicacion.ciudad": p_ciudad_filtro,
			tickets: {
				$elemMatch: {
					disponibles: { $gte: 1 },
					precio: { $lt: p_monto_filtro }
				}
			}
		}
	},
	{
		$project: {
			_id: 0,
			titulo: 1,
			tipo_evento: "$tipo",
			descripcion: 1,
			capacidad: 1,
			fecha_inicio: "$fecha_hora_ini",
			fecha_finalizacion: "$fecha_hora_fin",
			calle: "$ubicacion.calle",
			n_calle: "$ubicacion.n_calle",
			coordenadas: "$ubicacion.coordenadas",
			tipos_disponibles: {
				$filter: {
					input: "$tickets",
					as: "t",
					cond: {
						$and: [{ $gte: ["$$t.disponibles", 1] }, { $lt: ["$$t.precio", p_monto_filtro] }]
					}
				}
			}
		}
	}
]);

/* ----------------------------------------
    CONSULTA 4: Elemento Diferenciador
-------------------------------------------
Generar un informe, que, para cada evento muestre el precio promedio de sus tickets y
la calificacion (numero de estrallas) promedia obtenidad */
use("no-sql-ev2");
db.eventos.aggregate([
	{
		// JOIN entre eventos -> reseñas
		$lookup: {
			from: "review_evaluaciones",
			localField: "_id",
			foreignField: "evento_id",
			as: "reviews"
		}
	},
	{
		$project: {
			_id: 0,
			codigo: 1,
			titulo: 1,
			tipo: 1,
			// Calcula el precio promedio de entradas
			precio_promedio_tickets: {
				$round: [{ $avg: "$tickets.precio" }, 2]
			},
			// Calcula la calificacion promedio de eventos
			calificacion_promedio: {
				$cond: {
					// Previene una posible division por cero
					if: { $gt: [{ $size: "$reviews" }, 0] },
					then: { $round: [{ $avg: "$reviews.calificacion" }, 2] },
					else: "Sin evaluaciones"
				}
			}
		}
	}
]);
