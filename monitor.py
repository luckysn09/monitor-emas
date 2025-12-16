import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime

URL = "https://logammulia.com/id/purchase/gold"
TOKEN = os.environ.get("FONNTE_TOKEN")

TARGETS = [
    "+6283197511188",
    "E8l1KMRnTCUDG3ZbQWuQKX"
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

res = requests.get(URL, timeout=20)
soup = BeautifulSoup(res.text, "html.parser")
text = soup.get_text(separator=" ")

pesan = "🚨 UPDATE STOK EMAS LOGAM MULIA 🚨\n\n"

for lokasi in LOKASI:
    pesan += f"📍 {lokasi}\n"
    for gram in GRAM_LIST:
        if gram in text and lokasi in text and "Tersedia" in text:
            pesan += f"✅ {gram}\n"
        else:
            pesan += f"❌ {gram}\n"
    pesan += "\n"

pesan += f"⏰ {datetime.now().strftime('%d-%m-%Y %H:%M WIB')}"

for t in TARGETS:
    requests.post(
        "https://api.fonnte.com/send",
        headers={"Authorization": TOKEN},
        data={"target": t, "message": pesan}
    )
