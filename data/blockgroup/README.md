# Census Block Group

U.S census block group shape files. The combined blockgroup shapefile will be generated without the population density values, while the combined blockgroup shapefile with the population density values will be within [`\data\blockgroup\processed\`](\processed\README.md).

## Access

To allow users to focus on working with the models, a subset of data available from Census API has been downloaded for users. Through this approach users gain easy access to relevant data without needing to learn the intricacies of the Census Bureau’s all-inclusive API. In compliance with their terms of service, the US Census Bureau has been identified as the source, the data values have not been modified in anyway, a link to the Census Bureau’s terms of service has been provided, and a link to the original source API has been provided so updates may be downloaded when the Bureau makes them available. For more details, please refer to the [U.S. Census Bureau Terms of Service Agreement](https://www.census.gov/data/developers/about/terms-of-service.html).

### Default

This repo already contains processed U.S. Census population density data for 2019.

### Manual

If different or updated census data is desired, the data can be downloaded manually:

1. Sign up for a U.S. Census [API key](https://api.census.gov/data/key_signup.html)
2. Copy key contents to `API.txt`, found in the root directory of this repository
3. Process the data using a python script, ```bash python python/block_group_process.py ```

## Distribution Statement

© 2020 Massachusetts Institute of Technology.

This material is based upon work supported by the Federal Aviation Administration under Air Force Contract No. FA8702-15-D-0001.

Delivered to the U.S. Government with Unlimited Rights, as defined in DFARS Part 252.227-7013 or 7014 (Feb 2014). Notwithstanding any copyright notice, U.S. Government rights in this work are defined by DFARS 252.227-7013 or DFARS 252.227-7014 as detailed above. Use of this work other than as specifically authorized by the U.S. Government may violate any copyrights that exist in this work.

Any opinions, findings, conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the Federal Aviation Administration.

This document is derived from work done for the FAA (and possibly others), it is not the direct product of work done for the FAA. The information provided herein may include content supplied by third parties.  Although the data and information contained herein has been produced or processed from sources believed to be reliable, the Federal Aviation Administration makes no warranty, expressed or implied, regarding the accuracy, adequacy, completeness, legality, reliability or usefulness of any information, conclusions or recommendations provided herein. Distribution of the information contained herein does not constitute an endorsement or warranty of the data or information provided herein by the Federal Aviation Administration or the U.S. Department of Transportation.  Neither the Federal Aviation Administration nor the U.S. Department of Transportation shall be held liable for any improper or incorrect use of the information contained herein and assumes no responsibility for anyone’s use of the information. The Federal Aviation Administration and U.S. Department of Transportation shall not be liable for any claim for any loss, harm, or other damages arising from access to or use of data or information, including without limitation any direct, indirect, incidental, exemplary, special or consequential damages, even if advised of the possibility of such damages. The Federal Aviation Administration shall not be liable to anyone for any decision made or action taken, or not taken, in reliance on the information contained herein.

<!--  https://www.census.gov/data/developers/about/terms-of-service.html -->
This product uses the Census Bureau Data API but is not endorsed or certified by the Census Bureau.
