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
    """
    Search CoinGecko for cryptocurrencies.
    """

    if not query:
        return []

    try:

        response = requests.get(
            f"{COINGECKO_BASE}/search",
            params={
                "query": query
            },
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

        payload = response.json()

        coins = payload.get("coins", [])

        results = []

        for coin in coins[:10]:

            coin_id = coin.get("id")
            name = coin.get("name")
            symbol = coin.get("symbol")

            if coin_id and name and symbol:

                results.append({
                    "id": coin_id,
                    "name": name,
                    "symbol": symbol
                })

        return results

    except requests.RequestException:
        return []

    except (ValueError, TypeError):
        return []


# =========================================================
# CRYPTO MARKET DATA
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
                "sparkline": "true"
            },
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

        data = response.json()

        if isinstance(data, list):
            return data

    except requests.RequestException:
        return []

    except (ValueError, TypeError):
        return []

    return []


# =========================================================
# US STOCKS
# =========================================================

@st.cache_data(ttl=300)
def fetch_us_stocks(tickers):

    if not tickers:
        return []

    stock_data = []

    for ticker in tickers:

        try:

            ticker = ticker.strip().upper()

            if not ticker:
                continue

            response = requests.get(
                f"{YAHOO_BASE}/v8/finance/chart/{ticker}",
                params={
                    "interval": "1d",
                    "range": "5d"
                },
                headers={
                    "User-Agent": "Mozilla/5.0"
                },
                timeout=REQUEST_TIMEOUT
            )

            response.raise_for_status()

            payload = response.json()

            chart = payload.get("chart", {})
            results = chart.get("result")

            if not results:
                continue

            meta = results[0].get("meta", {})

            price = meta.get(
                "regularMarketPrice"
            )

            previous_close = meta.get(
                "chartPreviousClose"
            )

            if price is None:
                continue

            if previous_close in (None, 0):
                continue

            change = (
                (price - previous_close)
                / previous_close
            ) * 100

            stock_data.append({
                "symbol": ticker,
                "current_price": price,
                "price_change_percentage_24h": change,

                "high_24h": meta.get(
                    "regularMarketDayHigh",
                    price
                ),

                "low_24h": meta.get(
                    "regularMarketDayLow",
                    price
                ),

                "volume": meta.get(
                    "regularMarketVolume",
                    0
                )
            })

        except requests.RequestException:
            continue

        except (
            ValueError,
            TypeError,
            KeyError,
            IndexError
        ):
            continue

    return stock_data


# =========================================================
# FEAR & GREED
# =========================================================

@st.cache_data(ttl=300)
def fetch_crypto_fear_greed():

    try:

        response = requests.get(
            "https://api.alternative.me/fng/",
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

        payload = response.json()

        data = payload.get("data")

        if data and isinstance(data, list):

            item = data[0]

            value = item.get(
                "value",
                "50"
            )

            classification = item.get(
                "value_classification",
                "Neutral"
            )

            return value, classification

    except requests.RequestException:
        pass

    except (
        ValueError,
        TypeError,
        KeyError,
        IndexError
    ):
        pass

    return "50", "Neutral"
