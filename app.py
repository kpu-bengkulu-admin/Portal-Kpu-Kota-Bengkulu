import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
import base64
import os
import requests
from bs4 import BeautifulSoup
import json
import gspread
from google.oauth2.service_account import Credentials

# =====================================================
# CONFIG
# =====================================================
st.set_page_config(
    page_title="Portal Resmi KPU Kota Bengkulu",
    page_icon="logo_kpu.png",
    layout="wide"
)
st.markdown("""
<style>

/* Floating Button */
#a11y-btn{
    position:fixed;
    bottom:25px;
    right:25px;
    width:60px;
    height:60px;
    border-radius:50%;
    background:#dc2626;
    color:white;
    font-size:28px;
    border:none;
    cursor:pointer;
    z-index:99999;
    box-shadow:0 5px 15px rgba(0,0,0,.3);
}

/* Panel */
#a11y-panel{
    position:fixed;
    bottom:95px;
    right:25px;
    width:260px;
    background:white;
    border-radius:15px;
    padding:15px;
    box-shadow:0 5px 20px rgba(0,0,0,.25);
    z-index:99999;
    display:none;
}

#a11y-panel button{
    width:100%;
    margin-bottom:8px;
    padding:10px;
    border:none;
    border-radius:8px;
    background:#f1f5f9;
    cursor:pointer;
}

.big-cursor{
    cursor:crosshair !important;
}

.high-contrast{
    filter:contrast(150%);
}

.grayscale{
    filter:grayscale(100%);
}

.highlight-links a{
    background:yellow !important;
    color:black !important;
    padding:2px;
}

.section-title{
    text-align:center;
    font-size:32px;
    font-weight:700;
    margin-bottom:25px;
}

.stLinkButton button{
    width:100%;
    border-radius:10px;
    border:1px solid #d1d5db;
    background:white;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# GOOGLE SHEET COUNTER
# =====================================================

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=SCOPES
)

client = gspread.authorize(creds)

sheet = client.open(
    "COUNTER PORTAL KPU"
).sheet1

# =====================================================
# COUNTER PENGUNJUNG GOOGLE SHEET
# =====================================================

def tambah_pengunjung():

    sheet.append_row(
        [
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        ]
    )

def get_total_pengunjung():

    return max(len(sheet.col_values(1)) - 1, 0)


if "visitor_counted" not in st.session_state:

    tambah_pengunjung()

    st.session_state.visitor_counted = True

total_pengunjung = get_total_pengunjung()

components.html(
    """
    <div id="clockbar">
        <span id="clock"></span>
    </div>

    <style>
    #clockbar{
        position:sticky;
        top:0;
        z-index:9999;

        background:#0f172a;
        color:white;
        padding:10px 20px;
        border-radius:12px;
        text-align:center;
        font-weight:bold;
        font-size:16px;
        margin-bottom:15px;
    }
    </style>

    <script>
    function updateClock(){

        const now = new Date();

        const hari = [
            "Minggu",
            "Senin",
            "Selasa",
            "Rabu",
            "Kamis",
            "Jumat",
            "Sabtu"
        ];

        const teks =
            hari[now.getDay()] +
            ", " +
            now.toLocaleDateString("id-ID") +
            " | " +
            now.toLocaleTimeString("id-ID");

        document.getElementById("clock").innerHTML = teks;
    }

    updateClock();
    setInterval(updateClock,1000);
    </script>
    """,
    height=45
)

st.markdown("""
<div style="
background:#1e3a8a;
color:white;
padding:8px;
border-radius:10px;
font-weight:bold;
">
<marquee>
Selamat Datang di Portal Resmi KPU Kota Bengkulu POINT • Pengaduan Online • Pelayanan Digital Terintegrasi • Transparan • Akuntabel • Profesional • Siap Melayani
</marquee>
</div>
""", unsafe_allow_html=True)

components.html("""
<script>

setTimeout(() => {

const speech =
new SpeechSynthesisUtterance(
"Selamat datang di Portal Resmi Komisi Pemilihan Umum Kota Bengkulu POINT. Pengaduan Online, Pelayanan Digital Terintegrasi, Transparan, Akuntabel dan Profesional, KPU Kota Bengkulu Siap Melayani."
);

speech.lang = "id-ID";
const voices =
window.speechSynthesis.getVoices();

const indoVoice =
voices.find(v => v.lang === "id-ID");

if(indoVoice){
    speech.voice = indoVoice;
}

speech.rate = 0.9;
speech.pitch = 1.5;
speech.volume = 1.0;

window.speechSynthesis.speak(speech);

}, 2000);

</script>
""", height=0)

# =====================================================
# HELPER
# =====================================================
def image_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()
def audio_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_b64 = image_to_base64("logo_kpu.png")
audio_b64 = audio_to_base64("mars_kpu.mp3")

@st.cache_data(ttl=1800)
def get_kpu_news():

    try:

        url = "https://kota-bengkulu.kpu.go.id/"

        html = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=20
        ).text

        soup = BeautifulSoup(html, "html.parser")

        berita = []

        rows = soup.find_all("div", class_="content")

        for row in rows:

            try:

                judul = row.find("h4").get_text(strip=True)

                ringkasan = row.find("p").get_text(strip=True)[:300]

                link = row.find("a", href=True)["href"]

                parent = row.parent

                gambar = parent.find("img")

                img_url = ""

                if gambar:
                    img_url = gambar.get("src")

                berita.append({
                    "judul": judul,
                    "ringkasan": ringkasan,
                    "link": link,
                    "gambar": img_url
                })

            except:
                pass

        return berita[:5]

    except Exception as e:

        st.error(f"Error berita: {e}")

        return []

# =====================================================
# WAKTU
# =====================================================
now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

# =====================================================
# CSS
# =====================================================
st.markdown(
    f"""
<style>

#MainMenu {{
    visibility:hidden;
}}

footer {{
    visibility:hidden;
}}

header {{
    visibility:hidden;
}}

.stApp {{
    background:
    linear-gradient(
        135deg,
        #f8fafc 0%,
        #eef2ff 50%,
        #f1f5f9 100%
    );
}}

.block-container {{
    max-width:1400px;
    padding-top:1rem;
    padding-bottom:1rem;
}}

.hero {{
    background:
    linear-gradient(
        180deg,
        #7A1F1F 0%,
        #681818 40%,
        #561313 75%,
        #300B0C 100%
    );

    border-radius:20px;
    padding:10px 20px;
    color:white;
    box-shadow:0 15px 35px rgba(0,0,0,.15);
}}

.hero-title {{
    font-size:42px;
    font-weight:900;
}}

.hero-sub {{
    font-size:18px;
    opacity:0.95;
}}

.banner {{
    margin-top:20px;
    margin-bottom:20px;
}}

.banner img {{
    width:100%;
    border-radius:22px;
    box-shadow:0 10px 25px rgba(0,0,0,.12);
}}

.kpi {{
    background:white;
    border-radius:20px;
    padding:20px;
    text-align:center;
    box-shadow:0 8px 20px rgba(0,0,0,.08);
    margin-top:10px;
}}

.kpi-number {{
    font-size:36px;
    font-weight:900;
    color:##B8860B;
}}

.kpi-label {{
    color:#64748b;
    font-weight:600;
}}

.section-title {{
    text-align:center;
    font-size:30px;
    font-weight:800;
    color:#0f172a;
    margin-top:25px;
    margin-bottom:20px;
}}

.card {{
    background:white;
    border-radius:22px;
    padding:20px;
    height:260px;              /* ⬅️ INI KUNCI (samakan tinggi) */
    display:flex;              /* ⬅️ pakai flex */
    flex-direction:column;
    justify-content:space-between;
    box-shadow:0 10px 25px rgba(0,0,0,.08);
    transition:0.3s;
}}

.card:hover {{
    transform:translateY(-8px);
}}

.footer {{
    text-align:center;
    margin-top:40px;
    padding:25px;
    color:#64748b;
    font-size:14px;
}}

</style>
""",
    unsafe_allow_html=True
)


# =====================================================
# HERO
# =====================================================
st.markdown(
    f"""
<div class="hero">

<div style="display:flex;align-items:center;gap:20px;flex-wrap:wrap;">

<div>
<img src="data:image/png;base64,{logo_b64}" width="90">
</div>

<div>

<div class="hero-title">
PORTAL RESMI KPU KOTA BENGKULU POINT
</div>

<div class="hero-sub">
Pengaduan Online & Pelayanan Informasi Terintegrasi
</div>

<br>

🟢 Sistem Online &nbsp;&nbsp;&nbsp;
⚡ 8 Aplikasi Terhubung &nbsp;&nbsp;&nbsp;

</div>

</div>

</div>
""",
    unsafe_allow_html=True
)
st.markdown("### 🎵 Mars Komisi Pemilihan Umum")
st.audio("mars_kpu.mp3")

# ================= NEWS CAROUSEL =================

berita = get_kpu_news()

#st.write("Jumlah berita:", len(berita))
if berita:

    news_json = json.dumps(berita)

    components.html(
        f"""
        <div style="margin-top:25px;">

            <h2 style="
                text-align:center;
                color:#0f172a;
                margin-bottom:25px;
                font-weight:800;
            ">
            📰 BERITA TERBARU KPU KOTA BENGKULU
            </h2>

            <div id="news-card"
                 style="
                    position:relative;
                    background:white;
                    border-radius:25px;
                    overflow:visible;
                    box-shadow:0 10px 25px rgba(0,0,0,.10);
                 ">

                <div style="
                    display:flex;
                    flex-wrap:wrap;
                ">

                    <div style="
                        flex:1;
                        min-width:450px;
                    ">

                        <img
                            id="news-img"
                            src=""
                            style="
                                width:100%;
                                height:280px;
                                object-fit:contain;
                                background:white;
                            ">
                    </div>

                    <div style="
                        flex:1;
                        min-width:400px;
                        padding:20px;
                    ">

                        <h2 id="news-title"
                            style="
                                color:#1e3a8a;
                                margin-bottom:15px;
                            ">
                        </h2>

                        <p id="news-desc"
                           style="
                                font-size:15px;
                                line-height:1.8;
                                color:#334155;
                           ">
                        </p>

                        <a
                            id="news-link"
                            href="#"
                            target="_blank"
                            style="
                                display:inline-block;
                                background:#dc2626;
                                color:white;
                                padding:12px 20px;
                                border-radius:10px;
                                text-decoration:none;
                                margin-top:15px;
                            ">
                            📖 Baca Selengkapnya
                        </a>

                    </div>

                </div>

            </div>

            <div
                id="dots"
                style="
                    text-align:center;
                    margin-top:15px;
                    font-size:24px;
                ">
            </div>

        </div>

        <script>

        const berita = {news_json};

        let index = 0;

        function tampilkanBerita() {{

            document.getElementById("news-img")
                .src = berita[index].gambar;

            document.getElementById("news-title")
                .innerHTML = berita[index].judul;

            document.getElementById("news-desc")
                .innerHTML = berita[index].ringkasan;

            document.getElementById("news-link")
                .href = berita[index].link;

            let dots = "";

            for(let i=0;i<berita.length;i++) {{

                if(i===index)
                    dots += "🔵 ";

                else
                    dots += "⚪ ";

            }}

            document.getElementById("dots")
                .innerHTML = dots;
        }}

        tampilkanBerita();

        setInterval(() => {{

            index++;

            if(index >= berita.length)
                index = 0;

            tampilkanBerita();

        }}, 5000);

        </script>
        """,
        height=500,
        scrolling=True
    )

# ================= KPI =================

left, center, right = st.columns([1, 8, 1])

with center:

    c1, c2, c3, c4 = st.columns(4)

    kpis = [
        ("8", "Aplikasi"),
        ("100%", "Online"),
        ("24", "Jam Layanan"),
        (f"{total_pengunjung:,}", "Pengunjung")
    ]

    for col, (num, label) in zip([c1, c2, c3, c4], kpis):
        with col:
            st.markdown(f"""
            <div class="kpi">
                <div class="kpi-number">{num}</div>
                <div class="kpi-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

# ================= TITLE =================
st.markdown("""
<div class="section-title">
🚀 Akses Pengaduan dan Aplikasi Pelayanan Terintegrasi
</div>
""", unsafe_allow_html=True)

# ================= CARD =================
def app_card(icon, title, desc, url, color):

    html = f"""
    <div style="
        background:white;
        border-radius:18px;
        height:220px;
        padding:20px;
        border-top:5px solid {color};
        box-shadow:0 4px 12px rgba(0,0,0,.08);

        display:flex;
        flex-direction:column;
        justify-content:center;
        align-items:center;
        text-align:center;
    ">

        <div style="
            font-size:60px;
            margin-bottom:10px;
        ">
            {icon}
        </div>

        <div style="
            font-size:22px;
            font-weight:700;
            color:#1e1b4b;
            margin-bottom:8px;
        ">
            {title}
        </div>

        <div style="
            color:#64748b;
            font-size:14px;
            line-height:1.4;
        ">
            {desc}
        </div>

    </div>
    """

    st.components.v1.html(html, height=230)

    st.link_button(
        f"🔗 Buka {title}",
        url,
        use_container_width=True
    )

# ================= MENU BARIS 1 =================
c1, c2, c3, c4 = st.columns(4)

with c1:
    app_card(
        "📊",
        "E-KINERJA",
        "Monitoring kinerja pegawai",
        "https://aplikasi-kinerja-kpu-kota-bengkulu.streamlit.app",
        "#2563eb"
    )

with c2:
    app_card(
        "🗳️",
        "PENGADUAN ONLINE",
        "Pelaporan Pencatutan partai politik",
        "https://kpu-kota-bengkulu-point.base44.app/",
        "#dc2626"
    )

with c3:
    app_card(
        "📋",
        "CEK DPT",
        "Data pemilih nasional",
        "https://cekdptonline.kpu.go.id/",
        "#16a34a"
    )

with c4:
    app_card(
        "📨",
        "SP4N LAPOR",
        "Aspirasi masyarakat",
        "https://www.lapor.go.id/",
        "#9333ea"
    )

# ================= MENU BARIS 2 =================
c1, c2, c3, c4 = st.columns(4)

with c1:
    app_card(
        "📚",
        "PPID",
        "Pusat Pelayanan Informasi dan Dokumentasi KPU Kota Bengkulu",
        "https://bengkulukotappid.kpu.go.id/",
        "#475569"
    )

with c2:
    app_card(
        "⭐",
        "SKM",
        "Kuesioner Survei Kepuasan Masyarakat pada Unit Layanan KPU Kota Bengkulu",
        "https://forms.gle/YErvV9ArS9M8hZVb9/",
        "#f59e0b"
    )

with c3:
    app_card(
        "🗂️",
        "SITAPEL",
        "Pemutakhiran Data Pemilih Berkelanjutan (PDPB) Tahun 2026",
        "https://form.jotform.com/260114453918455/",
        "#0d9488"
    )

with c4:
    app_card(
        "⚖️",
        "JDIH KPU KOTA BENGKULU",
        "Jaringan Dokumentasi dan Informasi Hukum",
        "https://jdih.kpu.go.id/bengkulu/bengkulu-kota",
        "#b45309"
    )

# HUBUNGI KAMI

st.markdown("---")

st.markdown("""
<h3 style='text-align:center'>
📞 Hubungi & Ikuti Kami
</h3>
""", unsafe_allow_html=True)

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.link_button(
        "🌐 Website",
        "https://kota-bengkulu.kpu.go.id/",
        use_container_width=True
    )

with c2:
    st.link_button(
        "📘 Facebook",
        "https://www.facebook.com/share/1Koz9czfo5/",
        use_container_width=True
    )

with c3:
    st.link_button(
        "📸 Instagram",
        "https://www.instagram.com/kpukotabengkulu",
        use_container_width=True
    )

with c4:
    st.link_button(
        "▶️ YouTube",
        "https://youtube.com/@kpukotabengkulu4944",
        use_container_width=True
    )

with c5:
    st.link_button(
        "📱 WhatsApp",
        "https://wa.me/6289530256359",
        use_container_width=True
    )

st.markdown("""
<div style="
    background:#dbeafe;
    padding:16px;
    border-radius:12px;
    text-align:center;
    color:#1e3a8a;
    font-size:18px;
    font-weight:500;
">
📍 Kantor KPU Kota Bengkulu |
☎️ Telp: (0736 730403) |
📧 Email: kpukotabengkulu@gmail.com
</div>
""", unsafe_allow_html=True)

# ================= FOOTER =================
st.markdown(f"""
<div class="footer">
<b>KOMISI PEMILIHAN UMUM KOTA BENGKULU</b><br>
Portal Pengaduan Online dan Sistem Pelayanan Informasi Terintegrasi<br><br>

👥 Total Pengunjung : <b>{total_pengunjung:,}</b><br><br>


©by.es 2025 KPU Kota Bengkulu
</div>
""", unsafe_allow_html=True)
