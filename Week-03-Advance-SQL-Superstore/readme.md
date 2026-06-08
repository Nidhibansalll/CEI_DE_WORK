# 📅 Week 03 — Advanced SQL: Superstore Sales Analysis

> *"Good data analysis isn't just about writing queries — it's about asking the right questions."*

## 🎯 Objective
Dive deep into the **Sample Superstore dataset** using advanced SQL techniques —
Subqueries, CTEs, and Window Functions — to uncover real business insights about customers, sales, and order patterns.

---

## 📦 Dataset
| Property | Value |
|---|---|
| 📁 Dataset | Sample Superstore |
| 📊 Size | 9,994 rows × 21 columns |
| 🗓️ Period | 2015 – 2018 |
| 🌍 Region | United States |

---

## 🗄️ Database Architecture

superstore_raw  ──►  customers
──►  orders
──►  products

| Table | Description | Records |
|---|---|---|
| `superstore_raw` | Complete raw imported dataset | 9,994 |
| `customers` | Unique customer profiles | 793 |
| `orders` | Order-level transaction data | ~5,009 |
| `products` | Unique product catalogue | 1,850 |

---

## 🔍 Concepts Applied

### 🔸 Subqueries
| # | Query | What it solves |
|---|---|---|
| 1 | Sales > Average Sales | Find all high-value orders |
| 2 | Highest order per customer | Correlated subquery — best purchase per person |

### 🔸 CTEs (Common Table Expressions)
| # | Query | What it solves |
|---|---|---|
| 3 | Total sales per customer | Clean aggregation using WITH clause |
| 4 | Above-average customers | CTE + Subquery combined |

### 🔸 Window Functions
| # | Query | What it solves |
|---|---|---|
| 5 | RANK() | Rank every customer by revenue |
| 6 | ROW_NUMBER() + PARTITION BY | Number each order within a customer |
| 7 | Top 3 customers | Filter ranked results |

### 🔸 Final Boss Query 🏆
Combined **JOIN + CTE + DENSE_RANK()** in a single query to produce:
> Customer Name → Total Sales → Rank

---

## 📊 Business Insights

### 🏆 Top 5 Customers
| Rank | Customer | Total Sales |
|---|---|---|
| 1 | Sean Miller | ₹25,043.05 |
| 2 | Tamara Chand | ₹19,017.85 |
| 3 | Raymond Buch | ₹15,117.34 |
| 4 | Tom Ashbrook | ₹14,595.62 |
| 5 | Adrian Barton | ₹14,355.61 |

### 📉 Bottom 5 Customers
| Rank | Customer | Total Sales |
|---|---|---|
| 1 | Thais Sissman | ₹4.83 |
| 2 | Lela Donovan | ₹5.30 |
| 3 | Mitch Gastineau | ₹12.32 |
| 4 | Carl Jackson | ₹16.52 |
| 5 | Roy Skaria | ₹22.33 |

### 💡 Key Findings
| Metric | Value | Insight |
|---|---|---|
| 🥇 Highest single order | ₹22,638.48 | Sean Miller — power buyer |
| 📦 Single-order customers | 12 | Potential churn risk |
| 📈 Above-average customers | 299 out of 793 | ~38% drive most revenue |
| 💰 Average customer sales | ~₹2,300 | Skewed by top buyers |

---

## 🧠 What I Learned
- How **correlated subqueries** work row-by-row (and why they're slow!)
- Why **CTEs** make complex queries readable and reusable
- How **window functions** let you rank and segment without losing rows
- The difference between **RANK vs DENSE_RANK** — gaps vs no gaps
- How to combine everything into one powerful final query

---

## 🛠️ Tools Used
- 🐬 MySQL Workbench 8.0
- 📄 Sample Superstore Dataset (Kaggle)

---

## 👩‍💻 Author
**Nidhi Bansal**
Celebal Technologies — Data Engineering Intern

⭐ Star this repo if you found it helpful!
