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
    # deal with .. in place of NaN in census data 
    df = pd.read_csv(source)
    df.replace({'..': np.nan}, regex=True, inplace=True)
    path = get_destination_table(tableid, total_name)
    df.to_csv(path, index=False, na_rep='Null')

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
# we combine together so the weighter has the denominator column for all of them
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
# we combine together so the weighter has the denominator column for all of them
combine_tables(['G24A', 'G24B'], total_name)
combine_tables(['G26A', 'G26B'], total_name)

# tables with T_T_T as proportions
total_name = 'T_T_T'

# tables split across multiple files
# we combine together so the weighter has the denominator column for all of them
combine_tables(['G11A', 'G11B', 'G11C', 'G11D'], total_name)

# tables with TCF_T_M_T as proportions
total_name = 'TCF_T_M_T'

# tables split across multiple files
# we combine together so the weighter has the denominator column for all of them
combine_tables(['G12A', 'G12B'], total_name)

# tables with Tot_Families as proportions
total_name = 'Tot_Families'

for tableid in (['G31']):
    copy_files(tableid, total_name)
    print(f'output table {tableid}\r\n')

# tables with Tot_P as proportions
total_name = 'Tot_P'

# single tables we just need to copy
for tableid in (['G14', 'G15']):
    copy_files(tableid, total_name)
    print(f'output table {tableid}\r\n')

# tables split across multiple files
# we combine together so the weighter has the denominator column for all of them
combine_tables(['G04A', 'G04B'], total_name)

# tables with Tot_P_P as proportions
total_name = 'Tot_P_P'

# single tables we just need to copy
for tableid in (['G01']):
    copy_files(tableid, total_name)
    print(f'output table {tableid}\r\n')

# tables with Tot_P_Tot_resp as proportions
total_name = 'Tot_P_Tot_resp'

# single tables we just need to copy
for tableid in (['G08']):
    copy_files(tableid, total_name)
    print(f'output table {tableid}\r\n')

# tables with Tot_Tot as proportions
total_name = 'Tot_Tot'

# single tables we just need to copy
for tableid in (['G30','G32','G33','G38','G39','G40','G42']):
    copy_files(tableid, total_name)
    print(f'output table {tableid}\r\n')

# tables split across multiple files
# we combine together so the weighter has the denominator column for all of them
combine_tables(['G10A', 'G10B', 'G10C'], total_name)

# tables with Tot_Tot as proportions
total_name = 'Tot_Tot_P'

# single tables we just need to copy
for tableid in (['G07']):
    copy_files(tableid, total_name)
    print(f'output table {tableid}\r\n')

# tables split across multiple files
# we combine together so the weighter has the denominator column for all of them
combine_tables(['G10A', 'G10B', 'G10C'], total_name)

# tables with Total_dwelings as proportions
total_name = 'Total_dwelings'

# single tables we just need to copy
for tableid in (['G34']):
    copy_files(tableid, total_name)
    print(f'output table {tableid}\r\n')

# tables with Total_P as proportions
total_name = 'Total_P'

# single tables we just need to copy
for tableid in (['G29']):
    copy_files(tableid, total_name)
    print(f'output table {tableid}\r\n')

# tables with Total_Total as proportions
total_name = 'Total_Total'

# single tables we just need to copy
# for tableid in (['G03','G28','G35','G37','G41']):
for tableid in (['G35']):
    copy_files(tableid, total_name)
    print(f'output table {tableid}\r\n')
