from api.database import db

class DashboardService:

    @staticmethod
    def get_kpis():
        """
        Retorna los 3 KPIs del negocio:
        - KPI 1: porcentaje de ocupacion de los eventos activos
        - KPI 2: gasto promedio por orden de compra
        - KPI 3: calificacion promedio de las reseñas
        """
        # KPI 1: tickets vendidos / stock inicial de los eventos activos
        pipeline_ocupacion = [
            {"$match": {"activo": True}},
            {
                "$group": {
                    "_id": None,
                    "stock_total": {"$sum": {"$sum": "$tickets.stock_ini"}},
                    "disponibles": {"$sum": {"$sum": "$tickets.disponibles"}}
                }
            }
        ]
        res_ocupacion = list(db.eventos.aggregate(pipeline_ocupacion))

        # KPI 2: promedio y suma del total de las ordenes
        pipeline_gasto = [
            {
                "$group": {
                    "_id": None,
                    "gasto_promedio": {"$avg": "$total"},
                    "total_recaudado": {"$sum": "$total"}
                }
            }
        ]
        res_gasto = list(db.ordenes_compra.aggregate(pipeline_gasto))

        # KPI 3: promedio de calificacion
        pipeline_calificacion = [
            {
                "$group": {
                    "_id": None,
                    "promedio": {"$avg": "$calificacion"}
                }
            }
        ]
        res_calificacion = list(db.review_evaluaciones.aggregate(pipeline_calificacion))

        ocupacion = 0.0
        if res_ocupacion and res_ocupacion[0]["stock_total"] > 0:
            stock = res_ocupacion[0]["stock_total"]
            vendidos = stock - res_ocupacion[0]["disponibles"]
            ocupacion = vendidos / stock * 100

        gasto_promedio = res_gasto[0]["gasto_promedio"] if res_gasto else 0.0
        total_recaudado = res_gasto[0]["total_recaudado"] if res_gasto else 0
        calificacion = res_calificacion[0]["promedio"] if res_calificacion else 0.0

        return {
            "ocupacion_eventos_activos": round(ocupacion, 2),
            "gasto_promedio_orden": round(gasto_promedio),
            "total_recaudado": total_recaudado,
            "calificacion_promedio": round(calificacion, 2)
        }

    @staticmethod
    def compras_usuario(run: str, dv: str, ciudad: str):
        """
        Consulta 1 ($lookup + $unwind):
        detalle de compras de un usuario en una ciudad y su gasto total.
        """
        pipeline = [
            {"$match": {"run": run, "dv": dv}},
            {
                "$lookup": {
                    "from": "ordenes_compra",
                    "localField": "_id",
                    "foreignField": "usuario_id",
                    "as": "ordenes"
                }
            },
            {"$unwind": "$ordenes"},
            {
                "$lookup": {
                    "from": "eventos",
                    "localField": "ordenes.evento_id",
                    "foreignField": "_id",
                    "as": "evento_info"
                }
            },
            {"$unwind": "$evento_info"},
            {"$match": {"evento_info.ubicacion.ciudad": ciudad}},
            {
                "$group": {
                    "_id": "$_id",
                    "nombre_usuario": {"$first": {"$concat": ["$nombre", " ", "$apellido"]}},
                    "correo": {"$first": "$correo"},
                    "ciudad": {"$first": "$evento_info.ubicacion.ciudad"},
                    "gasto_total": {"$sum": "$ordenes.total"},
                    "compras_desglosadas": {
                        "$push": {
                            "orden_id": {"$toString": "$ordenes._id"},
                            "evento": "$evento_info.titulo",
                            "codigo": "$evento_info.codigo",
                            "tipo": "$evento_info.tipo",
                            "fecha_compra": "$ordenes.fecha",
                            "monto": "$ordenes.total"
                        }
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "nombre_usuario": 1,
                    "correo": 1,
                    "ciudad": 1,
                    "gasto_total": 1,
                    "compras_desglosadas": 1
                }
            }
        ]
        return list(db.usuarios.aggregate(pipeline))

    @staticmethod
    def gasto_usuarios_por_ciudad():
        """
        Consulta 1 para el grafico:
        gasto total de cada usuario en cada ciudad (sin filtrar por RUN ni ciudad).
        """
        pipeline = [
            {
                "$lookup": {
                    "from": "ordenes_compra",
                    "localField": "_id",
                    "foreignField": "usuario_id",
                    "as": "ordenes"
                }
            },
            {"$unwind": "$ordenes"},
            {
                "$lookup": {
                    "from": "eventos",
                    "localField": "ordenes.evento_id",
                    "foreignField": "_id",
                    "as": "evento_info"
                }
            },
            {"$unwind": "$evento_info"},
            {
                "$group": {
                    "_id": {"usuario": "$_id", "ciudad": "$evento_info.ubicacion.ciudad"},
                    "nombre_usuario": {"$first": {"$concat": ["$nombre", " ", "$apellido"]}},
                    "gasto_total": {"$sum": "$ordenes.total"},
                    "compras": {"$sum": 1}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "ciudad": "$_id.ciudad",
                    "nombre_usuario": 1,
                    "gasto_total": 1,
                    "compras": 1
                }
            },
            {"$sort": {"gasto_total": -1}}
        ]
        return list(db.usuarios.aggregate(pipeline))

    @staticmethod
    def reporte_ventas_eventos():
        """
        Consulta 2 (pipeline de reporte):
        recaudacion, tickets vendidos, ocupacion y rendimiento por evento.
        """
        pipeline = [
            {
                "$addFields": {
                    "stock_total": {"$sum": "$tickets.stock_ini"},
                    "stock_restante": {"$sum": "$tickets.disponibles"},
                    "subtotales_tickets": {
                        "$map": {
                            "input": "$tickets",
                            "as": "t",
                            "in": {
                                "$multiply": [
                                    {"$subtract": ["$$t.stock_ini", "$$t.disponibles"]},
                                    "$$t.precio"
                                ]
                            }
                        }
                    }
                }
            },
            {
                "$addFields": {
                    "total_recaudado": {"$sum": "$subtotales_tickets"},
                    "tickets_vendidos": {"$subtract": ["$stock_total", "$stock_restante"]}
                }
            },
            {
                "$addFields": {
                    "ptje_ocupacion": {
                        "$cond": {
                            "if": {"$gt": ["$stock_total", 0]},
                            "then": {
                                "$multiply": [{"$divide": ["$tickets_vendidos", "$stock_total"]}, 100]
                            },
                            "else": 0
                        }
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "codigo": 1,
                    "titulo": 1,
                    "tipo": 1,
                    "total_recaudado": 1,
                    "tickets_vendidos": 1,
                    "stock_total": 1,
                    "ptje_ocupacion": {"$round": ["$ptje_ocupacion", 2]},
                    "rendimiento": {
                        "$cond": {
                            "if": {"$gte": ["$ptje_ocupacion", 60]},
                            "then": "Exitoso",
                            "else": "Por Mejorar"
                        }
                    }
                }
            }
        ]
        return list(db.eventos.aggregate(pipeline))

    @staticmethod
    def eventos_futuros(ciudad: str, monto: int):
        """
        Consulta 3 (subdocumentos y fechas):
        eventos futuros en una ciudad con tickets disponibles bajo un monto.
        Devuelve una fila por ticket para mostrarla como tabla.
        """
        pipeline = [
            {
                "$match": {
                    "$expr": {"$gt": ["$fecha_hora_ini", "$$NOW"]},
                    "ubicacion.ciudad": ciudad,
                    "tickets": {
                        "$elemMatch": {
                            "disponibles": {"$gte": 1},
                            "precio": {"$lt": monto}
                        }
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "titulo": 1,
                    "tipo_evento": "$tipo",
                    "fecha_inicio": "$fecha_hora_ini",
                    "calle": "$ubicacion.calle",
                    "n_calle": "$ubicacion.n_calle",
                    "tipos_disponibles": {
                        "$filter": {
                            "input": "$tickets",
                            "as": "t",
                            "cond": {
                                "$and": [
                                    {"$gte": ["$$t.disponibles", 1]},
                                    {"$lt": ["$$t.precio", monto]}
                                ]
                            }
                        }
                    }
                }
            },
            {"$unwind": "$tipos_disponibles"},
            {
                "$project": {
                    "titulo": 1,
                    "tipo_evento": 1,
                    "fecha_inicio": 1,
                    "calle": 1,
                    "n_calle": 1,
                    "ticket": "$tipos_disponibles.tipo",
                    "precio": "$tipos_disponibles.precio",
                    "disponibles": "$tipos_disponibles.disponibles",
                    "zona": "$tipos_disponibles.zona"
                }
            }
        ]
        return list(db.eventos.aggregate(pipeline))

    @staticmethod
    def calidad_vs_precio(precio_alto: int = 20000):
        """
        Consulta 4 (libre): relacion precio-satisfaccion.
        Usa $lookup con subpipeline, $addFields encadenados y $switch.
        """
        pipeline = [
            {
                "$lookup": {
                    "from": "review_evaluaciones",
                    "let": {"ev_id": "$_id"},
                    "pipeline": [
                        {"$match": {"$expr": {"$eq": ["$evento_id", "$$ev_id"]}}},
                        {
                            "$group": {
                                "_id": None,
                                "promedio": {"$avg": "$calificacion"},
                                "total": {"$sum": 1}
                            }
                        }
                    ],
                    "as": "resumen"
                }
            },
            {"$unwind": "$resumen"},
            {
                "$addFields": {
                    "precio_promedio": {"$avg": "$tickets.precio"},
                    "calificacion_promedio": "$resumen.promedio",
                    "total_reviews": "$resumen.total"
                }
            },
            {
                "$addFields": {
                    "relacion": {
                        "$switch": {
                            "branches": [
                                {
                                    "case": {
                                        "$and": [
                                            {"$gte": ["$precio_promedio", precio_alto]},
                                            {"$lt": ["$calificacion_promedio", 3]}
                                        ]
                                    },
                                    "then": "Riesgo: caro y mal evaluado"
                                },
                                {
                                    "case": {"$gte": ["$calificacion_promedio", 4]},
                                    "then": "Bien evaluado"
                                }
                            ],
                            "default": "Regular"
                        }
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "codigo": 1,
                    "titulo": 1,
                    "tipo": 1,
                    "total_reviews": 1,
                    "relacion": 1,
                    "precio_promedio": {"$round": ["$precio_promedio", 0]},
                    "calificacion_promedio": {"$round": ["$calificacion_promedio", 2]}
                }
            },
            {"$sort": {"calificacion_promedio": -1}}
        ]
        return list(db.eventos.aggregate(pipeline))