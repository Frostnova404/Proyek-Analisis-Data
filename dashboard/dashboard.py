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

# Sidebar: Pilih Rentang Waktu
st.sidebar.title("Filter Data")
date_range = st.sidebar.date_input(
    label="Pilih Rentang Waktu",
    value=[all_df['dteday_day'].min(), all_df['dteday_day'].max()],
    min_value=all_df['dteday_day'].min(),
    max_value=all_df['dteday_day'].max()
)

# Filter data berdasarkan rentang waktu
filtered_df = all_df[(all_df['dteday_day'] >= pd.Timestamp(date_range[0])) &
                     (all_df['dteday_day'] <= pd.Timestamp(date_range[1]))]

# Judul Dashboard
st.title("Dashboard Analisis Penggunaan Sepeda")
st.markdown("---")

# **1. Insight Statistik Pengguna**
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

st.markdown("Statistik di atas menunjukkan jumlah total pengguna sepeda dalam rentang waktu yang dipilih.")

# **2. Penggunaan Sepeda Harian**
st.header("Penggunaan Sepeda Harian")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(filtered_df['dteday_day'], filtered_df['cnt_day'], marker='o', color='#90CAF9', label='Total Pengguna')
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Pengguna Sepeda")
ax.legend()
st.pyplot(fig)
st.markdown("Grafik ini menunjukkan tren jumlah pengguna sepeda setiap hari. Anda dapat melihat fluktuasi penggunaan berdasarkan hari kerja atau akhir pekan.")

# **3. Hubungan Suhu dan Pengguna Sepeda (Per Jam)**
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
st.markdown("Scatterplot ini menunjukkan bahwa suhu memiliki hubungan positif dengan jumlah pengguna sepeda, sementara kelembapan (dihubungkan dengan warna) memberikan pengaruh kecil terhadap pola.")

# **4. Perbandingan Pengguna Biasa vs Terdaftar**
st.header("Pengguna Biasa vs Pengguna Terdaftar")
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(filtered_df['dteday_day'], filtered_df['casual_day'], label='Pengguna Biasa', color='#FFC107')
ax.bar(filtered_df['dteday_day'], filtered_df['registered_day'], bottom=filtered_df['casual_day'], label='Pengguna Terdaftar', color='#03A9F4')
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Pengguna")
ax.legend()
st.pyplot(fig)
st.markdown("Bar chart ini menunjukkan perbandingan antara pengguna biasa dan pengguna terdaftar setiap hari. Pengguna terdaftar cenderung mendominasi, terutama pada hari kerja.")

# Footer
st.markdown("---")
st.caption("Dibuat oleh Andi Muhammad Naufal - Proyek Dicoding 2025")
