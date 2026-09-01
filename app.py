import streamlit as st
import pandas as pd
import html
from datetime import datetime

from data_fetcher import (
    search_crypto,
    fetch_crypto_market,
    fetch_crypto_ohlc,
    fetch_crypto_global,
    fetch_us_stocks,
    fetch_stock_history,
    fetch_crypto_fear_greed,
    fetch_sector_data,
    fetch_etf_data,
)

st.set_page_config(
    page_title="Capi | Decision Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# SESSION STATE
# =========================================================

if "selected_crypto" not in st.session_state:
    st.session_state.selected_crypto = "bitcoin"

if "selected_stock" not in st.session_state:
    st.session_state.selected_stock = "NVDA"


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

T = {
    "ar": {
        "crypto": "العملات الرقمية",
        "stocks": "الأسهم الأمريكية",
        "market": "السوق",
        "overview": "نظرة السوق",
        "top": "الأصول الرئيسية",
        "search": "البحث عن أصل",
        "search_crypto": "ابحث عن عملة رقمية",
        "search_stock": "أدخل رمز السهم",
        "refresh": "تحديث البيانات",
        "sentiment": "مؤشر الخوف والطمع",
        "market_cap": "القيمة السوقية",
        "updated": "آخر تحديث",
        "analyze": "تحليل",
        "price": "السعر الحالي",
        "change": "التغير 24 ساعة",
        "high": "أعلى سعر",
        "low": "أدنى سعر",
        "volume": "حجم التداول",
        "chart": "الرسم السعري",
        "candles": "الشموع اليابانية",
        "analysis": "التحليل العميق",
        "indicators": "المؤشرات الفنية",
        "rsi": "RSI",
        "macd": "MACD",
        "volatility": "التقلب",
        "trend": "درجة الاتجاه",
        "opportunity": "درجة الفرصة",
        "entry": "منطقة دخول محتملة",
        "exit": "منطقة خروج محتملة",
        "support": "الدعم",
        "resistance": "المقاومة",
        "decision": "قرار Capi",
        "scenario": "السيناريو البديل",
        "sector": "تحليل القطاع",
        "sector_strength": "قوة القطاع",
        "relative": "القوة النسبية",
        "funds": "الصناديق / ETFs",
        "status": "حالة السوق",
        "bullish": "إيجابي",
        "neutral": "محايد",
        "bearish": "سلبي",
        "no_data": "لا تتوفر بيانات كافية لهذا الأصل.",
        "not_advice": "تحليل معلوماتي مبني على بيانات السوق، وليس توصية مالية.",
    },
    "en": {
        "crypto": "Cryptocurrency",
        "stocks": "US Equities",
        "market": "Market",
        "overview": "Market Overview",
        "top": "Top Assets",
        "search": "Search Asset",
        "search_crypto": "Search cryptocurrency",
        "search_stock": "Enter stock symbol",
        "refresh": "Refresh Data",
        "sentiment": "Fear & Greed",
        "market_cap": "Market Cap",
        "updated": "Last Update",
        "analyze": "Analyze",
        "price": "Current Price",
        "change": "24h Change",
        "high": "24h High",
        "low": "24h Low",
        "volume": "Volume",
        "chart": "Price Chart",
        "candles": "Candlestick Chart",
        "analysis": "Deep Analysis",
        "indicators": "Technical Indicators",
        "rsi": "RSI",
        "macd": "MACD",
        "volatility": "Volatility",
        "trend": "Trend Score",
        "opportunity": "Opportunity Score",
        "entry": "Potential Entry Zone",
        "exit": "Potential Exit Zone",
        "support": "Support",
        "resistance": "Resistance",
        "decision": "Capi Decision",
        "scenario": "Alternative Scenario",
        "sector": "Sector Analysis",
        "sector_strength": "Sector Strength",
        "relative": "Relative Strength",
        "funds": "Funds / ETFs",
        "status": "Market Status",
        "bullish": "Bullish",
        "neutral": "Neutral",
        "bearish": "Bearish",
        "no_data": "Not enough data is available for this asset.",
        "not_advice": "Informational market analysis, not financial advice.",
    },
}["ar" if AR else "en"]


# =========================================================
# RESPONSIVE THEME
# =========================================================

st.markdown(
    """
<style>

.stApp {
    background: #F5F7FA;
    color: #111827;
}

.block-container {
    max-width: 1280px;
    padding-top: 1rem;
    padding-bottom: 3rem;
}

.capi-header {
    background: linear-gradient(145deg, #ffffff, #eef2f7);
    border: 1px solid #dce2ea;
    border-radius: 22px;
    padding: 25px 22px 20px;
    text-align: center;
    margin-bottom: 16px;
    box-shadow: 0 10px 30px rgba(15,23,42,.08);
}

.capi-title {
    color: #111827;
    font-size: 34px;
    font-weight: 850;
    margin: 0;
}

.capi-subtitle {
    color: #64748b;
    font-size: 12px;
    letter-spacing: 1.2px;
    margin-top: 6px;
}

.sentiment-bar {
    background: linear-gradient(145deg,#ffffff,#f1f5f9);
    border: 1px solid #dce2ea;
    border-radius: 15px;
    padding: 13px 17px;
    margin-bottom: 18px;
}

.card {
    background: #ffffff;
    border: 1px solid #dfe5ec;
    border-radius: 16px;
    padding: 14px;
    min-height: 105px;
    box-shadow: 0 7px 22px rgba(15,23,42,.06);
}

.card-name {
    color: #64748b;
    font-size: 12px;
}

.card-price {
    color: #111827;
    font-size: 19px;
    font-weight: 800;
    margin-top: 5px;
}

.up {
    color: #059669;
    font-size: 12px;
    font-weight: 800;
}

.down {
    color: #dc2626;
    font-size: 12px;
    font-weight: 800;
}

.flat {
    color: #64748b;
    font-size: 12px;
    font-weight: 800;
}

.info {
    background: #ffffff;
    border: 1px solid #dfe5ec;
    border-radius: 16px;
    padding: 16px;
    text-align: center;
}

.info-label {
    color: #64748b;
    font-size: 11px;
}

.info-value {
    color: #111827;
    font-size: 22px;
    font-weight: 850;
    margin-top: 4px;
}

.ai {
    background: linear-gradient(145deg,#ffffff,#f3f6fa);
    border: 1px solid #dce3eb;
    border-left: 5px solid #2563eb;
    border-radius: 18px;
    padding: 20px;
    margin-top: 16px;
    box-shadow: 0 10px 28px rgba(15,23,42,.07);
}

.mini {
    color: #64748b;
    font-size: 11px;
}

.section {
    color: #1f2937;
    font-size: 20px;
    font-weight: 800;
    margin: 17px 0 11px;
}

.zone {
    border-radius: 14px;
    padding: 14px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    text-align: center;
}

.zone-label {
    font-size: 11px;
    color: #64748b;
}

.zone-value {
    font-size: 18px;
    font-weight: 850;
    color: #111827;
}

.candle-wrap {
    background: #ffffff;
    border: 1px solid #dfe5ec;
    border-radius: 17px;
    padding: 8px;
    overflow: hidden;
}

@media (prefers-color-scheme: dark) {

    .stApp {
        background: #090c12;
        color: #e5e7eb;
    }

    .capi-header {
        background: linear-gradient(145deg,#151a24,#0d1118);
        border-color: #252d3b;
        box-shadow: 0 12px 35px rgba(0,0,0,.3);
    }

    .capi-title {
        color: #f8fafc;
    }

    .capi-subtitle,
    .card-name,
    .info-label,
    .zone-label,
    .mini {
        color: #94a3b8;
    }

    .sentiment-bar,
    .card,
    .info,
    .candle-wrap {
        background: #111620;
        border-color: #273141;
        box-shadow: 0 8px 25px rgba(0,0,0,.22);
    }

    .card-price,
    .info-value,
    .zone-value {
        color: #f8fafc;
    }

    .section {
        color: #e5e7eb;
    }

    .ai {
        background: linear-gradient(145deg,#141a25,#0d1118);
        border-color: #2a3444;
    }

    .zone {
        background: #0f141c;
        border-color: #273141;
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
    """
<div class="capi-header">
    <h1 class="capi-title">⚡ Capi Decision Intelligence</h1>
    <div class="capi-subtitle">
        ADVANCED MULTI-MARKET ANALYTICS
    </div>
</div>
""",
    unsafe_allow_html=True,
)


# =========================================================
# HELPERS
# =========================================================

def fmt_money(value):
    if value is None:
        return "N/A"

    value = float(value)

    if abs(value) >= 1000:
        return f"${value:,.0f}"

    if abs(value) >= 1:
        return f"${value:,.2f}"

    return f"${value:,.4f}"


def fmt_volume(value):
    value = float(value or 0)

    if value >= 1e9:
        return f"${value / 1e9:.2f}B"

    if value >= 1e6:
        return f"${value / 1e6:.1f}M"

    if value >= 1e3:
        return f"${value / 1e3:.1f}K"

    return f"${value:,.0f}"


# =========================================================
# TECHNICAL ANALYSIS
# =========================================================

def indicators_from_ohlc(rows):

    if not rows:
        return None

    df = pd.DataFrame(rows).copy()

    for col in [
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]:
        if col in df:
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce",
            )

    df = df.dropna(
        subset=["close"]
    )

    if len(df) < 20:
        return None

    close = df["close"]

    delta = close.diff()

    gain = (
        delta
        .clip(lower=0)
        .rolling(14)
        .mean()
    )

    loss = (
        -delta
        .clip(upper=0)
        .rolling(14)
        .mean()
    )

    rs = gain / loss.replace(0, pd.NA)

    rsi_series = 100 - (
        100 / (1 + rs)
    )

    rsi = (
        float(rsi_series.iloc[-1])
        if pd.notna(rsi_series.iloc[-1])
        else 50.0
    )

    ema12 = close.ewm(
        span=12,
        adjust=False,
    ).mean()

    ema26 = close.ewm(
        span=26,
        adjust=False,
    ).mean()

    macd_series = ema12 - ema26

    signal_series = (
        macd_series
        .ewm(span=9, adjust=False)
        .mean()
    )

    macd = float(
        macd_series.iloc[-1]
    )

    macd_signal = float(
        signal_series.iloc[-1]
    )

    returns = (
        close
        .pct_change()
        .dropna()
    )

    volatility = (
        float(
            returns.tail(30).std() * 100
        )
        if len(returns)
        else 0.0
    )

    support = float(
        df["low"]
        .tail(30)
        .min()
    )

    resistance = float(
        df["high"]
        .tail(30)
        .max()
    )

    current = float(
        close.iloc[-1]
    )

    previous = float(
        close.iloc[-2]
    )

    momentum = (
        ((current - previous) / previous) * 100
        if previous
        else 0
    )

    score = 50.0

    score += max(
        -15,
        min(15, momentum * 3),
    )

    if rsi >= 55:
        score += 10
    elif rsi <= 45:
        score -= 10

    if macd > macd_signal:
        score += 10
    else:
        score -= 10

    ema20 = (
        close
        .ewm(span=20, adjust=False)
        .mean()
        .iloc[-1]
    )

    if current > ema20:
        score += 10
    else:
        score -= 10

    trend_score = int(
        max(
            0,
            min(
                100,
                round(score),
            ),
        )
    )

    opportunity = trend_score

    if rsi > 70:
        opportunity -= 8

    if rsi < 30:
        opportunity += 4

    if volatility > 5:
        opportunity -= 5

    opportunity = int(
        max(
            0,
            min(
                100,
                opportunity,
            ),
        )
    )

    # -----------------------------------------------------
    # Entry / Exit zones
    # -----------------------------------------------------

    entry_low = support

    entry_high = min(
        current,
        support
        + (resistance - support) * 0.35,
    )

    if entry_high < entry_low:
        entry_low = current
        entry_high = current

    exit_low = max(
        current,
        resistance
        - (resistance - support) * 0.25,
    )

    exit_high = resistance

    if exit_high < exit_low:
        exit_low = current
        exit_high = current

    # -----------------------------------------------------
    # Market regime
    # -----------------------------------------------------

    if trend_score >= 65:

        regime = (
            "إيجابي"
            if AR
            else "Bullish"
        )

        signal = T["bullish"]

        accent = "#10B981"

    elif trend_score <= 40:

        regime = (
            "سلبي"
            if AR
            else "Bearish"
        )

        signal = T["bearish"]

        accent = "#EF4444"

    else:

        regime = (
            "محايد"
            if AR
            else "Neutral"
        )

        signal = T["neutral"]

        accent = "#3B82F6"

    if AR:

        scenario = (
            "إذا فشل السعر في الثبات فوق منطقة الدعم، "
            "فقد يعود لاختبار الدعم التالي. "
            "اختراق المقاومة بحجم أقوى يحسن التأكيد."
        )

    else:

        scenario = (
            "Failure to hold support may lead to a "
            "retest of lower support. A breakout above "
            "resistance with stronger volume improves confirmation."
        )

    return {
        "df": df,
        "rsi": rsi,
        "macd": macd,
        "macd_signal": macd_signal,
        "volatility": volatility,
        "support": support,
        "resistance": resistance,
        "trend_score": trend_score,
        "opportunity": opportunity,
        "entry_low": entry_low,
        "entry_high": entry_high,
        "exit_low": exit_low,
        "exit_high": exit_high,
        "regime": regime,
        "signal": signal,
        "accent": accent,
        "scenario": scenario,
    }


# =========================================================
# CANDLESTICK SVG
# =========================================================

def candle_svg(
    rows,
    width=900,
    height=430,
):

    if not rows:
        return ""

    df = pd.DataFrame(
        rows
    ).copy()

    for col in [
        "open",
        "high",
        "low",
        "close",
    ]:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce",
        )

    df = df.dropna(
        subset=[
            "open",
            "high",
            "low",
            "close",
        ]
    ).tail(60)

    if df.empty:
        return ""

    lo = float(
        df["low"].min()
    )

    hi = float(
        df["high"].max()
    )

    pad = (
        (hi - lo) * 0.06
        or max(
            abs(hi) * 0.01,
            1,
        )
    )

    lo -= pad
    hi += pad

    left = 45
    right = 15
    top = 18
    bottom = 35

    plot_w = (
        width - left - right
    )

    plot_h = (
        height - top - bottom
    )

    step = (
        plot_w / max(len(df), 1)
    )

    body_w = max(
        3,
        step * 0.58,
    )

    def y(value):
        return (
            top
            + (
                hi - float(value)
            )
            / (
                hi - lo
            )
            * plot_h
        )

    parts = [
        f'<svg viewBox="0 0 {width} {height}" '
        f'width="100%" '
        f'xmlns="http://www.w3.org/2000/svg">'
    ]

    for i, row in enumerate(
        df.itertuples(
            index=False
        )
    ):

        x = (
            left
            + i * step
            + step / 2
        )

        yo = y(row.open)
        yc = y(row.close)
        yh = y(row.high)
        yl = y(row.low)

        up = row.close >= row.open

        stroke = (
            "#10B981"
            if up
            else "#EF4444"
        )

        fill = (
            stroke
            if up
            else "transparent"
        )

        parts.append(
            f'<line '
            f'x1="{x:.2f}" '
            f'y1="{yh:.2f}" '
            f'x2="{x:.2f}" '
            f'y2="{yl:.2f}" '
            f'stroke="{stroke}" '
            f'stroke-width="1.3"/>'
        )

        body_y = min(
            yo,
            yc,
        )

        body_h = max(
            1.5,
            abs(yc - yo),
        )

        parts.append(
            f'<rect '
            f'x="{x-body_w/2:.2f}" '
            f'y="{body_y:.2f}" '
            f'width="{body_w:.2f}" '
            f'height="{body_h:.2f}" '
            f'fill="{fill}" '
            f'stroke="{stroke}" '
            f'stroke-width="1.2" '
            f'rx="1"/>'
        )

    parts.append(
        f'<line '
        f'x1="{left}" '
        f'y1="{top}" '
        f'x2="{left}" '
        f'y2="{height-bottom}" '
        f'stroke="#94A3B8" '
        f'stroke-opacity=".35"/>'
    )

    parts.append(
        f'<line '
        f'x1="{left}" '
        f'y1="{height-bottom}" '
        f'x2="{width-right}" '
        f'y2="{height-bottom}" '
        f'stroke="#94A3B8" '
        f'stroke-opacity=".35"/>'
    )

    parts.append("</svg>")

    return "".join(parts)


# =========================================================
# SENTIMENT
# =========================================================

def render_sentiment():

    fear_value, fear_class = (
        fetch_crypto_fear_greed()
    )

    try:
        fv = int(fear_value)
    except Exception:
        fv = 50

    if fv >= 60:
        accent = "#10B981"

    elif fv <= 40:
        accent = "#EF4444"

    else:
        accent = "#3B82F6"

    st.markdown(
        f"""
<div class="sentiment-bar">
<b>{T["sentiment"]}</b>
&nbsp;&nbsp;
<span style="color:{accent};
font-weight:850;
font-size:18px;">
{fv}/100
</span>
&nbsp;
<span class="mini">
{html.escape(str(fear_class))}
</span>
</div>
""",
        unsafe_allow_html=True,
    )


# =========================================================
# SIDEBAR
# =========================================================

market_type = st.sidebar.radio(
    T["market"],
    [
        T["crypto"],
        T["stocks"],
    ],
)

if st.sidebar.button(
    T["refresh"],
    use_container_width=True,
):

    st.cache_data.clear()

    st.rerun()


# Fear & Greed exists on both pages.
render_sentiment()


# =========================================================
# CRYPTO PAGE
# =========================================================

if market_type == T["crypto"]:

    global_data = fetch_crypto_global()

    market_cap = (
        global_data
        .get(
            "total_market_cap",
            {}
        )
        .get(
            "usd",
            0,
        )
        if global_data
        else 0
    )

    a, b, c = st.columns(3)

    with a:

        st.markdown(
            f"""
<div class="info">
<div class="info-label">
{T["market_cap"]}
</div>
<div class="info-value">
${market_cap / 1e12:.2f}T
</div>
</div>
""",
            unsafe_allow_html=True,
        )

    with b:

        st.markdown(
            f"""
<div class="info">
<div class="info-label">
{T["status"]}
</div>
<div class="info-value">
Crypto
</div>
</div>
""",
            unsafe_allow_html=True,
        )

    with c:

        st.markdown(
            f"""
<div class="info">
<div class="info-label">
{T["updated"]}
</div>
<div class="info-value"
style="font-size:17px;">
{datetime.now().strftime("%H:%M")}
</div>
</div>
""",
            unsafe_allow_html=True,
        )

    default_ids = [
        "bitcoin",
        "ethereum",
        "solana",
        "ripple",
        "cardano",
        "binancecoin",
        "dogecoin",
    ]

    coins = fetch_crypto_market(
        default_ids
    )

    st.markdown(
        f'<div class="section">🪙 '
        f'{T["top"]}</div>',
        unsafe_allow_html=True,
    )

    if coins:

        rows = [
            coins[i:i + 4]
            for i in range(
                0,
                len(coins),
                4,
            )
        ]

        for row in rows:

            cols = st.columns(
                len(row)
            )

            for col, coin in zip(
                cols,
                row,
            ):

                price = (
                    coin.get(
                        "current_price",
                        0,
                    )
                    or 0
                )

                chg = (
                    coin.get(
                        "price_change_percentage_24h",
                        0,
                    )
                    or 0
                )

                cls = (
                    "up"
                    if chg > 0
                    else (
                        "down"
                        if chg < 0
                        else "flat"
                    )
                )

                with col:

                    st.markdown(
                        f"""
<div class="card">
<div class="card-name">
{html.escape(
    coin.get("name", "")
)}
 ·
{html.escape(
    coin.get(
        "symbol",
        ""
    ).upper()
)}
</div>

<div class="card-price">
{fmt_money(price)}
</div>

<div class="{cls}">
{chg:+.2f}%
</div>
</div>
""",
                        unsafe_allow_html=True,
                    )

                    if st.button(
                        T["analyze"],
                        key=f'c_{coin["id"]}',
                        use_container_width=True,
                    ):

                        st.session_state.selected_crypto = (
                            coin["id"]
                        )

                        st.rerun()

    # -----------------------------------------------------
    # Search
    # -----------------------------------------------------

    st.markdown(
        f'<div class="section">🔎 '
        f'{T["search"]}</div>',
        unsafe_allow_html=True,
    )

    query = st.text_input(
        T["search_crypto"],
        placeholder=(
            "Bitcoin / XRP / Avalanche / Chainlink..."
        ),
    )

    if query.strip():

        results = search_crypto(
            query.strip()
        )

        if results:

            labels = {
                f'{x["name"]} '
                f'({x["symbol"].upper()})':
                x["id"]
                for x in results
            }

            selected = st.selectbox(
                "Select",
                list(labels.keys()),
            )

            if selected:

                st.session_state.selected_crypto = (
                    labels[selected]
                )

        else:

            st.warning(
                T["no_data"]
            )

    # -----------------------------------------------------
    # Selected crypto
    # -----------------------------------------------------

    selected_id = (
        st.session_state.selected_crypto
    )

    data = fetch_crypto_market(
        [selected_id]
    )

    if data:

        coin = data[0]

        ohlc = fetch_crypto_ohlc(
            selected_id
        )

        tech = indicators_from_ohlc(
            ohlc
        )

        if tech:

            price = float(
                coin.get(
                    "current_price",
                    0,
                )
                or 0
            )

            chg = float(
                coin.get(
                    "price_change_percentage_24h",
                    0,
                )
                or 0
            )

            high = float(
                coin.get(
                    "high_24h",
                    price,
                )
                or price
            )

            low = float(
                coin.get(
                    "low_24h",
                    price,
                )
                or price
            )

            volume = float(
                coin.get(
                    "total_volume",
                    0,
                )
                or 0
            )

            st.divider()

            st.markdown(
                f'<div class="section">⚡ '
                f'{html.escape(coin.get("name",""))} '
                f'· '
                f'{html.escape(coin.get("symbol","").upper())}'
                f'</div>',
                unsafe_allow_html=True,
            )

            m1, m2, m3, m4 = st.columns(4)

            m1.metric(
                T["price"],
                fmt_money(price),
                f"{chg:+.2f}%",
            )

            m2.metric(
                T["high"],
                fmt_money(high),
            )

            m3.metric(
                T["low"],
                fmt_money(low),
            )

            m4.metric(
                T["volume"],
                fmt_volume(volume),
            )

            # -------------------------------------------------
            # Candles
            # -------------------------------------------------

            st.markdown(
                f"#### 🕯️ {T['candles']}"
            )

            svg = candle_svg(
                ohlc
            )

            if svg:

                st.markdown(
                    f'<div class="candle-wrap">'
                    f'{svg}'
                    f'</div>',
                    unsafe_allow_html=True,
                )

            # -------------------------------------------------
            # Entry / Exit
            # -------------------------------------------------

            z1, z2, z3, z4 = st.columns(4)

            z1.markdown(
                f"""
<div class="zone">
<div class="zone-label">
{T["entry"]}
</div>
<div class="zone-value">
{fmt_money(
    tech["entry_low"]
)}
—
{fmt_money(
    tech["entry_high"]
)}
</div>
</div>
""",
                unsafe_allow_html=True,
            )

            z2.markdown(
                f"""
<div class="zone">
<div class="zone-label">
{T["exit"]}
</div>
<div class="zone-value">
{fmt_money(
    tech["exit_low"]
)}
—
{fmt_money(
    tech["exit_high"]
)}
</div>
</div>
""",
                unsafe_allow_html=True,
            )

            z3.markdown(
                f"""
<div class="zone">
<div class="zone-label">
{T["support"]}
</div>
<div class="zone-value">
{fmt_money(
    tech["support"]
)}
</div>
</div>
""",
                unsafe_allow_html=True,
            )

            z4.markdown(
                f"""
<div class="zone">
<div class="zone-label">
{T["resistance"]}
</div>
<div class="zone-value">
{fmt_money(
    tech["resistance"]
)}
</div>
</div>
""",
                unsafe_allow_html=True,
            )

            # -------------------------------------------------
            # Indicators
            # -------------------------------------------------

            st.markdown(
                f"#### 📐 {T['indicators']}"
            )

            i1, i2, i3, i4 = st.columns(4)

            i1.metric(
                T["rsi"],
                f'{tech["rsi"]:.2f}',
            )

            i2.metric(
                T["macd"],
                f'{tech["macd"]:.5f}',
            )

            i3.metric(
                T["trend"],
                f'{tech["trend_score"]}/100',
            )

            i4.metric(
                T["opportunity"],
                f'{tech["opportunity"]}/100',
            )

            # -------------------------------------------------
            # Decision
            # -------------------------------------------------

            st.markdown(
                f"""
<div class="ai"
style="border-left-color:{tech["accent"]};">

<div style="
font-size:20px;
font-weight:850;
color:{tech["accent"]};
">
⚡ {T["decision"]}:
{html.escape(coin.get("name",""))}
</div>

<p>
<b>Signal:</b>
{tech["signal"]}
</p>

<p>
<b>{T["status"]}:</b>
{tech["regime"]}
</p>

<p>
<b>{T["scenario"]}:</b>
{tech["scenario"]}
</p>

<div class="mini">
{T["not_advice"]}
</div>

</div>
""",
                unsafe_allow_html=True,
            )


# =========================================================
# US STOCKS PAGE
# =========================================================

else:

    stocks = fetch_us_stocks(
        [
            "AAPL",
            "MSFT",
            "GOOGL",
            "AMZN",
            "TSLA",
            "NVDA",
            "META",
        ]
    )

    st.markdown(
        f'<div class="section">🇺🇸 '
        f'{T["top"]}</div>',
        unsafe_allow_html=True,
    )

    if stocks:

        rows = [
            stocks[i:i + 4]
            for i in range(
                0,
                len(stocks),
                4,
            )
        ]

        for row in rows:

            cols = st.columns(
                len(row)
            )

            for col, stock in zip(
                cols,
                row,
            ):

                symbol = stock["symbol"]

                price = stock[
                    "current_price"
                ]

                chg = stock[
                    "price_change_percentage_24h"
                ]

                cls = (
                    "up"
                    if chg > 0
                    else (
                        "down"
                        if chg < 0
                        else "flat"
                    )
                )

                with col:

                    st.markdown(
                        f"""
<div class="card">

<div class="card-name">
🇺🇸 {symbol}
</div>

<div class="card-price">
{fmt_money(price)}
</div>

<div class="{cls}">
{chg:+.2f}%
</div>

</div>
""",
                        unsafe_allow_html=True,
                    )

                    if st.button(
                        T["analyze"],
                        key=f"s_{symbol}",
                        use_container_width=True,
                    ):

                        st.session_state.selected_stock = (
                            symbol
                        )

                        st.rerun()

    # -----------------------------------------------------
    # Stock search
    # -----------------------------------------------------

    st.markdown(
        f'<div class="section">🔎 '
        f'{T["search"]}</div>',
        unsafe_allow_html=True,
    )

    stock_query = st.text_input(
        T["search_stock"],
        placeholder=(
            "NVDA / AMD / JPM / AVGO / AMZN..."
        ),
    )

    if stock_query.strip():

        st.session_state.selected_stock = (
            stock_query.strip().upper()
        )

    ticker = (
        st.session_state.selected_stock
    )

    stock_result = fetch_us_stocks(
        [ticker]
    )

    if stock_result:

        stock = stock_result[0]

        ohlc = fetch_stock_history(
            ticker
        )

        tech = indicators_from_ohlc(
            ohlc
        )

        if tech:

            price = float(
                stock["current_price"]
            )

            chg = float(
                stock[
                    "price_change_percentage_24h"
                ]
            )

            high = float(
                stock["high_24h"]
            )

            low = float(
                stock["low_24h"]
            )

            volume = float(
                stock.get(
                    "volume",
                    0,
                )
                or 0
            )

            st.divider()

            st.markdown(
                f'<div class="section">⚡ '
                f'{ticker} · '
                f'{T["analysis"]}'
                f'</div>',
                unsafe_allow_html=True,
            )

            m1, m2, m3, m4 = st.columns(4)

            m1.metric(
                T["price"],
                fmt_money(price),
                f"{chg:+.2f}%",
            )

            m2.metric(
                T["high"],
                fmt_money(high),
            )

            m3.metric(
                T["low"],
                fmt_money(low),
            )

            m4.metric(
                T["volume"],
                fmt_volume(volume),
            )

            # -------------------------------------------------
            # Candles
            # -------------------------------------------------

            st.markdown(
                f"#### 🕯️ {T['candles']}"
            )

            svg = candle_svg(
                ohlc
            )

            if svg:

                st.markdown(
                    f'<div class="candle-wrap">'
                    f'{svg}'
                    f'</div>',
                    unsafe_allow_html=True,
                )

            # -------------------------------------------------
            # Entry / Exit
            # -------------------------------------------------

            z1, z2, z3, z4 = st.columns(4)

            z1.markdown(
                f"""
<div class="zone">
<div class="zone-label">
{T["entry"]}
</div>
<div class="zone-value">
{fmt_money(
    tech["entry_low"]
)}
—
{fmt_money(
    tech["entry_high"]
)}
</div>
</div>
""",
                unsafe_allow_html=True,
            )

            z2.markdown(
                f"""
<div class="zone">
<div class="zone-label">
{T["exit"]}
</div>
<div class="zone-value">
{fmt_money(
    tech["exit_low"]
)}
—
{fmt_money(
    tech["exit_high"]
)}
</div>
</div>
""",
                unsafe_allow_html=True,
            )

            z3.markdown(
                f"""
<div class="zone">
<div class="zone-label">
{T["support"]}
</div>
<div class="zone-value">
{fmt_money(
    tech["support"]
)}
</div>
</div>
""",
                unsafe_allow_html=True,
            )

            z4.markdown(
                f"""
<div class="zone">
<div class="zone-label">
{T["resistance"]}
</div>
<div class="zone-value">
{fmt_money(
    tech["resistance"]
)}
</div>
</div>
""",
                unsafe_allow_html=True,
            )

            # -------------------------------------------------
            # Indicators
            # -------------------------------------------------

            st.markdown(
                f"#### 📐 {T['indicators']}"
            )

            i1, i2, i3, i4 = st.columns(4)

            i1.metric(
                T["rsi"],
                f'{tech["rsi"]:.2f}',
            )

            i2.metric(
                T["macd"],
                f'{tech["macd"]:.5f}',
            )

            i3.metric(
                T["trend"],
                f'{tech["trend_score"]}/100',
            )

            i4.metric(
                T["opportunity"],
                f'{tech["opportunity"]}/100',
            )

            # -------------------------------------------------
            # Sector
            # -------------------------------------------------

            st.markdown(
                f"#### 🏢 {T['sector']}"
            )

            sector = fetch_sector_data(
                ticker
            )

            if sector:

                sec1, sec2, sec3 = st.columns(3)

                sec1.metric(
                    T["sector_strength"],
                    f'{sector["score"]}/100',
                )

                sec2.metric(
                    T["relative"],
                    f'{sector["relative_change"]:+.2f}%',
                )

                sec3.metric(
                    "ETF",
                    sector["etf"],
                )

                # -------------------------------------------------
                # ETF
                # -------------------------------------------------

                st.markdown(
                    f"#### 🏦 {T['funds']}"
                )

                if sector.get("etf"):

                    etf = fetch_etf_data(
                        sector["etf"]
                    )

                    if etf:

                        f1, f2, f3 = st.columns(3)

                        f1.metric(
                            "ETF",
                            etf["symbol"],
                        )

                        f2.metric(
                            T["price"],
                            fmt_money(
                                etf["price"]
                            ),
                        )

                        f3.metric(
                            T["change"],
                            f'{etf["change"]:+.2f}%',
                        )

            # -------------------------------------------------
            # Decision
            # -------------------------------------------------

            st.markdown(
                f"""
<div class="ai"
style="border-left-color:{tech["accent"]};">

<div style="
font-size:20px;
font-weight:850;
color:{tech["accent"]};
">
⚡ {T["decision"]}: {ticker}
</div>

<p>
<b>Signal:</b>
{tech["signal"]}
</p>

<p>
<b>{T["status"]}:</b>
{tech["regime"]}
</p>

<p>
<b>{T["scenario"]}:</b>
{tech["scenario"]}
</p>

<div class="mini">
{T["not_advice"]}
</div>

</div>
""",
                unsafe_allow_html=True,
            )

    else:

        st.warning(
            T["no_data"]
        )
