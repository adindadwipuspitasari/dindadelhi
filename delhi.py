import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import matplotlib.pyplot as plt
import streamlit as st

# 1. Membaca Data dari Excel
file_path = 'delhi.xlsx'

# Membaca data dari sheet pertama
df = pd.read_excel(file_path)

# 2. Data Cleaning
# Bersihkan kolom 'Distance to Landmark'
def clean_distance(value):
    if isinstance(value, str):  # Jika value adalah string
        value = value.strip()  # Hapus spasi di awal/akhir
        if 'km' in value:
            return float(value.replace('km', '').strip())  # Ubah '8.0 km' menjadi 8.0
        elif 'm' in value:
            return float(value.replace('m', '').strip()) / 1000  # Ubah '500 m' menjadi 0.5
    elif isinstance(value, (int, float)):  # Jika value sudah numerik
        return value
    return np.nan  # Jika format tidak dikenal, anggap sebagai NaN

df['Distance to Landmark'] = df['Distance to Landmark'].apply(clean_distance)

# Periksa missing values dan isi dengan median jika ada
df['Distance to Landmark'].fillna(df['Distance to Landmark'].median(), inplace=True)

# Filter data hanya untuk 'Very Good' dan 'Excellent'
df = df[df['Rating Description'].isin(['Very Good', 'Excellent'])]

# 3. Fitur dan Target
# Tentukan fitur (X) dan target (y)
X = df[['Rating', 'Reviews', 'Star Rating', 'Distance to Landmark', 'Price']]
y = df['Rating Description']

# 4. Split Data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 5. Random Forest Classifier
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# 6. Melatih model
rf_model.fit(X_train, y_train)

# 7. Evaluasi model
y_pred = rf_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# Streamlit display
st.title('Hotel Rating Prediction')
st.write(f'Test accuracy: {accuracy * 100:.2f}%')

# 8. Classification Report
st.subheader('Classification Report:')
st.text(classification_report(y_test, y_pred))

# 9. Feature Importance (Visualisasi)
importance = rf_model.feature_importances_
features = X.columns

fig, ax = plt.subplots(figsize=(8, 6))
ax.barh(features, importance, color='skyblue')
ax.set_xlabel('Feature Importance')
ax.set_ylabel('Features')
ax.set_title('Feature Importance in Random Forest')
st.pyplot(fig)

# 10. Confusion Matrix (Visualisasi)
from sklearn.metrics import confusion_matrix
import seaborn as sns

conf_matrix = confusion_matrix(y_test, y_pred)

# Plot confusion matrix
fig2, ax2 = plt.subplots(figsize=(6, 5))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=['Very Good', 'Excellent'], yticklabels=['Very Good', 'Excellent'])
ax2.set_xlabel('Predicted')
ax2.set_ylabel('True')
ax2.set_title('Confusion Matrix')
st.pyplot(fig2)
