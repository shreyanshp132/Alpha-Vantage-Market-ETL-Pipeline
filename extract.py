import os
import requests
import pandas as pd
import psycopg2
import psycopg2.extras as extras
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
conn = psycopg2.connect(db_url)
cursor = conn.cursor()

api_key = os.getenv('ALPHA_VANTAGE_KEY')
url = 'https://www.alphavantage.co/query'
params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "IBM",
    "apikey": api_key
}

response = requests.get(url, params=params)
data = response.json()

time_series = data.get('Time Series (Daily)')
symbol = data['Meta Data']['2. Symbol']

if not time_series:
    print("Error: No time series data found. Check your API limit or symbol.")
    exit()

df = pd.DataFrame.from_dict(time_series, orient='index').reset_index()

df.rename(columns={
    'index': 'trade_date',
    '1. open': 'open_price',
    '2. high': 'high_price',
    '3. low': 'low_price',
    '4. close': 'close_price',
    '5. volume': 'volume'
}, inplace=True)
df['symbol'] = symbol

df['trade_date'] = pd.to_datetime(df['trade_date'])
numeric_cols = ['open_price', 'high_price', 'low_price', 'close_price']
df[numeric_cols] = df[numeric_cols].astype(float)
df['volume'] = df['volume'].astype(int)

df = df.sort_values(by='trade_date', ascending=True)
df['sma_7'] = df['close_price'].rolling(window=7).mean()

df['sma_7'] = df['sma_7'].where(pd.notnull(df['sma_7']), None)


df = df[['symbol', 'trade_date', 'open_price', 'high_price', 'low_price', 'close_price', 'volume', 'sma_7']]

data_tuples = [tuple(row) for row in df.to_numpy()]

insert_query = """
    INSERT INTO daily_stock_price (symbol, trade_date, open_price, high_price, low_price, close_price, volume, sma_7) 
    VALUES %s 
    ON CONFLICT (symbol, trade_date) DO NOTHING;
"""

extras.execute_values(cursor, insert_query, data_tuples)
conn.commit()

cursor.close()
conn.close()
print("Data successfully transformed and bulk loaded into the database!")