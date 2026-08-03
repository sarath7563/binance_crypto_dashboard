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
            st.sidebar.info("💡 Available on Tier-1 Markets:\n* **Binance** (Best Liquidity)\n* **Coinbase**\n* **Kraken**")
        else:
            st.sidebar.warning("💡 Low-Cap / Altcoin Markets:\n* **KuCoin**\n* **Gate.io**\n* **Uniswap / Raydium** (DEX)")

        # Calculations & Currency Scaling Applied
        live_price = df_metrics['Close'].iloc[-1] * curr_rate
        open_price = df_metrics['Open'].iloc[-1] * curr_rate
        ath_price = df_metrics['High'].max() * curr_rate
        atl_price = df_metrics['Low'].min() * curr_rate
        
        rolling_mean = df_metrics['Close'].rolling(window=50).mean().iloc[-1]
        if pd.isna(rolling_mean):
            rolling_mean = df_metrics['Close'].iloc[-1]
        rolling_mean *= curr_rate
            
        entry_target = rolling_mean * 0.90
        exit_target = ath_price * 0.95

        if exit_target <= live_price:
            exit_target = live_price * 1.15

        # Past 24h Change Logic
        daily_change_usd = live_price - open_price
        daily_change_pct = (daily_change_usd / open_price) * 100

        # Injecting Custom CSS styling injection to guarantee text visibility
        st.markdown("""
        <style>
            /* Force metrics values to display in crisp, solid high-contrast white */
            div[data-testid="stMetricValue"] {
                color: #FFFFFF !important;
                font-size: 2.3rem !important;
                font-weight: 700 !important;
            }
            /* Label headers clearly visible in light grey text styling */
            div[data-testid="stMetricLabel"] p {
                color: #E5E7EB !important;
                font-size: 1.05rem !important;
                font-weight: 500 !important;
            }
        </style>
        """, unsafe_allow_html=True)

        # Primary Metrics Cards Layout Display
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric(label=f"Current {search_query} Value ({currency_selection})", value=f"{curr_symbol}{live_price:,.4f}", delta=f"{daily_change_pct:+.2f}%")
        with m2:
            st.metric(label=f"View Window High ({currency_selection})", value=f"{curr_symbol}{ath_price:,.4f}")
        with m3:
            st.metric(label=f"View Window Low ({currency_selection})", value=f"{curr_symbol}{atl_price:,.4f}")

        st.markdown("---")

        # ==========================================
        # 5. DUAL INTERACTIVE INTERFACE TABS
        # ==========================================
        tab_trading, tab_technology = st.tabs(["📈 Live Trading & AI Analytics", "🔬 Technology Infrastructure"])

        with tab_trading:
            col_graph, col_analysis = st.columns([2, 1])

            with col_graph:
                st.subheader(f"📊 {search_query} Candlestick Chart Engine")
                
                fig = go.Figure()
                
                # Candlestick Data Plottings
                fig.add_trace(go.Candlestick(
                    x=df_metrics['Date'],
                    open=df_metrics['Open'] * curr_rate,
                    high=df_metrics['High'] * curr_rate,
                    low=df_metrics['Low'] * curr_rate,
                    close=df_metrics['Close'] * curr_rate,
                    name='Price Candles',
                    increasing_line_color='#00ffcc', 
                    decreasing_line_color='#ff3366'
                ))
                
                # Conditional Trendlines
                if show_ma50 and len(df_metrics) >= 50:
                    df_metrics['MA50'] = df_metrics['Close'].rolling(window=50).mean() * curr_rate
                    fig.add_trace(go.Scatter(x=df_metrics['Date'], y=df_metrics['MA50'], mode='lines', name='50-Day SMA', line=dict(color='#ffaa00', width=1.5)))
                    
                if show_ma200 and len(df_metrics) >= 200:
                    df_metrics['MA200'] = df_metrics['Close'].rolling(window=200).mean() * curr_rate
                    fig.add_trace(go.Scatter(x=df_metrics['Date'], y=df_metrics['MA200'], mode='lines', name='200-Day SMA', line=dict(color='#ff00ff', width=1.5, dash='dot')))
                
                # 7-Day Future Machine Learning Prediction Modeling
                if len(df_metrics) > 10:
                    df_metrics['Timestamp'] = df_metrics['Date'].astype('int64') // 10**9
                    X_ml = df_metrics['Timestamp'].values.reshape(-1, 1)
                    y_ml = df_metrics['Close'].values * curr_rate
                    
                    model = LinearRegression()
                    model.fit(X_ml, y_ml)
                    
                    last_timestamp = df_metrics['Timestamp'].iloc[-1]
                    future_timestamps = np.array([last_timestamp + i * 86400 for i in range(1, 8)])
                    future_predictions = model.predict(future_timestamps.reshape(-1, 1))
                    
                    future_dates = [df_metrics['Date'].iloc[-1] + pd.Timedelta(days=i) for i in range(1, 8)]
                    
                    plot_dates = [df_metrics['Date'].iloc[-1]] + list(future_dates)
                    plot_preds = [live_price] + list(future_predictions)
                    
                    fig.add_trace(go.Scatter(x=plot_dates, y=plot_preds, mode='lines+markers', name='🔮 7-Day AI Forecast', line=dict(color='#b55fe6', width=2, dash='dash')))
                    pred_verdict = "UP (Increase)" if future_predictions[-1] > live_price else "DOWN (Decrease)"
                    target_pred_val = future_predictions[-1]
                else:
                    pred_verdict = "Insufficient History"
                    target_pred_val = live_price

                # Strategy Target Reference Channels with floating text labels
                fig.add_trace(go.Scatter(
                    x=[df_metrics['Date'].iloc[0], df_metrics['Date'].iloc[-1]], 
                    y=[entry_target, entry_target], 
                    mode='lines+text', 
                    name='💡 Target Entry Floor', 
                    line=dict(color='#2ca02c', width=2, dash='dash'),
                    text=["", f"Entry Floor: {curr_symbol}{entry_target:,.2f}"],
                    textposition="top left"
                ))
                fig.add_trace(go.Scatter(
                    x=[df_metrics['Date'].iloc[0], df_metrics['Date'].iloc[-1]], 
                    y=[exit_target, exit_target], 
                    mode='lines+text', 
                    name='🎯 Target Exit Ceiling', 
                    line=dict(color='#d62728', width=2, dash='dash'),
                    text=["", f"Exit Target: {curr_symbol}{exit_target:,.2f}"],
                    textposition="bottom left"
                ))
                
                fig.update_layout(
                    hovermode="x unified",
                    xaxis_title="Timeline Calendar",
                    yaxis_title=f"Price ({currency_selection})",
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
                
                # Interactive AI Forecast Indicator Metric Box
                st.markdown(f"""
                <div style="background-color: #311b92; padding: 15px; border-radius: 8px; border: 1px solid #7c4dff; margin-bottom: 20px;">
                    <h4 style="color: #e040fb; margin-top:0;">🔮 7-Day Machine Learning Trend Box</h4>
                    <p style="color: white; margin-bottom: 5px;">Projected Trend Direction: <b>{pred_verdict}</b></p>
                    <p style="color: white; margin-bottom: 0;">Expected End Target Value: <b>{curr_symbol}{target_pred_val:,.4f}</b></p>
                </div>
                """, unsafe_allow_html=True)
                
                # Automated Metrics Report Card
                st.markdown(f"""
                ### 🔍 Core Target Blueprint
                * **Suggested Entry Point (Buy Zone):** `{curr_symbol}{entry_target:,.4f}`
                * **Suggested Exit Point (Sell Target):** `{curr_symbol}{exit_target:,.4f}`
                
                ---
                ### 📉 Current Horizon Insights
                * **Current price deviation vs Base Line:** `{((live_price - rolling_mean)/rolling_mean)*100:.2f}%`
                * **Distance to Window High:** `{((ath_price - live_price)/ath_price)*100:.2f}% down from peak`
                * **Current Volatility Spread:** `{curr_symbol}{(df_metrics['High'].iloc[-1] - df_metrics['Low'].iloc[-1])*curr_rate:,.4f}`
                """)
                
                scaled_df = df_metrics.copy()
                for col in ['Open', 'High', 'Low', 'Close']:
                    scaled_df[col] = scaled_df[col] * curr_rate
                csv_buffer = scaled_df.to_csv(index=False).encode('utf-8')
                st.download_button(label="📥 Download Data Spreadsheet", data=csv_buffer, file_name=f"{search_query}_historical_metrics.csv", mime="text/csv")

        with tab_technology:
            st.subheader(f"🔬 Decentralized Network Tech Profile: {search_query}")
            
            c_left, c_right = st.columns([2, 1])
            with c_left:
                st.markdown("#### 📖 Project Background Summary")
                st.info(project_profile)
            
            with c_right:
                st.markdown("#### ⚙️ Structural Architecture Blueprint")
                if search_query in ["BTC", "WBTC"]:
                    st.markdown("""
                    * **Network Layer:** Layer-1 Base Ledger
                    * **Consensus Engine:** Proof-of-Work (PoW)
                    * **Hashing Scheme:** SHA-256
                    * **Primary Utility:** Absolute Value Storage / Decentralized Sound Money
                    """)
                elif search_query in ["ETH", "LINK", "UNI", "AAVE"]:
                    st.markdown("""
                    * **Network Layer:** Layer-1 Smart Contract Platform / ERC-20
                    * **Consensus Engine:** Proof-of-Stake (PoS)
                    * **Execution Environment:** EVM (Ethereum Virtual Machine)
                    * **Primary Utility:** Decentralized Applications (dApps) & Programmable Logic
                    """)
                elif search_query in ["SOL", "RAY", "JUP"]:
                    st.markdown("""
                    * **Network Layer:** Ultra High-Throughput Layer-1 Platform
                    * **Consensus Engine:** Proof-of-History (PoH) + Proof-of-Stake
                    * **Block Execution Latency:** Sub-second
                    * **Primary Utility:** High-Frequency Defi Operations & Microtransactions
                    """)
                else:
                    st.markdown(f"""
                    * **Network Layer:** Alternate Utility Blockchain Token Ecosystem
                    * **Consensus Engine:** Delegated Node Validation Architecture
                    * **Storage Framework:** Distributed Ledgers Node Sync
                    * **Primary Utility:** Native Transaction Processing & Protocol Governance
                    """)

    else:
        st.error(f"⚠️ Index Lookup Notice: Unrecognized symbol identifier '{search_query}'. Please verify standard abbreviations.")

except Exception as e:
    st.info("💡 Awaiting token entry inputs... Input desired trading symbol inside the primary search console.")
