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

def process_data(raw_data):
    """
    Safely process cryptocurrency data, ensuring correct handling of missing fields.
    """
    if not raw_data:
        return pd.DataFrame()

    processed_data = []

    for crypto, values in raw_data.items():
        processed_entry = {
            'cryptocurrency': crypto,
            'price': values.get('usd', None),
            'market_cap': values.get('usd_market_cap', None),
            'volume_24h': values.get('usd_24h_vol', None),
            'change_24h': values.get('usd_24h_change', None)
        }
        processed_data.append(processed_entry)

    df = pd.DataFrame(processed_data)

    return df
