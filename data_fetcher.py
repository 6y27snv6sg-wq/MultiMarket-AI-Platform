import requests
import streamlit as st


REQUEST_TIMEOUT = 15

COINGECKO_BASE = (
    "https://api.coingecko.com/api/v3"
)

YAHOO_BASE = (
    "https://query1.finance.yahoo.com"
)


# =========================================================
# CRYPTO SEARCH
# =========================================================

@st.cache_data(ttl=300)
def search_crypto(query):

    if not query:
        return []

    try:

        response = requests.get(
            f"{COINGECKO_BASE}/search",
            params={
                "query": query
            },
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        payload = response.json()

        coins = payload.get(
            "coins",
            [],
        )

        results = []

        for coin in coins[:10]:

            coin_id = coin.get("id")
            name = coin.get("name")
            symbol = coin.get("symbol")

            if coin_id and name and symbol:

                results.append({
                    "id": coin_id,
                    "name": name,
                    "symbol": symbol,
                })

        return results

    except (
        requests.RequestException,
        ValueError,
        TypeError,
    ):
        return []


# =========================================================
# CRYPTO MARKET
# =========================================================

@st.cache_data(ttl=60)
def fetch_crypto_market(coin_ids):

    if not coin_ids:
        return []

    try:

        response = requests.get(
            f"{COINGECKO_BASE}/coins/markets",
            params={
                "vs_currency": "usd",
                "ids": ",".join(coin_ids),
                "order": "market_cap_desc",
                "sparkline": "false",
            },
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        data = response.json()

        if isinstance(data, list):
            return data

    except (
        requests.RequestException,
        ValueError,
        TypeError,
    ):
        return []

    return []


# =========================================================
# CRYPTO HISTORY
# =========================================================

@st.cache_data(ttl=300)
def fetch_crypto_history(coin_id):

    if not coin_id:
        return []

    try:

        response = requests.get(
            f"{COINGECKO_BASE}/coins/{coin_id}/market_chart",
            params={
                "vs_currency": "usd",
                "days": "7",
                "interval": "hourly",
            },
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        payload = response.json()

        prices = payload.get(
            "prices",
            [],
        )

        result = []

        for item in prices:

            if len(item) >= 2:

                result.append({
                    "timestamp": item[0] / 1000,
                    "price": item[1],
                })

        return result

    except (
        requests.RequestException,
        ValueError,
        TypeError,
    ):
        return []


# =========================================================
# CRYPTO GLOBAL
# =========================================================

@st.cache_data(ttl=300)
def fetch_crypto_global():

    try:

        response = requests.get(
            f"{COINGECKO_BASE}/global",
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        payload = response.json()

        return payload.get(
            "data",
            {},
        )

    except (
        requests.RequestException,
        ValueError,
        TypeError,
    ):
        return {}


# =========================================================
# US STOCKS
# =========================================================

@st.cache_data(ttl=300)
def fetch_us_stocks(tickers):

    if not tickers:
        return []

    results = []

    for ticker in tickers:

        try:

            ticker = ticker.strip().upper()

            if not ticker:
                continue

            response = requests.get(
                f"{YAHOO_BASE}/v8/finance/chart/{ticker}",
                params={
                    "interval": "1d",
                    "range": "5d",
                },
                headers={
                    "User-Agent": "Mozilla/5.0",
                },
                timeout=REQUEST_TIMEOUT,
            )

            response.raise_for_status()

            payload = response.json()

            chart = payload.get(
                "chart",
                {},
            )

            data = chart.get(
                "result"
            )

            if not data:
                continue

            meta = data[0].get(
                "meta",
                {},
            )

            price = meta.get(
                "regularMarketPrice"
            )

            previous_close = meta.get(
                "chartPreviousClose"
            )

            if price is None:
                continue

            if previous_close in (
                None,
                0,
            ):
                continue

            change = (
                (price - previous_close)
                / previous_close
            ) * 100

            results.append({
                "symbol": ticker,
                "current_price": price,
                "price_change_percentage_24h": change,
                "high_24h": meta.get(
                    "regularMarketDayHigh",
                    price,
                ),
                "low_24h": meta.get(
                    "regularMarketDayLow",
                    price,
                ),
                "volume": meta.get(
                    "regularMarketVolume",
                    0,
                ),
            })

        except (
            requests.RequestException,
            ValueError,
            TypeError,
            KeyError,
            IndexError,
        ):
            continue

    return results


# =========================================================
# STOCK HISTORY
# =========================================================

@st.cache_data(ttl=300)
def fetch_stock_history(ticker):

    if not ticker:
        return []

    try:

        ticker = ticker.strip().upper()

        response = requests.get(
            f"{YAHOO_BASE}/v8/finance/chart/{ticker}",
            params={
                "interval": "1h",
                "range": "1mo",
            },
            headers={
                "User-Agent": "Mozilla/5.0",
            },
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        payload = response.json()

        chart = payload.get(
            "chart",
            {},
        )

        results = chart.get(
            "result"
        )

        if not results:
            return []

        result = results[0]

        timestamps = result.get(
            "timestamp",
            [],
        )

        quote = (
            result
            .get("indicators", {})
            .get("quote", [])
        )

        if not quote:
            return []

        closes = quote[0].get(
            "close",
            [],
        )

        output = []

        for timestamp, close in zip(
            timestamps,
            closes,
        ):

            if close is not None:

                output.append({
                    "timestamp": timestamp,
                    "price": close,
                })

        return output

    except (
        requests.RequestException,
        ValueError,
        TypeError,
        KeyError,
        IndexError,
    ):
        return []


# =========================================================
# FEAR & GREED
# =========================================================

@st.cache_data(ttl=300)
def fetch_crypto_fear_greed():

    try:

        response = requests.get(
            "https://api.alternative.me/fng/",
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        payload = response.json()

        data = payload.get(
            "data",
            [],
        )

        if data:

            item = data[0]

            return (
                item.get(
                    "value",
                    "50",
                ),
                item.get(
                    "value_classification",
                    "Neutral",
                ),
            )

    except (
        requests.RequestException,
        ValueError,
        TypeError,
        KeyError,
        IndexError,
    ):
        pass

    return "50", "Neutral"
