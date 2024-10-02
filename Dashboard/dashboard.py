import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MaxNLocator
import numpy as np
sns.set(style='dark')

# Load dataset
@st.cache_data
def load_hour_data():
    return pd.read_csv("Dashboard/hour.csv")

hour_dataset = load_hour_data()  # Pemanggilan langsung tanpa `st.cache_resource`

@st.cache_data
def load_day_data():
    return pd.read_csv("Dashboard/day.csv")

day_dataset = load_day_data()  # Pemanggilan langsung tanpa `st.cache_resource`

# Mengambil tanggal awal dan akhir dari dataset
hour_dataset['date'] = pd.to_datetime(hour_dataset['date'])
min_date = hour_dataset['date'].min()
max_date = hour_dataset['date'].max()

# Sidebar untuk filter rentang waktu
with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    start_date, end_date = st.date_input(
        label='Rentang Waktu', 
        min_value=min_date, 
        max_value=max_date, 
        value=[min_date, max_date]
    )

# Filter dataset berdasarkan rentang waktu yang dipilih
filtered_dataset = hour_dataset[(hour_dataset['date'] >= pd.to_datetime(start_date)) & 
                                (hour_dataset['date'] <= pd.to_datetime(end_date))]

# Title dan Author Information
st.header("Bike Share Dashboard")
st.write("""
    **Author Information**
    - Name       : Muhammad Nauval Almas
    - Email      : nauvalalmas@gmail.com 
    - Dicoding ID: valalmas   
""")
st.write('*October 1st, 2024*')

# Summary of Total Rentals
st.subheader("Description")
st.write("""
    Bike sharing systems automate the membership, rental, and return process. 
    With over 500 programs worldwide, these systems help in addressing traffic, environmental, and health issues.
""")

# Display Raw Data
st.subheader("Raw Data")
with st.expander("Hour Dataset"):
    st.write(hour_dataset)
with st.expander("Day Dataset"):
    st.write(day_dataset)

# Display summary statistics
st.subheader("Summary")
st.write("Hour Dataset")
st.write(hour_dataset.describe())
st.write("Day Dataset")
st.write(day_dataset.describe())

# Visualisasi pola sewa sepeda
st.subheader("Bagaimana pola sewa sepeda berubah berdasarkan waktu (hari, bulan, musim)?")

# Mengatur ukuran plot
fig, axs = plt.subplots(3, 1, figsize=(15, 12))

# Visualisasi 1: Rata-rata Sewa Sepeda berdasarkan Hari dalam Seminggu
sns.barplot(data=day_dataset, x='day_of_the_week', y='count_cr', errorbar=None, ax=axs[0])
axs[0].set_title('Rata-rata Jumlah Sewa Sepeda per Hari dalam Seminggu')
axs[0].set_ylabel('Rata-rata Jumlah Sewa (count_cr)')

# Visualisasi 2: Rata-rata Sewa Sepeda berdasarkan Bulan
sns.barplot(data=day_dataset, x='month', y='count_cr', errorbar=None, hue='month', palette='coolwarm', ax=axs[1])
axs[1].set_title('Rata-rata Jumlah Sewa Sepeda per Bulan')
axs[1].set_xlabel('Bulan')
axs[1].set_ylabel('Rata-rata Jumlah Sewa (count_cr)')

# Visualisasi 3: Rata-rata Sewa Sepeda berdasarkan Musim
sns.barplot(data=day_dataset, x='season', y='count_cr', errorbar=None, hue='season', palette='Set2', ax=axs[2])
axs[2].set_title('Rata-rata Jumlah Sewa Sepeda per Musim')
axs[2].set_ylabel('Rata-rata Jumlah Sewa (count_cr)')

plt.tight_layout()
st.pyplot(fig)

# Summary of Findings
st.subheader("Summary of Findings")
st.write("""
         * Grafik menunjukkan bahwa rata-rata jumlah sewa sepeda stabil sepanjang minggu, tanpa ada hari yang menonjol secara signifikan.
         * Jumlah sewa tertinggi terjadi di bulan-bulan dari Mei hingga September, dengan puncaknya pada bulan Juni.
         * Jumlah sewa sepeda menunjukkan peningkatan signifikan pada musim panas, sementara musim dingin mencatat jumlah sewa yang lebih rendah.
""")

# Pengaruh Hari Kerja vs. Akhir Pekan
st.subheader("Bagaimana Pengaruh Hari Kerja vs. Akhir Pekan dan Faktor Cuaca terhadap Jumlah Sewa Sepeda?")

# Membuat dua subset: hari kerja dan akhir pekan
weekday_data = hour_dataset[hour_dataset['workingday'] == 1]
weekend_data = hour_dataset[hour_dataset['workingday'] == 0]

# Visualisasi rata-rata jumlah sewa pada hari kerja vs akhir pekan
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=weekday_data.groupby('hour')['count_cr'].mean().reset_index(), x='hour', y='count_cr', label='Hari Kerja', color='blue', ax=ax)
sns.lineplot(data=weekend_data.groupby('hour')['count_cr'].mean().reset_index(), x='hour', y='count_cr', label='Akhir Pekan', color='orange', ax=ax)
ax.set_title('Perbandingan Rata-rata Sewa Sepeda Hari Kerja vs Akhir Pekan')
ax.set_xlabel('Jam')
ax.set_ylabel('Rata-rata Jumlah Sewa')
ax.legend()

st.pyplot(fig)

# Pengaruh faktor cuaca
fig, axs = plt.subplots(2, 2, figsize=(15, 10))

sns.scatterplot(data=day_dataset, x='temp', y='count_cr', alpha=0.6, ax=axs[0, 0])
axs[0, 0].set_title('Hubungan Suhu (temp) dan Jumlah Sewa (count_cr)')
axs[0, 0].set_xlabel('Suhu (temp)')
axs[0, 0].set_ylabel('Jumlah Sewa (count_cr)')

sns.scatterplot(data=day_dataset, x='humidity', y='count_cr', alpha=0.6, color='orange', ax=axs[0, 1])
axs[0, 1].set_title('Hubungan Kelembaban (humidity) dan Jumlah Sewa (count_cr)')
axs[0, 1].set_xlabel('Kelembaban (humidity)')
axs[0, 1].set_ylabel('Jumlah Sewa (count_cr)')

sns.boxplot(data=day_dataset, x='humidity', y='count_cr', ax=axs[1, 0])
axs[1, 0].set_title('Distribusi Jumlah Sewa (count_cr) Berdasarkan Kelembaban (humidity)')
axs[1, 0].set_xlabel('Kelembaban (humidity)')
axs[1, 0].set_ylabel('Jumlah Sewa (count_cr)')

sns.boxplot(data=day_dataset, x='temp', y='count_cr', ax=axs[1, 1])
axs[1, 1].set_title('Distribusi Jumlah Sewa (count_cr) Berdasarkan Suhu (temp)')
axs[1, 1].set_xlabel('Suhu (temp)')
axs[1, 1].set_ylabel('Jumlah Sewa (count_cr)')

plt.tight_layout()
st.pyplot(fig)

# Summary of Findings
st.subheader("Summary of Findings")
st.write("""
        * Hari Kerja vs. Akhir Pekan: Jumlah sewa sepeda lebih tinggi pada jam sibuk hari kerja (pagi dan sore), sedangkan pada akhir pekan penggunaan sepeda lebih merata sepanjang hari.
        * Cuaca: Suhu yang lebih tinggi cenderung mendorong lebih banyak orang untuk menyewa sepeda, sementara kelembaban tidak secara signifikan memengaruhi jumlah sewa.
         """)

st.subheader("**Simpulan Utama:**")
st.write("""
         
1. Pola Sewa Sepeda Berdasarkan Waktu (Hari, Bulan, Musim):

- Jumlah sewa sepeda menunjukkan variasi yang jelas sepanjang tahun, dengan peningkatan penggunaan selama bulan-bulan hangat (Mei hingga September), terutama di musim panas. Sebaliknya, musim dingin mencatat penurunan yang signifikan.
- Pola ini mengindikasikan bahwa cuaca berpengaruh besar terhadap minat bersepeda, di mana pengguna lebih cenderung menggunakan sepeda untuk rekreasi dan transportasi selama musim yang nyaman.
- Penyedia layanan sewa sepeda harus mempersiapkan persediaan sepeda dan perawatan ekstra saat mendekati musim semi dan musim panas untuk mengakomodasi permintaan yang lebih tinggi.

2. Pengaruh Hari Kerja vs. Akhir Pekan dan Faktor Cuaca terhadap Jumlah Sewa:

- Di hari kerja, pola sewa sepeda menunjukkan dua puncak aktivitas utama pada pagi dan sore hari, yang menandakan penggunaannya untuk perjalanan ke tempat kerja atau sekolah. Pada akhir pekan, penggunaan sepeda lebih merata sepanjang hari, lebih menunjukkan kegiatan rekreasi.
- Faktor cuaca juga berpengaruh, di mana suhu hangat secara signifikan meningkatkan penggunaan sepeda, sementara tingkat kelembaban tidak memiliki dampak yang jelas terhadap jumlah sewa.
- Kesimpulan ini menunjukkan perlunya perencanaan penyewaan yang mempertimbangkan cuaca dan jenis hari. Misalnya, promosi bisa difokuskan pada hari akhir pekan dan musim panas untuk mendorong lebih banyak orang menyewa sepeda untuk rekreasi.""")