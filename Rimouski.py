# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 12:00:58 2021

@author: mohbiz1
"""

# Step 1: Read and join the csv water levels

from scipy import signal
#from scipy.fftpack import rfft, irfft, fftfreq, fft
import os
import pandas as pd
from glob import glob
#from datetime import timedelta
#import scipy.stats as stats
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
#from datetime import date
#from matplotlib.widgets import Cursor
import seaborn as sns
#import pingouin as pg

# %% Reading the station data

# check current working directory and change it to where the csv files reside
# path = os.getcwd()
os.chdir('/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT2/Rimouski/wl_hourly_data')
files = sorted(glob('2985-01-JAN-*_slev_UTC.csv'))

wl = pd.concat((pd.read_csv(file, encoding="ISO-8859-1", skiprows=7, index_col=False)
                for file in files))
wl['Date'] = pd.to_datetime(wl["Obs_date"])
wl['wl(m)'] = wl['SLEV(metres)']
wl = wl.set_index('Date')

wl = wl.drop(["Obs_date", 'SLEV(metres)'], axis=1)

# wl['wl(m)'] = wl['wl(m)']-1.135 # conversion of CD to CGVD28 for Belledune

wl['wl(m)'] = wl['wl(m)']-2.287 # conversion of CD to CGVD28

pth3 = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT2/Rimouski/wl_data_CGVD28.csv'
wl.to_csv(pth3, mode='w', index=True)

# %%



# name = 'au_Renard'
# pth2 = os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT2/'+name+'/wl_data_CGVD28.csv')
# wl= pd.read_csv(pth2, index_col = None)

# # To compare with extremes calculated using Zhang database (1979-2010)
# # data_wl = wl.loc['1979-01-01':'2010-12-31']

# # wl.reset_index(inplace=True)
# wl['Date'] = pd.to_datetime(wl['Date'])
# wl['year'] = pd.DatetimeIndex(wl['Date']).year
# wl['month'] = pd.DatetimeIndex(wl['Date']).month
# wl['day'] = pd.DatetimeIndex(wl['Date']).day
# wl = wl.set_index('Date')


# wl_max = data_wl.loc[data_wl.groupby("year")["wl"].idxmax()]

# pth3 = '/mnt/705300_rehaussement_marin/3- Data/LOT2/Belledune/wl_max.csv'
# wl_max.to_csv(pth3, mode='w', index=False)


# %% reading the tidal data of TPXO

path = os.getcwd()
os.chdir("/home/mohammad/Dossier_travail/Dossier_portable_Linux_Windows/OTPSnc")

data = pd.read_csv('Rimouski.out', sep="    ",  skiprows=4)
data[['lat', 'lon']] = data['Lat'].str.split(' ', 1, expand=True)
data = data.rename(columns={'   Lon': 'Date'})
data = data.rename(columns={'Unnamed: 2': 'z(m)'})
data = data.rename(columns={'mm.dd.yyyy hh:mm:ss': 'Depth(m)'})
data = data.drop(['Lat', ' z(m)   Depth(m)'], axis=1)
data['Date'] = pd.to_datetime(data["Date"])

# Originally, the dataset is in GMT, so it should be transformed to EST

# data['Date_EST'] = data['Date'].dt.tz_localize('GMT').dt.tz_convert('EST')

# dup = data[data.duplicated('Date_EST')]

# data = data.drop(['Date'], axis=1)
# data = data.rename(columns={'Date_EST': 'Date'})

# data['Date'] = pd.to_datetime(data["Date"])

# data['Date'] = data['Date'].dt.tz_localize(None)


# %% read Tide Harmonics tide time series at Belledune

name = 'Rimouski'
pth2 = os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT2/'+name+'/Tide_Harmonics.csv')
THarmonics= pd.read_csv(pth2, index_col = None)

THarmonics['Date'] = pd.to_datetime(THarmonics["Date"])

# %% 
df= pd.merge(data, THarmonics, on='Date', how='inner')


fig,ax = plt.subplots(1,1, sharex = False, figsize = (8,5), dpi = 300)
# sns.set(style='ticks', font_scale=1.2)
h = sns.lineplot(data=df, x="Tide_Harmonics", y = "Tide_Harmonics",color='blue', ci=None, linestyle='-', linewidth = 2)
g = sns.regplot(data=df, x="Tide_Harmonics", y="z(m)", scatter_kws={'color':'white','edgecolor':'black'},line_kws = {'color':'red'})

ax.set_ylabel('$Tide_{TPXO9}\ (m)$')
ax.set_xlabel('$Tide_{TideHarmonics}\ (m)$' )
ax.set_title('$(a)$')
ax.legend(['perfect-fit','data','least-square fit'])
#sns.despine()
plt.grid('on')
# plt.xlim([-1.3,1.5])
# plt.ylim([-1.3,1.5])


plt.savefig('/home/mohammad/Dossier_travail/705300_rehaussement_marin/paper/comparison_Tide_Rimouski.png', dpi=300)



# plot the differences in time
df['diff'] = df['Tide_Harmonics'] - df['z(m)']
df['month'] = df['Date'].dt.strftime('%b')
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
df['month'] = pd.Categorical(df['month'], categories=months, ordered=True)
df2 = df.sort_values(by='month',ascending=True)


# plot time series
fig, ax = plt.subplots(1, 1, sharex=True, figsize=(8, 5), dpi=300)
sns.boxplot(x = 'month', y = 'diff', data = df2, ax = ax)
# sns.despine()
plt.ylabel('$Tide_{TPXO}-Tide_{TideHarmonics}\ (m)$')
plt.grid('on')
ax.set_title('$(b)$')

plt.savefig('/home/mohammad/Dossier_travail/705300_rehaussement_marin/paper/monthly_delta_tide.png', dpi=300)

# %% calculating the storm surge time series

df['surge(m)'] = df['wl(m)'] - df['z(m)']

pth2 = os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT2/'+name+'/Mean_Sea_Level.csv')
Mean_Sea_Level= pd.read_csv(pth2, index_col = None)
Mean_Sea_Level['Date'] = pd.to_datetime(Mean_Sea_Level["Date"])

df= pd.merge(df, Mean_Sea_Level, on='Date', how='inner')

df['surge(m)'] = df['surge(m)'] + df['MSL']


pth2 = os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT2/'+name+'/Surge_UTC.csv')
df.to_csv(pth2, mode='w', index=False)


# %% constructing total water level at Petit Cascapedia and Ristigouche using strom surge extracted from Belledune station (Tide = TPXO)

path = os.getcwd()
os.chdir("/home/mohammad/Dossier_travail/Dossier_portable_Linux_Windows/OTPSnc")

data = pd.read_csv('Outardes.out', sep="    ",  skiprows=4)
data[['lat', 'lon']] = data['Lat'].str.split(' ', 1, expand=True)
data = data.rename(columns={'   Lon': 'Date'})
data = data.rename(columns={'Unnamed: 2': 'z(m)'})
data = data.rename(columns={'mm.dd.yyyy hh:mm:ss': 'Depth(m)'})
data = data.drop(['Lat', ' z(m)   Depth(m)'], axis=1)
data['Date'] = pd.to_datetime(data["Date"])

data = data.drop(['Depth(m)','lat','lon',], axis=1)

pth2 = os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT2/'+name+'/Surge_UTC.csv')
Surge= pd.read_csv(pth2, index_col = None)
Surge['Date'] = pd.to_datetime(Surge["Date"])

Surge = Surge.drop(['Depth(m)','lat','lon','Tide_Harmonics','wl(m)','diff','month','MSL','z(m)'], axis=1)

df= pd.merge(Surge, data, on='Date', how='inner')

df['wl(m)'] = df['z(m)'] + df['surge(m)']

# %% change the time from UTC to EST for subsequent creation of the joint datasets (WLcondQ and QcondWL)

df['Date_EST'] = df['Date'].dt.tz_localize('UTC').dt.tz_convert('EST')
df = df.drop_duplicates(subset=['Date'])
df = df.drop(['Date'], axis=1)
df = df.rename(columns={'Date_EST': 'Date'})

df['Date'] = df['Date'].dt.tz_localize(None)
pth2 = os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT2/Outardes/wl_data_CGVD28.csv')
df.to_csv(pth2, mode='w', index=False,columns=['Date','wl(m)'])




# %%

# Tr = pd.DataFrame({'Date': df_Renardd['Date'],
#                    'MSL': df_Renardd['MSL'],
#                   'Residual': df_Renardd['Residual']})


# # here id is common column
# df_Renard= pd.merge(data, Tr, on='Date', how='inner')

# df_Renard = df_Renard.rename(columns={'z(m)': 'TD(m)'})

# df_Renard['TD_est'] = df_Renard['TD(m)'] + df_Renard['MSL']


# df_Renard['wl'] = df_York['Residual'] + df_Renard['TD_est']

# df_Renard['year'] = pd.DatetimeIndex(df_Renard['Date']).year


# wl_max_Renard= df_Renard.loc[df_Renard.groupby("year")["wl"].idxmax()]


# pth3 = '/mnt/705300_rehaussement_marin/3- Data/LOT2/York/wl_max.csv'
# wl_max_Renard.to_csv(pth3, mode='w', index=False)

# pth3 = '/mnt/705300_rehaussement_marin/3- Data/LOT2/York/totalwl_and_tide.csv'
# df_York.to_csv(pth3, mode='w', index=False)


# # %matplotlib qt
# fig, ax = plt.subplots(1, 1, sharex=True, figsize=(8, 4), dpi=300)
# ax.plot(df_Rimouskii['Date'][119032:119775],
#         df_Rimouskii['wl'][119032:119775], label='Rimouski')
# #ax.plot(df_Matane['Date'][119032:119775], df_Matane['wl'][119032:119775],label='Matane')
# #ax.plot(df_inner['Date'], df_inner['wl'], label='WL')
# ax.set_ylabel('Water Level (m)')
# ax.set_xlabel('Date')
# ax.legend()
# plt.grid('on')
# ax.spines['top'].set_visible(False)
# ax.spines['right'].set_visible(False)


# plt.savefig(r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\LOT2\Rimouski\Mitis_Rimouski2.png')

# fig, ax = plt.subplots(1, 1, sharex=True, figsize=(8, 4), dpi=300)
# #ax.plot(df_inner['Date'], df_inner['TD(m)'],label='TD')
# #ax.plot(df_Mitis['Date'][-1000:], df_Mitis['wl'][-1000:],label='Mitis')
# ax.scatter(df_Rimouski['wl'], df_Mitis['wl'],
#            facecolors="k", s=5, edgecolors="none", zorder=2)
# #ax.plot(df_inner['Date'], df_inner['wl'], label='WL')
# ax.set_ylabel('WL at Rimouski')
# ax.set_xlabel('WL at Mitis')
# ax.legend()
# plt.grid('on')
# ax.spines['top'].set_visible(False)
# ax.spines['right'].set_visible(False)
# plt.savefig('C:/Users/mohbiz1/Desktop/Dossier_travail/705300_rehaussement_marin/3- Data/DFO-MPO/LOT1/A_Mars/linear_Saguenay_a_mars_daily_max_complete_cycle.png')


# %%


# pth = r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\LOT2\Rimouski\totalwl_and_tide.csv'
# wl = pd.read_csv(pth, index_col=None, parse_dates={
#                  "date": ["year", "month", "day"]})


# # %% comparison of Tide Harmonics Tide and TPXO

# pth = '/mnt/705300_rehaussement_marin/3- Data/LOT2/Rimouski/Tide_Harmonics_vs_TPXO.csv'
# data = pd.read_csv(pth, index_col=None)
# data = data.drop(['Unnamed: 0'], axis=1)
# data = data.rename(columns={'Tide_Tide_Harmonics': 'T_TH'})
# data = data.rename(columns={'c.data...TD.m.....': 'T_TPXO'})
# data = data.rename(columns={'c.data.Date.': 'Date'})

# pg.corr(data['T_TH'], data['T_TPXO'], method='pearson')


# plt.subplots(1, 1, sharex=True, figsize=(8, 8), dpi=300)
# sns.set(style='ticks', font_scale=1.2)
# g = sns.scatterplot(data=data, x="T_TH", y="T_TPXO", color="r")
# plt.xlabel('T_TH(m)')
# plt.ylabel('T_TPXO(m)')
# sns.despine()
# plt.savefig('/mnt/705300_rehaussement_marin/3- Data/LOT2/Rimouski/comparison_Tide_Rimouski.png', dpi=300)

# # plot the differences in time
# data['diff'] = data['T_TH'] - data['T_TPXO']
# data['Date'] = pd.to_datetime(data["Date"])
# data['month'] = data['Date'].dt.strftime('%b')
# # plot time series
# fig, ax = plt.subplots(1, 1, sharex=True, figsize=(8, 4), dpi=300)
# sns.boxplot(x = 'month', y = 'diff', data = data, ax = ax)
# sns.despine()
# plt.ylabel('DeltaTide(m)')
# plt.savefig('/mnt/705300_rehaussement_marin/3- Data/LOT2/Rimouski/monthly_delta_tide.png', dpi=300)

# # plot tides in 2019

# data = data.set_index('Date')
# Tide_nov_2019  = data.loc['2019-11-01':'2019-11-30']  # 52

# fig, ax = plt.subplots(1, 1, sharex=True, figsize=(12, 4), dpi=300)
# sns.lineplot(x = 'Date', y = 'T_TPXO', data = Tide_nov_2019, ax = ax,label = 'T_TPXO')
# sns.lineplot(x = 'Date', y = 'T_TH', data = Tide_nov_2019, ax = ax, label = 'T_TH')
# sns.despine()
# plt.ylabel('Tide level(m)')
# dateform = DateFormatter("%m/%d")
# ax.xaxis.set_major_formatter(dateform)
# plt.savefig('/mnt/705300_rehaussement_marin/3- Data/LOT2/Rimouski/Tide_delta_November.png', dpi=300)








