
## Script for creating the Figure 5 of the report
## Author: Mohammad Bizhanimanzar
## This script creates the Figure 5 of the report. Time series of water level, along with their annual maxima (red circles), 
## and conditioned maximum water level (WLcondQ) are show in this Figure.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import datetime
from datetime import timedelta
import os

# %% reading the estimated water level data at Mitis, Matane, et Outardes
name = 'Petit_Cascapedia'
pth = os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT2/'+name+'/wl_data.csv')
data_wl= pd.read_csv(pth, index_col = None)


data_wl['Date'] = pd.to_datetime(data_wl['Date'])
data_wl = data_wl.set_index('Date')
data_wl = data_wl.loc['1968-01-01':'2019-12-31']  

# finding annual maxima along with its day, month, year

data_wl.reset_index(inplace=True) 
data_wl['year'] = pd.DatetimeIndex(data_wl['Date']).year
data_wl['month'] = pd.DatetimeIndex(data_wl['Date']).month
data_wl['day'] = pd.DatetimeIndex(data_wl['Date']).day

wl_max =data_wl.loc[data_wl.groupby("year")["wl(m)"].idxmax()]

# To plot the water level annual maxima

wl_max =  wl_max.drop(['year', 'month','day'], axis=1)
wl_max = wl_max.set_index('Date')
wl_max = wl_max.squeeze()



wl_plt =  data_wl.drop(['year', 'month','day'], axis=1)
wl_plt = wl_plt.set_index('Date')
wl_plt_s = wl_plt.squeeze()


pth2 = os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT2/'+name+'/WLcondQ.csv')
wlcond = pd.read_csv(pth2, index_col = None,parse_dates= {"date" : ["year","month","day"]})
wlcond =  wlcond.drop(['Date','Qmax'], axis=1)
wlcond = wlcond.set_index('date')
wlcond = wlcond.squeeze()


# step 4: extracting annual maxima for flow discharges

fig,ax = plt.subplots(1,1,sharex = True,figsize=(5, 2),dpi=300)
wl_plt_s.plot(c= "dodgerblue",linewidth=0.2,zorder=0)
wl_max.plot(style = '.r',zorder=1)
plt.scatter(wlcond.index,wlcond,facecolors="k", s=5,edgecolors="none",zorder=2)
plt.grid(which='both')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.title(name, fontsize=10)
ax.set_ylim(min(wl_plt_s-1),max(wl_plt_s+1))
plt.ylabel('Niveau deau (m)')
plt.savefig('/mnt/705300_rehaussement_marin/3- Data/LOT2/WLmax_annual_Mitis.png')





