def coordConvToSwiss(df,lon,lat):
    swiss_coord_lon = []
    E_list = []
    N_list = []
    swiss_coord_lat = []
    for i, row in df.iterrows():
        x = row[lon]
        y = row[lat]
        x = x*3600
        y = y*3600
        phi_prime = (y-169028.66)/10000
        lambda_prime = (x - 26782.5)/10000
        E = 2600072.37 + 211455.93 * lambda_prime - 10938.51*lambda_prime*phi_prime - 0.36*lambda_prime*phi_prime*phi_prime - 44.54 *lambda_prime*lambda_prime*lambda_prime
        new_y = E - 2000000.00
        N = 1200147.07 + 308807.95 * phi_prime + 3745.25 *lambda_prime*lambda_prime + 76.63 *phi_prime*phi_prime - 194.56 *lambda_prime*lambda_prime*phi_prime + 119.79 *phi_prime*phi_prime*phi_prime
        new_x = N-1000000.00
        swiss_coord_lon.append(new_x)
        swiss_coord_lat.append(new_y)
        E_list.append(E)
        N_list.append(N)
    df['E'] = E_list
    df['N'] = N_list
    df['swiss_coord_lon'] = swiss_coord_lon
    df['swiss_coord_lat'] = swiss_coord_lat
    return df
def coordConvfromSwiss(df,lon,lat):
    inProj = Proj(init='epsg:2056')
    outProj = Proj(init='epsg:4326')
    for index, row in df.iterrows():
        x = row[lon]
        y = row[lat]
        df.loc[index,'x'],df.loc[index,'y'] = transform(inProj,outProj,x,y)
    return df


