import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
import base64
import os
import requests
from bs4 import BeautifulSoup
import json

# =====================================================
# CONFIG
# =====================================================
st.set_page_config(
    page_title="Portal Resmi KPU Kota Bengkulu",
    page_icon="logo_kpu.png",
    layout="wide"
)
# =====================================================
# COUNTER PENGUNJUNG
# =====================================================
COUNTER_FILE = "counter.txt"

if not os.path.exists(COUNTER_FILE):
    with open(COUNTER_FILE, "w") as f:
        f.write("0")

with open(COUNTER_FILE, "r") as f:
    total_pengunjung = int(f.read())

total_pengunjung += 1

with open(COUNTER_FILE, "w") as f:
    f.write(str(total_pengunjung))

components.html(
    """
    <div id="clockbar">
        <span id="clock"></span>
    </div>

    <style>
    #clockbar{
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

# =====================================================
# HELPER
# =====================================================
def image_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_b64 = image_to_base64("logo_kpu.png")
kantor_b64 = image_to_base64("kantor_kpu.jpg")

# =====================================================
# CUACA BENGKULU
# =====================================================
@st.cache_data(ttl=1800)
def get_weather():

    try:

        url = (
            "https://api.open-meteo.com/v1/forecast"
            "?latitude=-3.8004"
            "&longitude=102.2655"
            "&current_weather=true"
        )

        data = requests.get(
            url,
            timeout=10
        ).json()

        return {
            "temp": data["current_weather"]["temperature"],
            "wind": data["current_weather"]["windspeed"]
        }

    except:
        return None

@st.cache_data(ttl=1800)
def get_kpu_news():

    try:

        url = "https://kota-bengkulu.kpu.go.id/"

        html = requests.get(
            url,
            headers={
                "User-Agent":"Mozilla/5.0"
            },
            timeout=20
        ).text

        soup = BeautifulSoup(html, "lxml")

        berita = []

        rows = soup.find_all("div", class_="content")

        for row in rows:

            try:

                judul = row.find("h4").get_text(strip=True)

                ringkasan = row.find("p").get_text(
                    strip=True
                )[:250]

                link = row.find(
                    "a",
                    href=True
                )["href"]

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

    except:

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
        135deg,
        #0f172a 0%,
        #1e3a8a 45%,
        #dc2626 100%
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
    color:#1e3a8a;
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
    padding:25px;
    min-height:220px;
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
⚡ 7 Aplikasi Terhubung &nbsp;&nbsp;&nbsp;

</div>

</div>

</div>
""",
    unsafe_allow_html=True
)

# ================= KANTOR =================
st.markdown(f"""
<div style="margin-top:20px;border-radius:20px;overflow:hidden;">
    <img src="data:image/jpg;base64,{kantor_b64}" style="width:100%;height:320px;object-fit:cover;">
</div>
""", unsafe_allow_html=True)

# ================= CUACA =================

weather = get_weather()

if weather:

    st.markdown(f"""
    <div style="
        background:white;
        padding:18px;
        border-radius:18px;
        text-align:center;
        margin-top:20px;
        margin-bottom:20px;
        box-shadow:0 5px 15px rgba(0,0,0,.08);
        font-size:18px;
    ">
        🌤️ <b>Cuaca Kota Bengkulu</b>
        &nbsp;&nbsp;|&nbsp;&nbsp;
        🌡️ {weather['temp']}°C
        &nbsp;&nbsp;|&nbsp;&nbsp;
        💨 {weather['wind']} km/jam
    </div>
    """, unsafe_allow_html=True)

# ================= NEWS CAROUSEL =================

berita = get_kpu_news()

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
                    background:white;
                    border-radius:25px;
                    overflow:hidden;
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
                                height:500px;
                                object-fit:cover;
                            ">
                    </div>

                    <div style="
                        flex:1;
                        min-width:400px;
                        padding:35px;
                    ">

                        <h2 id="news-title"
                            style="
                                color:#1e3a8a;
                                margin-bottom:20px;
                            ">
                        </h2>

                        <p id="news-desc"
                           style="
                                font-size:18px;
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
        height=720,
        scrolling=False
    )

# ================= KPI =================

left, center, right = st.columns([1, 8, 1])

with center:

    c1, c2, c3, c4 = st.columns(4)

    kpis = [
        ("7", "Aplikasi"),
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

    st.markdown(
        f"""
        <div class="card" style="
            border-top:6px solid {color};
        ">
            <h1>{icon}</h1>
            <h3>{title}</h3>
            <p>{desc}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

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
        "ADU ONLINE",
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
        "🗂️",
        "PINDAH MEMILIH 2025",
        "Pemutakhiran Data Pemilih Berkelanjutan (PDPB) Tahun 2025",
        "https://forms.gle/sBLgbjKQFobKusdKA/",
        "#1e40af"
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
        "PINDAH MEMILIH 2026",
        "Pemutakhiran Data Pemilih Berkelanjutan (PDPB) Tahun 2026",
        "https://form.jotform.com/260114453918455/",
        "#0d9488"
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


© {datetime.now().year} KPU Kota Bengkulu
</div>
""", unsafe_allow_html=True)