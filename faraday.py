# Faraday is a tool for transforming csv files

import csv
import os

# input
DATA_PATH = '/home/jgp/srproj/data'
data_files = os.listdir(DATA_PATH)
data_paths = [os.path.join(DATA_PATH, x) for x in data_files]

# output
XFORM_PATH = '/home/jgp/faraday/xform'
xform_paths = [os.path.join(XFORM_PATH, x) for x in data_files]


def add_column_to_csv(csvpath, writepath, func):
    """
    appends a value to the end of each row of a csv file
    that value is computed by func, a function that operates on the row
    """
    with open(csvpath, 'r') as csvfile:
        with open(writepath, 'w') as writefile:
            csvwriter = csv.writer(writefile, delimiter=',')
            for row in csvfile:
                row_list = row.split(',')
                new_value = func(row_list)
                print("New Value to add: ", new_value)
                csvwriter.writerow(row + ',' + new_value)
            
def read_from_csv_f(csvpath, writepath, func):
    """
    appends a value to the end of each row of a csv file
    that value is computed by func, a function that operates on the row
    """
    with open(csvpath, 'r') as csvfile:
        for row in csvfile:
            row_list = row.split(',')
            print("Row: ", row)
            new_value = func(row_list)
            print("New Value to add: ", new_value)
            
def funct(row):
    """
    operates on a row
    returns a value
    """
    return row[0]+row[1]


def remove_first_row(csvpath):
    """
    Remove the first row (headers) from a csv 
    """
    csvpath

for index, data_path in enumerate(data_paths):
    print("Processing: ", data_path)
    add_column_to_csv(data_path, xform_paths[0], funct)
