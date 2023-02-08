
"""
This script reads the station water level data (multiple csv files) and create a merged one single csv

Inputs:

1. rivers: The list of river outlets to be transformed to one single Netcdf file.
2. Period: historic or future
3. pthbase: path to the directory of the files
4. outfile: Path to write the output Netcdf file

Output:

Netcdf file containing the water level time series

"""

import pandas as pd
from glob import glob


def read_water_levels (path,station_id,start,end,outfile):
    files = sorted(glob(path+station_id +'-01-JAN-*_slev.csv'))
    wl = pd.concat((pd.read_csv(file, encoding="ISO-8859-1", skiprows=7, index_col=False)
                    for file in files))
    wl['Date'] = pd.to_datetime(wl["Obs_date"])
    wl['wl(m)'] = wl['SLEV(metres)']
    wl = wl.set_index('Date')
    wl = wl.drop(["Obs_date", 'SLEV(metres)'], axis=1)
    wl = wl.loc[start:end]
    wl.to_csv(outfile, mode='w', index=True)

if __name__ == "__main__":
    # %% Inputs
    path = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/Saint_Joseph_de_la_rive/'
    station_id = '3057'
    start = '1968-01-01'
    end = '2021-12-31'
    outfile = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/Saint_Joseph_de_la_rive/Saint_Joseph_de_la_rive.csv'
    read_water_levels(path,station_id,start,end,outfile)