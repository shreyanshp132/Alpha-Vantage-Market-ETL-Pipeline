import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_url=os.getenv("DATABASE_URL")
conn= psycopg2.connect(db_url)
cursor=conn.cursor()


create_table_query="""
CREATE TABLE IF NOT EXISTS
daily_stock_price(symbol VARCHAR(10) NOT NULL,trade_date DATE NOT NULL,open_price FLOAT,high_price FLOAT,low_price FLOAT,close_price FLOAT,volume BIGINT,PRIMARY KEY (symbol, trade_date));
"""
cursor.execute(create_table_query)
cursor.execute("ALTER TABLE daily_stock_price ADD COLUMN IF NOT EXISTS sma_7 FLOAT;")
conn.commit()
cursor.close()
conn.close()
print("table created and altered successfully")