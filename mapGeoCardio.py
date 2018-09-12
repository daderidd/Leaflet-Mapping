import pandas as pd
import geopandas as gpd
# import pysal as ps
# from pysal.contrib.viz import mapping as maps
# from pysal.esda.getisord import G_Local
import folium
from folium.plugins import Fullscreen
from pathlib import Path
from scr import dopemap
import shapefile
from json import dumps

data_folder = Path("../../Projets/GeoCardio/Data/").resolve()
shp_folder = Path("../../Projets/GeoCardio/Shape_files/").resolve()
output_folder = Path("../../Projets/GeoCardio/Maps/").resolve()

mapping_data = data_folder / "geocardio_swiss_coord.csv"
df = pd.read_csv(mapping_data)
df = df[df.columns[1:]]

# geometry = [Point(xy) for xy in zip(df.E, df.N)]
# crs = {'init': 'epsg:2056'}
# gdf = GeoDataFrame(df, crs=crs, geometry=geometry)
df = df.loc[df['E'].isnull()==False]

df.loc[df['rcp_avant_amb'] == 1, 'rcp_avant_amb'] = 'Réanimation par témoin'
df.loc[df['rcp_avant_amb'] == 99, 'rcp_avant_amb'] = 'Donnée manquante'

#
shp_choro1 = shp_folder / "Vaud_communes4326.shp"
shp_choro1 = str(shp_choro1)
choro1 = gpd.read_file(shp_choro1)
choro1 = choro1.to_crs({'init': 'epsg:4326'})


# read the shapefile
reader = shapefile.Reader('../../Projets/GeoCardio/Shape_files/Vaud_communes4326.shp')
fields = reader.fields[1:]
field_names = [field[0] for field in fields]
buffer = []
for sr in reader.shapeRecords():
    atr = dict(zip(field_names, sr.record))
    geom = sr.shape.__geo_interface__
    buffer.append(dict(type="Feature", \
    geometry=geom, properties=atr)) 

# write the GeoJSON file
geojson = open(data_folder/"vaud_communes4326.json", "w")
geojson.write(dumps({"type": "FeatureCollection",\
"features": buffer}, indent=2, default=str) + "\n")
geojson.close()


map_geocardio = str(shp_folder / 'Vaud_communes_GeoCardio.shp')
vd_geocardio = gpd.read_file(map_geocardio)
vd_geocardio = vd_geocardio.to_crs({'init': 'epsg:4326'})

superficie_vaud = pd.read_csv(data_folder/'Superficie_2013-2018-communes.csv')

geo_data = vd_geocardio.groupby(['UUID','NAME','BFS_NUMMER']).size().reset_index(name='Number_geocardio_counts')
superficie_vaud = superficie_vaud.rename(columns={'Numero': 'BFS_NUMMER'})
superficie_vaud['BFS_NUMMER'] = superficie_vaud['BFS_NUMMER'].astype(int)
geo_data = geo_data.merge(superficie_vaud,on = 'BFS_NUMMER',how = 'left')
geo_data = geo_data.rename(columns={'Surfacedupolygone': 'PolygonSurface'})

geo_data['PolygonSurface'] = geo_data['PolygonSurface'].astype(float)
geo_data['Rate_bussante_perha'] = geo_data['Number_geocardio_counts']/geo_data['PolygonSurface']
geo_data = geo_data.groupby(['BFS_NUMMER','Rate_bussante_perha']).size().reset_index(name='NValues')
city_geo_path = str(data_folder/'vaud_communes4326.json')
city_geo = gpd.read_file(city_geo_path)
################
colors = ['red','blue','green','yellow','orange','pink','cyan']

# Create map
folium_map = dopemap.createMap(df,'lon','lat',10,14)
# Add additional tile style options
folium_map = dopemap.addTiles(folium_map,['Mapbox Control Room','Stamen Toner','CartoDB dark_matter'],14)
# Add Circle Markers at designed locations
    # Clustering points
dopemap.createMarkers(folium_map,df,'lon','lat','GeoCardio data points',['devenir_patient','lon','lat','geo_address','comment'],['Devenir patient','Longitud','Latitud','Address','Comment'],'devenir_patient',20,colors)
#Add legend to markers
legend_html = dopemap.createLegend(folium_map,df['devenir_patient'],colors)
# Add choropleth layer 
# createChoroplethMap(folium_map,city_geo,geo_data,'Number of cases',['Numero','Number_geocardio_counts'],'feature.properties.BFS_NUMMER','Number of cases ?')
# Add choropleth layer 
dopemap.createChoroplethMap(folium_map,city_geo,geo_data,'Number of cases per ha',['BFS_NUMMER','Rate_bussante_perha'],'feature.properties.BFS_NUMMER','Number of cases per ha')
# Add heatmap
dopemap.createHeatmap(folium_map,df,'lon','lat')
# Add fullscreen option
Fullscreen().add_to(folium_map)
# Add layer control
folium.LayerControl().add_to(folium_map)
# Save map
output_file = str(output_folder / 'all_devenir_patient.html')
folium_map.save(output_file)
