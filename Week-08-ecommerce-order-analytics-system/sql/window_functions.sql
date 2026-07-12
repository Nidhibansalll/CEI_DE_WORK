-- Queries 7, 8, 9, and 16 from the brief (Advanced: Window Functions)

-- Q7. Running total of revenue per region, ordered by date
WITH daily_region_revenue AS (
    SELECT
        o.region_code,
        DATE(o.order_date) AS order_day,
        SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)) AS daily_revenue
    FROM order_items oi
    JOIN orders o ON o.order_id = oi.order_id
    WHERE oi.quantity > 0
    GROUP BY o.region_code, DATE(o.order_date)
)
SELECT
    region_code,
    order_day AS order_date,
    ROUND(daily_revenue, 2) AS daily_revenue,
    ROUND(SUM(daily_revenue) OVER (
        PARTITION BY region_code
        ORDER BY order_day
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ), 2) AS running_total
FROM daily_region_revenue
ORDER BY region_code, order_day;

-- Q8. Rank products by total revenue within each category 
WITH product_revenue AS (
    SELECT
        p.category,
        p.product_name,
        SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)) AS total_revenue
    FROM order_items oi
    JOIN products p ON p.product_id = oi.product_id
    WHERE oi.quantity > 0
    GROUP BY p.category, p.product_name
)
SELECT
    category,
    product_name,
    ROUND(total_revenue, 2) AS total_revenue,
    DENSE_RANK() OVER (PARTITION BY category ORDER BY total_revenue DESC) AS rank_in_category
FROM product_revenue
ORDER BY category, rank_in_category;

-- Q9. Days between consecutive orders per customer (LAG), flag "At Risk" if their average gap is > 30 days.
WITH customer_orders AS (
    SELECT
        customer_id,
        order_date,
        LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date) AS previous_order_date
    FROM orders
    WHERE customer_id IS NOT NULL
),
with_gap AS (
    SELECT
        customer_id,
        order_date,
        previous_order_date,
        CASE
            WHEN previous_order_date IS NOT NULL
            THEN CAST(julianday(order_date) - julianday(previous_order_date) AS INTEGER)
            ELSE NULL
        END AS days_gap
    FROM customer_orders
),
avg_gap AS (
    SELECT customer_id, AVG(days_gap) AS avg_days_gap
    FROM with_gap
    WHERE days_gap IS NOT NULL
    GROUP BY customer_id
)
SELECT
    w.customer_id,
    w.order_date,
    w.previous_order_date,
    w.days_gap,
    CASE WHEN a.avg_days_gap > 30 THEN 'At Risk' ELSE 'Active' END AS risk_flag
FROM with_gap w
JOIN avg_gap a ON a.customer_id = w.customer_id
ORDER BY w.customer_id, w.order_date;

-- Q16. Self-join: products frequently bought together
-- I self-join order_items to itself on order_id, forcing product_a.id < product_b.id so each pair only shows up once (A-B, never also B-A), and product_a <> product_b so a 
 -- product is never paired with itself.
SELECT
    pa.product_name AS product_a,
    pb.product_name AS product_b,
    COUNT(*) AS times_bought_together
FROM order_items oi1
JOIN order_items oi2
    ON oi1.order_id = oi2.order_id
    AND oi1.product_id < oi2.product_id   -- avoids self-pairs and duplicate A-B/B-A rows
JOIN products pa ON pa.product_id = oi1.product_id
JOIN products pb ON pb.product_id = oi2.product_id
WHERE oi1.quantity > 0 AND oi2.quantity > 0
GROUP BY pa.product_name, pb.product_name
HAVING times_bought_together > 1
ORDER BY times_bought_together DESC
LIMIT 20;
