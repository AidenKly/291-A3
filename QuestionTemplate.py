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
QUERY = ";"



def connect_to_db(name):
    conn = sqlite3.connect(name) 
    c = conn.cursor()
    return conn, c

def commit_and_close_db(conn):
    conn.commit()
    conn.close()

def main():
    database_names = [SMALL_DB_NAME, MED_DB_NAME, LARGE_DB_NAME]
    times = []

    for database in database_names:
        # NO INDEX -------------------------------------------
        # Turns Off Indexing
        conn, c = connect_to_db(database)
        c.execute("PRAGMA automatic_index = OFF")
        c.execute("PRAGMA foreign_keys = OFF")
        
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