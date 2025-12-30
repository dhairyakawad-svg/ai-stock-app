import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="AI Stock Analyzer", layout="centered")

st.title("📊 AI Stock Analyzer")
st.write("Educational stock analysis tool (Not financial advice)")

# ---------------- SIMPLE NAME → TICKER MAP ---------------- #
NAME_TO_TICKER = {
    "apple": "AAPL",
    "tesla": "TSLA",
    "google": "GOOGL",
    "amazon": "AMZN",
    "microsoft": "MSFT",
    "mrf": "MRF.NS",
    "reliance": "RELIANCE.NS",
    "tcs": "TCS.NS",
    "infosys": "INFY.NS",
}

user_input = st.text_input(
    "Enter company name or ticker (Apple, MRF, Reliance, AAPL, MRF.NS)"
).strip().lower()

ticker = None
if user_input:
    ticker = NAME_TO_TICKER.get(user_input, user_input.upper())

# ---------------- TECHNICAL ANALYSIS ---------------- #
def calculate_rsi(data, period=14):
    delta = data.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def technical_signal(rsi):
    if rsi < 30:
        return "BUY", "RSI indicates oversold conditions"
    elif rsi > 70:
        return "AVOID", "RSI indicates overbought conditions"
    else:
        return "HOLD", "RSI is neutral"

# ---------------- FUNDAMENTAL ANALYSIS ---------------- #
def fundamental_signal(info):
    pe = info.get("pe_ratio")
    market_cap = info.get("market_cap")
    last_price = info.get("last_price")

    reasons = []

    if pe:
        reasons.append(f"P/E Ratio: {pe:.2f}")
    else:
        reasons.append("P/E Ratio not available")

    if market_cap:
        reasons.append("Market Cap available")
    else:
        reasons.append("Market Cap not available")

    return pe, market_cap, last_price, reasons

# ---------------- MAIN LOGIC ---------------- #
if st.button("Analyze"):
    if not ticker:
        st.error("Please enter a company name or ticker")
    else:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1y")
        info = stock.fast_info

        if data.empty:
            st.error("Invalid ticker or no data found")
        else:
            data["RSI"] = calculate_rsi(data["Close"])
            latest_rsi = data["RSI"].iloc[-1]
            tech_signal, tech_reason = technical_signal(latest_rsi)

            pe, market_cap, last_price, fund_reasons = fundamental_signal(info)

            st.subheader(f"📈 {ticker} Price (1 Year)")
            st.line_chart(data["Close"])

            st.subheader("📉 RSI")
            st.line_chart(data["RSI"])

            st.subheader("📊 Fundamental Analysis")
            st.write({
                "Last Price": last_price if last_price else "Not available",
                "P/E Ratio": pe if pe else "Not available",
                "Market Cap": market_cap if market_cap else "Not available"
            })

            for r in fund_reasons:
                st.write("•", r)

            st.subheader("🧠 Final Signal")
            if tech_signal == "BUY":
                st.success("Educational Signal: BUY")
            elif tech_signal == "AVOID":
                st.warning("Educational Signal: AVOID")
            else:
                st.info("Educational Signal: HOLD")

            st.write("**Technical Insight:**", tech_reason)

            st.warning(
                "⚠️ Educational purpose only. Not financial advice."
            )
