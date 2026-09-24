import os
import requests
from dotenv import load_dotenv
import psycopg2

load_dotenv()
db_url=os.getenv('DATABASE_URL')
conn=psycopg2.connect(db_url)
cursor=conn.cursor()
api_key = os.getenv('ALPHA_VANTAGE_KEY')
url = 'https://www.alphavantage.co/query'

params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "IBM",
    "apikey": api_key
}

response = requests.get(url, params=params)
data = response.json()

# 1. Exact string matches for the JSON keys
time_series = data.get('Time Series (Daily)')
symbol = data['Meta Data']['2. Symbol']

if not time_series:
    print("Error: No time series data found. Check your API limit or symbol.")
    exit()

for date, metrics in time_series.items():
    open_price = float(metrics['1. open'])
    high_price = float(metrics['2. high'])
    low_price = float(metrics['3. low'])
    close_price = float(metrics['4. close'])
    volume = int(metrics['5. volume'])
    
    cursor.execute("""INSERT INTO daily_stock_price(symbol, trade_date, open_price, high_price, low_price, close_price, volume) values (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (symbol, trade_date) DO NOTHING;
    """, (symbol, date, open_price, high_price, low_price, close_price, volume))
conn.commit()
cursor.close()
conn.close()
print("Data successfully loaded into the database!")
    