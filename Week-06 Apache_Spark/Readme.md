# Week-06: Apache Spark

This week's assignment covers core Apache Spark concepts using **PySpark** — Spark architecture, lazy evaluation, DataFrame transformations, fault tolerance, file formats (CSV vs Parquet), and building a simple read → transform → filter → write pipeline.

All queries were tested on a custom 1000-row sample dataset (`Data/source.csv`).

---

## 📁 Folder Structure

```
Week-06 Apache_Spark/
├── Data/
│   └── source.csv          
├── Week_06_Apache_Spark.ipynb   
└── README.md
```

---

## 🗂️ Dataset

A synthetic sales dataset with 1000 rows was used to test every query practically instead of just writing code blind. It includes:

| Column | Description |
|---|---|
| `order_id` | unique row id |
| `old_name` / `new_name` | customer name (renamed in Q6) |
| `product_id` | product identifier |
| `category` | e.g. Electronics, Clothing, Books |
| `price` | stored as string on purpose, to demonstrate casting |
| `base_price` | numeric base price |
| `status` | Completed / Pending / Cancelled |
| `amount` | order amount |
| `region` | North / South / East / West |
| `priority` | High / Medium / Low |
| `user_id` | ~5% intentionally left blank, to test null-filtering |

---

## ✅ What's Covered

### Spark Architecture
- Roles of **Driver**, **Cluster Manager**, and **Executor**
- **Client Mode vs Cluster Mode**

### Spark Internals
- **Lazy Evaluation** — how Spark builds an execution plan (DAG) before running anything, and why that helps performance
- **Lineage Graph** — how Spark uses it to recompute lost partitions instead of restarting a whole job (fault tolerance)
- **Transformations vs Actions** — with examples

### File Formats
- **CSV vs Parquet** — row-based vs columnar storage, and why it affects performance
- **Predicate Pushdown** in Parquet — filtering at read-time instead of after loading everything into memory

### DataFrame Operations (all tested on the dataset)
- Reading CSV with `header=True, inferSchema=True`
- `select()` + `filter()` on a column condition
- Renaming columns (`withColumnRenamed`) and type casting (`cast("double")`)
- Multi-condition filtering with `AND` (`&`) and `OR` (`|`)
- Adding a derived column (`final_price = base_price * 1.18`)
- Handling **null values** before writing output
- Building a small **pipeline**: read Parquet → filter nulls → write CSV

### Best Practices
- Avoided `.collect()` everywhere — used `.show(5)` instead, since `.collect()` pulls the entire dataset into the Driver's memory and can crash on large data
- Used `mode("overwrite")` on writes to make the notebook safely re-runnable

---

## 📊 Performance & Architecture Insights

- **Lazy evaluation** lets Spark see the *entire* chain of transformations before running anything, so it can optimize the whole plan (e.g. combine filters, skip unused columns) instead of executing each step blindly.
- **Parquet beats CSV** for analytical workloads because it's columnar — reading 2 out of 10 columns only touches those 2 columns on disk, unlike CSV which has to read full rows regardless.
- **Predicate pushdown** means filter conditions are applied *while reading* a Parquet file, not after — so entire row-groups that can't match get skipped, cutting down memory usage significantly.
- **Lineage graph (DAG)** is what makes Spark fault-tolerant without needing data replication — if a node dies, Spark just recomputes the lost partitions from the recorded transformation history instead of restarting the full job.
- **`.show(5)` over `.collect()`** is a non-negotiable habit at scale — `.collect()` tries to bring the *entire* result set into the Driver's memory, which is fine for small results but a guaranteed crash risk on multi-terabyte data.

---

## 🧠 Key Takeaway

Spark's biggest advantage isn't just "distributed processing" — it's that **laziness + lineage** together let it optimize a whole pipeline *and* recover from failures without expensive data replication. Understanding when to use Parquet over CSV, and when to filter early (predicate pushdown) vs late, made a real difference in how I now think about writing efficient pipelines instead of just "code that works."

---

## 👤 Author

**Nidhi Bansal**
Data Engineer Intern
