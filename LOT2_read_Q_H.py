
## T

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import datetime
from datetime import timedelta
import scipy.stats as stats

# %% Section 1: river flow

# inputs: path to the daily flow data (excel file) provided by DEH and name of the river outlets for analysis
pth = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT2/Extraction_Qjourn_Ouranos_20082021.xlsx'
name = 'Petit_Cascapedia'

data_Q = pd.read_excel(pth, index_col = None)

st = {'Ristigouche':'GASP00913', 'Matane':'GASP02848', 'Renard':'GASP00038', 'Saint-Jean':'01EX0000', 'Chicoutimi':'SAGU00012', 'Petit_Saguenay':'SAG00012', 'Moulin':'SAGU00279', 'Montmorency':'SLNO00294', 'Saint-Charles':'SLNO00004',
      'York':'GASP02158', 'Chaudiere':'SLSO02381', 'Outardes':'CNDA00096', 'Gouffre':'SLNO00195', 'Mitis':'GASP03111', 'Ha!Ha!':'SAGU00151', 'Sables':'SAGU00599','Sud':'SLSO02566','Petit_Cascapedia':'GASP01528' }  # to be confirned with DEH

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

# %% To plot river flow with annual maxima (Figure 5 report LOT2)

Q_annual_max =  Q_annual_max.drop(['year', 'month','day','index'], axis=1)
Q_annual_max = Q_annual_max.set_index('date')
Q_annual_max = Q_annual_max.squeeze()

Q_plt =  Q.drop(['year', 'month','day'], axis=1)
Q_plt = Q_plt.set_index('date')
Q_plt_s = Q_plt.squeeze()

pth = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT2/Petit_Cascapedia/QcondWL.csv'
Qcond = pd.read_csv(pth, index_col = None,parse_dates= {"date" : ["year","month","day"]})
Qcond =  Qcond.drop(['Date','Wlmax'], axis=1)
Qcond = Qcond.set_index('date')
Qcond = Qcond.squeeze()

# step 4: extracting annual maxima for flow discharges

fig,ax = plt.subplots(1,1,sharex = True,figsize=(5, 2),dpi=300)
Q_plt_s.plot(c= "dodgerblue",linewidth=0.2,zorder=0)
Q_annual_max.plot(style = '.r',zorder=1)
plt.scatter(Qcond.index,Qcond,facecolors="k", s=5,edgecolors="none",zorder=2)
plt.grid(which='both')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.title('Petit_Cascapedia', fontsize=10)
ax.set_ylim(0,max(Q_plt_s)+20)
plt.ylabel('Débit ($m^3$/s)')
plt.savefig('/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT2/Qmax_annual_Petit_Cascapedia.png')

# %% reading the estimated water level data at Mitis, Matane, et Outardes

pth2 = '/mnt/705300_rehaussement_marin/3- Data/LOT2/Au_Renard/totalwl_and_tide.csv'
data_wl= pd.read_csv(pth2, index_col = None)


data_wl['Date'] = pd.to_datetime(data_wl['Date'])
data_wl = data_wl.set_index('Date')
data_wl = data_wl.loc['1968-01-01':'2019-12-31']  # 52

# finding annual maxima along with its day, month, year

data_wl.reset_index(inplace=True) 
data_wl['year'] = pd.DatetimeIndex(data_wl['Date']).year
data_wl['month'] = pd.DatetimeIndex(data_wl['Date']).month
data_wl['day'] = pd.DatetimeIndex(data_wl['Date']).day

wl_max =data_wl.loc[data_wl.groupby("year")["wl"].idxmax()]
wl_max.reset_index(inplace=True) 


wl_plt =  data_wl.drop(['year', 'month','day','TD(m)','Depth(m)','lat','lon','MSL','TD_est','Residual'], axis=1)
wl_plt = wl_plt.set_index('Date')
wl_plt_s = wl_plt.squeeze()

# Resample the hourly data to daily
data_wl = data_wl.set_index('Date')
wl_daily =data_wl.resample('D')['wl'].agg(['max'])
wl_daily = wl_daily.rename(columns = {'max':'wl'})

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
        wlc = row['wl']
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

pth3  = '/mnt/705300_rehaussement_marin/3- Data/LOT2/York/WLcondQ.csv'
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
pth3  = '/mnt/705300_rehaussement_marin/3- Data/LOT2/York/QcondWL.csv'
df_QcondWL.to_csv(pth3,mode='w',index=False)

# calculating correlation    

tau, p_value_MK = stats.kendalltau(df_QcondWL['Qmax'], df_QcondWL['Wlmax'],nan_policy='omit')
rho, p_value_Sp = stats.spearmanr(df_QcondWL['Qmax'], df_QcondWL['Wlmax'],nan_policy='omit')


fig,ax = plt.subplots(1,1,sharex = True,figsize=(8, 4),dpi=300)
#ax.plot(df_inner['Date'], df_inner['TD(m)'],label='TD')
#ax.plot(df_Mitis['Date'][-1000:], df_Mitis['wl'][-1000:],label='Mitis')
ax.scatter(df_QcondWL['Qmax'],df_QcondWL['Wlmax'],facecolors="k", s=20,edgecolors="none")
#ax.plot(df_inner['Date'], df_inner['wl'], label='WL')
ax.set_ylabel('Wlmax')
ax.set_xlabel('Qmax')
ax.legend();
plt.grid('on')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)



# %%
# Section 2: Sea level 
#The water level data area read using read_sim_Denis script. here we load the resulting csv files that are saved in \Denis_simulation directory.

pth2 = '/mnt/705300_rehaussement_marin/3- Data/Denis_simulation_results/Chaudiere_normal.csv'
#pth2 = '/mnt/705300_rehaussement_marin/3- Data/LOT2/Petit_Saguenay/totalwl_and_tide.csv'
data_wl= pd.read_csv(pth2, index_col = None)


data_wl['Date'] = pd.to_datetime(data_wl['Date'])
data_wl = data_wl.set_index('Date')
data_wl = data_wl.loc['1968-01-01':'2019-12-31']  # 52

# finding annual maxima along with its day, month, year

data_wl =  data_wl.drop(['year'], axis=1)

data_wl.reset_index(inplace=True) 
data_wl['year'] = pd.DatetimeIndex(data_wl['Date']).year
data_wl['month'] = pd.DatetimeIndex(data_wl['Date']).month
data_wl['day'] = pd.DatetimeIndex(data_wl['Date']).day

wl_max =data_wl.loc[data_wl.groupby("year")["SL(m)"].idxmax()]
wl_max.reset_index(inplace=True) 

# To plot the water level annual maxima

wl_max =  wl_max.drop(['year', 'month','day','index','Unnamed: 0'], axis=1)
wl_max = wl_max.set_index('Date')
wl_max = wl_max.squeeze()



wl_plt =  data_wl.drop(['year', 'month','day','TD(m)','Depth(m)','lat','lon','MSL','TD_est','Residual'], axis=1)
wl_plt = wl_plt.set_index('Date')
wl_plt_s = wl_plt.squeeze()

# Resample the hourly data to daily
data_wl = data_wl.set_index('Date')
wl_daily =data_wl.resample('D')['wl'].agg(['max'])
wl_daily = wl_daily.rename(columns = {'max':'wl'})

# %% To plot the water level annual maxima (Figure)

wl_max =  wl_max.drop(['year', 'month','day','index','Unnamed: 0'], axis=1)
wl_max = wl_max.set_index('Date')
wl_max = wl_max.squeeze()


wl_plt =  data_wl.drop(['year', 'month','day','Unnamed: 0'], axis=1)
wl_plt = wl_plt.set_index('Date')
wl_plt_s = wl_plt.squeeze()

pth = '/mnt/705300_rehaussement_marin/3- Data/LOT2/Au_Renard/WLcondQ.csv'
wlcond = pd.read_csv(pth, index_col = None,parse_dates= {"date" : ["year","month","day"]})
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
plt.title('au Renard', fontsize=10)
ax.set_ylim(min(wl_plt_s-1),max(wl_plt_s+1))
#ax.set_xlim([datetime.date(1975, 1, 1), datetime.date(2019, 12, 31)])
plt.ylabel('Niveau deau(m)')
# major_ticks = np.arange(0, 101, 20)
# ax.set_xticks(major_ticks)
plt.savefig('/mnt/705300_rehaussement_marin/3- Data/LOT2/WLmax_annual_au_Renard.png')


# %%
# Resample the hourly data to daily
data_wl = data_wl.set_index('Date')
wl_daily =data_wl.resample('D')['SL(m)'].agg(['max'])
wl_daily = wl_daily.rename(columns = {'max':'SL(m)'})

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
        wl = row['SL(m)']
        dll = d = datetime.datetime(yl,ml,dl)
        if dQQ == dll:
            df_WLcondQ.at[index,'Wlmax_0'] = wl
        elif (dll == dQQ - timedelta(days=1)):
            df_WLcondQ.at[index,'Wlmax_1'] = wl
        elif (dll == dQQ + timedelta(days=1)):
            df_WLcondQ.at[index,'Wlmax+1'] = wl 

maxValue = df_WLcondQ[['Wlmax_0', 'Wlmax_1','Wlmax+1']].max(axis=1)  #finding maximum value among these three days
df_WLcondQ['Wlmax'] = maxValue

df_WLcondQ = df_WLcondQ.drop(['Wlmax_0','Wlmax_1','Wlmax+1'], axis=1)

df_WLcondQ = df_WLcondQ.dropna()
# Write results to a .csv file

pth3  = r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\LOT2\Petit_Saguenay\WLcondQ.csv'
df_WLcondQ.to_csv(pth3,mode='w',index=False)

# calculating correlation    

tau, p_value_MK = stats.kendalltau(df_WLcondQ['Qmax'], df_WLcondQ['Wlmax'],nan_policy='omit')
rho, p_value_Sp = stats.spearmanr(df_WLcondQ['Qmax'], df_WLcondQ['Wlmax'],nan_policy='omit')


df_QcondWL = pd.DataFrame({'Date':wl_max['Date'],
                   'year':wl_max['year'],
                  'month':wl_max['month'],
                  'day': wl_max['day'],
                  'Wlmax':wl_max['SL(m)']})
                  

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
df_WLcondQ = df_WLcondQ.dropna()
pth3  = r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\LOT2\Petit_Saguenay\QcondWL.csv'
df_QcondWL.to_csv(pth3,mode='w',index=False)

# calculating correlation    

tau, p_value_MK = stats.kendalltau(df_QcondWL['Qmax'], df_QcondWL['Wlmax'],nan_policy='omit')
rho, p_value_Sp = stats.spearmanr(df_QcondWL['Qmax'], df_QcondWL['Wlmax'],nan_policy='omit')



# %% plot the difference in peak time (in days) of Water level anmd river flow annual maxima

tdiff = []
for index, row in wl_max.iterrows():
#    import pdb; pdb.set_trace()
    tdiff.append((row['Date']-Q_annual_max['date'][index]).days)

tdiff_abs =  [abs(i) for i in tdiff]
tdiff_df = pd.DataFrame(tdiff_abs,columns = ['TDifference (day)'])
# %% plot histogram of peak time difference


hist = np.histogram(tdiff_abs, density=False)


# calculating correlation    

import scipy.stats as stats
tau, p_value_MK = stats.kendalltau(df2['Qmax'], df2['Wlmax'],nan_policy='omit')
rho, p_value_Sp = stats.spearmanr(df2['Qmax'], df2['Wlmax'],nan_policy='omit')

### write to a csv file
df = df.dropna()
pth3  = r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\DFO-MPO\LOT1\EC\EC_Hmax_at_Qmax_100cm.csv'
df2.to_csv(pth3,mode='w',index=False)

# %%
# Plot Figure 4 (water level maxima annuel and WLcondQ) of report for Mitis, and Petite-Cascapedia

pth2 = '/mnt/705300_rehaussement_marin/3- Data/LOT2/Mitis/totalwl_and_tide.csv'
data_wl= pd.read_csv(pth2, index_col = None)


data_wl['Date'] = pd.to_datetime(data_wl['Date'])
data_wl = data_wl.set_index('Date')
data_wl = data_wl.loc['1968-01-01':'2019-12-31']  # 52

# finding annual maxima along with its day, month, year

data_wl =  data_wl.drop(['year'], axis=1)

data_wl.reset_index(inplace=True) 
data_wl['year'] = pd.DatetimeIndex(data_wl['Date']).year
data_wl['month'] = pd.DatetimeIndex(data_wl['Date']).month
data_wl['day'] = pd.DatetimeIndex(data_wl['Date']).day

wl_max =data_wl.loc[data_wl.groupby("year")["wl"].idxmax()]

# To plot the water level annual maxima

wl_max =  wl_max.drop(['TD(m)', 'Depth(m)','lat','lon','MSL','Residual','TD_est','year','month','day'], axis=1)
wl_max = wl_max.set_index('Date')
wl_max = wl_max.squeeze()



wl_plt =  data_wl.drop(['TD(m)', 'Depth(m)','lat','lon','MSL','Residual','TD_est','year','month','day'], axis=1)
wl_plt = wl_plt.set_index('Date')
wl_plt_s = wl_plt.squeeze()

pth = '/mnt/705300_rehaussement_marin/3- Data/LOT2/Mitis/WLcondQ.csv'
wlcond = pd.read_csv(pth, index_col = None,parse_dates= {"date" : ["year","month","day"]})
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
plt.title('Mitis', fontsize=10)
ax.set_ylim(min(wl_plt_s-1),max(wl_plt_s+1))
#ax.set_xlim([datetime.date(1975, 1, 1), datetime.date(2019, 12, 31)])
plt.ylabel('Niveau deau (m)')
# major_ticks = np.arange(0, 101, 20)
# ax.set_xticks(major_ticks)
plt.savefig('/mnt/705300_rehaussement_marin/3- Data/LOT2/WLmax_annual_Mitis.png')



