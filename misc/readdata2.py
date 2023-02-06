# Reading data of N.Bernier

import numpy as np
from scipy.io import loadmat
from scipy import spatial
import matplotlib.pyplot as plt
# from mpl_toolkits.basemap import Basemap
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.io as pio

path = r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\DFO-MPO\Gridstats.mat'
data = loadmat(path)

lat = np.zeros((265,361))
lon = np.zeros((265,361))
for i in range(265):
    for j in range(361):
        lat[i][j] = 38 + (i-1)/12
        lon[i][j] = -72 + (j-1)/12


lat_rshp = lat.reshape(95665,1)
lon_rshp = lon.reshape(95665,1)

coordinate = np.hstack((lon_rshp,lat_rshp))   # this is to make a pair from lat lon vecotr

maxtwl = data['maxtwl']

# Now lets say we want to find the closest point to a given lat lon. here is how we do it. inspired by Stackoverflow
# the idea is to use spatial package of Scipy for this aim


pt =[-69.72,48.13]  # Longitude, Latitude of Saguenay

pt =[-60.68,46.942]  # Longitude, Latitude of Cape Breton

pt =[-64.164,48.577]  # Longitude, Latitude of Gaspesie

pt =[-64.94,50.24]  # Longitude, Latitude of Cote-Nord



[lon_p,lat_p] = coordinate[spatial.KDTree(coordinate).query(pt)[1]]

#twl_to_compare = maxtwl[(maxtwl[:,0]==lon_p) & (maxtwl[:,2]==lat_p)]

aa = np.where(lat[:,0]==lat_p)
bb = np.where(lon[0,:]==lon_p)

maxtwl_pt = maxtwl[aa,:,bb] # this is the maximum annual dta for that point


#reading annual maxima total water level


# read .mat file
pth2 = r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\DFO-MPO\RPtwlmax_40.mat'
data_wlrp = loadmat(pth2)  # Scipy loads matlab file as dictionary
RP40_twl = data_wlrp['RP40_max0']
RP100_twl = data_wlrp['RP100_max0']
TWL = data_wlrp['RP100_max0']

RP40_twl_rshp = RP40_twl.reshape(95665,1)
RP100_twl_rshp = RP100_twl.reshape(95665,1)

data = []
for i in range(95665):
    data.append([lat_rshp[i,0],lon_rshp[i,0],RP40_twl_rshp[i,0],RP100_twl_rshp[i,0]])
dff = pd.DataFrame(data,columns = ["latitude","longitude","twl_40yr","twl_100yr"])

# select not null values in dataframe (inland points will be excluded)
Bernier_notnull = dff.loc[dff['twl_40yr'].notnull(), ["latitude","longitude","twl_40yr","twl_100yr"]]


    
dff_GDF = gpd.GeoDataFrame(
    Bernier_notnull, geometry=gpd.points_from_xy(Bernier_notnull.longitude, Bernier_notnull.latitude))    

pio.renderers.default='browser'
fig = px.scatter_geo(dff_GDF,lat=dff_GDF.geometry.y,
                            lon=dff_GDF.geometry.x,
                            hover_name = dff_GDF.twl_40yr,resolution = 50)

fig.show()




###########################################################

# read the dataset of Muis et al.,2020
import xarray as xr
import plotly.express as px
import geopandas as gpd
import numpy as np
from scipy import spatial

path = r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\DFO-MPO\CODEC_amax_ERA5_1979_2017_coor_mask_GUM_RPS.nc'

data = xr.open_dataset(path)
df =  data.to_dataframe() # transform it to dataframe for further plotting
df_r = df.reset_index() # reset the index so that each coordinate can be represented as an individual column in dataframe

WL_2yr = df_r.loc[lambda df_r: df_r['return_periods']== 2.0,:]
lon = WL_2yr['station_x_coordinate']
lat = WL_2yr['station_y_coordinate']

coordinate = np.stack((lon,lat),axis=-1)   # this is to make a pair from lat lon vecotr


pt =[-69.72,48.13]  # Longitude, Latitude of Saguenay

pt =[-60.68,46.942]  # Longitude, Latitude of Cape Breton

pt =[-64.164,48.577]  # Longitude, Latitude of Gaspesie

pt =[-64.94,50.24]  # Longitude, Latitude of Cote-Nord

[lon_p,lat_p] = coordinate[spatial.KDTree(coordinate).query(pt)[1]]

data_pnt = data.where((data.station_x_coordinate==lon_p) & (data.station_y_coordinate==lat_p), drop=True)
data_pnt_df =  data_pnt.to_dataframe() # transform it to dataframe for further plotting

data_pnt_dff = data_pnt_df.reset_index()


#WL_2yr['Coordinates'] = list(zip(WL_2yr.station_x_coordinate, WL_2yr.station_y_coordinate))
WL_2yr_GDF = gpd.GeoDataFrame(
    WL_2yr, geometry=gpd.points_from_xy(WL_2yr.station_x_coordinate, WL_2yr.station_y_coordinate))


#WL_2yr['Coordinates'] = WL_2yr['Coordinates'].apply(Point)

WL_2yr_GDF['station_id'] = WL_2yr_GDF['station_id'].astype('str')

import plotly.io as pio

pio.renderers.default='browser'

fig = px.scatter_geo(WL_2yr_GDF,lat=WL_2yr_GDF.geometry.y,
                            lon=WL_2yr_GDF.geometry.x,
                            hover_name = "station_id")

fig.show()


df_r['station_id'] = df_r['station_id'].astype('str')

WL_Saguenay= df_r[df_r.station_id.str.contains('11745',case=False)]
WL_Saguenay_unique = WL_Saguenay.drop_duplicates('return_periods')
#PLOT THE DATA
WL_Saguenay_unique.plot(x = "return_periods", y="RPS",marker = 'o')
plt.xlabel('Return periods')
plt.ylabel('Water level (m)')
plt.title('Saguenay: lat = 48.13 lon =-69.72')

#######################################################################################################
#Reading data of Zhang et al., 2013

import numpy as np
from scipy.io import loadmat
from scipy import spatial
import matplotlib.pyplot as plt
# from mpl_toolkits.basemap import Basemap
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.io as pio

path = r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\Heng\Heng.mat'
data = loadmat(path)

lat = data['LAT2']
lon = data['LON2']

a_parameter_lizhai = data['a_parameter_lizhai']
b_parameter_lizhai = data['b_parameter_lizhai']



lat_rshp = lat.reshape(893025,1)  # 945*945 = 893025
lon_rshp = lon.reshape(893025,1)
coordinate = np.hstack((lon_rshp,lat_rshp))   # this is to make a pair from lat lon vecotr

a_parameter_lizhai_rshp = a_parameter_lizhai.reshape(893025,1)
b_parameter_lizhai_rshp = b_parameter_lizhai.reshape(893025,1)


# Now lets say we want to find the closest point to a given lat lon. here is how we do it. inspired by Stackoverflow
# the idea is to use spatial package of Scipy for this aim


pt =[-69.72,48.13]  # Longitude, Latitude of Saguenay

pt =[-60.68,46.942]  # Longitude, Latitude of Cape Breton

pt =[-64.164,48.577]  # Longitude, Latitude of Gaspesie

pt =[-64.94,50.24]  # Longitude, Latitude of Cote-Nord



[lon_p,lat_p] = coordinate[spatial.KDTree(coordinate).query(pt)[1]]


#twl_to_compare = maxtwl[(maxtwl[:,0]==lon_p) & (maxtwl[:,2]==lat_p)]

aa = np.where(lat[:,0]==lat_p)
bb = np.where(lon[0,:]==lon_p)

a_parameter_point = a_parameter_lizhai[aa,bb] # this is the location parameter of the point
b_parameter_point = b_parameter_lizhai[aa,bb] # this is the scale parameter of the point







dataa = []
for i in range(893025):
    dataa.append([lat_rshp[i,0],lon_rshp[i,0],a_parameter_lizhai_rshp[i,0],b_parameter_lizhai_rshp[i,0]])
dff = pd.DataFrame(dataa,columns = ["latitude","longitude","a","b"])



# Zhang_notnull = dff.loc[dff['a'].notnull(), ["latitude","longitude","a","b"]]

Zhang_notnull = dff[(dff[['a']] != 0).all(axis=1)]
    
dff_GDF = gpd.GeoDataFrame(
    dff, geometry=gpd.points_from_xy(dff.Longitude, dff.Latitude))    

import plotly.io as pio

pio.renderers.default='browser'

fig = px.scatter_geo(dff_GDF,lat=dff_GDF.geometry.y,
                            lon=dff_GDF.geometry.x)



fig.show()



################################################################################################
#comparison of three DB at extreme water level value prediction of Sagueny
x= [2,5,10,25,50,100]
Bernier =[2.77,2.8,2.81,2.83,2.84,2.84]
Zhang = [3.87,3.95,3.99,4.02,4.03,4.05]
Muise = [4.17,4.3,4.4,4.5,4.6,4.65]

plt.plot(x,Bernier,'-o',ms=10,label='Bernier et al., 2006')
plt.plot(x,Zhang,'-o',ms=10,label='Zhang et al., 2019')
plt.plot(x,Muise,'-o',ms=10,label='Muise et al., 2020')
plt.xticks(x)


plt.xlabel('Return periods')
plt.ylabel('Water level (m)')
plt.title('Saguenay: lat = 48.13 lon =-69.72')
plt.grid('on')
plt.legend(framealpha=1, frameon=True);
plt.savefig('Saguenay.png')

#comparison of three DB at extreme water level value prediction of cape_Breton
x= [2,5,10,25,50,100]
Bernier =[0.5066,0.5181,0.5230,0.5275,0.530,0.532]
Zhang = [0.863,0.930,0.959,0.986,1.000,1.015]
Muise = [1.111,1.219,1.29138,1.38172,1.44873,1.51525]

plt.plot(x,Bernier,'-o',ms=10,label='Bernier et al., 2006')
plt.plot(x,Zhang,'-o',ms=10,label='Zhang et al., 2019')
plt.plot(x,Muise,'-o',ms=10,label='Muise et al., 2020')
plt.xticks(x)


plt.xlabel('Return periods')
plt.ylabel('Water level (m)')
plt.title('Cape Breton: lat = 46.942 lon =-60.68')
plt.grid('on')
#plt.legend(framealpha=1, frameon=True,loc = 'lower left');
plt.savefig('Cape_Breton.png')


#Gaspesie
x= [2,5,10,25,50,100]
Bernier =[1.156102964,1.25484472,1.296825008,1.336092035,1.358951612,1.378072324]
Zhang = [1.023587522,1.095832325,1.126547373,1.155277252,1.172002553,1.185992299]
Muise = [1.437801906,1.540012168,1.607684255,1.693188116,1.756619765,1.819583044]

plt.plot(x,Bernier,'-o',ms=10,label='Bernier et al., 2006')
plt.plot(x,Zhang,'-o',ms=10,label='Zhang et al., 2019')
plt.plot(x,Muise,'-o',ms=10,label='Muise et al., 2020')
plt.xticks(x)


plt.xlabel('Return periods')
plt.ylabel('Water level (m)')
plt.title('Gaspésie: lat = 48.577 lon =-64.164')
plt.grid('on')
#plt.legend(framealpha=1, frameon=True,loc = 'lower left');
plt.savefig('Gaspesie.png')

##### Cote-Nord



#Gaspesie
x= [2,5,10,25,50,100]
Bernier =[1.755337875,1.840447497,1.876632053,1.910477935,1.930181554,1.94666249]
Zhang = [1.976694007,2.052854191,2.085233873,2.115520796,2.133152542,2.147900477]
Muise = [2.260804334,2.404414227,2.499496472,2.61963314,2.708757384,2.797223548]

plt.plot(x,Bernier,'-o',ms=10,label='Bernier et al., 2006')
plt.plot(x,Zhang,'-o',ms=10,label='Zhang et al., 2019')
plt.plot(x,Muise,'-o',ms=10,label='Muise et al., 2020')
plt.xticks(x)


plt.xlabel('Return periods')
plt.ylabel('Water level (m)')
plt.title('Cote-Nord: lat =  50.24  lon =-64.94')
plt.grid('on')
#plt.legend(framealpha=1, frameon=True,loc = 'lower left');
plt.savefig('cotenord.png')

#########################################################33
data = {'Station':['Saguenay', 'Cape Breton', 'Gaspesie', 'Cote Nord'], 
        'lat':[-69.72,-60.68,-64.164,-64.94],
        'lon':[48.13,46.942,48.577,50.24]} 

df = pd.DataFrame(data) 
ruh_m = plt.imread('C:/Users/mohbiz1/Desktop/Dossier_travail/basinmaker-master/map.png')
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize = (8,7))
ax.scatter(df.lon, df.lat, zorder=1, alpha= 0.2, c='b')
ax.imshow(ruh_m, zorder=0, aspect= 'equal')


######################################################################
import geopandas as gpd
import plotly.express as px
import plotly.io as pio
import pandas as pd
import shapefile

sf_path = r'C:/Users/mohbiz1/Desktop/Dossier_travail/705300_rehaussement_marin/3- Data/Embouchure_23_BV.shp'
sf = shapefile.Reader(sf_path)

fields = [x[0] for x in sf.fields][1:]
records = [y[:] for y in sf.records()]
shps = [s.points for s in sf.shapes()]
sf_df = pd.DataFrame(columns = fields, data = records)

sf_df['type'] = 'Info Crue'

DEH = pd.DataFrame({'latitude': sf_df['LATITUDE_D'], 'longitude':sf_df['LONGITUDE_'], 'type':sf_df['type']})

## read Muise database
import xarray as xr
import plotly.express as px
import geopandas as gpd
import numpy as np
from scipy import spatial
import pandas as pd

path = r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\DFO-MPO\CODEC_amax_ERA5_1979_2017_coor_mask_GUM_RPS.nc'

data = xr.open_dataset(path)
df =  data.to_dataframe() # transform it to dataframe for further plotting
df_r = df.reset_index() # reset the index so that each coordinate can be represented as an individual column in dataframe

WL_2yr = df_r.loc[lambda df_r: df_r['return_periods']== 2.0,:]

WL_2yr['type']='Muise et al.,2020'


# combine two dataframe to create one for plotting
Muise = pd.DataFrame({'latitude': WL_2yr['station_y_coordinate'], 'longitude':WL_2yr['station_x_coordinate']})
Muise['type']='Muise et al., 2020'


merge_Muise_DEH = pd.concat([Muise,DEH])


GDF_pnt = gpd.GeoDataFrame(
    merge_Muise_DEH, geometry=gpd.points_from_xy(merge_Muise_DEH.longitude, merge_Muise_DEH.latitude))





mapbox_access_token =  'pk.eyJ1IjoiYml6aGFuaW1hbnphciIsImEiOiJja2xxdHVraWYxMXB1Mm5sYjJkaGNycnZvIn0.F1aT22S01-QiXpXbGHQNFw'
import plotly.express as px
import geopandas as gpd

geo_df = gpd.read_file(gpd.datasets.get_path('naturalearth_cities'))

px.set_mapbox_access_token(mapbox_access_token)
fig = px.scatter_mapbox(GDF_pnt,
                        lat=GDF_pnt.geometry.y,
                        lon=GDF_pnt.geometry.x,
                        color="type",
                        zoom=1)
fig.show()





# pio.renderers.default='browser'

# fig = px.scatter_geo(GDF_pnt,lat=GDF_pnt.geometry.y,
#                             lon=GDF_pnt.geometry.x,
#                             color='type')

# fig.show()


#################################################### combine_with Bernier
import geopandas as gpd
import plotly.express as px
import plotly.io as pio
import pandas as pd
import shapefile

sf_path = r'C:/Users/mohbiz1/Desktop/Dossier_travail/705300_rehaussement_marin/3- Data/Embouchure_23_BV.shp'
sf = shapefile.Reader(sf_path)

fields = [x[0] for x in sf.fields][1:]
records = [y[:] for y in sf.records()]
shps = [s.points for s in sf.shapes()]
sf_df = pd.DataFrame(columns = fields, data = records)

sf_df['type'] = 'Info Crue'

DEH = pd.DataFrame({'latitude': sf_df['LATITUDE_D'], 'longitude':sf_df['LONGITUDE_'], 'type':sf_df['type']})

import numpy as np
from scipy.io import loadmat
from scipy import spatial
import matplotlib.pyplot as plt
# from mpl_toolkits.basemap import Basemap
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.io as pio

path = r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\DFO-MPO\Gridstats.mat'
data = loadmat(path)

lat = np.zeros((265,361))
lon = np.zeros((265,361))
for i in range(265):
    for j in range(361):
        lat[i][j] = 38 + (i-1)/12
        lon[i][j] = -72 + (j-1)/12

lat_rshp = lat.reshape(95665,1)
lon_rshp = lon.reshape(95665,1)

Bernier = pd.DataFrame({'latitude': lat_rshp[:,0], 'longitude':lon_rshp[:,0]})
Bernier['type']='Bernier et al., 2006'


Bernier_notnull['type'] = 'Bernier et al., 2006'



merge_Bernier_DEH = pd.concat([Bernier_notnull,DEH])


GDF_pnt = gpd.GeoDataFrame(
    merge_Bernier_DEH, geometry=gpd.points_from_xy(merge_Bernier_DEH.longitude, merge_Bernier_DEH.latitude))



GDF_pnt = gpd.GeoDataFrame(
    DEH, geometry=gpd.points_from_xy(DEH.longitude, DEH.latitude))


# pio.renderers.default='browser'

# fig = px.scatter_geo(GDF_pnt,lat=GDF_pnt.geometry.y,
#                             lon=GDF_pnt.geometry.x,
#                             color='type')
# fig.show()


# latt_merge = merge_Bernier_DEH['latitude'].to_numpy()
# lonn_merge = merge_Bernier_DEH['longitude'].to_numpy()

# import pyproj

# infocrue = pyproj.Proj(init='epsg:4269')
# mapboxx = pyproj.Proj(init='epsg:4326')


# from pyproj import Proj, transform

# lon_proj, lat_proj = pyproj.transform(infocrue, mapboxx, lonn_merge, latt_merge)

# lon_proj, lat_proj = transform(Proj(init='epsg:4269'), Proj(init='epsg:4326'), lonn_merge, latt_merge)  # longitude first, latitude second

# merge_Bernier_DEH['lon'] =    lon_proj
# merge_Bernier_DEH['lat'] =    lat_proj



# GDF_pnt = gpd.GeoDataFrame(
#     merge_Bernier_DEH, geometry=gpd.points_from_xy(merge_Bernier_DEH.lon, merge_Bernier_DEH.lat))




mapbox_access_token =  'pk.eyJ1IjoiYml6aGFuaW1hbnphciIsImEiOiJja3BwaGo3MWQwM2xwMnBsZTl0YWMyZDVqIn0.nupd2c37sYE79L4lT9jBgg'
import plotly.express as px
import geopandas as gpd

geo_df = gpd.read_file(gpd.datasets.get_path('naturalearth_cities'))

px.set_mapbox_access_token(mapbox_access_token)
fig = px.scatter_mapbox(GDF_pnt,
                        lat=GDF_pnt.geometry.y,
                        lon=GDF_pnt.geometry.x,
                        color="type",
                        zoom=1)
fig.show()



############################################################## combined with Zhang
import geopandas as gpd
import plotly.express as px
import plotly.io as pio
import pandas as pd
import shapefile

sf_path = r'C:/Users/mohbiz1/Desktop/Dossier_travail/705300_rehaussement_marin/3- Data/Embouchure_23_BV.shp'
sf = shapefile.Reader(sf_path)

fields = [x[0] for x in sf.fields][1:]
records = [y[:] for y in sf.records()]
shps = [s.points for s in sf.shapes()]
sf_df = pd.DataFrame(columns = fields, data = records)

sf_df['type'] = 'Info Crue'

DEH = pd.DataFrame({'latitude': sf_df['LATITUDE_D'], 'longitude':sf_df['LONGITUDE_'], 'type':sf_df['type']})





import numpy as np
from scipy.io import loadmat
from scipy import spatial
import matplotlib.pyplot as plt
# from mpl_toolkits.basemap import Basemap
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go


path = r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\Heng\Heng.mat'
data = loadmat(path)

lat = data['LAT2']
lon = data['LON2']


lat_rshp = lat.reshape(893025,1)  # 945*945 = 893025
lon_rshp = lon.reshape(893025,1)


Zhang = pd.DataFrame({'latitude': lat_rshp[:,0], 'longitude':lon_rshp[:,0]})
Zhang_notnull['type']='Zhang et al., 2013'

merge_Zhang_DEH = pd.concat([Zhang_notnull,DEH])


GDF_pnt = gpd.GeoDataFrame(
    merge_Zhang_DEH, geometry=gpd.points_from_xy(merge_Zhang_DEH.longitude, merge_Zhang_DEH.latitude))




mapbox_access_token =  'pk.eyJ1IjoiYml6aGFuaW1hbnphciIsImEiOiJja2xxdHVraWYxMXB1Mm5sYjJkaGNycnZvIn0.F1aT22S01-QiXpXbGHQNFw'
import plotly.express as px
import geopandas as gpd

geo_df = gpd.read_file(gpd.datasets.get_path('naturalearth_cities'))

px.set_mapbox_access_token(mapbox_access_token)
fig = px.scatter_mapbox(GDF_pnt,
                        lat=GDF_pnt.geometry.y,
                        lon=GDF_pnt.geometry.x,
                        color="type",
                        zoom=1)
fig.show()

 pio.renderers.default='browser'

 fig = px.scatter_geo(GDF_pnt,lat=GDF_pnt.geometry.y,                            lon=GDF_pnt.geometry.x,
                            color='type')

 fig.show()



