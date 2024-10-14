SELECT o.order_no, c.full_name, m.full_name 
FROM "order" o JOIN customer c ON c.customer_id = o.customer_id
JOIN manager m ON o.manager_id = m.manager_id 
WHERE c.city <> m.city;
