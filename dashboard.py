import os
import pandas as pd
import psycopg2
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# 1. Page Configuration
st.set_page_config(page_title="Stock Market ETL Dashboard", layout="wide")
st.title("📈 Stock Price & Moving Average Dashboard")

# 2. Fetch Data from PostgreSQL
# The @st.cache_data decorator prevents the app from querying the DB every time you click a button
@st.cache_data
def load_data():
    db_url = os.getenv("DATABASE_URL")
    conn = psycopg2.connect(db_url)
    
    # Fetch all data and sort chronologically
    query = "SELECT * FROM daily_stock_price ORDER BY trade_date ASC;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

df = load_data()

# 3. Sidebar Filters
st.sidebar.header("Filter Data")
available_symbols = df['symbol'].unique()
# Default to showing the first 3 stocks so the chart isn't too cluttered immediately
selected_symbols = st.sidebar.multiselect(
    "Select Companies to Compare:", 
    available_symbols, 
    default=available_symbols[:3]
)

# 4. Main Dashboard Area
if not selected_symbols:
    st.warning("Please select at least one company from the sidebar to view data.")
else:
    # Filter the dataframe based on user selection
    filtered_df = df[df['symbol'].isin(selected_symbols)]
    
    # Format data for Streamlit's native line chart (Closing Prices)
    st.subheader("Closing Price Comparison")
    close_price_chart = filtered_df.pivot(index='trade_date', columns='symbol', values='close_price')
    st.line_chart(close_price_chart)
    
    # Format data for the 7-Day SMA
    st.subheader("7-Day Simple Moving Average (SMA)")
    sma_chart = filtered_df.pivot(index='trade_date', columns='symbol', values='sma_7')
    st.line_chart(sma_chart)
    
    # Show the raw data table
    st.subheader("Raw Database Records")
    st.dataframe(filtered_df)