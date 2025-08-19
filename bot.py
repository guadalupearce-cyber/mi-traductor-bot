import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from deep_translator import GoogleTranslator

# 📌 Idiomas disponibles
IDIOMAS_DISPONIBLES = {
    "es": "Español",
    "en": "Inglés",
    "fr": "Francés",
    "de": "Alemán",
    "it": "Italiano"
}

# 📌 Obtener el token desde variable de entorno
TOKEN = os.getenv("BOT_TOKEN")

# ✅ Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    idiomas = ", ".join([f"{nombre} ({codigo})" for codigo, nombre in IDIOMAS_DISPONIBLES.items()])
    await update.message.reply_text(
        f"👋 ¡Hola! Soy tu bot traductor.\n\n"
        f"Idiomas disponibles: {idiomas}\n\n"
        "Usa el comando así:\n"
        "/translate <código_idioma> <texto>\n\n"
        "Ejemplo:\n"
        "/translate en Hola, ¿cómo estás?"
    )

# ✅ Comando /translate
async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("⚠️ Uso incorrecto.\nEjemplo: /translate en Hola mundo")
        return

    codigo_idioma = context.args[0].lower()
    texto_original = " ".join(context.args[1:])

    if codigo_idioma not in IDIOMAS_DISPONIBLES:
        await update.message.reply_text("⚠️ Código de idioma no válido. Usa /start para ver los disponibles.")
        return

    try:
        traduccion = GoogleTranslator(source="auto", target=codigo_idioma).translate(texto_original)
        await update.message.reply_text(f"✅ Traducción ({IDIOMAS_DISPONIBLES[codigo_idioma]}):\n{traduccion}")
    except Exception as e:
        await update.message.reply_text(f"❌ Error al traducir: {e}")

# ✅ Función principal
def main():
    if not TOKEN:
        print("❌ ERROR: No se encontró el token. Define BOT_TOKEN en Render o tu entorno local.")
        return

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("translate", translate))

    print("🤖 Bot en ejecución...")
    app.run_polling()

if __name__ == "__main__":
    main()
