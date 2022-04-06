# -*- coding: utf-8 -*-
"""
Created on Mon May  3 08:47:18 2021

@author: mohbiz1
"""

import pandas as pd
import numpy as np
from pyextremes import EVA
import matplotlib.pyplot as plt
from scipy.io import loadmat
from scipy import spatial

path = r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\DFO-MPO\modeleMPO_extraits.mat'
rng = pd.date_range(pd.Timestamp("1968-01-01 00:00"),periods=52, freq='y')
time = rng.to_frame(index = False, name = 'date')
a = pd.DataFrame(loadmat(path)['qmax_StAnne'],columns=["Sea_Level(m)"])


df = pd.merge(a, time,right_index=True, left_index=True)

df = df.set_index('date')


# path_to_data = r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\DFO-MPO\St_Anne_MPO.csv'

# data = (pd.read_csv(path_to_data, index_col = 0, parse_dates=['date'])
#         .dropna()
#         )

Ann_max= df.resample('Y').max()

Yearly_mean= data.resample('Y').mean()

Longterm_mean = data.mean()
AnnM_longtm = Yearly_mean - Longterm_mean
Adjusted_Annmax = Ann_max- Yearly_mean


data.reset_index(inplace=True)
data['month'] = pd.DatetimeIndex(data['Date']).month
Seas_max =data.loc[data.groupby("month")["Sea_Level(m)"].idxmax()]


fig, ax = plt.subplots()
ax.plot(Seas_max['month'],Seas_max['Sea_Level(m)'],
marker='o', markersize=8, linestyle='-', label='Monthly maxima')
ax.set_ylabel('Sea_Level(m)')
ax.legend();
plt.savefig('monthly maxima.png')

hist_monthly_max = data.resample('M').max()




Yearly_mean.reset_index(inplace=True)
Yearly_mean['x'] = Yearly_mean.index

Ann_max.reset_index(inplace=True)
Ann_max['x'] = Ann_max.index

Adjusted_Annmax.reset_index(inplace=True)
Adjusted_Annmax['x'] = Adjusted_Annmax.index



# plot Annual mean plus the trend

# compute the trend line
idx = np.isfinite(Yearly_mean['x']) & np.isfinite(Yearly_mean['Sea_Level(m)'])
fit = np.polyfit(Yearly_mean['x'][idx],Yearly_mean['Sea_Level(m)'][idx], 1)
fit_fn = np.poly1d(fit)

#plt.plot(Yearly_mean['Date'], fit_fn(Yearly_mean['x']), 'r-')
#plt.plot(Yearly_mean['Date'], Yearly_mean['Sea_Level(m)'], 'b-',marker='o', ms=5)

fig, ax = plt.subplots()
ax.plot(Yearly_mean['date'],Yearly_mean['Sea_Level(m)'],
marker='o', markersize=8, linestyle='-', label='Annual mean')
ax.plot(Yearly_mean['date'], fit_fn(Yearly_mean['x']), 'r-', label='Linear trend')
ax.set_ylabel('Sea_Level(m)')
ax.legend();
plt.grid('on')
plt.savefig('Annual_Mean_trend_St_Anne.png')


# plot Annual maxima plus trend


idx = np.isfinite(Ann_max['x']) & np.isfinite(Ann_max['Sea_Level(m)'])
fit = np.polyfit(Ann_max['x'][idx],Ann_max['Sea_Level(m)'][idx], 1)
fit_fn = np.poly1d(fit)

fig, ax = plt.subplots()
ax.plot(Ann_max['date'],Ann_max['Sea_Level(m)'],
marker='o', markersize=8, linestyle='-', label='Annual max')
ax.plot(Ann_max['date'], fit_fn(Ann_max['x']), 'r-', label='Linear trend')
ax.set_ylabel('Sea_Level(m)')
ax.legend();
plt.grid('on')
plt.savefig('Annual_Max_trend_St_Anne.png')


#  plot adjusted annual maxima

idx = np.isfinite(Adjusted_Annmax['x']) & np.isfinite(Adjusted_Annmax['Sea_Level(m)'])
fit = np.polyfit(Adjusted_Annmax['x'][idx],Adjusted_Annmax['Sea_Level(m)'][idx], 1)
fit_fn = np.poly1d(fit)

fig, ax = plt.subplots()
#ax.plot(data,
#linestyle='-', linewidth=0.2, label='Sea_Level')
ax.plot(Adjusted_Annmax['Date'],Adjusted_Annmax['Sea_Level(m)'],
marker='o', markersize=8, linestyle='-', label='Adjusted Annual max')
ax.plot(Ann_max['Date'], fit_fn(Ann_max['x']), 'r-', label='Linear trend')
ax.set_ylabel('Sea_Level(m)')
ax.legend();
plt.savefig('Adjusted_Ann_max.png')


########################################################################################


pth = r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\Debits_Journ_Exutoire.xlsx'

data = pd.read_excel(pth, index_col = 0,sheet_name = 'SLNO03193')

Q = data.loc['1962-01-01':'2019-12-31']['50']  # 45 years

# calculating annual mean
Q_annual_mean= Q.resample('Y').mean()
Q_annual_mean['x'] = np.linspace(0,44,45)

# calculating annual max
Q_annual_max= Q.resample('Y').max()
Q_annual_max['x'] = np.linspace(0,57,58)

Q_annual_max_df = pd.DataFrame(Q_annual_max)

#fitting a linear trend to the data
idx = np.isfinite(Q_annual_mean['x']) & np.isfinite(Q_annual_mean['50'])
fit = np.polyfit(Q_annual_mean['x'][idx],Q_annual_mean['50'][idx], 1)
fit_fn = np.poly1d(fit)

Q_annual_mean.reset_index(inplace=True)
fig, ax = plt.subplots()
ax.plot(Q_annual_mean['Time'],Q_annual_mean['50'], color='black', label='Annual mean',marker='o', markersize=8)
ax.plot(Q_annual_mean['Time'], fit_fn(Q_annual_mean['x']), 'r-', label='Linear trend')
ax.set_ylabel('Discharge (m3/s)')
ax.legend();
plt.savefig('Q_Annual_mean.png')




#fitting a linear trend to the data
Q_annual_max_df['x'] = np.linspace(0,57,58)
idx = np.isfinite(Q_annual_max_df['x']) & np.isfinite(Q_annual_max_df['50'])
fit = np.polyfit(Q_annual_max_df['x'][idx],Q_annual_max_df['50'][idx], 1)
fit_fn = np.poly1d(fit)
Q_annual_max_df.reset_index(inplace=True)


fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(Q_annual_max_df['Time'],Q_annual_max_df['50'], color='black', label='Annual max',marker='o', markersize=8)
ax.plot(Q_annual_max_df['Time'], fit_fn(Q_annual_max_df['x']), 'r-', label='Linear trend')
ax.set_ylabel('Discharge (m3/s)')
ax.legend();
plt.grid('on')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.savefig('Q_Annual_max_SA.png')


######################################################################################

Annmax = Ann_max['Sea_Level(m)']
import pymannkendall as mk
mk.original_test(Annmax)

#########################################################################################################################################

###fitting a distribution to the data and select the best model based on AIC criterion

import pandas as pd
import numpy as np
from pyextremes import EVA
import matplotlib.pyplot as plt


path_to_data = r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\DFO-MPO\LOT1\Riviere_a_mars\data.csv'

# for using the Eva, the data should be series
data = pd.read_csv(path_to_data, index_col = 0, parse_dates=True,squeeze=True)

Ann_max= data.resample('Y').max()

Ann_max_clean=Ann_max.dropna() 
# Ann_max_clean.reset_index(inplace=True)  ## clean Annual maxima

# Ann_max_clean['year'] = Ann_max_clean['Date'].map(lambda x: x.strftime('%Y'))  #extracting year from the datetime data (Date column)

# # to work with skextremes package, the dataset (Annmax_clean) shoudl be a 1D array

# Annmax_array = Ann_max_clean['Sea_Level(m)']
# #Annmax_array = Ann_max_clean.to_numpy()

# model = ske.models.classic.Gumbel(Annmax_array, fit_method = 'lmoments', ci = 0.05,
# ci_method = 'bootstrap')

# model.plot_summary()  # plots 4 graphs related to the fitting performance (including return period)

# fit the gumbel_r distribution to the maxannual data, this time using new parameters
import lmoments3 as lm
from lmoments3 import distr,stats
import scikits.bootstrap as boot
import scipy.stats as st

LMU = lm.lmom_ratios(Ann_max['Sea_Level(m)']) # This will give the first 5 moments of the sample distribution

paras_GEV = distr.gev.lmom_fit(Ann_max['Sea_Level(m)']) # this will give the parameters of GEV distrinbution
paras_GUM = distr.gum.lmom_fit(Ann_max['Sea_Level(m)']) # this will give the parameters of Gumbel distrinbution


paras_GEV_Q = distr.gev.lmom_fit(Q_annual_max_df['50']) # this will give the parameters of GEV distrinbution
paras_GUM_Q = distr.gum.lmom_fit(Q_annual_max_df['50']) # this will give the parameters of Gumbel distrinbution



fitted_gev = distr.gev(**paras_GEV)
fitted_gum = distr.gum(**paras_GUM)

# calculating the AIC criterion and selecting the best model

AIC_gev= stats.AIC(Q_annual_max_df['50'], 'gev', paras_GEV_Q)
AIC_gumbel = stats.AIC(Q_annual_max_df['50'], 'gum', paras_GUM_Q)


#ci = boot.ci(Ann_max_clean, st.gumbel_r.fit)
ci = boot.ci(Q_annual_max_df['50'], st.gumbel_r.fit,alpha=0.05)

# param_l = {"c":ci[0,0],"loc": ci[0,1],"scale": ci[0,2]}
# param_m = {"c":0.07863740730368093,"loc": 422.72413971244504,"scale": 125.70003964488146}
# param_h = {"c":ci[1,0],"loc": ci[1,1],"scale": ci[1,2]}

param_l = {"loc": ci[0,0],"scale": ci[0,1]}
param_m = {"loc": 418.34136217557614,"scale": 117.48125049814418}
param_h = {"loc": ci[1,0],"scale": ci[1,1]}


# ddl = distr.gev(**param_l)
# ddm = distr.gev(**param_m)
# ddh = distr.gev(**param_h)

ddl = distr.gum(**param_l)
ddm = distr.gum(**param_m)
ddh = distr.gum(**param_h)


T = np.arange(0.1,350.1,0.1) +1
gevRP_l = ddl.ppf(1.0-1./T)
gevRP_m = ddm.ppf(1.0-1./T)
gevRP_h = ddh.ppf(1.0-1./T)


# plots



fig,ax = plt.subplots(1,1,sharex = True,figsize=(8, 4))
ax.fill_between(T, gevRP_l, gevRP_h,
                  facecolor="orange", # The fill color
                  color='cornflowerblue',       # The outline color
                  alpha=0.2)          # Transparency of the fill

ax.plot(T,gevRP_m,'b-', label='Stationary return period')
ax.set_ylabel('Q (m3/s)')
ax.set_xlabel('Return period (yr)')
ax.legend();
plt.grid('on')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.savefig('RP_stationary_Q_SA.png')


ax.plot(T,gevRP_m,'r-', label='Stationary return period: H2019')





#############################################################################################

##  Nonstationary analysis
import pymannkendall as mk
from matplotlib import pyplot as plt
from pandas import DataFrame

i=0
t=0
window_size = 15
pvalues = []
Mov_mean = []
Std = []

while i <len(Ann_max_clean)-window_size +1:
    
    temp = Ann_max_clean[i:i+window_size]
    result = mk.original_test(temp)
    pvalues.append(result.p)
 #   a = temp.mean()
 #   b = temp.std()
 #   Mov_mean.append(a)
 #   Std.append(b)
    i += 1
    
# calculate rolling mean and standard deviation

MVMean = Ann_max_clean.rolling(15,min_periods=3).mean()
MVStd = Ann_max_clean.rolling(15,min_periods=3).std()


MVMean_df = pd.DataFrame(MVMean)
MVStd_df = pd.DataFrame(MVStd)


MVMean_df.reset_index(inplace=True)  ## 
MVMean_df['year'] = MVMean_df['Date'].map(lambda x: x.strftime('%Y'))  #extracting year from the datetime data (Date column)


MVStd_df.reset_index(inplace=True)  ## 
MVStd_df['year'] = MVStd_df['Date'].map(lambda x: x.strftime('%Y'))  #extracting year from the datetime data (Date column)


## fit a linear regression to the data
MVMean_df['year'] = np.array(MVMean_df['year'], dtype=float)
MVStd_df['year'] = np.array(MVStd_df['year'], dtype=float)

idx = np.isfinite(MVMean_df['year']) & np.isfinite(MVMean_df['Sea_Level(m)'])
fit = np.polyfit(MVMean_df['year'][idx],MVMean_df['Sea_Level(m)'][idx], 1)
fit_fn = np.poly1d(fit)

# determining location and scale parameters in nonstationary model
loc_2019 = 2.086e+1 + (-7.17e-3 * 2019)
scale_2019 = 5.3263 + (-2.583e-03 * 2019)




#ci = boot.ci(Ann_max_clean, st.gumbel_r.fit)

#param_l = {"loc": ci[0,0],"scale": ci[0,1]}
param_m = {"loc": loc_2019,"scale": scale_2019}
#param_h = {"loc": ci[1,0],"scale": ci[1,1]}


dd = distr.gum(**param_m)


T = np.arange(0.1,350.1,0.1) +1
#gevRP_l = dd.ppf(1.0-1./T)
gevRP_m_nonst = dd.ppf(1.0-1./T)
#gevRP_h = dd.ppf(1.0-1./T)

fig,ax = plt.subplots(1,1,sharex = True)
# ax.fill_between(T, gevRP_l, gevRP_h,
#                  facecolor="orange", # The fill color
#                  color='cornflowerblue',       # The outline color
#                  alpha=0.2)          # Transparency of the fill

ax.plot(T,gevRP_m,'b-', label='Stationary return period')
ax.plot(T,gevRP_m_nonst,'r-', label='NonStationary return period: H2019')
ax.set_ylabel('Sea Level(m)')
ax.set_xlabel('Return period (yr)')
ax.legend();
plt.grid('on')
plt.savefig('RP_stationary_nonstationary.png')



###########################################################################################################
## in this section we will find the correlation between maximum river flow and 








