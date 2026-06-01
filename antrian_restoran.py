import streamlit as st
import time
from datetime import datetime

# ─────────────────────────────────────────
#   QUEUE LINKED LIST IMPLEMENTATION
# ─────────────────────────────────────────

class Node:
    """Setiap tamu adalah sebuah Node."""
    def __init__(self, nama: str, jumlah_orang: int, catatan: str = ""):
        self.nama = nama
        self.jumlah_orang = jumlah_orang
        self.catatan = catatan
        self.waktu_daftar = datetime.now().strftime("%H:%M:%S")
        self.next = None


class QueueLinkedList:
    """Antrian berbasis Linked List — FIFO."""

    def __init__(self):
        self.head = None   # Tamu paling depan
        self.tail = None   # Tamu paling belakang
        self._size = 0

    def is_empty(self) -> bool:
        return self.head is None

    def enqueue(self, nama: str, jumlah_orang: int, catatan: str = ""):
        """Tambah tamu baru ke belakang antrian."""
        node = Node(nama, jumlah_orang, catatan)
        if self.tail:
            self.tail.next = node
        else:
            self.head = node
        self.tail = node
        self._size += 1

    def dequeue(self) -> Node | None:
        """Layani tamu paling depan."""
        if self.is_empty():
            return None
        served = self.head
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self._size -= 1
        served.next = None
        return served

    def peek(self) -> Node | None:
        """Lihat tamu terdepan tanpa menghapus."""
        return self.head

    def size(self) -> int:
        return self._size

    def to_list(self) -> list[Node]:
        """Konversi antrian ke Python list (untuk tampilan)."""
        result = []
        cur = self.head
        while cur:
            result.append(cur)
            cur = cur.next
        return result


# ─────────────────────────────────────────
#   SESSION STATE INIT
# ─────────────────────────────────────────

if "queue" not in st.session_state:
    st.session_state.queue = QueueLinkedList()

if "log" not in st.session_state:
    st.session_state.log = []   # Riwayat tamu yang telah dilayani

if "total_dilayani" not in st.session_state:
    st.session_state.total_dilayani = 0

queue: QueueLinkedList = st.session_state.queue


# ─────────────────────────────────────────
#   PAGE CONFIG & CUSTOM CSS
# ─────────────────────────────────────────

st.set_page_config(
    page_title="Antrian Restoran",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0f0d0a;
    color: #f0ead6;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem; max-width: 1200px; }

/* ── Hero Title ── */
.hero {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
    margin-bottom: 0.5rem;
}
.hero h1 {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.4rem, 5vw, 4rem);
    font-weight: 900;
    letter-spacing: -1px;
    color: #f0ead6;
    margin: 0;
    line-height: 1.1;
}
.hero .accent { color: #c9a96e; }
.hero .subtitle {
    font-size: 0.9rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #7a6e5a;
    margin-top: 0.5rem;
}
.divider {
    border: none;
    border-top: 1px solid #2a2520;
    margin: 1.5rem 0;
}

/* ── Stat Cards ── */
.stat-row { display: flex; gap: 1rem; margin-bottom: 1.5rem; }
.stat-card {
    flex: 1;
    background: #1a1714;
    border: 1px solid #2a2520;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    text-align: center;
}
.stat-card .num {
    font-family: 'Playfair Display', serif;
    font-size: 2.4rem;
    font-weight: 700;
    color: #c9a96e;
    line-height: 1;
}
.stat-card .lbl {
    font-size: 0.75rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #7a6e5a;
    margin-top: 0.3rem;
}

/* ── Queue Cards ── */
.queue-card {
    background: #1a1714;
    border: 1px solid #2a2520;
    border-left: 3px solid #c9a96e;
    border-radius: 10px;
    padding: 1rem 1.4rem;
    margin-bottom: 0.7rem;
    display: flex;
    align-items: center;
    gap: 1.2rem;
    transition: border-color 0.2s;
}
.queue-card:hover { border-color: #e0c285; }
.queue-card.first {
    border-left-color: #e8593a;
    background: #1e1510;
}
.queue-card .no {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: #3a352c;
    min-width: 2rem;
    text-align: center;
}
.queue-card.first .no { color: #e8593a; }
.queue-card .info { flex: 1; }
.queue-card .info .name {
    font-weight: 500;
    font-size: 1.05rem;
    color: #f0ead6;
}
.queue-card .info .meta {
    font-size: 0.78rem;
    color: #7a6e5a;
    margin-top: 0.2rem;
}
.queue-card .badge {
    background: #2a2520;
    border-radius: 20px;
    padding: 0.3rem 0.8rem;
    font-size: 0.8rem;
    color: #c9a96e;
    white-space: nowrap;
}
.tag-next {
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #e8593a;
    border: 1px solid #e8593a;
    border-radius: 4px;
    padding: 0.1rem 0.4rem;
    margin-left: 0.5rem;
    vertical-align: middle;
}

/* ── Form Area ── */
.form-box {
    background: #1a1714;
    border: 1px solid #2a2520;
    border-radius: 14px;
    padding: 1.8rem;
    margin-bottom: 1.5rem;
}
.form-box h3 {
    font-family: 'Playfair Display', serif;
    font-size: 1.3rem;
    margin-bottom: 1.2rem;
    color: #c9a96e;
}

/* ── Streamlit input overrides ── */
input[type="text"], input[type="number"], textarea, .stTextInput input,
.stNumberInput input, .stTextArea textarea {
    background: #0f0d0a !important;
    border: 1px solid #2a2520 !important;
    border-radius: 8px !important;
    color: #f0ead6 !important;
    font-family: 'DM Sans', sans-serif !important;
}
input::placeholder { color: #4a4337 !important; }

/* ── Buttons ── */
.stButton > button {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    border-radius: 8px !important;
    transition: all 0.2s !important;
    border: none !important;
}
div[data-testid="column"]:nth-child(1) .stButton > button {
    background: #c9a96e !important;
    color: #0f0d0a !important;
}
div[data-testid="column"]:nth-child(1) .stButton > button:hover {
    background: #e0c285 !important;
}
div[data-testid="column"]:nth-child(2) .stButton > button {
    background: #e8593a !important;
    color: #fff !important;
}
div[data-testid="column"]:nth-child(2) .stButton > button:hover {
    background: #ff6b4a !important;
}

/* ── Log table ── */
.log-row {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.6rem 0;
    border-bottom: 1px solid #1e1c18;
    font-size: 0.85rem;
    color: #a09070;
}
.log-row:last-child { border-bottom: none; }
.log-row .lname { color: #c9a96e; font-weight: 500; flex: 1; }
.log-row .ltime { color: #4a4337; font-size: 0.75rem; }

/* ── Section labels ── */
.section-label {
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #4a4337;
    margin-bottom: 0.8rem;
    margin-top: 0.5rem;
}
.empty-state {
    text-align: center;
    padding: 3rem 1rem;
    color: #3a352c;
    font-family: 'Playfair Display', serif;
    font-size: 1.1rem;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
#   HERO
# ─────────────────────────────────────────

st.markdown("""
<div class="hero">
    <h1>🍽 <span class="accent">MJ</span> Restoran</h1>
    <div class="subtitle">Sistem Manajemen Antrian &nbsp;·&nbsp; Queue Linked List</div>
</div>
<hr class="divider"/>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
#   STATS
# ─────────────────────────────────────────

total_orang = sum(n.jumlah_orang for n in queue.to_list())

st.markdown(f"""
<div class="stat-row">
    <div class="stat-card">
        <div class="num">{queue.size()}</div>
        <div class="lbl">Kelompok Antri</div>
    </div>
    <div class="stat-card">
        <div class="num">{total_orang}</div>
        <div class="lbl">Total Tamu</div>
    </div>
    <div class="stat-card">
        <div class="num">{st.session_state.total_dilayani}</div>
        <div class="lbl">Sudah Dilayani</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
#   MAIN LAYOUT — 2 kolom
# ─────────────────────────────────────────

col_left, col_right = st.columns([1.1, 1], gap="large")

# ── KOLOM KIRI: Form & Aksi ──────────────
with col_left:
    st.markdown('<div class="section-label">Daftarkan Tamu Baru</div>', unsafe_allow_html=True)

    with st.container():
        nama = st.text_input("Nama / Kode Meja", placeholder="cth. Budi Santoso")
        col_a, col_b = st.columns(2)
        with col_a:
            jumlah = st.number_input("Jumlah Orang", min_value=1, max_value=20, value=2)
        with col_b:
            catatan = st.text_input("Catatan", placeholder="Alergi, VIP, dll.")

    st.markdown("<br/>", unsafe_allow_html=True)
    col_btn1, col_btn2 = st.columns(2)

    with col_btn1:
        if st.button("＋ Tambah ke Antrian", use_container_width=True):
            if nama.strip():
                queue.enqueue(nama.strip(), jumlah, catatan.strip())
                st.toast(f"✅ {nama} masuk antrian!", icon="🍽️")
                st.rerun()
            else:
                st.warning("Masukkan nama tamu terlebih dahulu.")

    with col_btn2:
        if st.button("✓ Layani Tamu Berikut", use_container_width=True):
            served = queue.dequeue()
            if served:
                st.session_state.log.insert(0, served)
                st.session_state.total_dilayani += 1
                st.toast(f"🎉 {served.nama} kini dilayani!", icon="✨")
                st.rerun()
            else:
                st.warning("Antrian sedang kosong.")

    # ── Riwayat ──
    if st.session_state.log:
        st.markdown("<br/>", unsafe_allow_html=True)
        st.markdown('<div class="section-label">Riwayat Dilayani</div>', unsafe_allow_html=True)
        rows_html = ""
        for tamu in st.session_state.log[:8]:
            rows_html += f"""
            <div class="log-row">
                <span class="lname">✓ {tamu.nama}</span>
                <span>{tamu.jumlah_orang} org</span>
                <span class="ltime">{tamu.waktu_daftar}</span>
            </div>"""
        st.markdown(f'<div style="background:#1a1714;border:1px solid #2a2520;border-radius:10px;padding:1rem 1.2rem">{rows_html}</div>', unsafe_allow_html=True)


# ── KOLOM KANAN: Antrian Saat Ini ───────
with col_right:
    st.markdown('<div class="section-label">Antrian Saat Ini</div>', unsafe_allow_html=True)

    antrian = queue.to_list()
    if not antrian:
        st.markdown('<div class="empty-state">Belum ada tamu<br/><span style="font-size:2rem">🪑</span></div>', unsafe_allow_html=True)
    else:
        for i, tamu in enumerate(antrian):
            is_first = (i == 0)
            card_cls = "queue-card first" if is_first else "queue-card"
            next_tag = '<span class="tag-next">NEXT</span>' if is_first else ""
            catatan_html = f"<br/>📝 {tamu.catatan}" if tamu.catatan else ""
            st.markdown(f"""
            <div class="{card_cls}">
                <div class="no">#{i+1}</div>
                <div class="info">
                    <div class="name">{tamu.nama}{next_tag}</div>
                    <div class="meta">⏱ {tamu.waktu_daftar}{catatan_html}</div>
                </div>
                <div class="badge">👥 {tamu.jumlah_orang}</div>
            </div>
            """, unsafe_allow_html=True)


# ─────────────────────────────────────────
#   FOOTER
# ─────────────────────────────────────────

st.markdown("<br/>", unsafe_allow_html=True)
st.markdown("""
<hr class="divider"/>
<div style="text-align:center;font-size:0.72rem;color:#3a352c;letter-spacing:0.15em;text-transform:uppercase;">
    MJ Restoran &nbsp;·&nbsp; 
</div>
""", unsafe_allow_html=True)
