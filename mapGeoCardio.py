import pandas as pd
import geopandas as gpd
from geopandas import GeoDataFrame
# import pysal as ps
# from pysal.contrib.viz import mapping as maps
# from pysal.esda.getisord import G_Local
import folium
from folium.plugins import Fullscreen
from pathlib import Path
from shapely.geometry import Point, Polygon
from scr import dopemap
import shapefile
from json import dumps
#############
data_folder = Path("../../Projets/GeoCardio/Data/").resolve()
shp_folder = Path("../../Projets/GeoCardio/Shape_files/").resolve()
output_folder = Path("../../Projets/GeoCardio/Maps/").resolve()
datatomap = data_folder / "geocardio_swiss_coord.csv"

##############
df = pd.read_csv(datatomap)
df = df[df.columns[1:]]
df = df.loc[df['E'].isnull()==False]
##############
df.loc[df['rcp_avant_amb'] == 1, 'rcp_avant_amb'] = 'Réanimation par témoin'
df.loc[df['rcp_avant_amb'] == 99, 'rcp_avant_amb'] = 'Donnée manquante'
df['lon'] = df['lon'].round(7)
df['lat'] = df['lat'].round(7)
##############
geometry = [Point(xy) for xy in zip(df.lon, df.lat)]
crs = {'init': 'epsg:4326'}
gdf = GeoDataFrame(df, crs=crs, geometry=geometry)
##############
choro1 = gpd.read_file('/Users/david/Dropbox/PhD/Projets/GeoFood/Data/Background_maps/SHAPEFILE_LV95_LN02/swissBOUNDARIES3D_1_3_TLM_HOHEITSGEBIET.shp',encoding = 'ISO-8859-1')
choro1 = choro1.to_crs({'init': 'epsg:4326'})
choro1 = choro1.loc[choro1['KANTONSNUM'] == 22.0]
geojson_file = data_folder/"swiss_cities.geojson"
if geojson_file.is_file():
	pass
else:
	choro1.to_file(geojson_file, driver='GeoJSON')
choro1 = choro1.merge(gdf, left_on = 'BFS_NUMMER',right_on='nouveau_no_commune', how = 'right')
# ###############
gdf['localite'] = gdf['localite'].str.replace('\(VD\)','')
gdf['localite'] = gdf['localite'].str.replace('VD','')
choro1['NAME'] = choro1['NAME'].str.replace('\(VD\)','')
choro1['NAME'] = choro1['NAME'].str.replace('VD','')
# ###############
superficie_vaud = pd.read_csv(data_folder/'Superficie_2013-2018-communes.csv')

geo_data = choro1.groupby(['NAME','BFS_NUMMER']).size().reset_index(name='Number_geocardio_counts')
geo_data = geo_data.loc[geo_data['Number_geocardio_counts'] != 0]

superficie_vaud = superficie_vaud.rename(columns={'Numero': 'BFS_NUMMER'})
superficie_vaud['BFS_NUMMER'] = superficie_vaud['BFS_NUMMER'].astype(int)
geo_data = geo_data.merge(superficie_vaud,on = 'BFS_NUMMER',how = 'left')
geo_data = geo_data.rename(columns={'Surfacedupolygone': 'PolygonSurface'})

geo_data['PolygonSurface'] = geo_data['PolygonSurface'].astype(float)
geo_data['Rate_bussante_perha'] = geo_data['Number_geocardio_counts']/geo_data['PolygonSurface']
# ################
city_geo_path = str(data_folder/'swiss_cities.geojson')
city_geo = gpd.read_file(city_geo_path)
################
colors = ['red','blue','green','yellow','orange','pink','cyan']
gjs = city_geo.merge(geo_data,on = 'BFS_NUMMER',how = 'right')





################ 1/ MAP
folium_map = dopemap.createMap(df,'lon','lat',10,14)
# Add additional tile style options
folium_map = dopemap.addTiles(folium_map,['Stamen Toner','CartoDB dark_matter'],14)
# Add Circle Markers at designed locations
    # Clustering points
dopemap.createMarkers(folium_map,df,'lon','lat','GeoCardio data points',['devenir_patient','lon','lat','geo_address','comment'],['Devenir patient','Longitud','Latitud','Address','Comment'],'devenir_patient',20,colors)
#Add legend to markers
legend_html = dopemap.createLegend(folium_map,df['devenir_patient'],colors)
# Add heatmap
dopemap.createHeatmap(folium_map,df,'lon','lat')
# Add fullscreen option
Fullscreen().add_to(folium_map)
# Add layer control
folium.LayerControl().add_to(folium_map)
# Save map 1A ########################################################################################
output_file = str(output_folder / 'Devenir_patient.html')
folium_map.save(output_file)
# Add choropleth layer 
dopemap.createChoroplethMap(folium_map,gjs,'Number of cases per ha',['BFS_NUMMER','Rate_bussante_perha'],'feature.properties.BFS_NUMMER','Number of cases per ha')
# Save map 1B ########################################################################################
output_file = str(output_folder / 'Devenir_patient_choro.html')
folium_map.save(output_file)



################ 2/ MAP
folium_map = dopemap.createMap(df,'lon','lat',10,14)
# Add additional tile style options
folium_map = dopemap.addTiles(folium_map,['Stamen Toner','CartoDB dark_matter'],14)
# Add Circle Markers at designed locations
    # Clustering points
dopemap.createMarkers(folium_map,df,'lon','lat','GeoCardio data points',['rcp_avant_amb','lon','lat','geo_address','comment'],['Réanimation par témoin','Longitud','Latitud','Address','Comment'],'rcp_avant_amb',20,colors)
#Add legend to markers
legend_html = dopemap.createLegend(folium_map,df['rcp_avant_amb'],colors)
# Add heatmap
dopemap.createHeatmap(folium_map,df,'lon','lat')
# Add fullscreen option
Fullscreen().add_to(folium_map)
# Add layer control
folium.LayerControl().add_to(folium_map)
# Save map
output_file = str(output_folder / 'Reanimation.html')
folium_map.save(output_file)
