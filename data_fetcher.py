
import requests
import streamlit as st


REQUEST_TIMEOUT = 15
COINGECKO_BASE = "https://api.coingecko.com/api/v3"
YAHOO_BASE = "https://query1.finance.yahoo.com"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Capi Decision Intelligence)"
}


def _get_json(url, params=None):
    try:
        response = requests.get(
            url,
            params=params,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        return response.json()
    except (
        requests.RequestException,
        ValueError,
        TypeError,
    ):
        return None


@st.cache_data(ttl=300)
def search_crypto(query):
    if not query:
        return []

    data = _get_json(
        f"{COINGECKO_BASE}/search",
        {"query": query},
    )

    if not data:
        return []

    results = []
    for coin in data.get("coins", [])[:10]:
        if coin.get("id") and coin.get("name"):
            results.append({
                "id": coin["id"],
                "name": coin["name"],
                "symbol": coin.get("symbol", ""),
            })
    return results


@st.cache_data(ttl=60)
def fetch_crypto_market(coin_ids):
    if not coin_ids:
        return []

    data = _get_json(
        f"{COINGECKO_BASE}/coins/markets",
        {
            "vs_currency": "usd",
            "ids": ",".join(coin_ids),
            "order": "market_cap_desc",
            "sparkline": "false",
            "price_change_percentage": "24h",
        },
    )

    return data if isinstance(data, list) else []


@st.cache_data(ttl=300)
def fetch_crypto_ohlc(coin_id):
    if not coin_id:
        return []

    data = _get_json(
        f"{COINGECKO_BASE}/coins/{coin_id}/ohlc",
        {
            "vs_currency": "usd",
            "days": "7",
        },
    )

    if not isinstance(data, list):
        return []

    result = []
    for row in data:
        if len(row) >= 5:
            result.append({
                "timestamp": row[0] / 1000,
                "open": row[1],
                "high": row[2],
                "low": row[3],
                "close": row[4],
            })
    return result


@st.cache_data(ttl=300)
def fetch_crypto_global():
    data = _get_json(
        f"{COINGECKO_BASE}/global"
    )
    return data.get("data", {}) if data else {}


@st.cache_data(ttl=300)
def fetch_crypto_fear_greed():
    data = _get_json(
        "https://api.alternative.me/fng/"
    )

    if data and data.get("data"):
        item = data["data"][0]
        return (
            item.get("value", "50"),
            item.get("value_classification", "Neutral"),
        )

    return "50", "Neutral"


@st.cache_data(ttl=300)
def fetch_us_stocks(tickers):
    if not tickers:
        return []

    results = []

    for ticker in tickers:
        ticker = str(ticker).strip().upper()

        if not ticker:
            continue

        data = _get_json(
            f"{YAHOO_BASE}/v8/finance/chart/{ticker}",
            {
                "interval": "1d",
                "range": "5d",
            },
        )

        if not data:
            continue

        try:
            result = data["chart"]["result"][0]
            meta = result.get("meta", {})

            price = meta.get("regularMarketPrice")
            previous = meta.get("chartPreviousClose")

            if price is None or previous in (None, 0):
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

        except (
            KeyError,
            IndexError,
            TypeError,
            ValueError,
        ):
            continue

    return results


@st.cache_data(ttl=300)
def fetch_stock_history(ticker):
    ticker = str(ticker).strip().upper()

    if not ticker:
        return []

    data = _get_json(
        f"{YAHOO_BASE}/v8/finance/chart/{ticker}",
        {
            "interval": "1d",
            "range": "6mo",
        },
    )

    if not data:
        return []

    try:
        result = data["chart"]["result"][0]
        timestamps = result.get("timestamp", [])
        quote = (
            result
            .get("indicators", {})
            .get("quote", [{}])[0]
        )

        opens = quote.get("open", [])
        highs = quote.get("high", [])
        lows = quote.get("low", [])
        closes = quote.get("close", [])
        volumes = quote.get("volume", [])

        output = []

        for i, timestamp in enumerate(timestamps):
            values = [
                opens[i] if i < len(opens) else None,
                highs[i] if i < len(highs) else None,
                lows[i] if i < len(lows) else None,
                closes[i] if i < len(closes) else None,
            ]

            if any(v is None for v in values):
                continue

            output.append({
                "timestamp": timestamp,
                "open": values[0],
                "high": values[1],
                "low": values[2],
                "close": values[3],
                "volume": (
                    volumes[i]
                    if i < len(volumes)
                    and volumes[i] is not None
                    else 0
                ),
            })

        return output

    except (
        KeyError,
        IndexError,
        TypeError,
        ValueError,
    ):
        return []


SECTOR_MAP = {
    "AAPL": ("Technology", "XLK"),
    "MSFT": ("Technology", "XLK"),
    "NVDA": ("Technology", "XLK"),
    "AVGO": ("Technology", "XLK"),
    "AMD": ("Technology", "XLK"),
    "GOOGL": ("Communication Services", "XLC"),
    "META": ("Communication Services", "XLC"),
    "AMZN": ("Consumer Discretionary", "XLY"),
    "TSLA": ("Consumer Discretionary", "XLY"),
    "JPM": ("Financials", "XLF"),
    "BAC": ("Financials", "XLF"),
    "WMT": ("Consumer Staples", "XLP"),
    "JNJ": ("Healthcare", "XLV"),
    "UNH": ("Healthcare", "XLV"),
    "XOM": ("Energy", "XLE"),
    "CVX": ("Energy", "XLE"),
    "CAT": ("Industrials", "XLI"),
    "LIN": ("Materials", "XLB"),
    "PLD": ("Real Estate", "XLRE"),
    "NEE": ("Utilities", "XLU"),
}


@st.cache_data(ttl=300)
def fetch_etf_data(symbol):
    rows = fetch_us_stocks([symbol])
    if not rows:
        return None

    row = rows[0]

    return {
        "symbol": symbol,
        "price": row["current_price"],
        "change": row["price_change_percentage_24h"],
    }


@st.cache_data(ttl=300)
def fetch_sector_data(ticker):
    ticker = str(ticker).strip().upper()

    sector_name, etf = SECTOR_MAP.get(
        ticker,
        ("Broad Market", "SPY"),
    )

    etf_rows = fetch_us_stocks([etf])

    if not etf_rows:
        return {
            "name": sector_name,
            "etf": etf,
            "score": 50,
            "relative_change": 0.0,
        }

    etf_change = etf_rows[0]["price_change_percentage_24h"]

    score = 50 + max(
        -40,
        min(40, etf_change * 8),
    )

    return {
        "name": sector_name,
        "etf": etf,
        "score": int(round(score)),
        "relative_change": etf_change,
    }
