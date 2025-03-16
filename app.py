import pandas as pd
import streamlit as st
from src.data_fetcher import fetch_crypto_data, fetch_historical_data
from src.data_processor import process_data, process_historical_data
from src.visualizer import plot_crypto_prices, plot_market_cap, plot_historical_prices

# App configuration
st.set_page_config(page_title='Crypto Market Tracker', layout='wide')

# App header
st.title("🚀 Cryptocurrency Market Tracker")

# Sidebar configuration
st.sidebar.header("Configure your preferences:")
crypto_options = st.sidebar.multiselect(
    'Select cryptocurrencies:',
    options=['bitcoin', 'ethereum', 'solana', 'ripple', 'cardano', 'dogecoin'],
    default=['bitcoin', 'ethereum', 'solana'],
    key='crypto_multiselect'
)

currency = st.sidebar.selectbox(
    'Select Currency:', ['usd', 'eur', 'gbp'], key='main_currency_select'
)

# Fetch and process current cryptocurrency data
try:
    raw_data = fetch_crypto_data(crypto_ids=crypto_options, currency=currency)
    crypto_df = process_data(raw_data)
except Exception as e:
    st.error(f"Error fetching data: {e}")
    crypto_df = pd.DataFrame()

# Historical data section (sidebar)
st.sidebar.subheader("Historical Data Settings")
selected_crypto = st.sidebar.selectbox(
    'Select cryptocurrency for historical data:',
    options=['bitcoin', 'ethereum', 'solana', 'cardano', 'ripple'],
    index=0,
    key='historical_crypto_select'
)

historical_currency = st.sidebar.selectbox(
    'Select Currency for historical data:', ['usd', 'eur', 'gbp'], key='historical_currency_select'
)

historical_days = st.sidebar.slider(
    'Days of history', min_value=7, max_value=365, value=30, key='historical_days_slider'
)

# Fetch and process historical data
try:
    raw_hist_data = fetch_historical_data(
        crypto_id=selected_crypto,
        currency=historical_currency,
        days=historical_days
    )
    hist_df = process_historical_data(raw_hist_data)
except Exception as e:
    st.error(f"Error fetching historical data: {e}")
    hist_df = pd.DataFrame()

# Display historical data visualization
if 'date' in hist_df.columns and not hist_df.empty:
    st.subheader(f"📈 Historical Price of {selected_crypto.capitalize()}")
    hist_chart = plot_historical_prices(hist_df, crypto_name=selected_crypto.capitalize())
    st.plotly_chart(hist_chart, use_container_width=True)
else:
    st.warning("No historical data available.")

# Display current cryptocurrency market data
st.subheader("📊 Cryptocurrency Market Data")
if not crypto_df.empty:
    st.dataframe(crypto_df, use_container_width=True)
    st.plotly_chart(plot_crypto_prices(crypto_df), use_container_width=True)
    
    # Properly handle market cap distribution
    market_cap_fig = plot_market_cap(crypto_df)
    if market_cap_fig:
        st.plotly_chart(market_cap_fig, use_container_width=True)
    else:
        st.warning("Market cap data unavailable for selected cryptocurrencies.")
else:
    st.warning("No data to display.")
