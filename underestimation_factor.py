"""
This script plots the Kendall's correlation coefficient as well as the corresponding p-value for the river outlets (Figures 7 and 8). The data are stored in a 
excel file (exutoires_LOT2_cartopy.csv).
"""

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

path = os.getcwd()
os.chdir('/home/mohammad/Dossier_travail/705300_rehaussement_marin/paper')
data = pd.read_csv('Underestimation_factor.csv',encoding="ISO-8859-1", skiprows=0, index_col=False)

# plots

fig = plt.figure(dpi=300)
ax = fig.add_subplot(2,2,1,projection = ccrs.PlateCarree())

ax.add_feature(cfeat.LAND,color = 'lightgrey')
ax.add_feature(cfeat.OCEAN, color = 'white')
# ax.add_feature(cfeat.RIVERS)
# ax.add_feature(cfeat.LAKES)
ax.add_feature(cfeat.COASTLINE, alpha=1, color = 'black',linewidth = 0.5)

ax.set_extent([-74,-63,44,51])
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)

# add scatterplot onto the map
# cmap = colors.ListedColormap(['midnightblue', 'mediumblue','blue','slateblue','lightsteelblue','white','white','tomato','red','darkred'])

bounds = np.linspace(0,30,31)

cmap = matplotlib.cm.Reds  #define the colormap
cmaplist = [cmap(i) for i in range(cmap.N)] #extract all the colors from the colormap
cmaplist[0] = (.5, .5, .5, 1.0)  #make the first color as gray
# cmaplist[0] = (1.0, 1.0, 1.0, 1.0)  #make the first color as gray

cmap = matplotlib.colors.LinearSegmentedColormap.from_list(
    'Custom cmap', cmaplist, cmap.N)

norm = colors.BoundaryNorm(bounds,ncolors=cmap.N,extend = 'max')

h=plt.scatter(data['Longitude'], data['Latitude'],
            c=data['UF_WLcondQ'], 
            cmap=cmap, 
            transform=ccrs.PlateCarree(),
            norm = norm,s = 5)

divider = make_axes_locatable(ax)
ax_cb = divider.new_horizontal(size="3%", pad=0.05, axes_class=plt.Axes)
fig.add_axes(ax_cb)
cbars = plt.colorbar(h, cax=ax_cb, ticks = np.array([0, 5, 10, 15, 20, 25, 30, 35, 40, 45]))
cbars.ax.tick_params(labelsize=10)
# cbars.set_label('p-value', fontsize=10)

ax.set_title('$WL_{cond}$Q',fontsize=10)

axins = inset_axes(ax, width="40%", height="40%", loc="lower right", 
                   axes_class=cartopy.mpl.geoaxes.GeoAxes, 
                   axes_kwargs=dict(map_projection=cartopy.crs.PlateCarree()))

axins.add_feature(cfeat.LAND,color = 'lightgrey')
axins.add_feature(cfeat.OCEAN, color = 'white')
axins.add_feature(cfeat.COASTLINE, alpha=1, color = 'black',linewidth = 0.5)

axins.set_extent([-71.9,-74.2,45.5,46.7])
axins.xaxis.set_visible(False)
axins.yaxis.set_visible(False)



bounds = np.linspace(0,30,31)

cmap = matplotlib.cm.Reds  #define the colormap
cmaplist = [cmap(i) for i in range(cmap.N)] #extract all the colors from the colormap
cmaplist[0] = (.5, .5, .5, 1.0)  #make the first color as gray

cmap = matplotlib.colors.LinearSegmentedColormap.from_list(
    'Custom cmap', cmaplist, cmap.N)

norm = colors.BoundaryNorm(bounds,ncolors=cmap.N,extend = 'max')

h=axins.scatter(data['Longitude'], data['Latitude'],
            c=data['UF_WLcondQ'], 
            cmap=cmap, 
            transform=ccrs.PlateCarree(),
            norm = norm,s=5)

# Now for QcondWL
ax2 = fig.add_subplot(2,2,2,projection = ccrs.PlateCarree())

ax2.add_feature(cfeat.LAND,color = 'lightgrey')
ax2.add_feature(cfeat.OCEAN, color = 'white')
# ax.add_feature(cfeat.RIVERS)
# ax.add_feature(cfeat.LAKES)
ax2.add_feature(cfeat.COASTLINE, alpha=1, color = 'black',linewidth = 0.5)

ax2.set_extent([-74,-63,44,51])
ax2.xaxis.set_visible(False)
ax2.yaxis.set_visible(False)

# add scatterplot onto the map
# cmap = colors.ListedColormap(['midnightblue', 'mediumblue','blue','slateblue','lightsteelblue','white','white','tomato','red','darkred'])

bounds = np.linspace(0,20,21)

cmap = matplotlib.cm.Reds  #define the colormap
cmaplist = [cmap(i) for i in range(cmap.N)] #extract all the colors from the colormap
cmaplist[0] = (.5, .5, .5, 1.0)  #make the first color as gray
# cmaplist[0] = (1.0, 1.0, 1.0, 1.0)  #make the first color as gray

cmap = matplotlib.colors.LinearSegmentedColormap.from_list(
    'Custom cmap', cmaplist, cmap.N)

norm = colors.BoundaryNorm(bounds,ncolors=cmap.N,extend = 'max')

h=plt.scatter(data['Longitude'], data['Latitude'],
            c=data['UF_QcondWL'], 
            cmap=cmap, 
            transform=ccrs.PlateCarree(),
            norm = norm,s = 5)

divider = make_axes_locatable(ax2)
ax_cb = divider.new_horizontal(size="3%", pad=0.05, axes_class=plt.Axes)
fig.add_axes(ax_cb)
cbars = plt.colorbar(h, cax=ax_cb, ticks = np.array([0, 5, 10, 15, 20, 25, 30, 35, 40, 45]))
cbars.ax.tick_params(labelsize=10)
# cbars.set_label('p-value', fontsize=10)

ax2.set_title('$Q_{cond}$WL',fontsize=10)

axins = inset_axes(ax2, width="40%", height="40%", loc="lower right", 
                   axes_class=cartopy.mpl.geoaxes.GeoAxes, 
                   axes_kwargs=dict(map_projection=cartopy.crs.PlateCarree()))

axins.add_feature(cfeat.LAND,color = 'lightgrey')
axins.add_feature(cfeat.OCEAN, color = 'white')
axins.add_feature(cfeat.COASTLINE, alpha=1, color = 'black',linewidth = 0.5)

axins.set_extent([-71.9,-74.2,45.5,46.7])
axins.xaxis.set_visible(False)
axins.yaxis.set_visible(False)



bounds = np.linspace(0,20,21)

cmap = matplotlib.cm.Reds  #define the colormap
cmaplist = [cmap(i) for i in range(cmap.N)] #extract all the colors from the colormap
cmaplist[0] = (.5, .5, .5, 1.0)  #make the first color as gray

cmap = matplotlib.colors.LinearSegmentedColormap.from_list(
    'Custom cmap', cmaplist, cmap.N)

norm = colors.BoundaryNorm(bounds,ncolors=cmap.N,extend = 'max')

h=axins.scatter(data['Longitude'], data['Latitude'],
            c=data['UF_QcondWL'], 
            cmap=cmap, 
            transform=ccrs.PlateCarree(),
            norm = norm,s=5)


plt.savefig('Underestimation Factor3.png',bbox_inches='tight')
