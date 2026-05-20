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

col_text, col_tips = st.columns([3, 2])
with col_text:
    st.write("Aplikasi ini memprediksi apakah sebuah produk layak direkomendasikan kepada pengguna berdasarkan data historis dan fitur produk, menggunakan **Support Vector Machine (SVM)**.")
with col_tips:
    with st.expander("💡 Tips Akurat Mendapatkan Rekomendasi"):
        st.markdown(
            "👤 Sentimen pelanggan harus mendekati 1.0 untuk mendapat hasil yang direkomendasikan.\n"
            "⭐ Rating tinggi & banyak dibeli akan sangat direkomendasikan.\n"
            "🏷️ Brand yang dipilih sangat berpengaruh.\n"
            "📲 Jumlah klik yang banyak namun tanpa pembelian akan berdampak negatif terhadap hasil prediksi."
        )

# --- Kelompok Input Data ---
st.markdown("### 🚹 Informasi Pengguna & Lingkungan")
st.markdown("Masukkan informasi mengenai target pengguna dan kondisi lingkungan sekitar saat ini.")
col_usr1, col_usr2, col_usr3, col_usr4 = st.columns(4)
with col_usr1:
    gender = st.selectbox("Jenis Kelamin", GENDER_OPTIONS, key='k_gender')
with col_usr2:
    geo = st.selectbox("Lokasi Geografis", GEO_OPTIONS, key='k_geo')
with col_usr3:
    season = st.selectbox("Musim", SEASON_OPTIONS, key='k_season')
with col_usr4:
    holiday = st.selectbox("Hari Libur?", HOLIDAY_OPTIONS, key='k_holiday')

st.markdown("### 🛒 Histori Pembelian & Produk Serupa")
st.markdown("Masukkan informasi mengenai histori pembelian produk serupa oleh user.")
col_hist1, col_hist2, col_hist3, col_hist4 = st.columns(4)
with col_hist1:
    clicks = st.number_input("Klik (Produk Serupa)", min_value=0, step=1, key='k_clicks')
with col_hist2:
    purchased = st.number_input("Beli (Produk Serupa)", min_value=0, step=1, key='k_purchased')
with col_hist3:
    avg_rating = st.slider("Rata-rata Rating Serupa", min_value=0.0, max_value=5.0, step=0.1, key='k_avg_rating')
with col_hist4:
    median_price = st.number_input("Rata-rata Harga Beli oleh user", min_value=100, step=100, key='k_median_price')

st.markdown("### 📦 Informasi Produk (Target)")
st.markdown("Masukkan informasi mengenai target produk yang akan direkomendasikan.")
col_prod1, col_prod2, col_prod3, col_prod4 = st.columns(4)
with col_prod1:
    brand = st.selectbox("Brand Produk", daftar_brand, key='k_brand')
with col_prod2:
    price = st.number_input("Harga Produk", min_value=90, step=50, key='k_price')
with col_prod3:
    product_rating = st.slider("Rating Produk", min_value=0.0, max_value=5.0, step=0.1, key='k_product_rating')
with col_prod4:
    sentiment = st.slider("Sentimen Ulasan", min_value=-1.0, max_value=1.0, step=0.05, key='k_sentiment')

# --- Tombol Aksi ---
st.write("---")
b1, b2, b3, b4 = st.columns(4)
with b1: st.button("✨ Auto-Isi: Pasti Lolos", on_click=set_random_recommended, args=(daftar_brand,), use_container_width=True)
with b2: st.button("🚫 Auto-Isi: Pasti Ditolak", on_click=set_random_not_recommended, args=(daftar_brand,), use_container_width=True)
with b3: st.button("🎲 Auto-Isi: Acak Total", on_click=set_random_all, args=(daftar_brand,), use_container_width=True)
with b4: cek_btn = st.button("🔍 Cek Rekomendasi Sekarang", type="primary", use_container_width=True)

if cek_btn:
    
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