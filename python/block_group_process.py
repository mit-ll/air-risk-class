# Copyright 2020, MIT Lincoln Laboratory
# SPDX-License-Identifier: BSD-2-Clause
# This product uses the Census Bureau Data API but is not endorsed or certified by the Census Bureau.

## Import python modules
import geopandas
import numpy as np
import requests
import urllib
from us import states
import time
from p_tqdm import p_map

#loading census api key
census_api = str(np.loadtxt('../API.txt',dtype=str))

# creating session object to query API
s = requests.Session()

print('loading data...')

# reading in the single block group shape file
bg_df = geopandas.read_file('../data/blockgroup/BG.dbf')

print('data loaded!')


def getDensity(bg,tract,county,state,aland,awater):
    '''
    Given a (lon,lat) shapely point, determines what census BG this point belongs to and the corresponding population density.


    Parameters:
    -----------
    point {shapely obj}: (lon,lat) shapely point
    config {class}: class object containing config hyperparameters.


    Returns:
    --------
    density {float}: population density for a census block group.


    '''

    # area of land/ area of water in census block group
    aland = float(aland)
    awater = float(awater)


    # base URL to query census API
    base_url = 'https://api.census.gov/data/2018/acs/acs5?get=B01003_001E&for=block%20group:{}&in=state:{}%20county:{}%20tract:{}'.format(bg,state,county,tract)
    response = None

    # this loop will try to connect to the census API and grab data up to 250 times before breaking out

    count = 0
    while True:
        try:
            data_url = f'{base_url}&key={census_api}'
            response=s.get(data_url).json()
        except:
            time.sleep(0.01)
            count += 1
            if count == 250:
                response = None
                break
            continue


        break

    if response == None:
        return np.nan

    total_pop = int(response[1][0])

    # area is in square meters. Need to convert to square miles
    area = (aland + awater)*0.00000038610215855

    density = total_pop/area

    return density

bg_df['density'] = p_map(getDensity, bg_df['BLKGRPCE'],bg_df['TRACTCE'],bg_df['COUNTYFP'],bg_df['STATEFP'],bg_df['ALAND'],bg_df['AWATER'])

# saving off snapshot so that the density values can be reused next time without API
sub_df = bg_df.loc[:,['STATEFP','COUNTYFP','TRACTCE',"BLKGRPCE","density"]]
sub_df.to_csv('../data/blockgroup/processed/density_values.csv',index=False)

print('Finished Processing')

# saving processed dataframe
bg_df.to_file("../data/blockgroup/processed/bg.shp")
