import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="AI Stock Analyzer", layout="centered")

st.title("📊 AI Stock Analyzer")
st.write("Educational stock analysis tool (Not financial advice)")

# ---------------- COMPANY SEARCH ---------------- #
company_query = st.text_input(
    "Enter company name or ticker (Apple, MRF, Reliance, AAPL, MRF.NS)"
).strip()

selected_ticker = None

if company_query:
    try:
        search_results = yf.search(company_query, max_results=5)
        quotes = search_results.get("quotes", [])

        if quotes:
            ticker_options = {
                f"{q.get('shortname', 'Unknown')} ({q.get('symbol')})": q.get("symbol")
                for q in quotes if q.get("symbol")
            }
            selected_label = st.selectbox(
                "Select the correct stock:",
                ticker_options.keys()
            )
            selected_ticker = ticker_options[selected_label]
        else:
            st.warning("No matching companies found.")
    except Exception as e:
        st.error("Error searching company name.")

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

    score = 0
    reasons = []

    if pe:
        reasons.append(f"P/E Ratio available ({pe:.2f})")
        if pe < 25:
            score += 1
    else:
        reasons.append("P/E Ratio not available")

    if market_cap:
        reasons.append("Market Cap available")
        score += 1
    else:
        reasons.append("Market Cap not available")

    return score, reasons, pe, market_cap, last_price

# ---------------- MAIN LOGIC ---------------- #
if st.button("Analyze"):
    if not selected_ticker:
        st.error("Please select a stock first")
    else:
        stock = yf.Ticker(selected_ticker)
        data = stock.history(period="1y")
        info = stock.fast_info

        if data.empty or not info:
            st.error("No data available for this stock")
        else:
            data["RSI"] = calculate_rsi(data["Close"])
            latest_rsi = data["RSI"].iloc[-1]
            tech_signal, tech_reason = technical_signal(latest_rsi)

            fund_score, fund_reasons, pe, market_cap, last_price = fundamental_signal(info)

            # ---------------- DISPLAY ---------------- #
            st.subheader(f"📈 {selected_ticker} Price (1 Year)")
            st.line_chart(data["Close"])

            st.subheader("📉 RSI Indicator")
            st.line_chart(data["RSI"])

            st.subheader("📊 Fundamental Analysis")
            st.write({
                "Last Price": last_price if last_price else "Not available",
                "P/E Ratio": pe if pe else "Not available",
                "Market Cap": market_cap if market_cap else "Not available"
            })

            st.write("**Fundamental Insights:**")
            for r in fund_reasons:
                st.write("•", r)

            st.subheader("🧠 Final Signal")
            if tech_signal == "BUY" and fund_score >= 1:
                st.success("Educational Signal: BUY")
            elif tech_signal == "AVOID":
                st.warning("Educational Signal: AVOID")
            else:
                st.info("Educational Signal: HOLD")

            st.write("**Technical Insight:**", tech_reason)

            st.warning(
                "⚠️ This app is for educational purposes only. "
                "It is not financial advice."
            )
