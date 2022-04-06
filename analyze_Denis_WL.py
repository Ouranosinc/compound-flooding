
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
from scipy import spatial
import lmoments3 as lm
from lmoments3 import distr,stats
import scikits.bootstrap as boot
import scipy.stats as st
from scipy.stats import genextreme



pth2 = r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\DFO-MPO\LOT1\A_Mars\A_Mars_Hmax_annual.csv'
#pth2 = r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\DFO-MPO\EC.csv'
data_50cm = pd.read_csv(pth2, index_col = 0,squeeze=False)

data_50cm = data_50cm.rename(columns = {'tstep':'Date'})

data_50cm['year'] = pd.DatetimeIndex(data_50cm['Date']).year
data_50cm['month'] = pd.DatetimeIndex(data_50cm['Date']).month
data_50cm['day'] = pd.DatetimeIndex(data_50cm['Date']).day

data_50cm['Date'] = pd.to_datetime(data_50cm['Date'])
data_50cm = data_50cm.set_index('Date')
data_50cm = data_50cm.loc['1968-01-01':'2019-12-31']  # 58

data_100cm= data_100cm.rename(columns = {'SL(m)':'Water Level(m)'})
# pth3  = r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\DFO-MPO\LOT1\JC\JC_normal.csv'
# data.to_csv(pth3,mode='w')




# finding annual maxima along with its day, month, year

data_100cm.reset_index(inplace=True) 
wl_max_100cm =data_100cm.loc[data_100cm.groupby("year")["Water Level(m)"].idxmax()]

pth3  = r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\DFO-MPO\LOT1\EC\EC_Hmax_annual_100cm.csv' 
wl_max_100cm.to_csv(pth3,mode='w',index=False)

# wl_max = wl_max.rename(columns = {'tstep':'Date'})

pth = r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\Debits_Journ_Exutoire.xlsx'
data_Q = pd.read_excel(pth, index_col = 0, squeeze=True, sheet_name = 'SLSO02381')

## resampling the water level data to daily and running the extremal analysis
data_100cm = data_100cm.set_index('Date')
wl_daily_100cm =data_100cm.resample('D')['Water Level(m)'].agg(['max'])
wl_daily_100cm= wl_daily_100cm.rename(columns = {'max':'Water Level(m)'})

Wl_daily_50cm = wl_daily_50cm.squeeze()

## running the extremal analysis
from pyextremes import EVA
modelwl_50cm = EVA(Wl_daily_50cm)

# step 3: selecting the annual maxima

modelwl_50cm.get_extremes(method="BM", block_size="365.2425D", errors = 'ignore')

#step 5: fit the extreme value analysis

modelwl_100cm.fit_model()


#  

modelwl_100cm.plot_diagnostic(alpha=0.95)

# step 6: calculating the extreme values

summary_H_100cm= modelwl_100cm.get_summary(
    return_period=[1, 2, 5, 10, 20, 25, 50, 100, 350, 500, 1000],
    alpha=0.95,
    n_samples=1000)

pth3  = r'C:/Users/mohbiz1/Desktop/Dossier_travail/705300_rehaussement_marin/3- Data/DFO-MPO/LOT1/EC/RP_wl_100cm.csv'
summary_H_100cm.to_csv(pth3,mode='w')



array = np.array([[4.292,4.229,4.357],[4.535,4.437,4.640],[4.696,4.571,4.824],[4.899,4.738,5.063],[5.050,4.861,5.238],[5.20,4.983,5.412],[5.470,5.204,5.730]])

summary_H_normal = pd.DataFrame(data=array, index=[2.0,5.0,10.0,25.0,50.0,100.0,350.0], columns=["return value", "lower ci", "upper ci"])

## plots


# plots

T = [2.0,5.0,10.0,25.0,50.0,100.0,350.0]

H_50_lower = [summary_H_50cm['lower ci'][2.0],summary_H_50cm['lower ci'][5.0],summary_H_50cm['lower ci'][10.0],
              summary_H_50cm['lower ci'][25.0],summary_H_50cm['lower ci'][50.0],summary_H_50cm['lower ci'][100.0],
              summary_H_50cm['lower ci'][350.0]]

H_50_upper = [summary_H_50cm['upper ci'][2.0],summary_H_50cm['upper ci'][5.0],summary_H_50cm['upper ci'][10.0],
              summary_H_50cm['upper ci'][25.0],summary_H_50cm['upper ci'][50.0],summary_H_50cm['upper ci'][100.0],
              summary_H_50cm['upper ci'][350.0]]

H_50_median = [summary_H_50cm['return value'][2.0],summary_H_50cm['return value'][5.0],summary_H_50cm['return value'][10.0],
              summary_H_50cm['return value'][25.0],summary_H_50cm['return value'][50.0],summary_H_50cm['return value'][100.0],
              summary_H_50cm['return value'][350.0]]

H_100_lower = [summary_H_100cm['lower ci'][2.0],summary_H_100cm['lower ci'][5.0],summary_H_100cm['lower ci'][10.0],
              summary_H_100cm['lower ci'][25.0],summary_H_100cm['lower ci'][50.0],summary_H_100cm['lower ci'][100.0],
              summary_H_100cm['lower ci'][350.0]]

H_100_upper = [summary_H_100cm['upper ci'][2.0],summary_H_100cm['upper ci'][5.0],summary_H_100cm['upper ci'][10.0],
              summary_H_100cm['upper ci'][25.0],summary_H_100cm['upper ci'][50.0],summary_H_100cm['upper ci'][100.0],
              summary_H_100cm['upper ci'][350.0]]

H_100_median = [summary_H_100cm['return value'][2.0],summary_H_100cm['return value'][5.0],summary_H_100cm['return value'][10.0],
              summary_H_100cm['return value'][25.0],summary_H_100cm['return value'][50.0],summary_H_100cm['return value'][100.0],
              summary_H_100cm['return value'][350.0]]


fig,ax = plt.subplots(1,1,sharex = True,figsize=(6, 4))
ax.plot([2.05,5.0,10.0,25.0,50.0,100.0,350.0],summary_H_normal['return value'],'b-', label='Reference')
ax.plot([2.05,5.0,10.0,25.0,50.0,100.0,350.0],H_50_median,color = 'orange', label='SLR: 50cm')
ax.plot([2.05,5.0,10.0,25.0,50.0,100.0,350.0],H_100_median,color = 'orangered', label='SLR: 100cm')

ax.fill_between([2.05,5.0,10.0,25.0,50.0,100.0,350.0], summary_H_normal['lower ci'], summary_H_normal['upper ci'],
                  facecolor="orange", # The fill color
                  color='cornflowerblue',       # The outline color
                  alpha=0.2)          # Transparency of the fill

ax.set_ylabel('Water Level(m)')
ax.set_xlabel('Return period (yr)')
#ax.set_xticks([2.05,5.0,10.0,25.0,50.0,100.0,350.0])
ax.legend(loc = 'lower right');
#plt.grid('on')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.fill_between([2.05,5.0,10.0,25.0,50.0,100.0,350.0], H_50_lower, H_50_upper,
                  facecolor="orange", # The fill color
                  color='orange',       # The outline color
                  alpha=0.2)          # Transparency of the fill
ax.fill_between([2.05,5.0,10.0,25.0,50.0,100.0,350.0], H_100_lower, H_100_upper,
                  facecolor="orangered", # The fill color
                  color='orangered',       # The outline color
                  alpha=0.2)          # Transparency of the fill
ax.set_title('Etchemin')
ax.set_xticks([2,10,20,50,100,350])
plt.xticks(fontsize = 7)
ax.grid(axis='both')
plt.savefig('C:/Users/mohbiz1/Desktop/Dossier_travail/705300_rehaussement_marin/3- Data/DFO-MPO/LOT1/EC/RP_CC.png',dpi=300)



### pour riviere à mars
T = [2.0,5.0,10.0,25.0,50.0,100.0,350.0]
summary_H_normal = summary_H.loc[summary_H.index.isin(T)]
summary_H_rcp85_95e_percentile =summary_H_normal.copy() 
summary_H_rcp85_95e_percentile['return value'] = summary_H_normal['return value'] + 0.482


fig,ax = plt.subplots(1,1,sharex = True,figsize=(6, 4))
ax.plot([2.05,5.0,10.0,25.0,50.0,100.0,350.0],summary_H_normal['return value'],'b-', label='Reference')
ax.plot([2.05,5.0,10.0,25.0,50.0,100.0,350.0],summary_H_rcp85_median['return value'],color = 'orangered', label='SLR:RCP 8.5,H2070,95e percentile')

ax.fill_between([2.05,5.0,10.0,25.0,50.0,100.0,350.0], summary_H_normal['lower ci'], summary_H_normal['upper ci'],
                  facecolor="orange", # The fill color
                  color='cornflowerblue',       # The outline color
                  alpha=0.2)          # Transparency of the fill

ax.set_ylabel('Water Level(m)')
ax.set_xlabel('Return period (yr)')
#ax.set_xticks([2.05,5.0,10.0,25.0,50.0,100.0,350.0])
ax.legend(loc = 'lower right');
#plt.grid('on')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_title('à Mars')
ax.set_xticks([2,10,20,50,100,350])
plt.xticks(fontsize = 7)
ax.grid(axis='both')
plt.savefig('C:/Users/mohbiz1/Desktop/Dossier_travail/705300_rehaussement_marin/3- Data/DFO-MPO/LOT1/A_Mars/RP_CC.png',dpi=300)



















plt.savefig('RP_stationary_Q_SA.png')









## find the annual maximum flow nad its index
Q = data_Q.loc['1968-01-01':'2019-12-31']['50']  # 45 years
Q_df = Q.to_frame()
Q_df= Q_df.rename(columns = {'50':'Discharge (m3/s)'})

Q_df.reset_index(inplace=True)
Q_df= Q_df.rename(columns = {'Time':'Date'})
Q_df['year'] = pd.DatetimeIndex(Q_df['Date']).year
Q_df['month'] = pd.DatetimeIndex(Q_df['Date']).month
Q_df['day'] = pd.DatetimeIndex(Q_df['Date']).day

Q = Q_df.squeeze()




Q.reset_index(inplace=True) 
wl_max =data.loc[data.groupby("year")["SL(m)"].idxmax()]















# Extreme value analysis

paras_GEV_H = distr.gev.lmom_fit(wl_max['SL(m)']) # this will give the parameters of GEV distrinbution
paras_GUM_H = distr.gum.lmom_fit(wl_max['SL(m)']) # this will give the parameters of Gumbel distrinbution



# fitted_gev = distr.gev(**paras_GEV_H)
# fitted_gum = distr.gum(**paras_GUM)

# calculating the AIC criterion and selecting the best model

AIC_gev= stats.AIC(wl_max['SL(m)'], 'gev', paras_GEV_H)
AIC_gumbel = stats.AIC(wl_max['SL(m)'], 'gum', paras_GUM_H)

dd = wl_max['SL(m)']

ci = boot.ci(data_50cm['Water Level(m)'], st.genpareto.fit,alpha=0.05)
ci = boot.ci(wl_max['SL(m)'], st.genextreme.fit,alpha=0.05,n_samples=1000)


# param_l_H = {"c":ci[0,0],"loc": ci[0,1],"scale": ci[0,2]}
# param_m_H = {"c":paras_GEV_H['c'],"loc": paras_GEV_H['loc'],"scale": paras_GEV_H['scale']}
# param_h_H = {"c":ci[1,0],"loc": ci[1,1],"scale": ci[1,2]}



param_l_H = {"loc": ci[0,0],"scale": ci[0,1]}
param_m_H = {"loc": paras_GUM_H['loc'],"scale": paras_GUM_H['scale']}
param_h_H = {"loc": ci[1,0],"scale": ci[1,1]}


ddl = distr.gum(**param_l_H)
ddm = distr.gum(**param_m_H)
ddh = distr.gum(**param_h_H)

# ddl = distr.gev(**param_l_H)
# ddm = distr.gev(**param_m_H)
# ddh = distr.gev(**param_h_H)



T = np.arange(1,350,1) +1
gevRP_l = ddl.ppf(1.0-1./T)
gevRP_m = ddm.ppf(1.0-1./T)
gevRP_h = ddh.ppf(1.0-1./T)


# plots



fig,ax = plt.subplots(1,1,sharex = True,figsize=(8, 4))
ax.fill_between(T, gevRP_l, gevRP_h,
                  facecolor="orange", # The fill color
                  color='cornflowerblue',       # The outline color
                  alpha=0.2)          # Transparency of the fill

ax.plot(T,gevRP_m,'b-')
ax.set_ylabel('Water Level (m)')
ax.set_xlabel('Return period (yr)')
ax.legend();
plt.grid('on')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.savefig('C:/Users/mohbiz1/Desktop/Dossier_travail/705300_rehaussement_marin/3- Data/DFO-MPO/LOT1/SA/RP_stationary_H_SA.png')

#save the workspace
import dill


dill.dump_session('C:/Users/mohbiz1/Desktop/Dossier_travail/705300_rehaussement_marin/3- Data/DFO-MPO/LOT1/SA/SA_bk_dill_H.pkl')

# to restore session

dill.load_session('C:/Users/mohbiz1/Desktop/Dossier_travail/705300_rehaussement_marin/3- Data/DFO-MPO/LOT1/SA/SA_bk_dill_H.pkl')








