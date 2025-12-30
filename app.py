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
    info = stock.info

    data = {
        "Company Name": info.get("longName"),
        "Current Price": info.get("currentPrice"),
        "Market Cap": info.get("marketCap"),
        "P/E Ratio": info.get("trailingPE"),
        "Book Value": info.get("bookValue"),
        "ROE": info.get("returnOnEquity"),
        "Debt to Equity": info.get("debtToEquity")
    }

    score = 0
    reasons = []

    pe = data["P/E Ratio"]
    roe = data["ROE"]
    debt_equity = data["Debt to Equity"]

    if pe and pe < 25:
        score += 1
        reasons.append("Reasonable P/E ratio")
    elif pe:
        reasons.append("High P/E ratio")
    else:
        reasons.append("P/E ratio not available")

    if roe and roe > 0.15:
        score += 1
        reasons.append("Strong return on equity")
    elif roe:
        reasons.append("Low return on equity")
    else:
        reasons.append("ROE not available")

    if debt_equity and debt_equity < 100:
        score += 1
        reasons.append("Debt level is manageable")
    elif debt_equity:
        reasons.append("High debt level")
    else:
        reasons.append("Debt data not available")

    return data, score, reasons

# ---------------- MAIN ---------------- #
if st.button("Analyze Fundamentals"):
    if ticker == "":
        st.error("Please enter a stock ticker")
    else:
        try:
            stock = yf.Ticker(ticker)
            data, score, reasons = fundamental_analysis(stock)

            if not data["Company Name"]:
                st.error("Invalid ticker or no data found")
            else:
                st.subheader("🏢 Company Overview")
                st.write(data)

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
                    "⚠️ This analysis is for educational purposes only. "
                    "It is NOT financial advice."
                )

        except Exception as e:
            st.error("Error fetching data. Try another ticker.")
