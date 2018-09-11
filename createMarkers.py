def createMarkers(map,df,x,y,markers_name,comment_cols,comment_names,color_var,radius,colors,popup =True):
    feature_group = FeatureGroup(name=markers_name)
    marker_cluster = MarkerCluster(name = 'test').add_to(map)
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
