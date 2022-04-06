
## This script calculates the QcondWL and WLcondQ for the river outlet.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import datetime
from datetime import timedelta
import os

# %% Section 1: river flow

# inputs: path to the daily flow data (excel file) provided by DEH and name of the river outlets for analysis
name = 'Petit_Cascapedia'
pth = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT2/Extraction_Qjourn_Ouranos_20082021.xlsx'

data_Q = pd.read_excel(pth, index_col = None)

st = {'Ristigouche':'GASP00913', 'Matane':'GASP02848', 'au_Renard':'GASP00038', 'Saint-Jean':'01EX0000', 'Chicoutimi':'SAGU00012', 'Petit_Saguenay':'SAG00012', 'Moulin':'SAGU00279', 'Montmorency':'SLNO00294', 'Saint-Charles':'SLNO00004',
      'York':'GASP02158', 'Chaudiere':'SLSO02381', 'Outardes':'CNDA00096', 'Gouffre':'SLNO00195', 'Mitis':'GASP03111', 'Ha_Ha':'SAGU00151', 'Sables':'SAGU00599','RivSud':'SLSO02566','Petit_Cascapedia':'GASP01528' }  # to be confirned with DEH

idd = st[name]
Q = pd.DataFrame({'Q(m3/s)':data_Q[idd][1:],
                   'year':data_Q['Unnamed: 0'][1:].astype(int),
                  'month':data_Q['Unnamed: 1'][1:].astype(int),
                  'day': data_Q['Unnamed: 2'][1:].astype(int)})

# Transform the year, month, and day columns to datetime
Q['date'] = pd.to_datetime(Q[["year", "month", "day"]])

# Calculating the annual maxima

Q_annual_max = Q.loc[Q.groupby("year")["Q(m3/s)"].idxmax()]
Q_annual_max.reset_index(inplace=True) 


# %% reading the water level data time series
pth2 = os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT2/'+name+'/wl_data.csv')
data_wl= pd.read_csv(pth2, index_col = None)


data_wl['Date'] = pd.to_datetime(data_wl['Date'])
data_wl = data_wl.set_index('Date')
data_wl = data_wl.loc['1968-01-01':'2019-12-31']  # 52

# finding annual maxima along with its day, month, year

data_wl.reset_index(inplace=True) 
data_wl['year'] = pd.DatetimeIndex(data_wl['Date']).year
data_wl['month'] = pd.DatetimeIndex(data_wl['Date']).month
data_wl['day'] = pd.DatetimeIndex(data_wl['Date']).day

wl_max =data_wl.loc[data_wl.groupby("year")["wl(m)"].idxmax()]

wl_plt =  data_wl.drop(['year', 'month','day'], axis=1)
wl_plt = wl_plt.set_index('Date')
wl_plt_s = wl_plt.squeeze()

# Resample the hourly data to daily
data_wl = data_wl.set_index('Date')
wl_daily =data_wl.resample('D')['wl(m)'].agg(['max'])
wl_daily = wl_daily.rename(columns = {'max':'wl(m)'})

# Dropping the NAN columns 

wl_daily = wl_daily.dropna()

# adding year, month, day to the daily time series

wl_daily.reset_index(inplace=True) 
wl_daily['year'] = pd.DatetimeIndex(wl_daily['Date']).year
wl_daily['month'] = pd.DatetimeIndex(wl_daily['Date']).month
wl_daily['day'] = pd.DatetimeIndex(wl_daily['Date']).day

# Section3: constructing the compound dataframe

df_WLcondQ = pd.DataFrame({'Date':Q_annual_max['date'],
                   'year':Q_annual_max['year'],
                  'month':Q_annual_max['month'],
                  'day': Q_annual_max['day'],
                  'Qmax':Q_annual_max['Q(m3/s)']})                  

for index, row in Q_annual_max.iterrows():
#    import pdb; pdb.set_trace()
    yQ = row['year']
    mQ = row['month']
    dQ = row['day']
    dQQ = datetime.datetime(yQ,mQ,dQ)
    for index2,row in wl_daily.iterrows():
        yl = row['year']
        ml = row['month']
        dl = row['day']
        wlc = row['wl(m)']
        dll = d = datetime.datetime(yl,ml,dl)
        if dQQ == dll:
            df_WLcondQ.at[index,'Wlmax_0'] = wlc
        elif (dll == dQQ - timedelta(days=1)):
            df_WLcondQ.at[index,'Wlmax_1'] = wlc
        elif (dll == dQQ + timedelta(days=1)):
            df_WLcondQ.at[index,'Wlmax+1'] = wlc

df_WLcondQ = df_WLcondQ.dropna()

maxValue = df_WLcondQ[['Wlmax_0', 'Wlmax_1','Wlmax+1']].max(axis=1)  #finding maximum value among these three days
df_WLcondQ['Wlmax'] = maxValue

df_WLcondQ = df_WLcondQ.drop(['Wlmax_0','Wlmax_1','Wlmax+1'], axis=1)


# Write results to a .csv file
pth3 = os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT2/'+name+'/WLcondQ.csv')
df_WLcondQ.to_csv(pth3,mode='w',index=False)

tau, p_value_MK = stats.kendalltau(df_WLcondQ['Qmax'], df_WLcondQ['Wlmax'],nan_policy='omit')
rho, p_value_Sp = stats.spearmanr(df_WLcondQ['Qmax'], df_WLcondQ['Wlmax'],nan_policy='omit')

# Constructing QcondWL dataframe

df_QcondWL = pd.DataFrame({'Date':wl_max['Date'],
                   'year':wl_max['year'],
                  'month':wl_max['month'],
                  'day': wl_max['day'],
                  'Wlmax':wl_max['wl']})
                  

for index, row in wl_max.iterrows():
    yl = row['year']
    ml = row['month']
    dl = row['day']
    dll = datetime.datetime(yl,ml,dl)
    for index2,row in Q.iterrows():
        yQ = row['year']
        mQ = row['month']
        dQ = row['day']
        Qd = row['Q(m3/s)']
        dQQ = datetime.datetime(yQ,mQ,dQ)
        if (dQQ == dll):
            df_QcondWL.at[index,'Qmax_0'] = Qd
        elif (dQQ == dll - timedelta(days=1)):
            df_QcondWL.at[index,'Qmax_1'] = Qd
        elif (dQQ == dll + timedelta(days=1)):
            df_QcondWL.at[index,'Qmax+1'] = Qd 

maxValue = df_QcondWL[['Qmax_0', 'Qmax_1','Qmax+1']].max(axis=1)  #finding maximum value among these three days
df_QcondWL['Qmax'] = maxValue

df_QcondWL = df_QcondWL.drop(['Qmax_0', 'Qmax_1','Qmax+1'], axis=1)

# Write results to a .csv file
df_QcondWL = df_QcondWL.dropna()
pth3 = os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT2/'+name+'/QcondWL.csv')
df_QcondWL.to_csv(pth3,mode='w',index=False)

# calculating correlation    

tau, p_value_MK = stats.kendalltau(df_QcondWL['Qmax'], df_QcondWL['Wlmax'],nan_policy='omit')
rho, p_value_Sp = stats.spearmanr(df_QcondWL['Qmax'], df_QcondWL['Wlmax'],nan_policy='omit')





