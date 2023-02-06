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




pth = ('/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT2/rehaussement_marin_LOT2.csv')
data = pd.read_csv(pth,encoding="ISO-8859-1", skiprows=0, index_col=False)


data = data.drop({3,11})

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

for axis in ['top', 'bottom', 'left', 'right']:
    ax.spines[axis].set_color('black')    # change color





# Define the color map

cmap = plt.cm.viridis
cmaplist = [cmap(i) for i in range(cmap.N)]

cmap = mpl.colors.LinearSegmentedColormap.from_list(
    'Custom cmap', cmaplist, cmap.N)

bounds = np.linspace(40, 70, 10)
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

# add scatterplot onto the map

h=plt.scatter(data['Longitude'], data['Latitude'],
            c=data['RM'], 
            cmap=cmap, 
            transform=ccrs.PlateCarree(), s= 5)

divider = make_axes_locatable(ax)
ax_cb = divider.new_horizontal(size="3%", pad=0.05, axes_class=plt.Axes)
fig.add_axes(ax_cb)

cb = plt.colorbar(h, cax = ax_cb, cmap=cmap, norm=norm,
    spacing='proportional', boundaries=bounds, format='%2i')
cb.outline.set_visible(False)

cb.ax.tick_params(labelsize=5) 



# cb.set_label('Rehaussement marin [cm]', fontsize = 8)
# cbars = plt.colorbar(h, cax=ax_cb,extend = 'neither')

plt.clim(40,70);
# ax.set_ylabel("Latitude", fontsize=14)
# ax.set_xlabel("Longitude", fontsize=14)
ax.set_title('Rehaussement marin [cm], RCP=8.5, horizon 2100', fontsize = 5)

plt.savefig('rehaussement_marin.png',bbox_inches='tight')




































