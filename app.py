import streamlit as st
import streamlit.components.v1 as components
import requests
import base64
from PIL import Image
from io import BytesIO

# === 1. KONFIGURASI HALAMAN ===
st.set_page_config(
    page_title="Portal Resmi Karang Taruna RW 11",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# === 2. ID FILE GOOGLE DRIVE ===
LOGO_DRIVE_ID = "1XFU2iNW4e34Xiqko5mxzvcWpwNDPDic9"
FOTO_MUDAMUDI_DRIVE_ID = "1uaA0uRpgxWkF8SO0VMsxMDoF4-l3IPkm"

# Helper fungsi untuk mengunduh gambar dari Google Drive
@st.cache_data(show_spinner=False)
def load_drive_image(file_id, fallback_url):
    if not file_id:
        try:
            res = requests.get(fallback_url)
            return Image.open(BytesIO(res.content))
        except:
            return None
    
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    try:
        session = requests.Session()
        response = session.get(url, stream=True)
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                response = session.get(f"{url}&confirm={value}", stream=True)
                break
        return Image.open(BytesIO(response.content))
    except:
        try:
            thumb_url = f"https://drive.google.com/thumbnail?id={file_id}&sz=w1000"
            res = requests.get(thumb_url)
            return Image.open(BytesIO(res.content))
        except:
            return None

# Convert PIL Image ke Base64 String untuk HTML
def image_to_base64(img):
    if img is None:
        return ""
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Load Gambar
img_logo = load_drive_image(
    LOGO_DRIVE_ID, 
    "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?q=80&w=200"
)
img_muda_mudi = load_drive_image(
    FOTO_MUDAMUDI_DRIVE_ID, 
    "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?q=80&w=1000"
)

logo_b64 = image_to_base64(img_logo)

# === 3. DATABASE FOLDER GOOGLE DRIVE KEGIATAN ===
DATABASE_FOLDER_DRIVE = {
    "2026": {
        "Pentas Seni": "1tLm3QKkctMNbeGhqCLKefgEd3pdueqJP", 
        "Jalan Sehat": "12q5Ua5raidz1aLooqu1loshOQvDxIWzT"},
    "2025": {
        "Pentas Seni": "17Pf41jWbEalo3oGVe4tmdhvt0Sc8HXVx", 
        "Jalan Sehat": "1Nm_POWpLqW73w5tBLd2aSx42FGB8tWVl"},
    "2024": {
        "Pentas Seni": "1Okq8SGjXaQ-XRZfXsrMl7DgLebM89TUE",
        "Jalan Sehat": "12TnXgfdiMMp9HsUHK2ts3Ip-DtisRKhV"
    },
    "2023": {
        "Pentas Seni": "1qL-l8YTk0mx0tElKEoB7VSne5Zl1RnDx",
        "Jalan Sehat": "1FKCbDrBv6Vs_PWRIRDCs0nzYyZ8Ol5Jq"
    },
    "2022": {
        "Pentas Seni": "1NUDV0plxl3IAm0YCoxs-bkwhM5Y-4CJ9", 
        "Jalan Sehat": "1uM1OZtI3bIXgdfxAPG-2874I8jFXx73V"}
}

# === 4. CUSTOM CSS ===
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    
    .stApp {
        background-color: #0b0f19;
        color: #f1f5f9;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    .top-header-container {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 4px 0px;
        margin-top: -45px;
        margin-bottom: 12px;
    }
    .logo-img-style {
        width: 44px;
        height: 44px;
        border-radius: 8px;
        object-fit: cover;
    }
    
    .hero-box {
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.65) 0%, rgba(11, 15, 25, 0.95) 100%),
                    url('https://images.unsplash.com/photo-1500382017468-9049fed747ef?q=80&w=1600&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        padding: 40px 16px;
        border-radius: 14px;
        border: 1px solid #1e293b;
        color: white;
        text-align: center !important;
        margin-bottom: 20px;
    }
    .hero-tag {
        display: inline-block;
        padding: 4px 12px;
        background: rgba(245, 158, 11, 0.15);
        border: 1px solid rgba(245, 158, 11, 0.3);
        color: #fbbf24;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.8px;
        text-transform: uppercase;
        margin-bottom: 10px;
    }
    .hero-h1 {
        font-size: 1.75rem;
        font-weight: 800;
        margin-bottom: 8px;
        color: #ffffff;
        letter-spacing: -0.5px;
        text-align: center !important;
    }
    .hero-p {
        font-size: 0.88rem;
        color: #94a3b8;
        max-width: 600px;
        margin: 0 auto !important;
        line-height: 1.5;
        text-align: center !important;
    }
    
    .vm-card {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 12px;
        padding: 20px;
        height: 100%;
    }
    .vm-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #f59e0b;
        margin-bottom: 8px;
    }
    .vm-text {
        font-size: 0.88rem;
        color: #cbd5e1;
        line-height: 1.6;
    }
    
    .stat-box {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 10px;
        padding: 12px;
        text-align: center;
        margin-bottom: 8px;
    }
    .stat-number {
        font-size: 1.25rem;
        font-weight: 700;
        color: #f8fafc;
    }
    .stat-label {
        font-size: 0.75rem;
        color: #94a3b8;
        margin-top: 2px;
    }
    
    div[data-baseweb="select"] > div {
        background-color: #111827 !important;
        border-color: #1f2937 !important;
        color: #f8fafc !important;
        border-radius: 8px !important;
    }
    
    .stIframe iframe {
        border-radius: 12px;
        border: 1px solid #1f2937;
    }
</style>
""", unsafe_allow_html=True)

# === 5. TOP NAVIGATION BAR ===
st.markdown(f"""
<div class="top-header-container">
    <img src="data:image/png;base64,{logo_b64}" class="logo-img-style" alt="Logo Karang Taruna"/>
    <div>
        <div style="font-weight: 800; font-size: 1.1rem; color: #f8fafc; line-height: 1.2;">KARANG TARUNA RW 11</div>
        <div style="font-size: 0.78rem; color: #94a3b8; margin-top: 2px;">Portal Resmi & Arsip Digital Kemerdekaan</div>
    </div>
</div>
<hr style="border: 0; border-top: 1px solid #1f2937; margin-top: 4px; margin-bottom: 20px;">
""", unsafe_allow_html=True)

# === 6. HERO SECTION BANNER ===
st.markdown("""
<div class="hero-box">
    <span class="hero-tag">Arsip Kemerdekaan Agustus</span>
    <div class="hero-h1">Galeri Kegiatan RW 11</div>
    <p class="hero-p">Dokumentasi resmi seluruh rangkaian acara Pentas Seni dan Jalan Sehat Peringatan HUT RI Karang Taruna RW 11 periode 2022 hingga 2026.</p>
</div>
""", unsafe_allow_html=True)

# === 7. VISI & MISI SECTION ===
col_visi, col_misi = st.columns(2)

with col_visi:
    st.markdown("""
    <div class="vm-card">
        <div class="vm-title">🎯 Visi Kami</div>
        <div class="vm-text">
            Mewujudkan generasi muda RW 11 yang solid, kreatif, berakhlak mulia, serta aktif berkontribusi dalam pembangunan kebersamaan dan kemajuan lingkungan masyarakat.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_misi:
    st.markdown("""
    <div class="vm-card">
        <div class="vm-title">🚀 Misi Utama</div>
        <div class="vm-text">
            • Mempererat tali silaturahmi antar pemuda dan warga RW 11.<br>
            • Menyelenggarakan kegiatan kebudayaan, olahraga, dan sosial yang positif.<br>
            • Membangun jiwa kepemimpinan dan kewirausahaan generasi muda.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# === 8. STATISTIK RINGKAS ===
s1, s2, s3, s4 = st.columns(4)
with s1:
    st.markdown('<div class="stat-box"><div class="stat-number">4 RT 1 RW</div><div class="stat-label">Penasehat</div></div>', unsafe_allow_html=True)
with s2:
    st.markdown('<div class="stat-box"><div class="stat-number">2022–2026</div><div class="stat-label">Periode Arsip</div></div>', unsafe_allow_html=True)
with s3:
    st.markdown('<div class="stat-box"><div class="stat-number">Agustus</div><div class="stat-label">Bulan Kegiatan</div></div>', unsafe_allow_html=True)
with s4:
    st.markdown('<div class="stat-box"><div class="stat-number">2 Acara Utama</div><div class="stat-label">Pentas Seni & Jalan Sehat</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# === 9. BANNER FOTO MUDA MUDI (PROPORSIONAL & DI TENGAH) ===
if img_muda_mudi:
    _, col_foto, _ = st.columns([1, 3, 1])
    with col_foto:
        st.image(img_muda_mudi, use_container_width=True)

st.markdown("<hr style='border: 0; border-top: 1px solid #1f2937;'><br>", unsafe_allow_html=True)

# === 10. FILTER TAHUN & FOLDER KEGIATAN ===
st.subheader("🖼️ Pilih Dokumentasi Kegiatan")

col_tahun, col_kegiatan = st.columns(2)

with col_tahun:
    tahun_pilihan = st.selectbox(
        "📅 Pilih Tahun :",
        ["2026", "2025", "2024", "2023", "2022"],
        index=4
    )

with col_kegiatan:
    kegiatan_pilihan = st.selectbox(
        "🎪 Pilih Kegiatan:",
        ["Pentas Seni", "Jalan Sehat"],
        index=0
    )

# === 11. TAMPILKAN GALERI EMBED GOOGLE DRIVE ===
folder_id = DATABASE_FOLDER_DRIVE.get(tahun_pilihan, {}).get(kegiatan_pilihan, "")

if folder_id:
    st.info(f"Menampilkan seluruh Dokumentasi: **{kegiatan_pilihan} ({tahun_pilihan})**")
    embed_url = f"https://drive.google.com/embeddedfolderview?id={folder_id}#grid"
    components.iframe(embed_url, height=500, scrolling=True)
else:
    st.warning(f"Folder untuk kegiatan **{kegiatan_pilihan} ({tahun_pilihan})** belum terhubung atau masih kosong.")

# === 12. MEDIA SOSIAL & FOOTER ===
st.markdown("<br><hr style='border: 0; border-top: 1px solid #1f2937;'><br>", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; padding: 10px;">
    <h4 style="color: #f8fafc; margin-bottom: 14px; font-weight: 600;">Ikuti Media Sosial Kami</h4>
    <div style="display: flex; justify-content: center; gap: 24px; flex-wrap: wrap; margin-bottom: 20px;">
        <a href="https://www.instagram.com/jabonsurvival/" target="_blank" style="color: #fbbf24; text-decoration: none; font-weight: 500; font-size: 0.95rem; display: flex; align-items: center; gap: 6px;">
            🅾 Instagram: @jabonsurvival
        </a>
        <a href="https://www.tiktok.com/@jabonsurvival_?_r=1&_t=ZS-99Ws1FncF6N" target="_blank" style="color: #38bdf8; text-decoration: none; font-weight: 500; font-size: 0.95rem; display: flex; align-items: center; gap: 6px;">
            ᕷ TikTok: @jabonsurvival_
        </a>
        <a href="https://www.youtube.com/@muda-mudijabonsurvivalrw1149" target="_blank" style="color: #38bdf8; text-decoration: none; font-weight: 500; font-size: 0.95rem; display: flex; align-items: center; gap: 6px;">
                    ▶ YouTube: @muda mudi jabonsurvival
        </a>          
    </div>
</div>

<div style="text-align: center; padding: 15px; border-top: 1px solid #1f2937; color: #64748b; font-size: 0.8rem;">
    © 2026 Pengurus Karang Taruna RW 11. Seluruh Hak Cipta Dilindungi.<br>
</div>
""", unsafe_allow_html=True)
