import os
import threading
import asyncio
import google.generativeai as genai
from flask import Flask, render_template
from flask_socketio import SocketIO, send
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# 1. Cargar variables de entorno desde el archivo .env
load_dotenv()
TOKEN = os.getenv("TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 2. Configuración de IA
genai.configure(api_key=GEMINI_API_KEY)
modelo = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

def consultar_gemini(texto):
    try:
        respuesta = modelo.generate_content(texto)
        return respuesta.text
    except Exception as e:
        print(f"Error IA: {e}")
        return "⚠️ Error al conectar con IA."

# --- TELEGRAM BOT ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 ¡Hola! Soy el asistente virtual de UDABOL. ¿En qué puedo ayudarte?")

async def responder_telegram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    respuesta = consultar_gemini(texto)
    await update.message.reply_text(respuesta)
    # Enviar al dashboard web
    socketio.emit("message", f"👤 Usuario (Tel): {texto}")
    socketio.emit("message", f"🤖 IA: {respuesta}")

def iniciar_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    bot = ApplicationBuilder().token(TOKEN).build()
    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder_telegram))
    bot.run_polling()

# --- WEB SOCKETS ---
@socketio.on("message")
def handle_message(msg):
    respuesta = consultar_gemini(msg)
    send(f"👤 Tú: {msg}", broadcast=True)
    send(f"🤖 IA: {respuesta}", broadcast=True)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    # Iniciar el bot en un hilo separado
    threading.Thread(target=iniciar_bot, daemon=True).start()
    # Iniciar servidor Flask
    socketio.run(app, host="0.0.0.0", port=5000, debug=False)