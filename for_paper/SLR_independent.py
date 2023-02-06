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




pth = ('/home/mohammad/Dossier_travail/705300_rehaussement_marin/paper/Multiplication_Factor.xlsx')
data = pd.read_excel(pth, sheet_name = 'Multiplication_Factor_QcondWL', index_col=False)


data = data.drop({3,11})

# plots
fig,axes = plt.subplots(4, 2, dpi = 300)
scenarios = [data['Scenario1'], data['Scenario2'], data['Scenario3'], data['Scenario4'], data['Scenario5'], data['Scenario6'],data['Scenario7'],data['Scenario8']]
labels = ["Scenario 1","Scenario 2","Scenario 3","Scenario 4","Scenario 5","Scenario 6","Scenario 7","Scenario 8"]
i=0
for i in range(8):
    
        # ax = plt.subplot2grid((4,2), (3, 0), colspan=2,projection = ccrs.PlateCarree())
        ax = plt.subplot(4, 2, i+1,projection = ccrs.PlateCarree())
        ax.add_feature(cfeat.LAND,color = 'lightgrey')
        ax.add_feature(cfeat.OCEAN, color = 'white')
        ax.add_feature(cfeat.COASTLINE, alpha=1, color = 'black',linewidth = 0.5)
    
        ax.set_extent([-74,-63,44,51])
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)
        cmap = plt.cm.viridis
        cmaplist = [cmap(i) for i in range(cmap.N)]
    
        cmap = mpl.colors.LinearSegmentedColormap.from_list('Custom cmap', cmaplist, cmap.N)
    
        bounds = np.linspace(1, 50, 50)
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    
        # add scatterplot onto the map
    
        h=ax.scatter(data['Longitude'], data['Latitude'],
                c=scenarios[i], 
                cmap=cmap, 
                transform=ccrs.PlateCarree(), norm = norm, s= 5)
        ax.set_title(f"{labels[i]}")
        
        if i==7:
            cmap = plt.cm.viridis
            cmaplist = [cmap(i) for i in range(cmap.N)]
        
            cmap = mpl.colors.LinearSegmentedColormap.from_list('Custom cmap', cmaplist, cmap.N)
        
            bounds = np.linspace(1, 50, 50)            
            norm = mpl.colors.BoundaryNorm(bounds, cmap.N,extend = 'max')
            divider = make_axes_locatable(ax)
            ax_cb = divider.new_horizontal(size="3%", pad=0.05, axes_class=plt.Axes)
            fig.add_axes(ax_cb)
        
            cb = plt.colorbar(h, cax = ax_cb, cmap=cmap, norm=norm,spacing='proportional', boundaries=bounds, format='%2i')
            cb.outline.set_visible(False)
        
            cb.ax.tick_params(labelsize=5) 
            ax.set_title(f"{labels[i]}")
        i = i +1
fig.tight_layout(pad = 0.05)
plt.savefig('RM_independnet_QcondWL.png',bbox_inches='tight')





# divider = make_axes_locatable(ax)
# ax_cb = divider.new_vertical(size="3%", pad=0.05)
# fig.add_axes(ax_cb)

# # cmap = plt.cm.viridis
# # cmaplist = [cmap(i) for i in range(cmap.N)]

# # cmap = mpl.colors.LinearSegmentedColormap.from_list('Custom cmap', cmaplist, cmap.N)

# # bounds = np.linspace(1, 50, 50)
# # norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
        
# cb = plt.colorbar(h, cax = ax_cb,cmap=cmap, norm=norm,
#     spacing='proportional', boundaries=bounds, format='%2i')
# # cb.outline.set_visible(False)

# cb.ax.tick_params(labelsize=5) 





# fig = plt.figure(dpi=300)
# ax = fig.add_subplot(2,2,1,projection = ccrs.PlateCarree())



# for axis in ['top', 'bottom', 'left', 'right']:
#     ax.spines[axis].set_color('black')    # change color





# Define the color map





# cb.set_label('Rehaussement marin [cm]', fontsize = 8)
# cbars = plt.colorbar(h, cax=ax_cb,extend = 'neither')

plt.clim(40,70);
# ax.set_ylabel("Latitude", fontsize=14)
# ax.set_xlabel("Longitude", fontsize=14)
ax.set_title('Rehaussement marin [cm], RCP=8.5, horizon 2100', fontsize = 5)







