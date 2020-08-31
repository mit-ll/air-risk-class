# Util

Default directory for python `.py` utilities. The `.py` files here represent all functions used to determine airspace risk class after preprocessing.

| Code        |  Description |
| :-------------| :--  |
|`AirspaceRiskClassification.py` | Contains function: `RiskClassification`. This function ties together the low risk criteria and medium risk criteria to provide an overall assessment as to what risk class a particular (lon, lat, alt) point belongs to. |
|`Low_Risk.py` | Contains functions: `Low_Risk_Airspace` and `checkLowRiskAirspace`. These functions contain the logic to determine if a (lon, lat, alt) point belongs to low risk airspace or not.  |
|`Medium_Risk.py` | Contains functions: `Medium_Risk_Airspace` and `checkMedRiskAirspace`. These functions contain the logic to determine if a (lon, lat, alt) point belongs to medium risk airspace or high risk airspace.  |
|`Geo.py` | Contains functions: `generate_grid_in_polygon`, `getLatLons`, `ckdnearest`, `calc_distance`. These geographic helper functions are used throughout `Low_Risk.py` and `Medium_Risk.py`. Function specific information can be found within `Geo.py`|
|`Elevation.py` | Contains functions: `make_remote_request`, `getElevation`. These API helper functions are used throughout `Low_Risk.py` and `Medium_Risk.py` to obtain the elevation for a given (lon, lat) point by querying the [USGS Elevation Point Query Service](https://nationalmap.gov/epqs/). Function specific information can be found within `Elevation.py`|



## Distribution Statement

© 2020 Massachusetts Institute of Technology.

This material is based upon work supported by the Federal Aviation Administration under Air Force Contract No. FA8702-15-D-0001.

Delivered to the U.S. Government with Unlimited Rights, as defined in DFARS Part 252.227-7013 or 7014 (Feb 2014). Notwithstanding any copyright notice, U.S. Government rights in this work are defined by DFARS 252.227-7013 or DFARS 252.227-7014 as detailed above. Use of this work other than as specifically authorized by the U.S. Government may violate any copyrights that exist in this work.

Any opinions, findings, conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the Federal Aviation Administration.

This document is derived from work done for the FAA (and possibly others), it is not the direct product of work done for the FAA. The information provided herein may include content supplied by third parties.  Although the data and information contained herein has been produced or processed from sources believed to be reliable, the Federal Aviation Administration makes no warranty, expressed or implied, regarding the accuracy, adequacy, completeness, legality, reliability or usefulness of any information, conclusions or recommendations provided herein. Distribution of the information contained herein does not constitute an endorsement or warranty of the data or information provided herein by the Federal Aviation Administration or the U.S. Department of Transportation.  Neither the Federal Aviation Administration nor the U.S. Department of Transportation shall be held liable for any improper or incorrect use of the information contained herein and assumes no responsibility for anyone’s use of the information. The Federal Aviation Administration and U.S. Department of Transportation shall not be liable for any claim for any loss, harm, or other damages arising from access to or use of data or information, including without limitation any direct, indirect, incidental, exemplary, special or consequential damages, even if advised of the possibility of such damages. The Federal Aviation Administration shall not be liable to anyone for any decision made or action taken, or not taken, in reliance on the information contained herein.
