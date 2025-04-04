import os
import csv
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN") or "7672348403:AAGH7nf2y-mGMsDzT--SAYrRQU5NzMudgso"

PLANTILLA_IMAGEN = "SOY NOMBRE 2.jpg"
FUENTE_PERSONALIZADA = "AQUAWAXPRO-BOLD.TTF"
ARCHIVO_ESTADISTICAS = "estadisticas.csv"


def generar_imagen(nombre):
    nombre = nombre.upper().strip()[:10]
    img = Image.open(PLANTILLA_IMAGEN).convert("RGBA")
    draw = ImageDraw.Draw(img)

    font_size = 160
    font = ImageFont.truetype(FUENTE_PERSONALIZADA, font_size)

    width, height = img.size
    text_width = draw.textlength(nombre, font=font)
    text_height = font.getbbox(nombre)[3]

    text_x = (width - text_width) // 2
    text_y = 860

    draw.text((text_x, text_y), nombre, font=font, fill="white")

    output_path = f"{nombre}.png"
    img.save(output_path)
    return output_path


def guardar_estadistica(nombre):
    nombre = nombre.upper().strip()[:10]
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    archivo_existe = os.path.exists(ARCHIVO_ESTADISTICAS)

    with open(ARCHIVO_ESTADISTICAS, mode="a", newline="") as archivo:
        writer = csv.writer(archivo)
        if not archivo_existe:
            writer.writerow(["Nombre", "FechaHora"])
        writer.writerow([nombre, fecha_hora])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 ¡Hola! Escribe el nombre que quieres en tu imagen (máx. 10 letras).\n\n"
        "🎨 *Este bot fue creado con ❤️ por Fernando Juárez* para el 93° Aniversario de IDEC Guatemala.",
        parse_mode="Markdown"
    )


async def recibir_nombre(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombre = update.message.text.strip()
    if len(nombre) > 10:
        await update.message.reply_text("❌ El nombre debe tener máximo 10 letras.")
        return

    await update.message.reply_text("✅ Generando tu imagen, por favor espera...")

    imagen_generada = generar_imagen(nombre)
    guardar_estadistica(nombre)

    await update.message.reply_photo(photo=open(imagen_generada, "rb"))
    os.remove(imagen_generada)


if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_nombre))
    app.run_polling()
