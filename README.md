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
🛠️ Python | SQL | MySQL | Pandas | Jupyter Notebook

---

## 📁 Repository Structure
CELEBAL_ASSIGNMENTS/
│
├── Week-01-Pandas-Data-Cleaning/
│   ├── CELEBAL_WEEK-1.ipynb        # Jupyter notebook 
│   ├── Combined_dataset.csv        # Original raw dataset
│   ├── Combined_dataset_CLEANED.csv # Cleaned output
│   └── readme.md
│
├── Week-02-SQL-Sales-Analysis/
│   ├── CELEBAL_WEEK-2.sql          # Full SQL script 
│   ├── Q23.png                     # Query result screenshot
│   ├── Q5.png                      # Query result screenshot
│   ├── Q6.png                      # Query result screenshot
│   └── readme.md
│
├── Week-03-Advance-SQL-Superstore/
│   ├── CELEBAL_WEEK-3.sql          # Advanced SQL — CTEs, Subqueries, Window Functions
│   └── readme.md
│
└── README.md                      
---

## 📅 Weekly Progress

| Week | Topic | Concepts Covered | Tools | Status |
|---|---|---|---|---|
| Week 01 | Python Data Cleaning | Pandas, Missing Values, Data Types, EDA | Python, Jupyter | ✅ Done |
| Week 02 | SQL Sales Analysis | SELECT, JOINs, Aggregation, Transactions, ACID | MySQL Workbench | ✅ Done |
| Week 03 | Advanced SQL — Superstore | Subqueries, CTEs, Window Functions, RANK | MySQL Workbench | ✅ Done |

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

---

## 📊 Skills Gained So Far
Data Engineering Stack
├── Python
│   └── Pandas — data cleaning, transformation, EDA
├── SQL
│   ├── DDL — CREATE, DROP, ALTER
│   ├── DML — INSERT, UPDATE, DELETE
│   ├── Queries — JOINs, Subqueries, CTEs
│   ├── Window Functions — RANK, DENSE_RANK, ROW_NUMBER
│   └── Transactions — ACID, BEGIN, COMMIT, ROLLBACK
└── Tools
├── MySQL Workbench 8.0
└── Jupyter Notebook

---

## 🧠 Learnings & Reflections

- Learned why **correlated subqueries are slow** and how CTEs are a cleaner alternative
- Understood the real difference between **RANK() vs DENSE_RANK()** through hands-on queries
- Realized how **window functions preserve row-level detail** while still doing aggregations
- Appreciated how **good database design** (normalized tables) makes queries faster and cleaner
- Grew comfortable reading and writing **production-style SQL** with proper comments

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat&logo=mysql&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=flat&logo=jupyter&logoColor=white)

---

## 📬 Connect With Me

Feel free to connect if you're also on this journey or want to discuss data engineering!

⭐ **Star this repo** if you find it helpful — it motivates me to keep going!



























CELEBAL TECHNOLOGIES-- DATA ENGINEERING INTERNSHIP
> Tools used: Python (Pandas), MySQL Workbench, Jupyter Notebook.
## 📅 Week 1 — Python Data Cleaning (Pandas)

### 🎯 Objective
Clean and prepare a raw E-Commerce dataset for analysis using Python and Pandas.

### 📦 Dataset
| Property | Value |
|---|---|
| Dataset | Indian E-Commerce Products |
| Original Size | 1000 rows × 24 columns |
| Cleaned File | `Combined_dataset_CLEANED.csv` |

### ✅ What Was Done

| Step | Task | Details |
|---|---|---|
| 1 | Loaded Data | Loaded CSV into Pandas DataFrame |
| 2 | Explored Data | Checked shape, columns, dtypes, head/tail |
| 3 | Missing Values | Filled `discount` → `0`, `seller_name` → `Unknown` |
| 4 | Cleaned Price | Removed ₹ symbol, converted `final_price` to float |
| 5 | Filtered Rows | Kept only products with `rating >= 4.0` |
| 6 | Selected Columns | Kept only useful columns for analysis |
| 7 | Removed Duplicates | Checked and removed duplicate rows |
| 8 | Derived Column | Created `total_amount = final_price × ratings_count` |
| 9 | Saved Output | Exported as `Combined_dataset_CLEANED.csv` |

### 📊 Key Stats

| Metric | Value |
|---|---|
| Total Products | 1000 |
| Unique Categories | 97 |
| Average Final Price | ₹1,706 |
| Duplicates Found | 0 |

### 🛠️ Tools Used
- Python 3.x
- Pandas
- Jupyter Notebook

---
## 📅 Week 2 — SQL Data Analysis (MySQL)

### 🎯 Objective
Analyze sales data using SQL with filtering, aggregation, joins, and transactions on a relational e-commerce database (ShopEase).

### 🗄️ Database Schema

```
customers ──(1:N)──► orders ──(1:N)──► order_items ◄──(N:1)── products
```

| Table | Primary Key | Rows |
|---|---|---|
| customers | customer_id | 8 |
| products | product_id | 8 |
| orders | order_id | 10 |
| order_items | item_id | 15 |

### ✅ Sections Covered

#### Section A — SQL Basics
| Q | Topic | Concept |
|---|---|---|
| Q1 | SELECT * | Retrieve all data |
| Q2 | SELECT specific columns | Column selection |
| Q3 | DISTINCT | Unique values |
| Q4 | Primary Keys | Uniqueness + NOT NULL |
| Q5 | UNIQUE constraint | Duplicate email prevention |
| Q6 | CHECK constraint | Negative price prevention |

#### Section B — Filtering & Optimization
| Q | Topic | Concept |
|---|---|---|
| Q7 | WHERE | Filter by status |
| Q8 | WHERE + AND | Multi-condition filter |
| Q9 | WHERE + BETWEEN | Date range filter |
| Q10 | WHERE + NOT | Exclude cancelled orders |
| Q11 | Index explanation | idx_orders_date performance |
| Q12 | SARGable queries | Index-friendly rewrites |

#### Section C — Aggregation
| Q | Topic | Concept |
|---|---|---|
| Q13 | COUNT | Total orders |
| Q14 | SUM + WHERE | Revenue from delivered orders |
| Q15 | AVG + GROUP BY | Average price per category |
| Q16 | GROUP BY + ORDER BY | Revenue by status |
| Q17 | MAX + MIN | Price range per category |
| Q18 | HAVING | Filter aggregated results |

#### Section D — Joins
| Q | Topic | Concept |
|---|---|---|
| Q19 | INNER JOIN | Orders with customer names |
| Q20 | LEFT JOIN | All customers including no-orders |
| Q21 | 3-Table JOIN | Orders + Items + Products |
| Q22 | LEFT vs RIGHT JOIN | Explanation + FULL OUTER |
| Q23 | Foreign Keys | FK violation demonstration |

#### Section E — Advanced Concepts
| Q | Topic | Concept |
|---|---|---|
| Q24 | CASE | Price tier classification |
| Q25 | CASE + SUM | Delivered vs Not Delivered |
| Q26 | ACID | Atomicity, Consistency, Isolation, Durability |
| Q27 | Transaction | BEGIN → COMMIT / ROLLBACK |

### 📊 Sample Query Results

```sql
-- Revenue by Category
Electronics  →  ₹2,224 avg price
Clothing     →  ₹2,699 avg price  
Home         →  ₹949   avg price

-- Order Status Breakdown
Delivered  →  6 orders  →  ₹17,191 revenue
Shipped    →  2 orders  →  ₹13,596 revenue
Cancelled  →  1 order   →  ₹2,999  revenue
Pending    →  1 order   →  ₹1,299  revenue
```

### 🛠️ Tools Used
- MySQL Workbench 8.x
- Sample Superstore Dataset (9,694 rows)
- ShopEase Database (custom schema)
---

### Author
NIDHI BANSAL

⭐ *Star this repo if you found it helpful!*


