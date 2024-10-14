SELECT c.full_name, o.order_no 
FROM "order" o JOIN customer c ON c.customer_id = o.customer_id 
WHERE c.manager_id IS NULL;
