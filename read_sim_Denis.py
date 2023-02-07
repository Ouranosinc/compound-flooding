
"""
This script is to read the water level simulations of DFO model (Denis Lefabvre et al., 2016)

inputs:

1. outlet: The name of the river outlet
2. Period: historic or future
3. pthbase: path to the directory of the files
4. outfile: Path to write the output Netcdf file

Output: The time series (in csv format)

"""

import pandas as pd
import numpy as np
import os
import bz2 # this is a library for reading the bz2 compressed files
from datetime import datetime,timedelta, date

def read_wl(pthbase,outlet,outfile,start,end):

    rivers = {'Batiscan':691,'Becancour':597,'Nicolet':520,'Yamaska':435,'Saint_Mauricie':567,'Saint_Francois':435,'Richelieu':359,'du_Loup':452,'Maskinonge':431,'Assomption':187,
              'Gouffre':1201,'du_Sud':1122,'Montmorency':1006,'Saint_Charles':962,'Chaudiere':912,'Etchemin':931,'Jacques_Cartier':819,'Sainte_Anne':700}

    files =[]
    df= pd.DataFrame(columns = ["wl(m)","outlet"])

    def datetime_range(start, end, delta):
        current = start
        while current < end:
            yield current
            current += delta

    yr = np.linspace(start,end,end-start,dtype=int)
    yrr = []
    yrb = 2000

    for i in range(len(yr)):
        if (yr[i]>= yrb and yr[i]>= 2010):
          yrr.append(str((yr[i]-yrb)))
        elif (yr[i]>= yrb and yr[i]< 2010):
          yrr.append('0' + str((yr[i]-yrb)))
        else:
          yrr.append(str((yr[i]-1900)))

    # i=0
    for i in range(len(yrr)):
    # while i < (len(yrr)): # loop through all years (1986 to 2020 = 53 years)
        yrrrr = yrr[i]
        files=[]
        print(i)
        for file in os.listdir(pthbase):
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
            begin = datetime(yyyy,mm,dd)
            stop = begin + timedelta(days=40)
            print("writing:",begin,"to", stop)
            dts = [dt.strftime('%Y-%m-%d %H:%M') for dt in
               datetime_range(begin, stop, timedelta(minutes=15))]

            fpth = os.path.join(pthbase,filename)
            dd = bz2.open(fpth,'rb')
            data = pd.read_csv(dd, encoding='utf-8', sep=';', header=None)

            grid = rivers[outlet]
            tmp = ((data.loc[grid,:])/1000.).to_frame()
            tmp.columns = ['wl(m)']
            tmp['outlet'] = outlet
            tmp['Date'] = dts
            df = pd.concat([df,tmp])
            del begin,stop,yy,mm,data,tmp,dd, dts
    df.to_csv(outfile,mode='w',columns=["Date","wl(m)"],index=False)


if __name__ == "__main__":
    # %% Inputs
    pthbase = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/DFO-MPO/plus50cm/'
    outlet = 'Batiscan'
    outfile = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/Denis_simulation_results/Bastiscan_50cm.csv'
    start = 1968
    end = 2020
    read_wl(pthbase,outlet,outfile,start,end)





