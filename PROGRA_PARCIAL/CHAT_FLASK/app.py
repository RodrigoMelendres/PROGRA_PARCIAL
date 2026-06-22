import os
import threading
import asyncio
import time
from flask import Flask, render_template
from flask_socketio import SocketIO, send
from dotenv import load_dotenv
from telegram import Bot
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from google import genai

# Cargar variables
load_dotenv()
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
API_KEY = os.getenv("GEMINI_API_KEY")

# Inicialización
client = genai.Client(api_key=API_KEY)
bot_instance = Bot(token=TOKEN)
app = Flask(__name__)
socketio = SocketIO(app, async_mode=None)

def consultar_gemini(texto):
    # Usamos un modelo más ligero (Lite) para mayor velocidad y menor saturación
    modelo_rapido = "models/gemini-2.0-flash-lite"
    
    try:
        # Petición con timeout implícito más rápido
        response = client.models.generate_content(
            model=modelo_rapido,
            contents=f"Eres un asistente de la UDABOL. Responde de forma directa, amable y muy breve: {texto}",
        )
        return response.text
    except Exception as e:
        # Fallback inmediato si el modelo Lite también falla
        return "⚠️ El servidor está muy ocupado, intenta de nuevo en un momento."

# --- BOT TELEGRAM ---
async def responder_telegram(update, context):
    texto = update.message.text
    respuesta = consultar_gemini(texto)
    await update.message.reply_text(respuesta)
    socketio.emit("message", f"👤 Usuario: {texto}")
    socketio.emit("message", f"🤖 IA: {respuesta}")

def run_bot():
    app_bot = ApplicationBuilder().token(TOKEN).build()
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder_telegram))
    print("🤖 Bot Telegram optimizado iniciado...")
    app_bot.run_polling()

# --- WEB SOCKET ---
@socketio.on("message")
def handle_msg(msg):
    respuesta = consultar_gemini(msg)
    send(f"👤 Tú: {msg}", broadcast=True)
    send(f"🤖 IA: {respuesta}", broadcast=True)
    
    if CHAT_ID:
        try:
            asyncio.run(bot_instance.send_message(chat_id=CHAT_ID, text=f"🌐 Web: {msg}\n🤖 IA: {respuesta}"))
        except: pass

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    socketio.run(app, host="127.0.0.1", port=5000, debug=False)