
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import datetime
from datetime import timedelta
import scipy.stats as stats
import pingouin as pg
import os
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

pth = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT3/Nicolet/WLcondQ.csv'
data = pd.read_csv(pth, index_col = None,parse_dates= {"date" : ["year","month","day"]})
data =  data.drop(['Date'], axis=1)
data = data.set_index('date')
# %% WLcondQ
pg.corr(data['Qmax'],data['Wlmax'],method='kendall')
sns.set(style='whitegrid', font_scale=1.2)
g = sns.jointplot(data=data, x="Qmax", y="Wlmax", color = "r")
g.plot_joint(sns.scatterplot,color="r")
g.plot_marginals(sns.histplot, kde=True, color="r")
g.plot_joint(sns.regplot,ci = None, color="r")
g.ax_joint.text(800, 4.0, r'$\tau$'' = 0.26, p = 0.006', fontstyle='italic')
g.ax_joint.set_xlabel('Qmax($m^3$/s)')
g.ax_joint.set_ylabel('$WL_{cond}Q(m)$')
g.fig.suptitle("Nicolet")                  
plt.savefig('/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT3/scatter_WLcondQ_Nicolet.png',dpi=300)                
 
# %% QcondWL       
pth = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT3/Nicolet/QcondWL.csv'
data = pd.read_csv(pth, index_col = None,parse_dates= {"date" : ["year","month","day"]})
data =  data.drop(['Date'], axis=1)
data = data.set_index('date')              

pg.corr(data['Wlmax'],data['Qmax'],method='kendall')

sns.set(style='whitegrid', font_scale=1.2)
g = sns.jointplot(data=data, x="Wlmax", y="Qmax", color = "r")
g.plot_joint(sns.scatterplot,color="r")
g.plot_marginals(sns.histplot, kde=True, color="r")
g.plot_joint(sns.regplot,ci = None, color="r")
g.ax_joint.text(6.0, 50, r'$\tau$'' = 0.17, p = 0.08', fontstyle='italic')
g.ax_joint.set_xlabel('WLmax(m)')
g.ax_joint.set_ylabel('$Q_{cond}$WL($m^3$/s)')
g.fig.suptitle("Nicolet")                  
plt.savefig('/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT3/scatter_QcondWL_Nicolet.png',dpi=300)                

# %% plot histograms
pth = r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\LOT2\Chaudiere\QcondWL.csv'
data = pd.read_csv(pth, index_col = None,parse_dates= {"date" : ["year","month","day"]})
data =  data.drop(['Date'], axis=1)

s_wl = data['date'].groupby([data.date.dt.month]).agg('count')
df_wl = s_wl .to_frame()
df_wl = df_wl.rename(columns = {'date':'Wlmax'})
df_wl = df_wl.reset_index()
df_wl['Probability'] = (df_wl['Wlmax']/(df_wl['Wlmax'].sum()))*100
df_wl = df_wl.rename(columns = {'date':'month'})
# data['month'] = data['date'].dt.strftime('%b')
df_wl['Wlmax'] =  df_wl['Probability']
df_wl =  df_wl.drop(['Probability'], axis=1)

pth = r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\LOT2\Chaudiere\WlcondQ.csv'
data2 = pd.read_csv(pth, index_col = None,parse_dates= {"date" : ["year","month","day"]})
data2 =  data2.drop(['Date'], axis=1)
s_Q = data2['date'].groupby([data2.date.dt.month]).agg('count')
df_Q = s_Q .to_frame()
df_Q = df_Q.rename(columns = {'date':'Qmax'})
df_Q = df_Q.reset_index()
df_Q['Probability'] = (df_Q['Qmax']/(df_Q['Qmax'].sum()))*100
df_Q = df_Q.rename(columns = {'date':'month'})
df_Q['Qmax'] =  df_Q['Probability']
df_Q =  df_Q.drop(['Probability'], axis=1)
# data2['month'] = data2['date'].dt.strftime('%b')

path = os.getcwd()
os.chdir(r"C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\LOT2")

df = pd.merge(df_wl, df_Q, on='month', how = 'outer')
df = df.fillna(0)
df = df.sort_values('month')
df = pd.melt(df, id_vars="month", var_name="variable", value_name="Probability")
m_names= st = {1:'Jan', 2:'Fev', 3:'Mar', 4:'Avr', 5:'Mai', 6:'Juin', 7:'Juil', 8:'Auot', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}  
df['Mois'] = df['month'].map(m_names)
df['Probabilité'] = df['Probability']
#plot
sns.set(style='whitegrid', font_scale=1.2)
ax = sns.catplot(x='Mois', y='Probabilité', hue='variable', data=df, kind='bar')
ax.fig.suptitle("Chaudiere")
plt.savefig('Qmax_Hmax_histogram_Montmorency.png')

# %% read the water level dataset of riviere au renard et riviere Ha Ha

# Step 1: Read and join the csv water levels 

import os
import pandas as pd
from glob import glob
import datetime
from datetime import timedelta
import scipy.stats as stats

# check current working directory and change it to where the csv files reside
path = os.getcwd()
os.chdir(r"C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\LOT2\Rimouski\wl_hourly_data")
files = sorted(glob('2985-01-JAN-*_slev.csv'))

wl = pd.concat((pd.read_csv(file, encoding="ISO-8859-1", skiprows = 7)
                for file in files),ignore_index=True )
wl['Date'] = pd.to_datetime(wl["Date"])
wl = wl.set_index('Date')

# the wl has the hourly data, so we transform it to daily data to work with river flow (correlation, etc.)

data_wl_daily_max = wl.groupby(pd.Grouper(freq='D')).max()

wl = wl.reset_index()
data_wl_daily = wl.groupby([pd.Grouper(key='Date',freq='D')]).size().reset_index(name='count')

wl_days = (data_wl_daily[data_wl_daily["count"] == 24])

data_wl_daily_max = data_wl_daily_max.reset_index()
wl_daily_data=pd.merge(wl_days['count'],data_wl_daily_max['wl'],left_on=wl_days['Date'],right_on=data_wl_daily_max['Date'])

# constructing the compound dataframe wlcondQ

wl_daily_data = wl_daily_data.rename(columns = {'key_0':'Date'})
wl_daily_data =  wl_daily_data.drop(['count'], axis=1)


wl_daily_data['year'] = pd.DatetimeIndex(wl_daily_data['Date']).year
wl_daily_data['month'] = pd.DatetimeIndex(wl_daily_data['Date']).month
wl_daily_data['day'] = pd.DatetimeIndex(wl_daily_data['Date']).day

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
    for index2,row in wl_daily_data.iterrows():
        yl = row['year']
        ml = row['month']
        dl = row['day']
        wl = row['wl']
        dll = d = datetime.datetime(yl,ml,dl)
        if dQQ == dll:
            df_WLcondQ.at[index,'Wlmax_0'] = wl
        elif (dll == dQQ - timedelta(days=1)):
            df_WLcondQ.at[index,'Wlmax_1'] = wl
        elif (dll == dQQ + timedelta(days=1)):
            df_WLcondQ.at[index,'Wlmax+1'] = wl 

df_WLcondQ = df_WLcondQ.dropna()

maxValue = df_WLcondQ[['Wlmax_0', 'Wlmax_1','Wlmax+1']].max(axis=1)  #finding maximum value among these three days
df_WLcondQ['Wlmax'] = maxValue

df_WLcondQ = df_WLcondQ.drop(['Wlmax_0','Wlmax_1','Wlmax+1'], axis=1)

# Write results to a .csv file

pth3  = r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\LOT2\Au_Renard\WLcondQ_50cm.csv'
df_WLcondQ.to_csv(pth3,mode='w',index=False)

# calculating correlation    

tau, p_value_MK = stats.kendalltau(df_WLcondQ['Qmax'], df_WLcondQ['Wlmax'],nan_policy='omit')
rho, p_value_Sp = stats.spearmanr(df_WLcondQ['Qmax'], df_WLcondQ['Wlmax'],nan_policy='omit')


# calculating the compound flooding for QcondWL

wl_max =wl_daily_data.loc[wl_daily_data.groupby("year")["wl"].idxmax()]

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

pth3  = r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\LOT2\Au_Renard\QcondWL_50cm.csv'
df_QcondWL.to_csv(pth3,mode='w',index=False)

tau, p_value_MK = stats.kendalltau(df_QcondWL['Qmax'], df_QcondWL['Wlmax'],nan_policy='omit')
rho, p_value_Sp = stats.spearmanr(df_QcondWL['Qmax'], df_QcondWL['Wlmax'],nan_policy='omit')


# %% Analysis of water level with sea level rise

import os
import pandas as pd
from glob import glob
import datetime
from datetime import timedelta
import scipy.stats as stats

# check current working directory and change it to where the csv files reside
path = os.getcwd()
os.chdir(r"C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\LOT2\Au_Renard\wl_hourly_data")
files = sorted(glob('2330-01-JAN-*_slev.csv'))

wl = pd.concat((pd.read_csv(file, encoding="ISO-8859-1")
                for file in files),ignore_index=True)
wl['Date'] = pd.to_datetime(wl["Date"])
wl = wl.set_index('Date')

wl = wl + 0.6128 # 95e percentile du rehaussement marin a l'horizon 2070

# the wl has the hourly data, so we transform it to daily data to work with river flow (correlation, etc.)

data_wl_daily_max = wl.groupby(pd.Grouper(freq='D')).max()

wl = wl.reset_index()
data_wl_daily = wl.groupby([pd.Grouper(key='Date',freq='D')]).size().reset_index(name='count')

wl_days = (data_wl_daily[data_wl_daily["count"] == 24])

data_wl_daily_max = data_wl_daily_max.reset_index()
wl_daily_data=pd.merge(wl_days['count'],data_wl_daily_max['wl'],left_on=wl_days['Date'],right_on=data_wl_daily_max['Date'])

# constructing the compound dataframe wlcondQ

wl_daily_data = wl_daily_data.rename(columns = {'key_0':'Date'})
wl_daily_data =  wl_daily_data.drop(['count'], axis=1)


wl_daily_data['year'] = pd.DatetimeIndex(wl_daily_data['Date']).year
wl_daily_data['month'] = pd.DatetimeIndex(wl_daily_data['Date']).month
wl_daily_data['day'] = pd.DatetimeIndex(wl_daily_data['Date']).day

# %% read (estimated) sea level time series at Mitis, Outardes, Matane outlets










 
