# Requirements Specification – Crypto Analytics Pipeline
Team:
- **Bora Alili – 231504**
- **Edita Axhami – 231513**
- **Hatixhe Alimi – 231533**

---

## 1. Introduction

### 1.1 Purpose
This document defines all functional and non-functional requirements for a cryptocurrency analytics system that collects historical market data using a Pipe-and-Filter architecture.

### 1.2 Scope
Homework 1 includes:
- Data ingestion
- Data validation
- Data transformation
- Database storage

Later homeworks will add:
- Backend API
- Web UI
- Architecture expansion

### 1.3 Stakeholders
- Students
- Instructors
- Crypto analysts
- Researchers

---

## 2. Personas

### Persona 1: Mila (Data Science Student)
Needs clean data for statistical analysis.

### Persona 2: Marko (Crypto Trader)
Wants long-term price history.

### Persona 3: Ana (Teaching Assistant)
Uses this project to demonstrate architecture patterns.

---

## 3. User Scenarios

### Scenario 1 – Downloading BTC data
Mila runs the tool → gets 10 years of Bitcoin OHLCV.

### Scenario 2 – Comparing ETH & SOL
Marko visualizes ETH vs. SOL (future homework).

### Scenario 3 – Teaching Pipe-and-Filter
Ana shows the 3 filters running in order.

---

## 4. Functional Requirements

### FR-1: Fetch Top Symbols
System downloads top active cryptocurrencies.

### FR-2: Filter Invalid Symbols
Removes:
- Low volume
- Duplicates
- Missing data

### FR-3: Determine Start Dates
Looks up last saved day in database.

### FR-4: Download OHLCV Data
Fetches daily:
- Open  
- High  
- Low  
- Close  
- Volume  

### FR-5: Store in SQLite
Saves into:
- `symbols`
- `ohlcv_daily`

### FR-6: Support Incremental Updates
Only missing days are fetched.

### FR-7: Timing Measurement
Prints total runtime.

---

## 5. Non-Functional Requirements

### Performance
- DB operations < 0.01s each
- Pipeline should handle 1000 assets efficiently

### Reliability
- Retries network failures
- Safe DB inserts

### Usability
- Simple run command
- Clear console output

### Maintainability
- Each filter isolated
- No shared mutable state

---

## 6. System Architecture

This project uses **Pipe-and-Filter**:

1. Filter 1 → symbol discovery  
2. Filter 2 → state checking  
3. Filter 3 → OHLCV processing  

Database is relational SQLite.

---

## 7. Database Schema

### symbols
| Field | Type | Notes |
|-------|------|--------|
| id | INTEGER | PK |
| cg_id | TEXT | CoinGecko ID |
| symbol | TEXT | Ticker |
| name | TEXT | Coin name |
| market_cap | REAL | |
| total_volume | REAL | |
| last_sync | TIMESTAMP | |

### ohlcv_daily
| Field | Type |
|-------|------|
| id | INTEGER PK |
| symbol_id | INTEGER FK |
| date | TEXT |
| open | REAL |
| high | REAL |
| low | REAL |
| close | REAL |
| volume | REAL |

