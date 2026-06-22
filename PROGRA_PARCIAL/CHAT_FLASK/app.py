import os
import threading
import asyncio
from flask import Flask, render_template
from flask_socketio import SocketIO, send
from dotenv import load_dotenv
from telegram import Bot
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from google import genai

# Cargar variables de entorno
load_dotenv()
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
API_KEY = os.getenv("GEMINI_API_KEY")

# Nueva forma de configurar Gemini
client = genai.Client(api_key=API_KEY)

# Instancias
bot_instance = Bot(token=TOKEN)
app = Flask(__name__)
socketio = SocketIO(app)

def consultar_gemini(texto):
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=f"Eres un asistente de la UDABOL. Responde de forma amable: {texto}",
        )
        return response.text
    except Exception as e:
        return f"⚠️ Error IA: {str(e)}"

# --- BOT TELEGRAM ---
async def responder_telegram(update, context):
    texto = update.message.text
    respuesta = consultar_gemini(texto)
    await update.message.reply_text(respuesta)
    socketio.emit("message", f"👤 Usuario: {texto}")
    socketio.emit("message", f"🤖 IA: {respuesta}")

def run_bot():
    # Usamos un nuevo loop para evitar conflictos con Flask
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    app_bot = ApplicationBuilder().token(TOKEN).build()
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder_telegram))
    print("🤖 Bot Telegram iniciado...")
    app_bot.run_polling()

# --- WEB SOCKET ---
@socketio.on("message")
def handle_msg(msg):
    respuesta = consultar_gemini(msg)
    send(f"👤 Tú: {msg}", broadcast=True)
    send(f"🤖 IA: {respuesta}", broadcast=True)
    # Reenvío a Telegram
    try:
        asyncio.run(bot_instance.send_message(chat_id=CHAT_ID, text=f"🌐 Web: {msg}\n🤖 IA: {respuesta}"))
    except Exception as e:
        print(f"Error enviando a Telegram: {e}")

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    # Iniciar bot en hilo separado
    threading.Thread(target=run_bot, daemon=True).start()
    # Iniciar Flask
    socketio.run(app, host="127.0.0.1", port=5000, debug=False)