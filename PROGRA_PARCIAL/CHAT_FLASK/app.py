from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import requests

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

TOKEN = "8855798797:AAGCYmIcdYH_8JN75o_fShlU23E5cyydo50"
# IMPORTANTE: Pon aquí el ID de tu propio chat con el bot
# Para obtenerlo: inicia tu bot, ve a https://api.telegram.org/botTU_TOKEN/getUpdates
MI_CHAT_ID = "TU_ID_AQUI" 

@app.route("/")
def inicio():
    return render_template("index.html")

@socketio.on("message")
def manejar_mensaje(mensaje):
    # 1. Mostrar en el chat web
    socketio.send(mensaje, broadcast=True)
    
    # 2. Enviar a Telegram vía API
    if ":" in mensaje:
        texto = mensaje.split(":")[1].strip()
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": MI_CHAT_ID, "text": texto})

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)