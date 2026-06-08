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
Celebal Technologies — Data Engineering Intern

⭐ *Star this repo if you found it helpful!*

