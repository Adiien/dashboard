import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Pengaturan Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="E-Commerce Data Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)

# 1. LOAD CLEANED DATA
@st.cache_data
def load_data():
    # Memuat file main_data.csv yang ada di folder dashboard
    df = pd.read_csv('main_data.csv')
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    return df

df = load_data()

# 2. SIDEBAR (FILTER RENTANG WAKTU YANG AMAN & FULL RANGE)
st.sidebar.header("Filter Data")

# Mengambil nilai minimum dan maksimum dari kolom tanggal (dikonversi ke date)
min_date = df['order_purchase_timestamp'].min().date()
max_date = df['order_purchase_timestamp'].max().date()

# Membuat widget date_input dengan rentang default dari awal hingga akhir data
date_range = st.sidebar.date_input(
    label="Rentang Waktu",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    st.sidebar.warning("⚠️ Mohon pilih tanggal awal dan tanggal akhir secara lengkap untuk menampilkan data spesifik.")
    start_date = min_date
    end_date = max_date

# Filter dataframe berdasarkan rentang tanggal yang dipilih
main_df = df[(df['order_purchase_timestamp'].dt.date >= start_date) & 
             (df['order_purchase_timestamp'].dt.date <= end_date)]

# 3. KONTROL UTAMA DASHBOARD
st.title("📊 Dashboard Analisis E-Commerce Public Dataset")
st.markdown("Proyek Akhir Analisis Data - Visualisasi Kinerja Penjualan dan Tren Transaksi")

# METRIK UTAMA DI ATAS
total_revenue = main_df['price'].sum()
total_orders = main_df['order_id'].nunique()
total_customers = main_df['customer_unique_id'].nunique() if 'customer_unique_id' in main_df.columns else main_df['customer_id'].nunique()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Pendapatan (Revenue)", value=f"BRL {total_revenue:,.2f}")
with col2:
    st.metric("Total Pesanan (Orders)", value=f"{total_orders:,}")
with col3:
    st.metric("Total Pelanggan Unik", value=f"{total_customers:,}")

st.markdown("---")

# VISUALISASI 1A: TOP 10 KATEGORI PRODUK TERTINGGI (Warna Seragam)
st.subheader("🏆 Top 10 Kategori Produk dengan Pendapatan Tertinggi")

product_revenue = main_df.groupby('product_category_name_english')['price'].sum().reset_index()
product_revenue_sorted = product_revenue.sort_values(by='price', ascending=False)

top_10 = product_revenue_sorted.head(10)
bottom_10 = product_revenue_sorted.tail(10).sort_values(by='price', ascending=True)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    x='price', 
    y='product_category_name_english', 
    data=top_10, 
    color='#1f77b4',  
    ax=ax
)
ax.set_title("10 Kategori Produk dengan Pendapatan Tertinggi", fontsize=14, fontweight='bold')
ax.set_xlabel("Total Pendapatan (BRL)", fontsize=12)
ax.set_ylabel("Kategori Produk", fontsize=12)
st.pyplot(fig)

# VISUALISASI 1B: 10 KATEGORI PRODUK DENGAN PENDAPATAN TERENDAH
st.subheader("📉 10 Kategori Produk dengan Pendapatan Terendah")

fig_bot, ax_bot = plt.subplots(figsize=(10, 5))
sns.barplot(
    x='price', 
    y='product_category_name_english', 
    data=bottom_10, 
    color='#ff7f0e',  # Warna seragam untuk pembeda
    ax=ax_bot         # Menggunakan parameter 'ax', bukan 'ax_bot'
)
ax_bot.set_title("10 Kategori Produk dengan Pendapatan Terendah", fontsize=14, fontweight='bold')
ax_bot.set_xlabel("Total Pendapatan (BRL)", fontsize=12)
ax_bot.set_ylabel("Kategori Produk", fontsize=12)
st.pyplot(fig_bot)

# 2. SIDEBAR (FILTER RENTANG WAKTU ANTI-COLLAPSE)
st.sidebar.header("Filter Data")

min_date = pd.to_datetime(df['order_purchase_timestamp']).min().date()
max_date = pd.to_datetime(df['order_purchase_timestamp']).max().date()

date_range = st.sidebar.date_input(
    label="Rentang Waktu",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Menangani berbagai format output dari date_input Streamlit
if isinstance(date_range, (tuple, list)):
    if len(date_range) == 2:
        start_date, end_date = date_range
    elif len(date_range) == 1:
        start_date = date_range[0]
        end_date = max_date
    else:
        start_date, end_date = min_date, max_date
else:
    start_date = date_range
    end_date = max_date

# PENGAMANAN: Jika tanggal awal dan akhir tidak sengaja sama (1 titik), 
# kembalikan end_date ke max_date agar grafik tren tidak ciut
if start_date == end_date:
    end_date = max_date
    st.sidebar.info("ℹ️ Menampilkan data penuh dari tanggal yang dipilih hingga akhir periode.")

# Filter dataframe berdasarkan rentang tanggal yang aman
main_df = df[(pd.to_datetime(df['order_purchase_timestamp']).dt.date >= start_date) & 
             (pd.to_datetime(df['order_purchase_timestamp']).dt.date <= end_date)]

# Footer catatan
st.markdown("---")
st.caption("Dibuat untuk memenuhi kriteria Proyek Akhir Analisis Data.")