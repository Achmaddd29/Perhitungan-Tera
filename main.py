import streamlit as st
import numpy as np

# Judul Aplikasi
st.title("Perhitungan Kapasitas dalam Ton/Jam")

# Input dari pengguna
berat_kotor = st.number_input("Masukkan berat kotor (kg):", min_value=0.0, format="%.2f")
waktu = st.number_input("Masukkan waktu (detik):", min_value=1.0, format="%.2f")
berapa_jam = st.number_input("Masukkan jumlah jam:", min_value=0.0, format="%.2f")
ketinggian = st.number_input("Masukkan ketinggian serbuk (meter):", min_value=0.0, format="%.2f")

# Validasi input
if waktu > 0:
    dasar_perhitungan = ((berat_kotor - 4) / waktu) * 3600 * berapa_jam

    # Kondisi berdasarkan ketinggian
    if ketinggian > 1.5:
        hasil = dasar_perhitungan * np.sqrt(ketinggian / 1.5)
    elif 0 < ketinggian <= 1.5:
        hasil = dasar_perhitungan * (ketinggian / 1.5)
    else:
        hasil = dasar_perhitungan * 0.5

    # Konversi ke ton/jam
    hasil_ton_per_jam = hasil / 1000

    st.success(f"Hasil perhitungan: {hasil_ton_per_jam:.2f} ton/jam")
else:
    st.error("Waktu harus lebih besar dari 0")
