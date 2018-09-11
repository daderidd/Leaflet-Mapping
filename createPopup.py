def createPopupText (col_names):
    """Return popup message for Folium markers"""
    popup_text = """"""
    for name in col_names:
        format_name = name + ': ' + '{} ' + '<br> '
        popup_text += format_name
    return popup_text