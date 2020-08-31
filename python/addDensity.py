# Copyright 2020, MIT Lincoln Laboratory
# SPDX-License-Identifier: BSD-2-Clause
import geopandas as gpd
import pandas as pd

########################################################################################################
####
#### Adds the population density values to a geopandas dataframe.
#### If you want to use newer density values, you will need to run the density process python script
####
########################################################################################################

# reading in single block group file and file of density values
df = gpd.read_file("../data/blockgroup/BG.dbf")
df2 = pd.read_csv("../data/blockgroup/processed/density_values.csv",dtype=object)

# now merging the files together on commen columns
df3 = pd.merge(df,df2,on=list(df2.columns[:-1]))

# assigning the density column to float instead of string
df3.loc[:,'density'] = df3.loc[:,'density'].astype(float)

# saving file
df3.to_file('../data/blockgroup/processed/BG.shp')
