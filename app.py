import streamlit as st
import pandas as pd
from datetime import datetime

from data_fetcher import (
    search_crypto,
    fetch_crypto_market,
    fetch_crypto_history,
    fetch_crypto_global,
    fetch_us_stocks,
    fetch_stock_history,
    fetch_crypto_fear_greed,
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Capi | Decision Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# SESSION STATE
# =========================================================

if "selected_asset" not in st.session_state:
    st.session_state.selected_asset = None

if "selected_symbol" not in st.session_state:
    st.session_state.selected_symbol = None


# =========================================================
# LANGUAGE
# =========================================================

st.sidebar.markdown("### ⚙️ Settings")

language = st.sidebar.radio(
    "Language / اللغة",
    ["العربية", "English"],
    index=0,
)

AR = language == "العربية"

if AR:
    T = {
        "market": "السوق",
        "crypto": "العملات الرقمية",
        "stocks": "الأسهم الأمريكية",
        "search": "بحث عن أصل",
        "search_crypto": "ابحث عن عملة رقمية",
        "search_stock": "أدخل رمز السهم",
        "refresh": "تحديث بيانات السوق",
        "market_value": "القيمة السوقية",
        "fear_greed": "مؤشر الخوف والطمع",
        "overview": "نظرة السوق",
        "top_assets": "الأصول الرئيسية",
        "select_asset": "اختر الأصل للتحليل",
        "price": "السعر الحالي",
        "change": "التغير 24 ساعة",
        "high": "أعلى سعر",
        "low": "أدنى سعر",
        "volume": "حجم التداول",
        "chart": "الحركة السعرية",
        "indicators": "المؤشرات الفنية",
        "rsi": "RSI",
        "macd": "MACD",
        "trend": "درجة الاتجاه",
        "decision": "محرك قرار Capi",
        "execute": "تشغيل تحليل Capi",
        "signal": "الإشارة",
        "score": "درجة الإشارة",
        "scenario": "السيناريو البديل",
        "bullish": "زخم إيجابي",
        "neutral": "تماسك محايد",
        "bearish": "ضغط هبوطي",
        "search_any": "يمكنك البحث عن أي أصل مدعوم",
        "no_result": "لم يتم العثور على الأصل.",
        "loading": "جاري تحليل بيانات السوق...",
        "updated": "آخر تحديث",
        "rank": "الترتيب",
        "market_cap": "القيمة السوقية",
        "not_advice": "تحليل معلوماتي مبني على بيانات السوق، وليس توصية مالية.",
        "weekly": "الاتجاه خلال 7 أيام",
        "session": "نطاق الجلسة",
        "stock_symbol": "رمز السهم",
        "crypto_name": "العملة",
        "status": "حالة السوق",
    }
else:
    T = {
        "market": "Market",
        "crypto": "Cryptocurrency",
        "stocks": "US Equities",
        "search": "Search Asset",
        "search_crypto": "Search cryptocurrency",
        "search_stock": "Enter stock symbol",
        "refresh": "Refresh Market Data",
        "market_value": "Market Value",
        "fear_greed": "Fear & Greed",
        "overview": "Market Overview",
        "top_assets": "Top Assets",
        "select_asset": "Select Asset",
        "price": "Current Price",
        "change": "24h Change",
        "high": "24h High",
        "low": "24h Low",
        "volume": "Volume",
        "chart": "Price Action",
        "indicators": "Technical Indicators",
        "rsi": "RSI",
        "macd": "MACD",
        "trend": "Trend Score",
        "decision": "Capi Decision Engine",
        "execute": "Run Capi Analysis",
        "signal": "Signal",
        "score": "Signal Score",
        "scenario": "Alternative Scenario",
        "bullish": "Positive Momentum",
        "neutral": "Neutral Consolidation",
        "bearish": "Bearish Pressure",
        "search_any": "Search for any supported asset",
        "no_result": "No asset found.",
        "loading": "Analyzing market data...",
        "updated": "Last update",
        "rank": "Rank",
        "market_cap": "Market Cap",
        "not_advice": "Informational market analysis, not financial advice.",
        "weekly": "7-Day Trend",
        "session": "Session Range",
        "stock_symbol": "Stock Symbol",
        "crypto_name": "Cryptocurrency",
        "status": "Market Status",
    }


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
<style>
.stApp {
    background: #090B11;
    color: #E5E7EB;
}

.block-container {
    max-width: 1250px;
    padding-top: 1.2rem;
    padding-bottom: 3rem;
}

.luxe-header {
    background: linear-gradient(145deg, #151A27, #0B0E15);
    border: 1px solid #252C3B;
    border-radius: 22px;
    padding: 28px 22px;
    text-align: center;
    margin-bottom: 18px;
    box-shadow: 0 12px 40px rgba(0,0,0,.28);
}

.luxe-title {
    color: #F8FAFC;
    font-size: 34px;
    font-weight: 800;
    margin: 0;
}

.luxe-subtitle {
    color: #8B95A7;
    font-size: 13px;
    margin-top: 7px;
    letter-spacing: 1.4px;
}

.section-title {
    color: #E5E7EB;
    font-size: 20px;
    font-weight: 750;
    margin: 18px 0 12px 0;
}

.market-card {
    background: linear-gradient(145deg, #171C28, #10141D);
    border: 1px solid #252D3C;
    border-radius: 16px;
    padding: 15px;
    min-height: 105px;
    box-shadow: 0 8px 25px rgba(0,0,0,.20);
}

.market-card-title {
    color: #AAB4C5;
    font-size: 13px;
    margin-bottom: 7px;
}

.market-card-price {
    color: #F8FAFC;
    font-size: 19px;
    font-weight: 750;
}

.market-card-change-up {
    color: #34D399;
    font-size: 13px;
    font-weight: 700;
}

.market-card-change-down {
    color: #F87171;
    font-size: 13px;
    font-weight: 700;
}

.market-card-change-flat {
    color: #94A3B8;
    font-size: 13px;
    font-weight: 700;
}

.info-card {
    background: #111620;
    border: 1px solid #242B38;
    border-radius: 17px;
    padding: 20px;
    text-align: center;
}

.info-label {
    color: #7F8A9D;
    font-size: 12px;
}

.info-value {
    color: #F8FAFC;
    font-size: 24px;
    font-weight: 800;
    margin-top: 5px;
}

.ai-box {
    background: linear-gradient(145deg, #131925, #0D1119);
    border: 1px solid #293244;
    border-left: 5px solid #58A6FF;
    border-radius: 18px;
    padding: 23px;
    margin-top: 18px;
    box-shadow: 0 12px 35px rgba(0,0,0,.25);
}

.ai-title {
    color: #58A6FF;
    font-size: 21px;
    font-weight: 800;
}

.ai-text {
    color: #CBD5E1;
    line-height: 1.7;
}

.small-note {
    color: #667085;
    font-size: 11px;
    margin-top: 14px;
}

div[data-testid="stMetric"] {
    background: #111620;
    border: 1px solid #252D3B;
    border-radius: 15px;
    padding: 15px;
}

.stButton > button {
    border-radius: 10px !important;
    font-weight: 700 !important;
    min-height: 42px !important;
}

@media (max-width: 768px) {
    .luxe-title {
        font-size: 27px;
    }

    .block-container {
        padding-left: 0.7rem;
        padding-right: 0.7rem;
    }
}
</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    f"""<div class="luxe-header">
<h1 class="luxe-title">⚡ Capi Decision Intelligence</h1>
<div class="luxe-subtitle">
{T["decision"]} · Multi-Market Analytics
</div>
</div>""",
    unsafe_allow_html=True,
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown(f"### 🌐 {T['market']}")

market_type = st.sidebar.radio(
    T["market"],
    [T["crypto"], T["stocks"]],
)

if st.sidebar.button(
    f"🔄 {T['refresh']}",
    use_container_width=True,
):
    st.cache_data.clear()
    st.rerun()


# =========================================================
# CRYPTO
# =========================================================

if market_type == T["crypto"]:

    fear_value, fear_class = fetch_crypto_fear_greed()
    global_data = fetch_crypto_global()

    if global_data:
        market_cap_total = global_data.get(
            "total_market_cap",
            0,
        )
        market_cap_usd = market_cap_total.get(
            "usd",
            0,
        )
    else:
        market_cap_usd = 0

    st.markdown(
        f'<div class="section-title">📊 {T["overview"]}</div>',
        unsafe_allow_html=True,
    )

    top_col1, top_col2, top_col3 = st.columns(3)

    with top_col1:
        st.markdown(
            f"""<div class="info-card">
<div class="info-label">{T["market_value"]}</div>
<div class="info-value">${market_cap_usd / 1e12:.2f}T</div>
</div>""",
            unsafe_allow_html=True,
        )

    with top_col2:
        st.markdown(
            f"""<div class="info-card">
<div class="info-label">{T["fear_greed"]}</div>
<div class="info-value">{fear_value}/100</div>
<div class="info-label">{fear_class}</div>
</div>""",
            unsafe_allow_html=True,
        )

    with top_col3:
        st.markdown(
            f"""<div class="info-card">
<div class="info-label">{T["updated"]}</div>
<div class="info-value" style="font-size:18px;">
{datetime.now().strftime("%H:%M")}
</div>
</div>""",
            unsafe_allow_html=True,
        )

    # -----------------------------------------------------
    # DEFAULT 7 CRYPTO ASSETS
    # -----------------------------------------------------

    default_crypto = [
        "bitcoin",
        "ethereum",
        "solana",
        "ripple",
        "cardano",
        "binancecoin",
        "dogecoin",
    ]

    crypto_data = fetch_crypto_market(default_crypto)

    st.markdown(
        f'<div class="section-title">🪙 {T["top_assets"]}</div>',
        unsafe_allow_html=True,
    )

    if crypto_data:

        rows = [
            crypto_data[i:i + 4]
            for i in range(0, len(crypto_data), 4)
        ]

        for row_index, row in enumerate(rows):

            cols = st.columns(len(row))

            for col, coin in zip(cols, row):

                price = coin.get("current_price", 0) or 0
                change = (
                    coin.get(
                        "price_change_percentage_24h",
                        0,
                    )
                    or 0
                )

                if change > 0:
                    change_class = "market-card-change-up"
                    arrow = "▲"
                elif change < 0:
                    change_class = "market-card-change-down"
                    arrow = "▼"
                else:
                    change_class = "market-card-change-flat"
                    arrow = "—"

                with col:

                    st.markdown(
                        f"""<div class="market-card">
<div class="market-card-title">
{coin.get("name", "")} · {coin.get("symbol", "").upper()}
</div>
<div class="market-card-price">
${price:,.2f}
</div>
<div class="{change_class}">
{arrow} {change:.2f}%
</div>
</div>""",
                        unsafe_allow_html=True,
                    )

                    if st.button(
                        "تحليل" if AR else "Analyze",
                        key=f"crypto_{coin['id']}",
                        use_container_width=True,
                    ):
                        st.session_state.selected_asset = coin["id"]
                        st.session_state.selected_symbol = coin.get(
                            "symbol",
                            "",
                        ).upper()

    # -----------------------------------------------------
    # SEARCH
    # -----------------------------------------------------

    st.markdown(
        f'<div class="section-title">🔎 {T["search"]}</div>',
        unsafe_allow_html=True,
    )

    crypto_query = st.text_input(
        T["search_crypto"],
        placeholder=(
            "Bitcoin / Ethereum / XRP / Avalanche..."
        ),
    )

    if crypto_query.strip():

        with st.spinner(T["loading"]):

            results = search_crypto(
                crypto_query.strip()
            )

        if results:

            options = {
                f"{x['name']} ({x['symbol'].upper()})": x["id"]
                for x in results
            }

            selected_label = st.selectbox(
                T["select_asset"],
                list(options.keys()),
            )

            st.session_state.selected_asset = options[
                selected_label
            ]

    # -----------------------------------------------------
    # SELECTED CRYPTO ANALYSIS
    # -----------------------------------------------------

    selected_crypto = st.session_state.selected_asset

    if selected_crypto:

        selected_data = fetch_crypto_market(
            [selected_crypto]
        )

        history = fetch_crypto_history(
            selected_crypto
        )

        if selected_data:

            coin = selected_data[0]

            price = coin.get(
                "current_price",
                0,
            ) or 0

            change = (
                coin.get(
                    "price_change_percentage_24h",
                    0,
                )
                or 0
            )

            high = coin.get(
                "high_24h",
                price,
            ) or price

            low = coin.get(
                "low_24h",
                price,
            ) or price

            volume = coin.get(
                "total_volume",
                0,
            ) or 0

            market_cap = coin.get(
                "market_cap",
                0,
            ) or 0

            st.divider()

            st.markdown(
                f"""<div class="section-title">
⚡ {coin.get("name", selected_crypto)}
({coin.get("symbol", "").upper()})
</div>""",
                unsafe_allow_html=True,
            )

            c1, c2, c3, c4 = st.columns(4)

            c1.metric(
                T["price"],
                f"${price:,.2f}",
                f"{change:.2f}%",
            )

            c2.metric(
                T["high"],
                f"${high:,.2f}",
            )

            c3.metric(
                T["low"],
                f"${low:,.2f}",
            )

            c4.metric(
                T["volume"],
                f"${volume / 1e6:,.1f}M",
            )

            chart_col, side_col = st.columns(
                [2.3, 1]
            )

            with chart_col:

                st.markdown(
                    f"#### 📈 {T['chart']}"
                )

                if history:

                    history_df = pd.DataFrame(
                        history
                    )

                    history_df["date"] = pd.to_datetime(
                        history_df["timestamp"],
                        unit="s",
                    )

                    history_df = history_df.set_index(
                        "date"
                    )

                    st.line_chart(
                        history_df["price"],
                        use_container_width=True,
                    )

                else:
                    st.info(
                        "Historical data unavailable."
                    )

            with side_col:

                st.markdown(
                    f"#### 📌 {T['overview']}"
                )

                st.metric(
                    T["market_cap"],
                    f"${market_cap / 1e9:,.2f}B",
                )

                rank = coin.get(
                    "market_cap_rank"
                )

                st.metric(
                    T["rank"],
                    str(rank)
                    if rank
                    else "N/A",
                )

                st.metric(
                    T["change"],
                    f"{change:.2f}%",
                )

            # -------------------------------------------------
            # INDICATORS
            # -------------------------------------------------

            st.markdown(
                f"#### 📐 {T['indicators']}"
            )

            if history:

                hdf = pd.DataFrame(history)

                closes = hdf["price"].astype(float)

                delta = closes.diff()

                gain = delta.clip(lower=0)
                loss = -delta.clip(upper=0)

                avg_gain = gain.rolling(
                    14
                ).mean()

                avg_loss = loss.rolling(
                    14
                ).mean()

                rs = avg_gain / avg_loss.replace(
                    0,
                    pd.NA,
                )

                rsi_series = 100 - (
                    100 / (1 + rs)
                )

                rsi = (
                    float(rsi_series.iloc[-1])
                    if pd.notna(rsi_series.iloc[-1])
                    else 50.0
                )

                ema12 = closes.ewm(
                    span=12,
                    adjust=False,
                ).mean()

                ema26 = closes.ewm(
                    span=26,
                    adjust=False,
                ).mean()

                macd_series = ema12 - ema26

                macd = float(
                    macd_series.iloc[-1]
                )

                trend_points = 50

                if change > 0:
                    trend_points += min(
                        change * 4,
                        20,
                    )
                else:
                    trend_points += max(
                        change * 4,
                        -20,
                    )

                if rsi > 55:
                    trend_points += 10
                elif rsi < 45:
                    trend_points -= 10

                if macd > 0:
                    trend_points += 10
                else:
                    trend_points -= 10

                trend_score = int(
                    max(
                        0,
                        min(
                            100,
                            trend_points,
                        ),
                    )
                )

                i1, i2, i3 = st.columns(3)

                i1.metric(
                    T["rsi"],
                    f"{rsi:.2f}",
                )

                i2.metric(
                    T["macd"],
                    f"{macd:.4f}",
                )

                i3.metric(
                    T["trend"],
                    f"{trend_score}/100",
                )

                # -------------------------------------------------
                # DECISION ENGINE
                # -------------------------------------------------

                if (
                    trend_score >= 65
                    and change > 0
                ):
                    signal = T["bullish"]
                    scenario = (
                        "الزخم يميل للإيجابية، "
                        "لكن استمرار الحركة يحتاج تأكيدًا "
                        "من الحجم والمقاومات."
                        if AR
                        else
                        "Momentum is positive, but continuation "
                        "needs confirmation from volume and resistance."
                    )
                    accent = "#34D399"

                elif trend_score <= 40:
                    signal = T["bearish"]
                    scenario = (
                        "الضغط قصير الأجل سلبي. "
                        "مراقبة مناطق الدعم أفضل من اعتبار الحركة "
                        "اتجاهًا مؤكدًا."
                        if AR
                        else
                        "Short-term pressure is negative. "
                        "Support levels should be monitored before "
                        "assuming a confirmed downtrend."
                    )
                    accent = "#F87171"

                else:
                    signal = T["neutral"]
                    scenario = (
                        "السوق في حالة توازن نسبي. "
                        "اختراق مصحوب بحجم أعلى قد يعطي إشارة أوضح."
                        if AR
                        else
                        "The market is relatively balanced. "
                        "A breakout with stronger volume may provide "
                        "a clearer directional signal."
                    )
                    accent = "#58A6FF"

                st.markdown(
                    f"""<div class="ai-box" style="border-left-color:{accent};">
<div class="ai-title" style="color:{accent};">
⚡ {T["decision"]}
</div>
<p class="ai-text">
<b>{T["signal"]}:</b> {signal}
</p>
<p class="ai-text">
<b>{T["score"]}:</b> {trend_score}/100
</p>
<p class="ai-text">
<b>{T["scenario"]}:</b> {scenario}
</p>
<div class="small-note">
{T["not_advice"]}
</div>
</div>""",
                    unsafe_allow_html=True,
                )


# =========================================================
# US STOCKS
# =========================================================

elif market_type == T["stocks"]:

    st.markdown(
        f'<div class="section-title">🇺🇸 {T["overview"]}</div>',
        unsafe_allow_html=True,
    )

    default_stocks = [
        "AAPL",
        "MSFT",
        "GOOGL",
        "AMZN",
        "TSLA",
        "NVDA",
        "META",
    ]

    stocks = fetch_us_stocks(
        default_stocks
    )

    # -----------------------------------------------------
    # 7 DEFAULT STOCKS
    # -----------------------------------------------------

    st.markdown(
        f'<div class="section-title">📈 {T["top_assets"]}</div>',
        unsafe_allow_html=True,
    )

    if stocks:

        rows = [
            stocks[i:i + 4]
            for i in range(0, len(stocks), 4)
        ]

        for row_index, row in enumerate(rows):

            cols = st.columns(len(row))

            for col, stock in zip(cols, row):

                symbol = stock["symbol"]
                price = stock["current_price"]
                change = stock[
                    "price_change_percentage_24h"
                ]

                if change > 0:
                    change_class = "market-card-change-up"
                    arrow = "▲"
                elif change < 0:
                    change_class = "market-card-change-down"
                    arrow = "▼"
                else:
                    change_class = "market-card-change-flat"
                    arrow = "—"

                with col:

                    st.markdown(
                        f"""<div class="market-card">
<div class="market-card-title">
🇺🇸 {symbol}
</div>
<div class="market-card-price">
${price:,.2f}
</div>
<div class="{change_class}">
{arrow} {change:.2f}%
</div>
</div>""",
                        unsafe_allow_html=True,
                    )

                    if st.button(
                        "تحليل" if AR else "Analyze",
                        key=f"stock_{symbol}",
                        use_container_width=True,
                    ):
                        st.session_state.selected_asset = symbol
                        st.session_state.selected_symbol = symbol

    # -----------------------------------------------------
    # STOCK SEARCH
    # -----------------------------------------------------

    st.markdown(
        f'<div class="section-title">🔎 {T["search"]}</div>',
        unsafe_allow_html=True,
    )

    stock_query = st.text_input(
        T["search_stock"],
        placeholder="AAPL / NVDA / AMD / JPM / AVGO...",
    )

    if stock_query.strip():

        st.session_state.selected_asset = (
            stock_query.strip().upper()
        )

    selected_stock = st.session_state.selected_asset

    # -----------------------------------------------------
    # STOCK ANALYSIS
    # -----------------------------------------------------

    if selected_stock:

        stock_data = fetch_us_stocks(
            [selected_stock]
        )

        if stock_data:

            stock = stock_data[0]

            price = stock["current_price"]
            change = stock[
                "price_change_percentage_24h"
            ]

            high = stock["high_24h"]
            low = stock["low_24h"]
            volume = stock.get(
                "volume",
                0,
            )

            history = fetch_stock_history(
                selected_stock
            )

            st.divider()

            st.markdown(
                f"""<div class="section-title">
⚡ {selected_stock} · {T["decision"]}
</div>""",
                unsafe_allow_html=True,
            )

            c1, c2, c3, c4 = st.columns(4)

            c1.metric(
                T["price"],
                f"${price:,.2f}",
                f"{change:.2f}%",
            )

            c2.metric(
                T["high"],
                f"${high:,.2f}",
            )

            c3.metric(
                T["low"],
                f"${low:,.2f}",
            )

            c4.metric(
                T["volume"],
                f"{volume / 1e6:,.1f}M",
            )

            chart_col, side_col = st.columns(
                [2.3, 1]
            )

            with chart_col:

                st.markdown(
                    f"#### 📈 {T['chart']}"
                )

                if history:

                    hdf = pd.DataFrame(
                        history
                    )

                    hdf["date"] = pd.to_datetime(
                        hdf["timestamp"],
                        unit="s",
                    )

                    hdf = hdf.set_index(
                        "date"
                    )

                    st.line_chart(
                        hdf["price"],
                        use_container_width=True,
                    )

                else:

                    st.info(
                        "Historical data unavailable."
                    )

            with side_col:

                st.markdown(
                    f"#### 📌 {T['session']}"
                )

                st.metric(
                    T["high"],
                    f"${high:,.2f}",
                )

                st.metric(
                    T["low"],
                    f"${low:,.2f}",
                )

                st.metric(
                    T["change"],
                    f"{change:.2f}%",
                )

            # -------------------------------------------------
            # TECHNICAL INDICATORS
            # -------------------------------------------------

            st.markdown(
                f"#### 📐 {T['indicators']}"
            )

            if history:

                hdf = pd.DataFrame(history)

                closes = hdf[
                    "price"
                ].astype(float)

                delta = closes.diff()

                gain = delta.clip(
                    lower=0
                )

                loss = -delta.clip(
                    upper=0
                )

                avg_gain = gain.rolling(
                    14
                ).mean()

                avg_loss = loss.rolling(
                    14
                ).mean()

                rs = avg_gain / avg_loss.replace(
                    0,
                    pd.NA,
                )

                rsi_series = 100 - (
                    100 / (1 + rs)
                )

                rsi = (
                    float(rsi_series.iloc[-1])
                    if pd.notna(
                        rsi_series.iloc[-1]
                    )
                    else 50.0
                )

                ema12 = closes.ewm(
                    span=12,
                    adjust=False,
                ).mean()

                ema26 = closes.ewm(
                    span=26,
                    adjust=False,
                ).mean()

                macd_series = (
                    ema12 - ema26
                )

                macd = float(
                    macd_series.iloc[-1]
                )

                trend_points = 50

                if change > 0:
                    trend_points += min(
                        change * 4,
                        20,
                    )
                else:
                    trend_points += max(
                        change * 4,
                        -20,
                    )

                if rsi > 55:
                    trend_points += 10
                elif rsi < 45:
                    trend_points -= 10

                if macd > 0:
                    trend_points += 10
                else:
                    trend_points -= 10

                trend_score = int(
                    max(
                        0,
                        min(
                            100,
                            trend_points,
                        ),
                    )
                )

                i1, i2, i3 = st.columns(3)

                i1.metric(
                    T["rsi"],
                    f"{rsi:.2f}",
                )

                i2.metric(
                    T["macd"],
                    f"{macd:.4f}",
                )

                i3.metric(
                    T["trend"],
                    f"{trend_score}/100",
                )

                if (
                    trend_score >= 65
                    and change > 0
                ):

                    signal = T["bullish"]

                    scenario = (
                        "الزخم يميل للإيجابية، "
                        "مع ضرورة مراقبة الحجم والمقاومات."
                        if AR
                        else
                        "Momentum is positive; "
                        "volume and resistance should be monitored."
                    )

                    accent = "#34D399"

                elif trend_score <= 40:

                    signal = T["bearish"]

                    scenario = (
                        "الضغط قصير الأجل سلبي، "
                        "ومراقبة الدعم ضرورية."
                        if AR
                        else
                        "Short-term pressure is negative; "
                        "support levels should be monitored."
                    )

                    accent = "#F87171"

                else:

                    signal = T["neutral"]

                    scenario = (
                        "الحركة متوازنة نسبيًا. "
                        "اختراق واضح مع حجم أعلى يعطي تأكيدًا أفضل."
                        if AR
                        else
                        "Price action is relatively balanced. "
                        "A breakout with stronger volume would provide "
                        "better confirmation."
                    )

                    accent = "#58A6FF"

                st.markdown(
                    f"""<div class="ai-box" style="border-left-color:{accent};">
<div class="ai-title" style="color:{accent};">
⚡ {T["decision"]}: {selected_stock}
</div>
<p class="ai-text">
<b>{T["signal"]}:</b> {signal}
</p>
<p class="ai-text">
<b>{T["score"]}:</b> {trend_score}/100
</p>
<p class="ai-text">
<b>{T["scenario"]}:</b> {scenario}
</p>
<div class="small-note">
{T["not_advice"]}
</div>
</div>""",
                    unsafe_allow_html=True,
                )

        else:

            st.error(
                f"{T['no_result']} {selected_stock}"
            )
