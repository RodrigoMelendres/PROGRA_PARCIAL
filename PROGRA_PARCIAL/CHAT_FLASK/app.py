from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import requests

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Configuración de tu Bot
TOKEN = "8855798797:AAGCYmIcdYH_8JN75o_fShlU23E5cyydo50"
CHAT_ID = "7233717619" # Debes poner aquí tu ID personal para que el bot te responda

def enviar_a_telegram(texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": texto, "parse_mode": "HTML"})

@app.route("/")
def inicio():
    return render_template("index.html")

@socketio.on("message")
def manejar_mensaje(mensaje):
    # Enviar al chat web
    socketio.send(mensaje, broadcast=True)
    
    # Si el usuario escribió un comando en el chat web
    if ":" in mensaje:
        comando = mensaje.split(":")[1].strip().lower()
        if comando.startswith("/"):
            # Enviamos el comando a Telegram para que el bot lo procese
            enviar_a_telegram(f"Comando recibido desde Web: {comando}")

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)