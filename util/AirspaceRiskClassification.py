# Copyright 2020, MIT Lincoln Laboratory
# SPDX-License-Identifier: BSD-2-Clause
import geopandas
import numpy as np
from util.Geo import *
from util.Elevation import *
from util.Low_Risk import *
from util.Medium_Risk import *

def RiskClassification(lonlats_deg,data,alt_ft_agl=500,points=None):
    '''
    Determines the risk class for a given longitude, latitude, and altitude. Brings
    together the Low risk and Medium Risk functions.


    Parameters:
    -----------
    lonlats {array}: (lon,lat) array of input points.
    data {class}: class object containing referenced data.
    alt {int, float, or array}: altitude for lon lat points. If int/float specified, this altitude will be applied to all lon/lat points. If array is provided it must be the same shape as lonlats.
    points {array}: (optional) array of shapely points. If not specified will be automatically created.

    Returns:
    --------
    df {geo dataframe}: dataframe containing classified lonlat,altitude points in High Risk, Medium Risk, and Low Risk.
    lr_df {geo dataframe}: dataframe containing classified lonlat,altitude points in only Low Risk/ Not Low Risk.

    '''

    # creating an empty status array. This will hold information as to why points are classified a particular class.
    status = np.empty(len(lonlats_deg),dtype=object)

    # Running Low Risk Airspace function
    low_risk,status = Low_Risk_Airspace(lonlats_deg,data,status,alt_ft_agl=alt_ft_agl,points=points)
    print("Finished Low Risk Airspace Check...")
    print("Starting Medium Risk Airspace Check...")

    # combining the point geometries with the low risk output as a new column
    combine_points_lr = np.append(points.reshape(-1,1),low_risk.reshape(-1,1),axis=1)
    combine_status = np.append(combine_points_lr,status.reshape(-1,1),axis=1)

    # creating the low risk dataframe
    lr_df = geopandas.GeoDataFrame(combine_status,columns=['geometry','Risk_Class','Status'])

    # Now creating a column with more explicit definitions for Risk Class
    # For example, Risk Class == 0 represents Not LR airspace
    lr_df.loc[lr_df.Risk_Class == 0,'Type'] = 'Not LR'
    lr_df.loc[lr_df.Risk_Class == 1,'Type'] = 'LR'

    # Now lr_df is a dataframe that has the following columns: [geometry, Risk_Class, Status, Type]



    # We only need to check the medium risk critera for points that failed the low risk critera
    sub_lonlats = lonlats_deg[low_risk == 0]
    sub_points = points[low_risk == 0]
    sub_status = status[low_risk == 0]


    if np.size(alt_ft_agl) == 1:
        sub_alt_ft_agl = alt_ft_agl
    else:
        sub_alt_ft_agl = alt_ft_agl[low_risk == 0]


    # Running Medium Risk Airspace function
    med_risk,sub_status = Medium_Risk_Airspace(sub_lonlats,data,sub_status,alt_ft_agl=sub_alt_ft_agl,points=sub_points)


    idx = np.arange(len(low_risk))
    idx_lr = idx[low_risk == 1]


    med_risk[med_risk == 0] = 2
    status[low_risk == 0] = sub_status
    low_risk[low_risk == 0] = med_risk
    low_risk[idx_lr] = 0


    combine_points_lr = np.append(points.reshape(-1,1),low_risk.reshape(-1,1),axis=1)
    combine_status = np.append(combine_points_lr,status.reshape(-1,1),axis=1)

    df = geopandas.GeoDataFrame(combine_status,columns=['geometry','Risk_Class','Status'])

    df.loc[df.Risk_Class == 0,'Type'] = 'LR'
    df.loc[df.Risk_Class == 1,'Type'] = 'MR'
    df.loc[df.Risk_Class == 2,'Type'] = 'HR'


    return df,lr_df
