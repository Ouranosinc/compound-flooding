## Script for creating the Figure 6 of the report
## Author: Mohammad Bizhanimanzar
## This script creates the Figure 6 of the report. Time series of river flow, along with their annual maxima (red circles), 
## and conditioned maximum river flow (QcondWL) are show in this Figure.

import pandas as pd
import matplotlib.pyplot as plt
import os
# %% Section 1: reading the river flow

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

# %% To plot river flow with annual maxima (Figure 5 report LOT2)

Q_annual_max =  Q_annual_max.drop(['year', 'month','day','index'], axis=1)
Q_annual_max = Q_annual_max.set_index('date')
Q_annual_max = Q_annual_max.squeeze()

Q_plt =  Q.drop(['year', 'month','day'], axis=1)
Q_plt = Q_plt.set_index('date')
Q_plt_s = Q_plt.squeeze()

pth2 = os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT2/'+name+'/QcondWL.csv')
Qcond = pd.read_csv(pth2, index_col = None,parse_dates= {"date" : ["year","month","day"]})
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
plt.title(name, fontsize=10)
ax.set_ylim(0,max(Q_plt_s)+20)
plt.ylabel('Débit ($m^3$/s)')
plt.savefig('/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT2/Qmax_annual_Petit_Cascapedia.png')



