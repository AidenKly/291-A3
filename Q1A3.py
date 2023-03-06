# General prompt:
# Q1: Given a random customer_postal_code from Customers, find how many orders containing more
# than 1 item have been placed by customers who have that customer_postal_code.

import time, sqlite3, random, matplotlib.pyplot as plt, numpy as np
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

SMALL_DB_NAME = "A3Small.db"
MED_DB_NAME = "A3Medium.db"
LARGE_DB_NAME = "A3Large.db"

ORDERS_INDEXING = "CREATE INDEX IF NOT EXISTS indx_orders_order_id ON Orders (order_id, customer_id);"
ORDER_ITEMS_INDEXING = "CREATE INDEX IF NOT EXISTS indx_order_items_order_id ON Order_items (order_id, order_item_id);"
CUSTOMER_INDEXING = "CREATE INDEX IF NOT EXISTS indx_customer_customerid ON Customers (customer_id, customer_postal_code);"
UNINFORMED_POSTAL_QUERY = "SELECT customer_postal_code FROM Customers2;"
POSTAL_QUERY = "SELECT customer_postal_code FROM Customers;"
DATABASE_NAMES = [SMALL_DB_NAME, MED_DB_NAME, LARGE_DB_NAME]
TABLE_NAMES = ['"Customers', '"Sellers', '"Orders', '"Order_items']
ATTRIBUTE_NAMES = ['"customer_id"', '"customer_postal_code"', '"seller_id"', '"seller_postal_code"', '"order_id"', 'customer_id']
ATTRIBUTE_DOMAINS = ["TEXT", "INTEGER", "TEXT", "INTEGER", "TEXT", "TEXT"]



def connect_to_db(name):
    conn = sqlite3.connect(name) 
    c = conn.cursor()
    return conn, c

def commit_and_close_db(conn):
    conn.commit()
    conn.close()

def setup_uninformed_tables(c):
    c.execute("PRAGMA automatic_index = OFF;")
    c.execute("PRAGMA foreign_keys = OFF;")
    for i in range(len(TABLE_NAMES) - 1):
        c.execute('CREATE TABLE IF NOT EXISTS' + TABLE_NAMES[i] + '2" (' + ATTRIBUTE_NAMES[2 * i] + ' ' + ATTRIBUTE_DOMAINS[2 * i] + ', ' + ATTRIBUTE_NAMES[2 * i + 1] + ' ' +  ATTRIBUTE_DOMAINS[2 * i + 1] + ');')
    c.execute('CREATE TABLE IF NOT EXISTS "Order_items2" ("order_id" TEXT, "order_item_id" INTEGER, "product_id" TEXT, "seller_id" TEXT);')
    for i in range(len(TABLE_NAMES)):
            c.execute('INSERT INTO ' + TABLE_NAMES[i] + '2" SELECT * FROM ' + TABLE_NAMES[i] + '" WHERE NOT EXISTS (SELECT * FROM ' + TABLE_NAMES[i] + '2");')

def execute_query(c, query1, query2):
    for i in range(50):
            c.execute(query1)
            codes = c.fetchall()
            code = random.choice(codes)
            c.execute(query2 + str(code[0]) + ";")

def main():
    times = []

    for database in DATABASE_NAMES:

        conn, c = connect_to_db(database)

        c.execute("DROP TABLE IF EXISTS indx_order_items_order_id;")
        c.execute("DROP TABLE IF EXISTS indx_orders_order_id;")
        c.execute("DROP TABLE IF EXISTS indx_customer_customer_id;")
        c.execute("DROP TABLE IF EXISTS indx_sellers_seller_id;")
        
        setup_uninformed_tables(c)
        
        # Start timer
        start_time = time.perf_counter() 
        execute_query(c, UNINFORMED_POSTAL_QUERY, "SELECT COUNT(O.order_id) FROM Orders2 O, Customers2 C, Order_items2 OI WHERE O.order_id = OI.order_id AND C.customer_id = O.customer_id AND OI.order_item_id > 1 AND C.customer_postal_code = ")
        stop_time = time.perf_counter()

        no_index_time_avg = (stop_time - start_time) / 50
        times.append(no_index_time_avg) # Append to time list
        print(no_index_time_avg)
        commit_and_close_db(conn)

        # SELF INDEX -----------------------------------------
        conn, c = connect_to_db(database)
        c.execute("PRAGMA automatic_index = ON;")
        c.execute("PRAGMA foreign_keys = ON;")

        start_time = time.perf_counter() 
        execute_query(c, POSTAL_QUERY, "SELECT COUNT(O.order_id) FROM Orders O, Customers C, Order_items OI WHERE O.order_id = OI.order_id AND C.customer_id = O.customer_id AND OI.order_item_id > 1 AND C.customer_postal_code = ")
        stop_time = time.perf_counter()

        self_index_time_avg = (stop_time - start_time) / 50
        times.append(self_index_time_avg) # Append to time list
        print(self_index_time_avg)
        commit_and_close_db(conn)

        # OUR INDEXING --------------------------------------
        conn, c = connect_to_db(database)
        c.execute(ORDERS_INDEXING)
        c.execute(ORDER_ITEMS_INDEXING)
        c.execute(CUSTOMER_INDEXING)

        start_time = time.perf_counter() 
        execute_query(c, POSTAL_QUERY, "SELECT COUNT(O.order_id) FROM Orders O, Customers C, Order_items OI WHERE O.order_id = OI.order_id AND C.customer_id = O.customer_id AND OI.order_item_id > 1 AND C.customer_postal_code = ")
        stop_time = time.perf_counter()

        our_index_time_avg = (stop_time - start_time) / 50
        times.append(our_index_time_avg) # Append to time list
        print(our_index_time_avg)
        commit_and_close_db(conn)
    
    x = ["SmallDB", "MediumDB", "LargeDB"]
    list1 = [times[0], times[3], times[6]]
    list2 =[times[1], times[4], times[7]]
    list3 = [times[2], times[5], times[8]]
    y1 = np.array(list1)
    y2 = np.array(list2)
    y3 = np.array(list3)

    plt.bar(x, y1, color = 'b')
    plt.bar(x, y2, bottom= y1, color = 'r')
    plt.bar(x, y3, bottom= y1 + y2, color = 'y')
    plt.xlabel("Database Sizes")
    plt.ylabel("Average Runtime (s)")
    plt.legend(["Uninformed", "Self-Optimized", "User-Optimized"])
    plt.title("Question 1")
    plt.savefig('Q1A3Chart.png')

main()