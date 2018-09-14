import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import Fullscreen
from pathlib import Path
from scr import dopemap
import shapefile
from json import dumps

#
data_folder = Path("../../path/to/data/folder/").resolve()
shp_folder = Path("../../path/to/shp_files/folder/").resolve()
output_folder = Path("../../path/to/output/folder/").resolve()

datatomap = data_folder / "filename"
df = pd.read_csv(datatomap)

#Delete all rows not having coordinates
df = df.loc[df['E'].isnull()==False]

#Example of choropleth layer creation
# We need to have a JSON dump file with all the variables and a shp file with a shared key to join
# We can create the JSON using a shapefile that already contains a lot of variables
# Read the shapefile
reader = shapefile.Reader('../../Projets/GeoCardio/Shape_files/shpfilename.shp')
fields = reader.fields[1:]
field_names = [field[0] for field in fields]
buffer = []
for sr in reader.shapeRecords():
    atr = dict(zip(field_names, sr.record))
    geom = sr.shape.__geo_interface__
    buffer.append(dict(type="Feature", \
    geometry=geom, properties=atr)) 
# Write the GeoJSON file
geojson = open(data_folder/"shpfilename.json", "w")
geojson.write(dumps({"type": "FeatureCollection",\
"features": buffer}, indent=2, default=str) + "\n")
geojson.close()

