import threading
from flask import Flask, render_template
from flask_socketio import SocketIO
from telegram.ext import ApplicationBuilder, MessageHandler, filters
import asyncio

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

TOKEN = "8855798797:AAGCYmIcdYH_8JN75o_fShlU23E5cyydo50"

# --- LÓGICA DEL BOT ---
async def responder_telegram(update, context):
    texto = update.message.text.lower()
    respuestas = {
        "/laptops": "💻 Laptops: Lenovo, HP, ASUS, Dell.",
        "/pcgamer": "🖥️ PC Gamer: Ryzen 5/7 + RTX 3060/4060.",
        "/ofertas": "🔥 Ofertas: Desde Bs. 3.999."
    }
    await update.message.reply_text(respuestas.get(texto, "Comando no reconocido."))

def iniciar_bot():
    # Usamos una nueva instancia de event loop para el bot
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    bot_app = ApplicationBuilder().token(TOKEN).build()
    bot_app.add_handler(MessageHandler(filters.TEXT, responder_telegram))
    bot_app.run_polling()

# --- RUTAS WEB ---
@app.route("/")
def inicio():
    return render_template("index.html")

@socketio.on("message")
def manejar_mensaje(mensaje):
    socketio.send(mensaje, broadcast=True)

if __name__ == "__main__":
    # Iniciar el bot en un hilo separado
    hilo_bot = threading.Thread(target=iniciar_bot, daemon=True)
    hilo_bot.start()
    # Iniciar la web
    socketio.run(app, host="0.0.0.0", port=5000)