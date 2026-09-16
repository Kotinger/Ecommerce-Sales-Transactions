-- шаг 6P | путь P | ключи уже в pipeline - только проверка
USE ecommerce_sales;

DESCRIBE clean_orders;
SELECT order_id, order_key FROM clean_orders LIMIT 5;

SELECT COUNT(*) AS bad_rows
FROM (
SELECT order_id
FROM clean_orders
GROUP BY order_id
HAVING COUNT(DISTINCT customer_id) > 1
) t;

SHOW TABLES LIKE 'people';
