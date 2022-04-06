# reading the observation data from Fichiers and Ocean Canada
import pandas as pd
import lmoments
file = r'C:\Users\mohbiz1\Desktop\Dossier_travail\705300_rehaussement_marin\3- Data\DFO-MPO\Saguenay_MFO.csv'

df = pd.read_csv(file,usecols=['date','Sea Level(m)'])

df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M') # the date column now is a dattime type

# in order to do time series analysis, we should have datetime index
df = df.set_index('date')

#find annual maximum for the time series and save it in a new dataframe
Max_annuel=df.resample('Y').max()  #finding annual maximums and save as a new dataframe
LMU = lmoments.samlmu(Max_annuel,5)  # calculating optimal parameter of a distribution using linear moments

gevfit = lmoments.pelgev(LMU)
T = 2
gevH = lmoments.quagev(1.0-1./T, gevfit)


Min_annuel=df.resample('Y').min()  #finding annual maximums and save as a new dataframe

Mean_annuel=df.resample('Y').mean()  #finding annual maximums and save as a new dataframe

wl = Max_annuel- Mean_annuel