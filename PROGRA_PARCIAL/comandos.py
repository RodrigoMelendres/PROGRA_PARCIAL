import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# CONFIGURACIÓN
TOKEN = "8855798797:AAGCYmIcdYH_8JN75o_fShlU23E5cyydo50"
URL_WEB = "http://127.0.0.1:5000/enviar-mensaje"

# Función para enviar datos al Chat Web
async def notificar_al_chat(texto):
    try:
        requests.post(URL_WEB, json={"texto": texto})
    except Exception as e:
        print(f"No se pudo conectar al chat web: {e}")

# --- COMANDOS ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "¡Bienvenido a TechStore Bolivia! Usa los comandos /catalogo, /laptops, /pcgamer, /accesorios, /ofertas, /contacto o /ubicacion."
    await update.message.reply_text(msg)

async def laptops(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "💻 Laptops: Lenovo, HP, ASUS, Dell. ¡Gran variedad en stock!"
    await update.message.reply_text(msg)
    await notificar_al_chat(msg)

async def pcgamer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "🖥️ PC Gamer: Ryzen 5/7 con RTX 3060/4060. Armado a medida."
    await update.message.reply_text(msg)
    await notificar_al_chat(msg)

async def accesorios(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "🎧 Accesorios: Teclados RGB, Mouse Gamer, Headsets y más."
    await update.message.reply_text(msg)
    await notificar_al_chat(msg)

async def ofertas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "🔥 ¡Ofertas! Lenovo IdeaPad desde Bs. 3.999 y PC Gamer desde Bs. 6.500."
    await update.message.reply_text(msg)
    await notificar_al_chat(msg)

async def contacto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "☎️ Contacto: WhatsApp 72456013 - TechStore Bolivia."
    await update.message.reply_text(msg)

async def ubicacion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "📍 Estamos ubicados en Oruro - Bolivia."
    await update.message.reply_text(msg)

# --- MAIN ---

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("laptops", laptops))
    app.add_handler(CommandHandler("pcgamer", pcgamer))
    app.add_handler(CommandHandler("accesorios", accesorios))
    app.add_handler(CommandHandler("ofertas", ofertas))
    app.add_handler(CommandHandler("contacto", contacto))
    app.add_handler(CommandHandler("ubicacion", ubicacion))

    print("🤖 Bot TechStore listo...")
    app.run_polling()

if __name__ == "__main__":
    main()