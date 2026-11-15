import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# 1. KONFIGURASI HALAMAN
st.set_page_config(
    page_title="E-Commerce Data Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)

# 2. MEMUAT DATA BERSIH
@st.cache_data
def load_data():
    df = pd.read_csv('main_data.csv')
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    return df

df = load_data()

# 3. SIDEBAR (FILTER RENTANG WAKTU - HANYA SATU Kali)
st.sidebar.header("Filter Data")

min_date = pd.to_datetime(df['order_purchase_timestamp']).min().date()
max_date = pd.to_datetime(df['order_purchase_timestamp']).max().date()

date_range = st.sidebar.date_input(
    label="Rentang Waktu",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
    key="main_date_range_filter"
)

# Validasi agar rentang tanggal aman dan tidak 1 titik
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

if start_date == end_date:
    end_date = max_date
    st.sidebar.info("ℹ️ Menampilkan data penuh dari tanggal yang dipilih hingga akhir periode.")

# Filter dataframe utama
main_df = df[(pd.to_datetime(df['order_purchase_timestamp']).dt.date >= start_date) & 
             (pd.to_datetime(df['order_purchase_timestamp']).dt.date <= end_date)]

# 4. HEADER & METRIK UTAMA DASHBOARD
st.title("📊 Dashboard Analisis E-Commerce Public Dataset")
st.markdown("Proyek Akhir Analisis Data - Visualisasi Kinerja Penjualan dan Tren Transaksi")

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

# Pengolahan data kategori produk
product_revenue = main_df.groupby('product_category_name_english')['price'].sum().reset_index()
product_revenue_sorted = product_revenue.sort_values(by='price', ascending=False)

top_10 = product_revenue_sorted.head(10)
bottom_10 = product_revenue_sorted.tail(10).sort_values(by='price', ascending=True)

# 5. VISUALISASI 1: TOP 10 KATEGORI PRODUK TERTINGGI
st.subheader("🏆 Top 10 Kategori Produk dengan Pendapatan Tertinggi")

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

# 6. VISUALISASI 2: 10 KATEGORI PRODUK TERENDAH (Sesuai Catatan Reviewer)
st.subheader("📉 10 Kategori Produk dengan Pendapatan Terendah")

fig_bot, ax_bot = plt.subplots(figsize=(10, 5))
sns.barplot(
    x='price', 
    y='product_category_name_english', 
    data=bottom_10, 
    color='#ff7f0e', 
    ax=ax_bot
)
ax_bot.set_title("10 Kategori Produk dengan Pendapatan Terendah", fontsize=14, fontweight='bold')
ax_bot.set_xlabel("Total Pendapatan (BRL)", fontsize=12)
ax_bot.set_ylabel("Kategori Produk", fontsize=12)
st.pyplot(fig_bot)

st.markdown("---")

# 7. VISUALISASI 3: TREN VOLUME TRANSAKSI BULANAN
st.subheader("📈 Tren Volume Transaksi Bulanan")

main_df['order_month_year'] = pd.to_datetime(main_df['order_purchase_timestamp']).dt.to_period('M').astype(str)
monthly_orders = main_df.groupby('order_month_year')['order_id'].nunique().reset_index()

fig2, ax2 = plt.subplots(figsize=(12, 5))
ax2.plot(
    monthly_orders['order_month_year'], 
    monthly_orders['order_id'], 
    marker='o', 
    color='b', 
    linewidth=2
)
plt.xticks(rotation=45)
ax2.set_title("Tren Jumlah Pesanan Bulanan", fontsize=14, fontweight='bold')
ax2.set_xlabel("Bulan-Tahun", fontsize=12)
ax2.set_ylabel("Jumlah Pesanan", fontsize=12)
st.pyplot(fig2)

# Footer
st.markdown("---")
st.caption("Dibuat untuk memenuhi kriteria Proyek Akhir Analisis Data.")