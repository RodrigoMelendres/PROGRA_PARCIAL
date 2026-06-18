from flask import Flask, render_template
from flask_socketio import SocketIO

# 1. Inicialización de la aplicación
app = Flask(__name__)
# 2. Inicialización de SocketIO (DEBE ir después de definir 'app')
socketio = SocketIO(app, cors_allowed_origins="*")

# 3. Definición de rutas
@app.route("/")
def inicio():
    return render_template("index.html")

# 4. Definición de eventos de chat
@socketio.on("message")
def manejar_mensaje(mensaje):
    # Enviar el mensaje original al chat
    socketio.send(mensaje, broadcast=True)
    
    # Lógica para detectar comandos y responder automáticamente
    # Limpiamos el mensaje: si llega "Nombre: /comando", tomamos "/comando"
    if ":" in mensaje:
        comando = mensaje.split(":")[1].strip().lower()
    else:
        comando = mensaje.strip().lower()

    # Diccionario de respuestas automáticas
    respuestas = {
        "/laptops": "💻 Laptops: Lenovo, HP, ASUS, Dell. ¡Gran variedad en stock!",
        "/pcgamer": "🖥️ PC Gamer: Ryzen 5/7 con RTX 3060/4060. Armado a medida.",
        "/ofertas": "🔥 Ofertas: Lenovo IdeaPad desde Bs. 3.999.",
        "/accesorios": "🎧 Accesorios: Teclados RGB, Mouse Gamer, Headsets.",
        "/contacto": "☎️ WhatsApp: 72456013 - TechStore Bolivia.",
        "/ubicacion": "📍 Estamos ubicados en Oruro - Bolivia."
    }

    # Si el mensaje es un comando reconocido, respondemos
    if comando in respuestas:
        socketio.send(f"🤖 Bot TechStore: {respuestas[comando]}", broadcast=True)

# 5. Ejecución del servidor
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)