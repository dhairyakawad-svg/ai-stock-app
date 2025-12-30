import streamlit as st
import yfinance as yf

st.title("📊 AI Stock Analyzer")
st.write("Educational tool only. Not financial advice.")

ticker = st.text_input("Enter stock ticker (Example: AAPL)")

if st.button("Analyze"):
    if ticker:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1y")

        st.line_chart(data["Close"])
        st.write(data.tail())
    else:
        st.error("Please enter a ticker symbol")
