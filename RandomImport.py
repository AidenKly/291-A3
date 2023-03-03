import csv, sqlite3, random
# Inserts data from a given csv file into a given sql table.


def read_csv(filename:str, row_count:int): # DONE
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



def reduce_to_columns(row_list:list, columns_to_save:tuple): # DONE
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
                row[index] = f"'{row[index]}'"
            
        str_row = ','.join(row)
        str_row.replace('"', "'")
        formatted_rows.append(str_row)
    
    formatted_rows_str = '),\n('.join(formatted_rows)
    formatted_rows_str = '(' + formatted_rows_str + ');'
    return formatted_rows_str
        



def insert_into_database(database_name:str, table_name:str, formatted_row_str:str): # DONE
    # Inserts a sql-formatted string of rows into a specified table in a database
    conn = sqlite3.connect(database_name) 
    c = conn.cursor()
    c.execute(' PRAGMA foreign_keys=ON; ')
    
    c.execute(f"INSERT INTO {table_name} VALUES\n{formatted_row_str}")
    conn.commit()
    conn.close()
    

    
def main():
    database_name = input("Enter a FULL Database filepath >> ")
    table_name = input("Enter the name of the table to be inserted into >> ")

    csv_file_path = input("Enter a FULL csv path >> ") 
    
    # "Dataset\\olist_customers_dataset.csv"
    preserved_columns = input("Enter the csv column indexes you want to insert into the database, seperated by COMMAS >> ")
    print()
    preserved_columns = preserved_columns.split(',')
    for index in range(len(preserved_columns)):
        preserved_columns[index] = int(preserved_columns[index])
    

    print("Starting Data extraction ...")
    row_list = read_csv(csv_file_path, 1000)
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
main()