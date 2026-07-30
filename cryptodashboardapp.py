import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
import yfinance as yf

# 1. APPLICATION VIEWPORT SETUP
st.set_page_config(page_title="Universal Crypto Intelligence Engine", page_icon="⚡", layout="wide")

st.title("⚡ Universal Real-Time Crypto Risk Analytics Terminal")
st.markdown("An enterprise-grade data engineering framework capable of indexing, scoring, and visually mapping **any asset class** across high-cap tokens, altcoins, meme economies, and micro-cap utility networks.")

# ==========================================
# 2. INTUITIVE TEXT INPUT ENGINE (ANY COIN IN EXISTENCE)
# ==========================================
st.sidebar.header("🎛️ Control Panel")
st.sidebar.markdown("Type the standard trading abbreviation for any coin in the global ecosystem to extract live calculations.")

# Main Input Bar
search_query = st.text_input("🎯 Enter Any Cryptocurrency Token Symbol (e.g. BTC, ETH, DMTR, VLO, PEPE, SHIB):", value="BTC").strip().upper()

# Handle empty submission string edge cases
if not search_query:
    search_query = "BTC"

# Core Formatting Conversion Layer for Stablecoins vs Utility Tokens
if search_query in ["USDT", "USDC", "DAI", "BUSD"]:
    ticker_symbol = f"{search_query}==X"
else:
    ticker_symbol = f"{search_query}-USD"

# Hard Reset Tooling
if st.sidebar.button("🔄 Clear App Cache Buffer"):
    st.cache_data.clear()
    st.rerun()

# ==========================================
# 3. HIGH-CAPACITY RESILIENT DATA RELAY
# ==========================================
@st.cache_data(ttl=30)  
def extract_crypto_lifespan(ticker):
    # Primary Vector: Pull maximum historical matrix from open financial nodes
    try:
        data_pull = yf.Ticker(ticker)
        # 1-year timeline maximizes rapid rendering response on remote servers
        raw_df = data_pull.history(period="1y") 
        if not raw_df.empty:
            df = raw_df.reset_index()
            df['Date'] = df['Date'].dt.tz_localize(None)
            return df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    except Exception:
        pass

    # Secondary Vector: Direct fallback pipeline request to primary spot markets
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
        df['Close'] = df['Close'].astype(float)
        df['High'] = df['High'].astype(float)
        df['Low'] = df['Low'].astype(float)
        return df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    except Exception:
        return pd.DataFrame()

# ==========================================
# 4. DATA COMPUTATION LOGIC EDGE ROOM
# ==========================================
try:
    with st.spinner(f"Ingesting live network ledgers for '{search_query}'..."):
        df_metrics = extract_crypto_lifespan(ticker_symbol)
    
    if not df_metrics.empty:
        live_price = df_metrics['Close'].iloc[-1]
        ath_price = df_metrics['High'].max()
        atl_price = df_metrics['Low'].min()
        
        # Calculate trailing 50-day support boundaries
        rolling_mean = df_metrics['Close'].rolling(window=50).mean().iloc[-1]
        if pd.isna(rolling_mean):
            rolling_mean = live_price
            
        entry_target = rolling_mean * 0.90
        exit_target = ath_price * 0.95

        # Protection condition if an asset is violently surging out to new historical records
        if exit_target <= live_price:
            exit_target = live_price * 1.15

        # Interface Grid Layout Outputs
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric(label=f"Current {search_query} Fair Value", value=f"${live_price:,.4f}")
        with m2:
            st.metric(label="Timeline Period High (ATH)", value=f"${ath_price:,.4f}")
        with m3:
            st.metric(label="Timeline Period Low (ATL)", value=f"${atl_price:,.4f}")

        st.markdown("---")

        # ==========================================
        # 5. DYNAMIC COLOR ADVISORY MATRIX (TRAFFIC LIGHT)
        # ==========================================
        st.subheader("🚦 Automated Position Architecture")
        if live_price <= entry_target * 1.05:
            st.success(f"🟢 BUY WINDOW ACTIVE: Valuation metrics imply asset is structurally oversold. Target Entry Point: **${entry_target:,.4f}**")
        elif live_price >= exit_target * 0.85:
            st.error(f"🔴 LIQUIDATION PEAK TRIGGERED: Asset approaching severe market overextension zones. Target Exit Point: **${exit_target:,.4f}**")
        else:
            st.warning(f"🟡 HOLD CHANNEL ENGAGED: Asset trading within neutral horizontal boundaries. Accumulation Floor: **${entry_target:,.4f}** | Distribution Ceiling: **${exit_target:,.4f}**")

        # ==========================================
        # 6. HIGH-RESOLUTION INTERACTIVE CHART CANVAS
        # ==========================================
        st.subheader(f"📈 Detailed {search_query} Chronological Valuation Map")
        
        fig = go.Figure()
        
        # Plot continuous valuation line
        fig.add_trace(go.Scatter(
            x=df_metrics['Date'], y=df_metrics['Close'], 
            mode='lines', name='Market Value Line', 
            line=dict(color='#00ffcc', width=2.5)
        ))
        
        # Plot mathematical floor channel boundary
        fig.add_trace(go.Scatter(
            x=[df_metrics['Date'].iloc[0], df_metrics['Date'].iloc[-1]], 
            y=[entry_target, entry_target], 
            mode='lines', name='💡 Target Entry Floor', 
            line=dict(color='#2ca02c', width=2, dash='dash')
        ))
        
        # Plot mathematical ceiling channel boundary
        fig.add_trace(go.Scatter(
            x=[df_metrics['Date'].iloc[0], df_metrics['Date'].iloc[-1]], 
            y=[exit_target, exit_target], 
            mode='lines', name='🎯 Target Exit Ceiling', 
            line=dict(color='#d62728', width=2, dash='dash')
        ))
        
        # Styling configurations for professional visual output
        fig.update_layout(
            hovermode="x unified",
            xaxis_title="Time Series Calendar",
            yaxis_title="Asset Valuation (USD Equivalents)",
            template="plotly_dark",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.error(f"⚠️ Index Lookup Notice: Unrecognized symbol identifier '{search_query}'. Please verify that the shorthand ticker tag matches global tracking standards.")

except Exception as e:
    st.info("💡 Awaiting token entry inputs... Input desired trading symbol inside the primary search console.")
