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
SMALL_DB_NAME = ?
MED_DB_NAME = ?
LARGE_DB_NAME = ?

QUERY = ?

def connect_to_db(name):
    conn = sqlite3.connect(name) 
    c = conn.cursor()
    return conn, c

def commit_and_close_db(conn):
    conn.commit()
    conn.close()

def main():
    database_names = [SMALL_DB_NAME, MED_DB_NAME, LARGE_DB_NAME]
    
    for database in database_names:
        # NO INDEX
        conn, c = connect_to_db(database)
        c.execute("PRAGMA automatic_index = OFF")
        c.execute("PRAGMA foreign_keys = OFF")
        for i in range(50):
            c.execute(QUERY)
        commit_and_close_db(conn)

        # SELF INDEX
        conn, c = connect_to_db(database)
        c.execute("PRAGMA PRAGMA automatic_index = ON")
        c.execute("PRAGMA foreign_keys = ON")
        for i in range(50):
            c.execute(QUERY)
        commit_and_close_db(conn)

        # OUR INDEXING
        conn, c = connect_to_db(database)
        c.execute(SELF_OPTIMIZED_HOW)
        c.execute(SELF_OPTIMIZED_HOW)
        for i in range(50):
            c.execute(QUERY)
        commit_and_close_db(conn)