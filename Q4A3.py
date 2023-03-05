--# Q4: Choose a random customer with more than one order and for that customer's orders, find in how
--# many (unique) postal codes the sellers provided those orders.





-- run next query for ever one of previous

SELECT COUNT(DISTINCT seller_postal_code) 
FROM Customers Cu, Orders Ord, Sellers S, Order_items Oi
WHERE Cu.customer_id = Ord.customer_id AND
Ord.order_id = Oi.order_id AND
S.seller_id = Oi.seller_id AND
Cu.order_id = "{order_id_from_random_customer}"


import time, sqlite3, random
# 1. Connect to A3Small.db
#       1. Set scenario “Uninformed”
#       2. Execute Q1 50 times (collecting query execution time).
#       3. DisconnectA3Small.db and reconnect (this is to minimizecaching effects by
#       SQLite)
#       4. Set scenario “Self-optimized”
#       5. Execute Q1 50 times (collecting query execution time)
#       6. DisconnectA3Small.db and reconnect (this is to minimizecaching effects by
#       SQLite)
#       7. Set scenario “User-optimized”
#       8. Execute Q1 50 times (collecting query execution time)
#       9. DisconnectA3Small.db
# 2. Connect toA3Medium.db
#       1. Repeat steps 2-9
#       2. DisconnectA3Medium.db
# 3. Connect to A3Large.db
#       1. Repeat steps 2-9
#       2. DisconnectA3Large.db
# 4. Plot query performance results.

SMALL_DB_NAME = "s.db"
MED_DB_NAME = "m.db"
LARGE_DB_NAME = "l.db"

OUR_OPTIMIZED_INDEXING = ";"
CUSTOMER_SELECT_QUERY = "SELECT Cu.customer_id \
                        FROM Customers Cu, Orders Ord \
                        WHERE Cu.customer_id = Ord.customer_id\
                        GROUP BY Cu.customer_id\
                        HAVING COUNT(order_id) > 1;"
# select a random result from previous
QUERY = f'SELECT Ord.order_id\
FROM Customers Cu, Orders Ord \
WHERE Cu.customer_id = Ord.customer_id AND\
customer_id = "{random_customer_id}"'



def connect_to_db(name):
    conn = sqlite3.connect(name) 
    c = conn.cursor()
    return conn, c

def commit_and_close_db(conn):
    conn.commit()
    conn.close()

def main():
    database_names = [SMALL_DB_NAME, MED_DB_NAME, LARGE_DB_NAME]
    table_names = ['"Customers', '"Sellers', '"Orders', '"Order_items']
    attribute_names = ['"customer_id"', '"customer_postal_code"', '"seller_id"', '"seller_postal_code"', '"order_id"', 'customer_id']
    attribute_domains = ["TEXT", "INTEGER", "TEXT", "INTEGER", "TEXT", "TEXT"]
    times = []

    for database in database_names:
        # NO INDEX -------------------------------------------
        # Turns Off Indexing
        conn, c = connect_to_db(database)
        c.execute("PRAGMA automatic_index = OFF")
        c.execute("PRAGMA foreign_keys = OFF")
        #           FIGURE OUT HOW TO REMOVE PRIMARY KEYS
        try:
            for i in range(len(table_names) - 1):
                c.execute('CREATE TABLE ' + table_names[i] + '2" (' + attribute_names[2 * i] + ' ' + attribute_domains[2 * i] + ', ' + attribute_names[2 * i + 1] + ' ' +  attribute_domains[2 * i + 1] + ');')
            c.execute('CREATE TABLE "Order_items2" ("order_id" TEXT, "order_item_id" INTEGER, "product_id" TEXT, "seller_id" TEXT);')
        except:
            pass

        for i in range(len(table_names)):
            c.execute('INSERT INTO ' + table_names[i] + '2" SELECT * FROM ' + table_names[i] + '";')



        
        # Start timer
        start_time = time.perf_counter() 
        for i in range(50):
            c.execute(QUERY)
            #---------------
            # ADD MORE HERE IF NEEDED
            #---------------
        stop_time = time.perf_counter()

        no_index_time_avg = (stop_time - start_time) / 50
        times.append(no_index_time_avg) # Append to time list
        print(no_index_time_avg)
        commit_and_close_db(conn)

        # SELF INDEX -----------------------------------------
        conn, c = connect_to_db(database)
        c.execute("PRAGMA automatic_index = ON")
        c.execute("PRAGMA foreign_keys = ON")

        start_time = time.perf_counter() 
        for i in range(50):
            c.execute(QUERY)
            #---------------
            # ADD MORE HERE IF NEEDED
            #---------------
        stop_time = time.perf_counter()

        self_index_time_avg = (stop_time - start_time) / 50
        times.append(self_index_time_avg) # Append to time list
        print(self_index_time_avg)
        commit_and_close_db(conn)



        # OUR INDEXING --------------------------------------
        conn, c = connect_to_db(database)
        c.execute(OUR_OPTIMIZED_INDEXING)
        c.execute(OUR_OPTIMIZED_INDEXING)

        start_time = time.perf_counter() 
        for i in range(50):
            c.execute(QUERY)
            #---------------
            # ADD MORE HERE IF NEEDED
            #---------------
        stop_time = time.perf_counter()

        our_index_time_avg = (stop_time - start_time) / 50
        times.append(our_index_time_avg) # Append to time list
        print(our_index_time_avg)
        commit_and_close_db(conn)


main()