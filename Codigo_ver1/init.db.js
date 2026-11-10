/* ==========================================================================
   SCRIPT DE CARGA DE DATOS DE PRUEBA (SEED) - EVENTIFY
   Genera un mínimo de 50 documentos por colección respetando los esquemas
   y asociando referencias con findOne()._id
   ========================================================================== */

use("no-sql-ev2");

// Limpieza previa opcional para pruebas
db.review_evaluaciones.deleteMany({});
db.ordenes_compra.deleteMany({});
db.eventos.deleteMany({});
db.usuarios.deleteMany({});

/* --------------------------------------------------------------------------
   1. INSERCIÓN EN COLECCIÓN: usuarios (50 documentos)
   -------------------------------------------------------------------------- */
db.usuarios.insertMany([
	{
		run: "21684030",
		dv: "5",
		nombre: "Amaru",
		apellido: "Burdiles",
		correo: "amaru.burdiles@gmail.com",
		telefono: "+56912345678",
		fecha_nacimiento: new Date("1998-05-14T00:00:00Z"),
		es_vip: true
	},
	{
		run: "18456123",
		dv: "k",
		nombre: "Aldo",
		apellido: "Inostroza",
		correo: "aldo.inostroza@outlook.com",
		telefono: "+56987654321",
		fecha_nacimiento: new Date("1993-11-20T00:00:00Z"),
		es_vip: false
	},
	{
		run: "19876543",
		dv: "2",
		nombre: "Yeira",
		apellido: "Inostroza",
		correo: "yeira.inostroza@yahoo.com",
		telefono: "+56923456789",
		fecha_nacimiento: new Date("1996-08-03T00:00:00Z"),
		es_vip: true
	},
	{
		run: "20123456",
		dv: "8",
		nombre: "Abraham",
		apellido: "Inostroza",
		correo: "abraham.inostroza@gmail.com",
		telefono: "+56934567890",
		fecha_nacimiento: new Date("1999-01-15T00:00:00Z"),
		es_vip: false
	},
	{
		run: "15987654",
		dv: "1",
		nombre: "Carlos",
		apellido: "Mendoza",
		correo: "carlos.mendoza@gmail.com",
		telefono: "+56945678901",
		fecha_nacimiento: new Date("1985-04-12T00:00:00Z"),
		es_vip: false
	},
	{
		run: "16543218",
		dv: "9",
		nombre: "Daniela",
		apellido: "Rojas",
		correo: "daniela.rojas@hotmail.com",
		telefono: "+56956789012",
		fecha_nacimiento: new Date("1988-09-25T00:00:00Z"),
		es_vip: true
	},
	{
		run: "17234567",
		dv: "3",
		nombre: "Esteban",
		apellido: "Pérez",
		correo: "esteban.perez@live.cl",
		telefono: "+56967890123",
		fecha_nacimiento: new Date("1990-02-28T00:00:00Z"),
		es_vip: false
	},
	{
		run: "18901234",
		dv: "4",
		nombre: "Fernanda",
		apellido: "Soto",
		correo: "fernanda.soto@gmail.com",
		telefono: "+56978901234",
		fecha_nacimiento: new Date("1994-07-19T00:00:00Z"),
		es_vip: true
	},
	{
		run: "19345678",
		dv: "6",
		nombre: "Gabriel",
		apellido: "Torres",
		correo: "gabriel.torres@uc.cl",
		telefono: "+56989012345",
		fecha_nacimiento: new Date("1996-12-10T00:00:00Z"),
		es_vip: false
	},
	{
		run: "20456789",
		dv: "7",
		nombre: "Javiera",
		apellido: "Morales",
		correo: "javiera.morales@usach.cl",
		telefono: "+56990123456",
		fecha_nacimiento: new Date("2000-03-05T00:00:00Z"),
		es_vip: false
	},
	{
		run: "21345678",
		dv: "0",
		nombre: "Lucas",
		apellido: "Silva",
		correo: "lucas.silva@gmail.com",
		telefono: "+56901234567",
		fecha_nacimiento: new Date("2002-06-22T00:00:00Z"),
		es_vip: true
	},
	{
		run: "14567890",
		dv: "K",
		nombre: "Maria",
		apellido: "García",
		correo: "maria.garcia@gmail.com",
		telefono: "+56911223344",
		fecha_nacimiento: new Date("1982-10-30T00:00:00Z"),
		es_vip: false
	},
	{
		run: "13456789",
		dv: "2",
		nombre: "Nicolas",
		apellido: "Fuentes",
		correo: "nicolas.fuentes@gmail.com",
		telefono: "+56922334455",
		fecha_nacimiento: new Date("1979-08-17T00:00:00Z"),
		es_vip: true
	},
	{
		run: "22123456",
		dv: "1",
		nombre: "Sofia",
		apellido: "Castro",
		correo: "sofia.castro@gmail.com",
		telefono: "+56933445566",
		fecha_nacimiento: new Date("2003-11-01T00:00:00Z"),
		es_vip: false
	},
	{
		run: "23123456",
		dv: "9",
		nombre: "Tomas",
		apellido: "Herrera",
		correo: "tomas.herrera@gmail.com",
		telefono: "+56944556677",
		fecha_nacimiento: new Date("2005-01-09T00:00:00Z"),
		es_vip: false
	},
	{
		run: "15123456",
		dv: "8",
		nombre: "Valentina",
		apellido: "Araya",
		correo: "valentina.araya@gmail.com",
		telefono: "+56955667788",
		fecha_nacimiento: new Date("1984-05-18T00:00:00Z"),
		es_vip: true
	},
	{
		run: "16123456",
		dv: "7",
		nombre: "Gonzalo",
		apellido: "Espinoza",
		correo: "gonzalo.espinoza@gmail.com",
		telefono: "+56966778899",
		fecha_nacimiento: new Date("1987-03-14T00:00:00Z"),
		es_vip: false
	},
	{
		run: "17123456",
		dv: "6",
		nombre: "Camila",
		apellido: "Valenzuela",
		correo: "camila.valenzuela@gmail.com",
		telefono: "+56977889900",
		fecha_nacimiento: new Date("1989-12-05T00:00:00Z"),
		es_vip: false
	},
	{
		run: "18123456",
		dv: "5",
		nombre: "Rodrigo",
		apellido: "Tapia",
		correo: "rodrigo.tapia@gmail.com",
		telefono: "+56988990011",
		fecha_nacimiento: new Date("1992-04-23T00:00:00Z"),
		es_vip: true
	},
	{
		run: "19123456",
		dv: "4",
		nombre: "Isadora",
		apellido: "Reyes",
		correo: "isadora.reyes@gmail.com",
		telefono: "+56999001122",
		fecha_nacimiento: new Date("1995-09-11T00:00:00Z"),
		es_vip: false
	},
	{
		run: "20987654",
		dv: "3",
		nombre: "Matías",
		apellido: "Díaz",
		correo: "matias.diaz@gmail.com",
		telefono: "+56910102020",
		fecha_nacimiento: new Date("2001-02-14T00:00:00Z"),
		es_vip: false
	},
	{
		run: "21987654",
		dv: "2",
		nombre: "Antonia",
		apellido: "Muñoz",
		correo: "antonia.munoz@gmail.com",
		telefono: "+56920203030",
		fecha_nacimiento: new Date("2002-08-29T00:00:00Z"),
		es_vip: true
	},
	{
		run: "12987654",
		dv: "1",
		nombre: "Felipe",
		apellido: "Contreras",
		correo: "felipe.contreras@gmail.com",
		telefono: "+56930304040",
		fecha_nacimiento: new Date("1978-01-04T00:00:00Z"),
		es_vip: false
	},
	{
		run: "13987654",
		dv: "0",
		nombre: "Paula",
		apellido: "Sepúlveda",
		correo: "paula.sepulveda@gmail.com",
		telefono: "+56940405050",
		fecha_nacimiento: new Date("1980-06-16T00:00:00Z"),
		es_vip: true
	},
	{
		run: "14987654",
		dv: "k",
		nombre: "Sebastián",
		apellido: "Alvarez",
		correo: "sebastian.alvarez@gmail.com",
		telefono: "+56950506060",
		fecha_nacimiento: new Date("1983-11-27T00:00:00Z"),
		es_vip: false
	},
	{
		run: "15876543",
		dv: "9",
		nombre: "Claudia",
		apellido: "Parra",
		correo: "claudia.parra@gmail.com",
		telefono: "+56960607070",
		fecha_nacimiento: new Date("1986-07-08T00:00:00Z"),
		es_vip: false
	},
	{
		run: "16876543",
		dv: "8",
		nombre: "Diego",
		apellido: "Figueroa",
		correo: "diego.figueroa@gmail.com",
		telefono: "+56970708080",
		fecha_nacimiento: new Date("1988-10-19T00:00:00Z"),
		es_vip: true
	},
	{
		run: "17876543",
		dv: "7",
		nombre: "Natalia",
		apellido: "Jara",
		correo: "natalia.jara@gmail.com",
		telefono: "+56980809090",
		fecha_nacimiento: new Date("1991-03-31T00:00:00Z"),
		es_vip: false
	},
	{
		run: "18876543",
		dv: "6",
		nombre: "Ignacio",
		apellido: "Vidal",
		correo: "ignacio.vidal@gmail.com",
		telefono: "+56990900011",
		fecha_nacimiento: new Date("1993-05-12T00:00:00Z"),
		es_vip: true
	},
	{
		run: "19876123",
		dv: "5",
		nombre: "Constanza",
		apellido: "Bravo",
		correo: "constanza.bravo@gmail.com",
		telefono: "+56911112222",
		fecha_nacimiento: new Date("1997-09-02T00:00:00Z"),
		es_vip: false
	},
	{
		run: "20876123",
		dv: "4",
		nombre: "Joaquín",
		apellido: "Gomez",
		correo: "joaquin.gomez@gmail.com",
		telefono: "+56922223333",
		fecha_nacimiento: new Date("2000-12-18T00:00:00Z"),
		es_vip: false
	},
	{
		run: "21876123",
		dv: "3",
		nombre: "Martina",
		apellido: "Vargas",
		correo: "martina.vargas@gmail.com",
		telefono: "+56933334444",
		fecha_nacimiento: new Date("2002-04-07T00:00:00Z"),
		es_vip: true
	},
	{
		run: "22876123",
		dv: "2",
		nombre: "Benjamín",
		apellido: "Lagos",
		correo: "benjamin.lagos@gmail.com",
		telefono: "+56944445555",
		fecha_nacimiento: new Date("2004-10-24T00:00:00Z"),
		es_vip: false
	},
	{
		run: "11765432",
		dv: "1",
		nombre: "Patricia",
		apellido: "Cortés",
		correo: "patricia.cortes@gmail.com",
		telefono: "+56955556666",
		fecha_nacimiento: new Date("1975-08-15T00:00:00Z"),
		es_vip: true
	},
	{
		run: "12765432",
		dv: "0",
		nombre: "Jorge",
		apellido: "Vergara",
		correo: "jorge.vergara@gmail.com",
		telefono: "+56966667777",
		fecha_nacimiento: new Date("1977-01-30T00:00:00Z"),
		es_vip: false
	},
	{
		run: "13765432",
		dv: "K",
		nombre: "Loreto",
		apellido: "Soto",
		correo: "loreto.soto@gmail.com",
		telefono: "+56977778888",
		fecha_nacimiento: new Date("1980-03-21T00:00:00Z"),
		es_vip: false
	},
	{
		run: "14765432",
		dv: "9",
		nombre: "Francisco",
		apellido: "Mora",
		correo: "francisco.mora@gmail.com",
		telefono: "+56988889999",
		fecha_nacimiento: new Date("1982-06-11T00:00:00Z"),
		es_vip: true
	},
	{
		run: "15765432",
		dv: "8",
		nombre: "Andrea",
		apellido: "Pizarro",
		correo: "andrea.pizarro@gmail.com",
		telefono: "+56999990000",
		fecha_nacimiento: new Date("1985-09-09T00:00:00Z"),
		es_vip: false
	},
	{
		run: "16765432",
		dv: "7",
		nombre: "Manuel",
		apellido: "Cárdenas",
		correo: "manuel.cardenas@gmail.com",
		telefono: "+56912123434",
		fecha_nacimiento: new Date("1987-11-13T00:00:00Z"),
		es_vip: false
	},
	{
		run: "17765432",
		dv: "6",
		nombre: "Bárbara",
		apellido: "Salazar",
		correo: "barbara.salazar@gmail.com",
		telefono: "+56923234545",
		fecha_nacimiento: new Date("1990-02-02T00:00:00Z"),
		es_vip: true
	},
	{
		run: "18765432",
		dv: "5",
		nombre: "Cristian",
		apellido: "Ríos",
		correo: "cristian.rios@gmail.com",
		telefono: "+56934345656",
		fecha_nacimiento: new Date("1992-05-17T00:00:00Z"),
		es_vip: false
	},
	{
		run: "19765432",
		dv: "4",
		nombre: "Macarena",
		apellido: "Escobar",
		correo: "macarena.escobar@gmail.com",
		telefono: "+56945456767",
		fecha_nacimiento: new Date("1995-12-25T00:00:00Z"),
		es_vip: true
	},
	{
		run: "20765432",
		dv: "3",
		nombre: "Álvaro",
		apellido: "Guzmán",
		correo: "alvaro.guzman@gmail.com",
		telefono: "+56956567878",
		fecha_nacimiento: new Date("1998-07-04T00:00:00Z"),
		es_vip: false
	},
	{
		run: "21765432",
		dv: "2",
		nombre: "Francisca",
		apellido: "Ojeda",
		correo: "francisca.ojeda@gmail.com",
		telefono: "+56967678989",
		fecha_nacimiento: new Date("2001-10-15T00:00:00Z"),
		es_vip: false
	},
	{
		run: "22765432",
		dv: "1",
		nombre: "Vicente",
		apellido: "Pena",
		correo: "vicente.pena@gmail.com",
		telefono: "+56978789090",
		fecha_nacimiento: new Date("2003-03-29T00:00:00Z"),
		es_vip: true
	},
	{
		run: "10654321",
		dv: "0",
		nombre: "Teresa",
		apellido: "Paredes",
		correo: "teresa.paredes@gmail.com",
		telefono: "+56989890101",
		fecha_nacimiento: new Date("1972-04-01T00:00:00Z"),
		es_vip: false
	},
	{
		run: "11654321",
		dv: "k",
		nombre: "Hernán",
		apellido: "Gallardo",
		correo: "hernan.gallardo@gmail.com",
		telefono: "+56990901212",
		fecha_nacimiento: new Date("1974-09-14T00:00:00Z"),
		es_vip: false
	},
	{
		run: "12654321",
		dv: "9",
		nombre: "Solange",
		apellido: "Acuna",
		correo: "solange.acuna@gmail.com",
		telefono: "+56901012323",
		fecha_nacimiento: new Date("1977-06-20T00:00:00Z"),
		es_vip: true
	},
	{
		run: "13654321",
		dv: "8",
		nombre: "Claudio",
		apellido: "Garrido",
		correo: "claudio.garrido@gmail.com",
		telefono: "+56912122323",
		fecha_nacimiento: new Date("1980-01-11T00:00:00Z"),
		es_vip: false
	},
	{
		run: "14654321",
		dv: "7",
		nombre: "Karina",
		apellido: "Becerra",
		correo: "karina.becerra@gmail.com",
		telefono: "+56923233434",
		fecha_nacimiento: new Date("1982-08-08T00:00:00Z"),
		es_vip: true
	}
]);

/* --------------------------------------------------------------------------
   2. INSERCIÓN EN COLECCIÓN: eventos (50 documentos)
   Incluye eventos en Santiago y otras ciudades, pasados y futuros con $$NOW
   -------------------------------------------------------------------------- */
db.eventos.insertMany([
	{
		codigo: "EVT-STG-001",
		titulo: "Lollapalooza Chile 2027",
		tipo: "Concierto",
		descripcion: "Festival masivo de música internacional.",
		capacidad: 50000,
		fecha_hora_ini: new Date("2027-03-19T12:00:00Z"),
		fecha_hora_fin: new Date("2027-03-21T23:59:00Z"),
		activo: true,
		ubicacion: {
			pais: "Chile",
			ciudad: "Santiago",
			calle: "Parque Bicentenario Cerrillos",
			n_calle: 1100,
			coordenadas: [-70.7012, -33.4921],
			detalle: "Acceso principal por Av. Pedro Aguirre Cerda"
		},
		tickets: [
			{ tipo: "General", precio: 8500, stock_ini: 10000, disponibles: 4500, zona: "Cancha" },
			{ tipo: "VIP Lolla", precio: 45000, stock_ini: 2000, disponibles: 100, zona: "Lounge VIP" }
		]
	},
	{
		codigo: "EVT-STG-002",
		titulo: "Feria del Libro Usado 2026",
		tipo: "Exposición",
		descripcion: "Exposición y venta de literatura clásica.",
		capacidad: 2000,
		fecha_hora_ini: new Date("2026-11-10T10:00:00Z"),
		fecha_hora_fin: new Date("2026-11-15T20:00:00Z"),
		activo: true,
		ubicacion: {
			pais: "Chile",
			ciudad: "Santiago",
			calle: "Alameda",
			n_calle: 1058,
			coordenadas: [-70.6511, -33.4431]
		},
		tickets: [{ tipo: "Entrada Libre", precio: 2000, stock_ini: 5000, disponibles: 1200, zona: "General" }]
	},
	{
		codigo: "EVT-STG-003",
		titulo: "Tech Summit Santiago 2027",
		tipo: "Conferencia",
		descripcion: "Encuentro de tecnología, IA y desarrollo de software.",
		capacidad: 1500,
		fecha_hora_ini: new Date("2027-01-15T09:00:00Z"),
		fecha_hora_fin: new Date("2027-01-16T18:00:00Z"),
		activo: true,
		ubicacion: {
			pais: "Chile",
			ciudad: "Santiago",
			calle: "Av. Dag Hammarskjöld",
			n_calle: 3267,
			coordenadas: [-70.5991, -33.4022]
		},
		tickets: [
			{ tipo: "Estudiante", precio: 9500, stock_ini: 500, disponibles: 150, zona: "Plenar" },
			{ tipo: "Profesional", precio: 35000, stock_ini: 1000, disponibles: 50, zona: "VIP Tech" }
		]
	},
	{
		codigo: "EVT-CCP-001",
		titulo: "REC - Rock en Conce 2026",
		tipo: "Concierto",
		descripcion: "Festival gratuito de rock en el Parque Bicentenario.",
		capacidad: 40000,
		fecha_hora_ini: new Date("2026-10-25T14:00:00Z"),
		fecha_hora_fin: new Date("2026-10-26T23:00:00Z"),
		activo: true,
		ubicacion: {
			pais: "Chile",
			ciudad: "Concepción",
			calle: "Av. Costanera",
			n_calle: 500,
			coordenadas: [-73.0611, -36.8261]
		},
		tickets: [{ tipo: "Pase Preferencial", precio: 7500, stock_ini: 3000, disponibles: 800, zona: "Frente al Escenario" }]
	},
	{
		codigo: "EVT-VAL-001",
		titulo: "Festival de Teatro Valparaíso",
		tipo: "Teatro",
		descripcion: "Obras teatrales en cerros y salas culturales.",
		capacidad: 800,
		fecha_hora_ini: new Date("2025-01-10T19:00:00Z"),
		fecha_hora_fin: new Date("2025-01-20T22:00:00Z"),
		activo: false,
		ubicacion: {
			pais: "Chile",
			ciudad: "Valparaíso",
			calle: "Plaza Sotomayor",
			n_calle: 123,
			coordenadas: [-71.6289, -33.0375]
		},
		tickets: [{ tipo: "General", precio: 5000, stock_ini: 800, disponibles: 0, zona: "Platea" }]
	},
	{
		codigo: "EVT-STG-004",
		titulo: "Noche de Jazz & Wine",
		tipo: "Concierto",
		descripcion: "Concierto de Jazz en vivo y degustación de vinos.",
		capacidad: 300,
		fecha_hora_ini: new Date("2026-12-05T20:00:00Z"),
		fecha_hora_fin: new Date("2026-12-05T23:30:00Z"),
		activo: true,
		ubicacion: {
			pais: "Chile",
			ciudad: "Santiago",
			calle: "Av. Italia",
			n_calle: 1500,
			coordenadas: [-70.6278, -33.4512]
		},
		tickets: [
			{ tipo: "Silla Individual", precio: 8000, stock_ini: 200, disponibles: 45, zona: "Salón Principal" },
			{ tipo: "Mesa VIP (2 personas)", precio: 25000, stock_ini: 50, disponibles: 0, zona: "Terraza" }
		]
	},
	// Generación de 44 eventos adicionales variados
	...Array.from({ length: 44 }).map((_, i) => {
		const num = i + 5;
		const esSantiago = i % 2 === 0;
		const esFuturo = i % 3 !== 0; // 2/3 son futuros, 1/3 pasado
		const ciudad = esSantiago ? "Santiago" : i % 3 === 0 ? "Concepción" : "Viña del Mar";
		const mes = (i % 12) + 1;
		const anio = esFuturo ? 2027 : 2025;

		return {
			codigo: `EVT-${ciudad.substring(0, 3).toUpperCase()}-${num.toString().padStart(3, "0")}`,
			titulo: `Evento Cultural y Deportivo N° ${num}`,
			tipo: i % 4 === 0 ? "Deportes" : i % 4 === 1 ? "Concierto" : i % 4 === 2 ? "Seminario" : "Feria",
			descripcion: `Descripción detallada para el evento cultural ${num} en la ciudad de ${ciudad}.`,
			capacidad: 1000 + i * 200,
			fecha_hora_ini: new Date(`${anio}-${mes.toString().padStart(2, "0")}-10T15:00:00Z`),
			fecha_hora_fin: new Date(`${anio}-${mes.toString().padStart(2, "0")}-10T22:00:00Z`),
			activo: esFuturo,
			ubicacion: {
				pais: "Chile",
				ciudad: ciudad,
				calle: "Av. Principal",
				n_calle: 100 + i,
				coordenadas: [-70.6 + i * 0.01, -33.4 - i * 0.01]
			},
			tickets: [
				{
					tipo: "Económico",
					precio: 3000 + i * 200, // Algunos menores a 10000, otros superiores
					stock_ini: 500,
					disponibles: esFuturo ? 150 : 0,
					zona: "General"
				},
				{
					tipo: "Preferencial",
					precio: 15000 + i * 500,
					stock_ini: 300,
					disponibles: esFuturo ? 50 : 0,
					zona: "Platea Alta"
				}
			]
		};
	})
]);

/* --------------------------------------------------------------------------
   3. REFERENCIAS DINÁMICAS CON findOne()._id
   Asociaciones por clave primaria de Usuarios y Eventos
   -------------------------------------------------------------------------- */

// Guardar los ObjectIds de Usuarios
const usrAmaru = db.usuarios.findOne({ run: "21684030" })._id;
const usrAldo = db.usuarios.findOne({ run: "18456123" })._id;
const usrYeira = db.usuarios.findOne({ run: "19876543" })._id;
const usrAbraham = db.usuarios.findOne({ run: "20123456" })._id;
const usrCarlos = db.usuarios.findOne({ run: "15987654" })._id;
const usrDaniela = db.usuarios.findOne({ run: "16543218" })._id;
const usrEsteban = db.usuarios.findOne({ run: "17234567" })._id;
const usrFernanda = db.usuarios.findOne({ run: "18901234" })._id;

// Guardar los ObjectIds de Eventos
const evtLolla = db.eventos.findOne({ codigo: "EVT-STG-001" })._id;
const evtLibro = db.eventos.findOne({ codigo: "EVT-STG-002" })._id;
const evtTech = db.eventos.findOne({ codigo: "EVT-STG-003" })._id;
const evtREC = db.eventos.findOne({ codigo: "EVT-CCP-001" })._id;
const evtTeatro = db.eventos.findOne({ codigo: "EVT-VAL-001" })._id;
const evtJazz = db.eventos.findOne({ codigo: "EVT-STG-004" })._id;

/* --------------------------------------------------------------------------
   4. INSERCIÓN EN COLECCIÓN: ordenes_compra (50 documentos)
   Garantiza compras para Amaru (Consulta 1) en eventos de Santiago
   -------------------------------------------------------------------------- */

// Lista auxiliar con todos los ObjectIds de usuarios y eventos para iterar
const todosLosUsuarios = db.usuarios
	.find({}, { _id: 1 })
	.toArray()
	.map((u) => u._id);
const todosLosEventos = db.eventos
	.find({}, { _id: 1 })
	.toArray()
	.map((e) => e._id);

db.ordenes_compra.insertMany([
	// Compras específicas de Amaru (RUN 21684030) en Santiago para validar Consulta 1
	{ usuario_id: usrAmaru, evento_id: evtLolla, total: 8500, fecha: new Date("2026-01-10T14:30:00Z") },
	{ usuario_id: usrAmaru, evento_id: evtLolla, total: 45000, fecha: new Date("2026-01-11T16:00:00Z") },
	{ usuario_id: usrAmaru, evento_id: evtLibro, total: 2000, fecha: new Date("2026-02-01T10:15:00Z") },
	{ usuario_id: usrAmaru, evento_id: evtTech, total: 9500, fecha: new Date("2026-03-05T18:20:00Z") },
	{ usuario_id: usrAmaru, evento_id: evtJazz, total: 8000, fecha: new Date("2026-04-12T21:00:00Z") },

	// Compras de otros usuarios conocidos
	{ usuario_id: usrAldo, evento_id: evtREC, total: 7500, fecha: new Date("2026-02-14T11:00:00Z") },
	{ usuario_id: usrYeira, evento_id: evtLolla, total: 45000, fecha: new Date("2026-01-20T15:45:00Z") },
	{ usuario_id: usrAbraham, evento_id: evtTeatro, total: 5000, fecha: new Date("2025-01-05T12:00:00Z") },
	{ usuario_id: usrCarlos, evento_id: evtLibro, total: 4000, fecha: new Date("2026-02-02T16:30:00Z") },
	{ usuario_id: usrDaniela, evento_id: evtTech, total: 35000, fecha: new Date("2026-03-01T09:10:00Z") },

	// Generación dinámica de las 40 órdenes restantes vinculando usuarios y eventos
	...Array.from({ length: 40 }).map((_, i) => {
		const uId = todosLosUsuarios[i % todosLosUsuarios.length];
		const eId = todosLosEventos[i % todosLosEventos.length];
		const dia = (i % 28) + 1;
		return {
			usuario_id: uId,
			evento_id: eId,
			total: 5000 + i * 1200,
			fecha: new Date(`2026-05-${dia.toString().padStart(2, "0")}T14:00:00Z`)
		};
	})
]);

/* --------------------------------------------------------------------------
   5. INSERCIÓN EN COLECCIÓN: review_evaluaciones (50 documentos)
   -------------------------------------------------------------------------- */
db.review_evaluaciones.insertMany([
	{ usuario_id: usrAmaru, evento_id: evtTeatro, calificacion: 5, comentario: "Excelente obra y montaje visual." },
	{ usuario_id: usrAldo, evento_id: evtTeatro, calificacion: 4, comentario: "Muy buena acústica en el recinto." },
	{ usuario_id: usrYeira, evento_id: evtLibro, calificacion: 5, comentario: "Gran variedad de títulos clásicos." },
	{ usuario_id: usrAbraham, evento_id: evtREC, calificacion: 3, comentario: "El sonido pudo ser mejor en la tarde." },
	{ usuario_id: usrCarlos, evento_id: evtTeatro, calificacion: 2, comentario: "Poca capacidad de estacionamiento." },
	{ usuario_id: usrDaniela, evento_id: evtTeatro, calificacion: 5, comentario: "Inolvidable experiencia teatral." },
	{ usuario_id: usrEsteban, evento_id: evtLibro, calificacion: 4, comentario: "Precios bastante accesibles." },
	{ usuario_id: usrFernanda, evento_id: evtREC, calificacion: 5, comentario: "Ambiente increíble y muy seguro." },

	// Generación dinámica de las 42 evaluaciones restantes
	...Array.from({ length: 42 }).map((_, i) => {
		const uId = todosLosUsuarios[(i + 5) % todosLosUsuarios.length];
		const eId = todosLosEventos[(i + 2) % todosLosEventos.length];
		return {
			usuario_id: uId,
			evento_id: eId,
			calificacion: (i % 5) + 1, // Calificación entre 1 y 5
			comentario: `Comentario de evaluación de prueba N° ${i + 1} sobre la organización del evento.`
		};
	})
]);

print("✅ Carga de datos completada exitosamente: 50+ documentos insertados por colección.");