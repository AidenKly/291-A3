Assignment 3 - CMPUT291

Group ID: #17

Members: William Creaser (wcreaser), Aiden Klymchuk (aklymchu), Kaye Maranan (kayecryz)

- We did not collaborate with anyone outside of our own group in this assignment

Resources:
    https://www.geeksforgeeks.org/working-csv-files-python/
    https://matplotlib.org/stable/gallery/lines_bars_and_markers/bar_stacked.html
    https://www.geeksforgeeks.org/create-a-stacked-bar-plot-in-matplotlib/
    https://www.sqlitetutorial.net/sqlite-index/



######################
# Info for questions #
######################
---------------------------------------------------------------------------------------------------------------------------------
For each Uninformed scenario, in order to remove primary keys, the tables were recreated as their respective names 
with the number 2 (eg. Customers2 vs Customers) WITHOUT declaring a primary key. The uninformed scenario queries 
were then run on these new, primary-key-less tables to ensure experimental consistency with the uninformed scenario description.
---------------------------------------------------------------------------------------------------------------------------------


    ***************
    * Question #1 *
    ***************

###########
# Queries #
###########

Queries here!

###########
# Indices #
###########

Indices here!

    ***************
    * Question #2 *
    ***************

###########
# Queries #
###########
------------------------------------------------------------------------------------------------------------------------------------
[2] indicates a variation in table names. The uninformed case uses the non-primary key tables ([2]), but the other two cases do not
------------------------------------------------------------------------------------------------------------------------------------

CREATE VIEW OrderSize 
AS SELECT i.order_id as oid, i.order_item_id  as size 
FROM Orders[2] o, Order_items[2] i, Customers[2] c 
WHERE o.order_id = i.order_id
AND c.customer_id = o.customer_id 
AND c.customer_postal_code = " + str(code[0]) + ";"

– This query creates a view that takes data from joining three tables (Orders, Customers and Order_items). This expands on Q1 by creating a view displaying the order ids and the sizes of the orders that are all from customers that have the same randomly selected postal code. The view is outside of the for loop since the view is only created once


SELECT oid 
FROM OrderSize 
WHERE size > (SELECT AVG(order_item_id) 
FROM Order_items2);
– This query is within the loop. It takes the oids (order ids) from the ordersize view that have an order size greater than the average out of the the order_item_id (number of items per order) from the order_times.

Drop view OrderSize;
– dropping the view is needed since the view is now unnecessary.

###########
# Indices #
###########

CREATE INDEX IF NOT EXISTS indx_orders_order_id ON Orders (order_id, customer_id);
– The index created here is on the order_id and the customer_id since these two are the attributes being used in the where statement and can increase efficiency compared to if there were no indices

CREATE INDEX IF NOT EXISTS indx_order_items_order_id ON Order_items (order_id, order_item_id);
– The index created here is on the order_id and the order_item_id since these two are the attributes being used in the where statement and can increase efficiency compared to if there were no indices

CREATE INDEX IF NOT EXISTS indx_customer_customer_id ON Customers (customer_id, customer_postal_code);
– The index created here is on the customer_id and the customer_postal_code since these two are the attributes being used in the where statement and can increase efficiency compared to if there were no indices

    ***************
    * Question #3 *
    ***************
    
###########
# Queries #
###########

Queries here!

###########
# Indices #
###########

Indices here!

    ***************
    * Question #4 *
    ***************

###########
# Queries #
###########
--------------------------------------------------------------------------------------------------------
Everything enclosed in [] indicates a potential difference depending on the scenario (eg. Customers[2]).
--------------------------------------------------------------------------------------------------------

SELECT Cu.customer_id 
FROM Customers[2] Cu, Orders[2] Ord 
WHERE Cu.customer_id = Ord.customer_id 
GROUP BY Cu.customer_id 
HAVING COUNT(order_id) > 1;
    
    - This query selects all of the customer_ids belonging to customers who have more than one order (differentiated by order_id).

SELECT Ord.order_id
FROM Customers[2] Cu, Orders[2] Ord 
WHERE Cu.customer_id = Ord.customer_id AND
Cu.customer_id = "{random_customer_id}"
    
    - This query selects all of the order_ids from a randomly chosen customer_id, the section "Cu.customer_id = "{random_customer_id}""
    uses python's f-string formatting to embed a randomly chosen customer_id into the query.

SELECT COUNT(DISTINCT seller_postal_code)
FROM Customers[2] Cu, Orders[2] Ord, Sellers[2] S, Order_items[2] Oi
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

    - Orders.order_id and Orders.customer_id are both indexed as they are used in every SQL query in Question 4. This would increase efficiency overall compared to not having any indices on Orders.


CREATE INDEX IF NOT EXISTS indx_order_items_orderid ON Order_items (order_id, seller_id);

    - Order_items.order_id and Order_items.seller_id are both indexed as they are used in the third SQL query in Question 4. This would increase efficiency for that query over not having any indices on Order_items.


CREATE INDEX IF NOT EXISTS indx_customer_customerid ON Customers (customer_id);

    - Customers.customer_id is indexed as it is used in every SQL query in Question 4. This would increase efficiency overall compared to not having any indices on Customers.


CREATE INDEX IF NOT EXISTS indx_sellers_sellerid ON Sellers (seller_id);

    - Sellers.seller_id is indexed as it is used in the third SQL query in Question 4. This would increase efficiency for that query over not having any indices on Sellers.
