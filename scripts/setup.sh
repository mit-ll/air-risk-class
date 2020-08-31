#!/bin/sh
# Copyright 2020, MIT Lincoln Laboratory
# SPDX-License-Identifier: BSD-2-Clause

# grabbing census block group shapelines
wget -r -P ../data/blockgroup/raw -l1 -H -t 5 -nd -N -np -A .zip -erobots=off https://www2.census.gov/geo/tiger/TIGER2019/BG/

# now unzip the files and moving them to a new location
unzip ../data/blockgroup/raw/*\*.zip -d ../data/blockgroup/raw/

# Running python script to combine individual shape files to one file
python python/combineBG.py

# adding on the density values to the single file
python python/addDensity.py
