import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
import yfinance as yf
from sklearn.linear_model import LinearRegression
import numpy as np

# ==========================================
# 1. APPLICATION VIEWPORT SETUP
# ==========================================
st.set_page_config(page_title="Universal Crypto Intelligence Engine", page_icon="⚡", layout="wide")

st.title("⚡ Universal Real-Time Crypto Risk Analytics Terminal")
st.markdown("An enterprise-grade data engineering framework capable of indexing, scoring, and visually mapping **any asset class** across high-cap tokens, altcoins, meme economies, and micro-cap utility networks.")

# ==========================================
# 2. CONTROL PANEL & SIDEBAR SETUP
# ==========================================
st.sidebar.header("🎛️ Control Panel")
st.sidebar.markdown("Configure your analytics viewport and technical tracking overlays below.")

# Main Input Bar
search_query = st.text_input("🎯 Enter Any Cryptocurrency Token Symbol (e.g. BTC, ETH, DMTR, VLO, PEPE, SHIB):", value="BTC").strip().upper()

if not search_query:
    search_query = "BTC"

# Global Currency Selector Switch
currency_selection = st.sidebar.selectbox("💵 Fiat Base Currency:", ["USD", "INR", "EUR", "GBP", "JPY"], index=0)

currency_symbols = {"USD": "$", "INR": "₹", "EUR": "€", "GBP": "£", "JPY": "¥"}
currency_rates = {"USD": 1.0, "INR": 83.5, "EUR": 0.92, "GBP": 0.78, "JPY": 155.0}

curr_symbol = currency_symbols[currency_selection]
curr_rate = currency_rates[currency_selection]

# Full Interactive Timeframe Range Selector
st.sidebar.markdown("---")
st.sidebar.subheader("⏰ Analysis Horizon")
timeframe = st.sidebar.radio(
    "Choose historical scale window:",
    ["1 Day", "1 Week", "1 Month", "3 Month", "6 Month", "1 Year", "MAX"],
    index=5,
    horizontal=False
)

tf_map = {
    "1 Day": "1d",
    "1 Week": "5d",
    "1 Month": "1mo",
    "3 Month": "3mo",
    "6 Month": "6mo",
    "1 Year": "1y",
    "MAX": "max"
}
chosen_period = tf_map[timeframe]

# Technical Moving Average Overlays
st.sidebar.markdown("---")
st.sidebar.subheader("📈 Chart Overlay Configurations")
show_ma50 = st.sidebar.checkbox("Overlay 50-Day SMA Trendline", value=True)
show_ma200 = st.sidebar.checkbox("Overlay 200-Day SMA Base line", value=False)

if search_query in ["USDT", "USDC", "DAI", "BUSD"]:
    ticker_symbol = f"{search_query}==X"
else:
    ticker_symbol = f"{search_query}-USD"

if st.sidebar.button("🔄 Clear App Cache Buffer"):
    st.cache_data.clear()
    st.rerun()

# ==========================================
# 3. DATA INGESTION ENGINE
# ==========================================
@st.cache_data(ttl=30)  
def extract_crypto_lifespan(ticker, period):
    try:
        data_pull = yf.Ticker(ticker)
        raw_df = data_pull.history(period=period) 
        if not raw_df.empty:
            df = raw_df.reset_index()
            df['Date'] = df['Date'].dt.tz_localize(None)
            return df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    except Exception:
        pass

    try:
        clean_pair = ticker.replace("-USD", "USDT")
        url = f"https://api.binance.com/api/v3/klines?symbol={clean_pair}&interval=1d&limit=100"
        response = requests.get(url, timeout=5).json()
        df = pd.DataFrame(response, columns=[
            'Open Time', 'Open', 'High', 'Low', 'Close', 'Volume',
            'Close Time', 'Quote Asset Volume', 'Number of Trades',
            'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore'
        ])
        df['Date'] = pd.to_datetime(df['Open Time'], unit='ms')
        df['Open'] = df['Open'].astype(float)
        df['High'] = df['High'].astype(float)
        df['Low'] = df['Low'].astype(float)
        df['Close'] = df['Close'].astype(float)
        df['Volume'] = df['Volume'].astype(float)
        return df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    except Exception:
        return pd.DataFrame()

@st.cache_data(ttl=3600)  
def fetch_asset_profile_summary(ticker, symbol):
    try:
        asset_engine = yf.Ticker(ticker)
        asset_info = asset_engine.info
        description = asset_info.get('description') or asset_info.get('longBusinessSummary')
        if description and len(description.strip()) > 10:
            return description
    except Exception:
        pass
    
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{symbol.lower()}"
        response = requests.get(url, timeout=5).json()
        description = response.get('description', {}).get('en')
        if description and len(description.strip()) > 10:
            return description.split("<a href=")[0]
    except Exception:
        pass

    return f"Detailed project documentation for '{symbol}' is actively tracked on decentralized ledger ecosystems."

# ==========================================
# 4. DATA COMPUTATION & VIEWPORT MATRIX
# ==========================================
try:
    with st.spinner(f"Ingesting live network ledgers for '{search_query}'..."):
        df_metrics = extract_crypto_lifespan(ticker_symbol, chosen_period)
        project_profile = fetch_asset_profile_summary(ticker_symbol, search_query)
    
    if not df_metrics.empty:
        # Fetching Sidebar Network Statistics
        try:
            live_ticker_instance = yf.Ticker(ticker_symbol)
            network_stats = live_ticker_instance.info
            st.sidebar.markdown("---")
            st.sidebar.subheader("🏆 Token Network Stats")
            m_cap = network_stats.get('marketCap')
            vol_24 = network_stats.get('volume24Hr') or network_stats.get('volume')
            circ_supply = network_stats.get('circulatingSupply')
            st.sidebar.write(f"**Market Cap:** {curr_symbol}{m_cap*curr_rate:,.0f}" if m_cap else "**Market Cap:** N/A")
            st.sidebar.write(f"**24h Vol:** {curr_symbol}{vol_24*curr_rate:,.0f}" if vol_24 else "**24h Vol:** N/A")
            st.sidebar.write(f"**Circ Supply:** {circ_supply:,.0f} {search_query}" if circ_supply else "**Circ Supply:** N/A")
        except Exception:
            pass

        # Exchange Recommendation Engine Logic
        st.sidebar.markdown("---")
        st.sidebar.subheader("🏪 Recommended Exchanges")
        if search_query in ["BTC", "ETH", "SOL", "BNB", "XRP"]:
            st.sidebar.info("💡 Available on Tier-1 Markets:\n* **Binance**\n* **Coinbase**\n* **Kraken**")
        else:
            st.sidebar.warning("💡 Low-Cap / Altcoin Markets:\n* **KuCoin**\n* **Gate.io**\n* **Uniswap / Raydium**")

        # Calculations & Currency Scaling Applied
        live_price = df_metrics['Close'].iloc[-1] * curr_rate
        open_price = df_metrics['Open'].iloc[-1] * curr_rate
        ath_price = df_metrics['High'].max() * curr_rate
        atl_price = df_metrics['Low'].min() * curr_rate
        
        rolling_mean = df_metrics['Close'].rolling(window=50).mean().iloc[-1]
        if pd.isna(rolling_mean):
            rolling_mean = df_metrics['Close'].iloc[-1]
        rolling_mean *= curr_rate
            
        entry_target =
