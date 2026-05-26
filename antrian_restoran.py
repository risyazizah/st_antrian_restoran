import streamlit as st
from datetime import datetime


# =============================================
# NODE — menyimpan data satu tamu
# =============================================
class Node:
    """Node untuk linked list"""

    def __init__(self, nama, jumlah_orang, catatan=""):
        self.nama = nama
        self.jumlah_orang = jumlah_orang
        self.catatan = catatan
        self.waktu = datetime.now().strftime("%H:%M")
        self.next = None


# =============================================
# QUEUE LINKED LIST — antrian tamu restoran
# =============================================
class QueueLinkedList:
    """Implementasi Queue menggunakan Linked List"""

    def __init__(self):
        self.front = None   # tamu paling depan (giliran berikutnya)
        self.rear = None    # tamu paling belakang (baru masuk)
        self.count = 0

    def enqueue(self, nama, jumlah_orang, catatan=""):
        """Menambahkan tamu baru ke belakang antrian"""

        node_baru = Node(nama, jumlah_orang, catatan)

        if self.rear is None:
            # Antrian masih kosong, tamu ini jadi yang pertama
            self.front = node_baru
            self.rear = node_baru
        else:
            # Sambungkan ke tamu terakhir, lalu pindahkan rear
            self.rear.next = node_baru
            self.rear = node_baru

        self.count += 1

    def dequeue(self):
        """Melayani tamu paling depan, hapus dari antrian"""

        if self.is_empty():
            return None

        tamu = self.front
        self.front = self.front.next

        if self.front is None:
            self.rear = None

        self.count -= 1
        return tamu

    def peek(self):
        """Melihat tamu paling depan tanpa menghapus"""
        return self.front if not self.is_empty() else None

    def is_empty(self):
        """Mengecek apakah antrian kosong"""
        return self.front is None

    def get_size(self):
        """Mengembalikan jumlah kelompok dalam antrian"""
        return self.count

    def ke_list(self):
        """Mengubah linked list menjadi list biasa untuk ditampilkan"""

        hasil = []
        current = self.front
        while current:
            hasil.append(current)
            current = current.next
        return hasil


# =============================================
# SETUP SESSION STATE
# =============================================
if "antrian" not in st.session_state:
    st.session_state.antrian = QueueLinkedList()
if "riwayat" not in st.session_state:
    st.session_state.riwayat = []
if "total_dilayani" not in st.session_state:
    st.session_state.total_dilayani = 0

antrian = st.session_state.antrian


# =============================================
# PAGE CONFIG & CSS
# =============================================
st.set_page_config(page_title="Antrian Restoran", page_icon="🍽️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background-color: #f9f4ee;
    color: #1e1a14;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem; max-width: 1100px; }

/* HERO */
.hero {
    background: #2c1a0e;
    border-radius: 20px;
    padding: 2.5rem 2rem;
    text-align: center;
    margin-bottom: 1.8rem;
}
.hero h1 {
    font-size: 2.6rem;
    font-weight: 700;
    color: #f5deb3;
    margin: 0;
    letter-spacing: -0.5px;
}
.hero p {
    color: #a07850;
    font-size: 0.85rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-top: 6px;
}

/* STAT CARDS */
.stat-row { display: flex; gap: 12px; margin-bottom: 1.8rem; }
.stat {
    flex: 1;
    border-radius: 14px;
    padding: 1.2rem 1rem;
    text-align: center;
}
.stat-antri  { background: #2c1a0e; }
.stat-tamu   { background: #7c3f1a; }
.stat-selesai { background: #b85c1a; }
.stat .num {
    font-size: 2.4rem;
    font-weight: 700;
    color: #f5deb3;
    line-height: 1;
}
.stat .lbl {
    font-size: 0.72rem;
    color: #c8975a;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    margin-top: 5px;
}

/* FORM CARD */
.form-card {
    background: white;
    border: 1px solid #e8ddd0;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.2rem;
}
.form-card h3 {
    font-size: 1rem;
    font-weight: 600;
    color: #2c1a0e;
    margin-bottom: 1rem;
    padding-bottom: 0.6rem;
    border-bottom: 2px solid #f5deb3;
}

/* INPUT FIELDS */
.stTextInput input, .stNumberInput input {
    background: #fdf8f3 !important;
    border: 1.5px solid #e0d0bc !important;
    border-radius: 10px !important;
    color: #1e1a14 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 14px !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: #b85c1a !important;
    box-shadow: 0 0 0 3px rgba(184,92,26,0.1) !important;
}
label { font-size: 13px !important; color: #6b5a47 !important; font-weight: 500 !important; }

/* BUTTONS */
.stButton > button {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    font-size: 14px !important;
    border: none !important;
    transition: all 0.2s !important;
    padding: 0.55rem 1rem !important;
}
div[data-testid="column"]:nth-child(1) .stButton > button {
    background: #2c1a0e !important;
    color: #f5deb3 !important;
}
div[data-testid="column"]:nth-child(1) .stButton > button:hover {
    background: #4a2e18 !important;
}
div[data-testid="column"]:nth-child(2) .stButton > button {
    background: #b85c1a !important;
    color: white !important;
}
div[data-testid="column"]:nth-child(2) .stButton > button:hover {
    background: #d4712a !important;
}

/* QUEUE CARDS */
.q-card {
    background: white;
    border: 1px solid #e8ddd0;
    border-radius: 14px;
    padding: 1rem 1.2rem;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 14px;
}
.q-card.next {
    background: #fff8f0;
    border: 2px solid #b85c1a;
}
.q-avatar {
    width: 42px; height: 42px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 14px;
    flex-shrink: 0;
}
.av-next   { background: #f5deb3; color: #7c3f1a; }
.av-normal { background: #f0ebe4; color: #8a7060; }
.q-info { flex: 1; }
.q-nama { font-size: 15px; font-weight: 600; color: #1e1a14; }
.q-meta { font-size: 12px; color: #a07850; margin-top: 3px; }
.q-catatan { font-size: 11px; color: #b85c1a; margin-top: 2px; }
.badge-next {
    background: #f5deb3; color: #7c3f1a;
    font-size: 10px; font-weight: 700;
    border-radius: 20px; padding: 3px 10px;
    text-transform: uppercase; letter-spacing: 0.05em;
}
.badge-no {
    background: #f0ebe4; color: #a07850;
    font-size: 12px; border-radius: 20px; padding: 3px 10px;
}
.badge-orang { font-size: 13px; color: #a07850; margin-top: 4px; }

/* RIWAYAT */
.log-item {
    display: flex; align-items: center; gap: 10px;
    padding: 8px 12px;
    background: #f0faf4;
    border: 1px solid #b8e0c8;
    border-radius: 10px;
    margin-bottom: 7px;
    font-size: 13px;
}
.log-nama { flex: 1; font-weight: 600; color: #1a4a2e; }
.log-meta { color: #5a8a6a; font-size: 11px; }

/* EMPTY STATE */
.empty {
    text-align: center; padding: 3rem 1rem;
    color: #c8b8a0; font-size: 0.95rem;
    background: white; border: 1px solid #e8ddd0;
    border-radius: 14px;
}
</style>
""", unsafe_allow_html=True)


# =============================================
# HERO
# =============================================
st.markdown("""
<div class="hero">
    <h1>🍽️ Antrian Restoran</h1>
    <p>Sistem Manajemen Antrian · Queue Linked List</p>
</div>
""", unsafe_allow_html=True)


# =============================================
# STATISTIK
# =============================================
daftar = antrian.ke_list()
total_orang = sum(t.jumlah_orang for t in daftar)

st.markdown(f"""
<div class="stat-row">
    <div class="stat stat-antri">
        <div class="num">{antrian.get_size()}</div>
        <div class="lbl">Kelompok Antri</div>
    </div>
    <div class="stat stat-tamu">
        <div class="num">{total_orang}</div>
        <div class="lbl">Total Tamu</div>
    </div>
    <div class="stat stat-selesai">
        <div class="num">{st.session_state.total_dilayani}</div>
        <div class="lbl">Sudah Dilayani</div>
    </div>
</div>
""", unsafe_allow_html=True)


# =============================================
# LAYOUT 2 KOLOM
# =============================================
kiri, kanan = st.columns([1, 1], gap="large")

# ── KOLOM KIRI: Form ──
with kiri:
    st.markdown('<div class="form-card"><h3>📋 Daftarkan Tamu Baru</h3>', unsafe_allow_html=True)

    nama    = st.text_input("Nama tamu / kode meja", placeholder="contoh: Budi Santoso")
    col_a, col_b = st.columns(2)
    with col_a:
        jumlah = st.number_input("Jumlah orang", min_value=1, max_value=20, value=2)
    with col_b:
        catatan = st.text_input("Catatan", placeholder="VIP, alergi...")

    st.markdown("</div>", unsafe_allow_html=True)

    col_btn1, col_btn2 = st.columns(2)

    with col_btn1:
        if st.button("➕ Tambah Antrian", use_container_width=True):
            if nama.strip():
                antrian.enqueue(nama.strip(), jumlah, catatan.strip())
                st.toast(f"✅ {nama} masuk antrian!")
                st.rerun()
            else:
                st.warning("Isi nama tamu dulu ya.")

    with col_btn2:
        if st.button("✅ Layani Berikutnya", use_container_width=True):
            tamu = antrian.dequeue()
            if tamu:
                st.session_state.riwayat.insert(0, tamu)
                st.session_state.total_dilayani += 1
                st.toast(f"🎉 {tamu.nama} sedang dilayani!")
                st.rerun()
            else:
                st.warning("Antrian masih kosong.")

    # Riwayat dilayani
    if st.session_state.riwayat:
        st.markdown("<br/>", unsafe_allow_html=True)
        st.markdown("**✔ Riwayat Dilayani**")
        for tamu in st.session_state.riwayat[:6]:
            st.markdown(f"""
            <div class="log-item">
                <span style="color:#2a7a4a;font-size:16px">✓</span>
                <span class="log-nama">{tamu.nama}</span>
                <span class="log-meta">{tamu.jumlah_orang} orang · {tamu.waktu}</span>
            </div>""", unsafe_allow_html=True)


# ── KOLOM KANAN: Daftar Antrian ──
with kanan:
    st.markdown("**🪑 Antrian Saat Ini**")
    st.markdown("<br/>", unsafe_allow_html=True)

    daftar = antrian.ke_list()

    if not daftar:
        st.markdown('<div class="empty">🪑<br/>Antrian masih kosong</div>', unsafe_allow_html=True)
    else:
        for i, tamu in enumerate(daftar):
            nomor   = i + 1
            is_next = (i == 0)
            inisial = "".join(w[0] for w in tamu.nama.split())[:2].upper()
            av_cls  = "av-next" if is_next else "av-normal"
            card_cls = "q-card next" if is_next else "q-card"
            badge   = '<span class="badge-next">▶ Next</span>' if is_next else f'<span class="badge-no">#{nomor}</span>'
            catatan_html = f'<div class="q-catatan">📝 {tamu.catatan}</div>' if tamu.catatan else ""

            st.markdown(f"""
            <div class="{card_cls}">
                <div class="q-avatar {av_cls}">{inisial}</div>
                <div class="q-info">
                    <div class="q-nama">{tamu.nama}</div>
                    <div class="q-meta">⏱ {tamu.waktu}</div>
                    {catatan_html}
                </div>
                <div style="text-align:right">
                    {badge}
                    <div class="badge-orang">👥 {tamu.jumlah_orang}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
