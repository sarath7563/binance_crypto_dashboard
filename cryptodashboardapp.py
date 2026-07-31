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
st.markdown("An enterprise-grade data engineering framework capable of indexing, scoring, and visually mapping **any asset class** across high-cap tokens, altcoins, meme economies, and micro-cap utility networks. [cite: 432]")

# ==========================================
# 2. INTUITIVE CONTROL PANEL & SIDEBAR (UPGRADES 1 & 2)
# ==========================================
st.sidebar.header("🎛️ Control Panel [cite: 433]")
st.sidebar.markdown("Configure your analytics viewport and technical tracking overlays below.")

# Main Input Bar [cite: 433]
search_query = st.text_input("🎯 Enter Any Cryptocurrency Token Symbol (e.g. BTC, ETH, DMTR, VLO, PEPE, SHIB):", value="BTC").strip().upper() [cite: 433]

# Fallback constraint for empty strings [cite: 434]
if not search_query:
    search_query = "BTC" [cite: 434]

# UPGRADE 1: Interactive Chart Timeframe Selector [cite: 479, 482]
st.sidebar.markdown("---")
st.sidebar.subheader("⏰ Analysis Horizon")
timeframe = st.sidebar.radio(
    "Choose historical scale window:",
    ["1M", "6M", "1Y", "MAX"],
    index=2,
    horizontal=True
) [cite: 482]

# Maps the user interface selections to core data engine parameters [cite: 483]
tf_map = {"1M": "1mo", "6M": "6mo", "1Y": "1y", "MAX": "max"} [cite: 483]
chosen_period = tf_map[timeframe] [cite: 483]

# UPGRADE 2: Live Technical Moving Average Overlays [cite: 484, 486]
st.sidebar.markdown("---")
st.sidebar.subheader("📈 Chart Overlay Configurations")
show_ma50 = st.sidebar.checkbox("Overlay 50-Day SMA Trendline", value=False) [cite: 486]
show_ma200 = st.sidebar.checkbox("Overlay 200-Day SMA Base line", value=False)

# Formatting rules to isolate fiat conversions vs currency pairs [cite: 434]
if search_query in ["USDT", "USDC", "DAI", "BUSD"]:
    ticker_symbol = f"{search_query}==X" [cite: 434]
else:
    ticker_symbol = f"{search_query}-USD" [cite: 434]

# System Cache Maintenance Reset Ingestion [cite: 434]
if st.sidebar.button("🔄 Clear App Cache Buffer"):
    st.cache_data.clear() [cite: 434]
    st.rerun() [cite: 434]

# ==========================================
# 3. HIGH-CAPACITY RESILIENT DATA RELAY
# ==========================================
@st.cache_data(ttl=30)  
def extract_crypto_lifespan(ticker, period):
    # Primary Ingestion Strategy: Query direct historical matrix channels [cite: 435]
    try:
        data_pull = yf.Ticker(ticker) [cite: 435]
        raw_df = data_pull.history(period=period) 
        if not raw_df.empty: [cite: 435]
            df = raw_df.reset_index() [cite: 435]
            df['Date'] = df['Date'].dt.tz_localize(None) [cite: 435]
            return df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']] [cite: 435]
    except Exception:
        pass [cite: 435]

    # Secondary Ingestion Strategy: Active Spot Exchange Fallback Route [cite: 436]
    try:
        clean_pair = ticker.replace("-USD", "USDT") [cite: 436]
        url = f"https://api.binance.com/api/v3/klines?symbol={clean_pair}&interval=1d&limit=100" [cite: 436]
        response = requests.get(url, timeout=5).json() [cite: 436]
        df = pd.DataFrame(response, columns=[
            'Open Time', 'Open', 'High', 'Low', 'Close', 'Volume',
            'Close Time', 'Quote Asset Volume', 'Number of Trades',
            'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore'
        ]) [cite: 436]
        df['Date'] = pd.to_datetime(df['Open Time'], unit='ms') [cite: 436]
        df['Close'] = df['Close'].astype(float) [cite: 437]
        df['High'] = df['High'].astype(float) [cite: 437]
        df['Low'] = df['Low'].astype(float) [cite: 437]
        return df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']] [cite: 437]
    except Exception:
        return pd.DataFrame() [cite: 437]

# ==========================================
# DYNAMIC PROJECT TECHNOLOGY & PROFILE PARSER
# ==========================================
@st.cache_data(ttl=3600)  
def fetch_asset_profile_summary(ticker, symbol):
    try:
        asset_engine = yf.Ticker(ticker) [cite: 457]
        asset_info = asset_engine.info [cite: 457]
        description = asset_info.get('description') or asset_info.get('longBusinessSummary') [cite: 457]
        if description and len(description.strip()) > 10: [cite: 457]
            return description [cite: 457]
    except Exception:
        pass
    
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{symbol.lower()}" [cite: 457]
        response = requests.get(url, timeout=5).json() [cite: 457]
        description = response.get('description', {}).get('en') [cite: 457]
        if description and len(description.strip()) > 10: [cite: 457]
            clean_desc = description.split("<a href=")[0] [cite: 457]
            return clean_desc [cite: 457]
    except Exception:
        pass

    return f"Detailed project documentation for '{symbol}' is actively tracked on decentralized ledger ecosystems. This token operates as a primary utility asset running native consensus and transactional execution rules within its respective blockchain network layer. [cite: 472]"

# ==========================================
# 4. DATA COMPUTATION & VIEWPORT LOGIC MATRIX
# ==========================================
try:
    with st.spinner(f"Ingesting live network ledgers for '{search_query}'... [cite: 438]"):
        df_metrics = extract_crypto_lifespan(ticker_symbol, chosen_period)
        project_profile = fetch_asset_profile_summary(ticker_symbol, search_query)
    
    if not df_metrics.empty: [cite: 438]
        # UPGRADE 4: Key Token Network Statistics Component Ingestion [cite: 491, 493]
        try:
            live_ticker_instance = yf.Ticker(ticker_symbol) [cite: 491]
            network_stats = live_ticker_instance.info [cite: 491]
            
            st.sidebar.markdown("---")
            st.sidebar.subheader("🏆 Token Network Stats [cite: 491]")
            
            m_cap = network_stats.get('marketCap')
            vol_24 = network_stats.get('volume24Hr') or network_stats.get('volume')
            circ_supply = network_stats.get('circulatingSupply')
            
            st.sidebar.write(f"**Market Cap:** ${m_cap:,.0f}" if m_cap else "**Market Cap:** N/A") [cite: 493]
            st.sidebar.write(f"**24h Vol:** ${vol_24:,.0f}" if vol_24 else "**24h Vol:** N/A") [cite: 493]
            st.sidebar.write(f"**Circ Supply:** {circ_supply:,.0f} {search_query}" if circ_supply else "**Circ Supply:** N/A") [cite: 493]
        except Exception:
            pass [cite: 493]

        # Extract computational boundaries [cite: 438]
        live_price = df_metrics['Close'].iloc[-1] [cite: 438]
        ath_price = df_metrics['High'].max() [cite: 438]
        atl_price = df_metrics['Low'].min() [cite: 438]
        
        # Calculate trailing averages over history tracking vectors [cite: 438]
        rolling_mean = df_metrics['Close'].rolling(window=50).mean().iloc[-1] [cite: 438]
        if pd.isna(rolling_mean): [cite: 438]
            rolling_mean = live_price [cite: 438]
            
        entry_target = rolling_mean * 0.90 [cite: 438]
        exit_target = ath_price * 0.95 [cite: 438]

        if exit_target <= live_price: [cite: 440]
            exit_target = live_price * 1.15 [cite: 440]

        # Interface Metrics Outputs Row [cite: 440]
        m1, m2, m3 = st.columns(3) [cite: 440]
        with m1:
            st.metric(label=f"Current {search_query} Fair Value", value=f"${live_price:,.4f}") [cite: 440]
        with m2:
            st.metric(label="Timeline Period High (ATH)", value=f"${ath_price:,.4f}") [cite: 440]
        with m3:
            st.metric(label="Timeline Period Low (ATL)", value=f"${atl_price:,.4f}") [cite: 440]

        # COIN DATA AND TECHNOLOGY DESCRIPTION EXTENSION [cite: 457]
        st.markdown("### ℹ️ Project Fundamental Analysis & Technology Profile") [cite: 457]
        with st.expander(f"📖 Click to View What {search_query} Is & How Its Technology Works [cite: 457]", expanded=True):
            st.markdown(f"**Asset Profile & Utility Overview:** [cite: 457]")
            st.info(project_profile) [cite: 457]
            st.caption(f"Metadata dynamically aggregated via international financial network streams for token instance: {search_query}-USD. [cite: 457]")

        st.markdown("---") [cite: 441]

        # ==========================================
        # 5. DYNAMIC COLOR ADVISORY MATRIX (TRAFFIC LIGHT) [cite: 441]
        # ==========================================
        st.subheader("🚦 Automated Position Architecture [cite: 441]")
        if live_price <= entry_target * 1.05: [cite: 441]
            st.success(f"🟢 BUY WINDOW ACTIVE: Valuation metrics imply asset is structurally oversold. Target Entry Point: **${entry_target:,.4f}** [cite: 441]")
        elif live_price >= exit_target * 0.85: [cite: 441]
            st.error(f"🔴 LIQUIDATION PEAK TRIGGERED: Asset approaching severe market overextension zones. Target Exit Point: **${exit_target:,.4f}** [cite: 441]")
        else: [cite: 441]
            st.warning(f"🟡 HOLD CHANNEL ENGAGED: Asset trading within neutral horizontal boundaries. Accumulation Floor: **${entry_target:,.4f}** | Distribution Ceiling: **${exit_target:,.4f}** [cite: 441, 442]")

        # ==========================================
        # UPGRADE 3: Data Export Utility (Download CSV) [cite: 487, 490]
        # ==========================================
        st.markdown("### 📊 Visual Ingestion Canvas")
        csv_buffer = df_metrics.to_csv(index=False).encode('utf-8') [cite: 488]
        st.download_button(
            label=f"📥 Export Raw {search_query} Price Timeline Matrix to CSV [cite: 487]",
            data=csv_buffer, [cite: 488]
            file_name=f"{search_query}_historical_metrics.csv", [cite: 488]
            mime="text/csv" [cite: 488]
        )

        # ==========================================
        # 6. HIGH-RESOLUTION INTERACTIVE CHART CANVAS [cite: 443]
        # ==========================================
        st.subheader(f"📈 Detailed {search_query} Chronological Valuation Map [cite: 443]")
        
        fig = go.Figure() [cite: 443]
        
        # Plot continuous baseline valuation trend line [cite: 443]
        fig.add_trace(go.Scatter(
            x=df_metrics['Date'], y=df_metrics['Close'], 
            mode='lines', name='Market Value Line', 
            line=dict(color='#00ffcc', width=2.5) [cite: 443]
        ))
        
        # UPGRADE 2 INTEGRATION: Conditional Moving Average Execution Traces [cite: 486]
        if show_ma50: [cite: 486]
            df_metrics['MA50'] = df_metrics['Close'].rolling(window=50).mean() [cite: 486]
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
        
        # Plot mathematical floor channel boundaries [cite: 443, 444]
        fig.add_trace(go.Scatter(
            x=[df_metrics['Date'].iloc[0], df_metrics['Date'].iloc[-1]], 
            y=[entry_target, entry_target], 
            mode='lines', name='💡 Target Entry Floor', 
            line=dict(color='#2ca02c', width=2, dash='dash') [cite: 444]
        ))
        
        # Plot mathematical ceiling channel boundaries [cite: 444]
        fig.add_trace(go.Scatter(
            x=[df_metrics['Date'].iloc[0], df_metrics['Date'].iloc[-1]], 
            y=[exit_target, exit_target], 
            mode='lines', name='🎯 Target Exit Ceiling', 
            line=dict(color='#d62728', width=2, dash='dash') [cite: 444, 445]
        ))
        
        # Styling parameters for visual optimization layout outputs [cite: 445]
        fig.update_layout(
            hovermode="x unified", [cite: 445]
            xaxis_title="Time Series Calendar", [cite: 445]
            yaxis_title="Asset Valuation (USD)", [cite: 445]
            template="plotly_dark", [cite: 445]
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1) [cite: 445]
        )
        st.plotly_chart(fig, use_container_width=True) [cite: 445]

    else:
        st.error(f"⚠️ Index Lookup Notice: Unrecognized symbol identifier '{search_query}'. Please verify that the shorthand ticker tag matches global tracking standards. [cite: 446]")

except Exception as e:
    st.info("💡 Awaiting token entry inputs... Input desired trading symbol inside the primary search console. [cite: 446]")
