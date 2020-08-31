# Copyright 2020, MIT Lincoln Laboratory
# SPDX-License-Identifier: BSD-2-Clause

import geopandas as gpd
import pandas as pd
import glob

########################################################################################################
###
###  Combining individual census block group shape files into one.
###
########################################################################################################


fp = glob.glob('../data/blockgroup/raw/tl_*_*_bg.dbf')
df = gpd.GeoDataFrame()

# looping over files and appending them all together
for i in range(len(fp)):
    df = df.append(gpd.read_file(fp[i]))


df.to_file('../data/blockgroup/BG.shp')
