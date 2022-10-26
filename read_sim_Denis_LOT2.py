
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
dire = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/simulation_MPO/plus50cm'
files =[]



df_Gouffre= pd.DataFrame(columns = ["tstep","wl(m)"])
df_Sud= pd.DataFrame(columns = ["tstep","wl(m)"])
df_Mmorency = pd.DataFrame(columns = ["tstep","wl(m)"])
df_Saint_Charles = pd.DataFrame(columns = ["tstep","wl(m)"])
df_Chaudiere = pd.DataFrame(columns = ["tstep","wl(m)"])
df_Etchemin = pd.DataFrame(columns = ["tstep","wl(m)"])
df_Jacques_Cartier= pd.DataFrame(columns = ["tstep","wl(m)"])
df_Sainte_Anne= pd.DataFrame(columns = ["tstep","wl(m)"])




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

        Gouffre_s = (tmp_df.loc[1201,:])/1000. # Row 913 is the location of Chaudiere  a 15 min time
        Sud_s = (tmp_df.loc[1122,:])/1000. # Row 992 is the location of Mont-Morency create  a 15 min time
        Mmorency_s = (tmp_df.loc[1006,:])/1000. # Row 964 is the location of Saint-Charles create  a 15 min time
        Saint_Charles_s = (tmp_df.loc[962,:])/1000. # Row 913 is the location of Chaudiere  a 15 min time
        Chaudiere_s = (tmp_df.loc[912,:])/1000. # Row 1207 is the location of riviere Gouffre create  a 15 min time
        Etchemin_s = (tmp_df.loc[931,:])/1000. # Row 1207 is the location of riviere Gouffre create  a 15 min time
        Jacques_Cartier_s = (tmp_df.loc[819,:])/1000. # Row 1143 is the location of riviere Sud create  a 15 min time
        Sainte_Anne_s = (tmp_df.loc[700,:])/1000. # Row 1143 is the location of riviere Sud create  a 15 min time
        
        df1 = Gouffre_s.to_frame()
        df1.columns = ['wl(m)']
        
        df2 = Sud_s.to_frame()
        df2.columns = ['wl(m)']
               
        df3 = Mmorency_s.to_frame()
        df3.columns = ['wl(m)']
        
        df4 = Saint_Charles_s.to_frame()
        df4.columns = ['wl(m)']
        
        df5= Chaudiere_s.to_frame()
        df5.columns = ['wl(m)']
        
        df6 = Etchemin_s.to_frame()
        df6.columns = ['wl(m)']
        
        df7 = Jacques_Cartier_s.to_frame()
        df7.columns = ['wl(m)']
        
        df8 = Sainte_Anne_s.to_frame()
        df8.columns = ['wl(m)']
        
        
        
        df1['Date'] = dts
        df2['Date'] = dts
        df3['Date'] = dts
        df4['Date'] = dts
        df5['Date'] = dts
        df6['Date'] = dts
        df7['Date'] = dts
        df8['Date'] = dts
        
        
        
        tmp1 = pd.concat([df_Gouffre,df1])
        df_Gouffre = tmp1
        
        tmp2 = pd.concat([df_Sud,df2])
        df_Sud = tmp2
        
        tmp3 = pd.concat([df_Mmorency,df3])
        df_Mmorency = tmp3
        
        tmp4 = pd.concat([df_Saint_Charles,df4])
        df_Saint_Charles = tmp4
        
        tmp5 = pd.concat([df_Chaudiere,df5])
        df_Chaudiere = tmp5
        
        tmp6 = pd.concat([df_Etchemin,df6])
        df_Etchemin = tmp6
        
        tmp7 = pd.concat([df_Jacques_Cartier,df7])
        df_Jacques_Cartier = tmp7
        
        tmp8 = pd.concat([df_Sainte_Anne,df8])
        df_Sainte_Anne = tmp8
        
        
        

        del start,end,yy,mm,dd,tmp_df,Gouffre_s, Sud_s, Mmorency_s, Saint_Charles_s, Chaudiere_s, Etchemin_s, Jacques_Cartier_s, Sainte_Anne_s, df1,df2,df3,df4,df5,df6,df7,df8,
        tmp1,tmp2,tmp3,tmp4,tmp5,tmp6,tmp7,tmp8

    i += 1


# pth1  = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/Denis_simulation_results/Gouffre_normal.csv'
# df_Gouffre.to_csv(pth1,mode='w',columns=["Date","wl(m)"],index=False)

# pth2  = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/Denis_simulation_results/Sud_normal.csv'
# df_Sud.to_csv(pth2,mode='w',columns=["Date","wl(m)"],index=False)

# pth3  = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/Denis_simulation_results/Mmorency_normal.csv'
# df_Mmorency.to_csv(pth3,mode='w',columns=["Date","wl(m)"],index=False)

# pth4  = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/Denis_simulation_results/Saint_Charles_normal.csv'
# df_Saint_Charles.to_csv(pth4,mode='w',columns=["Date","wl(m)"],index=False)

# pth5  = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/Denis_simulation_results/Chaudiere_normal.csv'
# df_Chaudiere.to_csv(pth5,mode='w',columns=["Date","wl(m)"],index=False)

# pth6  = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/Denis_simulation_results/Etchemin_normal.csv'
# df_Etchemin.to_csv(pth6,mode='w',columns=["Date","wl(m)"],index=False)

# pth7  = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/Denis_simulation_results/Jacques_Cartier_normal.csv'
# df_Jacques_Cartier.to_csv(pth7,mode='w',columns=["Date","wl(m)"],index=False)

# pth8  = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/Denis_simulation_results/Sainte_Anne_normal.csv'
# df_Sainte_Anne.to_csv(pth8,mode='w',columns=["Date","wl(m)"],index=False)


pth1  = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/Denis_simulation_results/Gouffre_50cm.csv'
df_Gouffre.to_csv(pth1,mode='w',columns=["Date","wl(m)"],index=False)

pth2  = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/Denis_simulation_results/Sud_50cm.csv'
df_Sud.to_csv(pth2,mode='w',columns=["Date","wl(m)"],index=False)

pth3  = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/Denis_simulation_results/Mmorency_50cm.csv'
df_Mmorency.to_csv(pth3,mode='w',columns=["Date","wl(m)"],index=False)

pth4  = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/Denis_simulation_results/Saint_Charles_50cm.csv'
df_Saint_Charles.to_csv(pth4,mode='w',columns=["Date","wl(m)"],index=False)

pth5  = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/Denis_simulation_results/Chaudiere_50cm.csv'
df_Chaudiere.to_csv(pth5,mode='w',columns=["Date","wl(m)"],index=False)

pth6  = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/Denis_simulation_results/Etchemin_50cm.csv'
df_Etchemin.to_csv(pth6,mode='w',columns=["Date","wl(m)"],index=False)

pth7  = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/Denis_simulation_results/Jacques_Cartier_50cm.csv'
df_Jacques_Cartier.to_csv(pth7,mode='w',columns=["Date","wl(m)"],index=False)

pth8  = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/Denis_simulation_results/Sainte_Anne_50cm.csv'
df_Sainte_Anne.to_csv(pth8,mode='w',columns=["Date","wl(m)"],index=False)




