-- Queries 10-15 from the brief.

-- Q10. Multi-level CTE: monthly revenue per customer -> bucket into High/Medium/Low -> count customers per bucket per month
WITH monthly_customer_revenue AS (
    SELECT
        o.customer_id,
        strftime('%Y-%m', o.order_date) AS order_month,
        SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)) AS monthly_revenue
    FROM order_items oi
    JOIN orders o ON o.order_id = oi.order_id
    WHERE oi.quantity > 0 AND o.customer_id IS NOT NULL
    GROUP BY o.customer_id, order_month
),
categorised AS (
    SELECT
        customer_id,
        order_month,
        monthly_revenue,
        CASE
            WHEN monthly_revenue > 10000 THEN 'High'
            WHEN monthly_revenue >= 5000 THEN 'Medium'
            ELSE 'Low'
        END AS revenue_category
    FROM monthly_customer_revenue
)
SELECT
    order_month,
    revenue_category,
    COUNT(DISTINCT customer_id) AS customer_count
FROM categorised
GROUP BY order_month, revenue_category
ORDER BY order_month, revenue_category;

-- Q11. NTILE(4) - divide customers into quartiles based on lifetime value
WITH customer_lifetime_value AS (
    SELECT
        c.customer_id,
        COALESCE(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)), 0) AS total_value
    FROM customers c
    LEFT JOIN orders o ON o.customer_id = c.customer_id
    LEFT JOIN order_items oi ON oi.order_id = o.order_id AND oi.quantity > 0
    GROUP BY c.customer_id
),
quartiled AS (
    SELECT
        customer_id,
        total_value,
        NTILE(4) OVER (ORDER BY total_value) AS quartile
    FROM customer_lifetime_value
)
SELECT
    customer_id,
    ROUND(total_value, 2) AS total_value,
    quartile,
    CASE quartile
        WHEN 4 THEN 'Platinum'
        WHEN 3 THEN 'Gold'
        WHEN 2 THEN 'Silver'
        ELSE 'Bronze'
    END AS quartile_label
FROM quartiled
ORDER BY total_value DESC;

-- Q12.Compare each month's revenue with same month previous year. Show: year, month, revenue, prev_year_revenue, yoy_growth_percent,Handle cases where previous year data doesn't exist.
WITH monthly_revenue AS (
    SELECT
        CAST(strftime('%Y', o.order_date) AS INTEGER) AS year,
        CAST(strftime('%m', o.order_date) AS INTEGER) AS month,
        SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)) AS revenue
    FROM order_items oi
    JOIN orders o ON o.order_id = oi.order_id
    WHERE oi.quantity > 0
    GROUP BY year, month
)
SELECT
    cur.year,
    cur.month,
    ROUND(cur.revenue, 2) AS revenue,
    ROUND(prev.revenue, 2) AS prev_year_revenue,
    CASE
        WHEN prev.revenue IS NULL OR prev.revenue = 0 THEN NULL
        ELSE ROUND(100.0 * (cur.revenue - prev.revenue) / prev.revenue, 2)
    END AS yoy_growth_percent
FROM monthly_revenue cur
LEFT JOIN monthly_revenue prev
    ON prev.year = cur.year - 1 AND prev.month = cur.month
ORDER BY cur.year, cur.month;

-- Q13.For each customer, show their first purchased category and most recent purchased category. Flag if they are different (category_shift = 'Yes'/'No')

WITH customer_category_orders AS (
    SELECT
        o.customer_id,
        o.order_date,
        p.category,
        FIRST_VALUE(p.category) OVER (
            PARTITION BY o.customer_id ORDER BY o.order_date
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) AS first_category,
        LAST_VALUE(p.category) OVER (
            PARTITION BY o.customer_id ORDER BY o.order_date
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) AS last_category
    FROM order_items oi
    JOIN orders o ON o.order_id = oi.order_id
    JOIN products p ON p.product_id = oi.product_id
    WHERE oi.quantity > 0 AND o.customer_id IS NOT NULL
)
SELECT DISTINCT
    customer_id,
    first_category,
    last_category,
    CASE WHEN first_category <> last_category THEN 'Yes' ELSE 'No' END AS category_shift
FROM customer_category_orders
ORDER BY customer_id;

-- Q14. Cumulative distribution: % of total revenue from top N% of customers
WITH customer_revenue AS (
    SELECT
        o.customer_id,
        SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)) AS revenue
    FROM order_items oi
    JOIN orders o ON o.order_id = oi.order_id
    WHERE oi.quantity > 0 AND o.customer_id IS NOT NULL
    GROUP BY o.customer_id
),
ranked AS (
    SELECT
        customer_id,
        revenue,
        SUM(revenue) OVER (ORDER BY revenue DESC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cumulative_revenue,
        SUM(revenue) OVER () AS grand_total_revenue
    FROM customer_revenue
)
SELECT
    customer_id,
    ROUND(revenue, 2) AS revenue,
    ROUND(cumulative_revenue, 2) AS cumulative_revenue,
    ROUND(100.0 * cumulative_revenue / grand_total_revenue, 2) AS cumulative_percent
FROM ranked
ORDER BY revenue DESC;

-- Q15. Group customers by their registration month (cohort).
-- For each cohort, calculate:
-- How many ordered in month 0 (registration month)
-- How many ordered in month 1, month 2, month 3
-- Retention rate for each month

WITH cohorts AS (
    SELECT
        customer_id,
        strftime('%Y-%m', registration_date) AS cohort_month
    FROM customers
),
customer_orders_with_offset AS (
    SELECT
        o.customer_id,
        c.cohort_month,
        -- month offset = how many calendar months after registration this order happened
        (CAST(strftime('%Y', o.order_date) AS INTEGER) - CAST(strftime('%Y', c2.registration_date) AS INTEGER)) * 12
        + (CAST(strftime('%m', o.order_date) AS INTEGER) - CAST(strftime('%m', c2.registration_date) AS INTEGER)) AS month_offset
    FROM orders o
    JOIN cohorts c ON c.customer_id = o.customer_id
    JOIN customers c2 ON c2.customer_id = o.customer_id
    WHERE o.customer_id IS NOT NULL
),
cohort_size AS (
    SELECT cohort_month, COUNT(DISTINCT customer_id) AS cohort_customers
    FROM cohorts
    GROUP BY cohort_month
),
activity_by_offset AS (
    SELECT
        cohort_month,
        month_offset,
        COUNT(DISTINCT customer_id) AS active_customers
    FROM customer_orders_with_offset
    WHERE month_offset BETWEEN 0 AND 3
    GROUP BY cohort_month, month_offset
)
SELECT
    a.cohort_month,
    cs.cohort_customers,
    a.month_offset,
    a.active_customers,
    ROUND(100.0 * a.active_customers / cs.cohort_customers, 2) AS retention_rate_percent
FROM activity_by_offset a
JOIN cohort_size cs ON cs.cohort_month = a.cohort_month
ORDER BY a.cohort_month, a.month_offset;
