# -*- coding: utf-8 -*-
##########################################

## This is the script for finding the correlation between annual maxima discharge and water level and test the significance of coorelation


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import datetime
from datetime import timedelta

pth = r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\Debits_Journ_Exutoire.xlsx'
data_Q = pd.read_excel(pth, index_col = 0,sheet_name = 'SLSO02381')

## find the annual maximum flow nad its index
Q = data_Q.loc['1968-01-01':'2019-12-31']['50']  # 45 years
#Q = data.loc['1968-01-01':'2019-12-31']['50']  # 45 years
Q_df = pd.DataFrame(Q)
Q_df.reset_index(inplace=True)

Q_df['month'] = pd.DatetimeIndex(Q_df['Time']).month
Q_df['year'] = pd.DatetimeIndex(Q_df['Time']).year
Q_df['day'] = pd.DatetimeIndex(Q_df['Time']).day

pth3  = r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\DFO-MPO\LOT1\SA\SA_Q.csv'
Q_df.to_csv(pth3,mode='w')

Q_annual_max = Q_df.loc[Q_df.groupby("year")["50"].idxmax()]
Q_annual_max = Q_annual_max.rename(columns = {'50':'Discharge (m3/s)'})

# write the results in a csv format

pth3  = r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\DFO-MPO\LOT1\SA\SA_Qmax_annual.csv'
Q_annual_max.to_csv(pth3,mode='w',columns=["Time","50","month","year","day"])


## water level analysis

pth2 = r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\DFO-MPO\LOT1\EC\EC_normal.csv'
#pth2 = r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\DFO-MPO\EC.csv'
data_wl= pd.read_csv(pth2, index_col = 0)

data_wl.reset_index(inplace=True) 
data_wl['year'] = pd.DatetimeIndex(data_wl['Date']).year
data_wl['month'] = pd.DatetimeIndex(data_wl['Date']).month
data_wl['day'] = pd.DatetimeIndex(data_wl['Date']).day

data_wl['Date'] = pd.to_datetime(data_wl['Date'])
data_wl = data_wl.set_index('Date')
data_wl = data_wl.loc['1968-01-01':'2019-12-31']  # 58





pth3  = r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\DFO-MPO\LOT1\AM\AM_Hmax_annual.csv'
extremes_df.to_csv(pth3,mode='w')


# finding annual maxima along with its day, month, year

data_wl.reset_index(inplace=True) 
wl_max =data_wl.loc[data_wl.groupby("year")["SL(m)"].idxmax()]

pth3  = r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\DFO-MPO\LOT1\SA\SA_Hmax_annual.csv'
wl_max.to_csv(pth3,mode='w')



































# pth2 = r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\DFO-MPO\St_Anne_MPO.csv'
# #pth2 = r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\DFO-MPO\EC.csv'
# data_wl = (pd.read_csv(pth2, index_col = 0)
#         .dropna()
#         )

# data_wl.reset_index(inplace=True) 
# #rng = pd.date_range(pd.Timestamp("1968-01-01 00:00"),periods=449275, freq='h')
# data_wl['Datetime'] = pd.to_datetime(data_wl['date'])
# #data_wl['Datetime']= rng
# data_wl = data_wl.set_index('Datetime')

# #data_wl = data_wl.loc['1968-01-01':'2019-12-31']  # 58
# data_wl = data_wl.loc['1962-01-01':'2019-12-31']  # 58

# ## find the maximum water level on the day (+-1) when Q is at its annual maximum value
# #data_wl.reset_index(inplace=True) 
# #data_wl['Date'] = pd.to_datetime(data_wl['Date'])

# #wl_daily =[data.groupby("day")["Water Level(m)"].idxmax()]
Q_annual_max.reset_index(inplace=True) 


wl_daily_50cm = wl_daily_50cm.to_frame()
data_50cm = data_50cm.set_index('Date')
wl_daily =data_wl.resample('D')['Water Level (m)'].agg(['max'])
wl_daily = wl_daily.rename(columns = {'max':'Water_Level(m)'})

wl_daily_50cm.reset_index(inplace=True) 
wl_daily_50cm['month'] = pd.DatetimeIndex(wl_daily_50cm['Date']).month
wl_daily_50cm['year'] = pd.DatetimeIndex(wl_daily_50cm['Date']).year
wl_daily_50cm['day'] = pd.DatetimeIndex(wl_daily_50cm['Date']).day

df_100cm = pd.DataFrame({'Date':Q_annual_max['Time'],
                   'year':Q_annual_max['year'],
                  'month':Q_annual_max['month'],
                  'day': Q_annual_max['day'],
                  'Qmax':Q_annual_max['Discharge (m3/s)']})
                  

for index, row in Q_annual_max.iterrows():
    yQ = row['year']
    mQ = row['month']
    dQ = row['day']
    dQQ = datetime.datetime(yQ,mQ,dQ)
    for index2,row in wl_daily_100cm.iterrows():
        yl = row['year']
        ml = row['month']
        dl = row['day']
        wl = row['Water Level(m)']
        dll = d = datetime.datetime(yl,ml,dl)
        if dQQ == dll:
            df_100cm.at[index,'Wlmax_0'] = wl
        elif (dll == dQQ - timedelta(days=1)):
            df_100cm.at[index,'Wlmax_1'] = wl
        elif (dll == dQQ + timedelta(days=1)):
            df_100cm.at[index,'Wlmax+1'] = wl 

maxValue = df_100cm[['Wlmax_0', 'Wlmax_1','Wlmax+1']].max(axis=1)  #finding maximum value among these three days
df_100cm['Wlmax'] = maxValue

Qm = df_100cm['Qmax'].median()

Hm = df_100cm['Wlmax'].median()









## find the maximum Q on the day (+-1) when H is at its annual maximum
#data_wl.reset_index(inplace=True) 
#data_wl['Date'] = pd.to_datetime(data_wl['Date'])


data['month'] = pd.DatetimeIndex(data['Time']).month
data['year'] = pd.DatetimeIndex(data['Time']).year
data['day'] = pd.DatetimeIndex(data['Time']).day
data.reset_index(inplace=True) 
H_max = data.loc[data.groupby("year")["SL(m)"].idxmax()]
H_max.reset_index(inplace=True) 


pth = r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\Debits_Journ_Exutoire.xlsx'
data = pd.read_excel(pth, index_col = 0,sheet_name = 'SLSO02381')

## find the annual maximum flow nad its index
Q = data.loc['1968-01-01':'2019-12-31']['50']  # 45 years
#Q = data.loc['1968-01-01':'2019-12-31']['50']  # 45 years
Q_df = pd.DataFrame(Q)
Q_df.reset_index(inplace=True) 

Q_df = Q_df.set_index('Time')
Q_df = Q_df.rename(columns = {'50':'Discharge (m3/s)'})
Q_daily_max = Q_df.resample('D')['Discharge (m3/s)'].agg(['max'])

Q_daily_max.reset_index(inplace=True) 
Q_daily_max['month'] = pd.DatetimeIndex(Q_daily_max['Time']).month
Q_daily_max['year'] = pd.DatetimeIndex(Q_daily_max['Time']).year
Q_daily_max['day'] = pd.DatetimeIndex(Q_daily_max['Time']).day


Q_daily_max = Q_daily_max.rename(columns = {'max':'Discharge (m3/s)'})




wl_max_N.reset_index(inplace=True) 
wl_max_N['month'] = pd.DatetimeIndex(wl_max_N['Date']).month
wl_max_N['year'] = pd.DatetimeIndex(wl_max_N['Date']).year
wl_max_N['day'] = pd.DatetimeIndex(wl_max_N['Date']).day

dfH_50cm = pd.DataFrame({'Date':wl_max_50cm['Date'],
                   'year':wl_max_50cm['year'],
                  'month':wl_max_50cm['month'],
                  'day': wl_max_50cm['day'],
                  'Wlmax':wl_max_50cm['Water Level(m)']})
                  

for index, row in wl_max_50cm.iterrows():
    yl = row['year']
    ml = row['month']
    dl = row['day']
    dll = datetime.datetime(yl,ml,dl)
    for index2,row in Q_daily_max.iterrows():
        yQ = row['year']
        mQ = row['month']
        dQ = row['day']
        Q = row['Discharge (m3/s)']
        dQQ = datetime.datetime(yQ,mQ,dQ)
        if (dQQ == dll):
            dfH_50cm.at[index,'Qmax_0'] = Q
        elif (dQQ == dll - timedelta(days=1)):
            dfH_50cm.at[index,'Qmax_1'] = Q
        elif (dQQ == dll + timedelta(days=1)):
            dfH_50cm.at[index,'Qmax+1'] = Q 

maxValue = dfH_50cm[['Qmax_0', 'Qmax_1','Qmax+1']].max(axis=1)  #finding maximum value among these three days
dfH_50cm['Qmax'] = maxValue

Hm = dfH_50cm['Wlmax'].median()

pth3  = r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\DFO-MPO\LOT1\SA\SA_Qmax_at_Hmax_50cm.csv'
dfH_50cm.to_csv(pth3,mode='w',index=False)



# pth3  = r'C:/Users/mohbiz1/Desktop/Dossier_travail/705300_rehaussement_marin/3- Data/DFO-MPO/LOT1/AM/Qmax_annual.csv'
# Q_annual_max.to_csv(pth3,mode='w')


# calculating correlation    

import scipy.stats as stats
tau, p_value_MK = stats.kendalltau(df2['Qmax'], df2['Wlmax'],nan_policy='omit')
rho, p_value_Sp = stats.spearmanr(df2['Qmax'], df2['Wlmax'],nan_policy='omit')

### write to a csv file
df = df.dropna()
pth3  = r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\DFO-MPO\LOT1\EC\EC_Hmax_at_Qmax_100cm.csv'
df2.to_csv(pth3,mode='w',index=False)



####


pth3  = r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\DFO-MPO\LOT1\JC\JC_Hmax_annual_50cm.csv'
wl_max_50cm.to_csv(pth3,mode='w',index=False)































