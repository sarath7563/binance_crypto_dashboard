import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
import yfinance as yf

# 1. PAGE LAYOUT CONFIGURATION
st.set_page_config(page_title="Binance Analytics Engine", page_icon="⚡", layout="wide")

st.title("⚡ Real-Time Binance Market Intelligence Dashboard")
st.markdown("An advanced college project tracking active trading pairs, full historical lifespans, and math-driven entry/exit signals.")

# 2. DYNAMIC BINANCE TICKER INGESTION PIPELINE
@st.cache_data(ttl=600)
def fetch_binance_symbols():
    try:
        url = "https://api.binance.com/api/v3/exchangeInfo"
        response = requests.get(url, timeout=5).json()
        symbols = []
        for s in response['symbols']:
            if s['status'] == 'TRADING' and s['quoteAsset'] == 'USDT':
                clean_name = f"{s['baseAsset']}/USDT"
                symbols.append((clean_name, s['symbol']))
        symbols.sort(key=lambda x: x[0])
        return symbols
    except Exception:
        return [("Bitcoin (BTC/USDT)", "BTCUSDT"), ("Ethereum (ETH/USDT)", "ETHUSDT")]

with st.spinner("Connecting to Binance API Endpoints..."):
    binance_pairs = fetch_binance_symbols()

pair_dict = {display: ticker for display, ticker in binance_pairs}

# 3. INTERACTIVE SEARCH & SELECTOR INTERFACE
st.markdown("### 🔍 Asset Discovery Workspace")
selected_display = st.selectbox("Type or select a cryptocurrency pair to analyze:", options=list(pair_dict.keys()), index=0)
selected_ticker = pair_dict[selected_display]

# Manual Refresh Trigger Button for Presentations
if st.button("🔄 Force Refresh Market Data"):
    st.cache_data.clear()

# 4. DATA PIPELINE WITH AUTOMATIC BACKUP 
@st.cache_data(ttl=30)  # Lowered cache time to 30 seconds for immediate updates
def get_historical_data(symbol):
    # Strategy A: Attempt pulling via Yahoo Finance backup engine immediately for cloud stability
    try:
        clean_ticker = symbol.replace("USDT", "-USD")
        fallback_data = yf.Ticker(clean_ticker).history(period="3mo") # 3 months data is much faster to load
        if not fallback_data.empty:
            df = fallback_data.reset_index()
            df.rename(columns={'High': 'High', 'Low': 'Low', 'Close': 'Close'}, inplace=True)
            df['Date'] = df['Date'].dt.tz_localize(None)
            return df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    except Exception:
        pass

    # Strategy B: Fallback to Binance REST App Connection
    try:
        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1d&limit=100"
        data = requests.get(url, timeout=5).json()
        df = pd.DataFrame(data, columns=[
            'Open Time', 'Open', 'High', 'Low', 'Close', 'Volume',
            'Close Time', 'Quote Asset Volume', 'Number of Trades',
            'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore'
        ])
        df['Date'] = pd.to_datetime(df['Open Time'], unit='ms')
        df['Close'] = df['Close'].astype(float)
        df['High'] = df['High'].astype(float)
        df['Low'] = df['Low'].astype(float)
        return df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    except Exception:
        return pd.DataFrame()

# Run evaluation logic
try:
    df_history = get_historical_data(selected_ticker)
    
    if not df_history.empty:
        # 5. MATHEMATICAL COMPUTATIONS (ATH, ATL, TARGETS)
        current_price = df_history['Close'].iloc[-1]
        all_time_high = df_history['High'].max()
        all_time_low = df_history['Low'].min()
        
        moving_avg_50 = df_history['Close'].rolling(window=50).mean().iloc[-1]
        if pd.isna(moving_avg_50):
            moving_avg_50 = current_price
            
        entry_point = moving_avg_50 * 0.90
        exit_point = all_time_high * 0.95

        if exit_point <= current_price:
            exit_point = current_price * 1.15

        # Render Information Dashboards Matrix
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric(label="Live Exchange Price", value=f"${current_price:,.4f}")
        with m2:
            st.metric(label="Recent Dynamic High", value=f"${all_time_high:,.4f}")
        with m3:
            st.metric(label="Recent Dynamic Low", value=f"${all_time_low:,.4f}")

        st.markdown("---")

        # 6. RISK ZONING VERDICTS (TRAFFIC LIGHT)
        st.subheader("🚦 Actionable Position Blueprint")
        if current_price <= entry_point * 1.05:
            st.success(f"🟢 BUY ZONE ACTIVATED: Optimal entry target: **${entry_point:,.4f}**")
        elif current_price >= exit_point * 0.85:
            st.error(f"🔴 TAKE PROFIT / EXIT ZONE INBOUND: Target complete exit: **${exit_point:,.4f}**")
        else:
            st.warning(f"🟡 HOLD ZONE: Next Entry Floor: **${entry_point:,.4f}** | Next Exit Peak: **${exit_point:,.4f}**")

        # 7. CUSTOM INTERACTIVE PLOTLY ENGINE
        st.subheader(f"📈 {selected_display} Lifespan Valuation Map")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_history['Date'], y=df_history['Close'], mode='lines', name='Price Timeline', line=dict(color='#1f77b4', width=2)))
        fig.add_trace(go.Scatter(x=[df_history['Date'].iloc[0], df_history['Date'].iloc[-1]], y=[entry_point, entry_point], mode='lines', name='💡 Target Entry Point', line=dict(color='#2ca02c', width=2, dash='dash')))
        fig.add_trace(go.Scatter(x=[df_history['Date'].iloc[0], df_history['Date'].iloc[-1]], y=[exit_point, exit_point], mode='lines', name='🎯 Target Exit Point', line=dict(color='#d62728', width=2, dash='dash')))
        
        fig.update_layout(hovermode="x unified", xaxis_title="Timeline Calendar", yaxis_title="Asset Valuation (USDT)", template="plotly_dark", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("🔄 Fetching network response tickers... click the 'Force Refresh' button above if loading takes too long.")

except Exception as e:
    st.info("💡 Application initializing... Select a cryptocurrency from the drop-down matrix above to populate live analytics charts.")
