
-- =========================================================
-- E-COMMERCE SALES DATA PIPELINE
-- SQL ANALYTICS QUERIES
-- Database: ecommerce_db
-- =========================================================


-- 1. Total gross order-item sales value
SELECT
    SUM(quantity * unit_price) AS total_gross_sales
FROM order_items;


-- 2. Monthly sales trend
SELECT
    DATE_TRUNC('month', o.order_date) AS sales_month,
    SUM(oi.quantity * oi.unit_price) AS monthly_sales
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY DATE_TRUNC('month', o.order_date)
ORDER BY sales_month;


-- 3. Top 5 products by sales value
SELECT
    p.product_name,
    SUM(oi.quantity) AS units_sold,
    SUM(oi.quantity * oi.unit_price) AS total_sales
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.product_id, p.product_name
ORDER BY total_sales DESC
LIMIT 5;


-- 4. Top 5 customers by gross order-item value
SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    SUM(oi.quantity * oi.unit_price) AS total_purchase_value
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY total_purchase_value DESC
LIMIT 5;


-- 5. Order status distribution
SELECT
    status,
    COUNT(*) AS total_orders
FROM orders
GROUP BY status
ORDER BY total_orders DESC;


-- 6. Payment status distribution
SELECT
    payment_status,
    COUNT(*) AS total_payments
FROM payments
GROUP BY payment_status
ORDER BY total_payments DESC;


-- 7. Payment method analysis
SELECT
    payment_method,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_payment_amount
FROM payments
GROUP BY payment_method
ORDER BY total_payment_amount DESC;


-- 8. Average order value
WITH order_values AS (
    SELECT
        o.order_id,
        SUM(oi.quantity * oi.unit_price) AS order_value
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY o.order_id
)
SELECT
    AVG(order_value) AS average_order_value
FROM order_values;


-- 9. Sales by product category
SELECT
    p.category,
    SUM(oi.quantity) AS units_sold,
    SUM(oi.quantity * oi.unit_price) AS category_sales
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.category
ORDER BY category_sales DESC;


-- 10. Sales by customer city
SELECT
    c.city,
    SUM(oi.quantity * oi.unit_price) AS total_sales
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY c.city
ORDER BY total_sales DESC;


-- 11. Successful payment collections
SELECT
    SUM(amount) AS successful_collections
FROM payments
WHERE payment_status IN ('Paid', 'Completed');


-- 12. Monthly successful payment collections
SELECT
    DATE_TRUNC('month', payment_date) AS payment_month,
    SUM(amount) AS monthly_collections
FROM payments
WHERE payment_status IN ('Paid', 'Completed')
GROUP BY DATE_TRUNC('month', payment_date)
ORDER BY payment_month;


-- 13. Returned orders and refunded payments
SELECT
    'Returned Orders' AS metric,
    COUNT(*) AS total_records
FROM orders
WHERE status = 'Returned'

UNION ALL

SELECT
    'Refunded Payments' AS metric,
    COUNT(*) AS total_records
FROM payments
WHERE payment_status = 'Refunded';
