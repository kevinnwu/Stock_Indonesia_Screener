import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf
from statsmodels.tsa.filters.hp_filter import hpfilter

if 'key' not in st.session_state:
    st.session_state['key'] = '0'
tickers = pd.read_csv('Tickers.csv')['Code']
df = pd.DataFrame()

process = st.button('Process')

if process:
    st.session_state['key'] = 1
    loading_text = st.empty()
    progress_bar = st.progress(0)
    for index, ticker in enumerate(tickers):
        progress_bar.progress(index / len(tickers))
        loading_text.write('Collecting ' + str(ticker))
        tick = yf.download(
            tickers=str(ticker) + '.JK',
            period="5d",
            interval="1d",
            group_by='ticker',
        )
        tick['YDV'] = tick.diff()['Volume'][1] * -1
        tick['Code'] = ticker
        df = df.append(tick.iloc[0], ignore_index=True)
    progress_bar.empty()
    loading_text.empty()

    df = df.iloc[df['YDV'].abs().argsort()].sort_values(by=['Volume'], ascending=[False])
    dicts = {}
    for i in df.columns:
        if i == 'Code':
            continue
        else:
            dicts[i] = lambda x: '{:,.0f}'.format(x)

    s = df.style.format(dicts)
    st.dataframe(s)
    st.text('YDV : Yesterday Different Volume')
elif st.session_state['key'] == 1:
    pass
else:
    st.stop()

tc = st.selectbox('Ticker', tickers)
tick = yf.download(
    tickers=str(tc) + '.JK',
    period="3mo",
    interval="1d",
    group_by='ticker',
)   
test = pd.DataFrame()
test['Close'] = tick['Close']

cycle, test['Trend'] = hpfilter(tick['Close'], lamb=100)

st.line_chart(test)
st.line_chart(cycle)