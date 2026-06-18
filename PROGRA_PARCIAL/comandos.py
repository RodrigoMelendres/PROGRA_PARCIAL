from telegram.ext import ApplicationBuilder, MessageHandler, filters
from telegram import Update

TOKEN = "8855798797:AAGCYmIcdYH_8JN75o_fShlU23E5cyydo50"

# Lógica central
def procesar(texto):
    diccionario = {
        "/laptops": "💻 Laptops: Lenovo, HP, ASUS, Dell.",
        "/pcgamer": "🖥️ PC Gamer: Ryzen 5/7 + RTX 3060/4060.",
        "/ofertas": "🔥 Ofertas: Desde Bs. 3.999."
    }
    return diccionario.get(texto.lower(), "Comando no reconocido.")

async def responder(update: Update, context):
    texto = update.message.text
    respuesta = procesar(texto)
    await update.message.reply_text(respuesta)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    # Este filtro captura cualquier texto, incluyendo los comandos enviados desde la web
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), responder))
    # Para los comandos reales escritos en Telegram
    app.add_handler(MessageHandler(filters.COMMAND, responder))
    
    print("🤖 Bot escuchando...")
    app.run_polling()

if __name__ == "__main__":
    main()