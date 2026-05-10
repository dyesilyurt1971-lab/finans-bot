import requests
from bs4 import BeautifulSoup
from datetime import datetime
import schedule
import time

# =========================================
# TELEGRAM BİLGİLERİ
# =========================================

TOKEN = "8660704753:AAHExzBOBoLA5iBWeg0I-9CNZ-7_rhIRLMM"

CHAT_ID = "1178067113"

# =========================================
# FİNANS RAPORU FONKSİYONU
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

    # GRAM ALTIN
    try:
        gram = soup.select_one(
            '[data-socket-key="gram-altin"]'
        ).text.strip()

        mesaj += f"🥇 Gram Altın: {gram}\n"

    except:
        mesaj += "🥇 Gram Altın alınamadı\n"

    # ONS ALTIN
    try:
        ons = soup.select_one(
            '[data-socket-key="ons"]'
        ).text.strip()

        mesaj += f"🌍 Ons Altın: {ons}\n"

    except:
        mesaj += "🌍 Ons Altın alınamadı\n"

    # GÜMÜŞ
    try:
        gumus = soup.select_one(
            '[data-socket-key="gumus"]'
        ).text.strip()

        mesaj += f"🥈 Gümüş: {gumus}\n"

    except:
        mesaj += "🥈 Gümüş alınamadı\n"

    mesaj += f"\n⏰ {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}"

    print("\nMesaj:\n")
    print(mesaj)

    # =========================================
    # TELEGRAM GÖNDER
    # =========================================

    telegram_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": mesaj
    }

    response = requests.post(
        telegram_url,
        data=data
    )

    print("\nTelegram mesajı gönderildi.")

# =========================================
# İLK AÇILIŞTA MANUEL ÇALIŞTIR
# =========================================

print("Program başladı.")
print("İlk manuel finans raporu gönderiliyor...")

finans_raporu()

# =========================================
# OTOMATİK SAATLER
# =========================================

saatler = [
    "10:00",
    "11:00",
    "12:00",
    "13:00",
    "14:00",
    "15:00",
    "16:00",
    "17:00",
    "18:00",
    "19:00",
    "20:00",
    "21:00",
    "22:00",
    "23:00"
]

# =========================================
# GÖREVLERİ EKLE
# =========================================

for saat in saatler:

    schedule.every().day.at(saat).do(finans_raporu)

    print(f"Görev eklendi: {saat}")

print("\nOtomatik finans botu çalışıyor...")
print("Saat başı Telegram mesajı gönderecek.")

# =========================================
# SÜREKLİ ÇALIŞ
# =========================================

while True:

    schedule.run_pending()

    time.sleep(30)