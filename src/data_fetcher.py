import requests


def fetch_crypto_data(crypto_ids=['bitcoin', 'ethereum', 'solana'], currency='usd'):
    """Fetch real-time cryptocurrency data from GoinGecko API"""
    url = 'https://api.coingecko.com/api/v3/simple/price'
    params = {
        'ids': ','.join(crypto_ids),
        'vs_currencies': currency,
        'include_market_cap': True,
        'include_24hr_vol': True,
        'include_24hr_change': True
    }
    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise Exception("API request failed. Status code: " + str(response.status_code))
    
    return response.json()
