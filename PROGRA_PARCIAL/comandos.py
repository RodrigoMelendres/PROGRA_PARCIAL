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
    ContextTypes
)

# RECUERDA: Mantén tu token seguro y no lo compartas públicamente.
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
# HANDLERS
# =====================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = "🛒 TECHSTORE BOLIVIA 2026\n\nBienvenido a nuestra tienda tecnológica.\n\nSeleccione una opción:"
    await update.message.reply_text(mensaje, reply_markup=menu_principal())

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📋 COMANDOS\n\n/start\n/help\n/catalogo")

async def catalogo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        with open("catalogo_techstore.pdf", "rb") as pdf:
            await update.message.reply_document(
                document=pdf,
                filename="Catalogo_TechStore_2026.pdf",
                caption="📄 Catálogo Oficial TechStore Bolivia"
            )
    except:
        await update.message.reply_text("❌ No se encontró el archivo catalogo_techstore.pdf")

# =====================================
# LOGICA DE BOTONES
# =====================================
async def botones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    opcion = query.data

    if opcion == "laptops":
        await query.message.reply_photo(
            photo="https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=1200&q=80",
            caption="💻 LAPTOPS DISPONIBLES\n\n✔ Lenovo IdeaPad 5\n✔ ASUS TUF Gaming\n✔ HP Pavilion\n✔ Dell Inspiron\n\n💰 Desde Bs. 4.500\n🛡 Garantía de 1 año\n🚚 Envíos a toda Bolivia"
        )

    elif opcion == "gamer":
        await query.message.reply_photo(
            photo="https://images.unsplash.com/photo-1587202372775-e229f172b9d7?auto=format&fit=crop&w=1200&q=80",
            caption="🖥️ PC GAMER\n\n🔥 Ryzen 7 7800X\n🔥 RTX 4060\n🔥 32GB RAM\n🔥 SSD NVMe 1TB\n\n💰 Bs. 9.999\n🎮 Ideal para gaming y streaming"
        )

    elif opcion == "accesorios":
        await query.message.reply_photo(
            photo="https://images.unsplash.com/photo-1546435770-a3e426bf472b?auto=format&fit=crop&w=1200&q=80",
            caption="🎧 ACCESORIOS\n\n⌨️ Teclados Mecánicos\n🖱️ Mouse Gamer\n🎧 Headsets RGB\n🖥️ Monitores\n\nStock disponible."
        )

    elif opcion == "ofertas":
        await query.message.reply_photo(
            photo="https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80",
            caption="🔥 OFERTA DEL MES\n\n💻 Lenovo IdeaPad 5\n\nAntes: Bs. 4.500\nAhora: Bs. 3.999\n\n⏳ Oferta limitada."
        )

    elif opcion == "galeria":
        media = [
            InputMediaPhoto(media="https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=1200&q=80", caption="💻 Laptop Profesional"),
            InputMediaPhoto(media="https://images.unsplash.com/photo-1593642702821-c8da6771f0c6?auto=format&fit=crop&w=1200&q=80"),
            InputMediaPhoto(media="https://images.unsplash.com/photo-1587202372775-e229f172b9d7?auto=format&fit=crop&w=1200&q=80"),
            InputMediaPhoto(media="https://images.unsplash.com/photo-1546435770-a3e426bf472b?auto=format&fit=crop&w=1200&q=80")
        ]
        await query.message.reply_media_group(media)

    elif opcion == "catalogo":
        try:
            with open("catalogo_techstore.pdf", "rb") as pdf:
                await query.message.reply_document(document=pdf, filename="Catalogo_TechStore_2026.pdf", caption="📄 Catálogo Oficial TechStore Bolivia")
        except:
            await query.message.reply_text("❌ No se encontró el catálogo.")

    elif opcion == "valoraciones":
        await query.message.reply_text("⭐ VALORACIÓN GENERAL\n\n⭐⭐⭐⭐⭐ 4.8/5\n\nBasado en más de 250 clientes satisfechos.\n\n💬 Excelente atención\n💬 Productos originales\n💬 Entregas rápidas")

    elif opcion == "ubicacion":
        await query.message.reply_venue(latitude=-17.9703, longitude=-67.1118, title="TechStore Bolivia", address="Oruro, Bolivia")

    elif opcion == "contacto":
        await query.message.reply_text("☎️ CONTACTO\n\n📱 WhatsApp:\nhttps://wa.me/59172456013\n\n📧 ventas@techstore.com\n\n🕒 Atención:\nLunes a Viernes\n08:00 - 18:00")

# =====================================
# MAIN
# =====================================
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("catalogo", catalogo))
    app.add_handler(CallbackQueryHandler(botones))
    print("✅ TechStore iniciado")
    app.run_polling()

if __name__ == "__main__":
    main()