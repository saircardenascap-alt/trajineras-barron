from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime
import json

app = Flask(__name__)

# Datos de los paquetes
# Datos de los paquetes (actualizados según las imágenes)
PACKAGES = {
    "recorrido-ajolotario": {
        "name": "Recorrido Ajolotario",
        "duration": "2 horas",
        "price": 1250,
        "original_price": 1500,
        "description": "2 horas de aventura + visita al fascinante mundo de los ajolotes. Entrada al ajolotario: $40 adicionales por persona.",
        "description_en": "2-hour adventure + visit to the fascinating world of axolotls. Ajolotario entrance: $40 additional per person.",
        "includes": [
            "Trajinera decorada con temática de ajolotes",
            "Anafre profesional para carne asada",
            "Guía especializado en ajolotes",
            "Visita al ajolotario (entrada adicional $40)",
            "Carbón y utensilios para asar",
            "Música ambiental mexicana",
            "Seguro básico incluido"
        ],
        "highlights": [
            "🎭 Experiencia única con ajolotes",
            "🔥 Anafre incluido para tu carne asada",
            "📸 Fotografías con ajolotes",
            "🌿 Entorno natural preservado"
        ]
    },
    "recorrido-normal": {
        "name": "Trajinera Normal",
        "duration": "2 horas",
        "price": 600,
        "original_price": 750,
        "description": "¡Disfruta un mágico paseo por los canales! Perfecto para un escape romántico o familiar. Incluye mantel.",
        "description_en": "Enjoy a magical boat trip along the canals! Perfect for a romantic getaway or a family escape. Tablecloth included.",
        "includes": [
            "Trajinera tradicional colorida",
            "Anafre con carbón incluido",
            "Mantel de mesa decorativo",
            "Recorrido por el canal de Apatlaco",
            "Capacidad para 18 personas máximo",
            "Guía local experto",
            "Hielera básica para tus bebidas"
        ],
        "highlights": [
            "🚣‍♀️ Paseo tradicional por canales",
            "🔥 Anafre para tu carne asada",
            "💑 Perfecto para parejas o familias",
            "🛶 Trajinera auténtica mexicana"
        ]
    },
    "recorrido-isla-munecas": {
        "name": "Recorrido Isla de las Muñecas",
        "duration": "4 horas",
        "price": 2250,
        "original_price": 2500,
        "description": "Experiencia única de 4 horas visitando la misteriosa y famosa Isla de las Muñecas. Entrada a la isla: $100 adicionales por persona.",
        "description_en": "Unique 4-hour experience visiting the mysterious and famous Island of the Dolls. Island entrance: $100 additional per person.",
        "includes": [
            "Trajinera temática de misterio",
            "Anafre premium para carne asada",
            "Guía especializado en leyendas",
            "Visita a la Isla de las Muñecas (entrada adicional $100)",
            "Iluminación especial nocturna",
            "Historia completa de la isla",
            "Carbón y parrilla profesional"
        ],
        "highlights": [
            "👻 Experiencia misteriosa única",
            "🔥 Asado bajo las estrellas",
            "📖 Leyendas e historias reales",
            "🌙 Ambiente nocturno espeluznante"
        ]
    },
    "recorrido-isla-llorona": {
        "name": "Recorrido Isla de la Llorona",
        "duration": "5 horas",
        "price": 2750,
        "original_price": 3000,
        "description": "Aventura de 5 horas a la hermosa y legendaria Isla de la Llorona. Entrada gratis.",
        "description_en": "5-hour adventure to the beautiful and legendary Island of the Weeping Woman. Free entry.",
        "includes": [
            "Trajinera de leyenda especial",
            "Anafre de lujo para carne asada",
            "Guía experto en mitología mexicana",
            "Visita completa a la Isla de la Llorona",
            "Narración teatralizada de la leyenda",
            "Decoración temática especial",
            "Parrilla profesional y carbón premium"
        ],
        "highlights": [
            "👻 Leyenda de la Llorona en vivo",
            "🔥 Carne asada con vista espectacular",
            "🎭 Actuación teatral incluida",
            "🌅 Atardecer en la isla legendaria"
        ]
    },
    "recorrido-familiar": {
        "name": "Recorrido Familiar",
        "duration": "3 horas",
        "price": 1800,
        "original_price": 2100,
        "description": "Increíble paseo familiar. Incluye mantel.",
        "description_en": "Amazing family outing. Includes a tablecloth.",
        "includes": [
            "Trajinera familiar decorada",
            "Anafre familiar grande",
            "Manteles festivos coloridos",
            "Juegos y actividades para niños",
            "Música familiar apropiada",
            "Capacidad para 20 personas",
            "Guía especializado en grupos familiares",
            "Área de juegos segura en la trajinera"
        ],
        "highlights": [
            "👨‍👩‍👧‍👦 Perfecto para toda la familia",
            "🔥 Asado familiar incluido",
            "🎮 Actividades para niños",
            "🎶 Música familiar divertida"
        ]
    },
    "recorrido-lunada-2horas": {
        "name": "Recorrido Lunada 2 Horas",
        "duration": "2 horas",
        "price": 1250,
        "original_price": 1500,
        "description": "Romance bajo la luna: mantel elegante, candeleros. Perfecto para propuestas o aniversarios.",
        "description_en": "Romance under the moon: elegant tablecloth, candlesticks. Perfect for proposals or anniversaries.",
        "includes": [
            "Trajinera romántica iluminada",
            "Anafre romántico para cena especial",
            "Mantel elegante de lino",
            "Candeleros y velas aromáticas",
            "Iluminación suave de luna",
            "Música romántica personalizada",
            "Decoración con pétalos de rosa",
            "Parrilla especial para cortes finos"
        ],
        "highlights": [
            "💖 Romance bajo la luna llena",
            "🔥 Carne asada gourmet",
            "🕯️ Ambiente con velas y candeleros",
            "💍 Perfecto para propuestas"
        ]
    },
    "recorrido-cumpleanos": {
        "name": "Recorrido Cumpleaños",
        "duration": "3 horas",
        "price": 1250,
        "original_price": 1500,
        "description": "¡Celebra tu cumpleaños con estilo! Trajinera decorada con globos, guirnaldas y letreros festivos. Incluye mantel de mesa.",
        "description_en": "Celebrate your birthday in style! A decorated trajinera with balloons, garlands, and festive signs. Includes a tablecloth.",
        "includes": [
            "Trajinera decorada para fiesta",
            "Anafre festivo para carne asada",
            "Decoración con globos y guirnaldas",
            "Letrero de 'Feliz Cumpleaños'",
            "Mantel festivo de cumpleaños",
            "Música de fiesta personalizada",
            "Área para pastel y regalos",
            "Sorpresa de cumpleaños especial"
        ],
        "highlights": [
            "🎂 Celebración única en el agua",
            "🔥 Asado de cumpleaños incluido",
            "🎈 Decoración festiva completa",
            "🎶 Música de fiesta todo el viaje"
        ]
    },
    "recorrido-amanecer": {
        "name": "Recorrido Amanecer",
        "duration": "3 horas",
        "price": 2250,
        "original_price": 2500,
        "description": "Experiencia mágica al amanecer en los canales de Xochimilco. Disfruta los primeros rayos del sol con un desayuno especial.",
        "description_en": "Magical experience at sunrise in the Xochimilco canals. Enjoy the first rays of sun with a special breakfast.",
        "includes": [
            "Trajinera especial para amanecer",
            "Anafre para desayuno asado",
            "Desayuno tradicional mexicano",
            "Café de olla recién hecho",
            "Guía experto en avistamiento de aves",
            "Binoculares para observación",
            "Mantas para el frío matutino",
            "Fotógrafo opcional (adicional)"
        ],
        "highlights": [
            "🌅 Amanecer espectacular en canales",
            "🔥 Desayuno asado tradicional",
            "🦅 Avistamiento de aves migratorias",
            "☕ Café de olla artesanal"
        ]
    },
    "paquete-lunada-4horas": {
        "name": "Paquete Lunada 4 Horas",
        "duration": "4 horas",
        "price": 5250,
        "original_price": 5560,
        "description": "4 horas de paseo nocturno + cena a bordo. Decorada con mantel y candelabros.",
        "description_en": "4-hour night cruise + dinner on board. Decorated with tablecloths and candelabras.",
        "includes": [
            "Trajinera de lujo para lunada",
            "Anafre gourmet profesional",
            "Cena completa a bordo",
            "Manteles de seda y candelabros",
            "Chef a bordo (adicional)",
            "Bar completo con bartender",
            "Sistema de sonido premium",
            "Calefacción para noches frías",
            "Servicio de mayordomo"
        ],
        "highlights": [
            "🌙 Noche completa bajo las estrellas",
            "🔥 Cena gourmet asada a bordo",
            "🍸 Bar completo con mixología",
            "💎 Experiencia de lujo exclusiva"
        ]
    }
}

# -------------------------------------------------
# NUEVA SECCIÓN: ANTOJITOS MEXICANOS
# -------------------------------------------------

COMIDA_MEXICANA = {
    "platillos": [
        {
            "id": "tlacoyos",
            "name": "Tlacoyos orden de 4",
            "price": 160,
            "original_price": 180,
            "description": "Tortilla hecha a mano, queso derretido y tu elección de flor de calabaza, hongos, tinga de pollo, chicharrón, huiltaoche, carne deshebrada, papa con chorizo. Acompañadas de salsa verde y lechuga.",
            "cantidad": "4 piezas",
            "icono": "🌮",
            "categoria": "antojitos",
            "acompañamientos": ["salsa verde", "lechuga"],
            "opciones": ["flor de calabaza", "hongos", "tinga de pollo", "chicharrón", "huiltaoche", "carne deshebrada", "papa con chorizo"]
        },
        {
            "id": "quesadillas",
            "name": "Quesadillas orden de 4",
            "price": 160,
            "original_price": 180,
            "description": "Tortilla hecha a mano, queso derretido y tu elección de flor de calabaza, hongos, tinga de pollo, chicharrón, huiltacoche, carne deshebrada, papa con chorizo. Acompañadas de salsa verde y lechuga.",
            "cantidad": "4 piezas",
            "icono": "🧀",
            "categoria": "antojitos",
            "acompañamientos": ["salsa verde", "lechuga"],
            "opciones": ["flor de calabaza", "hongos", "tinga de pollo", "chicharrón", "huiltacoche", "carne deshebrada", "papa con chorizo"]
        },
        {
            "id": "tostadas",
            "name": "Tostadas orden de 3",
            "price": 160,
            "original_price": 180,
            "description": "Tortilla hecha a mano, queso derretido y tu elección de flor de calabaza, hongos, tinga de pollo, chicharrón, huiltacoche, carne deshebrada, papa con chorizo. Acompañadas de salsa verde y lechuga.",
            "cantidad": "3 piezas",
            "icono": "🥑",
            "categoria": "antojitos",
            "acompañamientos": ["salsa verde", "lechuga"],
            "opciones": ["flor de calabaza", "hongos", "tinga de pollo", "chicharrón", "huiltacoche", "carne deshebrada", "papa con chorizo"]
        },
        {
            "id": "sopes",
            "name": "Sopes orden de 3",
            "price": 160,
            "original_price": 180,
            "description": "Tortilla hecha a mano, queso derretido y tu elección de flor de calabaza, hongos, tinga de pollo, chicharrón, huiltacoche, carne deshebrada, papa con chorizo. Acompañadas de salsa verde y lechuga.",
            "cantidad": "3 piezas",
            "icono": "🥙",
            "categoria": "antojitos",
            "acompañamientos": ["salsa verde", "lechuga"],
            "opciones": ["flor de calabaza", "hongos", "tinga de pollo", "chicharrón", "huiltacoche", "carne deshebrada", "papa con chorizo"]
        },
        {
            "id": "guacamole",
            "name": "Guacamole",
            "price": 100,
            "original_price": 120,
            "description": "Guacamole fresco preparado al momento con aguacate Hass, acompañado de chicharrón de cerdo y totopos.",
            "cantidad": "1 porción grande",
            "icono": "🥑",
            "categoria": "entradas",
            "acompañamientos": ["chicharrón de cerdo", "totopos"],
            "opciones": ["picante", "normal"]
        },
        {
            "id": "tamales",
            "name": "Tamales orden de 3",
            "price": 100,
            "original_price": 120,
            "description": "Elija entre verde con pollo, mole con pollo, o dulce y rojos. Hechos al estilo tradicional.",
            "cantidad": "3 tamales",
            "icono": "🌽",
            "categoria": "antojitos",
            "acompañamientos": ["salsa al gusto"],
            "opciones": ["verde con pollo", "mole con pollo", "dulce", "rojos"]
        },
        {
            "id": "mole-pollo",
            "name": "Mole con pollo y arroz",
            "price": 220,
            "original_price": 240,
            "description": "Una pieza de mole con pollo acompañado de arroz y tortillas.",
            "cantidad": "1 porción",
            "icono": "🍗",
            "categoria": "platillos",
            "acompañamientos": ["arroz", "tortillas"],
            "opciones": ["extra mole", "sin picante"]
        },
        {
            "id": "carne-asada",
            "name": "Carne asada",
            "price": 200,
            "original_price": 220,
            "description": "Carne asada acompañada con arroz o nopales y tortillas.",
            "cantidad": "1 porción",
            "icono": "🥩",
            "categoria": "platillos",
            "acompañamientos": ["arroz", "nopales", "tortillas"],
            "opciones": ["bien cocida", "término medio", "jugosa"]
        }
    ],
    "categorias": [
        {"id": "antojitos", "nombre": "🌮 Antojitos", "icono": "fas fa-utensils"},
        {"id": "entradas", "nombre": "🥑 Entradas", "icono": "fas fa-appetizer"},
        {"id": "platillos", "nombre": "🍛 Platillos Fuertes", "icono": "fas fa-drumstick-bite"}
    ],
    "opciones_adicionales": {
        "salsas": ["salsa verde", "salsa roja", "salsa habanero", "salsa taquera"],
        "extras": ["extra queso", "extra crema", "aguacate extra", "cebolla"],
        "bebidas": ["agua fresca", "refresco", "cerveza", "tequila"]
    }
}

# -------------------------------------------------
# RUTA PARA COMIDA MEXICANA
# -------------------------------------------------

@app.route('/antojitos-mexicanos')
def antojitos_mexicanos():
    """Ruta para la página de antojitos mexicanos"""
    return render_template('antojitos.html', comida=COMIDA_MEXICANA, packages=PACKAGES)

@app.route('/')
def inicio():
    return render_template('inicio.html', packages=PACKAGES, today=datetime.now().strftime('%Y-%m-%d'))

@app.route('/servicios')
def servicios():
    return render_template('servicios.html', packages=PACKAGES)

@app.route('/galeria')
def galeria():
    return render_template('galeria.html')

@app.route('/reservaciones')
def reservaciones():
    return render_template('reservaciones.html', packages=PACKAGES, today=datetime.now().strftime('%Y-%m-%d'))

@app.route('/ecologica')
def ecologica():
    return render_template('reservaEcologica.html')

@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        # Procesar formulario de contacto
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        telefono = request.form.get('telefono')
        mensaje = request.form.get('mensaje')
        fecha = request.form.get('fecha')
        
        # Aquí normalmente guardarías en base de datos
        print(f"Nuevo contacto: {nombre}, {email}, {telefono}")
        
        return redirect(url_for('contacto_gracias'))
    
    return render_template('contacto.html')

@app.route('/contacto/gracias')
def contacto_gracias():
    return render_template('contacto_gracias.html')

# -------------------------------------------------
# API PARA COMIDA MEXICANA
# -------------------------------------------------

@app.route('/api/comida/platillos')
def obtener_platillos_comida():
    """API para obtener todos los platillos de comida mexicana"""
    return jsonify(COMIDA_MEXICANA)

@app.route('/api/comida/agregar-carrito', methods=['POST'])
def agregar_al_carrito_comida():
    """API para agregar platillos al carrito de comida"""
    try:
        data = request.json
        platillo_id = data.get('platillo_id')
        cantidad = int(data.get('cantidad', 1))
        opciones = data.get('opciones', [])
        
        # Buscar el platillo
        platillo = next((p for p in COMIDA_MEXICANA['platillos'] if p['id'] == platillo_id), None)
        
        if not platillo:
            return jsonify({
                "success": False,
                "error": "Platillo no encontrado"
            }), 404
        
        # Calcular total
        total = platillo['price'] * cantidad
        
        # En producción, agregarías al carrito en la sesión o base de datos
        carrito_item = {
            "platillo_id": platillo_id,
            "nombre": platillo['name'],
            "cantidad": cantidad,
            "precio_unitario": platillo['price'],
            "total": total,
            "opciones": opciones,
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"Platillo agregado al carrito: {platillo['name']}")
        print(f"Cantidad: {cantidad}, Total: ${total}")
        
        return jsonify({
            "success": True,
            "mensaje": f"{platillo['name']} agregado al carrito",
            "carrito_item": carrito_item,
            "total_carrito": total  # En producción, calcularías el total actual del carrito
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

@app.route('/api/comida/calcular-total', methods=['POST'])
def calcular_total_comida():
    """API para calcular el total de la orden de comida"""
    try:
        data = request.json
        items = data.get('items', [])
        
        subtotal = 0
        detalle_items = []
        
        for item in items:
            platillo = next((p for p in COMIDA_MEXICANA['platillos'] if p['id'] == item['id']), None)
            if platillo:
                cantidad = item.get('cantidad', 1)
                item_total = platillo['price'] * cantidad
                subtotal += item_total
                
                detalle_items.append({
                    "nombre": platillo['name'],
                    "cantidad": cantidad,
                    "precio_unitario": platillo['price'],
                    "total_item": item_total
                })
        
        # Calcular IVA (16%)
        iva = subtotal * 0.16
        total = subtotal + iva
        
        return jsonify({
            "success": True,
            "resumen": {
                "subtotal": subtotal,
                "iva": iva,
                "total": total,
                "items": detalle_items
            },
            "resumen_texto": f"Total: ${total:,.2f} MXN (IVA incluido)"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

@app.route('/api/check-availability', methods=['POST'])
def check_availability():
    data = request.json
    fecha = data.get('fecha')
    hora = data.get('hora')
    
    # Simulación de verificación de disponibilidad
    # En producción, verificarías en una base de datos
    disponibilidad = {
        "available": True,
        "message": "Horario disponible"
    }
    
    return jsonify(disponibilidad)

@app.route('/api/reservar', methods=['POST'])
def hacer_reserva():
    data = request.json
    # Procesar reserva
    reserva_id = f"RES{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    return jsonify({
        "success": True,
        "reserva_id": reserva_id,
        "message": "Reserva creada exitosamente"
    })

# -------------------------------------------------
# NUEVAS RUTAS PARA SERVICIOS
# -------------------------------------------------

# Datos adicionales para servicios
SERVICIOS_ADICIONALES = {
    "musica": [
        {"nombre": "Mariachi Completo", "precio": 4500, "duracion": "1 hora", "icono": "🎺"},
        {"nombre": "Trio de Cuerdas", "precio": 2500, "duracion": "1 hora", "icono": "🎸"},
        {"nombre": "DJ/Bocina Bluetooth", "precio": 400, "duracion": "Evento completo", "icono": "🔊"}
    ],
    "decoracion": [
        {"nombre": "Decoración Temática", "precio": 500, "descripcion": "Globos, manteles, centro de mesa"},
        {"nombre": "Decoración Premium", "precio": 700, "descripcion": "Incluye luces y elementos especiales"},
        {"nombre": "Cambio de Nombre Trajinera", "precio": 500, "descripcion": "Personaliza el nombre por un día"}
    ],
    "fotografia": [
        {"nombre": "Fotógrafo Profesional", "precio": 1500, "duracion": "2 horas", "fotos": "50+ fotos editadas"},
        {"nombre": "Sesión Básica", "precio": 800, "duracion": "1 hora", "fotos": "25+ fotos"}
    ]
}

# Ruta para calcular cotización personalizada
@app.route('/api/calcular-cotizacion', methods=['POST'])
def calcular_cotizacion():
    try:
        data = request.json
        
        # Obtener datos del formulario
        paquete_base = data.get('paquete')
        personas = int(data.get('personas', 10))
        extras = data.get('extras', [])
        
        # Calcular precio base
        precio_base = PACKAGES.get(paquete_base, {}).get('price', 0)
        
        # Calcular extras
        total_extras = 0
        for extra in extras:
            servicio = next((s for categoria in SERVICIOS_ADICIONALES.values() 
                           for s in categoria if s['nombre'] == extra), None)
            if servicio:
                total_extras += servicio['precio']
        
        # Total
        total = precio_base + total_extras
        
        return jsonify({
            "success": True,
            "desglose": {
                "paquete_base": precio_base,
                "extras": total_extras,
                "total": total
            },
            "resumen": f"Total para {personas} personas: ${total:,} MXN"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

# Ruta para guardar personalización
@app.route('/api/guardar-personalizacion', methods=['POST'])
def guardar_personalizacion():
    data = request.json
    
    # Generar ID de personalización
    personalizacion_id = f"PER{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # En producción, guardarías en base de datos
    print(f"Personalización guardada: {personalizacion_id}")
    print(f"Datos: {data}")
    
    return jsonify({
        "success": True,
        "personalizacion_id": personalizacion_id,
        "message": "Personalización guardada exitosamente"
    })

# Ruta para calcular cotización personalizada
@app.route('/api/calcular-cotizacion', methods=['POST'])
def calcular_cotizacion():
    try:
        data = request.json
        
        # Obtener datos del formulario
        paquete_base = data.get('paquete')
        personas = int(data.get('personas', 10))
        extras = data.get('extras', [])
        catering = data.get('catering', [])
        
        # Calcular precio base
        precio_base = PACKAGES.get(paquete_base, {}).get('price', 0)
        
        # Calcular extras
        total_extras = 0
        for extra in extras:
            servicio = next((s for categoria in SERVICIOS_ADICIONALES.values() 
                           for s in categoria if s['nombre'] == extra), None)
            if servicio:
                total_extras += servicio['precio']
        
        # Calcular catering
        total_catering = 0
        for item in catering:
            servicio = next((s for s in SERVICIOS_ADICIONALES['catering'] 
                           if s['nombre'] == item), None)
            if servicio and servicio.get('pp'):
                total_catering += servicio['precio'] * personas
        
        # Total
        total = precio_base + total_extras + total_catering
        
        return jsonify({
            "success": True,
            "desglose": {
                "paquete_base": precio_base,
                "extras": total_extras,
                "catering": total_catering,
                "total": total
            },
            "resumen": f"Total para {personas} personas: ${total:,} MXN"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

# Ruta para guardar personalización
@app.route('/api/guardar-personalizacion', methods=['POST'])
def guardar_personalizacion():
    data = request.json
    
    # Generar ID de personalización
    personalizacion_id = f"PER{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # En producción, guardarías en base de datos
    print(f"Personalización guardada: {personalizacion_id}")
    print(f"Datos: {data}")
    
    return jsonify({
        "success": True,
        "personalizacion_id": personalizacion_id,
        "message": "Personalización guardada exitosamente"
    })

# -------------------------------------------------
# NUEVAS RUTAS PARA RESERVACIONES
# -------------------------------------------------

# Datos de disponibilidad (simulación)
HORARIOS_DISPONIBLES = {
    "09:00": True,
    "12:00": True,
    "15:00": True,
    "18:00": True
}

# Datos de precios dinámicos
PRECIOS_DINAMICOS = {
    "recorrido-ajolotario": {
        "base": 1250,
        "por_persona": 40,  # $40 adicional por entrada al ajolotario
        "fines_semana": 150
    },
    "recorrido-normal": {
        "base": 600,
        "por_persona": 30,
        "fines_semana": 100
    },
    "recorrido-isla-munecas": {
        "base": 2250,
        "por_persona": 100,  # $100 adicional por entrada a la isla
        "fines_semana": 200
    },
    "recorrido-isla-llorona": {
        "base": 2750,
        "por_persona": 0,  # Entrada gratis
        "fines_semana": 250
    },
    "recorrido-familiar": {
        "base": 1800,
        "por_persona": 100,
        "fines_semana": 200
    },
    "recorrido-lunada-2horas": {
        "base": 1250,
        "por_persona": 80,
        "fines_semana": 150
    },
    "recorrido-cumpleanos": {
        "base": 1250,
        "por_persona": 80,
        "fines_semana": 150
    },
    "recorrido-amanecer": {
        "base": 2250,
        "por_persona": 120,
        "fines_semana": 250
    },
    "paquete-lunada-4horas": {
        "base": 5250,
        "por_persona": 150,
        "fines_semana": 300
    }
}

# Datos de métodos de pago
METODOS_PAGO = [
    {
        "id": "transferencia",
        "nombre": "Transferencia Bancaria",
        "descripcion": "Depósito del 30% para confirmar",
        "instrucciones": "BBVA: 0123 4567 8901 2345\nBeneficiario: Trajineras Barrón",
        "requiere_deposito": True
    },
    {
        "id": "efectivo",
        "nombre": "Efectivo al llegar",
        "descripcion": "Pago total en el embarcadero",
        "instrucciones": "Aceptamos efectivo y tarjetas. Llega 30 min antes.",
        "requiere_deposito": False
    },
    {
        "id": "tarjeta",
        "nombre": "Tarjeta de Crédito/Débito",
        "descripcion": "Pago seguro en línea",
        "instrucciones": "Procesado por Stripe. 100% seguro.",
        "requiere_deposito": False
    }
]

@app.route('/api/verificar-disponibilidad', methods=['POST'])
def verificar_disponibilidad():
    try:
        data = request.json
        fecha = data.get('fecha')
        hora = data.get('hora')
        personas = int(data.get('personas', 10))
        
        # Simulación de verificación
        disponibilidad = {
            "disponible": True,
            "mensaje": "Horario disponible",
            "capacidad_maxima": 20,
            "capacidad_disponible": 20 - min(personas, 5)  # Simulación
        }
        
        # Validar capacidad
        if personas > 20:
            disponibilidad["disponible"] = False
            disponibilidad["mensaje"] = "Capacidad máxima: 20 personas"
        
        # Validar horario
        if hora not in HORARIOS_DISPONIBLES:
            disponibilidad["disponible"] = False
            disponibilidad["mensaje"] = "Horario no disponible"
        
        return jsonify(disponibilidad)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

# Ruta para calcular precio dinámico
@app.route('/api/calcular-precio', methods=['POST'])
def calcular_precio_dinamico():
    try:
        data = request.json
        paquete = data.get('paquete')
        personas = int(data.get('personas', 10))
        fecha_str = data.get('fecha')
        
        if not paquete or paquete not in PRECIOS_DINAMICOS:
            return jsonify({
                "success": False,
                "error": "Paquete no válido"
            }), 400
        
        # Parsear fecha
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d') if fecha_str else datetime.now()
        es_fin_semana = fecha.weekday() >= 5  # 5=Sábado, 6=Domingo
        
        # Calcular precio
        precio_info = PRECIOS_DINAMICOS[paquete]
        precio_base = precio_info['base']
        
        # Calcular precio por persona adicional
        precio_personas = precio_info['por_persona'] * max(0, personas - 10)
        incremento_fs = precio_info['fines_semana'] if es_fin_semana else 0
        precio_total = precio_base + precio_personas + incremento_fs
        
        return jsonify({
            "success": True,
            "precio_total": precio_total,
            "desglose": {
                "base": precio_base,
                "personas_extra": precio_personas,
                "fin_semana": incremento_fs if es_fin_semana else 0,
                "es_fin_semana": es_fin_semana
            }
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

# Ruta para procesar reserva
@app.route('/api/procesar-reserva', methods=['POST'])
def procesar_reserva():
    try:
        data = request.json
        
        # Validar datos requeridos
        required_fields = ['nombre', 'email', 'telefono', 'fecha', 'paquete', 'personas']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    "success": False,
                    "error": f"Campo requerido: {field}"
                }), 400
        
        # Generar ID de reserva
        reserva_id = f"RES{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Calcular total
        paquete = data.get('paquete')
        personas = int(data.get('personas'))
        fecha_str = data.get('fecha')
        
        # Calcular precio
        precio_info = PRECIOS_DINAMICOS.get(paquete, {"base": 0, "por_persona": 0})
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d') if fecha_str else datetime.now()
        es_fin_semana = fecha.weekday() >= 5
        
        precio_total = precio_info['base'] + (precio_info['por_persona'] * max(0, personas - 10))
        
        if es_fin_semana:
            precio_total += precio_info.get('fines_semana', 0)
        
        # Calcular depósito
        deposito = precio_total * 0.3
        
        # Guardar reserva (en producción sería en base de datos)
        reserva = {
            "id": reserva_id,
            "cliente": {
                "nombre": data.get('nombre'),
                "email": data.get('email'),
                "telefono": data.get('telefono')
            },
            "reserva": {
                "fecha": fecha_str,
                "hora": data.get('hora', '12:00'),
                "paquete": paquete,
                "personas": personas,
                "extras": data.get('extras', []),
                "comida": data.get('comida', [])  # Nueva sección de comida
            },
            "pago": {
                "total": precio_total,
                "deposito": deposito,
                "saldo": precio_total - deposito,
                "metodo": data.get('metodo_pago', 'efectivo')
            },
            "estado": "pendiente",
            "fecha_creacion": datetime.now().isoformat()
        }
        
        print(f"Reserva creada: {reserva_id}")
        print(f"Cliente: {data.get('nombre')}")
        print(f"Total: ${precio_total}")
        
        # En producción, enviar email de confirmación aquí
        
        return jsonify({
            "success": True,
            "reserva_id": reserva_id,
            "mensaje": "Reserva creada exitosamente",
            "deposito": deposito,
            "total": precio_total,
            "proximo_paso": "Realizar depósito del 30% para confirmar"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

# Ruta para obtener métodos de pago
@app.route('/api/metodos-pago')
def obtener_metodos_pago():
    return jsonify(METODOS_PAGO)

# Ruta para obtener horarios disponibles
@app.route('/api/horarios-disponibles/<fecha>')
def obtener_horarios_disponibles(fecha):
    try:
        # Simulación: todos los horarios disponibles
        return jsonify({
            "fecha": fecha,
            "horarios": HORARIOS_DISPONIBLES
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Ruta para confirmar pago
@app.route('/api/confirmar-pago', methods=['POST'])
def confirmar_pago():
    data = request.json
    reserva_id = data.get('reserva_id')
    metodo_pago = data.get('metodo_pago')
    referencia = data.get('referencia', '')
    
    # Simular confirmación de pago
    print(f"Pago confirmado para reserva {reserva_id}")
    print(f"Método: {metodo_pago}, Referencia: {referencia}")
    
    return jsonify({
        "success": True,
        "reserva_id": reserva_id,
        "estado": "confirmada",
        "mensaje": "Pago confirmado. Reserva activa.",
        "correo_enviado": True
    })

# Ruta para obtener servicios adicionales
@app.route('/api/servicios-adicionales')
def obtener_servicios_adicionales():
    return jsonify(SERVICIOS_ADICIONALES)



# -------------------------------------------------
# NUEVAS RUTAS PARA GALERÍA
# -------------------------------------------------

# Datos de la galería
GALERIA_DATOS = {
    "categorias": [
        {"id": "eventos", "nombre": "🎉 Eventos", "icono": "fas fa-calendar-star", "contador": 45},
        {"id": "familiar", "nombre": "👨‍👩‍👧‍👦 Familiar", "icono": "fas fa-users", "contador": 78},
        {"id": "romantico", "nombre": "💑 Romántico", "icono": "fas fa-heart", "contador": 52},
        {"id": "amanecer", "nombre": "🌅 Amanecer/Atardecer", "icono": "fas fa-sun", "contador": 34},
        {"id": "gastronomia", "nombre": "🍽️ Gastronomía", "icono": "fas fa-utensils", "contador": 29},
        {"id": "musica", "nombre": "🎵 Música y Fiesta", "icono": "fas fa-music", "contador": 41},
        {"id": "naturaleza", "nombre": "🌿 Naturaleza", "icono": "fas fa-leaf", "contador": 63}
    ],
    
    "experiencias": [
        {
            "id": "isla-munecas",
            "titulo": "Isla de las Muñecas",
            "descripcion": "Un lugar místico lleno de historia y tradición",
            "imagen": "https://images.unsplash.com/photo-1542601906990-b4d3fb778b09",
            "fotos": 25,
            "tipo": "historia"
        },
        {
            "id": "noche-leyendas",
            "titulo": "Noche de Leyendas",
            "descripcion": "Recorridos nocturnos con historias de Xochimilco",
            "imagen": "https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3",
            "fotos": 18,
            "tipo": "nocturno"
        },
        {
            "id": "trajineras-vivas",
            "titulo": "Trajineras Vivas",
            "descripcion": "Agricultura flotante en las chinampas",
            "imagen": "https://images.unsplash.com/photo-1528433556524-74e7e3bfa599",
            "fotos": 32,
            "tipo": "naturaleza"
        },
        {
            "id": "isla-llorona",
            "titulo": "Isla de la Llorona",
            "descripcion": "El legendario recorrido que estremece",
            "imagen": "https://images.unsplash.com/photo-1566073771259-6a8506099945",
            "fotos": 22,
            "tipo": "leyenda"
        },
        {
            "id": "lunadas",
            "titulo": "Lunadas Mágicas",
            "descripcion": "Las mejores noches bajo la luna",
            "imagen": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4",
            "fotos": 28,
            "tipo": "nocturno"
        },
        {
            "id": "amaneceres",
            "titulo": "Amaneceres Dorados",
            "descripcion": "Los primeros rayos del sol en los canales",
            "imagen": "https://images.unsplash.com/photo-1501854140801-50d01698950b",
            "fotos": 35,
            "tipo": "amanecer"
        }
    ],
    
    "videos": [
        {
            "id": "video1",
            "titulo": "Experiencia Familiar Completa",
            "descripcion": "Un día completo en Xochimilco con la familia Pérez",
            "duracion": "2:15",
            "thumbnail": "https://images.unsplash.com/photo-1566073771259-6a8506099945",
            "vistas": "1.2K",
            "fecha": "2024-03-15"
        },
        {
            "id": "video2",
            "titulo": "Boda en Trajinera",
            "descripcion": "La boda más romántica en los canales",
            "duracion": "1:45",
            "thumbnail": "https://images.unsplash.com/photo-1519225421980-715cb0215aed",
            "vistas": "2.5K",
            "fecha": "2024-02-28"
        },
        {
            "id": "video3",
            "titulo": "Xochimilco al Amanecer",
            "descripcion": "La magia de los primeros rayos de sol",
            "duracion": "3:20",
            "thumbnail": "https://images.unsplash.com/photo-1501854140801-50d01698950b",
            "vistas": "890",
            "fecha": "2024-03-01"
        }
    ],
    
    "albumes": [
        {
            "paquete": "familiar",
            "nombre": "Paquete Familiar",
            "fotos": 20,
            "portada": "https://images.unsplash.com/photo-1566073771259-6a8506099945",
            "descripcion": "Momentos inolvidables para toda la familia"
        },
        {
            "paquete": "romantico",
            "nombre": "Paquete Romántico",
            "fotos": 15,
            "portada": "https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3",
            "descripcion": "Noches mágicas para parejas"
        },
        {
            "paquete": "gastronomico",
            "nombre": "Paquete Gastronómico",
            "fotos": 25,
            "portada": "https://images.unsplash.com/photo-1565958011703-44f9829ba187",
            "descripcion": "Sabores tradicionales de Xochimilco"
        },
        {
            "paquete": "lunada",
            "nombre": "Paquete Lunada",
            "fotos": 18,
            "portada": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4",
            "descripcion": "Recorridos nocturnos bajo la luna"
        },
        {
            "paquete": "amanecer",
            "nombre": "Paquete Amanecer",
            "fotos": 22,
            "portada": "https://images.unsplash.com/photo-1501854140801-50d01698950b",
            "descripcion": "La belleza del amanecer en los canales"
        }
    ],
    
    "historico": [
        {
            "epoca": "años 50",
            "titulo": "Xochimilco en los años 50",
            "descripcion": "Las trajineras tradicionales en su esplendor",
            "imagen_antigua": "https://images.unsplash.com/photo-1542601906990-b4d3fb778b09",
            "imagen_actual": "https://images.unsplash.com/photo-1566073771259-6a8506099945",
            "nota": "Más de 70 años preservando la tradición"
        },
        {
            "epoca": "años 80",
            "titulo": "La evolución de las trajineras",
            "descripcion": "De la madera simple a las obras de arte flotantes",
            "imagen_antigua": "https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3",
            "imagen_actual": "https://images.unsplash.com/photo-1519225421980-715cb0215aed",
            "nota": "Misma tradición, nueva belleza"
        }
    ]
}

# Ruta para obtener datos de la galería
@app.route('/api/galeria/datos')
def obtener_datos_galeria():
    return jsonify(GALERIA_DATOS)

# Ruta para obtener imágenes por categoría
@app.route('/api/galeria/categoria/<categoria_id>')
def obtener_imagenes_categoria(categoria_id):
    try:
        # Simulación de datos de imágenes
        imagenes_por_categoria = {
            "eventos": [
                {"id": 1, "url": "https://images.unsplash.com/photo-1519225421980-715cb0215aed", "likes": 45, "autor": "Juan Pérez"},
                {"id": 2, "url": "https://images.unsplash.com/photo-1542601906990-b4d3fb778b09", "likes": 32, "autor": "María García"},
                {"id": 3, "url": "https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3", "likes": 67, "autor": "Carlos López"}
            ],
            "familiar": [
                {"id": 4, "url": "https://images.unsplash.com/photo-1566073771259-6a8506099945", "likes": 89, "autor": "Familia Rodríguez"},
                {"id": 5, "url": "https://images.unsplash.com/photo-1528433556524-74e7e3bfa599", "likes": 56, "autor": "Ana Martínez"}
            ]
        }
        
        imagenes = imagenes_por_categoria.get(categoria_id, [])
        
        return jsonify({
            "categoria": categoria_id,
            "imagenes": imagenes,
            "total": len(imagenes)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Ruta para "me gusta" en imágenes
@app.route('/api/galeria/like', methods=['POST'])
def dar_like_imagen():
    try:
        data = request.json
        imagen_id = data.get('imagen_id')
        
        # En producción, incrementarías en base de datos
        print(f"Like para imagen {imagen_id}")
        
        return jsonify({
            "success": True,
            "imagen_id": imagen_id,
            "mensaje": "Like registrado"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Ruta para subir foto de usuario
@app.route('/api/galeria/subir', methods=['POST'])
def subir_foto_galeria():
    try:
        # En producción, manejarías archivos subidos
        data = request.json
        hashtag = data.get('hashtag', '#XochimilcoBarron')
        
        print(f"Nueva foto subida con hashtag: {hashtag}")
        
        return jsonify({
            "success": True,
            "mensaje": "Foto recibida para revisión",
            "hashtag": hashtag,
            "nota": "Tu foto será revisada y publicada en 24-48 horas"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Ruta para fotógrafos profesionales
@app.route('/api/galeria/fotografos', methods=['POST'])
def contacto_fotografos():
    try:
        data = request.json
        nombre = data.get('nombre')
        email = data.get('email')
        portfolio = data.get('portfolio')
        
        print(f"Solicitud de fotógrafo: {nombre} - {email}")
        print(f"Portfolio: {portfolio}")
        
        return jsonify({
            "success": True,
            "mensaje": "Solicitud recibida. Te contactaremos en 48 horas."
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# -------------------------------------------------
# NUEVAS RUTAS PARA RESERVA ECOLÓGICA
# -------------------------------------------------

# Datos ecológicos
DATOS_ECOLOGICOS = {
    "compromiso": {
        "mision": "Por cada reserva, donamos el 5% a la reforestación de chinampas y la protección de especies endémicas.",
        "donacion_porcentaje": 5,
        "aliados": [
            {"nombre": "Pronatura", "logo": "pronatura.png", "url": "https://pronatura.org.mx"},
            {"nombre": "WWF México", "logo": "wwf.png", "url": "https://www.wwf.org.mx"},
            {"nombre": "UNAM Ecología", "logo": "unam.png", "url": "https://www.ecologia.unam.mx"},
            {"nombre": "CONANP", "logo": "conanp.png", "url": "https://www.gob.mx/conanp"}
        ],
        "certificaciones": [
            "Turismo Sustentable Certificado",
            "Sello Verde Xochimilco",
            "Miembro de Red de Turismo Responsable"
        ]
    },
    
    "ecosistema": {
        "especies": [
            {
                "nombre": "Ajolote Mexicano",
                "nombre_cientifico": "Ambystoma mexicanum",
                "estado": "En peligro crítico",
                "descripcion": "Anfibio endémico con capacidad de regeneración",
                "imagen": "https://images.unsplash.com/photo-1559253664-ca249d4608c6",
                "curiosidad": "Puede regenerar extremidades, órganos y tejidos"
            },
            {
                "nombre": "Garza Blanca",
                "nombre_cientifico": "Ardea alba",
                "estado": "Preocupación menor",
                "descripcion": "Ave migratoria que habita en humedales",
                "imagen": "https://images.unsplash.com/photo-1550853024-fae8cd4be47f",
                "curiosidad": "Puede vivir hasta 22 años en estado silvestre"
            },
            {
                "nombre": "Ahuejote",
                "nombre_cientifico": "Salix bonplandiana",
                "estado": "Especie nativa",
                "descripcion": "Árbol fundamental para las chinampas",
                "imagen": "https://images.unsplash.com/photo-1542601906990-b4d3fb778b09",
                "curiosidad": "Sus raíces fijan las chinampas al fondo del lago"
            }
        ],
        
        "aves_migratorias": [
            {"nombre": "Pato Canadiense", "temporada": "Octubre-Marzo", "ruta": "Canadá-México"},
            {"nombre": "Garceta Grande", "temporada": "Todo el año", "ruta": "Residente"},
            {"nombre": "Pelícano Blanco", "temporada": "Noviembre-Febrero", "ruta": "EEUU-México"}
        ],
        
        "chinampas": {
            "descripcion": "Sistema agrícola prehispánico único en el mundo",
            "importancia": "Patrimonio Agrícola Mundial (FAO)",
            "extension": "2,200 hectáreas",
            "productos": ["hortalizas", "flores", "plantas medicinales"]
        }
    },
    
    "proyectos": [
        {
            "id": "rescate-ajolote",
            "nombre": "Rescate del Ajolote",
            "descripcion": "Programa de conservación y reproducción del ajolote mexicano",
            "logros": ["50 ajolotes rescatados", "2 centros de reproducción", "3 investigaciones publicadas"],
            "colaboradores": ["UNAM", "Zoológico de Chapultepec"],
            "estado": "Activo"
        },
        {
            "id": "trajineras-vivas",
            "nombre": "Trajineras Vivas",
            "descripcion": "Reforestación con plantas nativas en bordes de canales",
            "logros": ["500 árboles plantados", "20 especies nativas recuperadas", "10 km reforestados"],
            "colaboradores": ["SEDEMA", "Comunidad local"],
            "estado": "Activo"
        },
        {
            "id": "canales-limpios",
            "nombre": "Canales Limpios",
            "descripcion": "Jornadas mensuales de limpieza de canales y humedales",
            "logros": ["20 km de canales limpios", "5 toneladas de basura recolectadas", "500 voluntarios"],
            "colaboradores": ["Voluntarios", "Escuelas locales"],
            "estado": "Activo"
        },
        {
            "id": "educacion-ambiental",
            "nombre": "Educación Ambiental",
            "descripcion": "Talleres y capacitación sobre conservación de humedales",
            "logros": ["30 guías capacitados", "500 estudiantes educados", "10 talleres realizados"],
            "colaboradores": ["SEP", "ONGs ambientales"],
            "estado": "Activo"
        }
    ],
    
    "experiencias": [
        {
            "id": "tour-agricultura",
            "nombre": "Tour Trajineras y Agricultura",
            "descripcion": "Visita a chinampas activas con explicación del sistema agrícola ancestral",
            "duracion": "3 horas",
            "precio": 1800,
            "incluye": ["Guía especializado", "Visita a chinampa activa", "Degustación de productos"],
            "eco_beneficio": "15% donado a reforestación"
        },
        {
            "id": "avistamiento-aves",
            "nombre": "Avistamiento de Aves",
            "descripcion": "Recorrido con guía naturalista para observar aves migratorias y residentes",
            "duracion": "2.5 horas",
            "precio": 1500,
            "incluye": ["Guía naturalista", "Binoculares", "Guía de identificación"],
            "eco_beneficio": "15% donado a conservación de hábitats"
        },
        {
            "id": "recorrido-nocturno",
            "nombre": "Recorrido Nocturno Ecológico",
            "descripcion": "Experiencia sensorial sin contaminación lumínica, enfocada en sonidos naturales",
            "duracion": "2 horas",
            "precio": 1200,
            "incluye": ["Guía especializado", "Linternas ecológicas", "Grabación de sonidos"],
            "eco_beneficio": "15% donado a investigación"
        }
    ],
    
    "impacto": {
        "desde": "2024",
        "metricas": [
            {"nombre": "Árboles reforestados", "valor": 500, "unidad": "árboles", "meta": 1000},
            {"nombre": "Ajolotes rescatados", "valor": 50, "unidad": "ajolotes", "meta": 100},
            {"nombre": "Canales limpios", "valor": 20, "unidad": "km", "meta": 50},
            {"nombre": "Guías capacitados", "valor": 30, "unidad": "guías", "meta": 100},
            {"nombre": "Voluntarios", "valor": 500, "unidad": "personas", "meta": 1000},
            {"nombre": "Estudiantes educados", "valor": 500, "unidad": "estudiantes", "meta": 2000}
        ],
        "donaciones_totales": 125000  # En MXN
    },
    
    "testimonios": [
        {
            "nombre": "Dra. Laura Méndez",
            "titulo": "Bióloga, UNAM",
            "texto": "Como bióloga, recomiendo esta experiencia por su compromiso real con la conservación. Cada recorrido contribuye directamente a la investigación y protección de especies endémicas.",
            "avatar": "LM",
            "estrellas": 5
        },
        {
            "nombre": "Michael Thompson",
            "titulo": "Ecologista, Canadá",
            "texto": "Viajé desde Canadá para ver los humedales de Xochimilco y quedé impresionado con su trabajo de conservación. El guía conocía cada especie y su importancia ecológica.",
            "avatar": "MT",
            "estrellas": 5
        },
        {
            "nombre": "Ana Rodríguez",
            "titulo": "Maestra de Biología",
            "texto": "Llevé a mis estudiantes y fue increíble. No solo se divirtieron, sino que aprendieron sobre la importancia de conservar nuestros ecosistemas. Educativo y entretenido.",
            "avatar": "AR",
            "estrellas": 5
        }
    ],
    
    "reglas": {
        "hacer": [
            "Respetar la distancia con la fauna silvestre",
            "Seguir las indicaciones del guía",
            "Usar bloqueador solar biodegradable",
            "Llevar agua en envases reutilizables",
            "Tomar fotografías sin flash a los animales"
        ],
        "no_hacer": [
            "Tirar basura en los canales",
            "Alimentar a los animales",
            "Colectar plantas o animales",
            "Usar repelentes químicos fuertes",
            "Hacer ruidos fuertes que alteren la fauna"
        ]
    }
}

@app.route('/api/ecologico/datos')
def obtener_datos_ecologicos():
    return jsonify(DATOS_ECOLOGICOS)

# Ruta para calcular impacto ecológico
@app.route('/api/ecologico/calcular-impacto', methods=['POST'])
def calcular_impacto_ecologico():
    try:
        data = request.json
        personas = int(data.get('personas', 10))
        experiencia = data.get('experiencia', 'tour-agricultura')
        
        # Encontrar la experiencia
        exp = next((e for e in DATOS_ECOLOGICOS['experiencias'] if e['id'] == experiencia), None)
        
        if not exp:
            return jsonify({"error": "Experiencia no encontrada"}), 400
        
        # Calcular donación
        precio_total = exp['precio'] * personas
        donacion_porcentaje = DATOS_ECOLOGICOS['compromiso']['donacion_porcentaje'] + 10  # 5% base + 10% extra por ser ecológico
        donacion = (precio_total * donacion_porcentaje) / 100
        
        # Calcular impacto equivalente
        arboles_equivalentes = donacion / 250  # 250 MXN por árbol
        metros_canal_limpios = donacion / 500   # 500 MXN por km de limpieza
        
        return jsonify({
            "success": True,
            "resumen": {
                "personas": personas,
                "experiencia": exp['nombre'],
                "precio_total": precio_total,
                "donacion_porcentaje": donacion_porcentaje,
                "donacion_monto": donacion,
                "impacto_equivalente": {
                    "arboles": round(arboles_equivalentes, 1),
                    "canales_limpios": round(metros_canal_limpios, 2),
                    "ajolotes": round(donacion / 5000, 2)  # 5000 MXN por ajolote rescatado
                }
            },
            "mensaje": f"Tu reserva contribuirá con ${donacion:,.2f} MXN a proyectos de conservación"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Ruta para registrar reserva ecológica
@app.route('/api/ecologico/reservar', methods=['POST'])
def registrar_reserva_ecologica():
    try:
        data = request.json
        
        # Validar datos requeridos
        required_fields = ['nombre', 'email', 'fecha', 'experiencia', 'personas']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    "success": False,
                    "error": f"Campo requerido: {field}"
                }), 400
        
        # Generar ID de reserva ecológica
        reserva_id = f"ECO{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Calcular impacto
        experiencia = data.get('experiencia')
        personas = int(data.get('personas'))
        
        exp = next((e for e in DATOS_ECOLOGICOS['experiencias'] if e['id'] == experiencia), None)
        if not exp:
            return jsonify({"error": "Experiencia no válida"}), 400
        
        precio_total = exp['precio'] * personas
        donacion_porcentaje = DATOS_ECOLOGICOS['compromiso']['donacion_porcentaje'] + 10
        donacion = (precio_total * donacion_porcentaje) / 100
        
        # Crear registro de reserva ecológica
        reserva_ecologica = {
            "id": reserva_id,
            "cliente": {
                "nombre": data.get('nombre'),
                "email": data.get('email'),
                "telefono": data.get('telefono', ''),
                "motivo": data.get('motivo', 'conservacion')
            },
            "reserva": {
                "fecha": data.get('fecha'),
                "experiencia": experiencia,
                "personas": personas,
                "observaciones": data.get('observaciones', '')
            },
            "impacto": {
                "donacion": donacion,
                "porcentaje": donacion_porcentaje,
                "proyectos": data.get('proyectos_destino', ['trajineras-vivas', 'rescate-ajolote'])
            },
            "fecha_registro": datetime.now().isoformat(),
            "estado": "pendiente"
        }
        
        # En producción, guardarías en base de datos
        print(f"Reserva ecológica registrada: {reserva_id}")
        print(f"Cliente: {data.get('nombre')}")
        print(f"Donación: ${donacion}")
        print(f"Proyectos: {reserva_ecologica['impacto']['proyectos']}")
        
        # Simular envío de certificado ecológico
        certificado_id = f"CER{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        return jsonify({
            "success": True,
            "reserva_id": reserva_id,
            "certificado_id": certificado_id,
            "donacion": donacion,
            "mensaje": "Reserva ecológica registrada exitosamente",
            "certificado_url": f"/certificados/{certificado_id}",
            "proximo_paso": "Recibirás un certificado de impacto ambiental por correo"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Ruta para obtener certificado ecológico
@app.route('/api/ecologico/certificado/<certificado_id>')
def obtener_certificado(certificado_id):
    # En producción, generarías un PDF o imagen del certificado
    return jsonify({
        "success": True,
        "certificado_id": certificado_id,
        "fecha_emision": datetime.now().strftime('%Y-%m-%d'),
        "mensaje": "Certificado de impacto ambiental generado",
        "detalles": {
            "organizacion": "Trajineras Barrón",
            "proyectos": ["Reforestación de chinampas", "Rescate del ajolote"],
            "validez": "1 año",
            "codigo_verificacion": f"VER-{certificado_id}"
        }
    })


# Ruta para suscribirse a newsletter ecológico
@app.route('/api/ecologico/suscribir', methods=['POST'])
def suscribir_newsletter_ecologico():
    try:
        data = request.json
        email = data.get('email')
        interes = data.get('interes', 'conservacion')
        
        if not email:
            return jsonify({"error": "Email requerido"}), 400
        
        # En producción, guardarías en base de datos
        print(f"Nueva suscripción ecológica: {email}")
        print(f"Interés: {interes}")
        
        return jsonify({
            "success": True,
            "email": email,
            "mensaje": "¡Te has suscrito al newsletter ecológico!",
            "bienvenida": "Recibirás actualizaciones sobre nuestros proyectos de conservación"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/reserva-ecologica')
def reserva_ecologica():
    return render_template('reservaEcologica.html')

if __name__ == '__main__':
    import os
    # Configuración para producción
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
    