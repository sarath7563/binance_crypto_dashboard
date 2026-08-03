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
# 2. CONTROL PANEL & SIDEBAR SETUP
# ==========================================
st.sidebar.header("🎛️ Control Panel")
st.sidebar.markdown("Configure your analytics viewport and technical tracking overlays below.")

# Main Input Bar
search_query = st.text_input("🎯 Enter Any Cryptocurrency Token Symbol (e.g. BTC, ETH, DMTR, VLO, PEPE, SHIB):", value="BTC").strip().upper()

if not search_query:
    search_query = "BTC"

# NEW & EXPANDED: Full Interactive Timeframe Range Selector
st.sidebar.markdown("---")
st.sidebar.subheader("⏰ Analysis Horizon")
timeframe = st.sidebar.radio(
    "Choose historical scale window:",
    ["1 Day", "1 Week", "1 Month", "3 Month", "6 Month", "1 Year", "MAX"],
    index=5,  # Defaults to 1 Year out of the box
    horizontal=False
)

# Maps the user interface selections perfectly to core financial data parameters
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
        # Fetch data based on the dynamic timeline choice
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
            st.sidebar.write(f"**Market Cap:** ${m_cap:,.0f}" if m_cap else "**Market Cap:** N/A")
            st.sidebar.write(f"**24h Vol:** ${vol_24:,.0f}" if vol_24 else "**24h Vol:** N/A")
            st.sidebar.write(f"**Circ Supply:** {circ_supply:,.0f} {search_query}" if circ_supply else "**Circ Supply:** N/A")
        except Exception:
            pass

        # Calculations
        live_price = df_metrics['Close'].iloc[-1]
        open_price = df_metrics['Open'].iloc[-1]
        ath_price = df_metrics['High'].max()
        atl_price = df_metrics['Low'].min()
        
        # Calculate trailing 50-day support averages
        rolling_mean = df_metrics['Close'].rolling(window=50).mean().iloc[-1]
        # Safety Fail-Safe: If the user selects a tiny period like '1 Day' or '1 Week', 
        # rolling_mean turns into NaN due to lack of historical rows. We cleanly catch it here:
        if pd.isna(rolling_mean):
            rolling_mean = live_price
            
        entry_target = rolling_mean * 0.90
        exit_target = ath_price * 0.95

        if exit_target <= live_price:
            exit_target = live_price * 1.15

        # Past 24h Change Logic
        daily_change_usd = live_price - open_price
        daily_change_pct = (daily_change_usd / open_price) * 100

        # Primary Overview Rows
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric(label=f"Current {search_query} Value", value=f"${live_price:,.4f}", delta=f"{daily_change_pct:+.2f}% (Selected View)")
        with m2:
            st.metric(label="View Window High", value=f"${ath_price:,.4f}")
        with m3:
            st.metric(label="View Window Low", value=f"${atl_price:,.4f}")

        st.markdown("---")

        # ==========================================
        # 5. DUAL LAYOUT: REAL GRAPH + DAY-TO-DAY ANALYSIS
        # ==========================================
        col_graph, col_analysis = st.columns([2, 1])

        with col_graph:
            st.subheader(f"📈 Pro-Style {search_query} Candlestick Chart Map")
            
            fig = go.Figure()
            
            # Candlestick Data Layers
            fig.add_trace(go.Candlestick(
                x=df_metrics['Date'],
                open=df_metrics['Open'],
                high=df_metrics['High'],
                low=df_metrics['Low'],
                close=df_metrics['Close'],
                name='Price Bars',
                increasing_line_color='#00ffcc', 
                decreasing_line_color='#ff3366'
            ))
            
            # Conditional Trendlines
            if show_ma50 and len(df_metrics) >= 50:
                df_metrics['MA50'] = df_metrics['Close'].rolling(window=50).mean()
                fig.add_trace(go.Scatter(x=df_metrics['Date'], y=df_metrics['MA50'], mode='lines', name='50-Day SMA', line=dict(color='#ffaa00', width=1.5)))
                
            if show_ma200 and len(df_metrics) >= 200:
                df_metrics['MA200'] = df_metrics['Close'].rolling(window=200).mean()
                fig.add_trace(go.Scatter(x=df_metrics['Date'], y=df_metrics['MA200'], mode='lines', name='200-Day SMA', line=dict(color='#ff00ff', width=1.5, dash='dot')))
            
            # Strategy Target Reference Channels
            fig.add_trace(go.Scatter(x=[df_metrics['Date'].iloc[0], df_metrics['Date'].iloc[-1]], y=[entry_target, entry_target], mode='lines', name='💡 Target Entry Floor', line=dict(color='#2ca02c', width=2, dash='dash')))
            fig.add_trace(go.Scatter(x=[df_metrics['Date'].iloc[0], df_metrics['Date'].iloc[-1]], y=[exit_target, exit_target], mode='lines', name='🎯 Target Exit Ceiling', line=dict(color='#d62728', width=2, dash='dash')))
            
            fig.update_layout(
                hovermode="x unified",
                xaxis_title="Timeline Calendar",
                yaxis_title="Price (USD)",
                template="plotly_dark",
                xaxis_rangeslider_visible=False,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig, use_container_width=True)

        with col_analysis:
            st.subheader("📋 Day-to-Day Technical Analysis")
            
            # Traffic Light Banner Alerts
            if live_price <= entry_target * 1.05:
                st.success(f"🟢 BUY SIGNAL: Structurally Undersold")
            elif live_price >= exit_target * 0.85:
                st.error(f"🔴 TAKE PROFIT: Approaching Resistance")
            else:
                st.warning(f"🟡 HOLD STATUS: Balanced Range Trading")
            
            # Automated Metrics Report Card
            st.markdown(f"""
            ### 🔍 Core Target Blueprint
            * **Suggested Entry Point (Buy Zone):** `${entry_target:,.4f}`
            * **Suggested Exit Point (Sell Target):** `${exit_target:,.4f}`
            
            ---
            ### 📉 Current Horizon Insights
            * **Current price deviation vs Base Line:** `{((live_price - rolling_mean)/rolling_mean)*100:.2f}%`
            * **Distance to Window High:** `{((ath_price - live_price)/ath_price)*100:.2f}% down from peak`
            * **Current Volatility Spread:** `${df_metrics['High'].iloc[-1] - df_metrics['Low'].iloc[-1]:,.4f}`
            """)
            
            csv_buffer = df_metrics.to_csv(index=False).encode('utf-8')
            st.download_button(label="📥 Download Data Spreadsheet", data=csv_buffer, file_name=f"{search_query}_historical_metrics.csv", mime="text/csv")

        # Project Info Section
        st.markdown("---")
        st.markdown("### ℹ️ Project Fundamental Analysis & Technology Profile")
        with st.expander(f"📖 Click to View What {search_query} Is & How Its Technology Works", expanded=True):
            st.info(project_profile)

    else:
        st.error(f"⚠️ Index Lookup Notice: Unrecognized symbol identifier '{search_query}'. Please verify standard abbreviations.")

except Exception as e:
    st.info("💡 Awaiting token entry inputs... Input desired trading symbol inside the primary search console.")
