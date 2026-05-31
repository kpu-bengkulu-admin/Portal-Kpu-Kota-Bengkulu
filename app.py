import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
import base64


# =====================================================
# CONFIG
# =====================================================
st.set_page_config(
    page_title="Portal Resmi KPU Kota Bengkulu",
    page_icon="logo_kpu.png",
    layout="wide"
)
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
Selamat Datang di Portal Resmi KPU Kota Bengkulu • Pelayanan Digital Terintegrasi • Transparan • Akuntabel • Profesional • Siap Melayani
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

    border-radius:25px;
    padding:35px;
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
PORTAL RESMI KPU KOTA BENGKULU
</div>

<div class="hero-sub">
Sistem Informasi Terintegrasi & Pelayanan Digital
</div>

<br>

🟢 Sistem Online &nbsp;&nbsp;&nbsp;
⚡ 5 Aplikasi Terhubung &nbsp;&nbsp;&nbsp;

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

# ================= KPI =================
c1, c2, c3, c4, c5 = st.columns(5)

kpis = [
    ("5", "Aplikasi"),
    ("100%", "Online"),
    ("24", "Jam Layanan"),
    ("1", "Portal")
]

for col, (num, label) in zip([c1, c2, c3, c4, c5], kpis):
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
🚀 Akses Aplikasi Terintegrasi
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

# ================= MENU =================
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    app_card("📊","E-Kinerja","Monitoring kinerja pegawai",
             "https://aplikasi-kinerja-kpu-kota-bengkulu.streamlit.app","#2563eb")

with c2:
    app_card("🗳️","BENGKULU POINT","Pelaporan Pencatutan partai politik",
             "https://kpu-kota-bengkulu-point.base44.app/","#dc2626")

with c3:
    app_card("📋","CEK DPT","Data pemilih nasional",
             "https://cekdptonline.kpu.go.id/","#16a34a")

with c4:
    app_card("📋","PINDAH MEMILIH (PDPB) 2025","Pemutakhiran Data Pemilih 2025",
             "https://forms.gle/mPL8zT362prjJSVg9/","#1e3a8a")

with c5:
    app_card("📨","SP4N LAPOR","Aspirasi masyarakat",
             "https://www.lapor.go.id/","#9333ea")


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

st.info(
    "📍 Kantor KPU Kota Bengkulu | "
    "☎️ Telp: (0736 730403) | "
    "📧 Email: (kpukotabengkulu@gmail.com)"
)


# ================= FOOTER =================
st.markdown(f"""
<div class="footer">
<b>KOMISI PEMILIHAN UMUM KOTA BENGKULU</b><br>
Portal Sistem Informasi Terintegrasi<br><br>
© {datetime.now().year} KPU Kota Bengkulu
</div>
""", unsafe_allow_html=True)