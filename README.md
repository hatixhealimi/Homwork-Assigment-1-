# Homework 1 – Crypto Market Data Pipeline (Pipe-and-Filter, SQLite)

This project implements an automated data ingestion pipeline for historical cryptocurrency market data using the **Pipe-and-Filter architectural style**.

The pipeline:

- Downloads top active cryptocurrencies (Filter 1)
- Checks last saved date in the SQLite database (Filter 2)
- Downloads missing OHLCV data from CoinGecko (Filter 3)
- Saves data into a structured SQLite database

Team:
- **Bora Alili – 231504**
- **Edita Axhami – 231513**
- **Hatixhe Alimi – 231533**

## How to Run

1. Open terminal inside the `pipeline/` folder  
2. Install dependencies:
3.  Run the ETL pipeline:


## Technologies

- Python 3
- SQLite
- CoinGecko API
- Pipe-and-Filter Architecture



