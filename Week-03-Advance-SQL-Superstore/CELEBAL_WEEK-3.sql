CREATE DATABASE superstore_db;
USE superstore_db;

-- STEP 1: SETUP DATA
CREATE TABLE superstore_raw (
    row_id        INT,
    order_id      VARCHAR(50),
    order_date    VARCHAR(20),
    ship_date     VARCHAR(20),
    ship_mode     VARCHAR(50),
    customer_id   VARCHAR(50),
    customer_name VARCHAR(100),
    segment       VARCHAR(50),
    country       VARCHAR(100),
    city          VARCHAR(100),
    state         VARCHAR(100),
    postal_code   VARCHAR(20),
    region        VARCHAR(50),
    product_id    VARCHAR(50),
    category      VARCHAR(50),
    sub_category  VARCHAR(50),
    product_name  VARCHAR(255),
    sales         DOUBLE,
    quantity      INT,
    discount      DOUBLE,
    profit        DOUBLE
);
SELECT * FROM superstore_raw;

-- Create customers table
CREATE TABLE customers AS
SELECT DISTINCT
    customer_id,
    customer_name,
    segment,
    country,
    city,
    state,
    postal_code,
    region
FROM superstore_raw;
SELECT * FROM customers;

-- Create orders table
CREATE TABLE orders AS
SELECT DISTINCT
    order_id,
    order_date,
    ship_date,
    ship_mode,
    customer_id,
    sales,
    quantity,
    discount,
    profit
FROM superstore_raw;
SELECT * FROM orders;

-- Create products table
CREATE TABLE products AS
SELECT DISTINCT
    product_id,
    category,
    sub_category,
    product_name
FROM superstore_raw;
SELECT * FROM products;

-- STEP 2:  QUERIES

-- 1. Find all orders where sales are greater than average sales (Subquery)
SELECT *
FROM orders
WHERE sales > (
    SELECT AVG(sales) FROM orders
);

-- 2. Find the highest sales order for each customer (Subquery)
SELECT *
FROM superstore_raw AS s
WHERE sales = (
    SELECT MAX(sales)
    FROM superstore_raw AS c
    WHERE c.customer_id = s.customer_id
);

-- 3. Calculate total sales for each customer (CTE)
WITH customer_sales AS (
    SELECT
        customer_id,
        customer_name,
        SUM(sales) AS total_sales
    FROM superstore_raw
    GROUP BY customer_id, customer_name
)
SELECT * 
FROM customer_sales;

-- 4. Find customers whose total sales are above average (CTE + Subquery)
WITH customer_sales AS (
    SELECT
        customer_id,
        customer_name,
        SUM(sales) AS total_sales
    FROM superstore_raw
    GROUP BY customer_id, customer_name
)
SELECT *
FROM customer_sales
WHERE total_sales > (
    SELECT AVG(total_sales) FROM customer_sales
);

-- 5. Rank all customers based on total sales (Window Function)
SELECT
    customer_id,
    customer_name,
    SUM(sales) AS total_sales,
    RANK() OVER (ORDER BY SUM(sales) DESC) AS sales_rank
FROM superstore_raw
GROUP BY customer_id, customer_name;

-- 6. Assign row numbers to each order within a customer (Window Function + PARTITION BY)
SELECT
    customer_id,
    customer_name,
    order_id,
    sales,
    ROW_NUMBER() OVER (
        PARTITION BY customer_id
        ORDER BY sales DESC
    ) AS row_num
FROM superstore_raw;

-- 7. Display top 3 customers based on total sales (Window Function)
WITH customer_ranking AS (
    SELECT
        customer_id,
        customer_name,
        SUM(sales) AS total_sales,
        RANK() OVER (ORDER BY SUM(sales) DESC) AS rank_number
    FROM superstore_raw
    GROUP BY customer_id, customer_name
)
SELECT *
FROM customer_ranking
WHERE rank_number <= 3;

-- Result
-- customer_id customer_name total_sales rank_number
-- SM-20320	Sean Miller	25043.05	1
-- TC-20980	Tamara Chand	19017.847999999998	2
-- RB-19360	Raymond Buch	15117.339	3

-- STEP 3: FINAL COMBINED QUERY
-- Customer Name | Total Sales | Rank
-- JOIN + CTE + Window Function

WITH customer_sales AS (
    SELECT
        customer_id,
        SUM(sales) AS total_sales
    FROM superstore_raw
    GROUP BY customer_id
),
customer_master AS (
    SELECT DISTINCT
        customer_id,
        customer_name
    FROM superstore_raw
)
SELECT
    cm.customer_name,
    cs.total_sales,
    DENSE_RANK() OVER (ORDER BY cs.total_sales DESC) AS customer_rank
FROM customer_sales cs
JOIN customer_master cm ON cs.customer_id = cm.customer_id
ORDER BY customer_rank;


-- MINI PROJECT: CUSTOMER SALES INSIGHTS

-- 1.Who are the top 5 customers?
SELECT
    customer_name,
    SUM(sales) AS total_sales
FROM superstore_raw
GROUP BY customer_name
ORDER BY total_sales DESC
LIMIT 5;

-- Results:
-- Sean Miller      - 25043.05
-- Tamara Chand     - 19017.847999999998
-- Raymond Buch     - 15117.339
-- Tom Ashbrook     - 14595.62
-- Adrian Barton    - 14355.610999999997


-- 2. Who are the bottom 5 customers?  
SELECT
    customer_name,
    SUM(sales) AS total_sales
FROM superstore_raw
GROUP BY customer_name
ORDER BY total_sales ASC
LIMIT 5;

/*
Results:
Thais Sissman    - 4.833
Lela Donovan     - 5.304
Mitch Gastineau  - 12.32
Carl Jackson     - 16.52
Roy Skaria       - 22.328
*/

-- 3. Which customers made only one order?  
SELECT
    customer_name,
    COUNT(DISTINCT order_id) AS total_orders
FROM superstore_raw
GROUP BY customer_name
HAVING COUNT(DISTINCT order_id) = 1;

/*
Results include:
customer_name      total_orders
Anemone Ratner       1
Anthony O'Donnell    1
Carl Jackson         1
Jenna Caffey         1
Jocasta Rupert       1 
Lela Donovan         1
Mitch Gastineau      1 
Patricia Hirasaki    1
Ricardo Emerson      1
Roland Murray        1
Susan MacKendrick    1
Theresa Coyne        1
*/

-- 4. Which customers have above-average sales?  
WITH customer_sales AS (
    SELECT
        customer_name,
        SUM(sales) AS total_sales
    FROM superstore_raw
    GROUP BY customer_name
)
SELECT *
FROM customer_sales
WHERE total_sales > (
    SELECT AVG(total_sales) FROM customer_sales
);
-- Result
-- 299 customers have sales above average

-- 5. What is the highest order value per customer? 
SELECT
    customer_name,
    MAX(sales) AS highest_order_value
FROM superstore_raw
GROUP BY customer_name
ORDER BY highest_order_value DESC;

/*
Result : 793 rows returned (one per customer), ordered by highest order value.
Top 5 highest single order values:
customer_name highest_order_value
Sean Miller	    22638.48
Tamara Chand	17499.95
Raymond Buch	13999.96
Tom Ashbrook	11199.968
Hunter Lopez	10499.97

*/
