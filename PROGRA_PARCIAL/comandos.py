import requests
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8855798797:AAGCYmIcdYH_8JN75o_fShlU23E5cyydo50"

# Lógica centralizada de respuestas
def obtener_respuesta(comando):
    respuestas = {
        "laptops": "💻 Laptops: Lenovo, HP, ASUS, Dell. ¡Gran variedad en stock!",
        "pcgamer": "🖥️ PC Gamer: Ryzen 5/7 con RTX 3060/4060. Armado a medida.",
        "accesorios": "🎧 Accesorios: Teclados RGB, Mouse Gamer, Headsets.",
        "ofertas": "🔥 Ofertas: Lenovo IdeaPad desde Bs. 3.999.",
        "contacto": "☎️ WhatsApp: 72456013 - TechStore Bolivia.",
        "ubicacion": "📍 Estamos ubicados en Oruro - Bolivia."
    }
    return respuestas.get(comando, None)

async def manejar_comando(update, context):
    cmd = update.message.text.replace("/", "")
    respuesta = obtener_respuesta(cmd)
    
    if respuesta:
        await update.message.reply_text(respuesta)
        # Enviar también al chat web
        try:
            requests.post("http://127.0.0.1:5000/enviar-mensaje", json={"texto": respuesta})
        except:
            pass
    else:
        await update.message.reply_text("Comando no reconocido.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    comandos = ["laptops", "pcgamer", "accesorios", "ofertas", "contacto", "ubicacion"]
    for cmd in comandos:
        app.add_handler(CommandHandler(cmd, manejar_comando))
    
    print("🤖 Bot TechStore iniciado.")
    app.run_polling()

if __name__ == "__main__":
    main()