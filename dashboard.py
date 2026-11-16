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
st.subheader("📊 Perbandingan Kategori Produk (Tertinggi vs Terendah)")

col_a, col_b = st.columns(2)

with col_a:
    st.markdown("**Top 5 Kategori Tertinggi**")
    fig_top, ax_top = plt.subplots(figsize=(7, 5))
    sns.barplot(
        x='price', 
        y='product_category_name_english', 
        data=top_5, 
        color='#1f77b4', 
        ax=ax_top
    )
    ax_top.set_xlabel("Total Pendapatan (BRL)")
    ax_top.set_ylabel("Kategori Produk")
    st.pyplot(fig_top)

with col_b:
    st.markdown("**Bottom 5 Kategori Terendah**")
    fig_bot, ax_bot = plt.subplots(figsize=(7, 5))
    sns.barplot(
        x='price', 
        y='product_category_name_english', 
        data=bottom_5, 
        color='#ff7f0e', 
        ax=ax_bot
    )
    ax_bot.set_xlabel("Total Pendapatan (BRL)")
    ax_bot.set_ylabel("")
    st.pyplot(fig_bot)

# 7. VISUALISASI 3: TREN VOLUME TRANSAKSI BULANAN (ROBUST & AMAN)
st.subheader("📈 Tren Volume Transaksi Bulanan")

# Pastikan kolom tanggal bertipe datetime
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

# Kita buat salinan dataframe untuk tren bulanan (opsional: bisa menggunakan df keseluruhan 
# atau main_df. Jika ingin tren tetap stabil menampilkan semua bulan meski di-filter, 
# gunakan df. Jika ingin mengikuti filter tanggal sidebar, gunakan main_df tapi pastikan formatnya aman).
# Di sini kita gunakan df agar tren bulanan utuh, atau main_df jika ingin mengikuti filter:
trend_df = main_df.copy()

# Ekstraksi bulan-tahun dengan aman menggunakan string formatting .dt.to_period('M') atau .dt.strftime('%Y-%m')
trend_df['order_month_year'] = trend_df['order_purchase_timestamp'].dt.strftime('%Y-%m')
monthly_orders = trend_df.groupby('order_month_year')['order_id'].nunique().reset_index()

# Urutkan berdasarkan bulan
monthly_orders = monthly_orders.sort_values('order_month_year')

# Pengecekan jika data bulanan kosong setelah filter
if monthly_orders.empty:
    st.warning("⚠️ Tidak ada data transaksi yang tersedia pada rentang tanggal yang dipilih.")
else:
    fig2, ax2 = plt.subplots(figsize=(12, 5))
    ax2.plot(
        monthly_orders['order_month_year'], 
        monthly_orders['order_id'], 
        marker='o', 
        color='#1f77b4', 
        linewidth=2
    )
    plt.xticks(rotation=45)
    ax2.set_title("Tren Jumlah Pesanan Bulanan", fontsize=14, fontweight='bold')
    ax2.set_xlabel("Bulan-Tahun", fontsize=12)
    ax2.set_ylabel("Jumlah Pesanan", fontsize=12)
    ax2.grid(True, linestyle='--', alpha=0.6)
    st.pyplot(fig2)

# Footer
st.markdown("---")
st.caption("Dibuat untuk memenuhi kriteria Proyek Akhir Analisis Data.")