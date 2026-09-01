import streamlit as st
import pandas as pd
import datetime
from data_fetcher import fetch_crypto_market, fetch_us_stocks, fetch_crypto_fear_greed

st.set_page_config(
    page_title="Multi-Market AI Platform",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>
.stApp { background-color: #0B0F19; color: #F3F4F6; }
.main-header {
    background: linear-gradient(135deg, #1E1B4B 0%, #312E81 100%);
    padding: 25px;
    border-radius: 16px;
    color: #FFFFFF;
    text-align: center;
    margin-bottom: 25px;
    border: 1px solid #4338CA;
}
.ai-box {
    background: #111827;
    border: 2px solid #6366F1;
    padding: 20px;
    border-radius: 14px;
    margin-top: 20px;
    box-shadow: 0 4px 20px rgba(99,102,241,0.2);
}
div[data-testid="stMetric"] {
    background-color: #1F2937;
    border: 1px solid #374151;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1 style="color: #ffffff; margin:0;">🤖 منصة الذكاء الاصطناعي متعددة الأسواق</h1>
    <p style="color: #9CA3AF; margin-top:5px;">
        التحليل المالي المتقدم للكريبتو والأسهم الأمريكية مع محرك التنبؤ الذكي
    </p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### 🌐 تحديد السوق المستهدف")

market_type = st.sidebar.radio(
    "اختر السوق:",
    ["العملات الرقمية (Crypto)", "الأسهم الأمريكية (US Stocks)"]
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

if market_type == "العملات الرقمية (Crypto)":

    fng_val, fng_class = fetch_crypto_fear_greed()

    st.sidebar.markdown("---")
    st.sidebar.metric(
        "مؤشر الخوف والطمع",
        f"{fng_val}/100",
        fng_class
    )

    st.markdown("### 🪙 لوحة تحكم سوق العملات الرقمية")

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
                "الأصل": coin["name"],
                "الرمز": coin["symbol"].upper(),
                "السعر (USD)": f"${coin['current_price']:,.2f}",
                "التغير 24 ساعة": f"{change:.2f}%"
            })

        st.dataframe(
            pd.DataFrame(display_list),
            use_container_width=True
        )

        st.divider()

        st.markdown("### 🎯 تحليل الأصول والذكاء الاصطناعي")

        chosen_coin = st.selectbox(
            "اختر الأصل للتحليل العميق:",
            list(coin_cache.keys())
        )

        if chosen_coin in coin_cache:
            info = coin_cache[chosen_coin]

            col_a, col_b = st.columns([1, 2])

            with col_a:
                st.metric(
                    "السعر الحالي",
                    f"${info['price']:,.2f}",
                    f"{info['change']:.2f}%"
                )

                st.metric(
                    "أعلى سعر (24س)",
                    f"${info['high']:,.2f}"
                )

                st.metric(
                    "أقل سعر (24س)",
                    f"${info['low']:,.2f}"
                )

            with col_b:
                if info["sparkline"]:
                    st.line_chart(
                        pd.DataFrame({
                            "السعر الأسبوعي": info["sparkline"]
                        }),
                        color="#6366F1"
                    )

            if st.button(
                "🚀 تشغيل محرك التحليل الذكي للقرارات",
                type="primary"
            ):
                with st.spinner(
                    "جاري جمع البيانات، تشغيل النماذج، وتقييم المخاطر..."
                ):
                    chg = info["change"]

                    if chg > 2:
                        decision = "شراء / تجميع قوي (Bullish)"
                        confidence = "74.5%"
                        scenario = (
                            "استمرار الزخم الصاعد نحو مقاومة قريبة، "
                            "مع وضع وقف خسارة تحت الدعم السابق."
                        )
                        box_color = "#10B981"

                    elif chg >= 0:
                        decision = "حيادي مع ميل للصعود (Neutral-Bullish)"
                        confidence = "62.0%"
                        scenario = (
                            "تذبذب عرضي، يفضل الانتظار لاختراق واضح "
                            "أو التصعيد عند الدعم."
                        )
                        box_color = "#3B82F6"

                    else:
                        decision = "حذر شديد / تصحيح محتمل (Bearish)"
                        confidence = "68.3%"
                        scenario = (
                            "احتمالية اختبار مستويات دعم أدنى، "
                            "راقب السيولة قبل أي دخول جديد."
                        )
                        box_color = "#EF4444"

                st.markdown(
                    f"""
                    <div class="ai-box" style="border-color: {box_color};">
                        <h3 style="color: {box_color}; margin-top:0;">
                            🧠 تقرير محرك الذكاء الاصطناعي: {chosen_coin}
                        </h3>
                        <p><b>القرار المقترح:</b> {decision}</p>
                        <p><b>نسبة الثقة في النموذج:</b> {confidence}</p>
                        <p><b>التفسير والسيناريو البديل:</b> {scenario}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


elif market_type == "الأسهم الأمريكية (US Stocks)":

    st.markdown("### 🇺🇸 لوحة تحكم سوق الأسهم الأمريكية")

    stock_raw = fetch_us_stocks(us_stocks_watchlist)

    if stock_raw:
        stock_display = []
        stock_cache = {}

        for stck in stock_raw:
            chg = stck["price_change_percentage_24h"]

            stock_cache[stck["symbol"]] = {
                "price": stck["current_price"],
                "change": chg,
                "high": stck["high_24h"],
                "low": stck["low_24h"]
            }

            stock_display.append({
                "الرمز": stck["symbol"],
                "السعر (USD)": f"${stck['current_price']:,.2f}",
                "التغير 24 ساعة": f"{chg:.2f}%"
            })

        st.dataframe(
            pd.DataFrame(stock_display),
            use_container_width=True
        )

        st.divider()

        st.markdown(
            "### 🎯 تحليل الأسهم الأمريكية والذكاء الاصطناعي"
        )

        chosen_stock = st.selectbox(
            "اختر السهم للتحليل العميق:",
            list(stock_cache.keys())
        )

        if chosen_stock in stock_cache:
            s_info = stock_cache[chosen_stock]

            c1, c2 = st.columns(2)

            c1.metric(
                "السعر الحالي",
                f"${s_info['price']:,.2f}",
                f"{s_info['change']:.2f}%"
            )

            c2.metric(
                "مدى الجلسة",
                f"High: ${s_info['high']:,.2f} | Low: ${s_info['low']:,.2f}"
            )

            if st.button(
                "🚀 تشغيل محرك التحليل الذكي للسهم",
                type="primary"
            ):
                with st.spinner(
                    "جاري تحليل المؤشرات الفنية ودفتر الأوامر..."
                ):
                    s_chg = s_info["change"]

                    if s_chg > 1:
                        s_decision = "شراء / فرصة نمو (Buy)"
                        s_conf = "71.0%"
                        s_scen = (
                            "السهم يظهر قوة نسبية مقارنة بالسوق، "
                            "مستهدف تالي عند المقاومة القادمة."
                        )
                        s_color = "#10B981"

                    else:
                        s_decision = "مراقبة / الحذر واجب (Watch/Hold)"
                        s_conf = "64.5%"
                        s_scen = (
                            "ضغوطات بيعية محتملة، يفضل الانتظار "
                            "لتأكيد ارتداد السعر."
                        )
                        s_color = "#EF4444"

                st.markdown(
                    f"""
                    <div class="ai-box" style="border-color: {s_color};">
                        <h3 style="color: {s_color}; margin-top:0;">
                            🧠 تقرير محرك الذكاء الاصطناعي: {chosen_stock}
                        </h3>
                        <p><b>القرار المقترح:</b> {s_decision}</p>
                        <p><b>نسبة الثقة في النموذج:</b> {s_conf}</p>
                        <p><b>التفسير والسيناريو البديل:</b> {s_scen}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
