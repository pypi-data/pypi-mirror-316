
# Osm2les

A Python package for processing and analyzing LES data with OpenStreetMap (OSM).

## Installation

```bash
pip install osm2les_dev
```

## Usage

<!-- Note: All WSF3D versions require GDAL to be installed -->
<!--'WSF3D_V02_BuildingHeight.tif' needs to be installed in the current folder to use WSF3D functions  -->

```python
import osm2les_dev
# Add usage examples here

# Prepare a dataframe of names and a point around which you'd like the visualization
osm2les_dev.extract_domain_from_points_wsf3d(df)
osm2les_dev.extract_domain_from_points_osm(df)
# You can choose whether or not to add the added WSF3D layer which takes more time
# but may result in more accurate visualizations.


# Below is an example of the KML File version
res = 1
bldH = 16
name = 'Ber1'
angleRotate = 0
extra_geometric_stats = True

bbox = parseKML(name+'.kml')[0:4]
domain = extract_domainKML(res,bldH,bbox,name,angleRotate,extra_geometric_stats)
# save the bbox
domain = extract_domain_from_KML_wsf3d(bbox, res, bldH, name, angleRotate, extra_geometric_stats)
np.savetxt(name+'.pos', bbox ,fmt='%f')
```

## License
MIT License
