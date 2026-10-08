import time

import requests
import streamlit as st


def make_request(url, params=None, max_retries=3):
    """
    Make an HTTP request with basic retry handling.
    """

    for attempt in range(max_retries):

        try:
            response = requests.get(
                url,
                params=params,
                timeout=10
            )

            if response.status_code == 200:
                return response.json()

            if response.status_code == 429:

                retry_after = response.headers.get(
                    "Retry-After"
                )

                if retry_after:
                    wait_time = int(retry_after)
                else:
                    wait_time = 5 * (attempt + 1)

                print(
                    f"Rate limit reached. "
                    f"Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)
                continue

            raise Exception(
                f"API request failed. "
                f"Status code: {response.status_code}. "
                f"Response: {response.text}"
            )

        except requests.RequestException as e:

            if attempt == max_retries - 1:
                raise Exception(
                    f"Network request failed: {e}"
                )

            time.sleep(2)

    raise Exception(
        "API request failed after multiple retries."
    )


@st.cache_data(ttl=600)
def fetch_historical_data(
    crypto_id="bitcoin",
    currency="usd",
    days=30
):
    """
    Fetch historical cryptocurrency data
    from CoinGecko API.
    """

    url = (
        f"https://api.coingecko.com/api/v3/"
        f"coins/{crypto_id}/market_chart"
    )

    params = {
        "vs_currency": currency,
        "days": days,
        "interval": "daily"
    }

    return make_request(url, params)


def fetch_crypto_data_no_cache(
    crypto_ids=None,
    currency="usd"
):
    """
    Fetch real-time cryptocurrency data
    from CoinGecko API.
    """

    if crypto_ids is None:
        crypto_ids = [
            "bitcoin",
            "ethereum",
            "solana"
        ]

    url = (
        "https://api.coingecko.com/api/v3/"
        "simple/price"
    )

    params = {
        "ids": ",".join(crypto_ids),
        "vs_currencies": currency,
        "include_market_cap": "true",
        "include_24hr_vol": "true",
        "include_24hr_change": "true"
    }

    return make_request(url, params)


@st.cache_data(ttl=300)
def fetch_crypto_data(
    crypto_ids=None,
    currency="usd"
):
    """
    Cached cryptocurrency data for Streamlit.
    """

    return fetch_crypto_data_no_cache(
        crypto_ids,
        currency
    )


@st.cache_data(ttl=900)
def fetch_crypto_news(
    api_key,
    query="cryptocurrency OR bitcoin OR ethereum",
    language="en",
    page_size=10
):
    """
    Fetch recent cryptocurrency news
    from NewsAPI.
    """

    url = "https://newsapi.org/v2/everything"

    params = {
        "q": query,
        "language": language,
        "sortBy": "publishedAt",
        "pageSize": page_size,
        "apiKey": api_key
    }

    return make_request(url, params)
