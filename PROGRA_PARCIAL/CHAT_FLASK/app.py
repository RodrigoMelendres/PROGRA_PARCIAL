from flask import Flask, render_template
from flask_socketio import SocketIO, send

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def inicio():
    return render_template("index.html")

@socketio.on("message")
def recibir_mensaje(mensaje):
    send(mensaje, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)