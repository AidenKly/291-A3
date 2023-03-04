--# Q4: Choose a random customer with more than one order and for that customer's orders, find in how
--# many (unique) postal codes the sellers provided those orders.

SELECT Cu.customer_id 
FROM Customers Cu, Orders Ord 
WHERE Cu.customer_id = Ord.customer_id
GROUP BY Cu.customer_id
HAVING COUNT(order_id) > 1;

-- select a random result from previous

SELECT Ord.order_id
FROM Customers Cu, Orders Ord 
WHERE Cu.customer_id = Ord.customer_id AND
customer_id = "{random_customer_id}"

-- run next query for ever one of previous

SELECT COUNT(DISTINCT seller_postal_code) 
FROM Customers Cu, Orders Ord, Sellers S, Order_items Oi
WHERE Cu.customer_id = Ord.customer_id AND
Ord.order_id = Oi.order_id AND
S.seller_id = Oi.seller_id AND
Cu.order_id = "{order_id_from_random_customer}"