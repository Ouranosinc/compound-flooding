import lmoments3 as lm
from lmoments3 import distr,stats
import scikits.bootstrap as boot
import scipy.stats as st

# LMU = lm.lmom_ratios(Ann_max['Sea_Level(m)']) # This will give the first 5 moments of the sample distribution

paras_GEV = distr.gev.lmom_fit(Q_annual_max['50']) # this will give the parameters of GEV distrinbution
paras_GUM = distr.gum.lmom_fit(Q_annual_max['50']) # this will give the parameters of Gumbel distrinbution


paras_GEV_H = distr.gev.lmom_fit(WlQ['SL(m)']) # this will give the parameters of GEV distrinbution
paras_GUM_H = distr.gum.lmom_fit(WlQ['SL(m)']) # this will give the parameters of Gumbel distrinbution



# fitted_gev = distr.gev(**paras_GEV)
# fitted_gum = distr.gum(**paras_GUM)


import scipy.stats as st
fitted_params = st.gumbel_r.fit(dfH['Qmax'])
logLik = np.sum( st.gumbel_r.logpdf(dfH['Qmax'], loc=fitted_params[0], scale=fitted_params[1]) ) 
k = 2
aic_gum = 2*k - 2*(logLik)


import scipy.stats as st
fitted_params = st.genextreme.fit(dfH['Qmax'])
logLik = np.sum( st.genextreme.logpdf(dfH['Qmax'], fitted_params[0], loc=fitted_params[1], scale=fitted_params[2]) ) 
k = 3
aic_gev = 2*k - 2*(logLik)





# # calculating the AIC criterion and selecting the best model

# AIC_gev= stats.AIC(Q_annual_max['50'], 'gev', paras_GEV)
# AIC_gumbel = stats.AIC(Q_annual_max['50'], 'gum', paras_GUM)


# AIC_gev= stats.AIC(dfH['Qmax'], 'gev', paras_GEV)
# AIC_gumbel = stats.AIC(dfH['Qmax'], 'gum', paras_GUM)



#ci = boot.ci(Ann_max_clean, st.gumbel_r.fit)
ci = boot.ci(Q_annual_max['50'], st.gumbel_r.fit,alpha=0.05)

# param_l = {"c":ci[0,0],"loc": ci[0,1],"scale": ci[0,2]}
param_m = {"loc": 5.361,"scale": 0.247}
# param_h = {"c":ci[1,0],"loc": ci[1,1],"scale": ci[1,2]}

param_l_Q = {"loc": ci[0,0],"scale": ci[0,1]}
param_m_Q = {"loc": paras_GUM['loc'],"scale": paras_GUM['scale']}
param_h_Q = {"loc": ci[1,0],"scale": ci[1,1]}


# ddl = distr.gev(**param_l)
ddm = distr.gev(**param_m)
# ddh = distr.gev(**param_h)

ddl = distr.gum(**param_l_Q)
ddm = distr.gum(**param_m_Q)
ddh = distr.gum(**param_h_Q)


T = np.arange(1,350,1) +1
gevRP_l = ddl.ppf(1.0-1./T)
gevRP_m = ddm.ppf(1.0-1./T)
gevRP_h = ddh.ppf(1.0-1./T)



Result = pd.DataFrame({'T':T,
                   'RP':gevRP_m})




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
plt.savefig('C:/Users/mohbiz1/Desktop/Dossier_travail/705300_rehaussement_marin/3- Data/DFO-MPO/LOT1/SA/RP_stationary_Q_SA.png')

#save the workspace

import dill

dill.dump_session('C:/Users/mohbiz1/Desktop/Dossier_travail/705300_rehaussement_marin/3- Data/DFO-MPO/LOT1/SA/SA_bk_dill.pkl')

# to restore session

dill.load_session('C:/Users/mohbiz1/Desktop/Dossier_travail/705300_rehaussement_marin/3- Data/DFO-MPO/LOT1/SA/SA_bk_dill_Q.pkl')




pth3  = r'C:/Users/mohbiz1/Desktop/Dossier_travail/705300_rehaussement_marin/3- Data/DFO-MPO/LOT1/SA/RP_wl_50cm.csv'
summary_H_50cm.to_csv(pth3,mode='w')




