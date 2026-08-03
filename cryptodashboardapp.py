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

st.title("⚡ Universal Crypto Risk Analytics & Predictive Terminal")
st.markdown("An advanced data engineering framework using machine learning trend projection to forecast price trajectories across thousands of global digital assets.")

# ==========================================
# 2. CONTROL PANEL & SIDEBAR SETUP
# ==========================================
st.sidebar.header("🎛️ Control Panel")
st.sidebar.markdown("Configure your analytics viewport and technical tracking overlays below.")

# Main Input Bar
search_query = st.text_input("🎯 Enter Any Cryptocurrency Token Symbol (e.g. BTC, ETH, DMTR, VLO, PEPE):", value="BTC").strip().upper()

if not search_query:
    search_query = "BTC"

# Timeframe Range Selector
st.sidebar.markdown("---")
st.sidebar.subheader("⏰ Analysis Horizon")
timeframe = st.sidebar.radio(
    "Choose historical scale window:",
    ["1 Week", "1 Month", "3 Month", "6 Month", "1 Year", "MAX"],
    index=4,  # Defaults to 1 Year
    horizontal=False
)

tf_map = {
    "1 Week": "5d",
    "1 Month": "1mo",
    "3 Month": "3mo",
    "6 Month": "6mo",
    "1 Year": "1y",
    "MAX": "max"
}
chosen_period = tf_map[timeframe]

# Technical Overlays
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
    return f"Detailed project documentation for '{symbol}' is actively tracked on decentralized ledger ecosystems."

# ==========================================
# 4. DATA COMPUTATION & MACHINE LEARNING PREDICTION
# ==========================================
try:
    with st.spinner(f"Ingesting live network ledgers for '{search_query}'..."):
        df_metrics = extract_crypto_lifespan(ticker_symbol, chosen_period)
        project_profile = fetch_asset_profile_summary(ticker_symbol, search_query)
    
    if not df_metrics.empty:
        # Core Calculations
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
        # Prepare historical index numbers for training array
        df_metrics['Day_Index'] = np.arange(len(df_metrics))
        X = df_metrics[['Day_Index']].values
        y = df_metrics['Close'].values
        
        # Fit Linear Regression Model
        model = LinearRegression()
        model.fit(X, y)
        
        # Predict the next 7 days out into the future
        future_indices = np.array([[len(df_metrics) + i] for i in range(1, 8)])
        future_predictions = model.predict(future_indices)
        
        # Create timestamps for the predicted 7 days
        last_date = df_metrics['Date'].iloc[-1]
        future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=7)
        
        # Check prediction direction slope
        is_increasing = future_predictions[-1] > live_price
        trend_status = "📈 INCREASE / UPWARD" if is_increasing else "📉 DECREASE / DOWNWARD"
        prediction_color = "#00ffcc" if is_increasing else "#ff3366"
        
        # Summary Row metrics
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric(label=f"Current {search_query} Value", value=f"${live_price:,.4f}", delta=f"{daily_change_pct:+.2f}%")
        with m2:
            st.metric(label="Suggested Entry (Floor)", value=f"${entry_target:,.4f}")
        with m3:
            st.metric(label="Suggested Exit (Ceiling)", value=f"${exit_target:,.4f}")

        st.markdown("---")

        # ==========================================
        # 5. SPLIT DISPLAY SCREEN
        # ==========================================
        col_graph, col_analysis = st.columns([2, 1])

        with col_graph:
            st.subheader(f"📈 Predictive Candlestick Map")
            fig = go.Figure()
            
            # Candlestick Bars
            fig.add_trace(go.Candlestick(
                x=df_metrics['Date'], open=df_metrics['Open'], high=df_metrics['High'],
                low=df_metrics['Low'], close=df_metrics['Close'], name='Price Candles',
                increasing_line_color='#00ffcc', decreasing_line_color='#ff3366'
            ))
            
            # Technical Overlays
            if show_ma50 and len(df_metrics) >= 50:
                df_metrics['MA50'] = df_metrics['Close'].rolling(window=50).mean()
                fig.add_trace(go.Scatter(x=df_metrics['Date'], y=df_metrics['MA50'], mode='lines', name='50-Day SMA', line=dict(color='#ffaa00', width=1.5)))
            
            # 🔮 UPGRADE: Plot 7-Day Machine Learning Prediction Track Line
            if show_predict:
                # Append last real price point to create a seamless connection line on graph
                connect_dates = [df_metrics['Date'].iloc[-1]] + list(future_dates)
                connect_prices = [live_price] + list(future_predictions)
                
                fig.add_trace(go.Scatter(
                    x=connect_dates, y=connect_prices, mode='lines+markers',
                    name='🔮 7-Day ML Forecast', line=dict(color='#ff00ff', width=2.5, dash='dash')
                ))
            
            # Horizontal Goal Bounds
            fig.add_trace(go.Scatter(
                x=[df_metrics['Date'].iloc[0], future_dates[-1]], y=[entry_target, entry_target], 
                mode='lines+text', name='Suggested Entry', text=["", f"  ENTRY: ${entry_target:,.2f}"],
                textposition="top right", textfont=dict(color="#2ca02c", size=11), line=dict(color='#2ca02c', width=2, dash='dash')
            ))
            fig.add_trace(go.Scatter(
                x=[df_metrics['Date'].iloc[0], future_dates[-1]], y=[exit_target, exit_target], 
                mode='lines+text', name='Suggested Exit', text=["", f"  EXIT: ${exit_target:,.2f}"],
                textposition="bottom right", textfont=dict(color="#d62728", size=11), line=dict(color='#d62728', width=2, dash='dash')
            ))
            
            fig.update_layout(
                hovermode="x unified", template="plotly_dark", xaxis_rangeslider_visible=False,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig, use_container_width=True)

        with col_analysis:
            st.subheader("🔮 Machine Learning Directional Report")
            
            # Custom Visual Alert Panel for the Prediction Direction
            st.markdown(
                f"<div style='background-color: rgba(255, 0, 255, 0.1); border: 2px solid #ff00ff; padding: 15px; border-radius: 10px; margin-bottom: 20px;'>"
                f"<h4 style='color: #ff00ff; margin-top:0;'>🤖 ML Trend Verdict:</h4>"
                f"<h2 style='color: {prediction_color}; margin: 5px 0;'>{trend_status}</h2>"
                f"<p style='color: #cccccc; font-size: 13px; margin-bottom:0;'>The linear regression model projects the 7-day terminal value around: <b>${future_predictions[-1]:,.4f}</b></p>"
                f"</div>", 
                unsafe_allow_code_html=True
            )
            
            st.markdown(f"""
            ### 📊 Statistical Metrics
            * **Current Volatility Spread:** `${df_metrics['High'].iloc[-1] - df_metrics['Low'].iloc[-1]:,.4f}`
            * **Distance to Window Peak:** `{((ath_price - live_price)/ath_price)*100:.2f}% down`
            * **Suggested Entry Zone:** `${entry_target:,.4f}`
            * **Suggested Exit Zone:** `${exit_target:,.4f}`
            """)
            
            csv_buffer = df_metrics.to_csv(index=False).encode('utf-8')
            st.download_button(label="📥 Download Historical Spreadsheet", data=csv_buffer, file_name=f"{search_query}_metrics.csv", mime="text/csv")

        st.markdown("---")
        st.markdown("### ℹ️ Project Fundamental Analysis & Technology Profile")
        with st.expander(f"📖 Click to View What {search_query} Is & How Its Technology Works", expanded=True):
            st.info(project_profile)

    else:
        st.error(f"⚠️ Index Lookup Notice: Unrecognized symbol identifier '{search_query}'.")

except Exception as e:
    st.info("💡 Awaiting token entry inputs... Input desired trading symbol inside the primary search console.")
