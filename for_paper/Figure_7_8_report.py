"""
This script plots the Kendall's correlation coefficient as well as the corresponding p-value for the river outlets (Figures 7 and 8). The data are stored in a 
excel file (exutoires_LOT2_cartopy.csv).
"""

import matplotlib.pyplot as plt 
import cartopy.crs as ccrs
import cartopy
import cartopy.feature as cfeat
import cartopy.io.shapereader as shpr
import os
import pandas as pd
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib import colors
import matplotlib
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker

path = os.getcwd()
os.chdir('/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT2')
data = pd.read_csv('exutoires_LOT2_cartopy.csv',encoding="ISO-8859-1", skiprows=0, index_col=False)

# plots

fig = plt.figure(figsize=(8,8),dpi=300)
ax = fig.add_subplot(2,1,1,projection = ccrs.PlateCarree())

ax.add_feature(cfeat.LAND,color = 'wheat')
ax.add_feature(cfeat.OCEAN, color = 'gainsboro')
# ax.add_feature(cfeat.RIVERS)
# ax.add_feature(cfeat.LAKES)
ax.add_feature(cfeat.COASTLINE, alpha=0.5)


# extent for LOT2
ax.set_extent([-73.1,-64.1,45.8,49.4])
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)

# # extent for LOT3
# ax.set_extent([-71.9,-74.2,45.2,46.7])
# ax.xaxis.set_visible(True)
# ax.yaxis.set_visible(True)


# add scatterplot onto the map
# cmap = matplotlib.cm.seismic
cmap = colors.ListedColormap(['midnightblue', 'mediumblue','blue','slateblue','lightsteelblue','white','white','tomato','red','darkred'])

bounds = np.array([-0.3,-0.25,-0.2, -0.15,-0.1, -0.05, 0, 0.05, 0.1, 0.15, 0.2])

norm = colors.BoundaryNorm(boundaries=bounds,ncolors=cmap.N)

h=plt.scatter(data['Longitude'], data['Latitude'],
            c=data['tau_QcondWL'], 
            cmap=cmap, 
            transform=ccrs.PlateCarree(),
            norm = norm)


divider = make_axes_locatable(ax)
ax_cb = divider.new_horizontal(size="3%", pad=0.03, axes_class=plt.Axes)
fig.add_axes(ax_cb)
cbars = plt.colorbar(h, cax=ax_cb, ticks=[-0.3,-0.25,-0.2, -0.15,-0.1, -0.05, 0, 0.05, 0.1, 0.15, 0.2])

cbars.set_label(r'$\tau$', fontsize=14)
plt.clim(-0.30,0.2);

ax.set_ylabel("Latitude", fontsize=14)
ax.set_xlabel("Longitude", fontsize=14)
ax.set_title('QcondWL')

gl = ax.gridlines(crs=ccrs.PlateCarree(), linewidth=0.5, color='black', alpha=0.5, linestyle='--', draw_labels=True)
gl.xlabels_top = False
gl.ylabels_left = False
gl.ylabels_right=True
gl.xlines = True
gl.xlocator = mticker.FixedLocator([-72, -71, -70,-69,-68,-67,-66,-65])
gl.ylocator = mticker.FixedLocator([46.5,47.0,47.5,48.0,48.5,49.0])
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
gl.xlabel_style = {'color': 'black'}
gl.left_labels = True
gl.right_labels = False




plt.savefig('tau_QcondWL_R2_v2.png',bbox_inches='tight')


# %% plot p-values


fig = plt.figure(figsize=(8,8),dpi=300)
ax = fig.add_subplot(2,1,2,projection = ccrs.PlateCarree())

ax.add_feature(cfeat.LAND,color = 'wheat')
ax.add_feature(cfeat.OCEAN, color = 'gainsboro')
#ax.add_feature(cfeat.OCEAN)
# ax.add_feature(cfeat.RIVERS)
# ax.add_feature(cfeat.LAKES)
ax.add_feature(cfeat.COASTLINE, alpha=0.5)
# ax.add_feature(cfeat.BORDERS,linestyle =':')

ax.set_extent([-73.1,-64.1,45.8,49.4])
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)


# extent for LOT3
# ax.set_extent([-71.9,-74.2,45.2,46.7])
# ax.xaxis.set_visible(True)
# ax.yaxis.set_visible(True)


# add scatterplot onto the map
cmap = colors.ListedColormap(['red', 'black'])
bounds=[0,0.05,0.5]
norm = colors.BoundaryNorm(bounds, cmap.N)

h=plt.scatter(data['Longitude'], data['Latitude'],
            c=data['pvalue_tau_QcondWL'], 
            cmap=cmap, 
            transform=ccrs.PlateCarree(),
            norm = norm)

divider = make_axes_locatable(ax)
ax_cb = divider.new_horizontal(size="3%", pad=0.03, axes_class=plt.Axes)
fig.add_axes(ax_cb)
cbars = plt.colorbar(h, cax=ax_cb,norm=norm, boundaries=bounds, ticks=[0, 0.05, 0.5])
cbars.set_label(r'p-value($\tau$)', fontsize=14)
#cbars.set_label(r'$\tau$', fontsize=14)
plt.clim(0,1);
ax.set_ylabel("Latitude", fontsize=14)
ax.set_xlabel("Longitude", fontsize=14)
ax.set_title('P-value: QcondWL')
gl = ax.gridlines(crs=ccrs.PlateCarree(), linewidth=0.5, color='black', alpha=0.5, linestyle='--', draw_labels=True)
gl.xlabels_top = False
gl.ylabels_left = False
gl.ylabels_right=True
gl.xlines = True
gl.xlocator = mticker.FixedLocator([-72, -71, -70,-69,-68,-67,-66,-65])
gl.ylocator = mticker.FixedLocator([46.5,47.0,47.5,48.0,48.5,49.0])
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
gl.xlabel_style = {'color': 'black'}
gl.left_labels = True
gl.right_labels = False

plt.savefig('p_value_QcondWL.png',bbox_inches='tight')



# %% plot the map of projected sea level rise


import matplotlib.pyplot as plt 
import cartopy.crs as ccrs
import cartopy
import cartopy.feature as cfeat
import cartopy.io.shapereader as shpr
import os
import pandas as pd
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib as mpl



path = os.getcwd()
os.chdir('/mnt/705300_rehaussement_marin/3- Data/LOT2')
data = pd.read_csv('rehaussement_marin_LOT2.csv',encoding="ISO-8859-1", skiprows=0, index_col=False)

# plots

fig = plt.figure(figsize=(8,8),dpi=300)
ax = fig.add_subplot(1,1,1,projection = ccrs.PlateCarree())

ax.add_feature(cfeat.LAND,color = 'gainsboro')
#ax.add_feature(cfeat.OCEAN)
ax.add_feature(cfeat.RIVERS)
ax.add_feature(cfeat.LAKES)
ax.add_feature(cfeat.COASTLINE, alpha=0.5)
ax.add_feature(cfeat.BORDERS,linestyle =':')

ax.set_extent([-73.1,-64.1,45.8,49.4])
ax.xaxis.set_visible(True)
ax.yaxis.set_visible(True)



# Define the color map

cmap = plt.cm.jet
cmaplist = [cmap(i) for i in range(cmap.N)]

cmap = mpl.colors.LinearSegmentedColormap.from_list(
    'Custom cmap', cmaplist, cmap.N)

bounds = np.linspace(40, 70, 10)
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

# add scatterplot onto the map

h=plt.scatter(data['Longitude'], data['Latitude'],
            c=data['RM'], 
            cmap=cmap, 
            transform=ccrs.PlateCarree())

divider = make_axes_locatable(ax)
ax_cb = divider.new_horizontal(size="5%", pad=0.1, axes_class=plt.Axes)
fig.add_axes(ax_cb)

cb = plt.colorbar(h, cax = ax_cb, cmap=cmap, norm=norm,
    spacing='proportional', ticks=bounds, boundaries=bounds, format='%2i')

# cbars = plt.colorbar(h, cax=ax_cb)
cb.set_label('Rehaussement marin [cm]', fontsize=14)
#cbars.set_label(r'$\tau$', fontsize=14)
plt.clim(40,70);
ax.set_ylabel("Latitude", fontsize=14)
ax.set_xlabel("Longitude", fontsize=14)
ax.set_title('Rehaussement marin [cm], RCP=8.5, horizon 2070')
plt.savefig('rehaussement_marin.png',bbox_inches='tight')




































