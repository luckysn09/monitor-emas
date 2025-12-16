import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime

TEST_MODE = False
URL = "https://logammulia.com/id/purchase/gold"
TOKEN = os.environ.get("FONNTE_TOKEN")

ADMIN_WA = "+6283197511188"

TARGETS = [
    "+6283197511188",
    "+6281289285528",
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

PRIORITAS_JAKARTA = [
    "Jakarta",
    "Pulogadung",
    "Graha Dipta",
    "Juanda",
    "Puri Indah"
]

STATUS_FILE = "last_status.txt"
STAT_BUTIK_FILE = "butik_stats.txt"
STAT_SENT_FILE = "stat_sent_today.txt"

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
        
# --- CATAT STATISTIK BUTIK (SETELAH HASIL TERBENTUK) ---
jam_sekarang = datetime.now().hour
for butik in hasil.keys():
    with open(STAT_BUTIK_FILE, "a") as f:
        f.write(f"{butik}|{jam_sekarang}\n")

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
        for t in TARGETS:
            r = requests.post(
                "https://api.fonnte.com/send",
                headers={"Authorization": TOKEN},
                data={
                    "target": t,
                    "message": pesan
                }
            )
            print(f"[WA SEND] target={t} status={r.status_code}")

    except Exception as e:
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

def statistik_butik_paling_sering():
    if not os.path.exists(STAT_BUTIK_FILE):
        return {}

    data = {}

    with open(STAT_BUTIK_FILE, "r") as f:
        for line in f:
            if "|" not in line:
                continue

            butik, jam = line.strip().split("|")
            if not jam.isdigit():
                continue

            if butik not in data:
                data[butik] = {}

            data[butik][jam] = data[butik].get(jam, 0) + 1

    hasil = {}
    for butik, jam_data in data.items():
        jam_terbanyak = max(jam_data, key=jam_data.get)
        hasil[butik] = (jam_terbanyak, jam_data[jam_terbanyak])

    return hasil

# --- KIRIM STATISTIK BUTIK JAM 22:00 WIB (ANTI DUPLIKASI) ---
sekarang = datetime.now()
today = sekarang.strftime("%Y-%m-%d")

sent_today = ""
if os.path.exists(STAT_SENT_FILE):
    with open(STAT_SENT_FILE, "r") as f:
        sent_today = f.read()

if sekarang.hour == 22 and sent_today != today:
    stats = statistik_butik_paling_sering()

    if stats:
        pesan = "📊 STATISTIK STOK EMAS PER BUTIK\n"
        pesan += "(Jam paling sering READY)\n\n"

        for butik, (jam, jumlah) in stats.items():
            pesan += f"🏪 {butik}\n"
            pesan += f"🕒 Jam {jam}:00 → {jumlah} kali\n\n"

        pesan += f"⏰ {sekarang.strftime('%d-%m-%Y %H:%M WIB')}"

        requests.post(
            "https://api.fonnte.com/send",
            headers={"Authorization": TOKEN},
            data={
                "target": ADMIN_WA,
                "message": pesan
            }
        )

        # 👉 SIMPAN FLAG HARIAN (PENTING)
        with open(STAT_SENT_FILE, "w") as f:
            f.write(today)
