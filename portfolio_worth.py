"""
This program allows a user to select from a pre-defined list of tickers 
to see the historical value of the asset in different currencies.
"""

# IMPORT required packages
import streamlit as st
#  for ease of data visualization
import pandas as pd
#  for storing data as pd.dataframe-- easy to use with streamlit
import yfinance as yf
#  for getting data from yahoo finance as pd.dataframe
#  can use yahoofinancials if we want JSON
from forex_python.converter import CurrencyRates

# ==== USER WIDGETS ====

st.title("A simple web app for seeing stock value in different currencies")
st.write("""
### User manual
* you can choose to see either the stock value of Google, Apple, or Meta for Jan 2022 in both US and EUR.
...
""")

ticker_option = st.selectbox(
    'Select the ticker you\'d like to see:',
    ('GOOG', 'AAPL', 'META'))
# NOTE : a more complex option is to read the available tickers from S&P_500 via the HTML
#       the wikipedia page.
#       Keeping it simple for illustrative purposes

# TODO : try add variable date range
# TODO : try add variable currency options
# TODO : optimize to make streamlit's rendering more fluid. e.g. use @st.cache decorator.

# ==== BUSINESS LOGIC ====
# get data for Apple's OHLC price from 2012-2022 September.
df_us = yf.download(ticker_option,
                    start="2022-01-01",
                    end="2022-01-30",
                    progress=False)  # don't display the progress bar

# drop adjusted close and volume for simplicity's sake
df_us = df_us.drop(columns=["Adj Close", "Volume"])

# create a new col in the dataframe for conversion rate between USD and EUR
c = CurrencyRates()
df_us["usd_eur"] = [c.get_rate("USD", "EUR", date) for date in df_us.index]
# NOTE : `get_rate` is time-consuming and limits the feasible data range.
#   e.g. If I specified `start` and `end` to be from Jan 2022 to Sept 2022, the Python script would just keep running.
#   QUESTION : how what happens if I wanna see a larger date range?

# create a new dataframe for the EUR values
df_eu = pd.DataFrame()
for column in df_us.columns[:-1]:
    df_eu[f"{column}_EUR"] = df_us[column] * df_us["usd_eur"]


# ==== RENDER RESULT ====
st.write(f"Line chart for value of {ticker_option} in USD")
st.line_chart(df_us)
st.write(f"Line chart for value of {ticker_option} in EUR")
st.line_chart(df_eu)
