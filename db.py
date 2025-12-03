import sqlite3
from datetime import datetime

DB_NAME = "currency_rates.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS rates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            currency TEXT NOT NULL,
            rate REAL NOT NULL,
            fetched_at TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_currency ON rates (currency)
    """)

    conn.commit()
    conn.close()


def save_rate(currency: str, rate: float):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    fetched_at = datetime.now().isoformat()

    cur.execute("""
        INSERT INTO rates (currency, rate, fetched_at)
        VALUES (?, ?, ?)
        ON CONFLICT(currency) DO UPDATE SET
            rate = excluded.rate,
            fetched_at = excluded.fetched_at
    """, (currency, rate, fetched_at))

    conn.commit()
    conn.close()


def get_saved_rate(currency: str) -> float | None:
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        SELECT rate FROM rates WHERE currency = ?
    """, (currency,))

    row = cur.fetchone()
    conn.close()

    return row[0] if row else None