import requests
import streamlit as st


REQUEST_TIMEOUT = 15

COINGECKO_BASE = "https://api.coingecko.com/api/v3"
YAHOO_BASE = "https://query1.finance.yahoo.com"


@st.cache_data(ttl=300)
def search_crypto(query):
    if not query:
        return []

    try:
        response = requests.get(
            f"{COINGECKO_BASE}/search",
            params={"query": query},
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        data = response.json()
        coins = data.get("coins", [])

        results = []

        for coin in coins[:10]:
            if coin.get("id") and coin.get("name"):
                results.append({
                    "id": coin["id"],
                    "name": coin["name"],
                    "symbol": coin.get("symbol", ""),
                })

        return results

    except Exception:
        return []


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

        return data if isinstance(data, list) else []

    except Exception:
        return []


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

        data = response.json()
        prices = data.get("prices", [])

        return [
            {
                "timestamp": item[0] / 1000,
                "price": item[1],
            }
            for item in prices
            if len(item) >= 2
        ]

    except Exception:
        return []


@st.cache_data(ttl=300)
def fetch_crypto_global():
    try:
        response = requests.get(
            f"{COINGECKO_BASE}/global",
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        data = response.json()

        return data.get("data", {})

    except Exception:
        return {}


@st.cache_data(ttl=300)
def fetch_us_stocks(tickers):
    if not tickers:
        return []

    results = []

    for ticker in tickers:

        try:
            ticker = ticker.strip().upper()

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

            data = response.json()

            chart = data.get("chart", {})
            result = chart.get("result")

            if not result:
                continue

            meta = result[0].get("meta", {})

            price = meta.get("regularMarketPrice")
            previous = meta.get("chartPreviousClose")

            if price is None or not previous:
                continue

            change = ((price - previous) / previous) * 100

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

        except Exception:
            continue

    return results


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

        data = response.json()

        result = data.get("chart", {}).get("result")

        if not result:
            return []

        result = result[0]

        timestamps = result.get("timestamp", [])

        quotes = (
            result
            .get("indicators", {})
            .get("quote", [])
        )

        if not quotes:
            return []

        closes = quotes[0].get("close", [])

        history = []

        for timestamp, close in zip(
            timestamps,
            closes,
        ):
            if close is not None:
                history.append({
                    "timestamp": timestamp,
                    "price": close,
                })

        return history

    except Exception:
        return []


@st.cache_data(ttl=300)
def fetch_crypto_fear_greed():
    try:
        response = requests.get(
            "https://api.alternative.me/fng/",
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        data = response.json().get("data", [])

        if data:
            return (
                data[0].get("value", "50"),
                data[0].get(
                    "value_classification",
                    "Neutral",
                ),
            )

    except Exception:
        pass

    return "50", "Neutral"
