"""
This script plots the projected sea level rise at the river outlets (Figures 20 of the report LOT2). The data are stored in a 
excel file (rehaussement_marin_LOT2.csv).

Author: Mohammad Bizhanimanzar

"""

# %% plot the map of projected sea level rise


import matplotlib.pyplot as plt 
import cartopy.crs as ccrs
import cartopy.feature as cfeat
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

cb.set_label('Rehaussement marin [cm]', fontsize=14)
plt.clim(40,70);
ax.set_ylabel("Latitude", fontsize=14)
ax.set_xlabel("Longitude", fontsize=14)
ax.set_title('Rehaussement marin [cm], RCP=8.5, horizon 2070')
plt.savefig('rehaussement_marin.png',bbox_inches='tight')




































