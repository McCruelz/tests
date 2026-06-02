import streamlit as st
import random

# --- Pilihan Dropdown Form ---
GENDER_OPTIONS = ['male', 'female']
HOLIDAY_OPTIONS = ['No', 'Yes']
SEASON_OPTIONS = ['winter', 'monsoon', 'spring', 'summer']
GEO_OPTIONS = ['plains', 'mountains', 'coastal']

# --- Preferensi Model untuk Skenario Tombol Random ---
GOOD_BRANDS_PREF = ['Dabur Chyawanprash', 'Head & Shoulders', 'HRX', 'Urban Ladder', 'Kama Ayurveda']
BAD_BRANDS_PREF = ['The Moms Co.', 'Libram', 'Wild Stone', 'Vero Moda', 'Moov', 'Wakefit']

# --- Nilai Bawaan (Default) Awal ---
DEFAULT_VALUES = {
    'gender': 'male',
    'clicks': 10,
    'purchased': 2,
    'avg_rating': 3.5,
    'median_price': 1500,
    'holiday': 'No',
    'season': 'winter',
    'geo': 'plains',
    'price': 500,
    'product_rating': 4.0,
    'sentiment': 0.50
}

def init_session_state(daftar_brand):
    """Fungsi untuk menginisialisasi nilai awal widget jika belum ada di memori."""
    if 'k_gender' not in st.session_state:
        st.session_state.k_gender = DEFAULT_VALUES['gender']
        st.session_state.k_clicks = DEFAULT_VALUES['clicks']
        st.session_state.k_purchased = DEFAULT_VALUES['purchased']
        st.session_state.k_avg_rating = DEFAULT_VALUES['avg_rating']
        st.session_state.k_median_price = DEFAULT_VALUES['median_price']
        st.session_state.k_holiday = DEFAULT_VALUES['holiday']
        st.session_state.k_season = DEFAULT_VALUES['season']
        st.session_state.k_geo = DEFAULT_VALUES['geo']
        st.session_state.k_brand = daftar_brand[0] if daftar_brand else 'PUMA'
        st.session_state.k_price = DEFAULT_VALUES['price']
        st.session_state.k_product_rating = DEFAULT_VALUES['product_rating']
        st.session_state.k_sentiment = DEFAULT_VALUES['sentiment']

def set_random_recommended(daftar_brand):
    """Mengisi form dengan kombinasi nilai yang sangat disukai oleh model."""
    st.session_state.k_gender = random.choice(GENDER_OPTIONS)
    st.session_state.k_clicks = random.randint(0, 5) 
    st.session_state.k_purchased = random.randint(5, 15) 
    st.session_state.k_avg_rating = round(random.uniform(4.0, 5.0), 1) 
    mp = random.randint(500, 2000)
    st.session_state.k_median_price = mp
    st.session_state.k_holiday = random.choice(HOLIDAY_OPTIONS)
    st.session_state.k_season = random.choice(SEASON_OPTIONS)
    st.session_state.k_geo = random.choice(GEO_OPTIONS)
    
    good_brands = [b for b in GOOD_BRANDS_PREF if b in daftar_brand]
    st.session_state.k_brand = random.choice(good_brands) if good_brands else random.choice(daftar_brand)
    
    st.session_state.k_price = mp 
    st.session_state.k_product_rating = round(random.uniform(4.5, 5.0), 1) 
    st.session_state.k_sentiment = round(random.uniform(0.8, 1.0), 2) 

def set_random_not_recommended(daftar_brand):
    """Mengisi form dengan kombinasi nilai yang dibenci oleh model."""
    st.session_state.k_gender = random.choice(GENDER_OPTIONS)
    st.session_state.k_clicks = random.randint(30, 50) 
    st.session_state.k_purchased = 0 
    st.session_state.k_avg_rating = round(random.uniform(1.0, 2.5), 1) 
    st.session_state.k_median_price = random.randint(200, 500)
    st.session_state.k_holiday = random.choice(HOLIDAY_OPTIONS)
    st.session_state.k_season = random.choice(SEASON_OPTIONS)
    st.session_state.k_geo = random.choice(GEO_OPTIONS)
    
    bad_brands = [b for b in BAD_BRANDS_PREF if b in daftar_brand]
    st.session_state.k_brand = random.choice(bad_brands) if bad_brands else random.choice(daftar_brand)
    
    st.session_state.k_price = random.randint(3000, 5000) 
    st.session_state.k_product_rating = round(random.uniform(1.0, 2.5), 1) 
    st.session_state.k_sentiment = round(random.uniform(-1.0, -0.5), 2)

def set_random_all(daftar_brand):
    """Mengisi form dengan nilai yang benar-benar acak (pure random)."""
    st.session_state.k_gender = random.choice(GENDER_OPTIONS)
    st.session_state.k_clicks = random.randint(0, 50)
    st.session_state.k_purchased = random.randint(0, 20)
    st.session_state.k_avg_rating = round(random.uniform(0.0, 5.0), 1)
    st.session_state.k_median_price = random.randint(100, 5000)
    st.session_state.k_holiday = random.choice(HOLIDAY_OPTIONS)
    st.session_state.k_season = random.choice(SEASON_OPTIONS)
    st.session_state.k_geo = random.choice(GEO_OPTIONS)
    
    st.session_state.k_brand = random.choice(daftar_brand)
    st.session_state.k_price = random.randint(100, 5000)
    st.session_state.k_product_rating = round(random.uniform(0.0, 5.0), 1)
    st.session_state.k_sentiment = round(random.uniform(-1.0, 1.0), 2)