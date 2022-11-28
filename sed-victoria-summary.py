from platform import java_ver
from utils.functions import log, make_directorytree_if_not_exists, get_files_in_directory
import os
import os.path
import shutil
import pandas as pd
import functools as ft
import numpy as np
from datetime import datetime

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

# create metadata summary table
metadata_input = f'census-data/Metadata_2021_GCP_DataPack_R1.xlsx'
metadata_output = f'{dir}{os.sep}summary{os.sep}2021Census_Metadata.csv'
if not os.path.isfile(metadata_output):
    df = pd.read_excel(metadata_input,
                       sheet_name = 'Cell Descriptors Information',
                       usecols='A:F',
                       skiprows=10)
    df.to_csv(metadata_output, index=False)

# format
pivot_districts_filepath_xlsx = pivot_districts_filepath.replace('.csv','.xlsx')
pivot_districts_filepath_xlsx_tab = 'data'
df = pd.read_csv(pivot_districts_filepath, na_values=['Null','NaN','nan','Nan'])
# xlsxwriter can't write nans
df = df.fillna('..')
# add long census var names to sheet
df_lookup = pd.read_csv(metadata_output)
df_lookup['table'] = df_lookup['DataPackfile'].str[:3]
df_lookup = df_lookup[['Short', 'Long', 'table']]
# take _pc off proportions
df['census_variable'] = df.census_variable.str.replace(r'_pc$', '', regex=True).str.strip()
# join
df = df.merge(df_lookup, how='left', left_on=['table', 'census_variable'], right_on=['table', 'Short'] )
# where the long label doesn't exist use the short
df['census_variable'] = df['Long'].fillna(df['census_variable'])
# get rid of redundant columns
df.drop(['Long','Short'], axis=1, inplace=True)

writer = pd.ExcelWriter(pivot_districts_filepath_xlsx, engine='xlsxwriter')

workbook = writer.book
worksheet = workbook.add_worksheet(pivot_districts_filepath_xlsx_tab)
global_format_options = {'align': 'center', 'font_name': 'Tahoma', 'font_size': 10}
percent_format = workbook.add_format(global_format_options | {'num_format': '0.0%'} )
number_format = workbook.add_format(global_format_options | {'num_format': '#,##0'})
header_format = workbook.add_format(global_format_options | {'bold': True})
global_format = workbook.add_format(global_format_options)
label_format = workbook.add_format({'align': 'right', 'font_name': 'Tahoma', 'font_size': 10})

rows = len(df)
for index, row in df.iterrows():
    needle = f'A{index+1}' # i.e index=0 returns A1
    if index == 0:
        cols = df.columns.tolist()
        worksheet.write_row('A1', cols, header_format)
        worksheet.set_row(index, 15)
    elif row['type'] == 'numeric':
        worksheet.set_row(index, 15, number_format)
        worksheet.write_row(needle, row)
    elif row['type'] == 'proportion':
        worksheet.set_row(index, 15, percent_format)
        worksheet.write_row(needle, row)
        # conditional formatting
        range = f'C{index+1}:CM{index+1}'# i.e index=1 returns C2:CM2
        worksheet.conditional_format(range, {'type': '3_color_scale'})
       
# set column widths
worksheet.set_column(0, 0, 10)
worksheet.set_column(1, 1, 75, label_format) # make census var column wider
worksheet.set_column(2, 91, 20)

worksheet.freeze_panes(1, 3)

worksheet.autofilter('A1:CM18063')

now = datetime.now()
now_formatted = now.strftime("%d/%m/%Y %H:%M:%S")

worksheet_attribution = workbook.add_worksheet('about')
attribution_format = workbook.add_format(global_format_options | {'align': 'right', 'font_name': 'Tahoma', 'font_size': 10} )

worksheet_attribution.write_row('A1', ['Data assembled by Jake Clarke'])
worksheet_attribution.write_row('A2', [f'Generated on {now_formatted}'])
worksheet_attribution.write_row('A3', [f'More information on the project can be found at:'])
worksheet_attribution.write_url('B3', 'https://github.com/jaketclarke/census-2021')
worksheet_attribution.write_row('A4', [f'The most up-to-date version of this spreadsheet can be found at:'])
worksheet_attribution.write_url('B4', 'https://github.com/jaketclarke/census-2021/blob/main/census-data-sed-victoria/summary/2021Census_VIC_SED_2022_long.xlsx')

worksheet_attribution.set_row(0, 15)
worksheet_attribution.set_row(1, 15)
worksheet_attribution.set_row(2, 15)
worksheet_attribution.set_row(3, 15)

worksheet_attribution.set_column(0, 0, 75, attribution_format)
worksheet_attribution.set_column(1, 1, 150, global_format)

workbook.read_only_recommended()
writer.save()