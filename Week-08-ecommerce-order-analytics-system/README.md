# 🛒 E-Commerce Order Analytics System

> Building an end-to-end order analytics pipeline — covering data generation, cleaning, SQLite warehousing, advanced SQL analysis, and CLI reporting, for the **Celebal Technologies Intern Mini Project**.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Cleaning-150458?logo=pandas&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-Window%20Functions-4479A1?logo=postgresql&logoColor=white)
![CLI](https://img.shields.io/badge/CLI-Reporting%20Tool-333333)

---

## 📌 Objective

Build a small but complete **order analytics system** for an e-commerce company — generate realistic (and intentionally messy) order data, clean it, load it into a SQLite warehouse, analyze it with 16 SQL queries ranging from basic aggregations to window functions and cohort retention, and serve business summaries through a command-line reporting tool.

---
## 🧾 Overview

An e-commerce company's order data comes in messy from multiple sources — missing customer IDs, inconsistent date formats, invalid emails, orphaned records, and more. This project builds a small but complete pipeline that:

1. **Generates** realistic, intentionally messy order data
2. **Cleans** it and produces a data-quality report
3. **Loads** it into a SQLite warehouse
4. **Analyzes** it with 16 SQL queries — from basic aggregations to window functions and cohort retention
5. **Serves** business summaries through a command-line reporting tool
6. **Verifies** correctness with edge-case tests

---

## 🏗️ Architecture

This project loosely follows a **medallion architecture** (Bronze → Silver → Gold), a common pattern in real data engineering pipelines, scaled down to fit a local SQLite setup:

| Layer | What it is here | Folder |
|---|---|---|
| 🥉 **Bronze** (raw) | Untouched, messy generated data — the "as received from source" layer | `data/raw/` |
| 🥈 **Silver** (cleaned) | Validated, deduplicated, standardized data — safe to build reports on | `data/cleaned/` |
| 🥇 **Gold** (analytics) | Query-ready SQLite warehouse + business-level SQL outputs | `ecommerce.db`, `sql/` |

```text
                 ┌─────────────────────┐
                │   generate_data.py   │   
                └──────────┬───────────┘
                           ▼
             🥉 data/raw/*.csv  (BRONZE)
                - missing customer_ids
                - wrong date formats
                - invalid emails
                - orphan order_items
                - duplicate rows
                           │
                ┌──────────▼───────────┐
                │    clean_data.py      │   
                └──────────┬───────────┘
                           ▼
          🥈 data/cleaned/*.csv  (SILVER)
          + output/data_quality_report.txt
                           │
                ┌──────────▼───────────┐
                │     load_db.py        │   
                │   (sql/schema.sql)    │
                └──────────┬───────────┘
                           ▼
            🥇 ecommerce.db  (GOLD)
                           │
    ┌──────────────────────┼───────────────────────┐
    ▼                      ▼                        ▼
aggregations.sql     window_functions.sql      cohort_analysis.sql
(Q1-Q6)              (Q7-Q9, Q16)               (Q10-Q15)
 │                      │                        │
 └──────────────────────┴────────────────────────┘
                       ▼
     ┌──────────────────────┐
     │    report_cli.py     │   Business reports on demand
     └──────────────────────┘
```
---

## 📁 Project Structure
```
ecommerce-analytics-system/
├── data/
│   ├── raw/                    # 🥉 Bronze 
│   │   ├── customers.csv
│   │   ├── products.csv
│   │   ├── orders.csv
│   │   └── order_items.csv
│   └── cleaned/                 # 🥈 Silver 
│       ├── customers_clean.csv
│       ├── products_clean.csv
│       ├── orders_clean.csv
│       └── order_items_clean.csv
├── scripts/
│   ├── generate_data.py         
│   ├── clean_data.py           
│   ├── load_db.py               
│   ├── report_cli.py             
│   └── test_edge_cases.py       
├── sql/
│   ├── schema.sql                
│   ├── aggregations.sql           
│   ├── window_functions.sql       
│   └── cohort_analysis.sql       
├── output/
│   ├── data_quality_report.txt    # 🥇 Gold 
│   └── sample_reports/            
├── ecommerce.db                   # 🥇 Gold 
└── README.md
```
---

## 🗃️ Data Model
customers                orders                   order_items              products
──────────                ──────                   ───────────              ────────
customer_id (PK)  ┐       order_id (PK)     ┐      item_id (PK)             product_id (PK)
customer_name     │       customer_id (FK) ─┘      order_id (FK)  ─┐        product_name
email              │      order_date               product_id (FK)─┼───┐    category
registration_date  │      status                   quantity        │   │    subcategory
customer_type      └────► region_code               unit_price      │   │    cost_price
discount_percent│   │
▼   ▼
orders products

One customer → many orders → many order_items → each order_item references one product.

---

## ✅ What Was Built 

| Part | Requirement | Delivered in |
|---|---|---|
| Part 1 | Generate 4 CSVs, 500+ rows each, with intentional issues | `generate_data.py` |
| Part 2 | `clean_orders()`, `clean_products()`, `validate_emails()`, `check_referential_integrity()` | `clean_data.py` |
| Part 3 | 16 SQL queries: basic, intermediate, and advanced (window functions, CTEs, cohorts) | `sql/*.sql` |
| Part 4 | CLI tool: report type + date range → summary report with % change | `report_cli.py` |
| Part 5 | Edge case tests as Python functions | `test_edge_cases.py` |

---

## 🧮 SQL Queries

**Basic (`aggregations.sql`)**
1. Total revenue per category
2. Top 10 customers by order value
3. Month-wise order count, last 12 months

**Intermediate (`aggregations.sql`)**
4. Customers who never had a delivered order
5. Products with more returns than purchases
6. Return rate per category

**Advanced — Window Functions (`window_functions.sql`)**
7. Running total of revenue per region
8. `DENSE_RANK` — top products per category
9. `LAG` — days between consecutive orders, "At Risk" flag
16. Self-join — products frequently bought together

**Advanced — CTEs & Cohorts (`cohort_analysis.sql`)**
10. Multi-level CTE — monthly revenue buckets (High/Medium/Low)
11. `NTILE(4)` — customer quartiles (Platinum/Gold/Silver/Bronze)
12. Year-over-year revenue comparison
13. `FIRST_VALUE` / `LAST_VALUE` — category shift detection
14. Cumulative revenue distribution (Pareto-style)
15. Cohort retention analysis (month 0-3)

---

## 🎯 Key Design Decisions

**1. Referential integrity by construction, broken on purpose for testing.**
`generate_order_items()` only ever samples `order_id` from the list already created in `generate_orders()` — so the dataset is correct by default. Exactly 12 "orphan" rows are then injected on purpose with a fabricated `order_id`, so `check_referential_integrity()` has something real to catch.

**2. Don't delete data just because it looks unusual.**

| Issue | Action | Why |
|---|---|---|
| Negative quantity | Kept | It's a return, not an error — needed for return-rate queries |
| Zero quantity | Kept, flagged | No revenue impact, but could signal a real data-entry bug |
| Future order_date | Kept, flagged | Could be a legitimate scheduled/pre-order |
| Orphan order_items | **Removed** | No parent order → breaks every revenue join |
| Exact duplicate rows | **Removed** | Classic double-submit / re-run ETL artifact |

**3. `FIRST_VALUE`/`LAST_VALUE` need an explicit window frame in SQLite.**
By default the frame only extends to the current row — without `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`, `LAST_VALUE` just returns the current row's own value.

**4. "Last 12 months" is anchored to the latest order date in the data**, not `datetime.now()`, since this is sample data — anchoring to the real clock would return almost nothing.

---

## 🧪 Edge Case Handling

| # | Scenario | System behavior |
|---|---|---|
| 1 | `order_items.order_id` not in `orders` | Detected, logged, excluded from cleaned data |
| 2 | `discount_percent > 100` | Flagged and capped at 100 |
| 3 | `quantity = 0` | Kept and flagged — no revenue impact, but worth reviewing |
| 4 | `order_date` in the future | Kept and flagged — could be a valid scheduled order |

All verified with passing automated tests in `test_edge_cases.py`.

---

## 🧠 Challenges & What I Learned

- **Cleaning is a judgment call, not a mechanical process.** The "right" fix depends on what the data will be used for downstream — not just whether a value looks odd.
- **SQLite's window function frames have real quirks.** `FIRST_VALUE`/`LAST_VALUE` silently returning the "wrong but plausible" answer without an explicit frame was the hardest bug to catch in this whole project.
- **Cohort month-offset math isn't a built-in function** — had to build it manually from `strftime()` year/month parts, and get the year-boundary math right.
- **Splitting the pipeline into small, independently runnable scripts** made debugging dramatically faster than working in one giant file.
- **A written data-quality report (not just print statements)** made it much easier to sanity-check my own work at every stage — something I'd carry into future projects.

---

## 🔭 Future Improvements

- Add `--start`/`--end` validation in the CLI tool (currently assumes start < end)
- Extend cohort retention tracking beyond month 3
- Add `EXPLAIN QUERY PLAN` checks on the heavier window-function queries for a larger dataset
- Fuzzy-match product names to catch near-duplicates beyond casing/spacing differences

---
**Author:** Nidhi Bansal · 
Data Engineer Intern at Celebal Technologies 







