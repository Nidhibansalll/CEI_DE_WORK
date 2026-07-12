# 🚀 Celebal Technologies — Data Engineering Internship

![Intern](https://img.shields.io/badge/Role-Data%20Engineering%20Intern-blue)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Tools](https://img.shields.io/badge/Tools-Python%20%7C%20MySQL%20%7C%20SQL-orange)

> A repository documenting my weekly assignments, projects, and learnings  
> during my **Data Engineering Internship at Celebal Technologies**.  
> Each week covers a new concept — from data cleaning to advanced SQL analytics.

---

## 👩‍💻 About Me

**Nidhi Bansal**  
Data Engineering Intern — Celebal Technologies  
📍 Jaipur, Rajasthan, India  
🛠️ Python | SQL | MySQL | Pandas | Jupyter Notebook| ADF

---
```text
CEI_DE_WORK/
│
├── Week-01/
│   ├── CELEBAL_WEEK-1.ipynb
│   ├── Combined_dataset.csv
│   ├── Combined_dataset_CLEANED.csv
│   └── README.md
│
├── Week-02-SQL-Sales-Analysis/
│   ├── CELEBAL_WEEK-2.sql
│   ├── Q23.png
│   ├── Q5.png
│   ├── Q6.png
│   └── README.md
│
├── Week-03-Advance-SQL-Superstore/
│   ├── CELEBAL_WEEK-3.sql
│   └── README.md
│
├── Week-04-DE-Concepts/
│   ├── dataset/
│   │   └── Sample - Superstore.csv
│   │
│   ├── screenshots/
│   │   ├── 1-Resource Group.png
│   │   ├── 2-Storage Setup.png
│   │   ├── 2-csv uploaded.png
│   │   ├── 3-linked.png
│   │   ├── 3-source.png
│   │   ├── 3-destination.png
│   │   ├── 3-metadata.png
│   │   ├── 4-pipeline design.png
│   │   ├── 5-pipeline execution.png
│   │   ├── 6-Roles.png
│   │   ├── output.png
│   │   └── README.md
│
├── Week-05-Spark-Assignment/
│   ├── data/
│   │   └── dataset.csv
│   ├── notebook/
│   │   └── spark_basics.ipynb
│   ├── output/
│   │   └── results.csv
│   └── README.md
│
├── Week-06-Apache-Spark/
│   ├── Data/
│   │   └── source.csv
│   ├── Week_06_Apache_Spark.ipynb
│   └── README.md
│
├── Week-07-delta-lake-assignment/
│   ├── Datasets/
│   │   ├── Sample - Superstore.csv
│   │   ├── customer_master.csv
│   │   └── customer_incremental.csv
│   │
│   ├── notebook/
│   │   └── delta_scd_assignment.ipynb
│   │
│   ├── screenshots/
│   │   ├── 01_Load_Dataset.png
│   │   ├── 02_Data_Cleaning.png
│   │   ├── 03_Save_Delta_Table.png
│   │   ├── 04_Read_Delta_Table.png
│   │   ├── 05_Create_Incremental_Data.png
│   │   ├── 06_Merge_Result.png
│   │   ├── 07_Validation.png
│   │   └── Final_Output.png
│   │
│   └── README.md
│
├── Week-08-ecommerce-order-analytics-system/
│   ├── data/
│   │   ├── raw/
│   │   │   ├── customers.csv
│   │   │   ├── products.csv
│   │   │   ├── orders.csv
│   │   │   └── order_items.csv
│   │   └── cleaned/
│   │       ├── customers_clean.csv
│   │       ├── products_clean.csv
│   │       ├── orders_clean.csv
│   │       └── order_items_clean.csv
│   ├── scripts/
│   │   ├── generate_data.py
│   │   ├── clean_data.py
│   │   ├── load_db.py
│   │   ├── report_cli.py
│   │   └── test_edge_cases.py
│   ├── sql/
│   │   ├── schema.sql
│   │   ├── aggregations.sql
│   │   ├── window_functions.sql
│   │   └── cohort_analysis.sql
│   ├── output/
│   │   ├── data_quality_report.txt
│   │   └── sample_reports/
│   ├── ecommerce.db
│   └── README.md
│
└── README.md
```
## 📅 Weekly Progress

| Week | Topic | Concepts Covered | Tools |  |
|---|---|---|---|---|
| Week 01 | Python Data Cleaning | Pandas, Missing Values, Data Types, EDA | Python, Jupyter |  |
| Week 02 | SQL Sales Analysis | SELECT, JOINs, Aggregation, Transactions, ACID | MySQL Workbench |  |
| Week 03 | Advanced SQL — Superstore | Subqueries, CTEs, Window Functions, RANK | MySQL Workbench |  |
| Week 04 | Azure Cloud & ADF Pipeline | Blob Storage, ADF, Linked Services, IAM, ETL Pipeline| Microsoft Azure |  |
| Week 05 | Spark-assignment | Apache Spark — DataFrame cleaning, transformation & aggregation| Python, Jupyter,Spark  |  |
| Week 06 | Apache Spark — Architecture & Pipelines | Spark Architecture, Lazy Evaluation, Lineage Graph, CSV vs Parquet, Predicate Pushdown, Read→Transform→Filter→Write Pipeline | Python, Jupyter, PySpark |  |
| Week 07 | Delta Lake (SCD Type-1) | Delta Tables, ACID Transactions, MERGE INTO, Incremental Loading, SCD Type-1 | Apache Spark, Delta Lake, Databricks |
| Week 08 | E-Commerce Order Analytics System | Data Generation, Data Cleaning, Referential Integrity, SQLite, Window Functions, CTEs, Cohort Analysis, CLI Tooling | Python, Pandas, SQLite |  |
---

## 🔑 Key Highlights

### 📌 Week 01 — Pandas Data Cleaning
- Cleaned a **1000-row Indian E-Commerce dataset** with 24 columns
- Handled missing values, removed ₹ symbols, filtered by rating ≥ 4.0
- Created derived column `total_amount = final_price × ratings_count`
- Exported clean data as `Combined_dataset_CLEANED.csv`

### 📌 Week 02 — SQL Sales Analysis (ShopEase DB)
- Built a relational database from scratch with **4 tables, 27 queries**
- Covered SQL Basics → Filtering → Aggregation → Joins → Transactions
- Demonstrated ACID properties with real BEGIN/COMMIT/ROLLBACK transactions
- Used CASE statements, HAVING, indexes, and SARGable query rewrites

### 📌 Week 03 — Advanced SQL (Superstore)
- Analyzed **9,994 rows** of Superstore sales data
- Applied correlated subqueries, CTEs, and 3 types of window functions
- Identified top customer **Sean Miller (₹25,043)** and churn risks (12 single-order customers)
- Built a final combined query using **JOIN + CTE + DENSE_RANK()** together


### 📌 Week 04 — Azure Cloud & ADF Pipeline
- Provisioned end-to-end Azure infrastructure: Resource Group → Storage Account → Blob Containers
- Uploaded Sample Superstore CSV as source data in Blob Storage
- Built ADF pipeline pl_CopySuperstoreData with Get Metadata + Copy Data activities
- Validated file metadata (itemName, size, columnCount) before triggering data copy
- Successfully copied data to destination container — output_superstore.csv 
- Implemented RBAC with Reader, Contributor, and Storage Blob Data Contributor roles

 ### 📌 Week 5 Spark Assignment 
 
- Set up an Apache Spark (PySpark) environment and loaded a 1000-row e-commerce dataset into Spark DataFrames.
- Cleaned real-world messy data by removing duplicates, handling null values, filling missing fields, and filtering invalid records.
- Applied DataFrame transformations such as filtering, renaming columns, type casting, and selecting relevant data.
- Performed aggregations using count(), sum(), avg(), min(), and max(), along with groupBy() operations.
- Built a complete Spark pipeline combining data cleaning, transformation, and revenue aggregation by store.

  ### 📌 Week 06 — Apache Spark (Architecture & Pipelines)
- Studied Spark's core architecture — roles of the **Driver**, **Cluster Manager**, and **Executors** — and the difference between **Client Mode** and **Cluster Mode**
- Explained **Lazy Evaluation** and how Spark builds an optimized execution plan (DAG) before running any job
- Understood how Spark uses the **Lineage Graph** for fault tolerance — recomputing only lost partitions instead of restarting the whole job on node failure
- Compared **CSV vs Parquet** storage (row-based vs columnar) and explained **Predicate Pushdown** in Parquet for reduced memory usage
- Tested all DataFrame operations on a custom **1000-row dataset** — filtering, renaming columns, type casting, multi-condition filters (AND/OR), and derived columns
- Built a complete **read → transform → filter → write pipeline**: loaded Parquet, removed null `user_id` rows, and saved clean output as CSV
- Practiced best practices for large datasets — avoided `.collect()`, used `.show(5)` for safe data exploration


### 📌 Week 07 — Delta Lake (SCD Type-1)

- Built an end-to-end **Delta Lake pipeline** using Apache Spark and Delta Lake.
- Loaded the customer master dataset and stored it as a **Delta Table**.
- Performed data validation by checking for null values and duplicate records before processing.
- Created an incremental (CDC-style) dataset containing both updated existing customers and new customer records.
- Applied **MERGE INTO** to implement **Slowly Changing Dimension (SCD Type-1)** by updating existing rows and inserting new ones atomically.
- Validated the final Delta table by verifying row counts, updates, inserts, and duplicate-free primary keys.
- Demonstrated Delta Lake features including **ACID Transactions**, **Schema Enforcement**, and efficient incremental data processing.

### 📌 Week 08 — E-Commerce Order Analytics System

- Built an end-to-end **order analytics pipeline** — data generation → cleaning → SQLite warehouse → SQL analysis → CLI reporting
- Generated **4 realistic datasets (2,900+ rows total)** with intentional data-quality issues: missing customer IDs, inconsistent date formats, invalid emails, negative quantities, orphan records, and duplicate rows
- Wrote cleaning functions (`clean_orders()`, `clean_products()`, `validate_emails()`, `check_referential_integrity()`) that fix what can be fixed and flag what can't be silently fixed
- Designed the data generator so referential integrity holds **by construction** — order_items always reference a real order, except for a small number of rows deliberately broken to test the integrity-check logic
- Wrote **16 SQL queries** across basic aggregations, intermediate business logic, and advanced analytics — including running totals, `DENSE_RANK`, `LAG`/`LEAD`, `NTILE` quartiles, year-over-year growth, and full cohort retention analysis
- Debugged a real SQLite quirk: `FIRST_VALUE`/`LAST_VALUE` need an explicit window frame (`ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`) or they silently return the wrong row
- Built a **command-line reporting tool** (using only `sqlite3`, no ORM) that generates daily/weekly/monthly business summaries with period-over-period % change
- Wrote automated edge-case tests as plain Python functions, verifying behavior for orphan foreign keys, invalid discounts, zero quantities, and future-dated orders
---
## 📊 Skills Gained So Far

| Category | Skills |
|---|---|
| 🐍 Python | Pandas, Data Cleaning, EDA, Data Transformation |
| 🗄️ SQL — DDL | CREATE, DROP, ALTER, Constraints |
| 📝 SQL — DML | INSERT, UPDATE, DELETE |
| 🔍 SQL — Queries | SELECT, JOINs, Subqueries, CTEs, HAVING |
| 🪟 Window Functions | RANK(), DENSE_RANK(), ROW_NUMBER(), PARTITION BY |
| 🔐 Transactions | ACID Properties, BEGIN, COMMIT, ROLLBACK |
|☁️ Azure Cloud | Resource Groups, Blob Storage, Storage Accounts, IAM |
|🔄ADF (ETL)| Linked Services, Datasets, Pipelines, Get Metadata, Copy Data|
|🔑 Security| RBAC, Managed Identity, Role Assignments, PoLP|
|⚡ Apache Spark (PySpark)|	SparkSession, DataFrames, Distributed Processing, In-Memory Computing|
|🧹 Data Processing|	Data Cleaning, Deduplication, Null Handling, Data Validation|
|🔄 Data Transformation|	Filtering, Column Renaming, Type Casting, DataFrame Transformations|
|📊 Data Analysis|	Aggregations (SUM, AVG, MIN, MAX, COUNT), GroupBy Operations|
|⚙️ Big Data Concepts|	MapReduce vs Spark, Narrow & Wide Transformations, Shuffle Operations|
|🚀 ETL Pipelines	|End-to-End Data Cleaning, Transformation, Aggregation Workflows|
|🏗️ Spark Architecture| Driver, Cluster Manager, Executors, Client vs Cluster Mode, Lineage Graph (DAG)|
|📦 File Formats| CSV vs Parquet, Columnar Storage, Predicate Pushdown|
| 🏞️ Delta Lake | Delta Tables, ACID Transactions, MERGE INTO, Schema Enforcement |
| 🔄 Incremental Processing | CDC, Upserts, SCD Type-1, Delta Merge Operations |
| 🗃️ Data Warehousing | SQLite Schema Design, Primary/Foreign Keys, CHECK Constraints, Indexing |
| 🧼 Data Quality Engineering | Referential Integrity Checks, Deduplication, Data Validation Reports |
| 🪟 Advanced SQL | NTILE, FIRST_VALUE/LAST_VALUE, Multi-level CTEs, Cohort Retention Analysis |
| 🖥️ CLI Tooling | argparse, Interactive Prompts, Period-over-Period Comparison Logic |
---

## 🧠 Learnings & Reflections

- Learned why **correlated subqueries are slow** and how CTEs are a cleaner alternative
- Understood the real difference between **RANK() vs DENSE_RANK()** through hands-on queries
- Realized how **window functions preserve row-level detail** while still doing aggregations
- Appreciated how **good database design** (normalized tables) makes queries faster and cleaner
- Grew comfortable reading and writing **production-style SQL** with proper comments
- Understood how Azure Resource Groups act as logical boundaries for cost and access management
- Learned how ADF Linked Services decouple connection logic from pipeline logic
- Experienced how metadata-driven pipelines make ETL workflows dynamic and fault-tolerant
- Applied Principle of Least Privilege using Azure IAM role assignments in a real cloud environment
- Developed a strong understanding of Apache Spark's DataFrame operations, including data cleaning, transformation, aggregation, and building efficient data-processing pipelines on large datasets.
- This assignment provided practical experience in handling real-world messy data and demonstrated how proper data cleaning and transformation are essential for producing accurate and meaningful analytical results.
- Understood why **lazy evaluation** matters — Spark optimizes the entire chain of transformations before execution instead of running each step blindly
- Realized that Spark's fault tolerance comes from its **lineage graph**, not data replication — failed partitions are simply recomputed from their transformation history
- Learned practically why **Parquet outperforms CSV** for analytics — columnar storage means only required columns get read off disk
- Understood **predicate pushdown** — filtering at the storage layer itself reduces the amount of data pulled into memory
- Built the habit of using `.show()` instead of `.collect()` — a small change in approach that matters a lot once datasets scale to production size
- Learned the real difference between running separate UPDATE/INSERT operations vs. Delta Lake's MERGE INTO, which does both atomically in a single transaction — no risk of partial writes.
- Understood that a Delta table is not just Parquet with a different name — re-reading the table after write proved the ACID durability guarantee in practice, not just in theory.
- Realized that clean data isn't a failure of the exercise — reporting an honest "0 nulls, 0 duplicates" result is still a valid, necessary validation step.
- Practiced designing a realistic incremental (CDC-style) batch — a mix of updated existing rows and genuinely new rows, rather than arbitrary random data.
- Learned that validation is what makes a pipeline trustworthy — checking exact row counts and duplicate keys after merge is what proves the operation worked, not just an assumption.
- Understood why working at the natural row-level grain of a dataset (rather than forcing an aggregation the task didn't ask for) keeps a MERGE pipeline simpler and closer to real-world usage.
- Realized that "cleaning" data isn't the same as "deleting anything unusual" — some messy-looking data (like negative quantities for returns, or future order dates for scheduled orders) is actually meaningful business information that should be flagged, not removed.

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat&logo=mysql&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=flat&logo=jupyter&logoColor=white)
![Microsoft Azure](https://img.shields.io/badge/Microsoft_Azure-0078D4?style=flat&logo=microsoft-azure&logoColor=white)
![Azure Data Factory](https://img.shields.io/badge/Azure_Data_Factory-0078D4?style=flat&logo=microsoft-azure&logoColor=white)
![Apache Spark](https://img.shields.io/badge/Apache_Spark-E25A1C?style=flat&logo=apachespark&logoColor=white)
![Azure Databricks](https://img.shields.io/badge/Azure_Databricks-FF3621?style=flat&logo=databricks&logoColor=white).

---

## 📬 Connect With Me
Feel free to connect if you're also on this journey or want to discuss data engineering!

⭐ **Star this repo** if you find it helpful — it motivates me to keep going!




