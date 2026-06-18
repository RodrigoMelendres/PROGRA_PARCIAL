from telegram.ext import ApplicationBuilder, CommandHandler
from telegram import Update

TOKEN = "8855798797:AAGCYmIcdYH_8JN75o_fShlU23E5cyydo50"

def obtener_respuesta(cmd):
    respuestas = {
        "/laptops": "💻 Laptops: Lenovo, HP, ASUS, Dell.",
        "/pcgamer": "🖥️ PC Gamer: Ryzen 5/7 + RTX 3060/4060.",
        "/ofertas": "🔥 Ofertas: Desde Bs. 3.999."
    }
    return respuestas.get(cmd, "Comando no reconocido.")

async def comando_general(update: Update, context):
    cmd = f"/{update.message.text.split()[0].replace('/', '')}"
    respuesta = obtener_respuesta(cmd)
    await update.message.reply_text(respuesta)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    comandos = ["laptops", "pcgamer", "ofertas", "accesorios", "contacto", "ubicacion"]
    for cmd in comandos:
        app.add_handler(CommandHandler(cmd, comando_general))
    
    print("🤖 Bot listo para responder a comandos...")
    app.run_polling()

if __name__ == "__main__":
    main()