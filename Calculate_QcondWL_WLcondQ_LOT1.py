
## This script calculates the QcondWL and WLcondQ for the river outlet.For LOT2 csv format.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import datetime
from datetime import timedelta
import os

# %% Section 1: river flow

# inputs: path to the daily flow data (excel file) provided by DEH and name of the river outlets for analysis
name = 'A_Mars'
pth = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT1/Extraction_Qjourn_Ouranos_LOT1.xlsx'

data_Q = pd.read_excel(pth, index_col = None)

st = {'A_Mars':'SAGU00175', 'Sainte-Anne':'SLNO03193', 'Jacques_Cartier':'SLNO00347', 'Etchemin':'SLSO02381'}  


data_Q['Date'] = pd.to_datetime(data_Q[['Year', 'Month', 'Day']])


idd = st[name]
Q = pd.DataFrame({'Q(m3/s)':data_Q[idd][0:],
                   'Date':data_Q['Date'][0:].astype('datetime64[ns]')})

# Transform the Date to year, month, and day columns
Q['year'] = pd.DatetimeIndex(Q['Date']).year
Q['month'] = pd.DatetimeIndex(Q['Date']).month
Q['day'] = pd.DatetimeIndex(Q['Date']).day

# Calculating the annual maxima

Q_annual_max = Q.loc[Q.groupby("year")["Q(m3/s)"].idxmax()]
Q_annual_max.reset_index(inplace=True) 


# %% reading the water level data time series
pth2 = os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT1/'+name+'/wl_data_CGVD28.csv')
data_wl= pd.read_csv(pth2, index_col = None)


data_wl['Date'] = pd.to_datetime(data_wl['Date'])
data_wl = data_wl.set_index('Date')
data_wl = data_wl.loc['1968-01-01':'2019-12-31']  

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

df_WLcondQ = pd.DataFrame({'Date':Q_annual_max['Date'],
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
pth3 = os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT1/'+name+'/WLcondQ_CGVD28.csv')
df_WLcondQ.to_csv(pth3,mode='w',index=False)

tau, p_value_MK = stats.kendalltau(df_WLcondQ['Qmax'], df_WLcondQ['Wlmax'],nan_policy='omit')
rho, p_value_Sp = stats.spearmanr(df_WLcondQ['Qmax'], df_WLcondQ['Wlmax'],nan_policy='omit')

# Constructing QcondWL dataframe

df_QcondWL = pd.DataFrame({'Date':wl_max['Date'],
                   'year':wl_max['year'],
                  'month':wl_max['month'],
                  'day': wl_max['day'],
                  'Wlmax':wl_max['wl(m)']})
                  

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
pth3 = os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT1/'+name+'/QcondWL_CGVD28.csv')
df_QcondWL.to_csv(pth3,mode='w',index=False)

# calculating correlation    

tau, p_value_MK = stats.kendalltau(df_QcondWL['Qmax'], df_QcondWL['Wlmax'],nan_policy='omit')
rho, p_value_Sp = stats.spearmanr(df_QcondWL['Qmax'], df_QcondWL['Wlmax'],nan_policy='omit')





df_QcondWL_RM = df_QcondWL
df_QcondWL_RM['Wlmax'] = df_QcondWL['Wlmax']+0.482

df_WLcondQ_RM = df_WLcondQ
df_WLcondQ_RM['Wlmax'] = df_WLcondQ['Wlmax']+0.482

pth3 = os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT1/'+name+'/QcondWL_CGVD28_48_2cm.csv')
df_QcondWL_RM.to_csv(pth3,mode='w',index=False)

pth3 = os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT1/'+name+'/WLcondQ_CGVD28_48_2cm.csv')
df_WLcondQ_RM.to_csv(pth3,mode='w',index=False)

tau, p_value_MK = stats.kendalltau(df_WLcondQ_RM['Qmax'], df_WLcondQ_RM['Wlmax'],nan_policy='omit')
rho, p_value_Sp = stats.spearmanr(df_WLcondQ_RM['Qmax'], df_WLcondQ_RM['Wlmax'],nan_policy='omit')

tau, p_value_MK = stats.kendalltau(df_QcondWL_RM['Qmax'], df_QcondWL_RM['Wlmax'],nan_policy='omit')
rho, p_value_Sp = stats.spearmanr(df_QcondWL_RM['Qmax'], df_QcondWL_RM['Wlmax'],nan_policy='omit')