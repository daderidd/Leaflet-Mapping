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
