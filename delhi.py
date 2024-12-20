import streamlit as st
import pandas as pd
import numpy as np

# Judul aplikasi
st.title('Klasifikasi Popularitas Hotel')

# Deskripsi aplikasi
st.write("""
    Aplikasi ini mengklasifikasikan popularitas hotel berdasarkan ulasan 'Excellent' atau 'Very Good'.
""")

# Fungsi untuk klasifikasi
def classify_popularity(rating):
    if rating >= 4.3:
        return "Excellent"
    else:
        return "Very Good"

# Path ke file dataset
file_path = 'delhi.xlsx'  # Sesuaikan dengan lokasi file Anda

try:
    # Membaca data dari dataset
    df = pd.read_excel(file_path)

    # Bersihkan kolom 'Distance to Landmark' jika ada
    def clean_distance(value):
        if isinstance(value, str):  # Jika value adalah string
            value = value.strip()
            if 'km' in value:
                return float(value.replace('km', '').strip())
            elif 'm' in value:
                return float(value.replace('m', '').strip()) / 1000
        elif isinstance(value, (int, float)):  # Jika value sudah numerik
            return value
        return np.nan

    if 'Distance to Landmark' in df.columns:
        df['Distance to Landmark'] = df['Distance to Landmark'].apply(clean_distance)
        df['Distance to Landmark'].fillna(df['Distance to Landmark'].median(), inplace=True)

    # Tambahkan kolom 'Rating Description' berdasarkan rating
    if 'Rating' in df.columns:
        df['Rating Description'] = df['Rating'].apply(classify_popularity)

    # Membagi layout ke dua kolom
    col1, col2 = st.columns(2)

    # Menampilkan 10 hotel dengan rating 'Very Good'
    with col1:
        st.subheader("10 Hotel 'Very Good'")
        very_good = df[df['Rating Description'] == "Very Good"].head(10)[['Hotel Name', 'Rating', 'Rating Description']]
        very_good = very_good.reset_index(drop=True)
        very_good.index = very_good.index + 1
        st.dataframe(very_good)

    # Menampilkan 10 hotel dengan rating 'Excellent'
    with col2:
        st.subheader("10 Hotel 'Excellent'")
        excellent = df[df['Rating Description'] == "Excellent"].head(10)[['Hotel Name', 'Rating', 'Rating Description']]
        excellent = excellent.reset_index(drop=True)
        excellent.index = excellent.index + 1
        st.dataframe(excellent)

    # Gabungkan data lama untuk diunduh
    gabungan_data = df[['Hotel Name', 'Rating', 'Rating Description']].reset_index(drop=True)

    # Reset index mulai dari 1
    gabungan_data.index = gabungan_data.index + 1

    # Tombol download data gabungan
    csv = gabungan_data.to_csv(index=False)
    st.download_button(
        label="Download Data Gabungan",
        data=csv,
        file_name='hotel_popularity_combined.csv',
        mime='text/csv'
    )

except Exception as e:
    st.error(f"Terjadi kesalahan saat membaca file: {e}")
