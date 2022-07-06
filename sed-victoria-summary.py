from utils.functions import log, make_directorytree_if_not_exists, get_files_in_directory
import os
import shutil
import pandas as pd
import functools as ft
import numpy as np

# get unpivoted data
files = []
df = pd.DataFrame()
path = 'census-data-sed-victoria'
for file in get_files_in_directory(path, suffix=".csv"):
    if 'unpivoted.csv' in file and 'ranked' not in file:
        files.append(file)
        infile = pd.read_csv(f'census-data-sed-victoria{os.sep}{file}', na_values=['Null','NaN','nan','Nan'])
        table = file[file.find("G"):file.find("G")+3]
        infile['table'] = table

        if df.empty:
            df = infile
        else:
            df = pd.concat([df, infile], ignore_index=True)
    
make_directorytree_if_not_exists( f'{path}{os.sep}summary')
out_n = f'{path}{os.sep}summary{os.sep}2021Census_VIC_SED_2022_unpivoted.csv'
df.to_csv(out_n, index=False)

# make pivot

pivot = df.pivot(index='district', columns=['table', 'census_variable'], values='value')
pivot.to_csv( f'{path}{os.sep}summary{os.sep}2021Census_VIC_SED_2022.csv')

# repivot
transform = pd.pivot_table(data=df, index=['table','census_variable'])
transform = transform.reset_index()
transform.to_csv( f'{path}{os.sep}summary{os.sep}foo.csv')

#ToDo - make sure we remove ranks for any question where sum(question)<2