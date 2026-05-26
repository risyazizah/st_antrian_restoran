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

        # Ambil tamu terdepan
        tamu = self.front
        self.front = self.front.next

        # Kalau antrian jadi kosong, rear juga di-reset
        if self.front is None:
            self.rear = None

        self.count -= 1
        return tamu

    def peek(self):
        """Melihat tamu paling depan tanpa menghapus"""

        if self.is_empty():
            return None

        return self.front

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
# SETUP SESSION STATE — agar data tidak hilang
# =============================================
if "antrian" not in st.session_state:
    st.session_state.antrian = QueueLinkedList()

if "riwayat" not in st.session_state:
    st.session_state.riwayat = []

if "total_dilayani" not in st.session_state:
    st.session_state.total_dilayani = 0

# Shortcut supaya tidak perlu nulis st.session_state.antrian terus
antrian = st.session_state.antrian


# =============================================
# TAMPILAN STREAMLIT
# =============================================
st.set_page_config(page_title="Antrian Restoran", page_icon="🍽️", layout="wide")

st.title("🍽️ Sistem Antrian Restoran")
st.caption("Menggunakan struktur data Queue Linked List")
st.divider()


# --- STATISTIK ---
col1, col2, col3 = st.columns(3)
col1.metric("Kelompok Antri", antrian.get_size())
col2.metric("Total Tamu", sum(t.jumlah_orang for t in antrian.ke_list()))
col3.metric("Sudah Dilayani", st.session_state.total_dilayani)

st.divider()


# --- FORM INPUT & TOMBOL ---
kiri, kanan = st.columns([1, 1], gap="large")

with kiri:
    st.subheader("Daftarkan Tamu Baru")

    nama    = st.text_input("Nama tamu / kode meja", placeholder="contoh: Budi Santoso")
    jumlah  = st.number_input("Jumlah orang", min_value=1, max_value=20, value=2)
    catatan = st.text_input("Catatan (opsional)", placeholder="VIP, alergi, dll.")

    col_a, col_b = st.columns(2)

    with col_a:
        if st.button("➕ Tambah Antrian", use_container_width=True):
            if nama.strip():
                antrian.enqueue(nama.strip(), jumlah, catatan.strip())
                st.toast(f"✅ {nama} masuk antrian!")
                st.rerun()
            else:
                st.warning("Isi nama tamu dulu ya.")

    with col_b:
        if st.button("✅ Layani Berikutnya", use_container_width=True):
            tamu = antrian.dequeue()
            if tamu:
                st.session_state.riwayat.insert(0, tamu)
                st.session_state.total_dilayani += 1
                st.toast(f"🎉 {tamu.nama} sedang dilayani!")
                st.rerun()
            else:
                st.warning("Antrian masih kosong.")

    # --- RIWAYAT DILAYANI ---
    if st.session_state.riwayat:
        st.divider()
        st.subheader("Riwayat Dilayani")

        for tamu in st.session_state.riwayat[:8]:
            st.success(f"✓ **{tamu.nama}** — {tamu.jumlah_orang} orang · {tamu.waktu}")


# --- DAFTAR ANTRIAN SAAT INI ---
with kanan:
    st.subheader("Antrian Saat Ini")

    daftar = antrian.ke_list()

    if not daftar:
        st.info("🪑 Antrian masih kosong.")
    else:
        for i, tamu in enumerate(daftar):
            nomor = i + 1

            if nomor == 1:
                # Tamu paling depan ditandai khusus
                label = f"🔴 #{nomor} **{tamu.nama}** ← GILIRAN BERIKUTNYA"
                st.error(label)
            else:
                label = f"🟡 #{nomor} **{tamu.nama}**"
                st.warning(label)

            st.caption(
                f"👥 {tamu.jumlah_orang} orang  |  "
                f"⏱ {tamu.waktu}"
                + (f"  |  📝 {tamu.catatan}" if tamu.catatan else "")
            )
