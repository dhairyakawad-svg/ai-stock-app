import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="AI Stock Analyzer", layout="centered")

st.title("📊 AI Stock Analyzer")
st.write("Educational stock analysis tool (Not financial advice)")

ticker = st.text_input(
    "Enter stock ticker (Example: AAPL, TSLA, MRF.NS)"
).upper().strip()

# ---------------- TECHNICAL ANALYSIS ---------------- #

def calculate_rsi(data, period=14):
    delta = data.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def technical_signal(rsi):
    if rsi < 30:
        return "BUY", "RSI indicates oversold conditions"
    elif rsi > 70:
        return "AVOID", "RSI indicates overbought conditions"
    else:
        return "HOLD", "RSI is in a neutral range"

# ---------------- FUNDAMENTAL ANALYSIS ---------------- #

def fundamental_signal(info):
    pe = info.get("trailingPE")
    market_cap = info.get("marketCap")
    debt = info.get("totalDebt")

    score = 0
    reasons = []

    if pe and pe < 25:
        score += 1
        reasons.append("Reasonable P/E ratio")
    elif pe:
        reasons.append("High P/E ratio")

    if market_cap:
        score += 1
        reasons.append("Strong market capitalization")

    if debt and market_cap and debt < market_cap * 0.5:
        score += 1
        reasons.append("Debt level appears manageable")
    elif debt:
        reasons.append("High debt level")

    return score, reasons

# ---------------- MAIN LOGIC ---------------- #

if st.button("Analyze"):
    if ticker == "":
        st.error("Please enter a stock ticker")
    else:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1y")
        info = stock.info

        if data.empty:
