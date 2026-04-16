# SJRBC-web-map-data
Repository for adding, updating, and maintaining water monitoring data for the SJRBC web map
## Data description

The data is formatted to work with the [St. Joe River Basin Commission Web Map](data.sjrbc.com). The source code for the web map is available [here](https://github.com/juozasg/river-data-explorer)


### sites.csv file

`sites.csv` list all monitored sites and their geographical coordinates.

Each site must have a unique `siteId` field in the format `dataset-number`. For example: `ecoli-1` or `fish-20`

The dataset names in `sites.csv` refer to files containing the data for the sites. So for `ecoli-1` the data is stored in `ecoli.csv`.



### Variables and datasets

`datasets` folder contains timeseries records for each site. Each CSV record is keyed by `siteId` and `date` and contains columns of variable readings. Variables are defined in `variables.yaml` file



### geojson geometries

Sites (points), rivers (lines), states/counties/HUCs (polygons) and site/river catchments (polygons) are all found `geojson` folder.

Catchments are calculated from from `sites.csv` by manually placing each site on a hydrological D8 accumulation flow raster map in QGIS and then using the codes and documentation in the [condem-pysheds](https://github.com/juozasg/condem-sheds) repository to generate catchment rasters, convert them to polygons and merge them into geojson files.


### Geoindexes

Each site belongs to multiple regions/areas (polygons): HUCs, state and a county. `indexes` folder contains this geoindex. Whenever new sites are added the indexes must be rebuild with `scripts/build-indexes.py`.


### Tolthawk and USGS realtime data

See `scripts/README.md` for instructions on updating tolthawk and USGS streamflow datasets and the real-time webservice


