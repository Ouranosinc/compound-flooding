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

# check current working directory and change it to where the csv files reside
path = os.getcwd()
os.chdir('/mnt/705300_rehaussement_marin/3- Data/LOT2/Au_Renard/wl_hourly_data')
files = sorted(glob('2330-01-JAN-*_slev.csv'))

wl = pd.concat((pd.read_csv(file, encoding="ISO-8859-1", skiprows=0, index_col=False)
                for file in files))
wl['Date'] = pd.to_datetime(wl["Date_d'observation"])
wl['wl'] = wl['SLEV(mètres)']
wl = wl.set_index('Date')

wl = wl.drop(["Date_d'observation", 'SLEV(mètres)'], axis=1)

# To compare with extremes calculated using Zhang database (1979-2010)
data_wl = wl.loc['1979-01-01':'2010-12-31']

wl.reset_index(inplace=True)
wl['year'] = pd.DatetimeIndex(wl['Date']).year
wl['month'] = pd.DatetimeIndex(wl['Date']).month
wl['day'] = pd.DatetimeIndex(wl['Date']).day


wl_max = data_wl.loc[data_wl.groupby("year")["wl"].idxmax()]

pth3 = '/mnt/705300_rehaussement_marin/3- Data/LOT2/Belledune/wl_max.csv'
wl_max.to_csv(pth3, mode='w', index=False)


# %% reading the tidal data of TPXO

path = os.getcwd()
os.chdir("/mnt/Dossier_portable_Linux_Windows/OTPSnc")

data = pd.read_csv('York.out', sep="    ",  skiprows=4)
data[['lat', 'lon']] = data['Lat'].str.split(' ', 1, expand=True)
data = data.rename(columns={'   Lon': 'Date'})
data = data.rename(columns={'Unnamed: 2': 'z(m)'})
data = data.rename(columns={'mm.dd.yyyy hh:mm:ss': 'Depth(m)'})
data = data.drop(['Lat', ' z(m)   Depth(m)'], axis=1)
data['Date'] = pd.to_datetime(data["Date"])

# Originally, the dataset is in GMT, so it should be transformed to EST

data['Date_EST'] = data['Date'].dt.tz_localize('GMT').dt.tz_convert('EST')

dup = data[data.duplicated('Date_EST')]

data = data.drop(['Date'], axis=1)
data = data.rename(columns={'Date_EST': 'Date'})

data['Date'] = pd.to_datetime(data["Date"])

data['Date'] = data['Date'].dt.tz_localize(None)

# %% intersecting the two datasewts TPXO and observed water levels
#data = data.drop_duplicates(subset=['Date'])

# here id is common column
df_Renard= pd.merge(data, wl, on='Date', how='inner')

df_Renard = df_Renard.drop(['Depth(m)'], axis=1)

df_Renard = df_Renard.rename(columns={'z(m)': 'TD(m)'})


wl_mean_annual = df_Renard.groupby(df_Renard.Date.dt.year)[
    'wl'].transform('mean')

wl_mean_annual.name = 'MSL'

wl_mean_annual = wl_mean_annual.to_frame()
wl_mean_annual['Date'] = df_Renard['Date']

df_Renard.reset_index(drop=True)
wl_mean_annual.reset_index(drop=True)

df_Renardd = wl_mean_annual.join(
    df_Renard, rsuffix='_r')  # here id is common column


df_Renardd = df_Renardd.drop(['Date_r'], axis=1)

MSL = df_Renard['wl'].mean()

#df_Rimouski['TD(m)'] = df_Rimouski['TD(m)'] +MSL

#df_Rimouski['Residual'] = df_Rimouski['wl'] - df_Rimouski['TD(m)']

df_Renardd['TD_obs'] = df_Renardd['TD(m)'] + df_Renardd['MSL']


df_Renardd['Residual'] = df_Renardd['wl'] - df_Renardd['TD_obs']


pth3 = '/mnt/705300_rehaussement_marin/3- Data/LOT2/Au_Renard/totalwl_and_tide.csv'
df_Renardd.to_csv(pth3, mode='w', index=False)

# %%
#y = df_Rimouski['Residual'].to_numpy()
# plot power spectrum to identify the


n = 292831  # number of points
Lx = 1  # time step = 1 hr
y = df_Rimouski['Residual'].to_numpy()
# Return the Discrete Fourier Transform sample frequencies.
W = fftfreq(292831, 1)
f_signal = fft(y)

fig, ax = plt.subplots(1, 1, sharex=True, figsize=(8, 4), dpi=300)
ax.plot(abs(W), abs(f_signal))
plt.xlabel('Frequency (1/day)')


lowcut = (1/(11*2))
highcut = (1/(14*2))
fs = 1  # sampling frequency in Hz = 1 value every 1 hr
order = 3


nyq = 0.5 * fs
low = lowcut / nyq
high = highcut / nyq
b, a = signal.butter(order, [low, high], btype='bandstop')

yf = signal.filtfilt(b, a, y)

yfdf = pd.DataFrame({'yf': yf})

df_inner = df_inner.drop(['yf'], axis=1)

df_inner = df_inner.join(yfdf)
df_inner['yf'] = df_inner['yf'].fillna(0)


# %%

fig, ax = plt.subplots(1, 1, sharex=True, figsize=(8, 4), dpi=300)
#ax.plot(df_inner['Date'], df_inner['TD(m)'],label='TD')
#ax.plot(df_Rimouski['Date'], df_Rimouski['MSL'],label='Mean_annual_water level')
ax.plot(df_Rimouski['Date'][-1000:],
        df_Rimouski['Residual'][-1000:], label='Residual')
# ax.plot(df_Rimouski['Date'][-5000:], df_Rimouski['TD_obs'][-5000:],label='TD')
# ax.plot(df_Rimouski['Date'][-5000:], df_Rimouski['wl'][-5000:], label='WL')
ax.set_ylabel('Water Level (m)')
ax.set_xlabel('Date')
ax.legend()
plt.grid('on')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.savefig(r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\LOT2\Rimouski\Residual2.png')


# %% constructing Mitis total water level, TR = non-deterministic tide + storm surge

TR = pd.DataFrame({'Date': df_Renardd['Date'],
                   'MSL': df_Renardd['MSL'],
                  'Residual': df_Renardd['Residual']})


# here id is common column
df_York= pd.merge(data, TR, on='Date', how='inner')

df_York = df_York.rename(columns={'z(m)': 'TD(m)'})

df_York['TD_est'] = df_York['TD(m)'] + df_York['MSL']


df_York['wl'] = df_York['Residual'] + df_York['TD_est']

df_York['year'] = pd.DatetimeIndex(df_York['Date']).year


wl_max_York= df_York.loc[df_York.groupby("year")["wl"].idxmax()]


pth3 = '/mnt/705300_rehaussement_marin/3- Data/LOT2/York/wl_max.csv'
wl_max_York.to_csv(pth3, mode='w', index=False)

pth3 = '/mnt/705300_rehaussement_marin/3- Data/LOT2/York/totalwl_and_tide.csv'
df_York.to_csv(pth3, mode='w', index=False)


# %matplotlib qt
fig, ax = plt.subplots(1, 1, sharex=True, figsize=(8, 4), dpi=300)
ax.plot(df_Rimouskii['Date'][119032:119775],
        df_Rimouskii['wl'][119032:119775], label='Rimouski')
#ax.plot(df_Matane['Date'][119032:119775], df_Matane['wl'][119032:119775],label='Matane')
#ax.plot(df_inner['Date'], df_inner['wl'], label='WL')
ax.set_ylabel('Water Level (m)')
ax.set_xlabel('Date')
ax.legend()
plt.grid('on')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)


plt.savefig(r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\LOT2\Rimouski\Mitis_Rimouski2.png')

fig, ax = plt.subplots(1, 1, sharex=True, figsize=(8, 4), dpi=300)
#ax.plot(df_inner['Date'], df_inner['TD(m)'],label='TD')
#ax.plot(df_Mitis['Date'][-1000:], df_Mitis['wl'][-1000:],label='Mitis')
ax.scatter(df_Rimouski['wl'], df_Mitis['wl'],
           facecolors="k", s=5, edgecolors="none", zorder=2)
#ax.plot(df_inner['Date'], df_inner['wl'], label='WL')
ax.set_ylabel('WL at Rimouski')
ax.set_xlabel('WL at Mitis')
ax.legend()
plt.grid('on')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.savefig('C:/Users/mohbiz1/Desktop/Dossier_travail/705300_rehaussement_marin/3- Data/DFO-MPO/LOT1/A_Mars/linear_Saguenay_a_mars_daily_max_complete_cycle.png')


# %%


pth = r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\LOT2\Rimouski\totalwl_and_tide.csv'
wl = pd.read_csv(pth, index_col=None, parse_dates={
                 "date": ["year", "month", "day"]})


# %% comparison of Tide Harmonics Tide and TPXO

pth = '/mnt/705300_rehaussement_marin/3- Data/LOT2/Rimouski/Tide_Harmonics_vs_TPXO.csv'
data = pd.read_csv(pth, index_col=None)
data = data.drop(['Unnamed: 0'], axis=1)
data = data.rename(columns={'Tide_Tide_Harmonics': 'T_TH'})
data = data.rename(columns={'c.data...TD.m.....': 'T_TPXO'})
data = data.rename(columns={'c.data.Date.': 'Date'})

pg.corr(data['T_TH'], data['T_TPXO'], method='pearson')


plt.subplots(1, 1, sharex=True, figsize=(8, 8), dpi=300)
sns.set(style='ticks', font_scale=1.2)
g = sns.scatterplot(data=data, x="T_TH", y="T_TPXO", color="r")
plt.xlabel('T_TH(m)')
plt.ylabel('T_TPXO(m)')
sns.despine()
plt.savefig('/mnt/705300_rehaussement_marin/3- Data/LOT2/Rimouski/comparison_Tide_Rimouski.png', dpi=300)

# plot the differences in time
data['diff'] = data['T_TH'] - data['T_TPXO']
data['Date'] = pd.to_datetime(data["Date"])
data['month'] = data['Date'].dt.strftime('%b')
# plot time series
fig, ax = plt.subplots(1, 1, sharex=True, figsize=(8, 4), dpi=300)
sns.boxplot(x = 'month', y = 'diff', data = data, ax = ax)
sns.despine()
plt.ylabel('DeltaTide(m)')
plt.savefig('/mnt/705300_rehaussement_marin/3- Data/LOT2/Rimouski/monthly_delta_tide.png', dpi=300)

# plot tides in 2019

data = data.set_index('Date')
Tide_nov_2019  = data.loc['2019-11-01':'2019-11-30']  # 52

fig, ax = plt.subplots(1, 1, sharex=True, figsize=(12, 4), dpi=300)
sns.lineplot(x = 'Date', y = 'T_TPXO', data = Tide_nov_2019, ax = ax,label = 'T_TPXO')
sns.lineplot(x = 'Date', y = 'T_TH', data = Tide_nov_2019, ax = ax, label = 'T_TH')
sns.despine()
plt.ylabel('Tide level(m)')
dateform = DateFormatter("%m/%d")
ax.xaxis.set_major_formatter(dateform)
plt.savefig('/mnt/705300_rehaussement_marin/3- Data/LOT2/Rimouski/Tide_delta_November.png', dpi=300)








