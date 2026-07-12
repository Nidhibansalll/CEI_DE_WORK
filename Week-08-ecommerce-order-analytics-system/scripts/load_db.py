"""
load_db.py
----------
Author: Nidhi

Small helper script that builds ecommerce.db from the cleaned CSVs using
sql/schema.sql. I kept this separate from clean_data.py because I wanted
cleaning and "loading into SQL" to be two independent, re-runnable steps -
useful while I was debugging the SQL queries and didn't want to re-run the
(slower) cleaning step every time.
"""

import os
import sqlite3
import pandas as pd

BASE = os.path.join(os.path.dirname(__file__), "..")
CLEAN_DIR = os.path.join(BASE, "data", "cleaned")
SQL_DIR = os.path.join(BASE, "sql")
DB_PATH = os.path.join(BASE, "ecommerce.db")


def build_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)

    with open(os.path.join(SQL_DIR, "schema.sql")) as f:
        conn.executescript(f.read())

    customers = pd.read_csv(os.path.join(CLEAN_DIR, "customers_clean.csv"))
    products = pd.read_csv(os.path.join(CLEAN_DIR, "products_clean.csv"))
    orders = pd.read_csv(os.path.join(CLEAN_DIR, "orders_clean.csv"))
    order_items = pd.read_csv(os.path.join(CLEAN_DIR, "order_items_clean.csv"))

    # orders with no parsable date got NaT during cleaning - sqlite doesn't
    # like NaT, so drop those few rows only when loading (they're still
    # visible in the cleaned CSV + the data quality report)
    orders = orders.dropna(subset=["order_date"])

    customers.to_sql("customers", conn, if_exists="append", index=False)
    products.to_sql("products", conn, if_exists="append", index=False)
    orders.to_sql("orders", conn, if_exists="append", index=False)
    order_items.to_sql("order_items", conn, if_exists="append", index=False)

    conn.commit()

    counts = {}
    for table in ["customers", "products", "orders", "order_items"]:
        counts[table] = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]

    conn.close()
    print(f"Database built at {DB_PATH}")
    for table, count in counts.items():
        print(f"  {table}: {count} rows")


if __name__ == "__main__":
    build_database()
