# Sistem Prediksi Rekomendasi Produk 🛍️

Aplikasi web interaktif berbasis **Streamlit** dan **Machine Learning (SVM)** untuk memprediksi apakah sebuah produk layak direkomendasikan kepada pengguna tertentu. Prediksi didasarkan pada data historis interaksi pengguna, spesifikasi produk, serta konteks waktu dan lokasi.

## 🌟 Fitur Utama
- **Prediksi Akurat**: Menggunakan algoritma **Support Vector Machine (SVM)** dengan kernel linear yang telah dilatih dengan dataset rekomendasi berbasis konten.
- **Antarmuka Interaktif**: Antarmuka pengguna yang bersih dan mudah digunakan dibangun dengan Streamlit, terbagi menjadi input data pengguna dan detail produk.
- **Pemrosesan Data Otomatis**: Secara otomatis menangani penskalaan data numerik (StandardScaler) dan encoding data kategorikal (OneHotEncoder) menggunakan preprocessor yang sudah disimpan.
- **Efek Visual**: Menampilkan animasi (balon atau hujan) untuk membuat pengalaman pengguna lebih menarik berdasarkan hasil prediksi.

## 🛠️ Teknologi yang Digunakan
- **Python 3.x**
- **Streamlit**: Untuk membangun antarmuka web.
- **Scikit-Learn**: Untuk melatih model Machine Learning (SVM) dan preprocessing data.
- **Pandas**: Untuk manipulasi dan analisis data.
- **Joblib**: Untuk menyimpan dan memuat model yang telah dilatih.

## 📁 Struktur Direktori
```
d:\tests\
├── app.py                                      # Skrip utama aplikasi web Streamlit
├── train.py                                    # Skrip untuk melatih model SVM dan menyimpan preprocessor
├── content_based_recommendation_dataset.csv    # Dataset yang digunakan untuk pelatihan model
├── model_svm_rekomendasi.pkl                   # Model SVM yang sudah dilatih (disimpan oleh train.py)
└── preprocessor_data.pkl                       # Preprocessor pipeline (disimpan oleh train.py)
```

## 🚀 Cara Menjalankan Aplikasi

### 1. Persiapan Lingkungan (Virtual Environment)
Sangat disarankan untuk menggunakan virtual environment.
```bash
python -m venv .venv
# Aktifkan virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate
```

### 2. Instalasi Dependensi
Pastikan Anda menginstal semua library yang dibutuhkan:
```bash
pip install streamlit streamlit-extras pandas scikit-learn joblib
```

### 3. Melatih Model (Opsional jika `.pkl` sudah tersedia)
Jika Anda ingin melatih ulang model dengan data baru, jalankan:
```bash
python train.py
```
*Ini akan memperbarui file `model_svm_rekomendasi.pkl` dan `preprocessor_data.pkl`.*

### 4. Menjalankan Aplikasi Web
Jalankan aplikasi Streamlit dengan perintah berikut:
```bash
streamlit run app.py
```
Aplikasi akan otomatis terbuka di browser default Anda, biasanya pada `http://localhost:8501/`.

## 📝 Cara Penggunaan
1. Buka aplikasi di browser Anda.
2. Isi formulir **Data Interaksi Pengguna** (Jenis Kelamin, Jumlah klik, dll).
3. Isi formulir **Konteks Waktu & Lokasi** (Libur, Musim, dll).
4. Isi formulir **Detail Produk Saat Ini** (Pilih Brand, Harga, Rating, dll).
5. Klik tombol **Cek Rekomendasi Sekarang**.
6. Sistem akan memproses data Anda dan menampilkan hasil analisis (Direkomendasikan / Tidak Direkomendasikan).

---
*Dibuat menggunakan Python & Streamlit.*
