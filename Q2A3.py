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


def main():
    times = []

    for database in DATABASE_NAMES:
        # NO INDEX -------------------------------------------
        # Turns Off Indexing
        conn, c = connect_to_db(database)

        c.execute("DROP TABLE IF EXISTS indx_order_items_order_id;")
        c.execute("DROP TABLE IF EXISTS indx_orders_order_id;")
        c.execute("DROP TABLE IF EXISTS indx_customers_customer_id;")
        c.execute("DROP TABLE IF EXISTS indx_sellers_seller_id;")
        
        setup_uninformed_tables(c)

        # Start timer
        start_time = time.perf_counter() 
        c.execute("CREATE VIEW OrderSize AS SELECT i.order_id as oid, i.order_item_id  as size FROM Orders2 o, Order_items2 i, Customers2 c WHERE o.order_id = i.order_id AND c.customer_id = o.customer_id;")
        for i in range(50):
            try:
                c.execute(UNINFORMED_POSTAL_QUERY)
                codes = c.fetchall()
                code = random.choice(codes)
                c.execute(
                    "SELECT oid FROM OrderSize WHERE size > (SELECT AVG(order_item_id) FROM Order_items2) AND c.customer_postal_code = " + str(code[0]) + ";"
                )

            except sqlite3.Error as e:
                print(e);
        c.execute ("drop view OrderSize;")
        stop_time = time.perf_counter()

        no_index_time_avg = ((stop_time - start_time) / 50) * 1000
        times.append(no_index_time_avg) # Append to time list
        print(no_index_time_avg)
        commit_and_close_db(conn)

        # SELF INDEX -----------------------------------------
        conn, c = connect_to_db(database)
        c.execute("PRAGMA automatic_index = ON")
        c.execute("PRAGMA foreign_keys = ON")

        start_time = time.perf_counter() 
        c.execute("CREATE VIEW OrderSize AS SELECT i.order_id as oid, i.order_item_id  as size FROM Orders o, Order_items i, Customers c WHERE o.order_id = i.order_id AND c.customer_id = o.customer_id;")
        for i in range(50):
            try:
                c.execute(POSTAL_QUERY)
                codes = c.fetchall()
                code = random.choice(codes)
                c.execute(
                    "SELECT oid FROM OrderSize WHERE size > (SELECT AVG(order_item_id) FROM Order_items2) AND c.customer_postal_code = " + str(code[0]) + ";"
                )

            except sqlite3.Error as e:
                print(e);
        c.execute ("drop view OrderSize;")

        stop_time = time.perf_counter()

        self_index_time_avg = ((stop_time - start_time) / 50) * 1000
        times.append(self_index_time_avg) # Append to time list
        print(self_index_time_avg)
        commit_and_close_db(conn)

        # OUR INDEXING --------------------------------------
        conn, c = connect_to_db(database)
        c.execute("PRAGMA automatic_index = ON")
        c.execute("PRAGMA foreign_keys = ON")
        c.execute(ORDERS_INDEXING)
        c.execute(ORDER_ITEMS_INDEXING)
        c.execute(CUSTOMER_INDEXING)
        
        start_time = time.perf_counter() 
        c.execute("CREATE VIEW OrderSize AS SELECT i.order_id as oid, i.order_item_id  as size FROM Orders o, Order_items i, Customers c WHERE o.order_id = i.order_id AND c.customer_id = o.customer_id;")
        for i in range(50):
            try:
                c.execute(POSTAL_QUERY)
                codes = c.fetchall()
                code = random.choice(codes)
                c.execute(
                    "SELECT oid FROM OrderSize WHERE size > (SELECT AVG(order_item_id) FROM Order_items2) AND c.customer_postal_code = " + str(code[0]) + ";"
                )

            except sqlite3.Error as e:
                print(e)
        c.execute ("drop view OrderSize;")
        stop_time = time.perf_counter()
        
        our_index_time_avg = ((stop_time - start_time) / 50) * 1000
        times.append(our_index_time_avg) # Append to time list
        print(our_index_time_avg)
        commit_and_close_db(conn)

    x = ['SmallDB', 'MediumDB', 'LargeDB']
    y1 = np.array([times[0], times[3], times[6]])
    y2 = np.array([times[1], times[4], times[7]])
    y3 = np.array([times[2], times[5], times[8]])
    
    # plot bars in stack manner
    plt.bar(x, y1, color='r')
    plt.bar(x, y2, bottom=y1, color='b')
    plt.bar(x, y3, bottom=y1+y2, color='y')
    plt.xlabel("Databases")
    plt.ylabel("Time in ms")
    plt.legend(["Uninformed", "Self-Optimized", "User Optimized"])
    plt.title("Query 2 (Runtime In Seconds)")
    plt.savefig("Q2A3chart.png")
main()
