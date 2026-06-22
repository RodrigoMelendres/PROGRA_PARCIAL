import os
import threading
import asyncio
import google.generativeai as genai
from flask import Flask, render_template
from flask_socketio import SocketIO, send
from dotenv import load_dotenv
from telegram import Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Cargar configuración
load_dotenv()
TOKEN = os.getenv("TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CHAT_ID = os.getenv("CHAT_ID") # Debes agregar tu ID de Telegram en el .env

# Configurar IA
genai.configure(api_key=GEMINI_API_KEY)
modelo = genai.GenerativeModel("gemini-1.5-flash")

# Instancias
bot_instance = Bot(token=TOKEN)
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

def consultar_gemini(texto):
    try:
        respuesta = modelo.generate_content(f"Eres un asistente de UDABOL: {texto}")
        return respuesta.text
    except Exception as e:
        return f"⚠️ Error IA: {str(e)}"

# --- LÓGICA DE TELEGRAM ---
async def responder_telegram(update, context):
    texto = update.message.text
    respuesta = consultar_gemini(texto)
    await update.message.reply_text(respuesta)
    socketio.emit("message", f"👤 Tel: {texto}")
    socketio.emit("message", f"🤖 IA: {respuesta}")

def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    app_bot = ApplicationBuilder().token(TOKEN).build()
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder_telegram))
    app_bot.run_polling()

# --- LÓGICA WEB ---
@socketio.on("message")
def handle_msg(msg):
    respuesta = consultar_gemini(msg)
    send(f"👤 Tú: {msg}", broadcast=True)
    send(f"🤖 IA: {respuesta}", broadcast=True)
    # Enviar a Telegram de forma sincrónica
    asyncio.run(bot_instance.send_message(chat_id=CHAT_ID, text=f"🌐 Web: {msg}\n🤖 IA: {respuesta}"))

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    socketio.run(app, host="0.0.0.0", port=5000)