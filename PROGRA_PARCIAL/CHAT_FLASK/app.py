from flask import Flask, render_template
from flask_socketio import SocketIO
import requests

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

TOKEN = "8855798797:AAGCYmIcdYH_8JN75o_fShlU23E5cyydo50"
MI_CHAT_ID = "7233717619" 

@app.route("/")
def inicio():
    return render_template("index.html")

@socketio.on("message")
def manejar_mensaje(mensaje):
    socketio.send(mensaje, broadcast=True)
    # Enviamos el mensaje tal cual a tu Telegram
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": MI_CHAT_ID, "text": mensaje})

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)