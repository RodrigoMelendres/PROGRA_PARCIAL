from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8855798797:AAGCYmIcdYH_8JN75o_fShlU23E5cyydo50"

# ==========================
# START
# ==========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    mensaje = """
<b>💻 TECHSTORE BOLIVIA 💻</b>

¡Bienvenido a nuestra tienda tecnológica!

📌 Comandos disponibles:

/catalogo
/laptops
/pcgamer
/accesorios
/ofertas
/contacto
/ubicacion
"""

    await update.message.reply_photo(
        photo="https://images.unsplash.com/photo-1518770660439-4636190af475",
        caption=mensaje,
        parse_mode="HTML"
    )

# ==========================
# CATALOGO
# ==========================
async def catalogo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_photo(
        photo="https://images.unsplash.com/photo-1496181133206-80ce9b88a853",
        caption="""
🛒 <b>CATÁLOGO GENERAL</b>

💻 Laptops
🖥️ PCs Gamer
⌨️ Teclados
🖱️ Mouse
🎧 Audífonos
📺 Monitores
""",
        parse_mode="HTML"
    )

# ==========================
# LAPTOPS
# ==========================
async def laptops(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_photo(
        photo="https://images.unsplash.com/photo-1496181133206-80ce9b88a853",
        caption="""
💻 <b>LAPTOPS DISPONIBLES</b>

✅ Lenovo IdeaPad
✅ HP Pavilion
✅ ASUS TUF Gaming
✅ Dell Inspiron

📦 Garantía incluida.
""",
        parse_mode="HTML"
    )

# ==========================
# PC GAMER
# ==========================
async def pcgamer(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_photo(
        photo="https://images.unsplash.com/photo-1587202372775-e229f172b9d7",
        caption="""
🖥️ <b>PC GAMER</b>

🔥 Ryzen 5 + RTX 3060
🔥 Ryzen 7 + RTX 4060
🔥 Intel i7 + RTX 4070

🎮 Armado personalizado.
""",
        parse_mode="HTML"
    )

# ==========================
# ACCESORIOS
# ==========================
async def accesorios(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_photo(
        photo="https://images.unsplash.com/photo-1545239351-1141bd82e8a6",
        caption="""
🎧 <b>ACCESORIOS</b>

⌨️ Teclados RGB
🖱️ Mouse Gamer
🎧 Headsets
📷 Webcams
🔊 Parlantes
""",
        parse_mode="HTML"
    )

# ==========================
# OFERTAS
# ==========================
async def ofertas(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        """
🔥 <b>OFERTAS DE LA SEMANA</b>

💻 Lenovo IdeaPad
💲 Desde Bs. 3.999

🖥️ PC Gamer
💲 Desde Bs. 6.500

⌨️ Combo Gamer
💲 Desde Bs. 450

🚚 Entrega rápida.
""",
        parse_mode="HTML"
    )

# ==========================
# CONTACTO
# ==========================
async def contacto(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        """
☎️ <b>CONTACTO</b>

📱 WhatsApp:
72456013

🕒 Atención:
Lunes a Sábado

💻 TechStore Bolivia
""",
        parse_mode="HTML"
    )

# ==========================
# UBICACION
# ==========================
async def ubicacion(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        """
📍 Estamos en Oruro - Bolivia

☎️ Referencias:
72456013
"""
    )

# ==========================
# MAIN
# ==========================
def main():

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("catalogo", catalogo))
    app.add_handler(CommandHandler("laptops", laptops))
    app.add_handler(CommandHandler("pcgamer", pcgamer))
    app.add_handler(CommandHandler("accesorios", accesorios))
    app.add_handler(CommandHandler("ofertas", ofertas))
    app.add_handler(CommandHandler("contacto", contacto))
    app.add_handler(CommandHandler("ubicacion", ubicacion))

    print("🤖 Bot TechStore iniciado correctamente")

    app.run_polling()

if __name__ == "__main__":
    main()