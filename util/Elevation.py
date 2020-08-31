# Copyright 2020, MIT Lincoln Laboratory
# SPDX-License-Identifier: BSD-2-Clause
import requests
import urllib

# Session object for querying Elevation API. Predefining results in faster query.
sess = requests.Session()


def make_remote_request(url, params):
    """
    Continually makes requests to the url until response is recieved.


    Parameters:
    -----------
    url {string}: url to connect to.
    params {dict}: dictionary containing url specific parameters (i.e. lat,lon)


    Returns:
    --------
    response {object}: Response from the API call. A request is attemped for up to 500 tries.


    """

    response = None
    count = 1
    while True:
        try:
            response = sess.get((url + urllib.parse.urlencode(params))).json()['USGS_Elevation_Point_Query_Service']['Elevation_Query']['Elevation']
        except:
            count += 1
            continue
        break



    return response



def getElevation(x):

    """
    Retrieves the elevation from the USGS 3DEP API at a given point, x.


    Parameters:
    -----------
    x {list}: list [x,y] containing the x (lon) and y (lat) coordinates.


    Returns:
    --------
    result {string}: Elevation for a given lon,lat point.


    """

    url = 'https://nationalmap.gov/epqs/pqs.php?'
    params = {'x': x[0],
              'y': x[1],
              'units': 'feet',
              'output': 'json'}

    result = make_remote_request(url,params)

    if result is None:
        return '-1000000'
    else:
        return result
