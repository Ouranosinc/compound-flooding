

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import datetime
from datetime import timedelta
from pyextremes import EVA
import matplotlib.pyplot as plt


pth = r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\LOT2\Extraction_Qjourn_Ouranos_20082021.xlsx'
data = pd.read_excel(pth, index_col = 0,sheet_name = 'SLSO02381')

## find the annual maximum flow nad its index
Q = data.loc['1968-01-01':'2019-12-31']['50']  # 45 years


#Step 1: transforming the dataframe to Series
# Q_df = data_Q.set_index('Time')

Q_df = Q_df.rename(columns = {'50':'Discharge (m3/s)'})
wl_daily = wl_daily.set_index('Date')
wl_series = wl_daily['Water_Level(m)'].squeeze()


#step 2: calling extreme value analysis function in PyExtremes
H_conjoint = pd.DataFrame({'Time':df['Date'],
                       'Wlmax':df['Wlmax(m)']})
H_conjoint = H_conjoint.set_index('Time')
H_conjoint_s = H_conjoint.squeeze()
H_model = EVA(wl_series)

H_conjoint_model.set_extremes(extremes=H_conjoint_s)

# step 3: selecting the annual maxima

H_model.get_extremes(method="BM", block_size="365.2425D", errors = 'ignore')

# step 4: extracting annual maxima for flow discharges

fig,ax = plt.subplots(1,1,sharex = True,figsize=(8, 4))
#fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(4, 1)
ax.set_title('Sainte-Anne', fontsize=10)
modelQ.plot_extremes(figsize=(5,2))

ax.set_xlabel('year')
plt.grid('on')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.savefig('C:/Users/mohbiz1/Desktop/Dossier_travail/705300_rehaussement_marin/3- Data/DFO-MPO/LOT1/SA/Qmax_annual.png')

#step 5: fit the extreme value analysis

H_model.fit_model()

# step 6: calculating the extreme values


summary_H= H_model.get_summary(
    return_period=[1, 2, 5, 10, 20, 25, 50, 100, 350, 500, 1000],
    alpha=0.95,
    n_samples=1000)




modelQ_100cm_conjoint.plot_diagnostic(alpha=0.95)






#### Extremal value analysis of water level
# wl = data_wl.set_index('tstep')
# wl_series = wl['SL(m)'].squeeze()
# wl_daily = wl_series.resample('D').max()
# data = data.rename(columns = {'tstep':'Time'})



## water level analysis

pth2 = r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\DFO-MPO\LOT1\EC\EC_Hmax_at_Qmax.csv'
#pth2 = r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\DFO-MPO\EC.csv'
df= pd.read_csv(pth2, index_col = 0)

data_wl.reset_index(inplace=True) 
data_wl['year'] = pd.DatetimeIndex(data_wl['Date']).year
data_wl['month'] = pd.DatetimeIndex(data_wl['Date']).month
data_wl['day'] = pd.DatetimeIndex(data_wl['Date']).day

data_wl['Date'] = pd.to_datetime(data_wl['Date'])
data_wl = data_wl.set_index('Date')
data_wl = data_wl.loc['1968-01-01':'2019-12-31']  # 58


data_wl = data_wl.rename(columns = {'tstep':'Time'})
data_wl.reset_index(inplace=True) 
wl = data_wl.set_index('Date')
wl = wl.rename(columns = {'SL(m)':'Water Level (m)'})


wl.reset_index(inplace=True) 
wl['Date'] = pd.to_datetime(wl['Date'])
wl.set_index('Date',inplace=True)

wl_series = wl['Water Level (m)'].squeeze()
wl_daily = wl_series.resample('D').max()
wl_daily_series = wl_series.resample('D').max()

modelH = EVA(wl_daily_series)

modelH.get_extremes(method="BM", block_size="365.2425D", errors = 'ignore')


fig,ax = plt.subplots(1,1,sharex = True,figsize=(8, 4))
#fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(4, 1)
ax.set_title('Sainte-Anne', fontsize=10)
modelH.plot_extremes(figsize=(5,2))

ax.set_xlabel('year')
plt.grid('on')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.savefig('C:/Users/mohbiz1/Desktop/Dossier_travail/705300_rehaussement_marin/3- Data/DFO-MPO/LOT1/AM/Wlmax_annual.png')






model.plot_diagnostic(alpha=0.95)

fig,ax = plt.subplots(1,1,sharex = True,figsize=(8, 4))
model.plot_diagnostic(alpha=0.95)
ax.set_xlabel('year')
plt.grid('on')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.savefig('C:/Users/mohbiz1/Desktop/Dossier_travail/705300_rehaussement_marin/3- Data/DFO-MPO/LOT1/JC/FFA_wl.png')


Q_annual_max = Q_annual_max.set_index('Time')
Q_annual_max = Q_annual_max.rename(columns = {'50':'Discharge (m3/s)'})
Qmax_s = Q_annual_max['Discharge (m3/s)'].squeeze()





Qmax_conjoint = pd.DataFrame({'Time':dfH['Date'],
                       'Discharge (m3/s)':dfH['Qmax']})

# data_Q = data_Q.rename(columns = {'50':'Discharge (m3/s)'})

Qmax_conjoint = Qmax_conjoint.set_index('Time')
Qmax_conjoint_s = Qmax_conjoint.squeeze()
modelQ_conjoint = EVA(Qmax_conjoint_s)




fig,ax = plt.subplots(1,1,sharex = True,figsize=(8, 4))
x = np.linspace(st.t.ppf(0.01,fitted_parameters[1],fitted_parameters[2]),st.t.ppf(0.99,fitted_parameters[1],fitted_parameters[2]), 100)
ax.plot(x, t.pdf(x, fitted_parameters[1], fitted_parameters[2]),
       'r-', lw=5, alpha=0.6, label='t pdf')

ax.hist(dfH['Qmax'], density=True, histtype='stepfilled', alpha=0.2)
plt.show()


#################################################
            
# finding common discarge and water level days on a mars outlet

df_merge = Q_df.merge(wl_daily, on = ["Date","Date"],how="right")

## 

Q_annual_max = Q_df.loc[Q_df.groupby("year")["Discharge (m3/s)"].idxmax()]

df = pd.DataFrame({'Date':Q_annual_max['Date'],
                   'year':Q_annual_max['year'],
                  'month':Q_annual_max['month'],
                  'day': Q_annual_max['day'],
                  'Qmax':Q_annual_max['Discharge (m3/s)']})
                  

for index, row in Q_annual_max.iterrows():
    yQ = row['year']
    mQ = row['month']
    dQ = row['day']
    dQQ = datetime.datetime(yQ,mQ,dQ)
    for index2,row in wl_daily.iterrows():
        yl = row['year']
        ml = row['month']
        dl = row['day']
        wl = row['Water Level(m)']
        dll = d = datetime.datetime(yl,ml,dl)
        if (dQQ == dll):
            df.at[index,'Wlmax_0'] = wl
        elif (dll == dQQ - timedelta(days=1)):
            df.at[index,'Wlmax_1'] = wl
        elif (dll == dQQ + timedelta(days=1)):
            df.at[index,'Wlmax+1'] = wl 

## remove rows with NaN 
df.dropna(subset = ["Wlmax_0","Wlmax_1","Wlmax+1"], inplace=True)

## find the maximum water levels between Wlmax_0, Wlmax_1, and Wlmax+1

maxValue = df[['Wlmax_0', 'Wlmax_1','Wlmax+1']].max(axis=1)  #finding maximum value among these three days
df['Wlmax'] = maxValue

Hm = df['Wlmax'].median()
Qm = df['Qmax'].median()

## calculate the Mann-Kendal and Spearman correlation coefficient
        
tau, p_value_MK = stats.kendalltau(df['Qmax'], df['Wlmax'],nan_policy='omit')
rho, p_value_Sp = stats.spearmanr(df['Qmax'], df['Wlmax'],nan_policy='omit')

## Write Hmax at Qmax results to the folder

pth3  = r'C:/Users/mohbiz1/Desktop/Dossier_travail/705300_rehaussement_marin/3- Data/DFO-MPO/LOT1/705300/A_Mars/RP_reference.csv'
summary_H_normal.to_csv(pth3,mode='w')


## Analysis of Qmax at Hmax

## finding the annual Wlmax

wl_annual_max = wl_daily.loc[wl_daily.groupby("year")["Water Level(m)"].idxmax()]


dfH = pd.DataFrame({'Date':wl_annual_max['Date'],
                   'year':wl_annual_max['year'],
                  'month':wl_annual_max['month'],
                  'day': wl_annual_max['day'],
                  'Hmax':wl_annual_max['Water Level(m)']})
                  

for index, row in wl_annual_max.iterrows():
    yl = row['year']
    ml = row['month']
    dl = row['day']
    dll = datetime.datetime(yl,ml,dl)
    for index2,row in Q_df.iterrows():
        yQ = row['year']
        mQ = row['month']
        dQ = row['day']
        Q = row['Discharge (m3/s)']
        dQQ = datetime.datetime(yQ,mQ,dQ)
        if (dQQ == dll):
            dfH.at[index,'Qmax_0'] = Q
        elif (dQQ == dll - timedelta(days=1)):
            dfH.at[index,'Qmax_1'] = Q
        elif (dQQ == dll + timedelta(days=1)):
            dfH.at[index,'Qmax+1'] = Q 

maxValue = dfH[['Qmax_0', 'Qmax_1','Qmax+1']].max(axis=1)  #finding maximum value among these three days
dfH['Qmax'] = maxValue

## running extremal value analysis over df (Hmax column) and dfH (Qmax column)




























