import pandas as pd
import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

@st.cache_data
def load_dataset(dataset_path='content_based_recommendation_dataset.csv'):
    try:
        return pd.read_csv(dataset_path)
    except Exception:
        return pd.DataFrame()

def get_similar_products(brand, price, product_rating, sentiment, top_n=3):
    # Menghitung kemiripan produk yang diinput dengan produk yang ada di dalam dataset 
    # menggunakan metode Content-Based Filtering (Cosine Similarity).
    df_all = load_dataset()
    if df_all.empty:
        return pd.DataFrame()
        
    product_features = [
        'Brand of the product', 
        'Price of the product', 
        'Rating of the product', 
        'Customer review sentiment score (overall)'
    ]
    
    # Validasi jika kolom yang dibutuhkan ada pada dataset
    for col in product_features:
        if col not in df_all.columns:
            return pd.DataFrame()

    df_products = df_all[product_features].copy()
    
    # Bentuk vektor dari input pengguna
    input_product = pd.DataFrame({
        'Brand of the product': [brand],
        'Price of the product': [price],
        'Rating of the product': [product_rating],
        'Customer review sentiment score (overall)': [sentiment]
    })
    
    # Gabungkan dengan dataset untuk proses OneHotEncoding agar encoder mengenali semua kategori
    df_combined = pd.concat([input_product, df_products], ignore_index=True)
    
    # Siapkan preprocessor khusus untuk fitur produk
    prod_preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), ['Price of the product', 'Rating of the product', 'Customer review sentiment score (overall)']),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), ['Brand of the product'])
        ])
    
    # Transformasi matriks
    produk_matrix = prod_preprocessor.fit_transform(df_combined)
    
    # Pisahkan kembali input vector dan target vectors
    input_vector = produk_matrix[0:1]
    dataset_vectors = produk_matrix[1:]
    
    # Hitung Cosine Similarity
    similarity_scores = cosine_similarity(input_vector, dataset_vectors)[0]
    
    # Tambahkan skor kemiripan ke dalam dataframe asli untuk pengurutan
    df_all_with_sim = df_all.copy()
    df_all_with_sim['similarity'] = similarity_scores
    
    # Hapus duplikat fitur produk dan urutkan berdasarkan kemiripan tertinggi
    df_unique_products = df_all_with_sim.drop_duplicates(subset=product_features).sort_values(by='similarity', ascending=False)
    
    # Kembalikan top N produk yang paling mirip
    top_similar = df_unique_products.head(top_n)
    return top_similar
