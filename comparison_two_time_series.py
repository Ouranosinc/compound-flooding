
import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns
from scipy.stats import ks_2samp
# from statannot import add_stat_annotation
# %% WLcondQ
name = 'Maskinonge'
serie = 'WLcondQ'


pth = os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT3/'+name+'/'+serie+'_1968_1984.csv')
data = pd.read_csv(pth, index_col = None,parse_dates= {"date" : ["year","month","day"]})
data =  data.drop(['Date'], axis=1)
data = data.set_index('date')
data['type'] = '1968-1984'
data['outlet'] = name
data['serie'] = serie

pth2 = os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT3/'+name+'/'+serie+'_1985_2020.csv')
data2 = pd.read_csv(pth2, index_col = None,parse_dates= {"date" : ["year","month","day"]})
data2 =  data2.drop(['Date'], axis=1)
data2 = data2.set_index('date')

data2['type'] = '1985-2020'
data2['outlet'] = name
data2['serie'] = serie

result = pd.concat([data,data2],axis=0)
del data,data2,pth

serie = 'QcondWL'
pth = os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT3/'+name+'/'+serie+'_1968_1984.csv')
data = pd.read_csv(pth, index_col = None,parse_dates= {"date" : ["year","month","day"]})
data =  data.drop(['Date'], axis=1)
data = data.set_index('date')
data['type'] = '1968-1984'
data['outlet'] = name
data['serie'] = serie

pth2 = os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT3/'+name+'/'+serie+'_1985_2020.csv')
data2 = pd.read_csv(pth2, index_col = None,parse_dates= {"date" : ["year","month","day"]})
data2 =  data2.drop(['Date'], axis=1)
data2 = data2.set_index('date')

data2['type'] = '1985-2020'
data2['outlet'] = name
data2['serie'] = serie

result2 = pd.concat([data,data2],axis=0)
del data,data2,pth

Maskinonge = pd.concat([result,result2],axis=0)
del result,result2,pth



data = pd.concat([Assomption,Maskinonge,Batiscan],axis=0)



data_WLcondQ = data[data['serie']=='WLcondQ']
data_QcondWL = data[data['serie']=='QcondWL']

g = sns.FacetGrid(data_WLcondQ, row="serie", col="outlet", hue='type', margin_titles=True,sharex=False, sharey=False)
g.map(sns.scatterplot, "Qmax", "Wlmax", alpha=.7)
g.add_legend()
plt.savefig(os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/5- Rapports/LOT3/scatterplot.png'),dpi=300,bbox_inches='tight')  

g = sns.FacetGrid(data_QcondWL, row="serie", col="outlet", hue='type', margin_titles=True,sharex=False, sharey=False)
g.map(sns.scatterplot, "Wlmax", "Qmax", alpha=.7)
plt.savefig(os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/5- Rapports/LOT3/scatterplot2.png'),dpi=300,bbox_inches='tight')  














# sns.set(style='ticks', font_scale=1)
# g = sns.scatterplot(data=result, x="Qmax", y="Wlmax", hue = 'type')
# g.set(xlabel ='Qmax($m^3$/s)',ylabel = '$WL_{cond}Q(m)$')
# g.legend(bbox_to_anchor=(1.02, 1),loc = 'upper left',title = 'Serie',borderaxespad=0)
# g.set_title(name,fontsize=12)    
# sns.despine()

# # g.axvline(result.Qmax.quantile(0.9),color = "r",linestyle='--') 
# # g.axhline(result.Wlmax.quantile(0.9),color = "r",linestyle='--') 

# # g.axvline(result.Qmax.quantile(0.5),color = "k",linestyle='--') 
# # g.axhline(result.Wlmax.quantile(0.5),color = "k",linestyle='--') 

# plt.savefig(os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT3/'+name+'/WLcondQ_scatter_2.png'),dpi=300,bbox_inches='tight')  

# pth3 = os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/5- Rapports/LOT3/data.csv')
# data.to_csv(pth3,mode='w',index=True)

# %% QcondWL
name = 'Batiscan'

pth = os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT3/'+name+'/QcondWL_1968_2020.csv')
#pth = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT3/Nicolet/WLcondQ.csv'
data = pd.read_csv(pth, index_col = None,parse_dates= {"date" : ["year","month","day"]})
data =  data.drop(['Date'], axis=1)
data = data.set_index('date')
data['type'] = '1968-2020'


pth2 = os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT3/'+name+'/QcondWL_1985_2020.csv')
#pth = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT3/Nicolet/WLcondQ.csv'
data2 = pd.read_csv(pth2, index_col = None,parse_dates= {"date" : ["year","month","day"]})
data2 =  data2.drop(['Date'], axis=1)
data2 = data2.set_index('date')

data2['type'] = '1985-2020'

result = pd.concat([data,data2],axis=0)

sns.set(style='ticks', font_scale=1)
g = sns.scatterplot(data=result, x="Wlmax", y="Qmax", hue = 'type')
# g.plot_joint(sns.scatterplot,color="r")
# g.plot_marginals(sns.histplot, kde=True, color="r")
# g.plot_joint(sns.regplot,ci = None, color="r")
# g.ax_joint.text(600, 5.75, r'$\tau$'' = 0.30, p = 0.01', fontstyle='italic')
# g.ax_joint.set_xlabel('Qmax($m^3$/s)')
g.set(xlabel ='WLmax(m)',ylabel = '$Q_{cond}$WL($m^3$/s)')
g.legend(bbox_to_anchor=(1.02, 1),loc = 'upper left',title = 'Serie',borderaxespad=0)
g.set_title(name,fontsize=12)    

sns.despine()

# g.axvline(result.Wlmax.quantile(0.9),color = "r",linestyle='--') 
# g.axhline(result.Qmax.quantile(0.9),color = "r",linestyle='--') 

# g.axvline(result.Wlmax.quantile(0.5),color = "k",linestyle='--') 
# g.axhline(result.Qmax.quantile(0.5),color = "k",linestyle='--') 

plt.savefig(os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT3/'+name+'/QcondWL_scatter_2.png'),dpi=300,bbox_inches='tight') 

# %% plotting the Kendal comparison


pth = os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT3/Comp_tau_periods2.xlsx')
#pth = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT3/Nicolet/WLcondQ.csv'
data = pd.read_excel(pth, index_col = None)


# WLcondQ = data.loc[data['serie'] == 'WLcondQ']

# QcondWL = data.loc[data['serie'] == 'QcondWL']


# data = pd.concat([WLcondQ,QcondWL],axis=0)


    
g = sns.FacetGrid(data, col="serie", hue='period', margin_titles=True,sharex=False, sharey=False)
g.map(sns.barplot, 'outlet','tau', alpha=.7,ci=None)
g.add_legend()
plt.savefig(os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/5- Rapports/LOT3/scatterplot.png'),dpi=300,bbox_inches='tight')  




sns.set(style='ticks', font_scale=1)
g = sns.barplot(data=WLcondQ, x="outlet",y = 'tau',hue = 'period')
g.set(xlabel = 'Exutoire',ylabel = r'$\tau$')
sns.despine()
g.set_title('WLcondQ',fontsize=12) 
g.legend(bbox_to_anchor=(1.02, 1),loc = 'upper left',title = 'Serie',borderaxespad=0)   
plt.savefig(os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT3/WLcondQ_barplot_4.png'),dpi=300,bbox_inches='tight')  

# plot QcondWL

sns.set(style='ticks', font_scale=1)
g = sns.barplot(data=QcondWL, x="outlet",y = 'tau',hue = 'period')
g.set(xlabel = 'Exutoire',ylabel = r'$\tau$')
sns.despine()
g.set_title('QcondWL',fontsize=12)
g.legend(bbox_to_anchor=(1.02, 1),loc = 'upper left',title = 'Serie',borderaxespad=0)    
plt.savefig(os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT3/QcondWL_barplot_4.png'),dpi=300,bbox_inches='tight')  

# plot p-value

sns.set(style='ticks', font_scale=1)
g = sns.barplot(data=WLcondQ, x="outlet",y = 'p-value',hue = 'period')
g.set(xlabel = 'Exutoire',ylabel = 'p-value')
sns.despine()
g.set_title('WLcondQ',fontsize=12) 
g.legend(bbox_to_anchor=(1.02, 1),loc = 'upper left',title = 'Serie',borderaxespad=0)   
plt.savefig(os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT3/WLcondQ_pvalue_barplot_4.png'),dpi=300,bbox_inches='tight')  

# plot QcondWL

sns.set(style='ticks', font_scale=1)
g = sns.barplot(data=QcondWL, x="outlet",y = 'p-value',hue = 'period')
g.set(xlabel = 'Exutoire',ylabel = 'p-value')
sns.despine()
g.set_title('QcondWL',fontsize=12)
g.legend(bbox_to_anchor=(1.02, 1),loc = 'upper left',title = 'Serie',borderaxespad=0)    
plt.savefig(os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT3/QcondWL_pvalue_barplot_4.png'),dpi=300,bbox_inches='tight')  

# %% plotting the water level- river flow data


sns.set(style='ticks', font_scale=1)
g = sns.scatterplot(data=df_WLcondQ, x="Qmax", y="Wlmax")
g.set(xlabel ='Qmax($m^3$/s)',ylabel = '$WL_{cond}Q(m)$')
# g.legend(bbox_to_anchor=(1.02, 1),loc = 'upper left',title = 'Serie',borderaxespad=0)
g.set_title(name,fontsize=12)    
sns.despine()
plt.savefig(os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/4- Présentations/LOT3/WLcondQ_du_Loup.png'),dpi=300)  


# %% plotting histogram of annual maxima (for LOT3 outlets)

name = 'Petit_Cascapedia'

pth = os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT3/'+name+'/WLcondQ_1968_2020.csv')
#pth = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT3/Nicolet/WLcondQ.csv'
data = pd.read_csv(pth, index_col = None,parse_dates= {"date" : ["year","month","day"]})
data =  data.drop(['Date'], axis=1)
data = data.set_index('date')
data['variable'] = 'Qmax'


data.reset_index(inplace=True) 
data['year'] = pd.DatetimeIndex(data['date']).year
data['month'] = pd.DatetimeIndex(data['date']).month
data['day'] = pd.DatetimeIndex(data['date']).day

pth = os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT3/'+name+'/QcondWL_1968_2020.csv')
#pth = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT3/Nicolet/WLcondQ.csv'
data2 = pd.read_csv(pth, index_col = None,parse_dates= {"date" : ["year","month","day"]})
data2 =  data2.drop(['Date'], axis=1)
data2 = data2.set_index('date')
data2['variable'] = 'WLmax'


data2.reset_index(inplace=True) 
data2['year'] = pd.DatetimeIndex(data2['date']).year
data2['month'] = pd.DatetimeIndex(data2['date']).month
data2['day'] = pd.DatetimeIndex(data2['date']).day


result = pd.concat([data,data2],axis=0)

result['month_max_annual'] = pd.to_datetime(result['month'], format='%m').dt.month_name().str.slice(stop=3)


result.reset_index(inplace=True) 

sns.set(style='ticks', font_scale=1)
g = sns.histplot(data=result, x="month_max_annual", hue = 'variable', element="bars",multiple='dodge')
# g.set(xlabel ='Qmax($m^3$/s)',ylabel = '$WL_{cond}Q(m)$')
# g.legend(bbox_to_anchor=(1.02, 1),loc = 'upper left',title = 'Serie',borderaxespad=0)
g.set_title(name,fontsize=12)    
sns.despine()
plt.savefig(os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/4- Présentations/LOT3/Annual_maxima_Becancour.png'),dpi=300)  

# %% plotting histogram of annual maxima (CWRA presentations) (for LOT2 outlets)

name = 'au_Renard'

pth = os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT2/'+name+'/WLcondQ.csv')
#pth = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT3/Nicolet/WLcondQ.csv'
data = pd.read_csv(pth, index_col = None,parse_dates= {"date" : ["year","month","day"]})
data =  data.drop(['Date'], axis=1)
data = data.set_index('date')
data['variable'] = 'Qmax'


data.reset_index(inplace=True) 
data['year'] = pd.DatetimeIndex(data['date']).year
data['month'] = pd.DatetimeIndex(data['date']).month
data['day'] = pd.DatetimeIndex(data['date']).day

pth = os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT2/'+name+'/QcondWL.csv')
#pth = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT3/Nicolet/WLcondQ.csv'
data2 = pd.read_csv(pth, index_col = None,parse_dates= {"date" : ["year","month","day"]})
data2 =  data2.drop(['Date'], axis=1)
data2 = data2.set_index('date')
data2['variable'] = 'WLmax'


data2.reset_index(inplace=True) 
data2['year'] = pd.DatetimeIndex(data2['date']).year
data2['month'] = pd.DatetimeIndex(data2['date']).month
data2['day'] = pd.DatetimeIndex(data2['date']).day


result = pd.concat([data,data2],axis=0)

result['month_max_annual'] = pd.to_datetime(result['month'], format='%m').dt.month_name().str.slice(stop=3)


result.reset_index(inplace=True) 

sns.set(style='ticks', font_scale=1)
g = sns.histplot(data=result, x="month_max_annual", hue = 'variable', element="bars",multiple='dodge')
# g.set(xlabel ='Qmax($m^3$/s)',ylabel = '$WL_{cond}Q(m)$')
# g.legend(bbox_to_anchor=(1.02, 1),loc = 'upper left',title = 'Serie',borderaxespad=0)
g.set_title(name,fontsize=12)    
sns.despine()
plt.savefig(os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/5- Rapports/CWRA/Annual_maxima_Renard.png'),dpi=300)  


 # %% comparison of annual mean between Maskinonge historic and Maskinonge future
 


pth = os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/Denis_simulation_results/Maskinonge_normal.csv')
#pth = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT3/Nicolet/WLcondQ.csv'
data = pd.read_csv(pth, index_col = None,parse_dates= ["Date"])

data['year'] = pd.DatetimeIndex(data['Date']).year
data['month'] = pd.DatetimeIndex(data['Date']).month
data['day'] = pd.DatetimeIndex(data['Date']).day
 
hist =data.loc[data.groupby("year")["wl(m)"].idxmax()]
hist =data.groupby("year")["wl(m)"].mean()
hist = hist[:-1] 


pth = os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/Denis_simulation_results/Maskinonge_50cm.csv')
#pth = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT3/Nicolet/WLcondQ.csv'
data2 = pd.read_csv(pth, index_col = None,parse_dates= ["Date"])

data2['year'] = pd.DatetimeIndex(data2['Date']).year
data2['month'] = pd.DatetimeIndex(data2['Date']).month
data2['day'] = pd.DatetimeIndex(data2['Date']).day
 
future =data2.loc[data2.groupby("year")["wl(m)"].idxmax()]

future =data2.groupby("year")["wl(m)"].mean()

sns.set(style='ticks', font_scale=1)
sns.lineplot(data= hist, color = "blue",label='historic')
sns.lineplot(data= future, color ="red",label='future')
sns.despine()
plt.grid()
plt.savefig(os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/5- Rapports/CWRA/SLR_Matane.png'),dpi=300)  

# %% histogram of the water level time series associate with two periods

import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns
from scipy.stats import ks_2samp

name = 'Maskinonge'

pth = os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT3/'+name+'/WLcondQ_1968_1984.csv')
data = pd.read_csv(pth, index_col = None,parse_dates= {"date" : ["year","month","day"]})
data =  data.drop(['Date'], axis=1)
data = data.set_index('date')
data['type'] = '1968-1984'


pth2 = os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT3/'+name+'/WLcondQ_1985_2020.csv')
data2 = pd.read_csv(pth2, index_col = None,parse_dates= {"date" : ["year","month","day"]})
data2 =  data2.drop(['Date'], axis=1)
data2 = data2.set_index('date')

data2['type'] = '1985-2020'

# result = pd.concat([data,data2],axis=0)

# result.reset_index(inplace=True) 
sns.set(style='ticks', font_scale=1)
g = sns.histplot(data=data, x="Wlmax", color="skyblue", label="1968-1984", kde=True)
g = sns.histplot(data=data2, x="Wlmax", color="red", label="1985-2020", kde=True)
# g.set(xlabel ='Qmax($m^3$/s)',ylabel = '$WL_{cond}Q(m)$')
g.legend(loc = 'upper left')
g.set_title(name,fontsize=12)    
sns.despine()
plt.savefig(os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/5- Rapports/CWRA/Maskinonge_distribution.png'),dpi=300)  


ks_2samp(data['Wlmax'],data2['Wlmax'])




