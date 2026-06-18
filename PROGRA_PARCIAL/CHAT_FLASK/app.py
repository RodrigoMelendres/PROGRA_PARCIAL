from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Lógica centralizada de respuestas
def obtener_respuesta(comando):
    respuestas = {
        "/laptops": "💻 Laptops: Lenovo, HP, ASUS, Dell. ¡Gran variedad en stock!",
        "/pcgamer": "🖥️ PC Gamer: Ryzen 5/7 con RTX 3060/4060. Armado a medida.",
        "/accesorios": "🎧 Accesorios: Teclados RGB, Mouse Gamer, Headsets.",
        "/ofertas": "🔥 Ofertas: Lenovo IdeaPad desde Bs. 3.999.",
        "/contacto": "☎️ WhatsApp: 72456013 - TechStore Bolivia.",
        "/ubicacion": "📍 Estamos ubicados en Oruro - Bolivia."
    }
    return respuestas.get(comando.lower(), None)

@app.route("/")
def inicio():
    return render_template("index.html")

# Ruta para que el Bot de Telegram envíe información
@app.route("/enviar-mensaje", methods=["POST"])
def recibir_de_bot():
    data = request.json
    mensaje = data.get("texto", "")
    socketio.send(f"🤖 Bot TechStore: {mensaje}", broadcast=True)
    return jsonify({"status": "éxito"}), 200

@socketio.on("message")
def manejar_mensaje(mensaje):
    # 1. Enviar el mensaje del usuario al chat
    socketio.send(mensaje, broadcast=True)
    
    # 2. Si el mensaje es un comando, el bot responde
    if isinstance(mensaje, str) and ":" in mensaje:
        comando = mensaje.split(":")[1].strip()
        respuesta = obtener_respuesta(comando)
        if respuesta:
            socketio.send(f"🤖 Bot TechStore: {respuesta}", broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)