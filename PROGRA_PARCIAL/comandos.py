from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InputMediaPhoto
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

# =====================================
# TOKEN DEL BOT
# =====================================
TOKEN = "8855798797:AAGCYmIcdYH_8JN75o_fShlU23E5cyydo50"

# =====================================
# BASE DE DATOS TEMPORAL
# =====================================
carritos = {}
valoraciones = []

# =====================================
# MENU PRINCIPAL
# =====================================
MENU = [
    [KeyboardButton("💻 Laptops"), KeyboardButton("🖥️ PC Gamer")],
    [KeyboardButton("🎧 Accesorios"), KeyboardButton("🔥 Ofertas")],
    [KeyboardButton("🛒 Carrito"), KeyboardButton("🖼️ Galería")],
    [KeyboardButton("📄 Catálogo"), KeyboardButton("⭐ Valorar")],
    [KeyboardButton("📍 Ubicación"), KeyboardButton("☎️ Contacto")],
    [KeyboardButton("🕒 Horarios")]
]

# =====================================
# START
# =====================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    teclado = ReplyKeyboardMarkup(
        MENU,
        resize_keyboard=True
    )

    mensaje = """
🛒 TECHSTORE BOLIVIA

Bienvenido a nuestra tienda tecnológica.

💻 Laptops
🖥️ PC Gamer
🎧 Accesorios
🔥 Ofertas
📄 Catálogo PDF

Seleccione una opción:
"""

    await update.message.reply_text(
        mensaje,
        reply_markup=teclado
    )

# =====================================
# HELP
# =====================================
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    texto = """
📋 COMANDOS DISPONIBLES

/start      → Menú principal
/help       → Ayuda
/catalogo   → Descargar catálogo PDF

También puedes usar los botones.
"""

    await update.message.reply_text(texto)

# =====================================
# CATALOGO PDF
# =====================================
async def catalogo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        with open("catalogo_techstore.pdf", "rb") as pdf:

            await update.message.reply_document(
                document=pdf,
                filename="Catalogo_TechStore_2026.pdf",
                caption="""
📄 CATÁLOGO OFICIAL TECHSTORE

✅ Laptops
✅ PC Gamer
✅ Accesorios
✅ Ofertas

Gracias por visitarnos.
"""
            )

    except FileNotFoundError:

        await update.message.reply_text(
            "❌ No se encontró el archivo catalogo_techstore.pdf"
        )

# =====================================
# MENSAJES
# =====================================
async def mensajes(update: Update, context: ContextTypes.DEFAULT_TYPE):

    texto = update.message.text
    user_id = update.effective_user.id

    # ==========================
    # VALORACIONES
    # ==========================
    if context.user_data.get("esperando_valoracion"):

        try:

            nota = int(texto)

            if 1 <= nota <= 5:

                valoraciones.append(nota)

                promedio = sum(valoraciones) / len(valoraciones)

                await update.message.reply_text(
                    f"""
⭐ Gracias por tu valoración

Tu calificación: {nota}/5

Promedio actual:
⭐ {promedio:.1f}/5
"""
                )

                context.user_data["esperando_valoracion"] = False
                return

        except:
            pass

        await update.message.reply_text(
            "Ingrese una nota válida del 1 al 5."
        )
        return

    # ==========================
    # LAPTOPS
    # ==========================
    if texto == "💻 Laptops":

        if user_id not in carritos:
            carritos[user_id] = []

        carritos[user_id].append("Lenovo IdeaPad 5")

        await update.message.reply_photo(
            photo="https://images.unsplash.com/photo-1496181133206-80ce9b88a853",
            caption="""
💻 LAPTOPS DISPONIBLES

• Lenovo IdeaPad 5
• ASUS TUF Gaming
• HP Pavilion

💰 Desde Bs. 4.500

✅ Agregado al carrito.
"""
        )

    # ==========================
    # PC GAMER
    # ==========================
    elif texto == "🖥️ PC Gamer":

        if user_id not in carritos:
            carritos[user_id] = []

        carritos[user_id].append("PC Gamer Ryzen 7")

        await update.message.reply_photo(
            photo="https://images.unsplash.com/photo-1587202372775-e229f172b9d7",
            caption="""
🖥️ PC GAMER

🔥 Ryzen 7
🔥 RTX 4060
🔥 32 GB RAM
🔥 SSD 1 TB

💰 Bs. 9.999

✅ Agregado al carrito.
"""
        )

    # ==========================
    # ACCESORIOS
    # ==========================
    elif texto == "🎧 Accesorios":

        await update.message.reply_text(
            """
🎧 ACCESORIOS

⌨️ Teclados Mecánicos
🖱️ Mouse Gamer
🎧 Headsets RGB
🖥️ Monitores

Disponibles en stock.
"""
        )

    # ==========================
    # OFERTAS
    # ==========================
    elif texto == "🔥 Ofertas":

        await update.message.reply_text(
            """
🔥 OFERTA DE LA SEMANA

💻 Lenovo IdeaPad 5

Antes: Bs. 4.500
Ahora: Bs. 3.999

⏳ Oferta limitada.
"""
        )

    # ==========================
    # CARRITO
    # ==========================
    elif texto == "🛒 Carrito":

        if user_id not in carritos or len(carritos[user_id]) == 0:

            await update.message.reply_text(
                "🛒 Tu carrito está vacío."
            )

        else:

            mensaje = "🛒 TU CARRITO\n\n"

            for producto in carritos[user_id]:
                mensaje += f"• {producto}\n"

            mensaje += "\n✅ Gracias por visitar TechStore."

            await update.message.reply_text(mensaje)

    # ==========================
    # GALERIA
    # ==========================
    elif texto == "🖼️ Galería":

        media = [

            InputMediaPhoto(
                media="https://images.unsplash.com/photo-1496181133206-80ce9b88a853",
                caption="💻 Laptop Lenovo"
            ),

            InputMediaPhoto(
                media="https://images.unsplash.com/photo-1593642702821-c8da6771f0c6"
            ),

            InputMediaPhoto(
                media="https://images.unsplash.com/photo-1517336714739-489689fd1ca8"
            ),

            InputMediaPhoto(
                media="https://images.unsplash.com/photo-1587202372775-e229f172b9d7"
            )
        ]

        await update.message.reply_media_group(media)

    # ==========================
    # CATALOGO
    # ==========================
    elif texto == "📄 Catálogo":

        await catalogo(update, context)

    # ==========================
    # VALORAR
    # ==========================
    elif texto == "⭐ Valorar":

        context.user_data["esperando_valoracion"] = True

        await update.message.reply_text(
            """
⭐ CALIFÍCANOS

Escribe una nota del 1 al 5.

Ejemplo:
5
"""
        )

    # ==========================
    # UBICACION
    # ==========================
    elif texto == "📍 Ubicación":

        await update.message.reply_venue(
            latitude=-17.9703,
            longitude=-67.1118,
            title="TechStore Bolivia",
            address="Oruro, Bolivia"
        )

    # ==========================
    # CONTACTO
    # ==========================
    elif texto == "☎️ Contacto":

        await update.message.reply_text(
            """
☎️ CONTACTO

📱 WhatsApp:
https://wa.me/59172456013

📧 Correo:
ventas@techstore.com

🌐 Web:
www.techstore.com
"""
        )

    # ==========================
    # HORARIOS
    # ==========================
    elif texto == "🕒 Horarios":

        await update.message.reply_text(
            """
🕒 HORARIOS

Lunes a Viernes
08:00 - 18:00

Sábado
09:00 - 13:00

Domingo
Cerrado
"""
        )

    else:

        await update.message.reply_text(
            "Seleccione una opción válida del menú."
        )

# =====================================
# MAIN
# =====================================
def main():

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("catalogo", catalogo))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            mensajes
        )
    )

    print("🤖 TechStore Bolivia iniciado correctamente")

    app.run_polling()

# =====================================
# EJECUTAR
# =====================================
if __name__ == "__main__":
    main()