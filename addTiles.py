def addTiles(map,tiles,max_zoom):
    for tile in tiles:
        folium.TileLayer(tile,max_zoom = max_zoom).add_to(map)
    return map