from utils.functions import log, make_directorytree_if_not_exists
import os
import shutil
import pandas as pd
import functools as ft

def get_source_table(tableid):
    return f'census-data{os.sep}SA1{os.sep}AUS{os.sep}2021Census_{tableid}_AUST_SA1.csv'

# check if we have the data
if not os.path.exists(f'census-data{os.sep}SA1{os.sep}AUS{os.sep}'):
    print('The census folders don\'t exist yet')

if not os.path.exists(f'census-data{os.sep}SA1{os.sep}AUS{os.sep}2021Census_G01_AUST_SA1.csv'):
    print('The census folder is likely empty')

### The tables with P_Tot_Tot as the proportion
def get_destination_table(tableid):
    
    #ToDo if I make this generic, move this to overrideable on startup of a class instance
    output_path = 'census-data-sed-victoria-input'
    total_name = 'P_Tot_Tot'

    make_directorytree_if_not_exists(output_path)
    make_directorytree_if_not_exists(output_path + os.sep + total_name)

    return f'{output_path}{os.sep}{total_name}{os.sep}2021Census_{tableid}_AUST_SA1.csv'

# helper util to copy files
def copy_files(tableid, destination):
    source = get_source_table(tableid)
    destination = get_destination_table(tableid)
    shutil.copyfile(source, destination)

# copy single files
# for tableid in ('G05','G13','G16','G17','G18','G19','G20','G22','G23','G25','G27'
# ):
#     copy_files(tableid, 'census-data-sed-victoria-input/P_Tot_Tot/')

# combine doubles
# for tableid in ('G09A', 'G09B', 'G09C') # loop like this for ease later

# import pandas pandas. merge dedup sa1 column 

tableid='G09'
tableids = ['G09A', 'G09B', 'G09C', 'G09D', 'G09E', 'G09F', 'G09G', 'G09H']

# get all dataframes in a list
dataframes = []
for id in tableids:
    path = get_source_table(id)
    data = pd.read_csv(path)
    dataframes.append(data)

# merge together on sa1 column
merge = ft.reduce(lambda left, right: pd.merge(left, right, on='SA1_CODE_2021'), dataframes)
merge.to_csv(get_destination_table(tableid), index=False)
