import pandas as pd

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
