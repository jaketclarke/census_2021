from platform import java_ver
from utils.functions import log, make_directorytree_if_not_exists, get_files_in_directory
import os
import os.path
import shutil
import pandas as pd
import functools as ft
import numpy as np

# combine all unpivoted data into one file
dir = 'census-data-sed-victoria'
make_directorytree_if_not_exists( f'{dir}{os.sep}summary')
unpivot_merge_filepath = f'{dir}{os.sep}summary{os.sep}2021Census_VIC_SED_2022_unpivoted.csv'

df = pd.DataFrame()
# if file does not exist, create
if not os.path.isfile(unpivot_merge_filepath):
    # for each unpivoted file (not ranks), combine
    for file in get_files_in_directory(dir, suffix=".csv"):
        if 'unpivoted.csv' in file and 'ranked' not in file:
            # get data
            infile = pd.read_csv(f'{dir}{os.sep}{file}', na_values=['Null','NaN','nan','Nan'])
            # find table from name eg G01
            table = file[file.find("G"):file.find("G")+3]
            infile['table'] = table

            if df.empty:
                df = infile
            else:
                df = pd.concat([df, infile], ignore_index=True)

    # reshape and order
    df_unpivot_all = df[['table','census_variable','district','value']].sort_values(['table','census_variable','district'])
    df_unpivot_all.to_csv(unpivot_merge_filepath, index=False, na_rep="Null")
    print(df_unpivot_all)

df = pd.read_csv(unpivot_merge_filepath, na_values=['Null','NaN','nan','Nan'])
pivot = df.pivot(index='district', columns=['table', 'census_variable'], values='value')
pivot.to_csv( f'{dir}{os.sep}summary{os.sep}2021Census_VIC_SED_2022.csv', na_rep="Null")

# # repivot
# transform = pd.pivot_table(data=df, index=['table','census_variable'])
# transform = transform.reset_index()
# transform.to_csv( f'{path}{os.sep}summary{os.sep}foo.csv')

# #ToDo - make sure we remove ranks for any question where sum(question)<2