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

# 2. SIDEBAR (FILTER RENTANG WAKTU YANG AMAN)
st.sidebar.header("Filter Data")

min_date = df['order_purchase_timestamp'].min()
max_date = df['order_purchase_timestamp'].max()

try:
    # Memastikan date_input mengembalikan rentang (start dan end)
    date_value = st.sidebar.date_input(
        label="Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
    # Validasi apakah user memilih lengkap (start dan end date)
    if isinstance(date_value, (list, tuple)) and len(date_value) == 2:
        start_date, end_date = date_value
    else:
        start_date = min_date
        end_date = max_date
        st.sidebar.warning("Mohon pilih tanggal awal dan akhir secara lengkap.")

except Exception as e:
    start_date = min_date
    end_date = max_date

# Filter dataframe berdasarkan tanggal
main_df = df[(df['order_purchase_timestamp'] >= pd.to_datetime(start_date)) & 
             (df['order_purchase_timestamp'] <= pd.to_datetime(end_date))]

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

# VISUALISASI 1: TOP 10 KATEGORI PRODUK (Warna Seragam)
st.subheader("🏆 Top 10 Kategori Produk dengan Pendapatan Tertinggi")

product_revenue = main_df.groupby('product_category_name_english')['price'].sum().reset_index()
product_revenue = product_revenue.sort_values(by='price', ascending=False).head(10)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    x='price', 
    y='product_category_name_english', 
    data=product_revenue, 
    color='#1f77b4',  # Menggunakan warna seragam (solid blue)
    ax=ax
)
ax.set_title("Top 10 Kategori Produk Berdasarkan Pendapatan", fontsize=14, fontweight='bold')
ax.set_xlabel("Total Pendapatan (BRL)", fontsize=12)
ax.set_ylabel("Kategori Produk", fontsize=12)
st.pyplot(fig)

# 5. VISUALISASI 2: TREN VOLUME TRANSAKSI BULANAN
st.subheader("📈 Tren Volume Transaksi Bulanan")

main_df['order_month_year'] = main_df['order_purchase_timestamp'].dt.to_period('M').astype(str)
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

# Footer catatan
st.markdown("---")
st.caption("Dibuat untuk memenuhi kriteria Proyek Akhir Analisis Data.")