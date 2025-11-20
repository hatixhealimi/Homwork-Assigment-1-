import requests
import sqlite3
import time
from datetime import datetime, timedelta

DB_PATH = "crypto_data.db"
BASE_URL = "https://api.coingecko.com/api/v3"
TOP_COINS = 1000
MIN_VOLUME = 1000000  # liquidity threshold


# ============================================================
# DATABASE INITIALIZATION
# ============================================================
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS symbols (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cg_id TEXT UNIQUE,
            symbol TEXT,
            name TEXT,
            market_cap REAL,
            total_volume REAL,
            last_sync TIMESTAMP
        );
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS ohlcv_daily (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol_id INTEGER,
            date TEXT,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume REAL,
            UNIQUE(symbol_id, date)
        );
    """)

    conn.commit()
    return conn


# ============================================================
# HELPER: API GET WITH RETRIES
# ============================================================
def fetch_json(url, params=None):
    for attempt in range(3):
        try:
            r = requests.get(url, params=params)
            if r.status_code == 200:
                return r.json()
        except:
            pass

        print(f"Retrying API ({attempt+1}/3)...")
        time.sleep(1)

    raise Exception(f"API failed: {url}")


# ============================================================
# FILTER 1: FETCH TOP SYMBOLS
# ============================================================
def filter1_symbols():
    print("\n===== FILTER 1: Fetching top crypto symbols =====")

    all_coins = []
    page = 1

    while len(all_coins) < TOP_COINS:
        data = fetch_json(
            f"{BASE_URL}/coins/markets",
            {
                "vs_currency": "usd",
                "order": "market_cap_desc",
                "per_page": 250,
                "page": page
            }
        )
        if not data:
            break

        all_coins.extend(data)
        page += 1

    seen = set()
    final = []

    for c in all_coins[:TOP_COINS]:
        ticker = c["symbol"].upper()

        if ticker in seen:
            continue
        if c["total_volume"] < MIN_VOLUME:
            continue

        final.append({
            "cg_id": c["id"],
            "symbol": ticker,
            "name": c["name"],
            "market_cap": c["market_cap"],
            "total_volume": c["total_volume"]
        })
        seen.add(ticker)

    print(f"✔ Filter 1: {len(final)} valid symbols selected.")
    return final


# ============================================================
# FILTER 2: CHECK LAST STORED DATE
# ============================================================
def filter2_dates(conn, symbols):
    print("\n===== FILTER 2: Checking last stored dates =====")
    c = conn.cursor()

    output = []

    for s in symbols:
        # Insert symbol metadata if not exists
        c.execute("""
            INSERT OR IGNORE INTO symbols (cg_id, symbol, name, market_cap, total_volume)
            VALUES (?, ?, ?, ?, ?)
        """, (s["cg_id"], s["symbol"], s["name"], s["market_cap"], s["total_volume"]))

        conn.commit()

        # Get local symbol_id
        c.execute("SELECT id FROM symbols WHERE cg_id=?", (s["cg_id"],))
        symbol_id = c.fetchone()[0]

        # Find last stored date
        c.execute("SELECT MAX(date) FROM ohlcv_daily WHERE symbol_id=?", (symbol_id,))
        last = c.fetchone()[0]

        if last:
            start_date = datetime.strptime(last, "%Y-%m-%d").date() + timedelta(days=1)
        else:
            start_date = datetime.utcnow().date() - timedelta(days=365 * 10)

        output.append({
            "symbol_id": symbol_id,
            "cg_id": s["cg_id"],
            "symbol": s["symbol"],
            "start_date": start_date
        })

    print("✔ Filter 2: Dates prepared for all symbols.")
    return output


# ============================================================
# FILTER 3: DOWNLOAD OHLCV FOR MISSING DAYS
# ============================================================
def filter3_ohlcv(conn, symbol_items):
    print("\n===== FILTER 3: Downloading OHLCV data =====")
    c = conn.cursor()

    for item in symbol_items:
        start = item["start_date"]
        today = datetime.utcnow().date()

        missing = (today - start).days

        if missing <= 0:
            print(f"{item['symbol']}: ✓ up to date")
            continue

        days_to_fetch = min(missing, 3650)

        print(f"{item['symbol']}: Fetching {days_to_fetch} days from {start} → {today}")

        # OHLC data
        ohlc = fetch_json(
            f"{BASE_URL}/coins/{item['cg_id']}/ohlc",
            {"vs_currency": "usd", "days": days_to_fetch}
        )

        # Volume data
        volumes = fetch_json(
            f"{BASE_URL}/coins/{item['cg_id']}/market_chart",
            {"vs_currency": "usd", "days": days_to_fetch}
        )["total_volumes"]

        volume_map = {
            datetime.utcfromtimestamp(v[0] / 1000).strftime("%Y-%m-%d"): v[1]
            for v in volumes
        }

        inserted = 0

        for row in ohlc:
            ts, op, hi, lo, cl = row
            dt = datetime.utcfromtimestamp(ts / 1000).strftime("%Y-%m-%d")

            try:
                c.execute("""
                    INSERT OR IGNORE INTO ohlcv_daily
                    (symbol_id, date, open, high, low, close, volume)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    item["symbol_id"], dt, op, hi, lo, cl,
                    volume_map.get(dt)
                ))
                inserted += c.rowcount
            except Exception as e:
                print("Insert error:", e)

        conn.commit()
        print(f"{item['symbol']}: {inserted} rows inserted")


# ============================================================
# PIPELINE ORCHESTRATOR
# ============================================================
def run_pipeline():
    print("=== STARTING PIPELINE ===")
    start = time.time()

    conn = init_db()
    step1 = filter1_symbols()
    step2 = filter2_dates(conn, step1)
    filter3_ohlcv(conn, step2)
    conn.close()

    print(f"\n=== PIPELINE COMPLETE in {time.time() - start:.2f} seconds ===")


if __name__ == "__main__":
    run_pipeline()
