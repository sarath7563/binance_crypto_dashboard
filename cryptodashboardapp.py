import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
import yfinance as yf
import numpy as np
from sklearn.linear_model import LinearRegression

# ==========================================
# 1. APPLICATION VIEWPORT SETUP
# ==========================================
st.set_page_config(page_title="Universal Crypto Predictive Engine", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    div.stMetric { background-color: #1f2937; border: 1px solid #374151; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ Universal Crypto Risk Analytics & Predictive Terminal")
st.markdown("An enterprise-grade data engineering framework using machine learning trend projection, currency conversion filters, and qualitative analysis modules.")

# ==========================================
# 2. CONTROL PANEL & SIDEBAR SETUP
# ==========================================
st.sidebar.header("🎛️ Control Panel")
st.sidebar.markdown("Configure your analytics viewport and currency tracking overlays below.")

# Main Input Bar
search_query = st.text_input("🎯 Enter Any Cryptocurrency Token Symbol (e.g. BTC, ETH, DMTR, VLO, PEPE):", value="BTC").strip().upper()

if not search_query:
    search_query = "BTC"

# Dynamic Global Currency Selector Filter
st.sidebar.markdown("---")
st.sidebar.subheader("💱 Fiat Base Currency")
selected_currency = st.sidebar.selectbox(
    "Select Display Currency Units:",
    ["USD ($)", "INR (₹)", "EUR (€)", "GBP (£)", "JPY (¥)"],
    index=0
)

# Set map symbols and conversion variables
currency_map = {"USD ($)": ("$", 1.0), "INR (₹)": ("₹", 83.5), "EUR (€)": ("€", 0.92), "GBP (£)": ("£", 0.78), "JPY (¥)": ("¥", 155.0)}
currency_symbol, fallback_rate = currency_map[selected_currency]

# Live Currency Conversion Multiplier Pipeline
@st.cache_data(ttl=3600)
def get_live_fiat_rate(target_currency):
    if target_currency == "USD ($)":
        return 1.0
    try:
        fiat_ticker = target_currency.split(" (")[0] + "=X"
        rate_data = yf.Ticker(fiat_ticker).history(period="1d")
        if not rate_data.empty:
            return float(rate_data['Close'].iloc[-1])
    except Exception:
        pass
    return fallback_rate

# Compute multiplier conversion index
conversion_rate = get_live_fiat_rate(selected_currency)

# Timeframe Range Selector (1D, 1W, 1M, 3M, 6M, 1Y, MAX)
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

# Technical Overlays Control
st.sidebar.markdown("---")
st.sidebar.subheader("📈 Chart Overlay Configurations")
show_ma50 = st.sidebar.checkbox("Overlay 50-Day SMA Trendline", value=True)
show_predict = st.sidebar.checkbox("🔮 Show 7-Day Machine Learning Forecast Line", value=True)

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

# Comprehensive Token Information and Technology Profile Parser (Completely closed and aligned)
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

    return f"Detailed project documentation for '{symbol}' is actively tracked on decentralized ledger networks. This token operates as a primary cryptographic asset running native consensus and execution rules within its respective blockchain network layer."

# ==========================================
# 4. DATA COMPUTATION & MACHINE LEARNING PREDICTION
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
            st.sidebar.write(f"**Market Cap:** {currency_symbol}{m_cap*conversion_rate:,.0f}" if m_cap else "**Market Cap:** N/A")
            st.sidebar.write(f"**24h Vol:** {currency_symbol}{vol_24*conversion_rate:,.0f}" if vol_24 else "**24h Vol:** N/A")
            st.sidebar.write(f"**Circ Supply:** {circ_supply:,.0f} {search_query}" if circ_supply else "**Circ Supply:** N/A")
        except Exception:
            pass

        # Apply Live Fiat Multiplier to Ticker Data Columns
        for col in ['Open', 'High', 'Low', 'Close']:
            df_metrics[col] = df_metrics[col] * conversion_rate

        live_price = df_metrics['Close'].iloc[-1]
        open_price = df_metrics['Open'].iloc[-1]
        ath_price = df_metrics['High'].max()
        atl_price = df_metrics['Low'].min()
        
        rolling_mean = df_metrics['Close'].rolling(window=50).mean().iloc[-1]
        if pd.isna(rolling_mean):
            rolling_mean = live_price
            
        entry_target = rolling_mean * 0.90
        exit_target = ath_price * 0.95

        if exit_target <= live_price:
            exit_target = live_price * 1.15

        daily_change_usd = live_price - open_price
        daily_change_pct = (daily_change_usd / open_price) * 100

        # --- MACHINE LEARNING PREDICTION PIPELINE ---
        df_metrics['Day_Index'] = np.arange(len(df_metrics))
        X = df_metrics[['Day_Index']].values
        y = df_metrics['Close'].values
        
        model = LinearRegression()
        model.fit(X, y)
        
        future_indices = np.array([[len(df_metrics) + i] for i in range(1, 8)])
        future_predictions = model.predict(future_indices)
        
        last_date = df_metrics['Date'].iloc[-1]
        future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=7)
        
        is_increasing = future_predictions[-1] > live_price
        trend_status = "📈 UPWARD EXPECTED" if is_increasing else "📉 DOWNWARD EXPECTED"
        
        # Summary Metrics Grid Display Row
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric(label=f"Current {search_query} Value ({selected_currency.split(' ')[0]})", value=f"{currency_symbol}{live_price:,.4f}", delta=f"{daily_change_pct:+.2f}%")
        with m2:
            st.metric(label="Suggested Entry (Floor Target)", value=f"{currency_symbol}{entry_target:,.4f}")
        with m3:
