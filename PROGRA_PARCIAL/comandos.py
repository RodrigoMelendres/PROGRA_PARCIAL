from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update

TOKEN = "8855798797:AAGCYmIcdYH_8JN75o_fShlU23E5cyydo50"

def get_respuesta(texto):
    respuestas = {
        "/laptops": "💻 Laptops: Lenovo, HP, ASUS, Dell.",
        "/pcgamer": "🖥️ PC Gamer: Ryzen 5/7 + RTX 3060/4060.",
        "/ofertas": "🔥 Ofertas: Desde Bs. 3.999."
    }
    return respuestas.get(texto.lower(), "Comando no reconocido. Prueba /laptops")

async def manejar_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text
    respuesta = get_respuesta(texto)
    await update.message.reply_text(respuesta)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Maneja cualquier mensaje (incluyendo los que enviaste desde la web)
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), manejar_mensaje))
    # Maneja comandos específicos
    for cmd in ["laptops", "pcgamer", "ofertas"]:
        app.add_handler(CommandHandler(cmd, manejar_mensaje))

    print("🤖 Bot conectado a la API de Telegram...")
    app.run_polling()

if __name__ == "__main__":
    main()