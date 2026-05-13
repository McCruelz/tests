import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.svm import SVC
import joblib

print("Membaca dataset...")
df = pd.read_csv("content_based_recommendation_dataset.csv")

# Bikin target >= 0.7 sesuai yang bikin akurasi jadi 98.31%
df['Is_Recommended'] = (df['Probability for the product to be recommended to the person'] >= 0.7).astype(int)

X = df.drop(columns=['Probability for the product to be recommended to the person', 'Is_Recommended'])
y = df['Is_Recommended']

categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
numerical_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()

print("Memproses data...")
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_cols)
    ])

X_processed = preprocessor.fit_transform(X)

print("Melatih model SVM...")
# Kita latih menggunakan seluruh data agar model lebih pintar saat di-deploy
svm_model = SVC(kernel='linear', random_state=42)
svm_model.fit(X_processed, y)

print("Menyimpan model ke versi terbaru...")
joblib.dump(svm_model, 'model_svm_rekomendasi.pkl')
joblib.dump(preprocessor, 'preprocessor_data.pkl')

print("✅ BERHASIL! File .pkl sudah diperbarui.")