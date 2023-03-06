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


# "SELECT Cu.customer_id FROM Customers Cu, Orders Ord WHERE Cu.customer_id = Ord.customer_id GROUP BY Cu.customer_id HAVING COUNT(order_id) > 1;"

# select a random result from previous

# SELECT Ord.order_id
# FROM Customers Cu, Orders Ord 
# WHERE Cu.customer_id = Ord.customer_id AND
# customer_id = "{random_customer_id}"

# run next query for ever one of previous

# SELECT COUNT(DISTINCT seller_postal_code) 
# FROM Customers Cu, Orders Ord, Sellers S, Order_items Oi
# WHERE Cu.customer_id = Ord.customer_id AND
# Ord.order_id = Oi.order_id AND
# S.seller_id = Oi.seller_id AND
# Cu.order_id = "{order_id_from_random_customer}



def connect_to_db(name):
    conn = sqlite3.connect(name) 
    c = conn.cursor()
    return conn, c

def commit_and_close_db(conn):
    conn.commit()
    conn.close()

def create_graph(times):
    Uninformed_times = [times[0], times[3], times[6]]
    Self_optimized_times = [times[1], times[4], times[7]]
    User_optimized_times = [times[2], times[5], times[8]]
    x_axies_labels = ["SmallDB", "MediumDB", "LargeDB"]

    plt.bar(x_axies_labels, Uninformed_times, color='b')
    plt.bar(x_axies_labels, Self_optimized_times, bottom=Uninformed_times , color='r')
    plt.bar(x_axies_labels, User_optimized_times, bottom=Uninformed_times + Self_optimized_times, color='g')
    plt.legend(["Uninformed", "Self-optimized", "User-optimized"])
    plt.title("Query 4 (Runtime in seconds)")
    plt.savefig("Q4A3Chart.png")
    

def main():
    database_names = [SMALL_DB_NAME, MED_DB_NAME, LARGE_DB_NAME]
    table_names = ['"Customers', '"Sellers', '"Orders', '"Order_items']
    attribute_names = ['"customer_id"', '"customer_postal_code"', '"seller_id"', '"seller_postal_code"', '"order_id"', 'customer_id']
    attribute_domains = ["TEXT", "INTEGER", "TEXT", "INTEGER", "TEXT", "TEXT"]
    times = []

    for database in database_names:
        print("\n" + database)
        # NO INDEX -------------------------------------------
        # Turns Off Indexing
        conn, c = connect_to_db(database)
        c.execute("DROP TABLE IF EXISTS indx_orders_order_id;")
        c.execute("DROP TABLE IF EXISTS indx_order_items_order_id;")
        c.execute("DROP TABLE IF EXISTS indx_customer_customer_id;")
        c.execute("DROP TABLE IF EXISTS indx_sellers_seller_id;")

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
            c.execute('INSERT INTO ' + table_names[i] + '2" SELECT * FROM ' + table_names[i] + '" WHERE NOT EXISTS (SELECT * FROM ' + table_names[i] + '2");')



        
        # Start timer
        start_time = time.perf_counter() 
        for i in range(50):
            c.execute("SELECT Cu.customer_id FROM Customers2 Cu, Orders2 Ord WHERE Cu.customer_id = Ord.customer_id GROUP BY Cu.customer_id HAVING COUNT(order_id) > 1;")
            customers = c.fetchall()
            try:
                random_customer_id = random.choice(customers)
            except:
                random_customer_id = "NONE"
            c.execute(f'SELECT Ord.order_id\
                        FROM Customers2 Cu, Orders2 Ord \
                        WHERE Cu.customer_id = Ord.customer_id AND\
                        Cu.customer_id = "{random_customer_id}"')
            order_ids = c.fetchall()
            for order_id_from_random_customer in order_ids:
                c.execute(f'SELECT COUNT(DISTINCT seller_postal_code)  \
                            FROM Customers2 Cu, Orders2 Ord, Sellers2 S, Order_items2 Oi \
                            WHERE Cu.customer_id = Ord.customer_id AND \
                            Ord.order_id = Oi.order_id AND \
                            S.seller_id = Oi.seller_id AND \
                            Cu.order_id = "{order_id_from_random_customer}"')
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
            c.execute("SELECT Cu.customer_id FROM Customers Cu, Orders Ord WHERE Cu.customer_id = Ord.customer_id GROUP BY Cu.customer_id HAVING COUNT(order_id) > 1;")
            customers = c.fetchall()
            try:
                random_customer_id = random.choice(customers)
            except:
                random_customer_id = ""
            c.execute(f'SELECT Ord.order_id\
                        FROM Customers Cu, Orders Ord \
                        WHERE Cu.customer_id = Ord.customer_id AND\
                        Cu.customer_id = "{random_customer_id}"')
            order_ids = c.fetchall()
            for order_id_from_random_customer in order_ids:
                c.execute(f'SELECT COUNT(DISTINCT seller_postal_code)  \
                            FROM Customers Cu, Orders Ord, Sellers S, Order_items Oi \
                            WHERE Cu.customer_id = Ord.customer_id AND \
                            Ord.order_id = Oi.order_id AND \
                            S.seller_id = Oi.seller_id AND \
                            Cu.order_id = "{order_id_from_random_customer}"')
        stop_time = time.perf_counter()

        self_index_time_avg = (stop_time - start_time) / 50
        times.append(self_index_time_avg) # Append to time list
        print(self_index_time_avg)
        commit_and_close_db(conn)



        # OUR INDEXING --------------------------------------
        conn, c = connect_to_db(database)
        c.execute("CREATE INDEX IF NOT EXISTS indx_orders_order_id ON Orders (order_id, customer_id);")
        c.execute("CREATE INDEX IF NOT EXISTS indx_order_items_order_id ON Order_items (order_id, seller_id);")
        c.execute("CREATE INDEX IF NOT EXISTS indx_customer_customer_id ON Customers (customer_id);")
        c.execute("CREATE INDEX IF NOT EXISTS indx_sellers_seller_id ON Sellers (seller_id);")

        start_time = time.perf_counter() 
        for i in range(50):
            c.execute("SELECT Cu.customer_id FROM Customers Cu, Orders Ord WHERE Cu.customer_id = Ord.customer_id GROUP BY Cu.customer_id HAVING COUNT(order_id) > 1;")
            customers = c.fetchall()
            try:
                random_customer_id = random.choice(customers)
            except:
                random_customer_id = "NONE"
            c.execute(f'SELECT Ord.order_id\
                        FROM Customers Cu, Orders Ord \
                        WHERE Cu.customer_id = Ord.customer_id AND\
                        Cu.customer_id = "{random_customer_id}"')
            order_ids = c.fetchall()
            for order_id_from_random_customer in order_ids:
                c.execute(f'SELECT COUNT(DISTINCT seller_postal_code)  \
                            FROM Customers Cu, Orders Ord, Sellers S, Order_items Oi \
                            WHERE Cu.customer_id = Ord.customer_id AND \
                            Ord.order_id = Oi.order_id AND \
                            S.seller_id = Oi.seller_id AND \
                            Cu.order_id = "{order_id_from_random_customer}"')
        stop_time = time.perf_counter()

        our_index_time_avg = (stop_time - start_time) / 50
        times.append(our_index_time_avg) # Append to time list
        print(our_index_time_avg)
        commit_and_close_db(conn)



    create_graph(times)

main()