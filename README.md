# 2021 Census Data
Data from the 2021 Australian census

This project makes use of code to transform data between different geographies which can be found [here](https://github.com/jaketclarke/geography-weighter/)

# Victorian Districts

If you are looking for census data by 2022 Victorian Districts, click (here)[https://github.com/jaketclarke/census-2021/census-data-sed-victoria]

The sed-victoria directory includes files calculated for the districts which will be used for the 2022 election.

# To repeat this work

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

4.