from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

TOKEN = "8855798797:AAGCYmIcdYH_8JN75o_fShlU23E5cyydo50"

# =====================================
# MENU PRINCIPAL
# =====================================
def menu_principal():

    keyboard = [
        [InlineKeyboardButton("💻 Laptops", callback_data="laptops")],
        [InlineKeyboardButton("🖥️ PC Gamer", callback_data="gamer")],
        [InlineKeyboardButton("🎧 Accesorios", callback_data="accesorios")],
        [InlineKeyboardButton("🔥 Ofertas", callback_data="ofertas")],
        [InlineKeyboardButton("📄 Catálogo PDF", callback_data="catalogo")],
        [InlineKeyboardButton("🖼️ Galería", callback_data="galeria")],
        [InlineKeyboardButton("⭐ Valoraciones", callback_data="valoraciones")],
        [InlineKeyboardButton("📍 Ubicación", callback_data="ubicacion")],
        [InlineKeyboardButton("☎️ Contacto", callback_data="contacto")]
    ]

    return InlineKeyboardMarkup(keyboard)

# =====================================
# START
# =====================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    mensaje = """
🛒 TECHSTORE BOLIVIA 2026

Bienvenido a nuestra tienda tecnológica.

Seleccione una opción:
"""

    await update.message.reply_text(
        mensaje,
        reply_markup=menu_principal()
    )

# =====================================
# HELP
# =====================================
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        """
📋 COMANDOS

/start
/help
/catalogo
"""
    )

# =====================================
# CATALOGO
# =====================================
async def catalogo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        with open("catalogo_techstore.pdf", "rb") as pdf:

            await update.message.reply_document(
                document=pdf,
                caption="📄 Catálogo Oficial TechStore Bolivia"
            )

    except:

        await update.message.reply_text(
            "❌ No se encontró el archivo catalogo_techstore.pdf"
        )

# =====================================
# BOTONES
# =====================================
async def botones(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    opcion = query.data

    if opcion == "laptops":

        await query.message.reply_photo(
            photo="https://picsum.photos/800/500",
            caption="""
💻 LAPTOPS DISPONIBLES

✔ Lenovo IdeaPad 5
✔ ASUS TUF Gaming
✔ HP Pavilion

💰 Desde Bs. 4.500
"""
        )

    elif opcion == "gamer":

        await query.message.reply_photo(
            photo="https://picsum.photos/801/500",
            caption="""
🖥️ PC GAMER

🔥 Ryzen 7
🔥 RTX 4060
🔥 SSD 1TB

💰 Bs. 9.999
"""
        )

    elif opcion == "accesorios":

        await query.message.reply_text(
            """
🎧 ACCESORIOS

⌨️ Teclados
🖱️ Mouse Gamer
🎧 Headsets
🖥️ Monitores
"""
        )

    elif opcion == "ofertas":

        await query.message.reply_text(
            """
🔥 OFERTAS DEL MES

💻 Lenovo IdeaPad

Antes: Bs. 4.500
Ahora: Bs. 3.999
"""
        )

    elif opcion == "catalogo":

        try:

            with open("catalogo_techstore.pdf", "rb") as pdf:

                await query.message.reply_document(
                    document=pdf,
                    caption="📄 Catálogo Oficial"
                )

        except:

            await query.message.reply_text(
                "❌ Catálogo no encontrado."
            )

    elif opcion == "galeria":

        await query.message.reply_text(
            """
🖼️ GALERÍA

Aquí puedes mostrar tus productos.
Agrega varias imágenes usando reply_media_group().
"""
        )

    elif opcion == "valoraciones":

        await query.message.reply_text(
            """
⭐ VALORACIÓN GENERAL

4.8 / 5 ⭐

Basado en 250 clientes.
"""
        )

    elif opcion == "ubicacion":

        await query.message.reply_venue(
            latitude=-17.9703,
            longitude=-67.1118,
            title="TechStore Bolivia",
            address="Oruro, Bolivia"
        )

    elif opcion == "contacto":

        await query.message.reply_text(
            """
☎️ CONTACTO

📱 WhatsApp
https://wa.me/59172456013

📧 ventas@techstore.com
"""
        )

# =====================================
# MAIN
# =====================================
def main():

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("help", help_command)
    )

    app.add_handler(
        CommandHandler("catalogo", catalogo)
    )

    app.add_handler(
        CallbackQueryHandler(botones)
    )

    print("✅ TechStore iniciado")

    app.run_polling()

# =====================================
# EJECUTAR
# =====================================
if __name__ == "__main__":
    main()