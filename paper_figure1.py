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
data = pd.read_csv('exutoires_cartopy.csv',encoding="ISO-8859-1", skiprows=0, index_col=False)

# plots

fig = plt.figure(dpi=300)

ax = fig.add_subplot(2,2,2,projection = ccrs.PlateCarree())

ax.add_feature(cfeat.LAND,color = 'lightgrey')
ax.add_feature(cfeat.OCEAN, color = 'white')
# ax.add_feature(cfeat.RIVERS)
# ax.add_feature(cfeat.LAKES)
ax.add_feature(cfeat.COASTLINE, alpha=1, color = 'black',linewidth = 0.5)

ax.set_extent([-74,-63,44,51])
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)



# add scatterplot onto the map
# cmap = matplotlib.cm.seismic
# bounds = np.array([-0.3,-0.2,-0.1,0.1, 0.2,0.3, 0.4,0.5])
# norm = colors.BoundaryNorm(boundaries=bounds,ncolors = cmap.N)

bounds = np.linspace(-0.5,0.5,11)

norm = colors.BoundaryNorm(boundaries=bounds,ncolors=256)

h = plt.scatter(data['Longitude'], data['Latitude'],
            c=data['tau_QcondWL'], 
            cmap=plt.get_cmap("RdBu"), 
            transform=ccrs.PlateCarree(),
            norm = norm,s=10)


# divider = make_axes_locatable(ax)
# ax_cb = divider.new_horizontal(size="3%", pad=0.05, axes_class=plt.Axes)
# fig.add_axes(ax_cb)
# cbars = plt.colorbar(h, cax=ax_cb)

divider = make_axes_locatable(ax)
ax_cb = divider.new_horizontal(size="3%", pad=0.05, axes_class=plt.Axes)
fig.add_axes(ax_cb)

cbars = plt.colorbar(h, cax=ax_cb,extend = 'both')


cbars.set_label(r'$\tau$', fontsize=10)

# plt.clim(-0.30,0.5);

# ax.set_ylabel("Latitude", fontsize=14)
# ax.set_xlabel("Longitude", fontsize=14)
ax.set_title('$Q_{cond}$WL',fontsize=10)

axins = inset_axes(ax, width="40%", height="40%", loc="lower right", 
                   axes_class=cartopy.mpl.geoaxes.GeoAxes, 
                   axes_kwargs=dict(map_projection=cartopy.crs.PlateCarree()))

axins.add_feature(cfeat.LAND,color = 'lightgrey')
axins.add_feature(cfeat.OCEAN, color = 'white')
axins.add_feature(cfeat.COASTLINE, alpha=1, color = 'black',linewidth = 0.5)

axins.set_extent([-71.9,-74.2,45.5,46.7])
axins.xaxis.set_visible(False)
axins.yaxis.set_visible(False)

# cmap = matplotlib.cm.seismic
# bounds = np.array([-0.3,-0.2,-0.1,0,0.1, 0.2,0.3, 0.4,0.5])
# norm = colors.BoundaryNorm(boundaries=bounds,ncolors=256)

h=axins.scatter(data['Longitude'], data['Latitude'],
            c=data['tau_QcondWL'], 
            cmap=plt.get_cmap("RdBu"), 
            transform=ccrs.PlateCarree(),
            norm = norm,s=10)


ax = fig.add_subplot(2,2,1,projection = ccrs.PlateCarree())

ax.add_feature(cfeat.LAND,color = 'lightgrey')
ax.add_feature(cfeat.OCEAN, color = 'white')
ax.add_feature(cfeat.COASTLINE, alpha=1, color = 'black',linewidth = 0.5)

ax.set_extent([-74,-63,44,51])
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)

# add scatterplot onto the map
# cmap = colors.ListedColormap(['midnightblue', 'mediumblue','blue','slateblue','lightsteelblue','white','white','tomato','red','darkred'])

# bounds = np.linspace(-0.5,0.5,11)

# norm = colors.BoundaryNorm(boundaries=bounds,ncolors=256)

h=plt.scatter(data['Longitude'], data['Latitude'],
            c=data['tau_WLcondQ'], 
            cmap=plt.get_cmap("RdBu"), 
            transform=ccrs.PlateCarree(),
            norm = norm,s = 10)

# divider = make_axes_locatable(ax)
# ax_cb = divider.new_horizontal(size="3%", pad=0.05, axes_class=plt.Axes)
# fig.add_axes(ax_cb)

# cbars = plt.colorbar(h, cax=ax_cb,extend = 'both')

# cbars.set_label(r'$\tau$', fontsize=10)

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


# cmap = matplotlib.cm.seismic
# bounds = np.linspace(-0.5,0.5,11)
# norm = colors.BoundaryNorm(boundaries=bounds,ncolors=256)

h=axins.scatter(data['Longitude'], data['Latitude'],
            c=data['tau_WLcondQ'], 
            cmap=plt.get_cmap("RdBu"), 
            transform=ccrs.PlateCarree(),
            norm = norm,s=10)


# %% p-value plots

ax = fig.add_subplot(2,2,3,projection = ccrs.PlateCarree())



ax.add_feature(cfeat.LAND,color = 'lightgrey')
ax.add_feature(cfeat.OCEAN, color = 'white')
# ax.add_feature(cfeat.RIVERS)
# ax.add_feature(cfeat.LAKES)
ax.add_feature(cfeat.COASTLINE, alpha=1, color = 'black',linewidth = 0.5)
# ax.add_feature(cfeat.BORDERS,linestyle =':')


# extent for LOT2
ax.set_extent([-74,-63,44,51])
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)

# # extent for LOT3
# ax.set_extent([-71.9,-74.2,45.2,46.7])
# ax.xaxis.set_visible(True)
# ax.yaxis.set_visible(True)


# add scatterplot onto the map
cmap = colors.ListedColormap(['red', 'black'])
bounds=[0,0.05,0.5]
norm = colors.BoundaryNorm(bounds, cmap.N)

ax.scatter(data['Longitude'], data['Latitude'],
            c=data['pvalue_tau_WLcondQ'], 
            cmap=cmap, 
            transform=ccrs.PlateCarree(),
            norm = norm,s=10)


# divider = make_axes_locatable(ax)
# ax_cb = divider.new_horizontal(size="3%", pad=0.03, axes_class=plt.Axes)
# fig.add_axes(ax_cb)
# cbars = plt.colorbar(h, cax=ax_cb)

# cbars.set_label(r'$\tau$', fontsize=12)
# cbars = plt.colorbar(h, pad = 0.05, orientation="horizontal")

# plt.clim(0,1);

# ax.set_ylabel("Latitude", fontsize=14)
# ax.set_xlabel("Longitude", fontsize=14)
ax.set_title('P-value:$WL_{cond}$Q',fontsize=10)

axins = inset_axes(ax, width="40%", height="40%", loc="lower right", 
                   axes_class=cartopy.mpl.geoaxes.GeoAxes, 
                   axes_kwargs=dict(map_projection=cartopy.crs.PlateCarree()))

axins.add_feature(cfeat.LAND,color = 'lightgrey')
axins.add_feature(cfeat.OCEAN, color = 'white')
axins.add_feature(cfeat.COASTLINE, alpha=1, color = 'black',linewidth = 0.5)

axins.set_extent([-71.9,-74.2,45.5,46.7])
axins.xaxis.set_visible(False)
axins.yaxis.set_visible(False)

cmap = colors.ListedColormap(['red', 'black'])
bounds=[0,0.05,0.5]
norm = colors.BoundaryNorm(bounds, cmap.N)

h=axins.scatter(data['Longitude'], data['Latitude'],
            c=data['pvalue_tau_WLcondQ'], 
            cmap=cmap, 
            transform=ccrs.PlateCarree(),
            norm = norm,s=10)


ax = fig.add_subplot(2,2,4,projection = ccrs.PlateCarree())



ax.add_feature(cfeat.LAND,color = 'lightgrey')
ax.add_feature(cfeat.OCEAN, color = 'white')
# ax.add_feature(cfeat.RIVERS)
# ax.add_feature(cfeat.LAKES)
ax.add_feature(cfeat.COASTLINE, alpha=1, color = 'black',linewidth = 0.5)
# ax.add_feature(cfeat.BORDERS,linestyle =':')


# extent for LOT2
ax.set_extent([-74,-63,44,51])
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)

# # extent for LOT3
# ax.set_extent([-71.9,-74.2,45.2,46.7])
# ax.xaxis.set_visible(True)
# ax.yaxis.set_visible(True)


# add scatterplot onto the map
cmap = colors.ListedColormap(['red', 'black'])
bounds=[0,0.05,0.5]
norm = colors.BoundaryNorm(bounds, cmap.N)

ax.scatter(data['Longitude'], data['Latitude'],
            c=data['pvalue_tau_QcondWL'], 
            cmap=cmap, 
            transform=ccrs.PlateCarree(),
            norm = norm,s=10)


divider = make_axes_locatable(ax)
ax_cb = divider.new_horizontal(size="3%", pad=0.05, axes_class=plt.Axes)
fig.add_axes(ax_cb)
cbars = plt.colorbar(h, cax=ax_cb)

cbars.set_label('p-value', fontsize=10)
#cbars.set_label(r'$\tau$', fontsize=14)
# plt.clim(0,1);

ax.set_ylabel("Latitude", fontsize=12)
ax.set_xlabel("Longitude", fontsize=12)
ax.set_title('P-value:$Q_{cond}$WL',fontsize=10)

axins = inset_axes(ax, width="40%", height="40%", loc="lower right", 
                   axes_class=cartopy.mpl.geoaxes.GeoAxes, 
                   axes_kwargs=dict(map_projection=cartopy.crs.PlateCarree()))

axins.add_feature(cfeat.LAND,color = 'lightgrey')
axins.add_feature(cfeat.OCEAN, color = 'white')
axins.add_feature(cfeat.COASTLINE, alpha=1, color = 'black',linewidth = 0.5)

axins.set_extent([-71.9,-74.2,45.5,46.7])
axins.xaxis.set_visible(False)
axins.yaxis.set_visible(False)

cmap = colors.ListedColormap(['red', 'black'])
bounds=[0,0.05,0.5]
norm = colors.BoundaryNorm(bounds, cmap.N)

h=axins.scatter(data['Longitude'], data['Latitude'],
            c=data['pvalue_tau_QcondWL'], 
            cmap=cmap, 
            transform=ccrs.PlateCarree(),
            norm = norm,s=10)

plt.savefig('Figure4.png',bbox_inches='tight')













