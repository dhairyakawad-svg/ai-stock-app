import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Fundamental Analysis", layout="centered")

st.title("📊 Fundamental Stock Analysis")
st.write("Free & educational fundamental analysis (Not financial advice)")

# ---------------- INPUT ---------------- #
ticker = st.text_input(
    "Enter stock ticker (Example: AAPL, TSLA, MRF.NS)"
).upper().strip()

# ---------------- FUNDAMENTAL LOGIC ---------------- #
def fundamental_analysis(stock):
    info = stock.fast_info   # ✅ reliable
    financials = stock.financials

    current_price = info.get("last_price")
    market_cap = info.get("market_cap")

    # Financial statement values
    revenue = None
    net_income = None

    if financials is not None and not financials.empty:
        revenue = financials.loc["Total Revenue"].iloc[0] if "Total Revenue" in financials.index else None
        net_income = financials.loc["Net Income"].iloc[0] if "Net Income" in financials.index else None

    score = 0
    reasons = []

    if market_cap:
        score += 1
        reasons.append("Market capitalization available")
    else:
        reasons.append("Market cap not available")

    if revenue and net_income:
        if net_income > 0:
            score += 1
            reasons.append("Company is profitable")
        else:
            reasons.append("Company is not profitable")
    else:
        reasons.append("Profit data not available")

    return {
        "Current Price": current_price,
        "Market Cap": market_cap,
        "Revenue": revenue,
        "Net Income": net_income
    }, score, reasons

# ---------------- MAIN ---------------- #
if st.button("Analyze Fundamentals"):
    if ticker == "":
        st.error("Please enter a stock ticker")
    else:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1y")

        if data.empty:
            st.error("Invalid ticker or no market data found")
        else:
            fundamentals, score, reasons = fundamental_analysis(stock)

            st.subheader("🏢 Fundamental Data")
            st.write(fundamentals)

            st.subheader("📌 Fundamental Insights")
            for r in reasons:
                st.write("•", r)

            st.subheader("🧠 Fundamental Verdict")
            if score >= 2:
                st.success("Overall Fundamentals: GOOD")
            elif score == 1:
                st.info("Overall Fundamentals: AVERAGE")
            else:
                st.warning("Overall Fundamentals: WEAK")

            st.warning(
                "⚠️ Educational purpose only. Not financial advice."
            )
