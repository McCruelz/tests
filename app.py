from streamlit_extras.let_it_rain import rain
import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Sistem Rekomendasi Produk", page_icon="🛍️", layout="wide")

@st.cache_resource
def load_models():
    model = joblib.load('model_svm_rekomendasi.pkl')
    prep = joblib.load('preprocessor_data.pkl')
    return model, prep

svm_model, preprocessor = load_models()

st.title("🛍️ Sistem Prediksi Rekomendasi Produk")
st.write("""
Aplikasi ini memprediksi apakah sebuah produk layak direkomendasikan kepada pengguna 
berdasarkan data historis dan fitur produk, menggunakan **Support Vector Machine (SVM)**.
""")
st.markdown("---")

st.header("📝 Info Data Pengguna dan Spesifikasi Produk")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Data Interaksi Pengguna")
    gender = st.selectbox("Jenis Kelamin (Gender)", ['male', 'female'])
    clicks = st.number_input("Jumlah klik pada produk serupa", min_value=0, value=10, step=1)
    purchased = st.number_input("Jumlah produk serupa yang sudah dibeli", min_value=0, value=2, step=1)
    avg_rating = st.slider("Rata-rata rating produk serupa", min_value=0.0, max_value=5.0, value=3.5, step=0.1)
    median_price = st.number_input("Median harga pembelian sebelumnya (dalam Rupee)", min_value=100, value=1500, step=100)
    
    st.subheader("Konteks Waktu & Lokasi")
    holiday = st.selectbox("Apakah sedang hari libur? (Holiday)", ['No', 'Yes'])
    season = st.selectbox("Musim saat ini (Season)", ['winter', 'monsoon', 'spring', 'summer'])
    geo = st.selectbox("Lokasi Geografis", ['plains', 'mountains', 'coastal'])

with col2:
    st.subheader("Detail Produk Saat Ini")
    daftar_brand = ['PUMA', 'Lee', 'Head Hunters', 'Johnson & Johnson', 'Wakefit', 'Dabur Chyawanprash', 
                    'Manyavar Mohey', 'Pepperfry', 'Lee Cooper', 'Libram', 'Flying Machine', 'SleepyCat', 
                    'Streax', 'Lakme Ayurveda', 'Forest Essentials', 'Dove Hair', 'Pepe Jeans London', 
                    'The Moms Co.', 'Himalaya Liv.52', 'Wildcraft', 'Godrej Interio', 'Patanjali Ayurved (Health Care)', 
                    'Lijoba', 'Moov', 'Kama Ayurveda', 'Urban Ladder', 'Allen Solly Woman', 'Max', 'Head & Shoulders', 
                    'Fastrack', 'Sugar Cosmetics', 'Parachute', 'Dettol', 'AmazonBasics', 'U.S. Polo Assn. Women', 
                    'Khadi Essentials', 'Whisper', 'Levis Strauss & Co.', 'Wild Stone', 'Biovea', 'Vero Moda', 
                    'Zandu', 'HRX', 'Mothercare', 'Duroflex', 'Spyker', 'Stayfree', 'Baidyanath']
    
    brand = st.selectbox("Pilih Brand Produk", sorted(daftar_brand))
    price = st.number_input("Harga Produk (dalam Rupee)", min_value=90, value=500, step=50)
    product_rating = st.slider("Rating Produk Ini", min_value=0.0, max_value=5.0, value=4.0, step=0.1)
    sentiment = st.slider("Skor Sentimen Ulasan (-1.0 s/d 1.0)", min_value=-1.0, max_value=1.0, value=0.5, step=0.05)

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