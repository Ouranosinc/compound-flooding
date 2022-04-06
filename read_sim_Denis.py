
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



df_Batiscan= pd.DataFrame(columns = ["tstep","wl(m)"])
df_Becancour= pd.DataFrame(columns = ["tstep","wl(m)"])
df_Nicolet = pd.DataFrame(columns = ["tstep","wl(m)"])
df_Yamaska = pd.DataFrame(columns = ["tstep","wl(m)"])
df_Saint_Mauricie = pd.DataFrame(columns = ["tstep","wl(m)"])
df_Saint_Francois = pd.DataFrame(columns = ["tstep","wl(m)"])
df_Richelieu= pd.DataFrame(columns = ["tstep","wl(m)"])
df_du_Loup= pd.DataFrame(columns = ["tstep","wl(m)"])
df_Maskinonge = pd.DataFrame(columns = ["tstep","wl(m)"])
df_Assomption= pd.DataFrame(columns = ["tstep","wl(m)"])



def datetime_range(start, end, delta):
    current = start
    while current < end:
        yield current
        current += delta

yr = np.linspace(1968,2020,53,dtype=int)
yrr = []
yrb = 2000
for i in range(len(yr)):
    if (yr[i]>= yrb and yr[i]>= 2010):
      yrr.append(str((yr[i]-yrb)))
    elif (yr[i]>= yrb and yr[i]< 2010):
      yrr.append('0' + str((yr[i]-yrb)))
    else:
      yrr.append(str((yr[i]-1900)))
      

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

        Batiscan_s = (tmp_df.loc[691,:])/1000. # Row 913 is the location of Chaudiere  a 15 min time
        Becancour_s = (tmp_df.loc[597,:])/1000. # Row 992 is the location of Mont-Morency create  a 15 min time
        Nicolet_s = (tmp_df.loc[520,:])/1000. # Row 964 is the location of Saint-Charles create  a 15 min time
        Yamaska_s = (tmp_df.loc[435,:])/1000. # Row 913 is the location of Chaudiere  a 15 min time
        Saint_Mauricie_s = (tmp_df.loc[567,:])/1000. # Row 1207 is the location of riviere Gouffre create  a 15 min time
        Saint_Francois_s = (tmp_df.loc[435,:])/1000. # Row 1143 is the location of riviere Sud create  a 15 min time
        Richelieu_s = (tmp_df.loc[359,:])/1000. # Row 1143 is the location of riviere Sud create  a 15 min time
        du_Loup_s = (tmp_df.loc[452,:])/1000. # Row 1143 is the location of riviere Sud create  a 15 min time
        Maskinoge_s = (tmp_df.loc[431,:])/1000. # Row 1143 is the location of riviere Sud create  a 15 min time
        Assomption_s = (tmp_df.loc[187,:])/1000. # Row 1143 is the location of riviere Sud create  a 15 min time
        
        df1 = Batiscan_s.to_frame()
        df1.columns = ['wl(m)']
        
        df2 = Becancour_s.to_frame()
        df2.columns = ['wl(m)']
        
        df3 = Nicolet_s.to_frame()
        df3.columns = ['wl(m)']
        
        df4 = Yamaska_s.to_frame()
        df4.columns = ['wl(m)']
        
        df5 = Saint_Mauricie_s.to_frame()
        df5.columns = ['wl(m)']
        
        df6= Saint_Francois_s.to_frame()
        df6.columns = ['wl(m)']
        
        df7 = Richelieu_s.to_frame()
        df7.columns = ['wl(m)']
        
        df8 = du_Loup_s.to_frame()
        df8.columns = ['wl(m)']
        
        df9 = Maskinoge_s.to_frame()
        df9.columns = ['wl(m)']
        
        df10 = Assomption_s.to_frame()
        df10.columns = ['wl(m)']
        
        
        df1['Date'] = dts
        df2['Date'] = dts
        df3['Date'] = dts
        df4['Date'] = dts
        df5['Date'] = dts
        df6['Date'] = dts
        df7['Date'] = dts
        df8['Date'] = dts
        df9['Date'] = dts
        df10['Date'] = dts
        
        
        
        tmp1 = pd.concat([df_Batiscan,df1])
        df_Batiscan = tmp1
        
        tmp2 = pd.concat([df_Becancour,df2])
        df_Becancour = tmp2
        
        tmp3 = pd.concat([df_Nicolet,df3])
        df_Nicolet = tmp3
        
        tmp4 = pd.concat([df_Yamaska,df4])
        df_Yamaska = tmp4
        
        tmp5 = pd.concat([df_Saint_Mauricie,df5])
        df_Saint_Mauricie = tmp5
        
        tmp6 = pd.concat([df_Saint_Francois,df6])
        df_Saint_Francois = tmp6
        
        tmp7 = pd.concat([df_Richelieu,df7])
        df_Richelieu = tmp7
        
        tmp8 = pd.concat([df_du_Loup,df8])
        df_du_Loup = tmp8
        
        tmp9 = pd.concat([df_Maskinonge,df9])
        df_Maskinonge = tmp9
        
        tmp10 = pd.concat([df_Assomption,df10])
        df_Assomption = tmp10
        

        del start,end,yy,mm,dd,tmp_df,Batiscan_s, Becancour_s, Nicolet_s, Yamaska_s, Saint_Mauricie_s, Saint_Francois_s, Richelieu_s, du_Loup_s, Maskinoge_s, Assomption_s, df1,df2,df3,df4,df5,df6,df7,df8,df9,df10,
        tmp1,tmp2,tmp3,tmp4,tmp5,tmp6,tmp7,tmp8,tmp9,tmp10

    i += 1


pth1  = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/Denis_simulation_results/Batiscan_normal.csv'
df_Batiscan.to_csv(pth1,mode='w',columns=["Date","wl(m)"],index=False)

pth2  = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/Denis_simulation_results/Becancour_normal.csv'
df_Becancour.to_csv(pth2,mode='w',columns=["Date","wl(m)"],index=False)

pth3  = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/Denis_simulation_results/Nicolet_normal.csv'
df_Nicolet.to_csv(pth3,mode='w',columns=["Date","wl(m)"],index=False)

pth4  = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/Denis_simulation_results/Yamaska_normal.csv'
df_Yamaska.to_csv(pth4,mode='w',columns=["Date","wl(m)"],index=False)

pth5  = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/Denis_simulation_results/Saint_Mauricie_normal.csv'
df_Saint_Mauricie.to_csv(pth5,mode='w',columns=["Date","wl(m)"],index=False)

pth6  = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/Denis_simulation_results/Saint_Francois_normal.csv'
df_Saint_Francois.to_csv(pth6,mode='w',columns=["Date","wl(m)"],index=False)

pth7  = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/Denis_simulation_results/Rechelieu_normal.csv'
df_Richelieu.to_csv(pth7,mode='w',columns=["Date","wl(m)"],index=False)

pth8  = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/Denis_simulation_results/du_Loup_normal.csv'
df_du_Loup.to_csv(pth8,mode='w',columns=["Date","wl(m)"],index=False)

pth9  = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/Denis_simulation_results/Maskinonge_normal.csv'
df_Maskinonge.to_csv(pth9,mode='w',columns=["Date","wl(m)"],index=False)

pth10  = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/Denis_simulation_results/Assomption_normal.csv'
df_Assomption.to_csv(pth10,mode='w',columns=["Date","wl(m)"],index=False)






