# 🚀 Week 07 — Delta Lake Incremental Data Processing

> Implementing incremental data pipelines using **Delta Lake's MERGE** capability on the Superstore dataset — covering data loading, cleaning, incremental simulation, merge, and validation on **Azure Databricks**.

![Delta Lake](https://img.shields.io/badge/Delta%20Lake-00ADD8?style=flat&logo=databricks&logoColor=white)
![Azure Databricks](https://img.shields.io/badge/Azure%20Databricks-FF3621?style=flat&logo=databricks&logoColor=white)
![PySpark](https://img.shields.io/badge/PySpark-E25A1C?style=flat&logo=apachespark&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)

---

## 📌 Objective

Perform **incremental data processing** using Delta Lake — load a dataset into a Delta table, clean it, simulate a real-world incremental batch (updates + new records), apply a `MERGE` operation, and validate the final result for consistency.

---

## 🗂️ Project Structure

```
Week-07-delta-lake-assignment/
├── Datasets/
│   ├── Sample - Superstore.csv        # Original raw dataset
│   ├── customer_master.csv            # Cleaned master data (exported)
│   └── customer_incremental.csv       # Simulated incremental batch (exported)
│
├── notebook/
│   └── delta_scd_assignment.ipynb     
│
├── screenshots/
│   ├── 01_Load_Dataset.png
│   ├── 02_data_cleaning.png
│   ├── 03_Save_Delta_Table.png
│   ├── 04_Read_Delta_Table.png
│   ├── 05_Create_Incremental_Data.png
│   ├── 06_Merge_Result.png
│   ├── 07-validation.png
│   └── final_output.png
│
└── README.md
```

---

## ⚙️ Tech Stack

| Component | Tool Used |
|---|---|
| Compute | Azure Databricks (Serverless) |
| Storage | Unity Catalog Volumes |
| Processing Engine | PySpark |
| Table Format | Delta Lake |
| Language | Python |

---

## 🔄 Workflow

| Step | Description | Notebook Section |
|---|---|---|
| 1️⃣ | Load raw Superstore CSV into a Spark DataFrame | `Step 1 - Load Dataset` |
| 2️⃣ | Clean data — check nulls, remove duplicates | `Step 2 - Data Cleaning` |
| 3️⃣ | Save cleaned data as a Delta table | `Step 3 - Save Delta Table` |
| 4️⃣ | Read back Delta table to confirm persistence | `Step 4 - Read Delta Table` |
| 5️⃣ | Create incremental dataset (updated + new rows) | `Step 5 - Create Incremental Data` |
| 6️⃣ | Apply `MERGE INTO` — update matches, insert new | `Step 6 - Merge Result` |
| 7️⃣ | Validate row counts & duplicate keys post-merge | `Step 7 - Validation` |

---

## 📊 Key Metrics

| Metric | Value |
|---|---|
| Original dataset rows | **9,994** |
| Null values found | **0** across all columns |
| Duplicate rows removed | **0** (data was already clean) |
| Incremental batch size | **10** rows (5 updated + 5 new) |
| Rows after `MERGE` | **9,999** |
| Duplicate keys after merge | **0** ✅ |

---
## 💡 What I Learned

- **MERGE vs separate UPDATE/INSERT**: Before this, I would have written two separate operations to update existing rows and insert new ones. `MERGE INTO` does both atomically in one pass — matched rows update, unmatched rows insert, and it's a single transaction so there's no risk of partial writes.

- **Delta tables ≠ just Parquet with a name**: Reading the same table twice (`Step 3` → `Step 4`) proved the write was durable and schema-consistent — this is the ACID guarantee in practice, not just theory.

- **Real data is rarely "dirty" in the way tutorials show**: My null/duplicate check came back clean (0 and 0). Instead of faking a "cleaning success," I learned to trust and report the actual result — an honest validation step, even a boring one, is still a valid engineering step.

- **Simulating incremental data is a skill on its own**: Real CDC (Change Data Capture) pipelines get incremental batches from source systems. I had to think about *what a realistic batch looks like* — a few updated rows (price change, quantity change) plus a few brand-new rows — instead of just duplicating random data.

- **Validation isn't optional — it's proof**: Checking for duplicate keys after merge and confirming the exact row count (9994 + 5 new = 9999) is what makes the pipeline trustworthy. Without that step, I'd just be assuming the merge worked.

- **Row-level grain > forced aggregation**: I initially aggregated data to one row per customer, but realized the assignment only asked to process the dataset — not redesign its grain. Working at the natural row level kept the logic simpler and closer to what a real MERGE use case looks like.

---
## 🧠 What This Demonstrates

- **ACID-compliant writes** using Delta Lake on top of Parquet
- **Schema enforcement** when reading/writing Delta tables
- **`MERGE INTO`** for combining update + insert logic in a single atomic operation
- **Incremental data simulation** — a realistic pattern for CDC (Change Data Capture) pipelines
- **Post-merge validation** to guarantee data integrity (no duplicate keys, expected row counts)

---

## ▶️ How to Run

1. Upload `Sample - Superstore.csv` to a Unity Catalog Volume in Azure Databricks.
2. Open `notebook/delta_scd_assignment.ipynb` in your Databricks workspace.
3. Update the file path in the first cell to match your Volume location.
4. Run all cells top to bottom (**Run All**).
5. Exported CSVs (`customer_master.csv`, `customer_incremental.csv`) will be generated in the `Datasets/` folder.

---

## 👤 Author

**Nidhi Bansal**
Week 07 Assignment — Delta Lake MERGE Implementation

---

⭐ *This project is part of a structured Data Engineering learning path covering Delta Lake fundamentals, incremental processing, and Lakehouse architecture.*
