# Persistence Homology Application to Resource Coverage, a Case Study on Fire Stations
This README has two parts. First is an explanation of the scripts and data uploaded here. Second is a list of miscellaneous notes relevant to the project.

## Description of files
- `Fire_Stations.geojson` - File with coordinates of fire stations across the US. The data was originally downloaded  from https://hifld-geoplatform.opendata.arcgis.com/datasets/0ccaf0c53b794eb8ac3d3de6afdb3286_0/explore?location=34.186760%2C-119.122303%2C9.54 but I believe that the database has migrated

- `chicagoCensusBlocksWithNearestFireStationAndDistance` - File with all chicago census blocks matched with their nearest fire stations and the distance to that closest fire station. The census block data was downloaded from https://hub.arcgis.com/datasets/d795eaa6ee7a40bdb2efeb2d001bf823_0/about (see `scripts/getCensusBlocks.py`). The fire stations come from the aforementioned `Fire_Stations.geojson` file

- `rectGrid_200RectsSallSide.geojson`


- `scripts/getCensusBlocks.py` - Used to download census block data from the arcgis database we found online (https://hub.arcgis.com/datasets/d795eaa6ee7a40bdb2efeb2d001bf823_0/about). The script downloads the census blocks in chunks which can be concatenated into a complete file with `scripts/concatCensusChunks.py`. This download-in-batches process is because the API has a limit on the number of rows which can be downloaded at a single time.

- `scripts/concatCensusChunks.py` - Concatenates the downloaded census block data from `scripts/getCensusBlocks.py`

- `scripts/filterArcGISblocksToCityBoundary.ipynb` - Took the data in `data/censusBlocks_Chicago.geojson` (which was formerly called `arcgisCensusBlocks.geojson` as you will see in the script) and filtered it to just the Chicago boundary, using the boundary in `data/Boundaries - City.geojson`. Blocks that intersected the city but were not fully contained within it were cropped to be fully within the city (ie they were intersected with the city geometry). Then a filter was run to remove blocks that, after being intersected with the city, were tiny slivers of what they originally were, which we interpreted as meaning that they weren't really in Chicago and their nontrivial intersections were artifacts of imprecise coordinates. I also filtered out the census blocks for the airport area in the top left part of the city. This file output `data/processedCensusBlocks-20240209T1320.geojson`

- `scripts/matchBlocksToStations_Chicago.ipynb` - Matches census blocks in Chicago to their nearest fire station (just using geodesic distance). Took in as an input the filtered census blocks from `scripts/filterArcGISblocksToCityBoundary.ipynb`. Created `data/censusBlocksAndClosestFireStations_Chicago-20240212T1545.geojson` (although I renamed it to include "chicago" later)

- `scripts/matchBlocksToStations_noCityBoundary.ipynb`
- 
- `scripts/overlayRectGrid.ipynb

- `scripts/plotFireStationsAndBlocks.ipynb`


## Miscallaneous Notes

- FIPS County codes for downloading census blocks were found here: https://transition.fcc.gov/oet/info/maps/census/fips/fips.txt

