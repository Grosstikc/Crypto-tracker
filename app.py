import pandas as pd
import streamlit as st
import requests
from src.data_fetcher import fetch_crypto_data
from src.data_processor import process_data
from src.visualizer import plot_crypto_prices, plot_market_cap


# App comfiguration
st.set_page_config(page_title='Crypto Market Tracker', layout='wide')

# App header
st.title("🚀 Cryptocurrency Market Tracker")

# User inputs (sidebar)
st.sidebar.header("Configure your preferences:")
crypto_options = st.sidebar.multiselect(
    'Select cryptocurrencies:',
    options=['bitcoin', 'ethereum', 'solana', 'ripple', 'cardano', 'dogecoin'],
    default=['bitcoin', 'ethereum', 'solana']
)

currency = st.sidebar.selectbox('Select Currency:', ['usd', 'eur', 'gbp'])

# Fetch and process data
try:
    raw_data = fetch_crypto_data(crypto_ids=crypto_options, currency=currency)
    crypto_df = process_data(raw_data)
except Exception as e:
    st.error(f"Error fetching data: {e}")
    crypto_df = pd.DataFrame()


# Display data table
st.subheader("📊 Cryptocurrency Market Data")
st.dataframe(crypto_df, use_container_width=True)

# Visualizations
if not crypto_df.empty:
    st.plotly_chart(plot_crypto_prices(crypto_df), use_container_width=True)
    st.plotly_chart(plot_market_cap(crypto_df), use_container_width=True)
else:
    st.warning("No data to display.")
