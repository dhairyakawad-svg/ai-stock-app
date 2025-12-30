import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="AI Stock Analyzer", layout="centered")

st.title("📊 AI Stock Analyzer")
st.write("Educational stock analysis tool (Not financial advice)")

ticker = st.text_input(
    "Enter stock ticker (Example: AAPL, TSLA, MSFT)"
).upper().strip()

def calculate_rsi(data, period=14):
    delta = data.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def ai_explanation(rsi_value):
    if rsi_value < 30:
        return (
            "The stock appears **oversold** based on the RSI indicator. "
            "This means selling pressure has been strong recently. "
            "Historically, oversold conditions can sometimes lead to short-term rebounds, "
            "but this is not guaranteed and market risks remain."
        )
    elif rsi_value > 70:
        return (
            "The stock appears **overbought** based on the RSI indicator. "
            "This suggests strong recent buying activity. "
            "Overbought conditions can sometimes be followed by pullbacks or consolidation."
        )
    else:
        return (
            "The stock is in a **neutral** RSI range. "
            "This suggests balanced buying and selling pressure, "
            "with no strong momentum signal at the moment."
        )

if st.button("Analyze"):
    if ticker == "":
        st.error("Please enter a stock ticker")
    else:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1y")

        if data.empty:
            st.error("Invalid ticker or no data found")
        else:
            data["RSI"] = calculate_rsi(data["Close"])
            latest_rsi = data["RSI"].iloc[-1]

            st.subheader("📈 Stock Price (Last 1 Year)")
            st.line_chart(data["Close"])

            st.subheader("📉 RSI Indicator")
            st.line_chart(data["RSI"])

            st.subheader("🧠 AI-Style Analysis")

            if latest_rsi < 30:
                st.success("Educational Signal: BUY (Oversold)")
            elif latest_rsi > 70:
                st.warning("Educational Signal: AVOID (Overbought)")
            else:
                st.info("Educational Signal: HOLD (Neutral)")

            st.write(f"📌 Current RSI: **{latest_rsi:.2f}**")
            st.write(ai_explanation(latest_rsi))

            st.warning(
                "⚠️ This platform provides educational market analysis only. "
                "It is NOT financial advice. No guarantees are provided."
            )
