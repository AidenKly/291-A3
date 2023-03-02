import csv, sqlite3, random
# Inserts data from a given csv file into a given sql table.

def get_db_info():
    database_name = input("Enter a Database filename. >> ")
    table_name = input("Enter the name of the table to be inserted into. >> ")

    csv_filename = input("Enter a csv filename. >> ")
    column_map = {}
    column_map_str = input("Enter the name of a column in the csv file then '':'' then the name of a column in the database table.\n \
                           Multiple entries are supported if they are seperated by a comma.")
    
    ','.split

def read_csv(filename:str, row_count:int):
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



def reduce_to_columns(row_list:list[list], columns_to_save:tuple[int]):
    #NOT NECESARILY NEEDED
    # remove all columns other than those specified in columns_to_save from the row list
    column_reduced_row_list = []
    for row_index in range(len(row_list)):
        single_row = []
        for column_index in columns_to_save:
            single_row.append(row_list[row_index][column_index])
            
        column_reduced_row_list.append(single_row)
    return column_reduced_row_list

def insert_into_database(database_name:str, table_name:str, column_names:list[str], row_list:list[list], columns_to_insert:tuple[int]):
    pass

def main():
    row_list = read_csv("Dataset\\olist_customers_dataset.csv", 5)
    reduced_entries = reduce_to_columns(row_list, [0,4])
    print(reduced_entries)
main()