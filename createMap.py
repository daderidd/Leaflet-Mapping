def createMap(df,x,y,zoom,max_zoom):
    map = folium.Map([mean(df[y]),mean(df[x])],zoom_start = zoom,max_zoom = max_zoom)
    return map