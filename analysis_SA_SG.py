
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
from scipy import spatial



pth2 = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/DFO-MPO/Saguenay_MPO.csv'
#pth2 = r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\DFO-MPO\EC.csv'
data = pd.read_csv(pth2, index_col = 0,squeeze=True)
data = data.to_frame()
data.reset_index(inplace=True) 


data['date'] = pd.to_datetime(data['date'])
data = data.set_index('date')


data['year'] = pd.DatetimeIndex(data['date']).year
data['month'] = pd.DatetimeIndex(data['date']).month
data['day'] = pd.DatetimeIndex(data['date']).day

fig,ax = plt.subplots(1,1,sharex = True,figsize=(8, 4))
ax.plot(data,'k')
ax.set_ylabel('Water Level (m)')
ax.set_xlabel('year')
ax.legend();
plt.grid('on')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.savefig('C:/Users/mohbiz1/Desktop/Dossier_travail/705300_rehaussement_marin/3- Data/DFO-MPO/LOT1/AM/Saguenay.png')



# %%
pth2 = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/DFO-MPO/LOT1/A_Mars/A_Mars_wl_data.csv'
#pth2 = r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\DFO-MPO\EC.csv'
data_wl = pd.read_csv(pth2, index_col = False)

data_wl.reset_index(inplace=True) 
data_wl['Date'] = pd.to_datetime(data_wl['Date'])
data_wl = data_wl.set_index('Date')

data_wl = data_wl.rename(columns = {'Sea_Level(m)':'Water Level (m)'})

data_wl['year'] = pd.DatetimeIndex(data_wl['Date']).year
data_wl['month'] = pd.DatetimeIndex(data_wl['Date']).month
data_wl['day'] = pd.DatetimeIndex(data_wl['Date']).day

fig,ax = plt.subplots(1,1,sharex = True,figsize=(8, 4))
ax.plot(data_AM,'k')
ax.set_ylabel('Water Level (m)')
ax.set_xlabel('year')
ax.legend();
plt.grid('on')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.savefig('C:/Users/mohbiz1/Desktop/Dossier_travail/705300_rehaussement_marin/3- Data/DFO-MPO/LOT1/Riviere_a_mars/Riviere_a_mars.png')


#############################################################

data_SG = data.loc['1975-01-01':'1990-12-31']  # 
data_AMA = data_wl.loc['1975-01-01':'1990-12-31']

# data_AMA.reset_index(inplace=True) 
# data_SG.reset_index(inplace=True) 

# Finding daily maximum
data_SG_daily_max = data_SG.groupby(pd.Grouper(freq='D')).max()
data_AM_daily_max = data_AMA.groupby(pd.Grouper(freq='D')).max()

data_SG_daily_max = data_SG_daily_max.rename(columns = {'Water Level (m)':'WL_m_SG'})
data_AM_daily_max = data_AM_daily_max.rename(columns = {'Water Level (m)':'WL_m_AM'})

#Finding the number of hours with data in each day
data_SG_daily = data_SG.groupby([pd.Grouper(key='date',freq='D')]).size().reset_index(name='count')
data_AM_daily = data_AMA.groupby([pd.Grouper(key='Date',freq='D')]).size().reset_index(name='count')


SG_days = (data_SG_daily[data_SG_daily["count"] == 24])
AM_days = (data_AM_daily[data_AM_daily["count"] == 24])

#Intersecting the daily maxima with dataframe containg the number of entries per day

SG_daily_data=pd.merge(SG_days['count'],data_SG_daily_max['WL_m_SG'],left_on=SG_days['date'],right_on=data_SG_daily_max['date'])
AM_daily_data=pd.merge(AM_days['count'],data_AM_daily_max['WL_m_AM'],left_on=AM_days['Date'],right_on=data_AM_daily_max['Date'])


# data_AMA = data_AMA.set_index('Date')
# data_SG = data_SG.set_index('date')

# merge=pd.merge(data_SG['Sea_Level_m'],data_AMA['Sea_Level(m)'], how='inner', left_index=True, right_index=True)

# data_SG_daily_max.reset_index(inplace=True) 
# data_AM_daily_max.reset_index(inplace=True) 

merge=pd.merge(SG_daily_data['WL_m_SG'],AM_daily_data['WL_m_AM'],left_on=SG_daily_data['key_0'],right_on=AM_daily_data['key_0'])

merge_clean = merge.dropna()

idx = np.isfinite(merge_clean['WL_m_SG']) & np.isfinite(merge_clean['WL_m_AM'])
fit = np.polyfit(merge_clean['WL_m_SG'][idx],merge_clean['WL_m_AM'][idx], 1)
fit_fn = np.poly1d(fit)


correlation_matrix = np.corrcoef(merge_clean['WL_m_SG'], merge_clean['WL_m_AM'])
correlation_xy = correlation_matrix[0,1]
r_squared = correlation_xy**2


from sklearn.metrics import r2_score
predict = np.poly1d(fit_fn)
R2 = r2_score(merge_clean['WL_m_SG'], predict(merge_clean['WL_m_SG']))
print(R2)


fig,ax = plt.subplots(1,1,sharex = True,figsize=(8, 4))
ax.plot(merge_clean['WL_m_SG'],merge_clean['WL_m_AM'],'o')
ax.set_ylabel('Water Level (m) à Mars')
ax.set_xlabel('Water Level (m) Tadoussac')
ax.legend();
plt.grid('on')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.savefig('C:/Users/mohbiz1/Desktop/Dossier_travail/705300_rehaussement_marin/3- Data/DFO-MPO/LOT1/A_Mars/linear_Saguenay_a_mars_daily_max_complete_cycle.png')


########################################################################################
# water level for petit Saguenay
wl_PS = data_wl
wl_PS['Water Level (m)']  = 1.09028*((data_wl['Water Level (m)']+0.33)/1.244)-0.1221

pth3  = r'C:/Users/mohbiz1/Desktop/Dossier_travail/705300_rehaussement_marin/3- Data/LOT2/Petit_Saguenay/PS_wl_data.csv'
wl_PS.to_csv(pth3,mode='w',index=False)

# water level for Saint-Jean

wl_Saint_Jean = pd.DataFrame({'Date':data_wl['Date']})

wl_Saint_Jean['Water Level (m)']  = 1.102*((data_wl['Water Level (m)']+0.33)/1.244)-0.139

pth3  = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT2/Saint_Jean/wl_data.csv'
wl_Saint_Jean.to_csv(pth3,mode='w',index=False)



########################################################################################
# finding the  intercept when slope is 1

X = merge_clean['WL_m_SG']
Y = merge_clean['WL_m_AM']
s = 1

def f(i):
    """Fixed slope 1-deg polynomial residuals"""
    return ((Y - (s*X + i))**2).sum()

from scipy.optimize import fsolve

fsolve(f,x0=0.05)











