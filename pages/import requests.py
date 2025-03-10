import streamlit as st
import streamlit.components.v1 as components

st.title("📊 Dukascopy Client Sentiment (Mở rộng)")

# Mở rộng danh sách mã giao dịch (Instruments)
html_code = """
<div>
    <script type="text/javascript">
        DukascopyApplet = {
            "type": "historical_sentiment_index",
            "params": {
                "showHeader": false,
                "tableBorderColor": "#D92626",
                "liquidity": "consumers",
                "availableInstruments": [
                    "EUR/USD","GBP/USD","USD/JPY","USD/CHF","EUR/JPY","GBP/JPY",
                    "AUD/USD", "NZD/USD", "USD/CAD",
                    "EUR/GBP", "EUR/CHF", "EUR/AUD", "EUR/CAD", "EUR/NZD",
                    "GBP/AUD", "GBP/CAD", "GBP/CHF", "GBP/NZD", "AUD/JPY", "AUD/NZD",
                    "XAU/USD", "XAG/USD","CAD/JPY"
                ],
                "availableCurrencies": [
                    "AUD","CAD","CHF","GBP","HKD","JPY","MXN","NOK","NZD","PLN","RUB",
                    "SEK","SGD","TRY","USD","ZAR","EUR","XAG","XAU"
                ],
                "last": true,
                "sixhours": true,
                "oneday": true,
                "fivedays": true,
                "width": "100%",
                "height": "400",
                "adv": "popup"
            }
        };
    </script>
    <script type="text/javascript" src="https://freeserv-static.dukascopy.com/2.0/core.js"></script>
</div>
"""

# Nhúng widget vào Streamlit
components.html(html_code, height=420, scrolling=True)
