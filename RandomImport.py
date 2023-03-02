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

def read_csv(filename, row_count):
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

def main():
    print(read_csv("Dataset\\olist_customers_dataset.csv", 5))

main()