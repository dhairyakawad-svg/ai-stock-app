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
    # Using fast_info for reliability
    market_cap = info.get("market_cap")
    pe = info.get("pe_ratio")
    last_price = info.get("last_price")

    score = 0
    reasons = []

    if pe:
        reasons.append(f"P/E ratio available ({pe:.2f})")
        if pe < 25:
            score += 1
    else:
        reasons.append("P/E ratio not available")

    if market_cap:
        reasons.append("Market capitalization available")
        score += 1
    else:
        reasons.append("Market capitalization not available")

    return score, reasons, pe, market_cap, last_price

# ---------------- AI-STYLE EXPLANATION ---------------- #
def ai_explanation(rsi, fund_score, fund_reasons):
    text = "Fundamental insights: " + ", ".join(fund_reasons) + ". "
    if rsi < 30 and fund_score >= 1:
        text += "Technicals show oversold conditions and fundamentals appear acceptable. This may indicate a potential opportunity, but risks remain."
    elif rsi > 70:
        text += "Technicals show overbought conditions, suggesting caution despite fundamentals."
    else:
        text += "Both technical and fundamental indicators suggest neutral conditions at this time."
    return text

# ---------------- MAIN LOGIC ---------------- #
if st.button("Analyze"):
    if ticker == "":
        st.error("Please enter a stock ticker")
    else:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1y")
        info = stock.fast_info  # fast_info is more reliable on Streamlit Cloud

        if data.empty or not info:
            st.error("Invalid ticker or no data found")
        else:
            # Technical Analysis
            data["RSI"] = calculate_rsi(data["Close"])
            latest_rsi = data["RSI"].iloc[-1]
            tech_signal, tech_reason = technical_signal(latest_rsi)

            # Fundamental Analysis
            fund_score, fund_reasons, pe, market_cap, last_price = fundamental_signal(info)

            # ---------------- DISPLAY ---------------- #
            st.subheader("📈 Stock Price (Last 1 Year)")
            st.line_chart(data["Close"])

            st.subheader("📉 RSI Indicator")
            st.line_chart(data["RSI"])

            st.subheader("📊 Fundamental Analysis")
            st.write({
                "P/E Ratio": pe if pe else "Not available",
                "Market Cap": market_cap if market_cap else "Not available",
                "Last Price": last_price if last_price else "Not available"
            })
            st.write("**Fundamental Insights:**")
            for r in fund_reasons:
                st.write("•", r)
            if (pe is None) and (market_cap is None):
                st.info("Fundamental data is limited for this stock from free sources.")

            st.subheader("🧠 Combined Analysis")
            if tech_signal == "BUY" and fund_score >= 1:
                st.success("Educational Signal: BUY")
            elif tech_signal == "AVOID":
                st.warning("Educational Signal: AVOID")
            else:
                st.info("Educational Signal: HOLD")

            st.write("**Technical Insight:**", tech_reason)
            st.write("**AI-Style Explanation:**", ai_explanation(latest_rsi, fund_score, fund_reasons))

            st.warning(
                "⚠️ This platform provides educational market analysis only. "
                "It is NOT financial advice. No guarantees are provided."
            )
