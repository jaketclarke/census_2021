from utils.functions import log, make_directorytree_if_not_exists
import os
import shutil
import pandas as pd
import functools as ft
import numpy as np

def get_source_table(tableid):
    return f'census-data{os.sep}SA1{os.sep}AUS{os.sep}2021Census_{tableid}_AUST_SA1.csv'

### The tables with P_Tot_Tot as the proportion
def get_destination_table(tableid, total_name):
    
    output_path = 'census-data-sed-victoria-input'
    # ToDo if I make this generic, move this to overrideable on startup of a class instance
    # its annoying to repeat it over and over
    # total_name = 'P_Tot_Tot'

    make_directorytree_if_not_exists(output_path)
    make_directorytree_if_not_exists(output_path + os.sep + total_name)

    return f'{output_path}{os.sep}{total_name}{os.sep}2021Census_{tableid}_AUST_SA1.csv'

# helper util to copy files
def copy_files(tableid, total_name):
    source = get_source_table(tableid)
    destination = get_destination_table(tableid, total_name)
    shutil.copyfile(source, destination)

# merge multiple tables
def combine_tables(tableids, total_name):
    # get the combined table name eg G09 from G09A
    tableid = tableids[0][:-1]
    print(f'starting table {tableid}')
    
    # get all dataframes in a list
    dataframes = []
    for id in tableids:
        path = get_source_table(id)
        data = pd.read_csv(path)
        dataframes.append(data)

    # merge together on sa1 column
    merge = ft.reduce(lambda left, right: pd.merge(left, right, on='SA1_CODE_2021'), dataframes)

    # some of the dataframes contain '..'
    # will check with abs but assume this means data not provided on small columns (e.g, M_Ptn_in_RM_0_14 in 27a)
    # replacing with nan
    merge.replace({'..': np.nan}, regex=True, inplace=True)

    merge.to_csv(get_destination_table(tableid, total_name), index=False, na_rep='NaN') #na_rep preserves the nan in csv dump

    print(f'output table {tableid}\r\n')

# check if we have the data
if not os.path.exists(f'census-data{os.sep}SA1{os.sep}AUS{os.sep}'):
    print('The census folders don\'t exist yet')

if not os.path.exists(f'census-data{os.sep}SA1{os.sep}AUS{os.sep}2021Census_G01_AUST_SA1.csv'):
    print('The census folder is likely empty')

# tables with P_Tot_Tot as proportions
total_name = 'P_Tot_Tot'

# single tables we just need to copy
for tableid in (['G05','G18','G22','G23','G25']):
    copy_files(tableid, total_name)
    print(f'output table {tableid}\r\n')

# tables split across multiple files
# we combine together so the weighter has the denominator columnn for all of them
combine_tables(['G09A', 'G09B', 'G09C', 'G09D', 'G09E', 'G09F', 'G09G', 'G09H'], total_name)
combine_tables(['G13A', 'G13B', 'G13C', 'G13D', 'G13E'], total_name)
combine_tables(['G16A', 'G16B'], total_name)
combine_tables(['G17A', 'G17B', 'G17C'], total_name)
combine_tables(['G19A', 'G19B', 'G19C'], total_name)
combine_tables(['G20A', 'G20B'], total_name)
combine_tables(['G27A', 'G27B'], total_name)


# tables with P_Tot_Tot as proportions
total_name = 'P_Tot_Total'

# single tables we just need to copy
for tableid in (['G06']):
    copy_files(tableid, total_name)
    print(f'output table {tableid}\r\n')

# tables split across multiple files
# we combine together so the weighter has the denominator columnn for all of them
combine_tables(['G24A', 'G24B'], total_name)
combine_tables(['G26A', 'G26B'], total_name)
