import streamlit as st
from datetime import datetime

# =============================================
# NODE — satu tamu dalam antrian
# =============================================
class Node:
    def __init__(self, nama, jumlah_orang, catatan=""):
        self.nama = nama
        self.jumlah_orang = jumlah_orang
        self.catatan = catatan
        self.waktu = datetime.now().strftime("%H:%M")
        self.next = None  # pointer ke tamu berikutnya


# =============================================
# QUEUE LINKED LIST — antrian FIFO
# =============================================
class QueueLinkedList:
    def __init__(self):
        self.head = None   # tamu paling depan (giliran berikutnya)
        self.tail = None   # tamu paling belakang (baru masuk)
        self.ukuran = 0

    def kosong(self):
        return self.head is None

    def enqueue(self, nama, jumlah_orang, catatan=""):
        """Tambah tamu baru ke BELAKANG antrian."""
        node = Node(nama, jumlah_orang, catatan)
        if self.tail:
            self.tail.next = node   # sambungkan ke node terakhir
        else:
            self.head = node        # kalau antrian kosong, jadi head sekaligus
        self.tail = node
        self.ukuran += 1

    def dequeue(self):
        """Layani tamu paling DEPAN, hapus dari antrian."""
        if self.kosong():
            return None
        dilayani = self.head
        self.head = self.head.next  # maju ke tamu berikutnya
        if self.head is None:
            self.tail = None
        self.ukuran -= 1
        dilayani.next = None
        return dilayani

    def peek(self):
        """Lihat tamu terdepan tanpa menghapus."""
        return self.head

    def ke_list(self):
        """Ubah linked list jadi list biasa (untuk tampilan)."""
        result = []
        cur = self.head
        while cur:
            result.append(cur)
            cur = cur.next
        return result


# =============================================
# SETUP SESSION STATE
# =============================================
if "antrian" not in st.session_state:
    st.session_state.antrian = QueueLinkedList()

if "log" not in st.session_state:
    st.session_state.log = []

if "total_dilayani" not in st.session_state:
    st.session_state.total_dilayani = 0

antrian: QueueLinkedList = st.session_state.antrian


# =============================================
# TAMPILAN (CSS)
# =============================================
st.set_page_config(page_title="Antrian Restoran", page_icon="🍽️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=Fraunces:ital,wght@0,700;1,400&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; background: #f7f5f0; color: #1a1814; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem; max-width: 1100px; }

.hero { text-align: center; padding: 2rem 0 1rem; }
.hero h1 { font-family: 'Fraunces', serif; font-size: 2.8rem; font-weight: 700; color: #1a1814; margin: 0; }
.hero h1 span { color: #c05a2a; }
.hero p { color: #888; font-size: 0.82rem; letter-spacing: 0.2em; text-transform: uppercase; margin-top: 6px; }

.stat-grid { display: flex; gap: 12px; margin: 1.5rem 0; }
.stat { flex: 1; background: white; border: 1px solid #ebe8e0; border-radius: 12px; padding: 1.2rem; text-align: center; }
.stat .num { font-family: 'Fraunces', serif; font-size: 2.2rem; color: #c05a2a; line-height: 1; }
.stat .lbl { font-size: 0.72rem; color: #aaa; text-transform: uppercase; letter-spacing: 0.12em; margin-top: 4px; }

.queue-card { background: white; border: 1px solid #ebe8e0; border-radius: 12px; padding: 1rem 1.2rem; margin-bottom: 8px; display: flex; align-items: center; gap: 14px; }
.queue-card.aktif { border-color: #c05a2a; background: #fdf5f0; }
.avatar { width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 600; font-size: 13px; flex-shrink: 0; }
.av-aktif { background: #fad5c0; color: #712b13; }
.av-normal { background: #f0ede8; color: #888; }
.q-nama { font-weight: 500; font-size: 15px; color: #1a1814; }
.q-meta { font-size: 12px; color: #aaa; margin-top: 2px; }
.q-catatan { font-size: 11px; color: #c05a2a; margin-top: 2px; }
.badge-next { background: #fad5c0; color: #712b13; font-size: 10px; border-radius: 20px; padding: 2px 9px; font-weight: 600; }
.badge-no { background: #f0ede8; color: #aaa; font-size: 12px; border-radius: 20px; padding: 2px 9px; }
.badge-orang { font-size: 12px; color: #888; }

.log-item { display: flex; align-items: center; gap: 10px; padding: 7px 0; border-bottom: 1px solid #f0ede8; font-size: 13px; }
.log-item:last-child { border: none; }
.log-nama { flex: 1; font-weight: 500; color: #1a1814; }
.log-meta { color: #aaa; font-size: 11px; }

.empty { text-align: center; padding: 3rem 1rem; color: #ccc; font-size: 0.95rem; }

div[data-testid="column"]:nth-child(1) .stButton > button {
    background: #c05a2a !important; color: white !important;
    border: none !important; border-radius: 8px !important; font-weight: 500 !important;
}
div[data-testid="column"]:nth-child(2) .stButton > button {
    background: #1a1814 !important; color: white !important;
    border: none !important; border-radius: 8px !important; font-weight: 500 !important;
}
input, .stTextInput input, .stNumberInput input {
    border-radius: 8px !important; border: 1px solid #ddd !important; background: white !important;
}
.stTextInput label, .stNumberInput label { font-size: 13px !important; color: #666 !important; }
</style>
""", unsafe_allow_html=True)


# =============================================
# HEADER
# =============================================
st.markdown("""
<div class="hero">
    <h1>🍽 La <span>File</span></h1>
    <p>Sistem Antrian Restoran · Queue Linked List</p>
</div>
""", unsafe_allow_html=True)


# =============================================
# STATISTIK
# =============================================
daftar = antrian.ke_list()
total_orang = sum(t.jumlah_orang for t in daftar)

st.markdown(f"""
<div class="stat-grid">
    <div class="stat"><div class="num">{antrian.ukuran}</div><div class="lbl">Kelompok Antri</div></div>
    <div class="stat"><div class="num">{total_orang}</div><div class="lbl">Total Tamu</div></div>
    <div class="stat"><div class="num">{st.session_state.total_dilayani}</div><div class="lbl">Sudah Dilayani</div></div>
</div>
""", unsafe_allow_html=True)


# =============================================
# LAYOUT 2 KOLOM
# =============================================
kiri, kanan = st.columns([1, 1], gap="large")

# ── Kolom Kiri: Form Input ──
with kiri:
    st.markdown("##### Daftarkan Tamu Baru")

    nama = st.text_input("Nama tamu / kode meja", placeholder="contoh: Budi Santoso")
    col_a, col_b = st.columns(2)
    with col_a:
        jumlah = st.number_input("Jumlah orang", min_value=1, max_value=20, value=2)
    with col_b:
        catatan = st.text_input("Catatan", placeholder="VIP, alergi, dll.")

    st.markdown("<br/>", unsafe_allow_html=True)
    col_btn1, col_btn2 = st.columns(2)

    with col_btn1:
        if st.button("＋ Tambah Antrian", use_container_width=True):
            if nama.strip():
                antrian.enqueue(nama.strip(), jumlah, catatan.strip())
                st.toast(f"✅ {nama} masuk antrian!")
                st.rerun()
            else:
                st.warning("Isi nama tamu dulu ya.")

    with col_btn2:
        if st.button("✓ Layani Berikutnya", use_container_width=True):
            dilayani = antrian.dequeue()
            if dilayani:
                st.session_state.log.insert(0, dilayani)
                st.session_state.total_dilayani += 1
                st.toast(f"🎉 {dilayani.nama} sedang dilayani!")
                st.rerun()
            else:
                st.warning("Antrian kosong.")

    # Riwayat tamu yang sudah dilayani
    if st.session_state.log:
        st.markdown("<br/>", unsafe_allow_html=True)
        st.markdown("##### Riwayat Dilayani")
        rows = ""
        for t in st.session_state.log[:8]:
            rows += f"""
            <div class="log-item">
                <span style="color:#c05a2a">✓</span>
                <span class="log-nama">{t.nama}</span>
                <span class="log-meta">{t.jumlah_orang} org · {t.waktu}</span>
            </div>"""
        st.markdown(f'<div style="background:white;border:1px solid #ebe8e0;border-radius:12px;padding:1rem 1.2rem">{rows}</div>', unsafe_allow_html=True)


# ── Kolom Kanan: Daftar Antrian ──
with kanan:
    st.markdown("##### Antrian Saat Ini")

    if not daftar:
        st.markdown('<div class="empty">🪑<br/>Antrian masih kosong</div>', unsafe_allow_html=True)
    else:
        for i, tamu in enumerate(daftar):
            is_next = (i == 0)
            inisial = "".join(w[0] for w in tamu.nama.split())[:2].upper()
            av_cls = "av-aktif" if is_next else "av-normal"
            card_cls = "queue-card aktif" if is_next else "queue-card"
            badge = '<span class="badge-next">NEXT</span>' if is_next else f'<span class="badge-no">#{i+1}</span>'
            catatan_html = f'<div class="q-catatan">📝 {tamu.catatan}</div>' if tamu.catatan else ""

            st.markdown(f"""
            <div class="{card_cls}">
                <div class="avatar {av_cls}">{inisial}</div>
                <div style="flex:1">
                    <div class="q-nama">{tamu.nama}</div>
                    <div class="q-meta">⏱ {tamu.waktu}</div>
                    {catatan_html}
                </div>
                <div style="display:flex;flex-direction:column;align-items:flex-end;gap:5px">
                    {badge}
                    <span class="badge-orang">👥 {tamu.jumlah_orang}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)


# =============================================
# FOOTER
# =============================================
st.markdown("""
<br/>
<div style="text-align:center;font-size:0.7rem;color:#ccc;letter-spacing:0.15em;text-transform:uppercase;border-top:1px solid #ebe8e0;padding-top:1.5rem">
    La File Restoran · Queue Linked List · Python + Streamlit
</div>
""", unsafe_allow_html=True)
