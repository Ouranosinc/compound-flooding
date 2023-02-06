from netCDF4 import Dataset,num2date
import matplotlib.pyplot as plt 
import cartopy.crs as ccrs
import cartopy
import cartopy.feature as cfeat
import os
import pandas as pd
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib import colors
import matplotlib
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker
import cartopy.mpl.geoaxes
from mpl_toolkits.axes_grid1.inset_locator import inset_axes


pth = os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/4- Presentations/Symposium_Ouranos/sea_level_climatedata.nc')
nc = Dataset(pth,'r')
variables = 
lat = nc.variables['lat'][:]
lon = nc.variables['lon'][:]
kopi= (nc.variables['Band1'][:,:])
nc.close()

