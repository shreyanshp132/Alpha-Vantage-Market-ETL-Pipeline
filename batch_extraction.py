import os
import time
import requests
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv()

# 1. Connect to Database
db_url = os.getenv("DATABASE_URL")
api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
conn = psycopg2.connect(db_url)
cursor = conn.cursor()

# 2. Define 10 companies (Uses 10 of your 25 daily limits)
symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NVDA', 'JPM', 'V', 'JNJ']

for symbol in symbols:
    print(f"Fetching data for {symbol}...")
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=compact&apikey={api_key}'
    
    response = requests.get(url)
    data = response.json()
    
    # Catch API limit warnings
    if "Time Series (Daily)" not in data:
        print(f"Error or API limit for {symbol}. Skipping. Response: {data}")
        continue

    # 3. Transform with Pandas
    time_series = data["Time Series (Daily)"]
    df = pd.DataFrame.from_dict(time_series, orient='index')
    df.reset_index(inplace=True)
    df.columns = ['trade_date', 'open_price', 'high_price', 'low_price', 'close_price', 'volume']
    
    # Clean data types
    df['symbol'] = symbol
    df['trade_date'] = pd.to_datetime(df['trade_date']).dt.date
    cols_to_float = ['open_price', 'high_price', 'low_price', 'close_price']
    df[cols_to_float] = df[cols_to_float].astype(float)
    df['volume'] = df['volume'].astype(int)
    
    # Calculate 7-day Simple Moving Average
    df.sort_values('trade_date', inplace=True)
    df['sma_7'] = df['close_price'].rolling(window=7).mean()
    
    # Replace Pandas NaNs with Python None for the database
    df = df.where(pd.notnull(df), None)

    # 4. Bulk Insert into PostgreSQL
    insert_query = """
    INSERT INTO daily_stock_price (symbol, trade_date, open_price, high_price, low_price, close_price, volume, sma_7)
    VALUES %s
    ON CONFLICT (symbol, trade_date) DO UPDATE 
    SET sma_7 = EXCLUDED.sma_7,
        close_price = EXCLUDED.close_price;
    """
    
    records = df[['symbol', 'trade_date', 'open_price', 'high_price', 'low_price', 'close_price', 'volume', 'sma_7']].values.tolist()
    execute_values(cursor, insert_query, records)
    conn.commit()
    
    print(f"Successfully loaded {len(records)} rows for {symbol}.")
    
    # 5. Pause to respect the 5-requests-per-minute limit
    print("Waiting 15 seconds...\n")
    time.sleep(15)

cursor.close()
conn.close()
print("Batch extraction fully complete!")