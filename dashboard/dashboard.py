import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Set style untuk seaborn
sns.set_theme(style="whitegrid")

# Load data
data_path = os.path.join(os.path.dirname(__file__), 'all_data.csv')
all_df = pd.read_csv(data_path)
all_df['dteday_day'] = pd.to_datetime(all_df['dteday_day'])

st.sidebar.title("Filter Data")
date_range = st.sidebar.date_input(
    label="Pilih Rentang Waktu",
    value=[all_df['dteday_day'].min(), all_df['dteday_day'].max()],
    min_value=all_df['dteday_day'].min(),
    max_value=all_df['dteday_day'].max()
)

filtered_df = all_df[(all_df['dteday_day'] >= pd.Timestamp(date_range[0])) &
                     (all_df['dteday_day'] <= pd.Timestamp(date_range[1]))]

# Judul Dashboard
st.title("Dashboard Analisis Penggunaan Sepeda")
st.markdown("---")

# Plot 1: Pengguna Harian
st.header("Statistik Pengguna Sepeda")
col1, col2, col3 = st.columns(3)
with col1:
    total_users = filtered_df['cnt_day'].sum()
    st.metric("Total Pengguna", value=total_users)
with col2:
    casual_users = filtered_df['casual_day'].sum()
    st.metric("Pengguna Biasa", value=casual_users)
with col3:
    registered_users = filtered_df['registered_day'].sum()
    st.metric("Pengguna Terdaftar", value=registered_users)

st.markdown(
    "Statistik ini memberikan gambaran jumlah total pengguna sepeda (biasa dan terdaftar) berdasarkan rentang waktu yang dipilih."
)

# Plot 2: Hubungan Suhu dengan Pengguna Sepeda (Per Jam)
st.header("Hubungan Suhu dengan Pengguna Sepeda (Per Jam)")
fig, ax = plt.subplots(figsize=(10, 5))
sns.scatterplot(
    data=filtered_df,
    x='temp_hour',
    y='cnt_hour',
    hue='hum_hour',
    palette='coolwarm',
    ax=ax
)
ax.set_xlabel("Suhu (per-jam)")
ax.set_ylabel("Jumlah Pengguna (per-jam)")
st.pyplot(fig)
st.markdown(
    "Scatterplot ini menggambarkan bahwa suhu memiliki hubungan positif dengan jumlah pengguna sepeda. Semakin tinggi suhu, semakin banyak pengguna sepeda. Warna menambahkan dimensi kelembapan (humidity), yang juga memengaruhi kenyamanan pengguna."
)

# Plot 3: Perbandingan Pengguna Biasa vs Terdaftar
st.header("Pengguna Biasa vs Pengguna Terdaftar")
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(filtered_df['dteday_day'], filtered_df['casual_day'], label='Pengguna Biasa', color='#FFC107')
ax.bar(filtered_df['dteday_day'], filtered_df['registered_day'], bottom=filtered_df['casual_day'], label='Pengguna Terdaftar', color='#03A9F4')
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Pengguna")
ax.legend()
st.pyplot(fig)
st.markdown(
    "Bar chart ini memperlihatkan kontribusi masing-masing jenis pengguna. Pengguna terdaftar biasanya lebih dominan dibandingkan pengguna biasa, terutama pada hari kerja."
)

# Plot 4: Faktor yang Mempengaruhi Penggunaan Sepeda
st.subheader("Faktor yang Mempengaruhi Penggunaan Sepeda")
correlation = filtered_df[['temp_hour', 'hum_hour', 'windspeed_hour', 'cnt_hour']].corr()
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(correlation, annot=True, cmap="coolwarm", ax=ax)
ax.set_title("Korelasi Variabel terhadap Jumlah Penggunaan")
st.pyplot(fig)
st.markdown("Heatmap ini menunjukkan faktor yang memiliki hubungan paling kuat terhadap jumlah penggunaan sepeda.")

# Footer
st.markdown("---")
st.caption("Dibuat oleh Andi Muhammad Naufal - Proyek Dicoding 2025")
