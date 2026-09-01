

```python
import requests
import pandas as pd
import streamlit as st

# 1. جلب بيانات الكريبتو (من CoinGecko المجاني)
@st.cache_data(ttl=60)
def fetch_crypto_market(coin_ids):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "ids": ",".join(coin_ids),
        "order": "market_cap_desc",
        "sparkline": "true"
    }
    try:
        res = requests.get(url, params=params)
        if res.status_code == 200:
            return res.json()
    except:
        return None
    return None

# 2. جلب بيانات السوق الأمريكي (باستخدام Yahoo Finance API المجاني)
@st.cache_data(ttl=300)
def fetch_us_stocks(tickers):
    stock_data = []
    for ticker in tickers:
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range=5d"
            headers = {'User-Agent': 'Mozilla/5.0'}
            res = requests.get(url, headers=headers)
            if res.status_code == 200:
                data = res.json()
                meta = data['chart']['result'][0]['meta']
                price = meta['regularMarketPrice']
                prev_close = meta['chartPreviousClose']
                change = ((price - prev_close) / prev_close) * 100
                stock_data.append({
                    "symbol": ticker,
                    "name": ticker,
                    "current_price": price,
                    "price_change_percentage_24h": change,
                    "high_24h": meta.get('regularMarketDayHigh', price),
                    "low_24h": meta.get('regularMarketDayLow', price),
                })
        except:
            continue
    return stock_data

# 3. جلب مؤشر الخوف والطمع للكريبتو
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
