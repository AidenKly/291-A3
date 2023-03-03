--# Q4: Choose a random customer with more than one order and for that customer's orders, find in how
--# many (unique) postal codes the sellers provided those orders.

SELECT COUNT(DISTINCT seller_postal_code) 
FROM Customers Cu, Orders Ord, Sellers S, Order_items Oi
WHERE Cu.customer_id = Ord.customer_id AND
Ord.order_id = Oi.order_id AND
S.seller_id = Oi.seller_id AND
Cu.customer_id = "{random_customer_id}"

