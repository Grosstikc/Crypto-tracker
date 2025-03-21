import pandas as pd


def process_historical_data(raw_historical_data):
    """Process raw historical cryptocurrecny data into a structured DataFrame"""
    prices = raw_historical_data.get('prices', [])
    market_caps = raw_historical_data.get('market_caps', [])
    volumes = raw_historical_data.get('total_volumes', [])

    if not prices:
        return pd.DataFrame()

    # Building a DataFrame
    df = pd.DataFrame({
        'date': [pd.to_datetime(p[0], unit='ms') for p in prices],
        'price': [p[1] for p in prices],
        'market_cap': [m[1] for m in market_caps],
        'volume': [v[1] for v in volumes],
    })

    return df

def process_data(raw_data, currency='usd'):
    """
    Safely process cryptocurrency data, ensuring correct handling of missing fields.
    """
    if not raw_data:
        return pd.DataFrame()

    processed_data = []

    for crypto, values in raw_data.items():
        processed_entry = {
            'cryptocurrency': crypto,
            'price': values.get(currency, None),
            'market_cap': values.get(f'{currency}_market_cap', None),
            'volume_24h': values.get(f'{currency}_24h_vol', None),
            'change_24h': values.get(f'{currency}_24h_change', None)
        }
        processed_data.append(processed_entry)

    df = pd.DataFrame(processed_data)

    return df

def process_crypto_news(raw_news_data):
    """
    Process raw cryptocurrency news data into structured DataFrame safely.
    """
    articles = raw_news_data.get('articles', [])

    if not articles:
        return pd.DataFrame()

    news_df = pd.DataFrame([{
        'title': article.get('title'),
        'description': article.get('description', 'No description available'),
        'url': article.get('url'),
        'published_at': article.get('publishedAt'),
        'source': article.get('source', {}).get('name', 'Unknown')
    } for article in articles])

    news_df['published_at'] = pd.to_datetime(news_df['published_at'])
    news_df.drop(columns=['publishedAt'], inplace=True, errors='ignore')

    return news_df
