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
unpivot_merge_filepath = f'{dir}{os.sep}summary{os.sep}2021Census_VIC_SED_2022_unpivoted_merged.csv'

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

pivot_questions_filepath = f'{dir}{os.sep}summary{os.sep}2021Census_VIC_SED_2022_wide_combined.csv'
if not os.path.isfile(pivot_questions_filepath):
    df = pd.read_csv(unpivot_merge_filepath, na_values=['Null','NaN','nan','Nan'])
    pivot = df.pivot(index='district', columns=['table', 'census_variable'], values='value')
    pivot.to_csv( pivot_questions_filepath, na_rep='Null')

pivot_districts_filepath_n = f'{dir}{os.sep}summary{os.sep}2021Census_VIC_SED_2022_long_n.csv'
if not os.path.isfile(pivot_districts_filepath_n):
    df = pd.read_csv(unpivot_merge_filepath, na_values=['Null','NaN','nan','Nan'])
    df = df[~df['census_variable'].str.endswith('_pc')]
    pivot = df.pivot(index=['table', 'census_variable'], columns='district', values='value')
    pivot.to_csv(pivot_districts_filepath_n, na_rep='Null')

pivot_districts_filepath_pc = f'{dir}{os.sep}summary{os.sep}2021Census_VIC_SED_2022_long_pc.csv'
if not os.path.isfile(pivot_districts_filepath_pc):
    df = pd.read_csv(unpivot_merge_filepath, na_values=['Null','NaN','nan','Nan'])
    df = df[df['census_variable'].str.endswith('_pc')]
    pivot = df.pivot(index=['table', 'census_variable'], columns='district', values='value')
    pivot.to_csv(pivot_districts_filepath_pc, na_rep='Null')

pivot_districts_filepath = f'{dir}{os.sep}summary{os.sep}2021Census_VIC_SED_2022_long.csv'
if not os.path.isfile(pivot_districts_filepath):
    dfp = pd.read_csv(pivot_districts_filepath_pc, na_values=['Null','NaN','nan','Nan'])
    dfn = pd.read_csv(pivot_districts_filepath_n, na_values=['Null','NaN','nan','Nan'])
    dfp['type'] = 'proportion'
    dfn['type'] = 'numeric'
    df = pd.concat([dfn, dfp], ignore_index=True)

    type = df.pop('type')
    df.insert(2, 'type', type)
    
    df = df.sort_values(['table', 'census_variable', 'type'])
    df.to_csv(pivot_districts_filepath, na_rep='Null', index=False)


# format
pivot_districts_filepath_xlsx = pivot_districts_filepath.replace('.csv','.xlsx')
pivot_districts_filepath_xlsx_tab = 'data'
df = pd.read_csv(pivot_districts_filepath, na_values=['Null','NaN','nan','Nan'])
#xlsxwriter can't write nans
df = df.fillna('..')
writer = pd.ExcelWriter(pivot_districts_filepath_xlsx, engine='xlsxwriter')
# df.to_excel(writer, sheet_name=pivot_districts_filepath_xlsx_tab, index=False)

workbook = writer.book
worksheet = workbook.add_worksheet(pivot_districts_filepath_xlsx_tab)
percent_format = workbook.add_format({'num_format': '0.0%'})
number_format = workbook.add_format({'num_format': '#,##0'})

rows = len(df)
for index, row in df.iterrows():
    needle = f'A{index+1}' # i.e index=0 returns A1
    worksheet.write_row(needle, row)
    if index == 0:
        cols = df.columns
        worksheet.write_row('A1', cols)
    elif index %2 == 0:
        worksheet.set_row(index, 15, number_format)
    else:
        worksheet.set_row(index, 15, percent_format)
    
writer.save()