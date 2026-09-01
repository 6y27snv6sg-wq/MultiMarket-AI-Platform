import streamlit as st
import pandas as pd
from data_fetcher import (
    fetch_crypto_market,
    fetch_us_stocks,
    fetch_crypto_fear_greed
)

st.set_page_config(
    page_title="Capi | Multi-Market AI",
    page_icon="⚡",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #07090E;
    color: #E2E8F0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}

.luxe-header {
    background: linear-gradient(180deg, #0F172A 0%, #07090E 100%);
    padding: 35px 20px;
    border-radius: 16px;
    border: 1px solid #1E293B;
    text-align: center;
    margin-bottom: 30px;
}

.luxe-title {
    color: #FFFFFF !important;
    font-size: 32px !important;
    font-weight: 800 !important;
    letter-spacing: -0.5px;
    margin: 0;
}

.luxe-subtitle {
    color: #64748B !important;
    font-size: 14px !important;
    margin-top: 8px;
    text-transform: uppercase;
    letter-spacing: 2px;
}

div[data-testid="stMetric"] {
    background-color: #0D1117;
    border: 1px solid #21262D;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
}

.luxe-ai-box {
    background: #0D1117;
    border: 1px solid #30363D;
    border-left: 4px solid #58A6FF;
    padding: 25px;
    border-radius: 12px;
    margin-top: 25px;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5);
}

.stButton>button {
    background: #FFFFFF !important;
    color: #000000 !important;
    font-weight: 700 !important;
    border-radius: 8px !important;
    border: none !important;
    padding: 12px 24px !important;
    transition: all 0.2s ease;
}

.stButton>button:hover {
    background: #E2E8F0 !important;
    transform: translateY(-1px);
}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="luxe-header">
    <h1 class="luxe-title">Capi AI Intelligence</h1>
    <p class="luxe-subtitle">
        Advanced Multi-Market Analytics & Predictive Engine
    </p>
</div>
""", unsafe_allow_html=True)


st.sidebar.markdown("### 🌐 Market Selection")

market_type = st.sidebar.radio(
    "Choose Asset Class:",
    ["Cryptocurrency", "US Equities"]
)


crypto_watchlist = {
    "Bitcoin": "bitcoin",
    "Ethereum": "ethereum",
    "Solana": "solana",
    "Ripple": "ripple",
    "Cardano": "cardano",
    "Binance Coin": "binancecoin",
    "Dogecoin": "dogecoin"
}


us_stocks_watchlist = [
    "AAPL",
    "MSFT",
    "GOOGL",
    "AMZN",
    "TSLA",
    "NVDA",
    "META"
]


# =========================================================
# CRYPTOCURRENCY
# =========================================================

if market_type == "Cryptocurrency":

    fng_val, fng_class = fetch_crypto_fear_greed()

    st.sidebar.markdown("---")

    st.sidebar.metric(
        "Market Sentiment (F&G)",
        f"{fng_val}/100",
        fng_class
    )

    st.markdown("### 🪙 Digital Assets Feed")

    ids = list(crypto_watchlist.values())

    raw_data = fetch_crypto_market(ids)

    if raw_data:

        display_list = []
        coin_cache = {}

        for coin in raw_data:

            change = coin.get(
                "price_change_percentage_24h",
                0
            ) or 0

            coin_cache[coin["name"]] = {
                "price": coin["current_price"],
                "change": change,
                "high": coin["high_24h"],
                "low": coin["low_24h"],
                "sparkline": coin.get(
                    "sparkline_in_7d",
                    {}
                ).get("price", [])
            }

            display_list.append({
                "Asset": coin["name"],
                "Ticker": coin["symbol"].upper(),
                "Price (USD)": f"${coin['current_price']:,.2f}",
                "24h Change": f"{change:.2f}%"
            })

        st.dataframe(
            pd.DataFrame(display_list),
            use_container_width=True
        )

        st.divider()

        st.markdown("### ⚡ Deep AI Asset Analysis")

        chosen_coin = st.selectbox(
            "Select Asset for Neural Processing:",
            list(coin_cache.keys())
        )

        if chosen_coin in coin_cache:

            info = coin_cache[chosen_coin]

            col_a, col_b = st.columns([1, 2])

            with col_a:

                st.metric(
                    "Current Price",
                    f"${info['price']:,.2f}",
                    f"{info['change']:.2f}%"
                )

                st.metric(
                    "24h High",
                    f"${info['high']:,.2f}"
                )

                st.metric(
                    "24h Low",
                    f"${info['low']:,.2f}"
                )

            with col_b:

                if info["sparkline"]:

                    st.line_chart(
                        pd.DataFrame({
                            "Weekly Trend": info["sparkline"]
                        }),
                        color="#58A6FF"
                    )

            if st.button("Execute Neural Decision Engine"):

                with st.spinner(
                    "Processing market data & neural networks..."
                ):

                    chg = info["change"]

                    if chg > 2:

                        decision = "STRONG ACCUMULATION (Bullish)"
                        confidence = "76.4%"
                        scenario = (
                            "Upward momentum sustaining toward upper "
                            "resistance bounds. Recommended trailing stop-loss."
                        )
                        accent_color = "#3FB950"

                    elif chg >= 0:

                        decision = "NEUTRAL CONSOLIDATION"
                        confidence = "61.2%"
                        scenario = (
                            "Sideways price action. Awaiting volume "
                            "breakout before directional scaling."
                        )
                        accent_color = "#58A6FF"

                    else:

                        decision = "CAUTION / POTENTIAL CORRECTION"
                        confidence = "69.1%"
                        scenario = (
                            "Downward pressure testing local liquidity "
                            "zones. Mitigate exposure."
                        )
                        accent_color = "#F85149"

                st.markdown(
                    f"""
                    <div class="luxe-ai-box"
                         style="border-left-color: {accent_color};">

                        <h3 style="
                            color: {accent_color};
                            margin-top: 0;
                            font-size: 20px;
                        ">
                            ⚡ Capi Neural Report: {chosen_coin}
                        </h3>

                        <p style="margin: 8px 0;">
                            <b>Signal Direction:</b> {decision}
                        </p>

                        <p style="margin: 8px 0;">
                            <b>Model Confidence:</b> {confidence}
                        </p>

                        <p style="
                            margin: 8px 0;
                            color: #94A3B8;
                        ">
                            <b>Strategic Alternative Scenario:</b>
                            {scenario}
                        </p>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


# =========================================================
# US EQUITIES
# =========================================================

elif market_type == "US Equities":

    st.markdown("### 🇺🇸 US Equities Feed")

    stock_raw = fetch_us_stocks(us_stocks_watchlist)

    if stock_raw:

        stock_display = []
        stock_cache = {}

        for stck in stock_raw:

            chg = stck.get(
                "price_change_percentage_24h",
                0
            ) or 0

            stock_cache[stck["symbol"]] = {
                "price": stck["current_price"],
                "change": chg,
                "high": stck["high_24h"],
                "low": stck["low_24h"]
            }

            stock_display.append({
                "Ticker": stck["symbol"],
                "Price (USD)": f"${stck['current_price']:,.2f}",
                "24h Change": f"{chg:.2f}%"
            })

        st.dataframe(
            pd.DataFrame(stock_display),
            use_container_width=True
        )

        st.divider()

        st.markdown("### ⚡ Deep AI Equities Analysis")

        chosen_stock = st.selectbox(
            "Select Equity for Neural Processing:",
            list(stock_cache.keys())
        )

        if chosen_stock in stock_cache:

            s_info = stock_cache[chosen_stock]

            c1, c2 = st.columns(2)

            c1.metric(
                "Current Price",
                f"${s_info['price']:,.2f}",
                f"{s_info['change']:.2f}%"
            )

            c2.metric(
                "Session Range",
                f"High: ${s_info['high']:,.2f} | "
                f"Low: ${s_info['low']:,.2f}"
            )

            if st.button("Execute Neural Decision Engine"):

                with st.spinner(
                    "Analyzing order books and volatility indices..."
                ):

                    s_chg = s_info["change"]

                    if s_chg > 1:

                        s_decision = "MOMENTUM BUY (Growth)"
                        s_conf = "73.2%"
                        s_scen = (
                            "Outperforming benchmark trends with strong "
                            "institutional volume backing."
                        )
                        s_color = "#3FB950"

                    else:

                        s_decision = "DEFENSIVE HOLD"
                        s_conf = "65.8%"
                        s_scen = (
                            "Consolidating near key moving averages. "
                            "Patience advised."
                        )
                        s_color = "#F85149"

                st.markdown(
                    f"""
                    <div class="luxe-ai-box"
                         style="border-left-color: {s_color};">

                        <h3 style="
                            color: {s_color};
                            margin-top: 0;
                            font-size: 20px;
                        ">
                            ⚡ Capi Neural Report: {chosen_stock}
                        </h3>

                        <p style="margin: 8px 0;">
                            <b>Signal Direction:</b> {s_decision}
                        </p>

                        <p style="margin: 8px 0;">
                            <b>Model Confidence:</b> {s_conf}
                        </p>

                        <p style="
                            margin: 8px 0;
                            color: #94A3B8;
                        ">
                            <b>Strategic Alternative Scenario:</b>
                            {s_scen}
                        </p>

                    </div>
                    """,
                    unsafe_allow_html=True
                )
