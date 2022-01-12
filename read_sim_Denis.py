
"""
This script is written to read and analyse the simulation results of MPO model (Denis Lefabvre et al., 2016)
@author: Mohammad Bizhanimanzar mohbiz1@ouranos.ca

"""


import pandas as pd
import numpy as np
import os
import bz2 # this is a library for reading the bz2 compressed files
from datetime import datetime,timedelta, date

## section 1: select results for a specific year in the direcotry
dire = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/simulation_MPO/normal'
files =[]


df_Chaudiere = pd.DataFrame(columns = ["tstep","wl(m)"])
df_MntMorency = pd.DataFrame(columns = ["tstep","wl(m)"])
df_Saint_Charles = pd.DataFrame(columns = ["tstep","wl(m)"])
df_Gouffre = pd.DataFrame(columns = ["tstep","wl(m)"])
df_Riv_Sud = pd.DataFrame(columns = ["tstep","wl(m)"])



def datetime_range(start, end, delta):
    current = start
    while current < end:
        yield current
        current += delta

yr = np.linspace(1968,2019,52,dtype=int)
#yrr = np.zeros(shape=len(yr),dtype=int)
yrr = []
yrb = 2000
for i in range(len(yr)):
    if (yr[i]>= yrb and yr[i]>= 2010):
      yrr.append(str((yr[i]-yrb)))
    elif (yr[i]>= yrb and yr[i]< 2010):
      yrr.append('0' + str((yr[i]-yrb)))
    else:
      yrr.append(str((yr[i]-1900)))
      
      
#yrrr = yrr.astype(str)

i=0
while i < (len(yrr)): # loop through all years (1968 to 2019 = 52 years)
#    import pdb; pdb.set_trace()
    yrrrr = yrr[i]
    files=[]
    print(i)
    for file in os.listdir(dire):
            if file.startswith(yrrrr):
                files.append(file)
        # loop through files
     # sort the file based on dates   
    files.sort()
        
    for k in range(len(files)):    
        filename = files[k]
        date = filename.split(".")[0] # the first section of the file name has the date
        yy = int(str(date)[:2])
        if (yy>21):
            yyyy = 1900 + yy
        else:
            yyyy = 2000 + yy
        mm = int(str(date)[2:4])
        dd = int(str(date)[4:6])
        start = datetime(yyyy,mm,dd)
        end = start + timedelta(days=40)
        print("writing:",start,"to", end)
        dts = [dt.strftime('%Y-%m-%d %H:%M') for dt in 
           datetime_range(start, end, timedelta(minutes=15))]
    
        fpth = os.path.join(dire,filename)
        data = bz2.open(fpth,'rb')
        tmp_df = pd.read_csv(data, encoding='utf-8', sep=';', header=None)
        # SA_s = (tmp_df.loc[697,:])/1000. # Row 697 is the location of St-Anne create  a 15 min time 
        # JC_s = (tmp_df.loc[818,:])/1000. # Row 697 is the location of JC create  a 15 min time 
        # EC_s = (tmp_df.loc[931,:])/1000. # Row 697 is the location of EC create  a 15 min time 
        CH_s = (tmp_df.loc[913,:])/1000. # Row 913 is the location of Chaudiere  a 15 min time
        MM_s = (tmp_df.loc[992,:])/1000. # Row 992 is the location of Mont-Morency create  a 15 min time
        SC_s = (tmp_df.loc[964,:])/1000. # Row 964 is the location of Saint-Charles create  a 15 min time
        RG_s = (tmp_df.loc[1207,:])/1000. # Row 1207 is the location of riviere Gouffre create  a 15 min time
        RS_s = (tmp_df.loc[1143,:])/1000. # Row 1143 is the location of riviere Sud create  a 15 min time
        
        
        
        df_CH = CH_s.to_frame()
        df_CH.columns = ['wl(m)']
        
        df_MM = MM_s.to_frame()
        df_MM.columns = ['wl(m)']
        
        df_SC = SC_s.to_frame()
        df_SC.columns = ['wl(m)']
        
        df_RG = RG_s.to_frame()
        df_RG.columns = ['wl(m)']
        
        df_RS = RS_s.to_frame()
        df_RS.columns = ['wl(m)']
        
        
        df = pd.DataFrame({'Date':dts,
                       'wl(m)':df_CH['wl(m)']})
        df2 = pd.DataFrame({'Date':dts,
                       'wl(m)':df_MM['wl(m)']})
        df3 = pd.DataFrame({'Date':dts,
                       'wl(m)':df_SC['wl(m)']})
        df4 = pd.DataFrame({'Date':dts,
                       'wl(m)':df_RG['wl(m)']})
        df5 = pd.DataFrame({'Date':dts,
                       'wl(m)':df_RS['wl(m)']})
        
        
        tmp = pd.concat([df_Chaudiere,df])
        df_Chaudiere = tmp
        
        tmp2 = pd.concat([df_MntMorency,df2])
        df_MntMorency = tmp2
        
        tmp3 = pd.concat([df_Saint_Charles,df3])
        df_Saint_Charles = tmp3
        
        tmp4 = pd.concat([df_Gouffre,df3])
        df_Gouffre = tmp3
        
        tmp5 = pd.concat([df_Riv_Sud,df3])
        df_Riv_Sud = tmp3
        
        del start,end,yy,mm,dd,tmp_df,CH_s,MM_s,SC_s,RG_s,RS_s,tmp,tmp2,tmp3,tmp4,tmp5,dts,df_CH,df_MM,df_SC,df_RG,df_RS, df, df2, df3, df4, df5

    i += 1


pth3  = r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\Denis_simulation\Chaudiere_normal.csv'
df_Chaudiere.to_csv(pth3,mode='w',columns=["Date","wl(m)"])

pth3  = r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\Denis_simulation\MMorency_100cm.csv'
df_MntMorency.to_csv(pth3,mode='w',columns=["Date","wl(m)"])

pth3  = r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\Denis_simulation\SCharles_100cm.csv'
df_Saint_Charles.to_csv(pth3,mode='w',columns=["Date","wl(m)"])

pth3  = r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\Denis_simulation\riv_Gouffre_100cm.csv'
df_Gouffre.to_csv(pth3,mode='w',columns=["Date","wl(m)"])

pth3  = r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\Denis_simulation\riv_Sud_100cm.csv'
df_Riv_Sud.to_csv(pth3,mode='w',columns=["Date","wl(m)"])
