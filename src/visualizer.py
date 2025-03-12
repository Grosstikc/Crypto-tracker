import plotly.express as px


def plot_crypto_prices(df):
    """Plot cryptocurrency prices in a bar chart."""
    fig = px.bar(
        df,
        x='cryptocurrency',
        y='price',
        title='Current Cryptocurrency Prices',
        labels={'price': 'Price (USD)', 'cryptocurrency': 'Cryptocurrency'}
    )
    return fig

def plot_market_cap(df):
    """Plot cryptocurrency market cap distrubution in a pie chart."""
    fig = px.pie(
        df,
        names='cryptocurrency',
        values='market_cap',
        title='Market Cap Distribution'
    )
    return fig 
