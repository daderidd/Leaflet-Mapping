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