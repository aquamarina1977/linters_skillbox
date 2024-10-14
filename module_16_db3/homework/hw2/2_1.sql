SELECT c.full_name
FROM "order" o JOIN customer c ON c.customer_id != o.customer_id;
