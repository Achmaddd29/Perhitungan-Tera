import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import locale

# Menentukan locale berdasarkan sistem operasi
try:
    locale.setlocale(locale.LC_TIME, 'id_ID.utf8')  # Linux/MacOS
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, 'Indonesian_Indonesia')  # Windows
    except locale.Error:
        st.warning("Locale tidak didukung, menggunakan default.")

# Fungsi untuk menghitung kapasitas rotary dryer
def calculate_dryer_capacity(weight_wet, mc_in, mc_out, fill_time):
    m_dry = weight_wet * ((1 - mc_in) / (1 - mc_out))
    boxes_per_hour = 3600 / fill_time  
    capacity_kg_per_hour = boxes_per_hour * m_dry
    capacity_ton_per_hour = capacity_kg_per_hour / 1000

    debug_data = {
        "Berat Kotak Penuh (kg)": weight_wet,
        "Moisture Content Input (%)": mc_in * 100,
        "Moisture Content Output (%)": mc_out * 100,
        "Waktu Isi Kotak (detik)": fill_time,
        "Berat Kering (kg)": m_dry,
        "Kotak per Jam": boxes_per_hour,
        "Kapasitas (kg/jam)": capacity_kg_per_hour,
        "Kapasitas (ton/jam)": capacity_ton_per_hour
    }
    return capacity_ton_per_hour, capacity_kg_per_hour, debug_data

# Konfigurasi Streamlit
st.set_page_config(page_title="Rotary Dryer Calculator", layout="wide")

# Tabs pada aplikasi
tab1, tab2, tab3 = st.tabs(["ℹ️ Instruksi Pemakaian", "📊 Kalkulator", "📢 Laporan Hasil Pengeringan"])

# Tab 1: Instruksi Penggunaan
with tab1:
    st.title("ℹ️ Instruksi Penggunaan")
    st.markdown("""
    1️⃣ **Masukkan Berat Kotak Penuh**  
    2️⃣ **Masukkan Moisture Content Input dan Output**  
    3️⃣ **Masukkan Waktu Kotak Terisi Penuh dalam detik**  
    4️⃣ **Klik tombol "Hitung Kapasitas" untuk melihat hasilnya**
    """)

# Tab 2: Kalkulator Kapasitas Rotary Dryer
with tab2:
    st.title("📌 Kalkulator Kapasitas Rotary Dryer")
    
    col1, col2 = st.columns(2)
    with col1:
        weight_wet = st.number_input("⚖️ Berat Kotak Penuh (kg)", min_value=0.1, value=11.0, step=0.1)
        mc_in = st.number_input("💧 Moisture Content Input (%)", min_value=0.0, max_value=100.0, value=55.0, step=0.1) / 100
    with col2:
        mc_out = st.number_input("🔥 Moisture Content Output (%)", min_value=0.0, max_value=100.0, value=15.0, step=0.1) / 100
        fill_time = st.number_input("⏳ Waktu Kotak Terisi Penuh (detik)", min_value=1.0, value=14.0, step=1.0)
    
    if st.button("🔍 Hitung Kapasitas"):
        capacity_ton_per_hour, capacity_kg_per_hour, debug_data = calculate_dryer_capacity(weight_wet, mc_in, mc_out, fill_time)
        st.success(f"✅ Kapasitas Rotary Dryer: {capacity_ton_per_hour:.2f} ton/jam")

        debug_df = pd.DataFrame(debug_data.items(), columns=["Parameter", "Nilai"])
        st.table(debug_df)

        data = pd.DataFrame({"Parameter": ["Input", "Output"], "Moisture Content": [mc_in * 100, mc_out * 100]})
        fig = px.bar(data, x="Parameter", y="Moisture Content", text="Moisture Content", title="📊 Grafik Moisture Content")
        st.plotly_chart(fig)

# Tab 3: Laporan Hasil Pengeringan
with tab3:
    st.title("📢 Laporan Hasil Pengeringan")
    
    # Input tanggal dan shift
    tanggal = st.date_input("📅 Pilih Tanggal Laporan", datetime.now())
    shift = st.selectbox("🕒 Pilih Shift", ["Shift 1 - Pagi", "Shift 2 - Malam"])
    
    # Input data pengeringan
    start_time = st.time_input("⏰ Waktu Mulai", value=datetime.strptime("08:00", "%H:%M").time())
    end_time = st.time_input("⏰ Waktu Selesai", value=datetime.strptime("12:00", "%H:%M").time())
    density = st.number_input("🧪 Density Serbuk (kg/m³)", min_value=0.1, value=89.0, step=0.1)
    selected_tera = st.selectbox("📌 Pilih Hasil TERA", ["TERA 1", "TERA 2", "TERA 3", "TERA 4", "TERA 5"])
    
    one_hour_production = st.number_input(f"📊 Produksi per jam {selected_tera}", min_value=0, step=1)
    total_production = st.number_input("📌 Total Produksi Selama Operasional (kg)", min_value=0, step=1)
    total_hours = st.number_input("⏳ Total Jam Operasional", min_value=1, step=1)

    # Hitung durasi produksi dalam jam
    start_time_dt = datetime.combine(datetime.today(), start_time)
    end_time_dt = datetime.combine(datetime.today(), end_time)
    duration_hours = round((end_time_dt - start_time_dt).total_seconds() / 3600, 2)
    
    if st.button("📄 Generate Laporan"):
        avg_production_per_hour = total_production // total_hours if total_hours > 0 else 0
        formatted_date = tanggal.strftime('%A, %d %B %Y').capitalize()  # Format tanggal Indonesia
        
        st.markdown(
            f"""
            ### 📅 {formatted_date} ({shift})
            
            📌 **Hasil {selected_tera} (Pukul {start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')})**
            - Waktu kotak penuh : {fill_time} detik
            - Berat Kotak (Netto) : {weight_wet -4} Kg
            - 1 jam = {one_hour_production} kg 
            - Total Dryer selama {duration_hours} Jam : {one_hour_production * duration_hours:.2f} kg
            
            📌 **Total Hasil Pengeringan**
            - Pukul {start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')} ({total_hours} jam): {total_production} kg
            - Rata-rata produksi per jam: {avg_production_per_hour} kg
            
            📌 **Parameter Bahan**
            - Density Serbuk: {density} kg/m³
            - 💧 Moisture Content Input: {mc_in * 100:.2f} %
            - 💧 Moisture Content Output: {mc_out * 100:.2f} %
            """
        )
