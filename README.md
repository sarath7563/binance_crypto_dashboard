A real-time cryptocurrency analytics terminal that runs data metrics, calculates market risk zones, and dynamic technology parsers.# ⚡ Universal Real-Time Crypto Analytics & Risk Terminal

This is a live, smart cryptocurrency dashboard website built entirely in Python. 

Instead of just showing a basic price line, this terminal acts like an automated financial advisor. It instantly calculates whether a coin is currently a good value or too expensive based on market history, while simultaneously reading the web to explain exactly what the coin's project does and the technology behind it.

🔗 **Click here to open the live app:** [Launch Live Crypto Terminal](https://binancecryptodashboard-7dkgvoqywtevrbwjkbp6po.streamlit.app/)

---

## 🎯 What it Solves (The Problem)
When people want to look into or invest in a cryptocurrency, they run into a major issue: **information fragmentation**. 
* You have to look at one website for confusing price charts and mathematical trendlines.
* You have to search completely different websites or read long technical whitepapers just to understand what the coin actually does.
* Most apps that try to load lists of thousands of coins end up lagging, freezing, or hitting API limits.

**The Solution:** This unified dashboard handles both the math and the meaning on a single screen. By using an **On-Demand Search Box**, the app handles over 5,000+ coins smoothly without slowing down or crashing your browser.

---

## 🚀 Interactive Features You Can Try Live!

* **Global Search Box:** Type in the shorthand abbreviation for ANY crypto token in existence (e.g., BTC, ETH, DMTR, VLO, PEPE) and hit Enter to pull its live metrics immediately.
* **Smart Traffic Light Advisory:** The app runs a 50-day moving average calculation behind the scenes and dynamically changes colors to give you instant feedback:
  * 🟢 **Green (Buy Window):** The coin is structurally underpriced (trading at a relative discount).
  * 🟡 **Yellow (Hold Channel):** The coin is trading in its normal, stable price range.
  * 🔴 **Red (Liquidation Peak):** The coin is overheated and too expensive to buy right now.
* **Tech & Project Summary Expander:** A dynamic text breakdown that automatically fetches and prints exactly what the coin is made for and its real-world utility.
* **Interactive Timeframe Buttons:** Toggle the chart timeline easily between **1 Month, 6 Months, 1 Year, or Max Lifespan** to see different growth perspectives.
* **Technical Trendline Checkboxes:** Check the boxes in the left sidebar to overlay a **50-day or 200-day trendline** right onto the graph.
* **One-Click CSV Spreadsheet Export:** Click the download button to instantly save the raw daily price matrix history straight to your laptop as an Excel-compatible spreadsheet.

---

## 🛠️ The Tech Stack (What I Used)
* **Language:** Python 🐍
* **Web App Interface:** Streamlit (For building the clean frontend website layout)
* **Data Processing:** Pandas (For running the rolling mathematical averages)
* **Interactive Graphs:** Plotly Graph Objects (For drawing smooth, hoverable charts)
* **Live Network Connections:** Yahoo Finance API & Binance REST Architecture (For fetching live global token data)

---

## 💻 How to Run It Locally on Your Computer

If you want to clone this code and run it on your own machine, follow these three simple steps:

1. **Clone this repository folder:**
   ```bash
   git clone [https://github.com/sarath7563/binance_crypto_dashboard.git](https://github.com/sarath7563/binance_crypto_dashboard.git)
   cd binance_crypto_dashboard
