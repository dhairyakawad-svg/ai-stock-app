import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="AI Stock Analyzer", layout="centered")

st.title("📊 AI Stock Analyzer")
st.write("Educational stock analysis tool (Not financial advice)")

ticker = st.text_input("Enter stock ticker (Example: AAPL, TSLA, MSFT)")

def calculate_rsi(data, period=14):
    delta = data.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

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

            st.subheader("🧠 Analysis Result")

            if latest_rsi < 30:
                st.success("RSI indicates the stock may be **OVERSOLD** → Educational BUY signal")
            elif latest_rsi > 70:
                st.warning("RSI indicates the stock may be **OVERBOUGHT** → Educational AVOID signal")
            else:
                st.info("RSI indicates **NEUTRAL** conditions → HOLD signal")

            st.write(f"📌 Current RSI value: **{latest_rsi:.2f}**")

            st.warning(
                "⚠️ This app provides educational market analysis only. "
                "It is NOT financial advice. Always consult a licensed financial advisor."
            )
