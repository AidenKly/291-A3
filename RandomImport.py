import csv
# Inserts data from a given csv file into a given sql table.

def get_db_info():
    database_name = input("Enter a Database filename. >> ")
    table_name = input("Enter the name of the table to be inserted into. >> ")

    csv_filename = input("Enter a csv filename. >> ")
    column_map = {}
    column_map_str = input("Enter the name of a column in the csv file then '':'' then the name of a column in the database table.\n \
                           Multiple entries are supported if they are seperated by a comma.")
    
    ','.split

def read_csv(filename):
    with open(filename, 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)
        columns = next(csvreader)
    