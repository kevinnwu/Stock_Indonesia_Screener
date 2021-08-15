import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf
from statsmodels.tsa.filters.hp_filter import hpfilter


def look_diff(stock):
    diff = stock['close-today'] - stock['close-yest']
    if diff > 0:
        return [''] * 9 + ['background-color: lightgreen'] * 1
    elif diff < 0:
        return [''] * 9 + ['background-color: pink'] * 1
    else:
        return [''] * 9 + ['background-color: yellow'] * 1


if 'key' not in st.session_state:
    st.session_state['key'] = '0'

tickers = pd.read_csv('Tickers.csv')['Code']
result = pd.DataFrame()

process = st.button('Process')

if process:
    st.session_state['key'] = 1
    loading_text = st.empty()
    progress_bar = st.progress(0)
    df = pd.DataFrame(columns=['code', 'close-ma30', 'close-ma7', 'close-yest', 'close-today',
                               'vol-ma30', 'vol-ma7', 'vol-yest', 'vol-today', 'look'])
    for index, ticker in enumerate(tickers):
        progress_bar.progress(index / len(tickers))
        loading_text.write('Collecting ' + str(ticker))
        tick = yf.download(
            tickers=str(ticker) + '.JK',
            period="30d",
            interval="1d",
            group_by='ticker',
        )
        try:
            df['code'] = str(ticker)
            df['close-ma30'] = tick['Close'].rolling(30).mean()
            df['close-ma7'] = tick['Close'].rolling(7).mean()
            df['close-yest'] = tick['Close'][-2]
            df['close-today'] = tick['Close'][-1]
            df['vol-ma30'] = tick['Volume'].rolling(30).mean()
            df['vol-ma7'] = tick['Volume'].rolling(7).mean()
            df['vol-yest'] = tick['Volume'][-2]
            df['vol-today'] = tick['Volume'][-1]
            df['look'] = df['vol-today'] / df['vol-ma7']
            result = result.append(df.iloc[-1], ignore_index=True)

        except:
            continue
    result = result[['code', 'close-ma30', 'close-ma7', 'close-yest', 'close-today',
                     'vol-ma30', 'vol-ma7', 'vol-yest', 'vol-today', 'look']]
    progress_bar.empty()
    loading_text.empty()
    dicts = {}
    for i in result.columns:
        if i == 'code':
            continue
        else:
            dicts[i] = lambda x: '{:,.0f}'.format(x)

    s = result.style.format(dicts) \
        .apply(look_diff, axis=1)

    st.dataframe(s)
elif st.session_state['key'] == 1:
    pass
else:
    st.stop()
