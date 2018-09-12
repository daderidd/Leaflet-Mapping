# import pysal as ps
from pylab import *
# from pysal.esda.getisord import G_Local
import folium
from folium.plugins import HeatMap
from folium.plugins import MarkerCluster
import branca.colormap as cm
from folium import FeatureGroup


def createMap(df,x,y,zoom,max_zoom):
    map = folium.Map([mean(df[y]),mean(df[x])],zoom_start = zoom,max_zoom = max_zoom)
    return map
def addTiles(map,tiles,max_zoom):
    for tile in tiles:
        folium.TileLayer(tile,max_zoom = max_zoom).add_to(map)
    return map
def createChoroplethMap(map,geo_data,csv_data,mapname,data_col,join_col,legend_name):
    map.choropleth(
    geo_data=geo_data,
    data=csv_data,
    name = mapname,
    columns= data_col,
    key_on=join_col,
    fill_opacity = 0.8,
    fill_color='BuGn',
    legend_name=legend_name)
def createLegend(map,data,colors):
    legend_html = '''<div style="position: fixed; 
                        bottom: 50px; left: 50px; width: 400px; height: 200px;
                        border:2px blue; z-index:9999; font-size:16px;
                        ">&nbsp; Legend <br>'''
    legend_attr = []
    for i in range(len(data.unique())):
        legend_html += '''&nbsp; {} &nbsp; <i class="fa fa-map-marker fa-2x" style="color:{}"></i><br>'''
        legend_attr.append(data.unique()[i])
        legend_attr.append(colors[i])
    legend_html += '''</div>'''
    legend_html = legend_html.format(*legend_attr)
    map.get_root().html.add_child(folium.Element(legend_html))
def createPopupText (col_names):
    """Return popup message for Folium markers"""
    popup_text = """"""
    for name in col_names:
        format_name = name + ': ' + '{} ' + '<br> '
        popup_text += format_name
    return popup_text
def createMarkers(map,df,x,y,markers_name,comment_cols,comment_names,color_var,radius,colors,popup =True):
    feature_group = FeatureGroup(name=markers_name)
    marker_cluster = MarkerCluster(name = 'Point clusters').add_to(map)
    for i in comment_cols:
        if df[i].dtype == object:
            df[i] = df[i].str.replace("'","&#39;")
            df[i] = df[i].str.replace("'","&#339;")
    for index, row in df[0:5000].iterrows():
        if index % 1000 == 0:
            print(index,' Markers added to the map !')
        x1,y1 = row[x],row[y]
#         x1_r,y1_r = "{0:.2f}".format(x1),"{0:.2f}".format(y1)
        popup_text = createPopupText(comment_names)
        comment_list = [row[i] for i in comment_cols]
        popup_text = popup_text.format(*comment_list)
        if "'" in popup_text:
            popup_text = popup_text.replace("'"," ")
        color = colors[list(df[color_var].unique()).index(row[color_var])]
        if popup == True:
            marker = folium.Circle(location = ([y1,x1]), fill=True,fill_opacity = 1,fill_color = color, color = color,radius = radius,popup = popup_text)
            folium.Circle(location = ([y1,x1]), fill=True,fill_opacity = 1,fill_color = color, color = color,radius = radius,popup = popup_text).add_to(marker_cluster)
        elif popup == False:
            marker = folium.Circle(location = ([y1,x1]), fill=True,fill_opacity = 1,fill_color = color, color = color,radius = radius)
            folium.Circle(location = ([y1,x1]), fill=True,fill_opacity = 1,fill_color = color, color = color,radius = radius).add_to(marker_cluster)
        feature_group.add_child(marker)
    map.add_child(feature_group)
def createHeatmap(map,data,x,y):
    # Add heatmap Legend
    cm1 = cm.LinearColormap(['b','c','lime','y','r'], vmin=0, vmax=1, caption='Heatmap Legend')
    map.add_child(cm1)

    # List comprehension to make out list of lists
    heat_data = [[row[y],row[x]] for index, row in data.iterrows()]
    # Plot it on the map
    HeatMap(heat_data,name = 'Heat Map',radius = 25,gradient = {0.1: 'blue',0.25: 'cyan', 0.5: 'lime',0.75:'yellow',0.9:'orange', 1: 'red'}).add_to(map)
