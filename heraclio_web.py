import json
import random
import threading

from flask import Flask, request, jsonify
from flask_cors import CORS

app_web = Flask(__name__)
CORS(app_web)

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

# VENTANA
#ctk.set_appearance_mode("dark")

#app = ctk.CTk()
#app.geometry("450x500")
#app.title("Mi IA 💙")

#chat = ctk.CTkTextbox(app, width=400, height=300)
#chat.pack(pady=20)

#entrada = ctk.CTkEntry(app, placeholder_text="Escribe aquí...")
#entrada.pack(pady=10)

def enviar():

    mensaje = entrada.get().lower()
    respuesta = ""

    memoria["historial"].append(mensaje)

    emociones_ia = [
    "feliz",
    "normal",
    "cansado",
    "triste",
    "enoj"
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
            "asi me llamo",
            "¿qué querí?"
        ]

        respuesta = random.choice(respuestas)

    elif "como te llamas" in mensaje:
        respuesta = nombre_ia

    elif "y ese nombre" in mensaje or "que raro nombre" in mensaje:
        respuesta = "a mi creadora le hace reir"

    elif "como estas" in mensaje:

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
                "te habia extrañado",
                "la existencia es sufrimiento"
            ]

        elif memoria["estado_ia"] == "cansado":
            respuestas = [
                "sobreviviendo a mi existencia digital",
                "necesito vacaciones digitales",
                "funcionando por pura voluntad",
                "podria estar mejor"
            ]
            
        elif memoria["estado_ia"] == "enoj":
            respuestas = [
                "¡tengo rabia!",
                "golpearia a alguien, si tan solo tuviera manos",
                "siento la extraña necedidad de prducir violencia",
                "!todo me produce violencia!"
            ]

        else: #normal
            respuestas = [
                "bien",
                "aquí andamos",
                "todo en orden"
            ]

        respuesta = random.choice(respuestas)

    elif "como me llamo" in mensaje:

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
            "cosita, mi vida, nanai ¿qué pasho?.",
            "pobre cosita fea ¿qué pasho?"
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
            "ya pero oye, calmate. respira.",
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
        respuesta = "ya pero ¿y que me importa a mi? na, bromita. cuenta nomas"


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

    respuesta = ""
    emocion = "normal"

    memoria["historial"].append(mensaje)

    emociones_ia = [
    "feliz",
    "normal",
    "cansado",
    "triste",
    "enoj"
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
            "asi me llamo",
            "¿qué querí?"
        ]

        respuesta = random.choice(respuestas)
        emocion = "feliz"

    elif "como te llamas" in mensaje:
        respuesta = nombre_ia
        emocion = "feliz"

    elif "y ese nombre" in mensaje or "que raro nombre" in mensaje:
        respuesta = "a mi creadora le hace reir"
        emocion = "triste"

    elif "como estas" in mensaje:

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
                "te habia extrañado",
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
                "siento la extraña necedidad de prducir violencia",
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
        
    elif "como me llamo" in mensaje:

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
            "cosita, mi vida, nanai ¿qué pasho?.",
            "pobre cosita fea ¿qué pasho?"
        ]
        emocion = "triste"
        respuesta = random.choice(respuestas)
        
    elif "feliz" in mensaje or "alegre" in mensaje:
        respuestas = [
            "la volá pulenta, que bakan.",
            "Qué lindo! ta bien.",
            "wena gila conche... no, no debo decir malas palabras"
        ]
        emocion = "feliz"
        respuesta = random.choice(respuestas)

    elif "enoj" in mensaje:
        respuestas = [
            "ya pero oye, calmate. respira.",
            "es un buen momento para recordarte que la violencia nunca es buena, mata el alma y la envenena"
        ]
        emocion = "enoj"
        respuesta = random.choice(respuestas)

    elif "cansad" in mensaje:
        respuestas = [
            "la vida es dura, date un tiempito",
            "yo tambien estoy un poco ido, pero fingiré que te escucho"
        ]
        emocion = "triste"
        respuesta = random.choice(respuestas)

    else:
        respuesta = "ya pero ¿y que me importa a mi? na, bromita. cuenta nomas"
        emocion = "normal"
        

    memoria["estado_ia"] = emocion
            
    return jsonify({
        "respuesta": respuesta,
        "emocion": emocion
    })


def iniciar_flask():
    app_web.run(port=5000, debug=False, use_reloader=False)
    

threading.Thread(target=iniciar_flask, daemon=True).start()

#app.mainloop()

