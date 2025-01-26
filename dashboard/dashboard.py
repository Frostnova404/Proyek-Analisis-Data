import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
data_path = os.path.join(os.path.dirname(__file__), 'all_data.csv')
all_df = pd.read_csv(data_path)
all_df['dteday_day'] = pd.to_datetime(all_df['dteday_day'])

date_range = st.sidebar.date_input(
    label="Pilih Rentang Waktu",
    value=[all_df['dteday_day'].min(), all_df['dteday_day'].max()],
    min_value=all_df['dteday_day'].min(),
    max_value=all_df['dteday_day'].max()
)
filtered_df = all_df[(all_df['dteday_day'] >= pd.Timestamp(date_range[0])) &
                     (all_df['dteday_day'] <= pd.Timestamp(date_range[1]))]

# Dashboard Title
st.title("Pengguna Sepeda")
st.markdown("---")

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

# Plot 1: Pengguna Harian
st.subheader("Pengguna Harian")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(filtered_df['dteday_day'], filtered_df['cnt_day'], marker='o', color='#90CAF9', label='Total Users')
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Pengguna Sepeda")
ax.legend()
st.pyplot(fig)

# Plot 2: Temperatur per-jam dan penggunanya
st.subheader("Temperatur per-jam dan Penggunanya")
fig, ax = plt.subplots(figsize=(10, 5))
sns.scatterplot(
    data=filtered_df,
    x='temp_hour',
    y='cnt_hour',
    hue='hum_hour',
    palette='coolwarm',
    ax=ax
)
ax.set_xlabel("Temperatur (per-jam)")
ax.set_ylabel("Pengguna (per-jam)")
st.pyplot(fig)

# Plot 3: Pengguna Biasa vs Pengguna Terdaftar
st.subheader("Pengguna Biasa vs Pengguna Terdaftar")
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(filtered_df['dteday_day'], filtered_df['casual_day'], label='Pengguna Biasa', color='#FFC107')
ax.bar(filtered_df['dteday_day'], filtered_df['registered_day'], bottom=filtered_df['casual_day'], label='Pengguna Terdaftar', color='#03A9F4')
ax.set_xlabel("Tanggal")
ax.set_ylabel("Pengguna")
ax.legend()
st.pyplot(fig)

# New Plot: Tren Berdasarkan Musim dan Hari Kerja
st.subheader("Tren Penggunaan Sepeda Berdasarkan Musim dan Hari Kerja")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    data=filtered_df,
    x='season_day',
    y='cnt_day',
    hue='workingday_day',
    palette='coolwarm',
    ax=ax
)
ax.set_xlabel("Musim")
ax.set_ylabel("Jumlah Pengguna")
ax.legend(title="Hari Kerja")
st.pyplot(fig)
st.markdown("Grafik ini menunjukkan bahwa hari kerja memiliki penggunaan sepeda lebih tinggi dibandingkan hari libur, dengan variasi berdasarkan musim.")

# New Plot: Faktor Utama yang Mempengaruhi Penggunaan Sepeda
st.subheader("Faktor Utama yang Mempengaruhi Penggunaan Sepeda")
correlation = filtered_df[['temp_hour', 'hum_hour', 'windspeed_hour', 'cnt_hour']].corr()
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(correlation, annot=True, cmap="coolwarm", ax=ax)
ax.set_title("Korelasi Variabel terhadap Jumlah Penggunaan")
st.pyplot(fig)
st.markdown("Heatmap ini menunjukkan bahwa suhu memiliki hubungan paling kuat terhadap jumlah penggunaan sepeda.")

# Footer
st.markdown("---")
st.caption("Dibuat oleh Andi Muhammad Naufal, Submisi file Dicoding Tugas Proyek 2025")
