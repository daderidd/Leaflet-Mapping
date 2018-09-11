def createHeatmap(map,data,x,y):
    # Add heatmap Legend
    cm1 = cm.LinearColormap(['b','c','lime','y','r'], vmin=0, vmax=1, caption='Heatmap Legend')
    map.add_child(cm1)

    # List comprehension to make out list of lists
    heat_data = [[row[y],row[x]] for index, row in data.iterrows()]
    # Plot it on the map
    HeatMap(heat_data,name = 'Heat Map',radius = 25,gradient = {0.1: 'blue',0.25: 'cyan', 0.5: 'lime',0.75:'yellow',0.9:'orange', 1: 'red'}).add_to(map)