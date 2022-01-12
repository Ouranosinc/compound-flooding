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

path = os.getcwd()
os.chdir('/mnt/705300_rehaussement_marin/3- Data/LOT2')
data = pd.read_csv('exutoires_LOT2.csv',encoding="ISO-8859-1", skiprows=0, index_col=False)

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

# add scatterplot onto the map

h=plt.scatter(data['Longitude'], data['Latitude'],
            c=data['rho_QcondWL'], 
            cmap=plt.get_cmap("brg",7), 
            transform=ccrs.PlateCarree())
divider = make_axes_locatable(ax)
ax_cb = divider.new_horizontal(size="5%", pad=0.1, axes_class=plt.Axes)
fig.add_axes(ax_cb)
cbars = plt.colorbar(h, cax=ax_cb)
cbars.set_label(r'$\rho$', fontsize=14)
#cbars.set_label(r'$\tau$', fontsize=14)
plt.clim(-0.3,0.3);
ax.set_ylabel("Latitude", fontsize=14)
ax.set_xlabel("Longitude", fontsize=14)
ax.set_title('QcondWL')
plt.savefig('rho_QcondWL.png',bbox_inches='tight')


# %% plot p-values


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
ax_cb = divider.new_horizontal(size="5%", pad=0.1, axes_class=plt.Axes)
fig.add_axes(ax_cb)
cbars = plt.colorbar(h, cax=ax_cb,norm=norm, boundaries=bounds, ticks=[0, 0.05, 0.5])
cbars.set_label(r'p-value($\tau$)', fontsize=14)
#cbars.set_label(r'$\tau$', fontsize=14)
plt.clim(0,1);
ax.set_ylabel("Latitude", fontsize=14)
ax.set_xlabel("Longitude", fontsize=14)
ax.set_title('QcondWL')
plt.savefig('pvalue_tau_QcondWL.png',bbox_inches='tight')




































