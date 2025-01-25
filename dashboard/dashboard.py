import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns


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


st.title("Pengguna sepeda")
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
    st.metric("Pengguna harian", value=registered_users)

# Plot 1: Pengguna Harian
st.subheader("Pengguna Harian")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(filtered_df['dteday_day'], filtered_df['cnt_day'], marker='o', color='#90CAF9', label='Total Users')
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah pengguna sepeda")
ax.legend()
st.pyplot(fig)

# Plot 2: Temperatur per-jam dan penggunanya
st.subheader("Temperatur per-jam dan penggunanya")
fig, ax = plt.subplots(figsize=(10, 5))
sns.scatterplot(
    data=filtered_df,
    x='temp_hour',
    y='cnt_hour',
    hue='hum_hour',
    palette='coolwarm',
    ax=ax
)
ax.set_xlabel("Temperature (per-jam)")
ax.set_ylabel("Pengguna (per-jam)")
st.pyplot(fig)

# Plot 3: Daily Casual vs Registered Users
st.subheader("Pengguna Biasa vs Pengguna Harian")
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(filtered_df['dteday_day'], filtered_df['casual_day'], label='Casual Users', color='#FFC107')
ax.bar(filtered_df['dteday_day'], filtered_df['registered_day'], bottom=filtered_df['casual_day'], label='Registered Users', color='#03A9F4')
ax.set_xlabel("Tanggal")
ax.set_ylabel("Pengguna")
ax.legend()
st.pyplot(fig)

st.markdown("---")
st.caption("Dibuat oleh Andi Muhammad Naufal, Submisi file dicoding tugas proyek 2025")
