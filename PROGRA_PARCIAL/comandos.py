from telegram.ext import ApplicationBuilder, MessageHandler, filters
from telegram import Update

TOKEN = "8855798797:AAGCYmIcdYH_8JN75o_fShlU23E5cyydo50"

def get_respuesta(texto):
    # Limpiamos el texto por si viene con el formato "Nombre: /comando"
    if ":" in texto:
        texto = texto.split(":")[1].strip()
    
    respuestas = {
        "/laptops": "💻 Laptops: Lenovo, HP, ASUS, Dell.",
        "/pcgamer": "🖥️ PC Gamer: Ryzen 5/7 + RTX 3060/4060.",
        "/ofertas": "🔥 Ofertas: Desde Bs. 3.999.",
        "/accesorios": "🎧 Accesorios: Teclados, Mouse, Headsets.",
        "/contacto": "☎️ WhatsApp: 72456013.",
        "/ubicacion": "📍 Oruro - Bolivia."
    }
    return respuestas.get(texto.lower(), "Comando no reconocido. Prueba /laptops")

async def responder(update: Update, context):
    texto = update.message.text
    respuesta = get_respuesta(texto)
    await update.message.reply_text(respuesta)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    # Este filtro captura todo el texto que entra al chat
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), responder))
    # Esto captura los comandos directos también
    app.add_handler(MessageHandler(filters.COMMAND, responder))
    
    print("🤖 Bot escuchando en Telegram...")
    app.run_polling()

if __name__ == "__main__":
    main()