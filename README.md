# 2021 Census Data
Data from the 2021 Australian census

This project makes use of code to transform data between different geographies which can be found [here](https://github.com/jaketclarke/geography-weighter/)

# Victorian Districts

## Just give me the data

If you are looking for census data by 2022 Victorian Districts, click [here](https://github.com/jaketclarke/census-2021/tree/main/census-data-sed-victoria)

If you want to know more about it and or repeat the calculation, read below.

## Notes

The output data includes four files for each table, e.g `2021Census_G01_AUST_SA1.csv`

|Filename pattern | Description |
|--|--|
|2021Census_G01_VIC_SED_2022.csv | Contains a calculation for the number of census respondents in the seat, and a proportion based on the total column for the given table. Numbers suffixed with _n, proportions with _pc, e.g `Tot_P_M_n` and `Tot_P_M_pc` |
|2021Census_G01_VIC_SED_2022_n.csv | Contains just the numeric calculation |
|2021Census_G01_VIC_SED_2022_n.csv | Contains just the proportion calculation |
|2021Census_G01_VIC_SED_2022_unpivot.csv | Contains both the numeric and proportional version, unpivoted for machine readability |

The total column for each table and any appropriate caveats are described in `total_columns_2021.ods`

## How to repeat

1. Download geography-weighter [here](https://github.com/jaketclarke/geography-weighter/) and follow the steps in that repo to get it up and running.c

2. Clone this repo & get started with `pipenv install`. If this fails ensure you have pip installed (e.g `sudo apt-get install pip`).

3. Download the census data into the census-data directory, e.g:

```bash
wget https://www.abs.gov.au/census/find-census-data/datapacks/download/2021_GCP_all_for_AUS_short-header.zip
7za x 2021_GCP_all_for_AUS_short-header
cd 2021\ Census\ GCP\ All\ Geographies\ for\ AUS/
mv * ../census-data/
cd ..
rm -r 2021\ Census\ GCP\ All\ Geographies\ for\ AUS/
rm 2021_GCP_all_for_AUS_short-header.zip
```

4. run `pipenv run python sed-victoria.py`, to create the files you need for weighting in `census-data-sed-victoria-input/`. This script will create subdirectories for each different total column containing the tables that have that total column name, and will combine separated files (e.g 4a and 4b into a 4) so that all data is paired with its total column

5. run these files in the geography weighter, and copy the output back to `census-data-sed-victoria/`