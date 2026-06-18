from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# =====================================
# TOKEN DEL BOT
# =====================================
TOKEN = "8895460418:AAFXRGM4uFe2yGj9R6rMP3SBEtHPSyC_nLI"

# =====================================
# COMANDO /start
# =====================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    mensaje = """
🎓 BOT ACADÉMICO UDABOL

¡Bienvenido al sistema académico!

Comandos disponibles:

/texto  - Información del estudiante
/imagen - Logo institucional
/pdf    - Descargar documento PDF

👩 Estudiante: Elena Sánchez Chuquichambi
🆔 Código: 120919
📚 Materia: Programación Avanzada
"""

    await update.message.reply_photo(
        photo="https://www.cladera.org/canvas/images/imagemodelo/canvas-182.jpg",
        caption=mensaje
    )

# =====================================
# COMANDO /texto
# =====================================
async def texto(update: Update, context: ContextTypes.DEFAULT_TYPE):

    mensaje = """
📋 INFORMACIÓN DEL ESTUDIANTE

Nombre:
Elena Sánchez Chuquichambi

Código:
120919

Materia:
Programación Avanzada

Universidad:
Universidad de Aquino Bolivia (UDABOL)
"""

    await update.message.reply_text(mensaje)

# =====================================
# COMANDO /imagen
# =====================================
async def imagen(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_photo(
        photo="https://www.cladera.org/canvas/images/imagemodelo/canvas-182.jpg",
        caption="""
🏛 UNIVERSIDAD DE AQUINO BOLIVIA

👩 Elena Sánchez Chuquichambi
🆔 Código: 120919
📚 Programación Avanzada
"""
    )

# =====================================
# COMANDO /pdf
# =====================================
async def pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:
        with open("caratula.pdf", "rb") as archivo:

            await update.message.reply_document(
                document=archivo,
                caption="""
📄 DOCUMENTO PDF

Elena Sánchez Chuquichambi
Código: 120919
Programación Avanzada
"""
            )

    except FileNotFoundError:

        await update.message.reply_text(
            "❌ No se encontró el archivo caratula.pdf"
        )

# =====================================
# COMANDO /ayuda
# =====================================
async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):

    mensaje = """
ℹ️ AYUDA DEL BOT

Comandos disponibles:

/start  - Menú principal
/texto  - Datos del estudiante
/imagen - Mostrar imagen
/pdf    - Descargar PDF
/ayuda  - Ver ayuda
"""

    await update.message.reply_text(mensaje)

# =====================================
# MAIN
# =====================================
def main():

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("texto", texto))
    app.add_handler(CommandHandler("imagen", imagen))
    app.add_handler(CommandHandler("pdf", pdf))
    app.add_handler(CommandHandler("ayuda", ayuda))

    print("🎓 BOT ACADÉMICO UDABOL INICIADO")

    app.run_polling()

# =====================================
# EJECUTAR BOT
# =====================================
if __name__ == "__main__":
    main()