# Copyright 2020, MIT Lincoln Laboratory
# SPDX-License-Identifier: BSD-2-Clause
import geopandas
from shapely.geometry import Point
import pandas as pd
import numpy as np
from p_tqdm import p_map
import time
from util.Geo import *
from util.Elevation import *

def Medium_Risk_Airspace(lonlats_deg,data,status=None,alt_ft_agl=500,points=None):
    ## --> Excessive global variable use should be avoided.
    ## --> Using two globals to speed up parallel processing
    global hierarchy
    global altitude_values

    """
    Determines if a given lon/lat coordinate is in medium risk airspace or not.


    Parameters:
    -----------
    lonlats_deg {array}: array of lon/lat points in degrees.
    data {class}: class containing relevant data for processing.
    status {array}: array of information for why a given latlon is has been characterized as a specific risk class.
    alt_ft_agl {float/int or array}: altitude for lon/lat points in AGL. Default is 500ft AGL.
    points {array}: (optional) array of shapely points for each input lon/lat.


    Returns:
    --------
    mr {array}: An array consisting of 1's (low risk) and 0's (not low risk) for each input lon/lat.


    Notes:
    --------
    See Main.ipynb for more information regarding the setup for input: [data].


    """

    bg_df,ap,airspace = data.bg_df,data.ap,data.airspace

    ## Checking to see if points are already provided
    if points is None:
        points = np.array([Point(x,y) for x,y in lonlats_deg],dtype=object)



    # Creating a geopandas dataframe with the array of shapely points
    df = geopandas.GeoDataFrame(points,columns=['geometry'])
    df.loc[:,'alt'] = alt_ft_agl


    # Pre-allocating
    mr = np.ones(len(lonlats_deg),dtype=int)
    idx = np.arange(len(lonlats_deg),dtype=int)

    if status is None:
        status = np.empty(len(lonlats_deg),dtype=object)


    # syncing up coordinate reference system (prevents warning)
    df.crs = bg_df.crs



    ### --------------------------------------------------------------------------------------------------------- ###
    ### Step 1: Check census block group density
    print("Step 1: Population Density Check")
    print("------------------------------------------------------------------------------")
    print("> Beginning check on {} points...".format(df.shape[0]))
    print(" ")

    start1 = time.time()
    density = geopandas.sjoin(df,bg_df,how='left',op='within') ## op='within' is faster than op='intersects'


    # violation of density

    ## indexing the mr array for where in the density dataframe the block group density is > 100
    ## density > 100 is not low risk airspace
    density_violation = density.loc[(density.alt >= 500) & (density.density >= 100),:].index
    mr[density_violation] = 0

    status[density_violation] = 'alt >= 500ft AGL over UA'

    end1 = time.time()
    print("> Finished! Time: {}s | Total Time: {}s".format(int(end1-start1),int(end1-start1)))
    print("> {} points violated population density criteria".format(density_violation.shape[0]))
    print("------------------------------------------------------------------------------")
    print("------------------------------------------------------------------------------")
    print(" ")


    del density_violation
    del density
    del bg_df

    ## if there are no more points to consider, break out of function
    if len(mr[mr==1]) == 0:
        return mr,status


    ### --------------------------------------------------------------------------------------------------------- ###



    ### --------------------------------------------------------------------------------------------------------- ###
    ### Step 2: Check distance to closest aerodrome

    # Only need to check further criteria for lonlats_deg where mr is not 0
    sub_idx = idx[mr == 1]
    sub_df = df.loc[mr == 1,:]
    sub_df.reset_index(inplace=True,drop=True)


    print("Step 2: Distance to Closest Aerodrome")
    print("------------------------------------------------------------------------------")
    print("> Beginning check on {} points...".format(sub_df.shape[0]))
    print(" ")

    start2 = time.time()

    min_ap = ckdnearest(sub_df,ap)

    d = np.array(p_map(calc_distance,sub_df.geometry.y,sub_df.geometry.x,min_ap.y,min_ap.x))

    min_ap_df = geopandas.GeoDataFrame(min_ap)
    min_ap_df.crs = airspace.crs
    airport_class = geopandas.sjoin(min_ap_df,airspace,how='left',op='within')
    airport_class.reset_index(inplace=True)
    airport_class.rename(columns={'index':'number'},inplace=True)

    index=pd.MultiIndex.from_arrays([airport_class.number,airport_class.index])
    airport_class = geopandas.GeoDataFrame(airport_class.values,index=index,columns = airport_class.columns)
    del airport_class['number']
    airport_class.LOWER_VAL = airport_class.LOWER_VAL.astype(float)


    classes = airport_class.groupby(level=0).CLASS.min()
    medium_risk_violation = sub_idx[((d < 5) & np.isin(classes,['E','F','G']) & (sub_df.alt >= 500))]
    mr[medium_risk_violation] = 0

    status[medium_risk_violation] = 'd_ap < 5, in class [E,F,G] and alt > 500ft AGL'


    medium_risk_violation = sub_idx[((d < 5) & np.isin(classes,['B','C','D']))]
    mr[medium_risk_violation] = 0
    status[medium_risk_violation] = 'd_ap < 5, in class [B,C,D]'


    end2 = time.time()

    print("> Finished! Time: {}s | Total Time: {}s".format(int(end2-start2),int(end2-start1)))
    print("> {} points violated distance to aerodrome criteria".format(medium_risk_violation.shape[0]))
    print("------------------------------------------------------------------------------")
    print("------------------------------------------------------------------------------")
    print(" ")

    del d
    del min_ap
    del min_ap_df
    del airport_class
    del classes
    del medium_risk_violation

    ## if there are no more points to consider, break out of function
    if len(mr[mr==1]) == 0:
        return mr,status


    ### --------------------------------------------------------------------------------------------------------- ###


    ### Step 3: Uncontrolled Airspace

    # Only need to check further criteria for lonlats_deg where mr is not 0
    sub_idx = idx[mr == 1]
    sub_df = df.loc[mr == 1,:]
    sub_df.reset_index(inplace=True,drop=True)


    print("Step 3: Uncontrolled Airspace")
    print("------------------------------------------------------------------------------")
    print("> Beginning check on {} points...".format(sub_df.shape[0]))
    print(" ")


    start3 = time.time()

    aspace_df = geopandas.sjoin(sub_df,airspace,how='left',op='within')
    aspace_df.reset_index(inplace=True)
    aspace_df.rename(columns={'index':'number'},inplace=True)

    index=pd.MultiIndex.from_arrays([aspace_df.number,aspace_df.index])
    hierarchy = geopandas.GeoDataFrame(aspace_df.values,index=index,columns = aspace_df.columns)

    del hierarchy['number']
    iter_index = np.unique(aspace_df.number)


    aspace = np.array(p_map(checkMedRiskAirspace,iter_index))
    airspace_violation = sub_idx[aspace == False]
    mr[airspace_violation] = 0

    status[airspace_violation] = 'alt >= 500ft AGL in [B,C,D,E] airspace'

    airspace_violation = sub_idx[aspace == 3]
    mr[airspace_violation] = 0
    status[airspace_violation] = 'Elevation API returned -1000000 (no elev.)'

    end3 = time.time()

    print("> Finished! Time: {}s | Total Time: {}s".format(int(end3-start3),int(end3-start1)))
    print("------------------------------------------------------------------------------")
    print("------------------------------------------------------------------------------")

    return mr,status



def checkMedRiskAirspace(iter_index):
    """
    Check the airspace corresponding to a lon/lat point to see if it is in the allowed critera for "Medium Risk".


    Parameters:
    -----------
    iter_index {int}: Integer for which index to grab lon/lat information from.


    Returns:
    --------
    True or False {Bool}: Whether or not the lon/lat point is in the allowed medium risk airspace.


    """

    allowed_controlled_airspace = ['B','C','D','E']

    aspace = hierarchy.loc[iter_index,:,:].copy()

    ## fixing high-altitude airspace value
    aspace.loc[aspace['UPPER_VAL'].astype(float) < 0,'UPPER_VAL'] = 6e4

    lat = float(aspace.geometry.values[0].y)
    lon = float(aspace.geometry.values[0].x)
    alt_ft_agl = float(aspace.alt.values[0])


    if not np.isin(aspace.LOWER_CODE,['SFC']).any() or not np.isin(aspace.UPPER_CODE,['SFC']).any():

        elevation_at_point = getElevation([lon,lat])
        if float(elevation_at_point) == -1000000:
            return 3

        aspace.loc[aspace.UPPER_CODE != 'SFC','UPPER_VAL'] = aspace.loc[aspace.UPPER_CODE != 'SFC','UPPER_VAL'].astype(float) - elevation_at_point
        aspace.loc[aspace.LOWER_CODE != 'SFC','LOWER_VAL'] = aspace.loc[aspace.LOWER_CODE != 'SFC','LOWER_VAL'].astype(float) - elevation_at_point

    class_airspace = aspace.loc[(aspace.UPPER_VAL.astype(float) >= alt_ft_agl) & (aspace.LOWER_VAL.astype(float) <= alt_ft_agl),:]

    if class_airspace.CLASS.values.size == 0:
        return True

    if np.isin(class_airspace.CLASS.values,allowed_controlled_airspace).all():
        if alt_ft_agl >= 500:
            return False

        else:
            return True
