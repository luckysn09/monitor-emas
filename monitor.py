import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime

TEST_MODE = True

URL = "xxx"
TOKEN = os.environ.get("FONNTE_TOKEN")

ADMIN_WA = "+6283197511188"

TARGETS = [
    "+6283197511188",
    "120363402852110732@g.us"
]

GRAM_LIST = [
    "Emas Batangan - 0.5 gr",
    "Emas Batangan - 1 gr",
    "Emas Batangan - 2 gr",
    "Emas Batangan - 3 gr",
    "Emas Batangan - 5 gr",
    "Emas Batangan - 10 gr",
    "Emas Batangan - 25 gr",
    "Emas Batangan - 50 gr",
    "Emas Batangan - 100 gr",
    "Emas Batangan - 250 gr",
    "Emas Batangan - 500 gr",
    "Emas Batangan - 1000 gr"
]

LOKASI = [
    "BELM - Pengiriman Ekspedisi, Pulogadung Jakarta, Jakarta",
    "BELM - Graha Dipta (Pengambilan Di Butik) Pulogadung Jakarta, Jakarta",
    "BELM - Bandung, Bandung",
    "BELM - Yogyakarta, Yogyakarta",
    "BELM - Denpasar Bali, Bali",
    "BELM - Balikpapan, Balikpapan",
    "BELM - Makasar, Makasar",
    "BELM - Medan",
    "BELM - Palembang, Palembang",
    "BELM - Pekanbaru, Pekanbaru",
    "BELM - Serpong (pengambilan Di Butik), Tangerang",
    "BELM - Bintaro, Tangerang Selatan",
    "BELM - Bogor, Bogor",
    "BELM - Bekasi, Bekasi",
    "BELM - Juanda, Jakarta",
    "BELM - Puri Indah"
]

STATUS_FILE = "last_status.txt"

res = requests.get(URL, timeout=20)
soup = BeautifulSoup(res.text, "html.parser")
text = soup.get_text(separator=" ")

hasil = {}

for lokasi in LOKASI:
    tersedia = []
    for gram in GRAM_LIST:
        if gram in text and lokasi in text and "Tersedia" in text:
            tersedia.append(gram)
    if tersedia:
        hasil[lokasi] = tersedia

status_baru = str(hasil)

status_lama = ""
if os.path.exists(STATUS_FILE):
    with open(STATUS_FILE, "r") as f:
        status_lama = f.read()

# 👉 ANTI SPAM: hanya kirim jika ADA PERUBAHAN
if TEST_MODE or (status_baru != status_lama and hasil):
    pesan = "🚨 UPDATE STOK EMAS LOGAM MULIA 🚨\n\n"

    for lokasi, grams in hasil.items():
        pesan += f"📍 {lokasi}\n"
        for g in grams:
            pesan += f"✅ {g}\n"
        pesan += "\n"

    pesan += f"⏰ {datetime.now().strftime('%d-%m-%Y %H:%M WIB')}"

    try:
    # kirim NOTIFIKASI STOK (pribadi + grup)
    for t in TARGETS:
        requests.post(
            "https://api.fonnte.com/send",
            headers={"Authorization": TOKEN},
            data={"target": t, "message": pesan}
        )

except Exception as e:
    # kirim ERROR HANYA ke WA pribadi
    error_msg = f"""⚠️ BOT LOGAM MULIA ERROR ⚠️

Pesan error:
{str(e)}

⏰ {datetime.now().strftime('%d-%m-%Y %H:%M WIB')}
"""
    requests.post(
        "https://api.fonnte.com/send",
        headers={"Authorization": TOKEN},
        data={
            "target": ADMIN_WA,
            "message": error_msg
        }
    )

    with open(STATUS_FILE, "w") as f:
        f.write(status_baru)
