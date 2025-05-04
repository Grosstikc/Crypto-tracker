import os
from dotenv import load_dotenv
import pandas as pd
import streamlit as st
import json
from pathlib import Path
from src.data_fetcher import fetch_crypto_data, fetch_crypto_news, fetch_historical_data
from src.data_processor import process_crypto_news, process_data, process_historical_data
from src.visualizer import plot_crypto_prices, plot_market_cap, plot_historical_prices
from src.database import SessionLocal, Alert, User

load_dotenv()
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

st.sidebar.subheader("Historical Data Settings")
selected_crypto = st.sidebar.selectbox(
    'Cryptocurrency for historical data:',
    options=['bitcoin', 'ethereum', 'solana', 'cardano', 'ripple'],
    index=0,
    key='historical_crypto_select'
)

historical_currency = st.sidebar.selectbox(
    'Currency for historical data:', ['usd', 'eur', 'gbp'], key='historical_currency_select'
)

historical_days = st.sidebar.slider(
    'Days of history', min_value=7, max_value=365, value=30, key='historical_days_slider'
)

# Explicitly apply filters with button
apply_filters = st.sidebar.button("🚀 Apply Filters")
refresh_data = st.sidebar.button("🔄 Refresh Data")

# Alert Configuration Section 
st.sidebar.subheader("🔔 Set Price Alerts")

telegram_username = st.sidebar.text_input("Your Telegram Username (without @):", key='telegram_username')

alert_crypto = st.sidebar.selectbox(
    "Crypto for Alert:",
    ["bitcoin", "ethereum", "solana", "ripple", "cardano"],
    key="alert_crypto_select"
)

alert_currency = st.sidebar.selectbox(
    "Currency:",
    ["usd", "eur", "gbp"],
    key="alert_currency_select"
)

alert_price = st.sidebar.number_input("Target Price:", value=0.0, step=1.0, key="alert_price_input")

price_direction = st.sidebar.selectbox(
    "Alert When Price Is:",
    ["Above", "Below"],
    key="alert_direction_select"
)

if st.sidebar.button("Set Alert 🚀", key="set_alert_button"):
    db = SessionLocal()
    user = db.query(User).filter(User.username.ilike(telegram_username.strip())).first()

    if user:
        alert = Alert(
            user_id=user.id,
            crypto=alert_crypto,
            currency=alert_currency,
            price=alert_price,
            direction=price_direction,
            triggered=False
        )
        db.add(alert)
        db.commit()
        db.refresh(alert)
        st.sidebar.success(f"✅ Alert set for {alert_crypto.capitalize()} at {alert_price} {alert_currency.upper()}!")
    else:
        st.sidebar.error("⚠️ Username not found. Please subscribe via Telegram bot first (/start).")
    
    db.close()

if refresh_data:
    st.cache_data.clear()
    st.rerun()

if apply_filters:
    # Fetch and display current cryptocurrency market data
    st.subheader("📊 Cryptocurrency Market Data")
    try:
        raw_data = fetch_crypto_data(crypto_ids=crypto_options, currency=currency)
        crypto_df = process_data(raw_data, currency=currency)

        if not crypto_df.empty:
            st.dataframe(crypto_df, use_container_width=True)
            st.plotly_chart(plot_crypto_prices(crypto_df), use_container_width=True)

            market_cap_fig = plot_market_cap(crypto_df)
            if market_cap_fig:
                st.plotly_chart(market_cap_fig, use_container_width=True)
            else:
                st.warning("Market cap data unavailable for selected cryptocurrencies.")
        else:
            st.warning("No data to display.")
    except Exception as e:
        st.error(f"Error fetching data: {e}")

    # Fetch and display historical cryptocurrency data
    st.subheader(f"📈 Historical Price of {selected_crypto.capitalize()}")
    try:
        raw_hist_data = fetch_historical_data(
            crypto_id=selected_crypto,
            currency=historical_currency,
            days=historical_days
        )
        hist_df = process_historical_data(raw_hist_data)

        if 'date' in hist_df.columns and not hist_df.empty:
            hist_chart = plot_historical_prices(hist_df, crypto_name=selected_crypto.capitalize())
            st.plotly_chart(hist_chart, use_container_width=True)
        else:
            st.warning("No historical data available.")
    except Exception as e:
        st.error(f"Error fetching historical data: {e}")
else:
    st.info("👈 Please configure your filters and click '🚀 Apply Filters' to display data.")

# Cryptocurrency News section 
st.subheader("📰 Latest Cryptocurrency News")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
if not NEWS_API_KEY:
    raise Exception("Missing NEWS_API_KEY envirement variable.")

# Fetch and process crypto news
try:
    raw_news_data = fetch_crypto_news(api_key=NEWS_API_KEY)
    news_df = process_crypto_news(raw_news_data)

    if not news_df.empty:
        for _, row in news_df.iterrows():
            st.markdown(f"### [{row['title']}]({row['url']})")
            if row['description']:
                st.write(row['description'])
            st.caption(f"Published on: {row['published_at'].strftime('%Y-%m-%d %H:%M')} | Source: {row['source']}")
            st.divider()
    else:
        st.warning("No recent news articles available.")
except Exception as e:
    st.error(f"Error fetching news: {e}")
