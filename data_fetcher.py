
import requests
import pandas as pd
import streamlit as st

@st.cache_data(ttl=60)
def fetch_crypto_market(coin_ids):
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={','.join(coin_ids)}&order=market_cap_desc&sparkline=true"
    try:
        res = requests.get(url)
        if res.status_code == 200:
            return res.json()
    except:
        return None
    return None

@st.cache_data(ttl=300)
def fetch_us_stocks(tickers):
    stock_data = []
    for ticker in tickers:
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range=5d"
            res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            if res.status_code == 200:
                meta = res.json()['chart']['result'][0]['meta']
                price = meta['regularMarketPrice']
                prev = meta['chartPreviousClose']
                change = ((price - prev) / prev) * 100
                stock_data.append({
                    "symbol": ticker,
                    "current_price": price,
                    "price_change_percentage_24h": change,
                    "high_24h": meta.get('regularMarketDayHigh', price),
                    "low_24h": meta.get('regularMarketDayLow', price),
                })
        except:
            continue
    return stock_data

@st.cache_data(ttl=300)
def fetch_crypto_fear_greed():
    try:
        res = requests.get("https://api.alternative.me/fng/")
        if res.status_code == 200:
            data = res.json()['data'][0]
            return data['value'], data['value_classification']
    except:
        return "50", "Neutral"
    return "50", "Neutral"
```
