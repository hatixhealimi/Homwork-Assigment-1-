# Project Description – Crypto Exchange Analytics Pipeline  
**Homework 1 – Software Design and Architecture**

## Team Members
- **Bora Alili – 231504**
- **Edita Axhami – 231513**
- **Hatixhe Alimi – 231533**

## 1. Overview
This project develops an automated ETL (Extract–Transform–Load) data pipeline for cryptocurrency analytics using the **Pipe-and-Filter architectural style**. The system focuses on collecting historical daily OHLCV data for the top 1000 active cryptocurrencies across major exchanges.

The final product is a structured SQLite database containing accurate, complete, and updated historical crypto market data.

## 2. Technologies Used
- **Python 3**
- **SQLite**
- **CoinGecko API (free, no key required)**
- **Pipe-and-Filter architecture**

## 3. Data Sources
We evaluated:
- Binance API  
- Coinbase API  
- Kraken API  
- CoinMarketCap  
- CoinGecko  

We selected **CoinGecko** because:
- Free  
- No API key  
- Unified data  
- Supports OHLC data  
- Active and stable  

## 4. Data to Be Processed
- Top 1000 symbols  
- Daily OHLCV:
  - Open  
  - High  
  - Low  
  - Close  
  - Volume  
- 24h data (liquidity, market cap, etc.)

## 5. Processing Pipeline
The pipeline follows:

1. **Filter 1 — Symbol Discovery**
   - Fetch top 1000 coins
   - Apply liquidity and validity filters

2. **Filter 2 — Last Synced Date**
   - Check SQLite for last date stored
   - If none → download 10 years

3. **Filter 3 — Missing Data Download**
   - Get all missing OHLCV
   - Store in database

## 6. Expected Results
- Fully populated database
- Validated data
- Consistent formatting
- Automated incremental updates

