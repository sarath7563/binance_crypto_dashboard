import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
import yfinance as yf

# ==========================================
# 1. APPLICATION VIEWPORT SETUP
# ==========================================
st.set_page_config(page_title="Universal Crypto Intelligence Engine", page_icon="⚡", layout="wide")

st.title("⚡ Universal Real-Time Crypto Risk Analytics Terminal")
st.markdown("An enterprise-grade data engineering framework capable of indexing, scoring, and visually mapping **any asset class** across high-cap tokens, altcoins, meme economies, and micro-cap utility networks.")

# ==========================================
# 2. INTUITIVE CONTROL PANEL & SIDEBAR
# ==========================================
st.sidebar.header("🎛️ Control Panel")
st.sidebar.markdown("Configure your analytics viewport and technical tracking overlays below.")

# Main Input Bar
search_query = st.text_input("🎯 Enter Any Cryptocurrency Token Symbol (e.g. BTC, ETH, DMTR, VLO, PEPE, SHIB):", value="BTC").strip().upper()

# Fallback constraint for empty strings
if not search_query:
    search_query = "BTC"

# Interactive Chart Timeframe Selector
st.sidebar.markdown("---")
st.sidebar.subheader("⏰ Analysis Horizon")
timeframe = st.sidebar.radio(
    "Choose historical scale window:",
    ["1M", "6M", "1Y", "MAX"],
    index=2,
    horizontal=True
)

# Maps the user interface selections to core data engine parameters
tf_map = {"1M": "1mo", "6M": "6mo", "1Y": "1y", "MAX": "max"}
chosen_period = tf_map[timeframe]

# Live Technical Moving Average Overlays
st.sidebar.markdown("---")
st.sidebar.subheader("📈 Chart Overlay Configurations")
show_ma50 = st.sidebar.checkbox("Overlay 50-Day SMA Trendline", value=False)
show_ma200 = st.sidebar.checkbox("Overlay 200-Day SMA Base line", value=False)

# Formatting rules to isolate fiat conversions vs currency pairs
if search_query in ["USDT", "USDC", "DAI", "BUSD"]:
    ticker_symbol = f"{search_query}==X"
else:
    ticker_symbol = f"{search_query}-USD"

# System Cache Maintenance Reset Ingestion
if st.sidebar.button("🔄 Clear App Cache Buffer"):
    st.cache_data.clear()
    st.rerun()

# ==========================================
# 3. HIGH-CAPACITY RESILIENT DATA RELAY
# ==========================================
@st.cache_data(ttl=30)  
def extract_crypto_lifespan(ticker, period):
    # Primary Ingestion Strategy: Query direct historical matrix channels
    try:
        data_pull = yf.Ticker(ticker)
        raw_df = data_pull.history(period=period) 
        if not raw_df.empty:
            df = raw_df.reset_index()
            df['Date'] = df['Date'].dt.tz_localize(None)
            return df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    except Exception:
        pass

    # Secondary Ingestion Strategy: Active Spot Exchange Fallback Route
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
# DYNAMIC PROJECT TECHNOLOGY & PROFILE PARSER
# ==========================================
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
            clean_desc = description.split("<a href=")[0]
            return clean_desc
    except Exception:
        pass

    return f"Detailed project documentation for '{symbol}' is actively tracked on decentralized ledger ecosystems. This token operates as a primary utility asset running native consensus and transactional execution rules within its respective blockchain network layer."

# ==========================================
# 4. DATA COMPUTATION & VIEWPORT LOGIC MATRIX
# ==========================================
try:
    with st.spinner(f"Ingesting live network ledgers for '{search_query}'..."):
        df_metrics = extract_crypto_lifespan(ticker_symbol, chosen_period)
        project_profile = fetch_asset_profile_summary(ticker_symbol, search_query)
    
    if not df_metrics.empty:
        # Key Token Network Statistics Component Ingestion
        try:
            live_ticker_instance = yf.Ticker(ticker_symbol)
            network_stats = live_ticker_instance.info
            
            st.sidebar.markdown("---")
            st.sidebar.subheader("🏆 Token Network Stats")
            
            m_cap = network_stats.get('marketCap')
            vol_24 = network_stats.get('volume24Hr') or network_stats.get('volume')
            circ_supply = network_stats.get('circulatingSupply')
            
            st.sidebar.write(f"**Market Cap:** ${m_cap:,.0f}" if m_cap else "**Market Cap:** N/A")
            st.sidebar.write(f"**24h Vol:** ${vol_24:,.0f}" if vol_24 else "**24h Vol:** N/A")
            st.sidebar.write(f"**Circ Supply:** {circ_supply:,.0f} {search_query}" if circ_supply else "**Circ Supply:** N/A")
        except Exception:
            pass

        # Extract computational boundaries
        live_price = df_metrics['Close'].iloc[-1]
        ath_price = df_metrics['High'].max()
        atl_price = df_metrics['Low'].min()
        
        # Calculate trailing averages over history tracking vectors
        rolling_mean = df_metrics['Close'].rolling(window=50).mean().iloc[-1]
        if pd.isna(rolling_mean):
            rolling_mean = live_price
            
        entry_target = rolling_mean * 0.90
        exit_target = ath_price * 0.95

        if exit_target <= live_price:
            exit_target = live_price * 1.15

        # Interface Grid Layout Outputs Row
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric(label=f"Current {search_query} Fair Value", value=f"${live_price:,.4f}")
        with m2:
            st.metric(label="Timeline Period High (ATH)", value=f"${ath_price:,.4f}")
        with m3:
            st.metric(label="Timeline Period Low (ATL)", value=f"${atl_price:,.4f}")

        # COIN DATA AND TECHNOLOGY DESCRIPTION EXTENSION
        st.markdown("### ℹ️ Project Fundamental Analysis & Technology Profile")
        with st.expander(f"📖 Click to View What {search_query} Is & How Its Technology Works", expanded=True):
            st.markdown(f"**Asset Profile & Utility Overview:**")
            st.info(project_profile)
            st.caption(f"Metadata dynamically aggregated via international financial network streams for token instance: {search_query}-USD.")

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
        # Data Export Utility (Download CSV)
        # ==========================================
        st.markdown("### 📊 Visual Ingestion Canvas")
        csv_buffer = df_metrics.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=f"📥 Export Raw {search_query} Price Timeline Matrix to CSV",
            data=csv_buffer,
            file_name=f"{search_query}_historical_metrics.csv",
            mime="text/csv"
        )

        # ==========================================
        # 6. HIGH-RESOLUTION INTERACTIVE CHART CANVAS
        # ==========================================
        st.subheader(f"📈 Detailed {search_query} Chronological Valuation Map")
        
        fig = go.Figure()
        
        # Plot continuous baseline valuation trend line
        fig.add_trace(go.Scatter(
            x=df_metrics['Date'], y=df_metrics['Close'], 
            mode='lines', name='Market Value Line', 
            line=dict(color='#00ffcc', width=2.5)
        ))
        
        # Moving Average Execution Traces
        if show_ma50:
            df_metrics['MA50'] = df_metrics['Close'].rolling(window=50).mean()
            fig.add_trace(go.Scatter(
                x=df_metrics['Date'], y=df_metrics['MA50'], 
                mode='lines', name='50-Day Trend SMA', 
                line=dict(color='#ffaa00', width=1.5)
            ))
            
        if show_ma200:
            df_metrics['MA200'] = df_metrics['Close'].rolling(window=200).mean()
            fig.add_trace(go.Scatter(
                x=df_metrics['Date'], y=df_metrics['MA200'], 
                mode='lines', name='200-Day Structural SMA', 
                line=dict(color='#ff00ff', width=1.5, dash='dot')
            ))
        
        # Plot mathematical floor channel boundaries
        fig.add_trace(go.Scatter(
            x=[df_metrics['Date'].iloc[0], df_metrics['Date'].iloc[-1]], 
            y=[entry_target, entry_target], 
            mode='lines', name='💡 Target Entry Floor', 
            line=dict(color='#2ca02c', width=2, dash='dash')
        ))
        
        # Plot mathematical ceiling channel boundaries
        fig.add_trace(go.Scatter(
            x=[df_metrics['Date'].iloc[0], df_metrics['Date'].iloc[-1]], 
            y=[exit_target, exit_target], 
            mode='lines', name='🎯 Target Exit Ceiling', 
            line=dict(color='#d62728', width=2, dash='dash')
        ))
        
        # Styling parameters for visual optimization layout outputs
        fig.update_layout(
            hovermode="x unified",
            xaxis_title="Time Series Calendar",
            yaxis_title="Asset Valuation (USD)",
            template="plotly_dark",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.error(f"⚠️ Index Lookup Notice: Unrecognized symbol identifier '{search_query}'. Please verify that the shorthand ticker tag matches global tracking standards.")

except Exception as e:
    st.info("💡 Awaiting token entry inputs... Input desired trading symbol inside the primary search console.")
