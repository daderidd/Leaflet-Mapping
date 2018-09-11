def coordConvfromSwiss(df,lon,lat):
    inProj = Proj(init='epsg:2056')
    outProj = Proj(init='epsg:4326')
    for index, row in df.iterrows():
        x = row[lon]
        y = row[lat]
        df.loc[index,'x'],df.loc[index,'y'] = transform(inProj,outProj,x,y)
    return df