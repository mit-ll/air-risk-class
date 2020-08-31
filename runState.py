# Copyright 2020, MIT Lincoln Laboratory
# SPDX-License-Identifier: BSD-2-Clause
import os
import geopandas
import numpy as np
from p_tqdm import p_map
from util.AirspaceRiskClassification import *
import argparse
import pathlib
from shapely.vectorized import contains



# specify your path to the em-core repository
try:
    path_to_emcore = os.environ['AEM_DIR_CORE']
except:
    print("PATH TO EMCORE NOT FOUND")
    path_to_emcore = input("Input path to em-core: (i.e ~/path/to/em-core) ")

########################################################################################################
########################################################################################################
########################################################################################################
########################################################################################################

parser = argparse.ArgumentParser(description='Classify airspace risk for input state')
parser.add_argument('state', type=str,default='NC',
                    help='a state for processing')
parser.add_argument('spacing', type=float,default=0.1,
                    help='longitude/latitude degree spacing')
parser.add_argument('alt_ft_agl', type=float,default=500,
                    help='altitude to run airspace risk classification')


args = parser.parse_args()

### This code is showing lon/lat grid spaced by 0.1 degree for demonstration
### Change to 0.02 for 1-1.2 nm grid
SPACING_deg = float(args.spacing)
STATE = args.state.upper()
ALTITUDE = args.alt_ft_agl

# checking to see if path to results already exists, if not then creating it
if not os.path.exists('output/states/{}/alt_{}/spacing_{}'.format(STATE,ALTITUDE,SPACING_deg)):
    pathlib.Path("output/states/{}/alt_{}/spacing_{}".format(STATE,ALTITUDE,SPACING_deg)).mkdir(parents=True, exist_ok=True)


# reading in airport data
ap = geopandas.read_file('{}/data/FAA-Airports/e0bf64fc-79a3-49bc-9659-ea3f9fe875b52020328-1-157xrfq.2z5h.dbf'.format(path_to_emcore))

## airspace classes
airspace = geopandas.read_file('{}/data/FAA-NASR/Class_Airspace.dbf'.format(path_to_emcore))


## state shape file
# reading from the em-core repository
states_df = geopandas.read_file('{}/data/NE-Adminstrative/ne_10m_admin_1_states_provinces.dbf'.format(path_to_emcore))
states_df = states_df.loc[states_df.iso_a2 == 'US']  ## only want to obtain US states
states_df.loc[:,'iso_3166_2'] = states_df.loc[:,'iso_3166_2'].apply(lambda x: x[3:]) ## slicing off 'US' from 'US-state'
states_df.loc[:,'fips'] = states_df.loc[:,'fips'].apply(lambda x: x[2:]) ## slicing off 'US' from 'USfips'


## preprocessed census block group shape file
bg_df = geopandas.read_file('data/blockgroup/processed/BG.dbf')




class Data:
    def __init__(self,bg_df,airspace,ap,states_df):
        self.bg_df = bg_df
        self.airspace = airspace
        self.ap = ap
        self.states_df = states_df

data = Data(bg_df,airspace,ap,states_df)

# freeing up memory since these dataframes are now contained in the class
del bg_df
del airspace
del ap


### Need this function here for global "poly" variable

def point_in(point):
    return point.within(poly)



# grabbing state polygon
state = states_df.loc[states_df.iso_3166_2 == STATE]
poly,points = generate_grid_in_polygon(SPACING_deg, state)  # generating lon,lat meshgrid

# lon/lat points corresponding to STATE
lonlats = np.array(getLatLons(points[0],points[1])) # converting the meshgrid to a list of lon/lat points.


# The points may not all be within STATE due to the linearity of numpy meshgrid.
# We now can trim off the points that do not fall withing the state boundary

print('Checking to make sure points are withing the state boundary...')
ind2keep = contains(poly,lonlats[:,0],lonlats[:,1])


lonlats = lonlats[ind2keep == 1] ## Note: if ind2keep is a BOOLEAN array then " == 1" is optional

# This is an array of shapely points
points = np.array([Point(x,y) for x,y in lonlats],dtype=object)

df,lr_df = RiskClassification(lonlats,data,alt_ft_agl=ALTITUDE,points=points)

# saving results
df.to_file('output/states/{}/alt_{}/spacing_{}/RiskClass.shp'.format(STATE,ALTITUDE,SPACING_deg))
df.to_file('output/states/{}/alt_{}/spacing_{}/LowRiskClass.shp'.format(STATE,ALTITUDE,SPACING_deg))
