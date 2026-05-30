import streamlit as st
from datetime import datetime
import base64
import streamlit.components.v1 as components

# ================= CONFIG =================
st.set_page_config(
    page_title="Portal Resmi KPU Kota Bengkulu",
    page_icon="🏛️",
    layout="wide"
)

# ================= STICKY HEADER CLOCK =================
components.html("""
<div id="header-clock">
    <div class="left">
        🏛️ <b>PORTAL KPU KOTA BENGKULU</b>
    </div>

    <div class="right">
        <span id="clock"></span>
    </div>
</div>

<style>
#header-clock {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 55px;
    background: #0f172a;
    color: white;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 20px;
    font-family: Arial;
    z-index: 9999;
    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
}

body {
    padding-top: 70px;
}

.right {
    font-weight: bold;
}
</style>

<script>
function updateClock() {
    const now = new Date();

    const days = ["Minggu","Senin","Selasa","Rabu","Kamis","Jumat","Sabtu"];
    const day = days[now.getDay()];

    const date = now.toLocaleDateString('id-ID');
    const time = now.toLocaleTimeString('id-ID');

    document.getElementById("clock").innerHTML =
        day + ", " + date + " | " + time;
}

setInterval(updateClock, 1000);
updateClock();
</script>
""", height=60)

# ================= HELPER =================
def image_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_b64 = image_to_base64("logo_kpu.png")
kantor_b64 = image_to_base64("kantor_kpu.jpg")

# ================= CSS =================
st.markdown("""
<style>
#MainMenu, footer, header {visibility:hidden;}

.stApp {
    background: linear-gradient(135deg,#f8fafc,#eef2ff,#f1f5f9);
}

.block-container {
    max-width:1400px;
    padding-top:1rem;
    padding-bottom:1rem;
}

/* HERO */
.hero {
    background: linear-gradient(135deg,#0f172a,#1e3a8a,#dc2626);
    border-radius:25px;
    padding:35px;
    color:white;
    box-shadow:0 15px 35px rgba(0,0,0,.15);
}

.hero-title {font-size:42px;font-weight:900;}
.hero-sub {font-size:18px;opacity:0.95;}

/* KPI */
.kpi {
    background:white;
    border-radius:20px;
    padding:20px;
    text-align:center;
    box-shadow:0 8px 20px rgba(0,0,0,.08);
}

.kpi-number {
    font-size:36px;
    font-weight:900;
    color:#1e3a8a;
}

.kpi-label {
    color:#64748b;
    font-weight:600;
}

/* TITLE */
.section-title {
    text-align:center;
    font-size:30px;
    font-weight:800;
    color:#0f172a;
    margin-top:25px;
    margin-bottom:20px;
}

/* FOOTER */
.footer {
    text-align:center;
    margin-top:40px;
    padding:25px;
    color:#64748b;
    font-size:14px;
}
</style>
""", unsafe_allow_html=True)

# ================= HERO =================
now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

st.markdown(f"""
<div class="hero">
    <div style="display:flex;align-items:center;gap:20px;flex-wrap:wrap;">

        <div>
            {"<img src='data:image/png;base64," + logo_b64 + "' width='90'>" if logo_b64 else ""}
        </div>

        <div>
            <div class="hero-title">PORTAL RESMI KPU KOTA BENGKULU</div>
            <div class="hero-sub">Sistem Informasi Terintegrasi & Pelayanan Digital</div>
            <br>
            🟢 Sistem Online &nbsp;&nbsp; ⚡ 4 Aplikasi Terhubung &nbsp;&nbsp; 🕒 {now}
        </div>

    </div>
</div>
""", unsafe_allow_html=True)

# ================= KANTOR =================
if kantor_b64:
    st.markdown(f"""
    <div style="margin-top:20px;border-radius:20px;overflow:hidden;">
        <img src="data:image/jpg;base64,{kantor_b64}"
        style="width:100%;height:320px;object-fit:cover;">
    </div>
    """, unsafe_allow_html=True)
else:
    st.warning("Gambar kantor tidak ditemukan (kantor_kpu.jpg)")

# ================= KPI =================
c1, c2, c3, c4 = st.columns(4)

kpis = [
    ("4", "Aplikasi"),
    ("100%", "Online"),
    ("24", "Jam Layanan"),
    ("1", "Portal")
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
🚀 Akses Aplikasi Terintegrasi
</div>
""", unsafe_allow_html=True)

# ================= CARD =================
def app_card(icon, title, desc, url, color):
    st.markdown(f"""
    <div style="
        background:white;
        padding:20px;
        border-radius:20px;
        border-top:6px solid {color};
        box-shadow:0 5px 15px rgba(0,0,0,0.1);
        min-height:220px;
    ">
        <h1>{icon}</h1>
        <h3>{title}</h3>
        <p>{desc}</p>
    </div>
    """, unsafe_allow_html=True)

    st.link_button(f"🔗 Buka {title}", url, use_container_width=True)

# ================= MENU =================
c1, c2, c3, c4 = st.columns(4)

with c1:
    app_card("📊","E-Kinerja","Monitoring kinerja pegawai",
             "https://aplikasi-kinerja-kpu-kota-bengkulu.streamlit.app","#2563eb")

with c2:
    app_card("🗳️","BENGKULU POINT","Pelaporan partai politik",
             "https://kpu-kota-bengkulu-point.base44.app","#dc2626")

with c3:
    app_card("📋","CEK DPT","Data pemilih nasional",
             "https://cekdptonline.kpu.go.id","#16a34a")

with c4:
    app_card("📨","SP4N LAPOR","Aspirasi masyarakat",
             "https://www.lapor.go.id","#9333ea")

# ================= CONTACT =================
st.markdown("---")

st.markdown("""
<h3 style='text-align:center'>📞 Hubungi & Ikuti Kami</h3>
""", unsafe_allow_html=True)

st.info("📍 KPU Kota Bengkulu | ☎️ (0736 730403) | 📧 kpukotabengkulu@gmail.com")

# ================= FOOTER =================
st.markdown(f"""
<div class="footer">
<b>KOMISI PEMILIHAN UMUM KOTA BENGKULU</b><br>
Portal Sistem Informasi Terintegrasi & Pelayanan Digital<br><br>
© {datetime.now().year} KPU Kota Bengkulu
</div>
""", unsafe_allow_html=True)