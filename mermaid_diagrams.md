1. Pipe-and-Filter Architecture Diagram
flowchart LR
    A[Filter 1<br/>Fetch Top 1000 Coins<br/>- CoinGecko API<br/>- Remove duplicates<br/>- Liquidity filter] 
        --> B[Filter 2<br/>Check Last Stored Date<br/>- SQLite lookup<br/>- Determine start_date]

    B --> C[Filter 3<br/>Download Missing OHLCV<br/>- OHLC + Volume endpoints<br/>- Format data]

    C --> D[(SQLite Database<br/>symbols + ohlcv_daily)]

    style A fill:#ffd27f,stroke:#333,stroke-width:1px
    style B fill:#ffe9a8,stroke:#333,stroke-width:1px
    style C fill:#fff7ba,stroke:#333,stroke-width:1px
    style D fill:#c4ffd0,stroke:#333,stroke-width:1px

2. ETL Dataflow Diagram (Full Data Movement)

flowchart LR
    API[CoinGecko API<br/>Raw Crypto Market Data] 
        --> F1[Filter 1<br/>Symbol Processing]

    F1 --> F2[Filter 2<br/>Determine Last Date]

    F2 --> F3[Filter 3<br/>Download Missing OHLCV]

    F3 --> DB[(SQLite Database<br/>Normalized Tables)]
    
    DB --> OUT[Clean Data for UI or Analysis]

    
3. System Context Diagram
flowchart TB
    User[End User<br/>Student / Analyst / TA]
    Sys[Crypto Analytics System]

    Pipeline[ETL Pipeline<br/>Pipe-and-Filter Architecture]
    DB[(SQLite Database)]
    API[CoinGecko Public API]

    User --> Sys
    Sys --> DB
    Pipeline --> DB
    Pipeline --> API
    API --> Pipeline

   
5. Component Diagram (For Future Homeworks)
flowchart TB
    UI[Web Frontend<br/>Charts, Tables, Filters]
    Backend[Backend API<br/>(Flask/FastAPI)]
    ETL[ETL Pipeline<br/>Pipe-and-Filter]
    DB[(SQLite Database)]
    API[CoinGecko API]

    UI --> Backend
    Backend --> DB
    Backend --> ETL
    ETL --> DB
    ETL --> API
   
5. Database ER Diagram
erDiagram
    SYMBOLS {
        INTEGER id PK
        TEXT cg_id UNIQUE
        TEXT symbol
        TEXT name
        REAL market_cap
        REAL total_volume
        TIMESTAMP last_sync
    }

    OHLCV_DAILY {
        INTEGER id PK
        INTEGER symbol_id FK
        TEXT date
        REAL open
        REAL high
        REAL low
        REAL close
        REAL volume
    }

    SYMBOLS ||--o{ OHLCV_DAILY : contains
   
6. High-Level System Flow (Complete Homework 1 Overview)
sequenceDiagram
    participant Script as Pipeline Script
    participant Filter1 as Filter 1<br/>Fetch Coins
    participant Filter2 as Filter 2<br/>Check DB
    participant Filter3 as Filter 3<br/>Download OHLCV
    participant DB as SQLite Database
    participant API as CoinGecko API

    Script ->> Filter1: Run Filter 1
    Filter1 ->> API: Request top 1000 coins
    API -->> Filter1: Return coin list

    Filter1 -->> Script: Validated symbol list

    Script ->> Filter2: Run Filter 2 with list
    Filter2 ->> DB: Query max(date)
    DB -->> Filter2: Last stored date
    Filter2 -->> Script: Start dates per symbol

    Script ->> Filter3: Run Filter 3 with dates
    Filter3 ->> API: Request daily OHLCV
    API -->> Filter3: OHLCV data
    Filter3 ->> DB: Insert rows (INSERT OR IGNORE)

    Script -->> Script: Print execution time

