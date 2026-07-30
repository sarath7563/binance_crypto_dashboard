import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
from datetime import datetime

# ==========================================
# 1. PAGE LAYOUT CONFIGURATION
# ==========================================
st.set_page_config(page_title="Binance Analytics Engine", page_icon="⚡", layout="wide")

st.title("⚡ Real-Time Binance Market Intelligence Dashboard")
st.markdown("An advanced college project utilizing the **Binance REST API** to track all active trading pairs, parse full historical lifespans, and generate math-driven structural entry/exit signals.")

# ==========================================
# 2. DYNAMIC BINANCE TICKER INGESTION PIPELINE
# ==========================================
@st.cache_data(ttl=600)  # Caches active symbols array for 10 minutes
def fetch_binance_symbols():
    try:
        url = "https://api.binance.com/api/v3/exchangeInfo"
        response = requests.get(url).json()
        
        # Filter explicitly for standard active pairs settled against USDT stablecoins
        symbols = []
        for s in response['symbols']:
            if s['status'] == 'TRADING' and s['quoteAsset'] == 'USDT':
                clean_name = f"{s['baseAsset']}/USDT"
                symbols.append((clean_name, s['symbol']))
        
        symbols.sort(key=lambda x: x[0])  # Sort directory alphabetically
        return symbols
    except Exception as e:
        # Emergency local safety fallback mapping if network times out
        return [("Bitcoin (BTC/USDT)", "BTCUSDT"), ("Ethereum (ETH/USDT)", "ETHUSDT")]

# Connect application framework to Binance node networks
with st.spinner("Connecting to Binance API Endpoints..."):
    binance_pairs = fetch_binance_symbols()

pair_dict = {display: ticker for display, ticker in binance_pairs}

# ==========================================
# 3. INTERACTIVE SEARCH & SELECTOR INTERFACE
# ==========================================
st.markdown("### 🔍 Asset Discovery Workspace")
selected_display = st.selectbox(
    "Type or select a cryptocurrency pair to analyze:",
    options=list(pair_dict.keys()),
    index=0
)
selected_ticker = pair_dict[selected_display]

# ==========================================
# 4. DATA REST COLLECTION DEPLOYMENT
# ==========================================
@st.cache_data(ttl=60)  # Hold data queries locally for 60 seconds
def get_historical_klines(symbol):
    # Fetch maximum chronological daily (1d) interval candlesticks from Binance infrastructure
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1d&limit=1000"
    data = requests.get(url).json()
    
    # Map out the structured data matrix into a functional Pandas DataFrame
    df = pd.DataFrame(data, columns=[
        'Open Time', 'Open', 'High', 'Low', 'Close', 'Volume',
        'Close Time', 'Quote Asset Volume', 'Number of Trades',
        'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore'
    ])
    
    # Format primitive string items into proper datetime matrices and floating point numbers
    df['Date'] = pd.to_datetime(df['Open Time'], unit='ms')
    df['Close'] = df['Close'].astype(float)
    df['High'] = df['High'].astype(float)
    df['Low'] = df['Low'].astype(float)
    
    return df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]

# Run evaluation logic
try:
    df_history = get_historical_klines(selected_ticker)
    
    if not df_history.empty:
        # ==========================================
        # 5. MATHEMATICAL COMPUTATIONS (ATH, ATL, TARGETS)
        # ==========================================
        current_price = df_history['Close'].iloc[-1]
        
        # Isolate absolute extreme indexes for ATH and ATL
        ath_row = df_history.loc[df_history['High'].idxmax()]
        atl_row = df_history.loc[df_history['Low'].idxmin()]
        
        all_time_high = ath_row['High']
        ath_date = ath_row['Date'].strftime('%Y-%m-%d')
        
        all_time_low = atl_row['Low']
        atl_date = atl_row['Date'].strftime('%Y-%m-%d')

        # Algorithmic Signal Calculations:
        # Moving average forms baseline. Accumulation (Entry) is set 10% under current rolling avg.
        moving_avg_50 = df_history['Close'].rolling(window=50).mean().iloc[-1]
        if pd.isna(moving_avg_50):
            moving_avg_50 = current_price
            
        entry_point = moving_avg_50 * 0.90
        exit_point = all_time_high * 0.95  # Target exit set near historic high range

        # Edge case protection: if asset is printing new absolute peaks
        if exit_point <= current_price:
            exit_point = current_price * 1.15

        # Render Information Dashboards Matrix
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric(label="Live Exchange Price", value=f"${current_price:,.4f}")
        with m2:
            st.metric(label="All-Time High (ATH)", value=f"${all_time_high:,.4f}", delta=f"Set on {ath_date}", delta_color="inverse")
        with m3:
            st.metric(label="All-Time Low (ATL)", value=f"${all_time_low:,.4f}", delta=f"Set on {atl_date}")

        st.markdown("---")

        # ==========================================
        # 6. RISK ZONING VERDICTS (TRAFFIC LIGHT)
        # ==========================================
        st.subheader("🚦 Actionable Position Blueprint")
        
        if current_price <= entry_point * 1.05:
            st.success(f"🟢 BUY ZONE ACTIVATED: Asset is structurally underpriced. Optimal entry target: **${entry_point:,.4f}**")
        elif current_price >= exit_point * 0.85:
            st.error(f"🔴 TAKE PROFIT / EXIT ZONE INBOUND: Valuation approaching resistance peaks. Target complete exit: **${exit_point:,.4f}**")
        else:
            st.warning(f"🟡 HOLD ZONE: Assets trading within balanced territory. Next Entry Floor: **${entry_point:,.4f}** | Next Exit Peak: **${exit_point:,.4f}**")

        # ==========================================
        # 7. CUSTOM INTERACTIVE PLOTLY ENGINE
        # ==========================================
        st.subheader(f"📈 {selected_display} Lifespan Valuation Map")
        
        fig = go.Figure()
        
        # Base Historical Timeline trace
        fig.add_trace(go.Scatter(
            x=df_history['Date'], y=df_history['Close'],
            mode='lines', name='Price Timeline', line=dict(color='#1f77b4', width=2)
        ))
        
        # Target Entry Horizontal Dash
        fig.add_trace(go.Scatter(
            x=[df_history['Date'].iloc[0], df_history['Date'].iloc[-1]],
            y=[entry_point, entry_point],
            mode='lines', name='💡 Target Entry Point',
            line=dict(color='#2ca02c', width=2, dash='dash')
        ))
        
        # Target Exit Horizontal Dash
        fig.add_trace(go.Scatter(
            x=[df_history['Date'].iloc[0], df_history['Date'].iloc[-1]],
            y=[exit_point, exit_point],
            mode='lines', name='🎯 Target Exit Point',
            line=dict(color='#d62728', width=2, dash='dash')
        ))
        
        # Aesthetic Styling parameters
        fig.update_layout(
            hovermode="x unified",
            xaxis_title="Timeline Calendar",
            yaxis_title="Asset Valuation (USDT)",
            template="plotly_dark",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.caption("The interface engine renders real-time tracking signals. Dashed green specifies buy triggers; dashed red specifies ultimate exit/profit liquidation floors.")

    else:
        st.warning("⚠️ Market Data Null: The asset requested holds unreadable metrics inside the network payload.")

except Exception as e:
    st.error(f"⚠️ API Pipeline Failure: Unable to compute historical metrics for this asset ticker symbol. Error: {str(e)}")