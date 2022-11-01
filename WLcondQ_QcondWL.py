

import pandas as pd
import scipy.stats as stats
import datetime
from datetime import timedelta
import os
# %% Inputs:

# 1. Name of the river outlet for which we want to create the joint datasets.
# 2. Path to the daily flow data (excel file) provided by DEH and 
# 3. Path to the hourly water level data (MPO simulations)
# 4. Path to write the outputs

# Output:

# WLcondQ/QcondWL datasets in csv format

name = 'Richelieu'
serie = 'WLcondQ'
pth_riverflow_data = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/Workshop/MhAST_inputs/Extraction_Qjourn_Ouranos.xlsx' # This is daily data
pth_water_level_data = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/Workshop/MhAST_inputs/wl_data.csv' # This is hourly data
pth_output = os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/Workshop/MhAST_inputs/'+name) # This is daily data
# %% The main function

def CreateJointDataset(name,pth_riverflow_data,pth_water_level_data,pth_output,serie):
    # check to see if the directory for output exist, otherwise it creates
    isexist = os.path.exists(pth_output)
    if not isexist:
        os.makedirs(pth_output)
        print('a new directory with the name of river outlet is created!')
        
    data_Q = pd.read_excel(pth_riverflow_data, index_col = None)
    st = {'Yamaska':'MONT00003', 'Richelieu':'MONT00502', 'Saint_Jacques':'MONT01296', 'Saint_Regis':'MONT01317', 'Chateauguay':'MONT01335', 'Maskinonge':'SLNO00496', 'Assomption':'SLNO00563', 'du_Loup':'SLNO00847', 'Saint_Maurice':'SLNO00930',
      'Batiscan':'SLNO02927', 'Becancour':'SLSO00767', 'Nicolet':'SLSO00941', 'Saint_Francois':'SLSO01193',
      'A_Mars':'SAGU00175', 'Sainte_Anne':'SLNO03193', 'Jacques_Cartier':'SLNO00347', 'Etchemin':'SLSO02381',
      'Ristigouche':'GASP00913', 'Petit_Cascapedia':'GASP01528', 'York':'GASP02158', 'au_Renard':'GASP00038','Matane':'GASP02848', 'Mitis':'GASP03111', 'Outardes':'CNDA00096', 'Ha_Ha':'SAGU00151', 'Petit_Saguenay':'SAGU00012',
      'Gouffre':'SLNO00195', 'RivSud':'SLSO02566', 'Montmorency':'SLNO00294', 'Chaudiere':'SLSO00003','Saint_Charles':'SLNO00004',
      'Chicoutimi':'SAGU00288','Moulin':'SAGU00279', 'Saint_Jean':'SAGU00068'}  

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
   
    data_wl= pd.read_csv(pth_water_level_data, index_col = None)
    data_wl['Date'] = pd.to_datetime(data_wl['Date'])
    data_wl = data_wl.set_index('Date')
    data_wl = data_wl.loc['1968-01-01':'2020-12-31']  
    
    #data_wl = data_wl.loc['1985-01-01':'2020-12-31'] 
    #data_wl = data_wl.loc['1968-01-01':'1984-12-31']  
    
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
    
    if serie == 'WLcondQ':
    
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
                dll  = datetime.datetime(yl,ml,dl)
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
        
        
        # Write results to a csv file
        df_WLcondQ.to_csv(os.path.join(pth_output,'WLcondQ.csv'),mode='w',index=False)
        
        tau, p_value_K = stats.kendalltau(df_WLcondQ['Qmax'], df_WLcondQ['Wlmax'],nan_policy='omit')
        rho, p_value_Sp = stats.spearmanr(df_WLcondQ['Qmax'], df_WLcondQ['Wlmax'],nan_policy='omit')
        print('WLcondQ joint dataset dependence significance:')
        print('Kendalls tau = ', tau, 'P-value', p_value_K )
        print('Spearman rho = ', rho, 'P-value', p_value_Sp )
    else:
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
        df_QcondWL.to_csv(os.path.join(pth_output,'QcondWL.csv'),mode='w',index=False)
        
        # calculating correlation    
        
        tau, p_value_K = stats.kendalltau(df_QcondWL['Qmax'], df_QcondWL['Wlmax'],nan_policy='omit')
        rho, p_value_Sp = stats.spearmanr(df_QcondWL['Qmax'], df_QcondWL['Wlmax'],nan_policy='omit')
        print('QcondWL joint dataset dependence significance:')
        print('Kendalls tau = ', tau, 'P-value', p_value_K )
        print('Spearman rho = ', rho, 'P-value', p_value_Sp )

# %% Call this function now
CreateJointDataset(name,pth_riverflow_data,pth_water_level_data,pth_output,serie)



    
