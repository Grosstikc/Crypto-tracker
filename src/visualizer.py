import plotly.express as px
import plotly.graph_objects as go


def plot_historical_prices(df, crypto_name='Bitcoin'):
    """Plot historical cryptocurrency prices using a line chart."""
    fig = px.line(
        df,
        x='date',
        y='price',
        title=f'{crypto_name} Historical Prices',
        labels={'date': 'Date', 'price': f'Price (USD)'}
    )

    return fig

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
    """Plot cryptocurrency market cap distribution in a pie chart."""

    # Drop rows with missing market_cap to avoid empty charts
    df_filtered = df.dropna(subset=['market_cap'])

    if df_filtered.empty:
        return None  # Avoid plotting empty data

    fig = px.pie(
        df_filtered,
        names='cryptocurrency',
        values='market_cap',
        title='Market Cap Distribution'
    )
    return fig
