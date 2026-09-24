# End-to-End Stock Market ETL Pipeline 📈

This repository contains a complete Data Engineering ETL (Extract, Transform, Load) pipeline that pulls live stock market data, calculates financial indicators, stores the data in a cloud database, and visualizes it through an interactive web dashboard. 

This project was built to demonstrate scalable data engineering practices, API integration, and full-stack data visualization.

## 🏗️ Architecture

1. **Extract:** Fetches daily time series stock data via the **Alpha Vantage API**. Includes a batch extraction script capable of handling multiple ticker symbols while respecting API rate limits.
2. **Transform:** Uses **Pandas** to clean the JSON payloads, format timestamps, and calculate financial metrics (e.g., 7-Day Simple Moving Average).
3. **Load:** Upserts the transformed data into a fully managed **PostgreSQL (Neon)** cloud database, preventing duplicate records.
4. **Serve:** A **Streamlit** dashboard connects directly to the database to serve interactive charts and metrics to end-users.

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Data Processing:** Pandas
* **Database:** PostgreSQL, psycopg2
* **Frontend:** Streamlit
* **Environment Management:** python-dotenv
* **Version Control:** Git, GitHub

## 🚀 Getting Started

### Prerequisites
* Python 3.8+
* A free [Alpha Vantage API Key](https://www.alphavantage.co/)
* A PostgreSQL database (e.g., [Neon.tech](https://neon.tech/))

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/alpha_vantage_etl.git
   cd alpha_vantage_etl
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Create a `.env` file in the root directory and add your credentials:
   ```env
   ALPHA_VANTAGE_API_KEY=your_api_key_here
   DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require
   ```

## 📊 Usage

**1. Run the Batch ETL Pipeline**
Fetch the latest data for all configured stocks, calculate moving averages, and load them into the database.
```bash
python batch_extraction.py
```

**2. Launch the Dashboard**
Start the interactive Streamlit web application to view the data.
```bash
streamlit run dashboard.py
```

## 📂 Project Structure

* `batch_extraction.py` - Core ETL script for fetching and processing multiple stocks.
* `extraction.py` - Lightweight script for ad-hoc, single-ticker data extraction.
* `dashboard.py` - Streamlit application for data visualization.
* `requirements.txt` - Python dependencies.
* `.env` - Environment variables (ignored by Git).