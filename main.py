import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf
from statsmodels.tsa.filters.hp_filter import hpfilter

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
                               'vol-ma30', 'vol-ma7', 'vol-yest', 'vol-today'])
    for index, ticker in enumerate(tickers):
        progress_bar.progress(index / len(tickers))
        loading_text.write('Collecting ' + str(ticker))
        tick = yf.download(
            tickers=str(ticker) + '.JK',
            period="30d",
            interval="1d",
            group_by='ticker',
        )

        df['code'] = str(ticker)
        df['close-ma30'] = tick['Close'].rolling(30).mean()
        df['close-ma7'] = tick['Close'].rolling(7).mean()
        df['close-yest'] = tick['Close'][-2]
        df['close-today'] = tick['Close'][-1]
        df['vol-ma30'] = tick['Volume'].rolling(30).mean()
        df['vol-ma7'] = tick['Volume'].rolling(7).mean()
        df['vol-yest'] = tick['Volume'][-2]
        df['vol-today'] = tick['Volume'][-1]
        result = result.append(df.iloc[-1], ignore_index=True)
    result = result[['code', 'close-ma30', 'close-ma7', 'close-yest', 'close-today',
                     'vol-ma30', 'vol-ma7', 'vol-yest', 'vol-today']]
    progress_bar.empty()
    loading_text.empty()
    dicts = {}
    for i in result.columns:
        if i == 'code':
            continue
        else:
            dicts[i] = lambda x: '{:,.0f}'.format(x)

    s = result.style.format(dicts)
    st.dataframe(s)
elif st.session_state['key'] == 1:
    pass
else:
    st.stop()


