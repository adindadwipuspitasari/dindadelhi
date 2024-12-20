import streamlit as st
import pandas as pd
import numpy as np

# Judul aplikasi
st.title('Klasifikasi Hotel')

# Deskripsi aplikasi
st.write("""
    mengklasifikasikan hotel berdasarkan ulasan menjadi 'Very Good' atau 'Excellent'.
""")

# Fungsi untuk klasifikasi
def classify_hotel(rating):
    if rating >= 4.3:
        return "Excellent"
    else:
        return "Very Good"

# Path ke file dataset bawaan
file_path = 'delhi.xlsx'

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

    # Filter data hanya untuk 'Very Good' dan 'Excellent'
    df = df[df['Rating Description'].isin(['Excellent', 'Very Good'])]

    # Membagi layout ke dua kolom
    col1, col2 = st.columns(2)

    # Menampilkan 15 hotel dengan rating Excellent di kolom kiri
    with col1:
        st.subheader("15 Hotel dengan Rating Excellent")
        hotel_excellent = df[df['Rating Description'] == "Excellent"].head(15)[['Hotel Name', 'Rating', 'Rating Description']]
        hotel_excellent = hotel_excellent.reset_index(drop=True)  # Reset index, drop kolom index lama
        hotel_excellent.index = hotel_excellent.index + 1  # Set index mulai dari 1
        st.dataframe(hotel_excellent)

    # Menampilkan 15 hotel dengan rating Very Good di kolom kanan
    with col2:
        st.subheader("15 Hotel dengan Rating Very Good")
        hotel_very_good = df[df['Rating Description'] == "Very Good"].head(15)[['Hotel Name', 'Rating', 'Rating Description']]
        hotel_very_good = hotel_very_good.reset_index(drop=True)  # Reset index, drop kolom index lama
        hotel_very_good.index = hotel_very_good.index + 1  # Set index mulai dari 1
        st.dataframe(hotel_very_good)

    # Inisialisasi DataFrame untuk data baru
    if "data_baru" not in st.session_state:
        st.session_state.data_baru = pd.DataFrame(columns=["Hotel Name", "Rating", "Rating Description"])

    # Form untuk input data baru
    with st.form("input_form"):
        title = st.text_input("Masukkan Nama Hotel:")
        rating = st.number_input("Masukkan Rating :", min_value=3.0, max_value=5.0, step=0.1)
        submitted = st.form_submit_button("Tambahkan")

        if submitted:
            if title.strip() and 0.0 <= rating <= 5.0:
                htl = classify_hotel(rating)

                new_data = pd.DataFrame({"Hotel Name": [title], "Rating": [rating], "Rating Description": [htl]})
                st.session_state.data_baru = pd.concat([st.session_state.data_baru, new_data], ignore_index=True)
                st.success(f"Hotel '{title}' berhasil ditambahkan!")
            else:
                st.error("Nama hotel tidak boleh kosong dan rating harus berada dalam rentang 1-5.")

    # Reset index dan mulai dari 1 untuk data baru
    st.session_state.data_baru = st.session_state.data_baru.reset_index(drop=True)
    st.session_state.data_baru.index = st.session_state.data_baru.index + 1

    # Tampilkan data baru yang telah ditambahkan
    st.write("Data Baru yang Ditambahkan:")
    st.write(st.session_state.data_baru)

    # Gabungkan data lama dan data baru untuk diunduh
    gabungan_data = pd.concat([df[['Hotel Name', 'Rating', 'Rating Description']], st.session_state.data_baru], ignore_index=True)

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
