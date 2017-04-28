# Faraday is a tool for transforming csv files
import sys, os
sys.path.insert(0, os.path.abspath('..'))

import csv
import os
import geocivics_assets
import shutil
import xform_schema

# input
DATA_PATH = '/home/jgp/geocivics/srproj/data'
data_files = os.listdir(DATA_PATH)
data_paths = [os.path.join(DATA_PATH, x) for x in data_files]

# output
XFORM_PATH = '/home/jgp/geocivics/faraday/xform'
xform_paths = [os.path.join(XFORM_PATH, x) for x in data_files]

def apply_transformation(header, csv_path, xform):
    """
    Applies a Transformation to each row of a csv file.
    """
    temp_path = csv_path + '.tmp'
    with open(temp_path, 'w') as wf:
        wf.truncate()
        with open(csv_path, 'r') as rf:
            for row in rf:
                row_list = row.split(',')
                new_value = xform.funct(header, row)
                new_row = row.rstrip() + ',' + new_value + '\n'
                wf.write(new_row)
    shutil.copyfile(temp_path, csv_path)
    os.remove(temp_path)

def pre_process(csvpath, to_path):
    """
    Remove the first row (headers) from a csv 
    Replace "PrivacySupressed" with "NULL"
    """
    print("removing first row from ", csvpath)
    line = None
    tmp = csvpath + '.tmp'
    trimmed = False
    with open(csvpath, 'r') as rf:
        with open(tmp, 'w') as wf:
            for l in rf:
                if not trimmed:
                    line = l
                    trimmed = True
                else:
                    row_l = l.split(',')
                    for i in range(len(row_l)):
                        if row_l[i] == "PrivacySuppressed":
                            row_l[i] = ""
                    wf.write(','.join([x for x in row_l]))
    print("line: ", line)
    shutil.copyfile(tmp, to_path)
    return line

def transform_assets(): 
    asset_list = geocivics_assets.get_assets()
    for asset in asset_list:
        print("asset: ", asset.filename)
        for xform in asset.transformations:
            asset.csvheader = pre_process(asset.data_path, asset.xform_path)
            # note that this now looks in xform path
            apply_transformation(asset.csvheader, asset.xform_path, xform)
        shutil.copyfile(asset.xform_path, asset.load_path)
if __name__ == '__main__':
    transform_assets()
