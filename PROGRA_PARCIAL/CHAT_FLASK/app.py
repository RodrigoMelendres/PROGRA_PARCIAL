import threading
import asyncio
import requests
import google.generativeai as genai

from flask import Flask, render_template
from flask_socketio import SocketIO, send

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# =========================
# CONFIGURACIÓN
# =========================

TOKEN = "8855798797:AAGCYmIcdYH_8JN75o_fShlU23E5cyydo50"
GEMINI_API_KEY = "AQ.Ab8RN6K206qLXuqKqmbzOldSgKpcExtuXT5owyiJksdrjL7hhw"

genai.configure(api_key=GEMINI_API_KEY)
modelo = genai.GenerativeModel("gemini-1.5-flash")

# =========================
# FLASK + SOCKETIO
# =========================

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# =========================
# GEMINI
# =========================

def consultar_gemini(texto):
    try:
        respuesta = modelo.generate_content(texto)
        return respuesta.text
    except:
        return "❌ Error en IA"

# =========================
# TELEGRAM BOT
# =========================

def menu_principal():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💻 Laptops", callback_data="laptops")],
        [InlineKeyboardButton("🖥️ PC Gamer", callback_data="gamer")],
        [InlineKeyboardButton("🔥 Ofertas", callback_data="ofertas")],
        [InlineKeyboardButton("🧠 Preguntar IA", callback_data="ia")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bienvenido a TechStore IA\nElige una opción:",
        reply_markup=menu_principal()
    )

async def botones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "laptops":
        await query.message.reply_text("💻 Lenovo, HP, ASUS desde Bs. 4500")

    elif query.data == "gamer":
        await query.message.reply_text("🖥️ Ryzen 7 + RTX 4060 desde Bs. 9999")

    elif query.data == "ofertas":
        await query.message.reply_text("🔥 Descuentos hasta 30%")

    elif query.data == "ia":
        await query.message.reply_text("Escribe tu pregunta directamente.")

async def responder_telegram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text

    respuesta = consultar_gemini(texto)

    await update.message.reply_text(respuesta)

    socketio.emit("message", f"📲 Telegram: {texto}")
    socketio.emit("message", f"🤖 IA: {respuesta}")

def iniciar_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    bot = ApplicationBuilder().token(TOKEN).build()

    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(CallbackQueryHandler(botones))
    bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder_telegram))

    print("🤖 Bot Telegram activo")
    bot.run_polling()

# =========================
# WEB SOCKET
# =========================

@socketio.on("message")
def handle_message(msg):

    print("WEB:", msg)

    send(msg, broadcast=True)

    respuesta = consultar_gemini(msg)

    send(f"🤖 IA: {respuesta}", broadcast=True)

# =========================
# WEB
# =========================

@app.route("/")
def index():
    return render_template("index.html")

# =========================
# MAIN
# =========================

if __name__ == "__main__":
    hilo = threading.Thread(target=iniciar_bot, daemon=True)
    hilo.start()

    print("🌐 Servidor iniciado en http://localhost:5000")

    socketio.run(app, host="0.0.0.0", port=5000, debug=True)