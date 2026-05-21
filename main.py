import requests
from bs4 import BeautifulSoup
from datetime import datetime

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters
)

# =========================================
# TELEGRAM TOKEN
# =========================================

TOKEN = "8809811334:AAFTDNaYeMz5IfgO087-25lhxgkuv7bEefk"

# =========================================
# FİNANS RAPORU
# =========================================

def finans_raporu():

    print(f"\nÇalıştı: {datetime.now()}")

    url = "https://www.doviz.com"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    mesaj = "📊 GÜNCEL FİNANS RAPORU\n\n"

    # DOLAR
    try:
        dolar = soup.select_one(
            '[data-socket-key="USD"]'
        ).text.strip()

        mesaj += f"💵 Dolar: {dolar}\n"

    except:
        mesaj += "💵 Dolar alınamadı\n"

    # EURO
    try:
        euro = soup.select_one(
            '[data-socket-key="EUR"]'
        ).text.strip()

        mesaj += f"💶 Euro: {euro}\n"

    except:
        mesaj += "💶 Euro alınamadı\n"

    # ALTIN
    try:
        gram = soup.select_one(
            '[data-socket-key="gram-altin"]'
        ).text.strip()

        mesaj += f"🥇 Gram Altın: {gram}\n"

    except:
        mesaj += "🥇 Gram Altın alınamadı\n"

    # GÜMÜŞ
    try:
        gumus = soup.select_one(
            '[data-socket-key="gumus"]'
        ).text.strip()

        mesaj += f"🥈 Gümüş: {gumus}\n"

    except:
        mesaj += "🥈 Gümüş alınamadı\n"

    mesaj += f"\n⏰ {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}"

    return mesaj

# =========================================
# TELEGRAM MESAJ KONTROL
# =========================================

async def mesaj_kontrol(update: Update, context: ContextTypes.DEFAULT_TYPE):

    gelen_mesaj = update.message.text.lower()

    print(f"Gelen mesaj: {gelen_mesaj}")

    if gelen_mesaj == "finans":

        mesaj = finans_raporu()

        await update.message.reply_text(mesaj)

# =========================================
# BOT BAŞLAT
# =========================================

print("Bot çalışıyor...")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(
    MessageHandler(filters.TEXT, mesaj_kontrol)
)

app.run_polling()
