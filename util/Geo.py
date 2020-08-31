# Copyright 2020, MIT Lincoln Laboratory
# SPDX-License-Identifier: BSD-2-Clause
from shapely.ops import cascaded_union
from geopy.distance import distance
import numpy as np
import numba as nb
from scipy.spatial import cKDTree

def generate_grid_in_polygon(spacing, polygon):
    """
    Generates evenly spaced points within a given polygon.


    Parameters:
    -----------
    spacing {float}: distance between the points in coordinate units.
    polygon {geo dataframe}: input geometry to generate points within.


    Returns:
    --------
    poly_in {geo dataframe}: combined shapely geometry.
    meshgrid {array}: x,y coordinates.


    """

    # Convert the GeoDataFrame to a single polygon
    poly_in = cascaded_union([poly for poly in polygon.geometry])

    # Get the bounds of the polygon
    minx, miny, maxx, maxy = poly_in.bounds

    # Now generate the entire grid
    x_coords = list(np.arange(np.floor(minx), int(np.ceil(maxx)), spacing))
    y_coords = list(np.arange(np.floor(miny), int(np.ceil(maxy)), spacing))

    return poly_in,np.meshgrid(x_coords, y_coords)



@nb.njit()
def getLatLons(xcoord,ycoord):
    """
    Returns a list of lon/lats for an input meshgrid.


    Parameters:
    -----------
    meshgrid {array}: meshgrid of lon/lat points.


    Returns:
    --------
    lonlats {list}: A list of lon/lat coordinates.


    """
    lonlats = []

    for x in zip(xcoord.flatten(), ycoord.flatten()):
        lonlats.append(x)


    return lonlats


### fast closest airport function
def ckdnearest(gdA, gdB):
    """
    A fast nearest neighbor approach for finding the closest airport.


    Parameters:
    -----------
    gdA {geo dataframe}: dataframe containing geometry of a given lon/lat point.
    gdB {geo dataframe}: dataframe containing the geometry of all aerodromes.


    Returns:
    --------
    min_airports {geo dataframe}: dataframe of the geometry for the closest airport.


    Notes:
    --------
    For more information regarding the approach used,
    see https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.cKDTree.html


    """

    nA = np.array(list(zip(gdA.geometry.x, gdA.geometry.y)) )
    nB = np.array(list(zip(gdB.geometry.x, gdB.geometry.y)) )
    btree = cKDTree(nB)
    dist, idx = btree.query(nA, k=1)

    min_airports = gdB.loc[idx,'geometry'].reset_index(drop=True)

    return min_airports



def calc_distance(lat1,lon1,lat2,lon2):
    """
    A helper function used to calculate the distance between two lat/lon points.


    Parameters:
    -----------
    lat1 {float}: latitude of first point in degrees.
    lon1 {float}: longitude of first point in degrees.
    lat2 {float}: latitude of second point in degrees.
    lon2 {float}: longitude of second point in degrees.


    Returns:
    --------
    distance {float}: distance between two lat/lon points in nautical miles.


    """
    return distance((lat1,lon1),(lat2,lon2)).nm
