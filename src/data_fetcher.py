import requests
import time
import streamlit as st

@st.cache_data(ttl=600)  # cache data for 5 minutes
def fetch_historical_data(crypto_id='bitcoin', currency='usd', days=30):
    """Fetch historical cryptocurrency data from CoinGecko API"""
    url = f'https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart'
    params = {
        'vs_currency': currency,
        'days': days,
        'interval': 'daily'
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise Exception(f"API request failed. Status code: {response.status_code}")
    
    return response.json()

@st.cache_data(ttl=300)  # cache data for 5 minutes
def fetch_crypto_data(crypto_ids=['bitcoin', 'ethereum', 'solana'], currency='usd'):
    """Fetch real-time cryptocurrency data from GoinGecko API"""
    url = 'https://api.coingecko.com/api/v3/simple/price'
    params = {
        'ids': ','.join(crypto_ids),
        'vs_currencies': currency,
        'include_market_cap': 'true',
        'include_24hr_vol': 'true',
        'include_24hr_change': 'true'
    }
    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise Exception(f"API request failed. Status code: {response.status_code}")
    
    return response.json()

@st.cache_data(ttl=900) # Cache data for 10 minutes
def fetch_crypto_news(api_key, query='cryptocurrency OR bitcoin OR ethereum', language='en', page_size=10):
    """Fetch recent crypto news from NewsAPI."""
    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': query,
        'language': language,
        'sortBy': 'publishedAt',
        'pageSize': page_size,
        'apiKey': api_key
    }

    response = requests.get(url, params=params)

    if response.status_code!= 200:
        raise Exception(f"API request failed. Status code: {response.status_code}, Message: {response.text}")
    
    return response.json()
