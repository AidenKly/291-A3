import csv, sqlite3, random
# Inserts data from a given csv file into a given sql table.


def read_csv(filename, row_count): # DONE
    # Takes in a filename and number of rows to randomly select
    # Returns a list of randomly selected rows from the specified .csv file name

    with open(filename, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)
        columns = next(csvreader)
        rows = []
        # extracting each data row one by one
        for row in csvreader:
            rows.append(row)
        csvfile.close()
        
    row_subset = []

    while len(row_subset) < row_count:
        random_row = random.choice(rows)
        if random_row not in row_subset:
            row_subset.append(random_row)
    
    return row_subset



def reduce_to_columns(row_list, columns_to_save): # DONE
    # remove all columns other than those specified in columns_to_save from the row list
    column_reduced_row_list = []
    for row_index in range(len(row_list)):
        single_row = []
        for column_index in columns_to_save:
            single_row.append(row_list[row_index][column_index])
            
        column_reduced_row_list.append(single_row)
    return column_reduced_row_list

def format_rows(row_list): # DONE
    # Formats the rows to be inserted into the database from standard python formatting
    # to a long sting following propper sql formatting
    formatted_rows = []
    for row in row_list:
        for index in range(len(row)):
            try:
                int(row[index])
            except:
                row[index] = "'" + row[index] + "'"
            
        str_row = ','.join(row)
        str_row.replace('"', "'")
        formatted_rows.append(str_row)
    
    formatted_rows_str = '),\n('.join(formatted_rows)
    formatted_rows_str = '(' + formatted_rows_str + ');'
    return formatted_rows_str
        



def insert_into_database(database_name, table_name, formatted_row_str): # DONE
    # Inserts a sql-formatted string of rows into a specified table in a database
    conn = sqlite3.connect(database_name) 
    c = conn.cursor()
    c.execute("INSERT INTO " + table_name + " VALUES\n" + formatted_row_str)
    conn.commit()
    conn.close()

def setup_database(database_name):
    # sets up the database using the "dbSetup.sql" file
    conn = sqlite3.connect(database_name) 
    c = conn.cursor()
    c.execute(' PRAGMA foreign_keys=ON; ')
    setup_file = open("dbSetup.sql")
    setup_script_list = setup_file.read().split(';')
    setup_file.close()
    for command in setup_script_list:
        c.execute(command)
    conn.commit()
    conn.close()

def insertion_setup(data_size, table_name):
    csv_file_path = input("Enter the FULL csv path for the " + table_name + " table data >> ") 
    
    preserved_columns = input("Enter the csv column indexes you want to insert into the " + table_name + "table, seperated by COMMAS >> ")
    print()
    preserved_columns = preserved_columns.split(',')
    for index in range(len(preserved_columns)):
        preserved_columns[index] = int(preserved_columns[index])
    
    for i in range(len(data_size)):
        print("Starting Data extraction ...")
        row_list = read_csv(csv_file_path, data_size[i])
        print("Data extraction complete\n")
        print("Starting Column removal ...")
        reduced_entries = reduce_to_columns(row_list, preserved_columns)
        print("Column removal complete\n")
        print("Starting row formatting ...")
        formatted_row_str = format_rows(reduced_entries)
        print("Row formatting complete\n")
        print(formatted_row_str)
        print("Starting data insert ...")
        insert_into_database(database_name, table_name, formatted_row_str)
        print("Data insert complete")

def main():
    SMALL_DATABASE_CUSTOMERS = 10000
    SMALL_DATABASE_SELLERS = 500
    SMALL_DATABASE_ORDERS = 10000
    SMALL_DATABASE_ORDER_ITEMS = 2000

    MEDIUM_DATABASE_CUSTOMERS = 20000
    MEDIUM_DATABASE_SELLERS = 750
    MEDIUM_DATABASE_ORDERS = 20000
    MEDIUM_DATABASE_ORDER_ITEMS = 4000
    
    LARGE_DATABASE_CUSTOMERS = 33000
    LARGE_DATABASE_SELLERS = 1000
    LARGE_DATABASE_ORDERS = 33000
    LARGE_DATABASE_ORDER_ITEMS = 10000

    table_names = {"Customers", "Sellers", "Orders", "Order_items"}

    customer_table_sizes = {SMALL_DATABASE_CUSTOMERS, MEDIUM_DATABASE_CUSTOMERS, LARGE_DATABASE_CUSTOMERS}
    seller_table_sizes = {SMALL_DATABASE_SELLERS, MEDIUM_DATABASE_SELLERS, LARGE_DATABASE_SELLERS}
    order_table_sizes = {SMALL_DATABASE_ORDERS, MEDIUM_DATABASE_ORDERS, LARGE_DATABASE_ORDERS}
    order_items_table_sizes = {SMALL_DATABASE_ORDER_ITEMS, MEDIUM_DATABASE_ORDER_ITEMS, LARGE_DATABASE_ORDER_ITEMS}

    table_sizes = {customer_table_sizes, seller_table_sizes, order_table_sizes, order_items_table_sizes}
    
    database_titles = {'Small', 'Medium', 'Large'}
    database_names = []

    for i in range(len(database_titles)):
        database_names.append(input("Enter the FULL Database filepath for the " + database_titles[i] + ">> "))
        setup_database(database_names[i])
    
    for i in range(len(table_names)):
        insertion_setup(table_sizes[i], table_names[i])
      
    
main()