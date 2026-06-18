from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO

app = Flask(__name__)
# Permitimos CORS para que el bot pueda enviar datos desde fuera
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/")
def inicio():
    return render_template("index.html")

# Ruta para que el Bot de Telegram envíe información al chat
@app.route("/enviar-mensaje", methods=["POST"])
def recibir_de_bot():
    data = request.json
    mensaje = data.get("texto", "Mensaje del Bot")
    # Emitimos el mensaje a todos los conectados en el chat
    socketio.send(f"🤖 Bot TechStore: {mensaje}", broadcast=True)
    return jsonify({"status": "éxito"}), 200

@socketio.on("message")
def recibir_mensaje(mensaje):
    socketio.send(mensaje, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)