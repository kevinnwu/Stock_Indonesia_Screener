import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf
import time
from statsmodels.tsa.filters.hp_filter import hpfilter


def look_diff(stock):
    diff = stock['close-ma7'] - stock['close-ma30']
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
                               'vol-ma30', 'vol-ma7', 'vol-yest', 'vol-today', 'look(%)'])
    for index, ticker in enumerate(tickers):
        progress_bar.progress(index / len(tickers))
        loading_text.write('Collecting ' + str(ticker))
        tick = yf.download(
            # tickers=str(ticker) + '.JK',
            tickers=str(ticker) + '-USD',
            period="5d",
            interval="1h",
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
            df['look(%)'] = abs((df['close-ma30'] - df['close-ma7']) / df['close-ma30'] * 100)
            result = result.append(df.iloc[-2], ignore_index=True)
        except:
            continue
    result = result[['code', 'close-ma30', 'close-ma7', 'close-yest', 'close-today',
                     'vol-ma30', 'vol-ma7', 'vol-yest', 'vol-today', 'look(%)']]
    progress_bar.empty()
    loading_text.empty()
    dicts = {}
    for i in result.columns:
        if i == 'code':
            continue
        else:
            dicts[i] = lambda x: '{:,.4f}'.format(x)

    s = result.style.format(dicts) \
        .apply(look_diff, axis=1)

    st.dataframe(s)
elif st.session_state['key'] == 1:
    pass
else:
    st.stop()