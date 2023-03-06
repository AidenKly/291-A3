Assignment 3 - CMPUT291

Group ID: #17

Members: William Creaser (wcreaser), Aiden Klymchuk (aklymchu), Kaye Maranan (kayecryz)

- We did not collaborate with anyone outside of our own group in this assignment

User Optimized Scenarios
#1

#2

#3

#4

###########
# Queries #
###########

SELECT Cu.customer_id 
FROM Customers Cu, Orders Ord 
WHERE Cu.customer_id = Ord.customer_id 
GROUP BY Cu.customer_id 
HAVING COUNT(order_id) > 1;
    
    - This query selects all of the customer_ids belonging to customers who have more than one order (differentiated by order_id).

SELECT Ord.order_id
FROM Customers2 Cu, Orders2 Ord 
WHERE Cu.customer_id = Ord.customer_id AND
Cu.customer_id = "{random_customer_id}"
    
    - This query selects all of the order_ids from a randomly chosen customer_id, the section "Cu.customer_id = "{random_customer_id}""
    uses python's f-string formatting to embed a randomly chosen customer_id into the query.

SELECT COUNT(DISTINCT seller_postal_code)
FROM Customers2 Cu, Orders2 Ord, Sellers2 S, Order_items2 Oi
WHERE Cu.customer_id = Ord.customer_id AND
Ord.order_id = Oi.order_id AND
S.seller_id = Oi.seller_id AND
Cu.order_id = "{order_id_from_random_customer}"
    
    - This query selects unique postal codes from which a given order_id was supplied. The query is run in a for loop for every result
    from the previous query and the and the section "Cu.order_id = "{order_id_from_random_customer}"" uses python's f-string formatting to embed
    every order_id gotten from the previous query into this query.

###########
# Indices #
###########


CREATE INDEX IF NOT EXISTS indx_orders_orderid ON Orders (order_id, customer_id);
CREATE INDEX IF NOT EXISTS indx_order_items_orderid ON Order_items (order_id, seller_id);
CREATE INDEX IF NOT EXISTS indx_customer_customerid ON Customers (customer_id, customer_postal_code);
CREATE INDEX IF NOT EXISTS indx_sellers_sellerid ON Sellers (seller_id);

Resources:
    https://www.geeksforgeeks.org/working-csv-files-python/
    https://matplotlib.org/stable/gallery/lines_bars_and_markers/bar_stacked.html
    https://www.geeksforgeeks.org/create-a-stacked-bar-plot-in-matplotlib/
    https://www.sqlitetutorial.net/sqlite-index/
