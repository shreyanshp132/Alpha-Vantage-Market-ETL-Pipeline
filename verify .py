import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()
conn = psycopg2.connect(os.getenv('DATABASE_URL'))

query = "SELECT * FROM daily_stock_price ORDER BY trade_date DESC LIMIT 10;"
df = pd.read_sql_query(query, conn)

print(df[['trade_date', 'close_price', 'sma_7']])
conn.close()