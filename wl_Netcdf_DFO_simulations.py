
"""
This script transforms the water level time series of DFO simulations from multiple csv files to one single Netcdf.

Inputs:

1. rivers: The list of river outlets to be transformed to one single Netcdf file.
2. Period: historic or future
3. pthbase: path to the directory of the files
4. outfile: Path to write the output Netcdf file

Output:

Netcdf file containing the water level time series

"""

import pandas as pd
import xarray as xr
import os

def Create_netcdf_wl(period,pthbase,rivers,outfile):
    if period == 'historic':

        # conversion for the historic period
        df = pd.DataFrame(columns=['time', 'river_name'])
        for count, r in enumerate(rivers):
            pth_wl = os.path.join(pthbase + r + '_normal.csv')
            data = pd.read_csv(pth_wl, index_col=None)
            data = data.rename(columns={'wl(m)': 'wl', 'Date': 'time'})
            data['river_name'] = r
            data['time'] = pd.to_datetime(data['time'])
            df = pd.concat([data, df], ignore_index=True)
            del data

        df = df.set_index(['time', 'river_name'])
        ds = df.to_xarray()  # this is the dataset
        ds['wl'].attrs = {'units': 'm', 'long_name': 'water_level'}
        ds.to_netcdf(outfile)
    else:
        # conversion for the future period
        # conversion for the historic period
        df = pd.DataFrame(columns=['time', 'river_name'])
        for count, r in enumerate(rivers):
            pth_wl = os.path.join(pthbase + r + '_50cm.csv')
            data = pd.read_csv(pth_wl, index_col=None)
            data = data.rename(columns={'wl(m)': 'wl', 'Date': 'time'})
            data['river_name'] = r
            data['time'] = pd.to_datetime(data['time'])
            df = pd.concat([data, df], ignore_index=True)
            del data

        df = df.set_index(['time', 'river_name'])
        ds = df.to_xarray()  # this is the dataset
        ds['wl'].attrs = {'units': 'm', 'long_name': 'water_level'}
        ds.to_netcdf(outfile)


if __name__ == "__main__":
    # %% Inputs
    rivers = ['Assomption', 'Batiscan', 'Becancour', 'Chaudiere', 'du_Loup', 'Etchemin', 'Gouffre', 'Jacques_Cartier',
              'Maskinonge','Mmorency', 'Nicolet', 'Richelieu', 'Saint_Charles', 'Saint_Francois', 'Saint_Mauricie', 'Sainte_Anne', 'du_Sud']
    period = ['historic', 'future']
    pthbase = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/Denis_simulation_results/'
    outfile = '/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/Denis_simulation_results/wl_historic.nc'

    Create_netcdf_wl('historic',pthbase,rivers,outfile)

