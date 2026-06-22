<div align="center">

# ⚡ Spark Basics — Data Cleaning, Transformation & Aggregation

### *Week 5 Assignment — Big Data Analytics*

![Apache Spark](https://img.shields.io/badge/Apache%20Spark-3.x-E25A1C?style=for-the-badge&logo=apachespark&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PySpark](https://img.shields.io/badge/PySpark-DataFrames-orange?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)

*"Hadoop reads from disk. Spark just remembers."*

</div>

---

## 🎯 Objective

Learn the basics of **Apache Spark** and use it to **clean, transform, and analyze data** using DataFrames — covering everything from why Spark beats MapReduce, to building a complete data-cleaning + aggregation pipeline from scratch.

---

## 📖 Overview

This repo walks through Spark fundamentals step-by-step on a **1000-row e-commerce-style dataset** that's intentionally messy — duplicate transactions, missing prices, empty usernames, null emails — basically every headache you'd actually run into with real data.

The notebook covers:

| Stage | What Happens |
|---|---|
| 🚀 Setup | Spin up a Spark session |
| 📥 Load | Read the CSV into a DataFrame |
| 🧹 Clean | Drop duplicates, handle nulls, fix inconsistent data |
| 🔍 Filter | Slice data by age, category, region |
| 🔄 Transform | Rename columns, cast types |
| 📊 Aggregate | count, sum, avg, min, max |
| 🗂️ Group | groupBy + conditions on aggregated results |
| 🌀 Shuffle | Understand wide transformations under the hood |
| 🏗️ Pipeline | Combine all of the above into one clean flow |

---

## 🛠️ Tech Stack

- **Apache Spark (PySpark)** — distributed in-memory data processing
- **Python 3** — driver language
- **Google Colab** — notebook environment (zero local setup needed)
- **Pandas** — used only for dataset generation, not the actual processing
- **GitHub** — version control & submission

---

## 🗃️ Dataset Info

**File:** `data/dataset.csv` &nbsp;|&nbsp; **Rows:** 1000 &nbsp;|&nbsp; **Columns:** 14

| Column | Type | Notes |
|---|---|---|
| `user_id` | int | unique-ish, repeats in intentional duplicate rows |
| `username` | string | a few empty strings on purpose |
| `age` | int | 15–65 |
| `subscription` | string | `Premium` / `Basic` |
| `region` | string | `West` / `East` / `North` / `South` |
| `city` | string | 12 Indian cities |
| `product_category` | string | Electronics, Clothing, Furniture, etc. |
| `sale_amount` | double | has nulls |
| `price` | double | has nulls |
| `email` | string | has nulls **and** empty strings |
| `transaction_date` | date | used with `user_id` for dedup |
| `raw_timestamp` | string | gets cast → `TimestampType` |
| `status` | string | has nulls — filled with `'Unknown'` |
| `store_id` | string | 20 stores, used for final revenue groupBy |

> 💡 ~150 duplicate rows and scattered nulls/empties were baked in **on purpose** so the cleaning steps actually produce a visible before/after difference.

---

## 📂 Repo Structure

```
spark-assignment/
├── data/
│   └── dataset.csv          # 1000-row messy dataset
├── notebook/
│   └── spark_basics.ipynb   # full runnable pipeline
├── output/
│   └── results.csv          # final aggregated output
└── README.md                # you're reading it
```

---

## ✅ Assignment Questions Covered

| # | Topic |
|---|---|
| Q1 | MapReduce limitations vs Spark |
| Q2 | In-memory computing for iterative ML |
| Q3 | Removing duplicates on `user_id` + `transaction_date` |
| Q4 | Filter region + groupBy avg sale amount |
| Q5 | `.na.drop()` vs `.na.fill()` |
| Q6 | groupBy city count with `count > 100` |
| Q7 | Immutability & its effect on cleaning |
| Q8 | Filter by age range + subscription type |
| Q9 | Why nulls should be handled before aggregation |
| Q10 | Casting `raw_timestamp` → `TimestampType`, renaming column |
| Q11 | Shuffle process & wide transformations |
| Q12 | Removing null/empty email & username rows |
| Q13 | `.agg()` with multiple stats at once |
| Q14 | Risks of `inferSchema=true` on messy dates |
| Q15 | Full pipeline: dedup → fill nulls → groupBy revenue |

---

## 📤 Output Files

- **`output/results.csv`** — final revenue grouped by `store_id` after the full cleaning + aggregation pipeline
- Inline `.show()` outputs throughout the notebook for every intermediate step (row counts before/after dedup, filtered subsets, grouped aggregates, etc.)

---

## 🧠 Key Learnings

- **Spark beats MapReduce mainly because of in-memory processing** — no constant disk round-trips between stages.
- **DataFrames are immutable** — every transformation (`drop`, `rename`, `filter`) returns a *new* DataFrame, it never edits in place.
- **Clean before you aggregate.** Nulls quietly skew `avg()` and `sum()` if left unhandled — order of operations matters.
- **`groupBy()` triggers a shuffle** — data gets physically moved across partitions to bring matching keys together, which is what makes it a *wide* transformation (vs `filter()`/`map()` which are *narrow* and don't need this).
- **`inferSchema=True` is convenient but risky** on inconsistent data — it can silently mistype columns or turn unparseable values into nulls without warning.
- Building the **pipeline last** (after understanding each piece individually) made it obvious how cleaning → filtering → transforming → aggregating naturally chain together in real workflows.

---

<div align="center">

### 👩‍💻 Author

**Nidhi Bansal**
Data Engineer Intern at Celebal Technologies

*Big Data Analytics — Week 5 Assignment*

</div>
