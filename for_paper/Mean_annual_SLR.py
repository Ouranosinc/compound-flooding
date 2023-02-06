
## This script calculates the QcondWL and WLcondQ for the river outlet.For LOT3 csv format.

import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns

# %% reading the water level data time series
name = {'Gouffre':'LOT2','RivSud':'LOT2','Montmorency':'LOT2','Saint_Charles':'LOT2','Chaudiere':'LOT2','Etchemin':'LOT1','Jacques_Cartier':'LOT1','Sainte_Anne':'LOT1','Batiscan':'LOT3','Becancour':'LOT3','Saint_Maurice':'LOT3','Nicolet':'LOT3','du_Loup':'LOT3','Maskinonge':'LOT3','Saint_Francois':'LOT3','Yamaska':'LOT3','Richelieu':'LOT3','Assomption':'LOT3',
        }


diff = pd.DataFrame()

for k, v in name.items():
    temp = pd.DataFrame()
    pth2 = os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/'+v+'/'+k+'/wl_data.csv')
    data_wl= pd.read_csv(pth2, index_col = None)
    data_wl['Date'] = pd.to_datetime(data_wl['Date'])
    data_wl = data_wl.set_index('Date')
    data_wl = data_wl.loc['1968-01-01':'2020-12-31']      
    
    # finding annual maxima along with its day, month, year
    
    data_wl.reset_index(inplace=True) 
    data_wl['year'] = pd.DatetimeIndex(data_wl['Date']).year
    data_wl['month'] = pd.DatetimeIndex(data_wl['Date']).month
    data_wl['day'] = pd.DatetimeIndex(data_wl['Date']).day

    # Resample the hourly data to daily
    data_wl = data_wl.set_index('Date')
    wl_yearly_mean_hist =data_wl.resample('Y')['wl(m)'].agg(['mean'])
    wl_yearly_mean_hist = wl_yearly_mean_hist.rename(columns = {'mean':'wl(m)'})

    del data_wl
    # future

    pth2 = os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/'+v+'/'+k+'/wl_50cm.csv')
    data_wl= pd.read_csv(pth2, index_col = None)
    
    
    data_wl['Date'] = pd.to_datetime(data_wl['Date'])
    data_wl = data_wl.set_index('Date')
    data_wl = data_wl.loc['1968-01-01':'2020-12-31']  

    
    # finding annual maxima along with its day, month, year
    
    data_wl.reset_index(inplace=True) 
    data_wl['year'] = pd.DatetimeIndex(data_wl['Date']).year
    data_wl['month'] = pd.DatetimeIndex(data_wl['Date']).month
    data_wl['day'] = pd.DatetimeIndex(data_wl['Date']).day

    # Resample the hourly data to daily
    data_wl = data_wl.set_index('Date')
    wl_yearly_mean_future =data_wl.resample('Y')['wl(m)'].agg(['mean'])
    wl_yearly_mean_future = wl_yearly_mean_future.rename(columns = {'mean':'wl(m)'})

    temp['value'] = wl_yearly_mean_future - wl_yearly_mean_hist
    temp['outlet'] = k
    temp['LOT'] = v
    diff = pd.concat([diff,temp])

    del wl_yearly_mean_future,data_wl, temp


Index = diff.index.unique('Date')
Chateauguay = pd.DataFrame(index = Index,columns=['value'])
Chateauguay['value'] = 0  # no sea level rise for Chateauguay 
Chateauguay['outlet'] = 'Chateauguay'  # no sea level rise for Chateauguay 
Chateauguay['LOT'] = v

Moulin = pd.DataFrame(index = Index,columns=['value'])
Moulin['value'] = 0.482  # no sea level rise for Chateauguay 
Moulin['outlet'] = 'Moulin'

diff = pd.concat([diff,Chateauguay,Moulin])

# %% plot time series
fig, ax = plt.subplots(1, 1, sharex=True, figsize = (10,10), dpi=300)
sns.set(style='whitegrid')
# sns.set(font_scale = 0.2)
g = sns.boxplot(y = 'outlet', x = 'value', data = diff, ax = ax, width= 0.3)
# sns.despine()
ax.set_xlabel(r'$\Delta$WL(m)')
g.set(ylabel=None)
plt.grid('on')
sns.despine(top=True, right=True)

plt.savefig('/home/mohammad/Dossier_travail/705300_rehaussement_marin/4- Présentations/Symposium_Ouranos/Delta_Mean_annual_WL.png', dpi=300)




