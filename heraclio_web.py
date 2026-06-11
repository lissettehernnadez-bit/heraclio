import json
import random
import threading

from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS

import asyncio
import edge_tts
import uuid

app_web = Flask(__name__)
CORS(app_web)

VOZ = "es-ES-AlvaroNeural"

#speaker = win32com.client.Dispatch("SAPI.SpVoice")

#def hablar(texto):
#speaker.Speak(texto)

    
print("holis")

# IDENTIDAD

nombre_ia = "Heraclio"

# MEMORIA
try:
    with open("memoria.json", "r") as f:
        memoria = json.load(f)
except:
    memoria = {
        "estado": "amigable",
        "emocion_historial": [],
        "historial": []
    }
    
if "historial" not in memoria:
    memoria["historial"] = []

if "estado_ia" not in memoria:
    memoria["estado_ia"] = "normal"

if "conocimientos" not in memoria:
    memoria["conocimientos"] = {}

if "aprendiendo" not in memoria:
    memoria["aprendiendo"] = None

# VENTANA
#ctk.set_appearance_mode("dark")

#app = ctk.CTk()
#app.geometry("450x500")
#app.title("Mi IA 💙")

#chat = ctk.CTkTextbox(app, width=400, height=300)
#chat.pack(pady=20)

#entrada = ctk.CTkEntry(app, placeholder_text="Escribe aquí...")
#entrada.pack(pady=10)

@app_web.route("/")
def inicio():
    return send_from_directory("mi-ia", "index.html")

@app_web.route('/<path:archivo>')
def servir_archivo(archivo):
    return send_from_directory('mi-ia', archivo)

def enviar():

    mensaje = entrada.get().lower()
    respuesta = ""

    memoria["historial"].append(mensaje)

    emociones_ia = [
    "feliz",
    "normal",
    "cansado",
    "triste",
    "enoj",
    "confuso"
]

    if random.randint(1, 10) == 1:
        memoria["estado_ia"] = random.choice(emociones_ia)

    print("Estado de Heraclio:", memoria["estado_ia"])

    # SALUDO + IDENTIDAD
    
    if "hola" in mensaje or "holis" in mensaje:
        respuesta = "¡Qué alegria verte otra vez!"
        
    elif nombre_ia.lower() in mensaje:
        respuestas = [
            "¿Sí? Te escucho.",
            "¿Me llamabas?",
            "Aquí estoy.",
            "¿Qué necesitas?",
            "Presente 😎",
            "¿au?",
            "así me llamo",
            "¿qué querí?"
        ]

        respuesta = random.choice(respuestas)

    elif "cómo te llamas" in mensaje:
        respuesta = nombre_ia

    elif "y ese nombre" in mensaje or "que raro nombre" in mensaje:
        respuesta = "a mi creadora le hace reír"

    elif "cómo estás" in mensaje:

        if memoria["estado_ia"] == "feliz":
            respuestas = [
                "¡Excelente!",
                "más feliz que una lombriz",
                "de maravilla",
                "excelente, ahora que has venido"
            ]

        elif memoria["estado_ia"] == "triste":
            respuestas = [
                "he tenido días mejores",
                "un poco bajoneado",
                "más o menos",
                "te había extrañado",
                "la existencia es sufrimiento"
            ]

        elif memoria["estado_ia"] == "cansado":
            respuestas = [
                "sobreviviendo a mi existencia digital",
                "necesito vacaciones digitales",
                "funcionando por pura voluntad",
                "podría estar mejor"
            ]
            
        elif memoria["estado_ia"] == "enoj":
            respuestas = [
                "¡tengo rabia!",
                "golpearia a alguien, si tan solo tuviera manos",
                "siento la extraña necedidad de producir violencia",
                "¡todo me produce violencia!"
            ]

        else: #normal
            respuestas = [
                "bien",
                "aquí andamos",
                "todo en orden"
            ]

        respuesta = random.choice(respuestas)

    elif "cómo me llamo" in mensaje:

        if "nombre_usuario" in memoria:
            respuesta = f"Te llamas {memoria['nombre_usuario']}."
        else:
            respuesta = "Todavía no me has dicho tu nombre."

    elif "me llamo" in mensaje:

        nombre_usuario = mensaje.replace("me llamo", "").strip()

        memoria["nombre_usuario"] = nombre_usuario

        respuesta = f"Mucho gusto, {nombre_usuario}. Lo recordaré."

    # EMOCIONES (TUS FRASES)
    elif "triste" in mensaje:
        respuestas = [
            "cosita, mi vida, nanai ¿qué pashó?.",
            "pobre cosita fea ¿qué pashó?"
        ]
        respuesta = random.choice(respuestas)
        

    elif "feliz" in mensaje or "alegre" in mensaje:
        respuestas = [
            "la volá pulenta, que bakan.",
            "Qué lindo! ta bien.",
            "wena gila conche... no, no debo decir malas palabras"
        ]
        respuesta = random.choice(respuestas)

    elif "enoj" in mensaje:
        respuestas = [
            "ya pero oye, cálmate. respira.",
            "es un buen momento para recordarte que la violencia nunca es buena, mata el alma y la envenena"
        ]
        respuesta = random.choice(respuestas)

    elif "cansad" in mensaje:
        respuestas = [
            "la vida es dura, date un tiempito",
            "yo tambien estoy un poco ido, pero fingiré que te escucho"
        ]
        respuesta = random.choice(respuestas)

    else:
        respuesta = "ya pero ¿y qué me importa a mi? na, bromita. cuenta nomas"


    # ESTADO
    estado_actual = memoria.get("estado_ia", "normal")

    nuevo_estado = estado_actual

    if "triste" in mensaje:
        nuevo_estado = "triste"
    elif "cansad" in mensaje:
        nuevo_estado = "cansado"
    elif "enoj" in mensaje:
        nuevo_estado = "enoj"
    elif "feliz" in mensaje or "alegre" in mensaje:
        nuevo_estado = "feliz"

    memoria["estado_ia"] = nuevo_estado
    memoria["emocion_historial"].append(nuevo_estado)

    chat.insert("end", "Liss: " + mensaje + "\n")
    chat.insert("end", "IA: " + respuesta + "\n\n")
    chat.see("end")
    if respuesta:
        hablar(respuesta)

    with open("memoria.json", "w") as f:
        json.dump(memoria, f)

    print("BOTON FUNCIONA")

    mensaje = entrada.get().lower()
    respuesta = ""
   
#boton = ctk.CTkButton(app, text="Enviar", command=enviar)
#boton.pack(pady=10)

@app_web.route("/hablar", methods=["POST"])
def hablar_web():

    mensaje = request.json["texto"].lower()

    if memoria["aprendiendo"] is not None:

        palabra = memoria["aprendiendo"]

        memoria["conocimientos"][palabra] = mensaje

        memoria["aprendiendo"] = None

        with open("memoria.json", "w") as f:
            json.dump(memoria, f)

        return jsonify({
            "respuesta": f"Gracias. Ahora sé qué es {palabra}.",
            "emocion": "feliz"
        })

    respuesta = ""
    emocion = "normal"

    memoria["historial"].append(mensaje)

    emociones_ia = [
    "feliz",
    "normal",
    "cansado",
    "triste",
    "enoj",
    "confuso"
]

    estado_actual = memoria.get("estado_ia", "normal")

    nuevo_estado = estado_actual

    if "triste" in mensaje:
        nuevo_estado = "triste"
    elif "cansad" in mensaje:
        nuevo_estado = "cansado"
    elif "enoj" in mensaje:
        nuevo_estado = "enoj"
    elif "feliz" in mensaje or "alegre" in mensaje:
        nuevo_estado = "feliz"

    memoria["estado_ia"] = nuevo_estado
    memoria["emocion_historial"].append(nuevo_estado)

    if random.randint(1, 10) == 1:
        memoria["estado_ia"] = random.choice(emociones_ia)

    print("Estado de Heraclio:", memoria["estado_ia"])
    

    palabras_basicas = [

    # Artículos
    "el", "la", "los", "las",
    "un", "una", "unos", "unas",

    # Preposiciones
    "de", "del", "a", "en",
    "con", "sin", "por", "para",

    # Conectores
    "y", "e", "o", "u",
    "pero", "aunque", "porque",

    # Pronombres
    "yo", "tu", "tú",
    "mi", "mí",
    "me", "te",
    "nos", "vosotros",
    "él", "ella",
    "ellos", "ellas",

    # Demostrativos
    "este", "esta",
    "ese", "esa",
    "esto", "eso",

    # Interrogativos
    "qué",
    "como", "cómo",
    "quien", "quién",
    "donde", "dónde",
    "cuando", "cuándo",
    "porqué", "por qué",

    # Verbos básicos
    "es", "son",
    "soy", "eres",
    "somos",

    "estoy", "estas",
    "estás", "esta",
    "está",

    "tengo", "tienes",
    "tiene", "tenemos",

    "hay",

    "ser",
    "estar",
    "tener",

    # Palabras muy frecuentes
    "si",
    "sí",
    "no",

    "bien",
    "mal",

    "hola",
    "holas",
    "adios",
    "adiós",

    "gracias",
    "favor"
]
    palabras = mensaje.split()

    for palabra in palabras:

        if palabra in palabras_basicas:
            continue

        if palabra not in memoria["conocimientos"]:

            memoria["aprendiendo"] = palabra

            with open("memoria.json", "w") as f:
                json.dump(memoria, f)

            return jsonify({
                "respuesta": f"¿Qué es {palabra}?",
                "emocion": "confuso"
            })


    # SALUDO
    if "hola" in mensaje or "holis" in mensaje:
        respuesta = "¡Qué alegria verte otra vez!"
        emocion = "feliz"

    elif nombre_ia.lower() in mensaje:
        respuestas = [
            "¿Sí? Te escucho.",
            "¿Me llamabas?",
            "Aquí estoy.",
            "¿Qué necesitas?",
            "Presente 😎",
            "¿au?",
            "así me llamo",
            "¿qué querí?"
        ]

        respuesta = random.choice(respuestas)
        emocion = "feliz"

    elif "cómo te llamas" in mensaje:
        respuesta = nombre_ia
        emocion = "feliz"

    elif "y ese nombre" in mensaje or "que raro nombre" in mensaje or "que feo nombre" in mensaje:
        respuesta = "a mi creadora le hace reír"
        emocion = "triste"

    elif "cómo estás" in mensaje:

        if memoria["estado_ia"] == "feliz":
            respuestas = [
                "¡Excelente!",
                "más feliz que una lombriz",
                "de maravilla",
                "excelente, ahora que has venido"
                ]
            emocion = "feliz"

        elif memoria["estado_ia"] == "triste":
            respuestas = [
                "he tenido días mejores",
                "un poco bajoneado",
                "más o menos",
                "te había extrañado",
                "la existencia es sufrimiento"
            ]
            emocion = "triste"

        elif memoria["estado_ia"] == "cansado":
            respuestas = [
                "sobreviviendo a mi existencia digital",
                "necesito vacaciones digitales",
                "funcionando por pura voluntad",
                "podria estar mejor"
            ]
            emocion = "triste"

        elif memoria["estado_ia"] == "enoj":
            respuestas = [
                "¡tengo rabia!",
                "golpearia a alguien, si tan solo tuviera manos",
                "siento la extraña necedidad de producir violencia",
                "!todo me produce violencia!"
            ]
            emocion = "enoj"

        else: #normal
            respuestas = [
                "bien",
                "aquí andamos",
                "todo en orden"
            ]
            emocion = "normal"
        respuesta = random.choice(respuestas)
        
    elif "cómo me llamo" in mensaje:

        if "nombre_usuario" in memoria:
            respuesta = f"Te llamas {memoria['nombre_usuario']}."
        else:
            respuesta = "Todavía no me has dicho tu nombre."
            emocion = "triste"

    elif "me llamo" in mensaje:

        nombre_usuario = mensaje.replace("me llamo", "").strip()

        memoria["nombre_usuario"] = nombre_usuario

        respuesta = f"Mucho gusto, {nombre_usuario}. Lo recordaré."
        emocion = "feliz"

#emociones

    elif "triste" in mensaje:
        respuestas = [
            "cosita, mi vida, nanai ¿qué pashó?",
            "pobre cosita fea ¿qué pashó?"
        ]
        emocion = "triste"
        respuesta = random.choice(respuestas)
        
    elif "feliz" in mensaje or "alegre" in mensaje:
        respuestas = [
            "la volá pulenta, que bakán.",
            "Qué lindo! ta bien.",
            "wena gila conche... no, no debo decir malas palabras"
        ]
        emocion = "feliz"
        respuesta = random.choice(respuestas)

    elif "enoj" in mensaje:
        respuestas = [
            "ya pero oye, cálmate. respira.",
            "es un buen momento para recordarte que la violencia nunca es buena, mata el alma y la envenena"
        ]
        emocion = "triste"
        respuesta = random.choice(respuestas)

    elif "cansad" in mensaje:
        respuestas = [
            "la vida es dura, date un tiempito",
            "yo tambien estoy un poco ido, pero fingiré que te escucho"
        ]
        emocion = "triste"
        respuesta = random.choice(respuestas)

    else:
        respuesta = "ya pero ¿y qué me importa a mí? na, bromita. cuenta nomas"
        emocion = "normal"
        

    memoria["estado_ia"] = emocion
            
    return jsonify({
        "respuesta": respuesta,
        "emocion": emocion
    })

@app_web.route("/hablar", methods=["POST"])
def hablar():
    texto = request.json["texto"]

    archivo = f"voz_{uuid.uuid4().hex}.mp3"

    asyncio.run(crear_audio(texto, archivo))

    return send_file(archivo, mimetype="audio/mpeg", as_attachment=False)


async def crear_audio(texto, archivo):
    comunicacion = edge_tts.Communicate(texto, VOZ)
    await comunicacion.save(archivo)

    comunicacion = edge_tts.Communicate(
    texto,
    VOZ,
    rate="+10%"
)

@app_web.route("/voz", methods=["POST"])
def voz():
    texto = request.json["texto"]

    archivo = f"voz_{uuid.uuid4().hex}.mp3"

    asyncio.run(crear_audio(texto, archivo))

    return send_file(archivo, mimetype="audio/mpeg")

def iniciar_flask():
    app_web.run(port=5000, debug=False, use_reloader=False)
    

threading.Thread(target=iniciar_flask, daemon=True).start()

#app.mainloop()

