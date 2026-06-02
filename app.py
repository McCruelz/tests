from streamlit_extras.let_it_rain import rain
import streamlit as st
import pandas as pd
import joblib

from input_data import (
    GENDER_OPTIONS, HOLIDAY_OPTIONS, SEASON_OPTIONS, GEO_OPTIONS,
    init_session_state, set_random_recommended, set_random_not_recommended, set_random_all
)
from recommendation_utils import get_similar_products

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

init_session_state(daftar_brand)

st.title("🛍️ Sistem Prediksi Rekomendasi Produk")

col_text, col_tips = st.columns([3, 2])
with col_text:
    st.write("Aplikasi ini memprediksi apakah sebuah produk layak direkomendasikan kepada pengguna berdasarkan data historis dan fitur produk, menggunakan **Support Vector Machine (SVM)**.")
with col_tips:
    with st.expander("💡 Tips Akurat Mendapatkan Rekomendasi"):
        st.markdown("""
                    👤 Sentimen pelanggan mendekati 1.0 akan mendapat hasil yang direkomendasikan.  
                    ⭐ Rating tinggi & banyak dibeli akan direkomendasikan.  
                    🏷️ Brand yang dipilih sangat berpengaruh.  
                    📲 Jumlah klik banyak tanpa pembelian berdampak negatif terhadap hasil prediksi.
                    """)

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

st.write("---")
cek_btn = st.button("🔍 Cek Rekomendasi Sekarang", type="primary", use_container_width=True)

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
            
        with st.spinner("Mencari produk yang mirip..."):
            top_similar = get_similar_products(brand, price, product_rating, sentiment, top_n=3)
            
            if not top_similar.empty:
                st.markdown("### 📦 3 Produk Serupa")
                # st.markdown("")
                cols = st.columns(len(top_similar))
                for idx, (_, row) in enumerate(top_similar.iterrows()):
                    with cols[idx]:
                        st.info(f"**{row['Brand of the product']}**")
                        st.write(f"💵 Harga: Rp {row['Price of the product']}")
                        st.write(f"⭐ Rating: {row['Rating of the product']} / 5.0")
                        st.write(f"💬 Sentimen: {row['Customer review sentiment score (overall)']}")
                        st.caption(f"Tingkat Kemiripan: {row['similarity']*100:.1f}%")
            else:
                st.write("Tidak ada produk serupa yang ditemukan.")
            
    except Exception as e:
        st.warning("Terjadi kesalahan pada pemrosesan data.")
        st.error(f"Detail error: {e}")