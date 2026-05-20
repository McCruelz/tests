from streamlit_extras.let_it_rain import rain
import streamlit as st
import pandas as pd
import joblib

# Import konfigurasi dan state manager agar app.py bersih
from input_data import (
    GENDER_OPTIONS, HOLIDAY_OPTIONS, SEASON_OPTIONS, GEO_OPTIONS,
    init_session_state, set_random_recommended, set_random_not_recommended, set_random_all
)

st.set_page_config(page_title="Sistem Rekomendasi Produk", page_icon="🛍️", layout="wide")

@st.cache_resource
def load_models():
    model = joblib.load('model_svm_rekomendasi.pkl')
    prep = joblib.load('preprocessor_data.pkl')
    return model, prep

@st.cache_data
def load_brands():
    try:
        df = pd.read_csv('content_based_recommendation_dataset.csv')
        brands = df['Brand of the product'].dropna().unique().tolist()
        return sorted(brands)
    except Exception:
        # Fallback if file is missing
        return ['PUMA']

svm_model, preprocessor = load_models()
daftar_brand = load_brands()

# --- Menginisialisasi Session State (Dipanggil dari file terpisah) ---
init_session_state(daftar_brand)

st.title("🛍️ Sistem Prediksi Rekomendasi Produk")
st.write("""
Aplikasi ini memprediksi apakah sebuah produk layak direkomendasikan kepada pengguna 
berdasarkan data historis dan fitur produk, menggunakan **Support Vector Machine (SVM)**.
""")

with st.expander("💡 Tips Akurat Mendapatkan Rekomendasi (Berdasarkan Analisis Model)"):
    st.write("""
    Berdasarkan analisis bobot pada model **Machine Learning (SVM)** yang digunakan, berikut adalah faktor penentu utama agar produk direkomendasikan:
    
    *   **Skor Sentimen Ulasan (Paling Penting!)**: Sentimen ulasan yang positif (mendekati 1.0) adalah **faktor nomor satu** yang paling meningkatkan peluang produk direkomendasikan.
    *   **Rating Produk & Histori Pembelian**: Rating produk yang tinggi (mendekati 5.0) dan jumlah produk serupa yang **sudah dibeli** memiliki pengaruh positif yang sangat besar.
    *   **Pilihan Brand Berpengaruh**: Model memiliki preferensi tinggi terhadap brand tertentu seperti *Dabur Chyawanprash, Head & Shoulders, HRX*, dan *Urban Ladder*.
    *   **Jumlah Klik vs Pembelian**: Menariknya, sekadar memiliki *jumlah klik* yang tinggi tanpa diiringi pembelian justru memiliki pengaruh *negatif* (menurunkan kecocokan) terhadap rekomendasi sistem.
    """)

st.markdown("---")

st.header("📝 Info Data Pengguna dan Spesifikasi Produk")

# --- Tombol Randomize ---
st.write("Coba skenario pengujian cepat dengan nilai acak:")
btn_col1, btn_col2, btn_col3 = st.columns(3)
with btn_col1:
    st.button("✨ Auto-Isi: Pasti Lolos", on_click=set_random_recommended, args=(daftar_brand,), use_container_width=True, help="Mengisi form dengan kombinasi yang disukai model.")
with btn_col2:
    st.button("🚫 Auto-Isi: Pasti Ditolak", on_click=set_random_not_recommended, args=(daftar_brand,), use_container_width=True, help="Mengisi form dengan kombinasi yang tidak disukai model.")
with btn_col3:
    st.button("🎲 Auto-Isi: Acak Total", on_click=set_random_all, args=(daftar_brand,), use_container_width=True, help="Mengisi seluruh form dengan nilai acak sepenuhnya.")
    
st.markdown("<br>", unsafe_allow_html=True)

# --- Input Forms ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Data Interaksi Pengguna")
    gender = st.selectbox("Jenis Kelamin (Gender)", GENDER_OPTIONS, key='k_gender')
    clicks = st.number_input("Jumlah klik pada produk serupa", min_value=0, step=1, key='k_clicks')
    purchased = st.number_input("Jumlah produk serupa yang sudah dibeli", min_value=0, step=1, key='k_purchased')
    avg_rating = st.slider("Rata-rata rating produk serupa", min_value=0.0, max_value=5.0, step=0.1, key='k_avg_rating')
    median_price = st.number_input("Median harga pembelian sebelumnya (dalam Rupee)", min_value=100, step=100, key='k_median_price')
    
    st.subheader("Konteks Waktu & Lokasi")
    holiday = st.selectbox("Apakah sedang hari libur? (Holiday)", HOLIDAY_OPTIONS, key='k_holiday')
    season = st.selectbox("Musim saat ini (Season)", SEASON_OPTIONS, key='k_season')
    geo = st.selectbox("Lokasi Geografis", GEO_OPTIONS, key='k_geo')

with col2:
    st.subheader("Detail Produk Saat Ini")
    brand = st.selectbox("Pilih Brand Produk", daftar_brand, key='k_brand')
    price = st.number_input("Harga Produk (dalam Rupee)", min_value=90, step=50, key='k_price')
    product_rating = st.slider("Rating Produk Ini", min_value=0.0, max_value=5.0, step=0.1, key='k_product_rating')
    sentiment = st.slider("Skor Sentimen Ulasan (-1.0 s/d 1.0)", min_value=-1.0, max_value=1.0, step=0.05, key='k_sentiment')

st.markdown("---")

st.write("### 🔍 Hasil Analisis Sistem")
if st.button("Cek Rekomendasi Sekarang", type="primary"):
    
    input_pengguna = pd.DataFrame({
        'Number of clicks on similar products': [clicks],
        'Number of similar products purchased so far': [purchased],
        'Average rating given to similar products': [avg_rating],
        'Gender': [gender],
        'Median purchasing price (in rupees)': [median_price],
        'Rating of the product': [product_rating],
        'Brand of the product': [brand],
        'Customer review sentiment score (overall)': [sentiment],
        'Price of the product': [price],
        'Holiday': [holiday],
        'Season': [season],
        'Geographical locations': [geo]
    })
    
    try:
        input_diproses = preprocessor.transform(input_pengguna)
        
        hasil_prediksi = svm_model.predict(input_diproses)
        
        if hasil_prediksi[0] == 1:
            st.success("✅ **PROSPEK BAGUS:** Produk ini dinilai **LAYAK DIREKOMENDASIKAN** kepada pengguna tersebut.")
            st.balloons() 
        else:
            st.error("❌ **KURANG COCOK:** Produk ini **TIDAK DIREKOMENDASIKAN** kepada pengguna tersebut.")
            rain(
                emoji="❌",
                font_size=54,
                falling_speed=10,
                animation_length=1,
            )
            
    except Exception as e:
        st.warning("Terjadi kesalahan pada pemrosesan data.")
        st.error(f"Detail error: {e}")