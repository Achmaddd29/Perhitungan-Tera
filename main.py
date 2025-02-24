import streamlit as st
import numpy as np

# Custom CSS untuk mempercantik tampilan
st.markdown(
    """
    <style>
        /* Pusatkan judul */
        .title {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: #ffffff;
        }
        /* Background gradient */
        body {
            background: linear-gradient(to right, #2c3e50, #4ca1af);
            color: white;
        }
        /* Styling box input */
        .stNumberInput > label {
            font-size: 18px;
            font-weight: bold;
            color: white;
        }
        .stTextInput, .stNumberInput, .stButton {
            border-radius: 10px;
            padding: 8px;
        }
        /* Styling hasil */
        .hasil-box {
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            background: #2ecc71;
            padding: 10px;
            border-radius: 10px;
            color: white;
            margin-top: 20px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Judul Aplikasi
st.markdown("<h1 class='title'>Perhitungan Kapasitas dalam Ton/Jam</h1>", unsafe_allow_html=True)

# Input dari pengguna dengan keterangan
berat_kotor = st.number_input(
    "Masukkan berat kotor (kg):",
    min_value=0.0,
    format="%.2f",
    help="Berat total material dalam kilogram sebelum dikurangi berat tetap (4 kg)."
)

waktu = st.number_input(
    "Masukkan waktu (detik):",
    min_value=1.0,
    format="%.2f",
    help="Waktu proses dalam satuan detik."
)

berapa_jam = st.number_input(
    "Masukkan jumlah jam:",
    min_value=0.0,
    format="%.2f",
    help="Durasi proses dalam jam yang ingin dihitung."
)

ketinggian = st.number_input(
    "Masukkan ketinggian serbuk (meter):",
    min_value=0.0,
    format="%.2f",
    help="Tinggi tumpukan serbuk kayu dalam meter."
)

# Validasi input
if waktu > 0 and berapa_jam > 0:
    dasar_perhitungan = ((berat_kotor - 4) / waktu) * 3600

    # Kondisi berdasarkan ketinggian
    if ketinggian > 1.5:
        hasil_per_jam = dasar_perhitungan * np.sqrt(ketinggian / 1.5)
    elif 0 < ketinggian <= 1.5:
        hasil_per_jam = dasar_perhitungan * (ketinggian / 1.5)
    else:
        hasil_per_jam = dasar_perhitungan * 0.5

    # Total hasil berdasarkan jumlah jam yang dimasukkan
    hasil_total = hasil_per_jam * berapa_jam

    # Konversi ke ton/jam
    hasil_per_jam_ton = hasil_per_jam / 1000
    hasil_total_ton = hasil_total / 1000

    # Menampilkan hasil
    st.markdown(f"<div class='hasil-box'>Hasil per jam: {hasil_per_jam_ton:.2f} ton/jam</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='hasil-box'>Hasil total untuk {berapa_jam:.2f} jam: {hasil_total_ton:.2f} ton</div>", unsafe_allow_html=True)
else:
    st.error("Waktu dan jumlah jam harus lebih besar dari 0")

# Instruksi Pemakaian
st.markdown(
    """

    ## 📌 Instruksi Pemakaian:
    
    1️⃣ **Masukkan berat kotor** material dalam kilogram (kg) pada kolom pertama.
    
    2️⃣ **Masukkan waktu proses** dalam detik (s) pada kolom kedua.
    
    3️⃣ **Masukkan jumlah jam** proses yang ingin dihitung.
    
    4️⃣ **Masukkan ketinggian serbuk kayu** dalam meter (m).
    
    5️⃣ Tekan **Enter** atau klik di luar kolom input untuk melihat hasil perhitungan.
    
    6️⃣ Hasil akan ditampilkan dalam **ton per jam** serta **total kapasitas produksi** berdasarkan jumlah jam yang diinput.
    
    🎯 *Pastikan semua input sudah benar agar hasil yang didapat akurat!* ✅
    """,
    unsafe_allow_html=True
)
