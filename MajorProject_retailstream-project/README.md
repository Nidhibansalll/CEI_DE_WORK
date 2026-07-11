# RetailStream — Batch, Incremental & Streaming Data Pipeline

![PySpark](https://img.shields.io/badge/PySpark-E25A1C?style=for-the-badge&logo=apachespark&logoColor=white)
![Databricks](https://img.shields.io/badge/Databricks-FF3621?style=for-the-badge&logo=databricks&logoColor=white)
![Delta Lake](https://img.shields.io/badge/Delta%20Lake-00ADD8?style=for-the-badge&logo=delta&logoColor=white)
![SQL](https://img.shields.io/badge/SparkSQL-4479A1?style=for-the-badge&logo=databricks&logoColor=white)

**PySpark · SparkSQL · Delta Lake · Databricks**

A Bronze → Silver → Gold pipeline built for RetailStream Inc., a fictional multi-city e-commerce retailer,
covering four core data engineering patterns in one notebook: an initial batch load, an incremental append
with deduplication, a streaming ingestion with Auto Loader, and a MERGE-based fix for a late-arriving file.

| | |
|---|---|
| **Author** | Nidhi Bansal |
| **Track** | Data Engineering Internship |
| **Platform** | Databricks (Unity Catalog Volumes) |
| **Notebook** | `Major_Project_Retail_Stream.ipynb` |
| **Report** | `RetailStream_Project_Report.pdf` |

---

## 🎯 Why this project

Most tutorials teach batch loading in isolation. Real retail pipelines rarely get that luxury — a store gets
onboarded mid-quarter, a payment feed shows up as a stream instead of a file, and a backfill lands two months
late because of a system migration. RetailStream is built around exactly that kind of mess: four ingestion
patterns feeding the same target table, each with a different correctness requirement.

## 🏗️ Architecture

```
                    ┌──────────┐      ┌──────────┐      ┌──────────┐      ┌──────────┐
                    │  Source  │ ───► │  Bronze  │ ───► │  Silver  │ ───► │   Gold   │
                    │UC Volume │      │+ audit   │      │ enriched │      │  SparkSQL│
                    │raw CSVs  │      │ columns  │      │  orders  │      │aggregates│
                    └──────────┘      └────▲─────┘      └──────────┘      └──────────┘
                                            │
        ┌──────────────┬──────────────┬────┴──────────┬──────────────┐
        │  Batch load  │ Incremental  │  Auto Loader   │    MERGE     │
        │   Task 1     │   Task 2     │    Task 3      │    Task 4    │
        │  Jan orders  │ anti-join    │ streaming txns │ late S04 file│
        └──────────────┴──────────────┴────────────────┴──────────────┘
```

All raw files and Delta tables live in a **Unity Catalog Volume**
(`/Volumes/databricksmaster/default/retailstream`) rather than legacy DBFS — Volumes are Databricks' current
governance-aware storage layer for non-tabular files.

## 📁 Repository structure

```
MajorProject_retailstream-project/
├── Major_Project_Retail_Stream.ipynb   <- the pipeline
├── README.md                                
├── RetailStream_Project_Report.pdf      
└── data/
    ├── products.csv, customers.csv, stores.csv
    ├── batch_initial/orders_2024_01.csv
    ├── batch_incremental/orders_2024_02.csv
    ├── late_arriving/orders_2024_01_LATE.csv
    └── autoloader_landing/transactions_*.csv  (3 files)
```
`checkpoints/` and `delta/` are intentionally **not** committed — they're runtime output the notebook
regenerates on every run, not source code.

## ✅ What each task does

| Task | What it does | Verified result |
|---|---|---|
| 1 — Initial batch load | Read January orders with an explicit schema, stamp audit columns, write Bronze | 20 rows |
| 2 — Incremental load | Append February orders via a `left_anti` join so already-loaded orders aren't re-inserted | 40 rows (2 real duplicate order_ids caught and skipped) |
| 3 — Auto Loader streaming | `cloudFiles` ingests all landed transaction files with its own checkpoint | 15 rows |
| 4 — Late-arriving MERGE | Store S04's delayed January orders merged in, idempotent on re-run | 45 total / 5 inserted by the merge |
| 5 — Silver enrichment | Left-join to product/customer/store dimensions, compute revenue & margin | 45 rows |
| 6 — Gold aggregates | SparkSQL monthly sales summary + payment method summary | 2 + 4 rows |

## 📊 Results

**Monthly sales (`gold_monthly_sales`)**

| month | total_orders | total_revenue | total_margin | avg_order_value |
|---|---|---|---|---|
| 2024-01 | 25 | 731,900 | 71,700 | 29,276.00 |
| 2024-02 | 20 | 959,000 | 615,800 | 47,950.00 |

**Payment methods (`gold_payment_summary`)**

| payment_method | total_transactions | success_rate | total_amount |
|---|---|---|---|
| UPI | 5 | 60.00% | 90,437.22 |
| DEBIT_CARD | 4 | 75.00% | 112,412.42 |
| NET_BANKING | 3 | 66.67% | 51,857.39 |
| CREDIT_CARD | 3 | 100.00% | 107,487.12 |

## ❓ The three questions

### (a) How was deduplication handled in Task 2?

A **left-anti join** against the `order_id`s already in `bronze_orders`, not `dropDuplicates()` —
`dropDuplicates()` only catches duplicates *within* the new file, not rows that already exist in the target
table, which is the actual risk here. This wasn't hypothetical: `orders_2024_02.csv` genuinely contains 22
rows, and 2 of them (`ORD003`, `ORD013`) are exact repeats of January orders already loaded in Task 1. The
anti-join correctly dropped both, landing on 40 rows instead of 42. It also makes the cell safe to re-run —
a second pass finds every Feb `order_id` already present and appends nothing.

### (b) What happens if the Auto Loader checkpoint is deleted and the stream restarts?

The checkpoint holds Auto Loader's record of which files it has already ingested. Delete it and restart, and
Auto Loader has no memory of prior progress — it treats every file currently in the landing folder as brand
new and reprocesses all of it. If `bronze_transactions` is left untouched, this **duplicates** every
previously-ingested row. If the table is also dropped and recreated, it's a clean re-ingest, but you've lost
the incremental benefit entirely — it's a full historical reload, not a resumed stream.

### (c) Why is MERGE preferred over overwrite for late-arriving data?

`overwrite` replaces the entire table with just the late file's rows — the other 40 records vanish.
`append` is safer but still not idempotent: if the late file is ever re-dropped into the landing zone (a
retried backfill, a re-run pipeline step), it creates duplicate `order_id`s with no error raised. `MERGE ...
WHEN NOT MATCHED THEN INSERT` solves both: it targets the existing table without destroying it, and every row
is matched on `order_id`, so a row already present is left untouched. Running Task 4 once or five times lands
on the same 45 rows either way.

## 🙏 Acknowledgments

This project was built as part of the Data Engineering track at **Celebal Technologies**, and I'm grateful
for the guidance and code reviews from my mentors **Yashashvi Dubey Mam, Raj Biswas sir** throughout the internship — their feedback on schema
design, idempotency, and thinking through failure modes (not just the happy path) shaped how this pipeline
is structured. Thank you to the **Celebal team** for the structured, hands-on learning environment that made a
project like this possible.

---

