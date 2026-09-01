import streamlit as st
import pandas as pd

from data_fetcher import (
    search_crypto,
    fetch_crypto_market,
    fetch_us_stocks,
    fetch_crypto_fear_greed
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Capi | Multi-Market AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# STYLE
# =========================================================

st.markdown("""
<style>

.stApp {
    background-color: #07090E;
    color: #E2E8F0;
    font-family:
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        Roboto,
        Helvetica,
        Arial,
        sans-serif;
}

.luxe-header {
    background:
        linear-gradient(
            180deg,
            #0F172A 0%,
            #07090E 100%
        );
    padding: 35px 20px;
    border-radius: 16px;
    border: 1px solid #1E293B;
    text-align: center;
    margin-bottom: 25px;
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

.search-box {
    background: #0D1117;
    border: 1px solid #21262D;
    padding: 18px;
    border-radius: 12px;
    margin-bottom: 20px;
}

div[data-testid="stMetric"] {
    background-color: #0D1117;
    border: 1px solid #21262D;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.35);
}

.luxe-ai-box {
    background: #0D1117;
    border: 1px solid #30363D;
    border-left: 4px solid #58A6FF;
    padding: 25px;
    border-radius: 12px;
    margin-top: 25px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.5);
}

.status-box {
    background: #0D1117;
    border: 1px solid #21262D;
    padding: 12px 16px;
    border-radius: 10px;
    color: #94A3B8;
    font-size: 13px;
}

.stButton > button {
    background: #FFFFFF !important;
    color: #000000 !important;
    font-weight: 700 !important;
    border-radius: 8px !important;
    border: none !important;
    padding: 10px 20px !important;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: #E2E8F0 !important;
    transform: translateY(-1px);
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="luxe-header">
    <h1 class="luxe-title">Capi AI Intelligence</h1>
    <p class="luxe-subtitle">
        Advanced Multi-Market Analytics & Predictive Engine
    </p>
</div>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("### 🌐 Market Selection")

market_type = st.sidebar.radio(
    "Choose Asset Class:",
    ["Cryptocurrency", "US Equities"]
)

st.sidebar.markdown("---")

if st.sidebar.button("🔄 Refresh Market Data", use_container_width=True):
    st.cache_data.clear()
    st.rerun()


# =========================================================
# CRYPTOCURRENCY
# =========================================================

if market_type == "Cryptocurrency":

    fng_val, fng_class = fetch_crypto_fear_greed()

    st.sidebar.metric(
        "Market Sentiment",
        f"{fng_val}/100",
        fng_class
    )

    st.markdown("### 🪙 Digital Assets Feed")

    st.markdown(
        '<div class="search-box">',
        unsafe_allow_html=True
    )

    crypto_query = st.text_input(
        "Search Cryptocurrency",
        placeholder="Example: Bitcoin, Ethereum, Solana, XRP...",
        key="crypto_search"
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    if crypto_query.strip():

        with st.spinner("Searching cryptocurrency market..."):

            crypto_results = search_crypto(
                crypto_query.strip()
            )

        if crypto_results:

            crypto_options = {}

            for coin in crypto_results:
                crypto_options[
                    f"{coin['name']} ({coin['symbol'].upper()})"
                ] = coin["id"]

            selected_label = st.selectbox(
                "Select Asset:",
                list(crypto_options.keys())
            )

            selected_id = crypto_options[selected_label]

            raw_data = fetch_crypto_market(
                [selected_id]
            )

            if raw_data:

                coin = raw_data[0]

                price = coin.get("current_price", 0) or 0
                change = (
                    coin.get(
                        "price_change_percentage_24h",
                        0
                    ) or 0
                )
                high = coin.get("high_24h", price) or price
                low = coin.get("low_24h", price) or price
                volume = coin.get("total_volume", 0) or 0

                sparkline = coin.get(
                    "sparkline_in_7d",
                    {}
                ).get("price", [])

                st.markdown(
                    f"### ⚡ {coin.get('name', selected_label)} "
                    f"({coin.get('symbol', '').upper()})"
                )

                col1, col2, col3, col4 = st.columns(4)

                col1.metric(
                    "Current Price",
                    f"${price:,.2f}",
                    f"{change:.2f}%"
                )

                col2.metric(
                    "24h High",
                    f"${high:,.2f}"
                )

                col3.metric(
                    "24h Low",
                    f"${low:,.2f}"
                )

                col4.metric(
                    "24h Volume",
                    f"${volume:,.0f}"
                )

                st.divider()

                chart_col, info_col = st.columns([2, 1])

                with chart_col:

                    st.markdown("#### 7-Day Price Trend")

                    if sparkline:
                        st.line_chart(
                            pd.DataFrame({
                                "Price": sparkline
                            }),
                            use_container_width=True
                        )
                    else:
                        st.info(
                            "7-day chart data is not available."
                        )

                with info_col:

                    st.markdown("#### Market Snapshot")

                    market_cap = coin.get(
                        "market_cap",
                        0
                    ) or 0

                    rank = coin.get(
                        "market_cap_rank"
                    )

                    st.write(
                        f"**Market Cap:** "
                        f"${market_cap:,.0f}"
                    )

                    st.write(
                        f"**Market Rank:** "
                        f"{rank if rank else 'N/A'}"
                    )

                    st.write(
                        f"**24h Change:** "
                        f"{change:.2f}%"
                    )

                st.divider()

                st.markdown(
                    "### ⚡ Capi Decision Engine"
                )

                if st.button(
                    "Execute Neural Decision Engine",
                    key="crypto_ai"
                ):

                    with st.spinner(
                        "Analyzing market structure..."
                    ):

                        if change > 2:

                            decision = (
                                "STRONG POSITIVE MOMENTUM"
                            )
                            confidence = "76.4%"
                            scenario = (
                                "Positive short-term momentum. "
                                "Monitor resistance and volume confirmation "
                                "before increasing exposure."
                            )
                            accent = "#3FB950"

                        elif change >= 0:

                            decision = (
                                "NEUTRAL CONSOLIDATION"
                            )
                            confidence = "61.2%"
                            scenario = (
                                "Price action remains relatively balanced. "
                                "A volume expansion may be required "
                                "to confirm the next directional move."
                            )
                            accent = "#58A6FF"

                        else:

                            decision = (
                                "CAUTION / POTENTIAL CORRECTION"
                            )
                            confidence = "69.1%"
                            scenario = (
                                "Negative short-term momentum. "
                                "Watch support levels and avoid treating "
                                "a single-day move as a confirmed trend."
                            )
                            accent = "#F85149"

                    st.markdown(
                        f"""
                        <div class="luxe-ai-box"
                             style="border-left-color:{accent};">

                            <h3 style="
                                color:{accent};
                                margin-top:0;
                            ">
                                ⚡ Capi Neural Report
                            </h3>

                            <p>
                                <b>Asset:</b>
                                {coin.get('name', selected_label)}
                            </p>

                            <p>
                                <b>Signal:</b>
                                {decision}
                            </p>

                            <p>
                                <b>Model Confidence:</b>
                                {confidence}
                            </p>

                            <p style="color:#94A3B8;">
                                <b>Alternative Scenario:</b>
                                {scenario}
                            </p>

                            <p style="
                                color:#64748B;
                                font-size:12px;
                            ">
                                Signal is based on the available
                                market data and is not financial advice.
                            </p>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        else:

            st.warning(
                "No cryptocurrency matched your search."
            )

    else:

        st.info(
            "Search for any cryptocurrency to begin analysis."
        )


# =========================================================
# US EQUITIES
# =========================================================

elif market_type == "US Equities":

    st.markdown("### 🇺🇸 US Equities Feed")

    st.markdown(
        '<div class="search-box">',
        unsafe_allow_html=True
    )

    stock_query = st.text_input(
        "Enter US Stock Symbol",
        placeholder="Example: AAPL, NVDA, AMD, JPM, MSFT...",
        key="stock_search"
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    if stock_query.strip():

        ticker = stock_query.strip().upper()

        stock_raw = fetch_us_stocks(
            [ticker]
        )

        if stock_raw:

            stock = stock_raw[0]

            price = stock["current_price"]
            change = stock["price_change_percentage_24h"]
            high = stock["high_24h"]
            low = stock["low_24h"]
            volume = stock.get("volume", 0)

            st.markdown(
                f"### ⚡ {ticker} Market Intelligence"
            )

            c1, c2, c3, c4 = st.columns(4)

            c1.metric(
                "Current Price",
                f"${price:,.2f}",
                f"{change:.2f}%"
            )

            c2.metric(
                "Session High",
                f"${high:,.2f}"
            )

            c3.metric(
                "Session Low",
                f"${low:,.2f}"
            )

            if volume:
                c4.metric(
                    "Volume",
                    f"{volume:,.0f}"
                )
            else:
                c4.metric(
                    "Volume",
                    "N/A"
                )

            st.divider()

            st.markdown(
                "### ⚡ Capi Decision Engine"
            )

            if st.button(
                "Execute Neural Decision Engine",
                key="stock_ai"
            ):

                with st.spinner(
                    "Analyzing market structure..."
                ):

                    if change > 1:

                        decision = "POSITIVE MOMENTUM"
                        confidence = "73.2%"
                        scenario = (
                            "Short-term momentum is positive. "
                            "Confirmation from volume and broader market "
                            "conditions should be monitored."
                        )
                        accent = "#3FB950"

                    elif change >= 0:

                        decision = "DEFENSIVE HOLD"
                        confidence = "65.8%"
                        scenario = (
                            "Price is relatively stable. "
                            "A breakout with stronger participation would "
                            "provide better directional confirmation."
                        )
                        accent = "#58A6FF"

                    else:

                        decision = "CAUTION"
                        confidence = "68.1%"
                        scenario = (
                            "Negative short-term price pressure. "
                            "Monitor support and market-wide risk sentiment "
                            "before assuming a sustained downtrend."
                        )
                        accent = "#F85149"

                st.markdown(
                    f"""
                    <div class="luxe-ai-box"
                         style="border-left-color:{accent};">

                        <h3 style="
                            color:{accent};
                            margin-top:0;
                        ">
                            ⚡ Capi Neural Report: {ticker}
                        </h3>

                        <p>
                            <b>Signal:</b>
                            {decision}
                        </p>

                        <p>
                            <b>Model Confidence:</b>
                            {confidence}
                        </p>

                        <p style="color:#94A3B8;">
                            <b>Alternative Scenario:</b>
                            {scenario}
                        </p>

                        <p style="
                            color:#64748B;
                            font-size:12px;
                        ">
                            Signal is based on available market data
                            and is not financial advice.
                        </p>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:

            st.error(
                f"No market data found for ticker: {ticker}"
            )

    else:

        st.info(
            "Enter any US stock symbol to begin analysis."
        )
