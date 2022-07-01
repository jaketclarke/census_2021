from utils.functions import log, make_directorytree_if_not_exists
import os
import shutil
import pandas as pd
import functools as ft


# check if we have the data
if not os.path.exists('census-data/SA1/AUS/'):
    print('The census folders don\'t exist yet')

if not os.path.exists('census-data/SA1/AUS/2021Census_G01_AUST_SA1.csv'):
    print('The census folder is likely empty')

# parent output dir
make_directorytree_if_not_exists('census-data-sed-victoria-input')

def get_source_table(tableid):
    return f'census-data/SA1/AUS/2021Census_{tableid}_AUST_SA1.csv'

# helper util to copy files
def copy_files(tableid, destination):
    source = get_source_table(tableid)
    destination = f'{destination}/2021Census_{tableid}_AUST_SA1.csv'
    shutil.copyfile(source, destination)

# P_Tot_Tot
make_directorytree_if_not_exists('census-data-sed-victoria-input/P_Tot_Tot/')

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

print(len(dataframes))

# merge together on sa1 column
merge = ft.reduce(lambda left, right: pd.merge(left, right, on='SA1_CODE_2021'), dataframes)
merge.to_csv('test.csv', index=False)
# for tableid in tableids:

#     current_table_id = tableids.pop(0)

#     if merge_table.empty:
#         first_table_needle = get_source_table(current_table_id)
#         merge_table = pd.read_csv(first_table_needle)

#         second_table_id = tableids.pop(0)
#         second_table_needle = get_source_table(second_table_id)
#         second_table = pd.read_csv(second_table_needle)

#         merge_table.merge(second_table, left_on = 'SA1_CODE_2021', right_on = 'SA1_CODE_2021')

#         print("hello")
#         print(tableids)

#     else:
#         print('else')
#         print(current_table_id)
#         nth_table_needle = get_source_table(current_table_id)
#         nth_table = pd.read_csv(nth_table_needle)
#         merge_table.merge(nth_table, left_on = 'SA1_CODE_2021', right_on = 'SA1_CODE_2021')

#     i+=1

# merge_table.to_csv('09.csv', index=False)

# source = f'census-data/SA1/AUS/2021Census_{tableid}_AUST_SA1.csv'
# a = pd.read_csv(source)
# print(a)