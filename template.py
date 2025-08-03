import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------
# USER AUTHENTICATION
# ------------------------
USERS = {
    "admin": {"password": "admin123", "role": "Admin"},
    "staff": {"password": "staff123", "role": "Gudang"},
}

def login():
    st.title("📦 Login Dashboard Inventory Retail")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = USERS.get(username)
        if user and user["password"] == password:
            st.session_state["login"] = True
            st.session_state["username"] = username
            st.session_state["role"] = user["role"]
            st.experimental_rerun()
        else:
            st.error("Username atau password salah")

# ------------------------
# MAIN DASHBOARD
# ------------------------
def load_data():
    inbound = pd.read_csv("sample_csv/inbound_data.csv")
    stock = pd.read_csv("sample_csv/inventory_stock.csv")
    lokasi = pd.read_csv("sample_csv/lokasi_produk.csv")
    return inbound, stock, lokasi

def dashboard():
    st.sidebar.title("Navigasi")
    menu = st.sidebar.radio("Pilih Halaman", ["Inbound", "Inventory Stock", "Lokasi Produk"])
    st.sidebar.markdown(f"**User:** {st.session_state['username']} ({st.session_state['role']})")
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.experimental_rerun()

    inbound, stock, lokasi = load_data()

    if menu == "Inbound":
        st.header("📥 Data Inbound")
        st.dataframe(inbound)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Jumlah Inbound Hari Ini", inbound[inbound['tanggal'] == '2025-08-01'].shape[0])
        with col2:
            top_supplier = inbound['supplier'].value_counts().idxmax()
            st.metric("Supplier Tersering", top_supplier)

        fig = px.line(inbound, x="tanggal", y="qty", color="supplier", markers=True, title="Tren Inbound per Hari")
        st.plotly_chart(fig)

    elif menu == "Inventory Stock":
        st.header("📦 Inventory Stock")
        st.dataframe(stock)

        low_stock = stock[stock['stok_tersedia'] < 100]
        st.warning("Produk dengan stok rendah:")
        st.dataframe(low_stock)

        fig = px.bar(stock, x="nama_produk", y="stok_tersedia", color="kategori", title="Stok Produk")
        st.plotly_chart(fig)

        fig2 = px.pie(stock, names="kategori", values="stok_tersedia", title="Distribusi Stok per Kategori")
        st.plotly_chart(fig2)

    elif menu == "Lokasi Produk":
        st.header("📍 Lokasi Penempatan Produk")
        st.dataframe(lokasi)

        fig = px.treemap(lokasi, path=["lokasi_rak", "nama_produk"], values="jumlah", title="Distribusi Produk di Gudang")
        st.plotly_chart(fig)

# ------------------------
# APP ENTRY POINT
# ------------------------
if "login" not in st.session_state:
    st.session_state["login"] = False

if not st.session_state["login"]:
    login()
else:
    dashboard()
