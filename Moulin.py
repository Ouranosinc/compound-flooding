import matplotlib
# matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr
import numpy as np
from scipy import stats
import os


filename = "/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT3/Moulin2.csv"
df = pd.read_csv(filename)

df['nv_alfred'] = df['nv_alfred'] -2.656 # conversion vers CGVD28 for Port-Alfred https://tides.gc.ca/en/stations/03460
df['nv_chicout'] = df['nv_chicout'] -1.945 # conversion vers CGVD28 for Chicoutimi https://tides.gc.ca/en/stations/03480

# Pandas --> Xarray
q_CCC = xr.DataArray(df["CCC"], coords={"time": pd.to_datetime(df["dates_ccc"])}).dropna(dim="time")
q_CSH = xr.DataArray(df["CSH"], coords={"time": pd.to_datetime(df["dates_csh"])}).dropna(dim="time")
q_vannes = xr.DataArray(df["Vannes"], coords={"time": pd.to_datetime(df["dates_vannes"])}).dropna(dim="time")
# 13e starts in 2012, so we reindex
q_13e = xr.DataArray(df["13e"], coords={"time": pd.to_datetime(df["dates_13e"])}).dropna(dim="time").reindex_like(q_vannes, fill_value=0)

slev_alfred = xr.DataArray(df["nv_alfred"], coords={"time": pd.to_datetime(df["dates_alfred"])}).dropna(dim="time")
slev_tad = xr.DataArray(df["nv_tad"], coords={"time": pd.to_datetime(df["dates_tad"])}).dropna(dim="time")
slev_chicoutimi = xr.DataArray(df["nv_chicout"].dropna(), coords={"time": pd.to_datetime(df["dates_chicout"].dropna())})

# Prepare plots
fig = plt.subplots(3, 5, figsize=[18, 9])

q = [q_CCC, q_CSH, q_vannes, q_13e, q_CSH + q_vannes + q_13e]
labels = ["Chutes-a-Caron", "Shipshaw", "Vannes", "13e", "Somme"]
for i in range(5):
    ax = plt.subplot(3, 5, i+1)

    # Select Q
    q_tot = q[i]
    # Select only common time()
    slev_vs_rt = slev_chicoutimi.reindex_like(q_tot)

    # Plot
    plt.scatter(q_tot, slev_vs_rt,s = 3)

    plt.xlabel("Q (m³/s)")
    plt.ylabel("N (m)")
    plt.title(f"{labels[i]} @ 12h")

# Mean daily values
slev_chicoutimi_mean = slev_chicoutimi.resample({"time": "1D"}).mean()
for i in range(5):
    ax = plt.subplot(3, 5, i+6)

    # Select Q
    q_tot = q[i].resample({"time": "1D"}).mean()
    # Select only common time()
    slev_vs_rt_mean = slev_chicoutimi_mean.reindex_like(q_tot)

    # Plot
    plt.scatter(q_tot, slev_vs_rt_mean,s = 3)

    plt.xlabel("Q (m³/s)")
    plt.ylabel("N (m)")
    plt.title(f"{labels[i]} @ Mean Daily")

# Max daily values
slev_chicoutimi_max = slev_chicoutimi.resample({"time": "1D"}).max()
for i in range(5):
    ax = plt.subplot(3, 5, i+11)

    # Select Q
    q_tot = q[i].resample({"time": "1D"}).mean()
    # Select only common time()
    slev_vs_rt_max = slev_chicoutimi_max.reindex_like(q_tot)

    # Plot
    plt.scatter(q_tot, slev_vs_rt_max,s = 3)

    plt.xlabel("Q (m³/s)")
    plt.ylabel("N (m)")
    plt.title(f"{labels[i]} @ Max Daily")

plt.tight_layout()

plt.savefig('/home/mohammad/Dossier_travail/705300_rehaussement_marin/5- Rapports/LOT3/Moulin.png',dpi=300)  


# %% Prepare SLEV plots


q = [slev_alfred, slev_tad]
labels = ["Port Alfred", "Baie-Sainte-Catherine"]
# Max daily values
slev_chicoutimi_max = slev_chicoutimi.resample({"time": "1D"}).max()

slev_chicoutimi2 = slev_chicoutimi.resample({"time": "1D"}).max().rolling({"time": 3}).max()
fig = plt.subplots(1, 2, figsize=[10, 5])

ax = plt.subplot(1, 2, 1)

# Select Q
q_tot = q[0].resample({"time": "1D"}).max()
# Select only common time()
slev_vs_rt = slev_chicoutimi_max.reindex_like(q_tot)

# Plot
plt.scatter(q_tot, slev_vs_rt)

plt.xlabel(f"N @ {labels[0]} (m)")
plt.ylabel("N @ Chicoutimi (m)")
plt.title("max @ Daily")
plt.xlim([1,7])
plt.ylim([1,7])
plt.xticks(np.arange(1, 7, 1))
plt.yticks(np.arange(1, 7, 1))
ax.set_aspect('equal')
plt.grid()

xx = q_tot.values
yy = slev_vs_rt.values

idxx = np.isfinite(xx) & np.isfinite(yy)
fit = np.polyfit(xx[idxx],yy[idxx], 1)
fit_fn = np.poly1d(fit)
slope1, intercept1, r_value1, p_value, std_err = stats.linregress(xx[idxx], yy[idxx])

Alfred = q_tot.to_dataframe(name = 'slev')
chicout = slev_vs_rt.to_dataframe(name = 'slev')

Alfred.reset_index(inplace=True) 

recons = fit_fn(xx)

d = {'time': Alfred['time'],'slev_chicout':yy, 'slev_chicout_fitted':recons}
fit_Chicoutimi = pd.DataFrame(data = d)
fit_Chicoutimi['recons'] = fit_Chicoutimi['slev_chicout'].fillna(fit_Chicoutimi['slev_chicout_fitted'])
fit_Chicoutimi = fit_Chicoutimi.set_index('time')




ax.plot(xx, fit_fn(xx), 'r-', label='Linear fit')






ax = plt.subplot(1, 2, 2)

# Select Q
q_tot = q[0].resample({"time": "1D"}).max().rolling({"time": 3}).max()
# Select only common time()
slev_vs_rt = slev_chicoutimi2.reindex_like(q_tot)

# Plot
plt.scatter(q_tot, slev_vs_rt)

plt.xlim([1,7])
plt.ylim([1,7])
plt.xticks(np.arange(1, 7, 1))
plt.yticks(np.arange(1, 7, 1))
ax.set_aspect('equal')
plt.grid()

x = q_tot.values
y = slev_vs_rt.values

idx = np.isfinite(x) & np.isfinite(y)
fit = np.polyfit(x[idx],y[idx], 1)
fit_fn = np.poly1d(fit)
slope, intercept, r_value, p_value, std_err = stats.linregress(x[idx], y[idx])

ax.plot(x, fit_fn(x), 'r-', label='Linear fit')


plt.xlabel(f"N @ {labels[0]} (m)")
plt.ylabel("N @ Chicoutimi (m)")
plt.title("3-day rolling max @ Daily")
plt.tight_layout()
plt.savefig('/home/mohammad/Dossier_travail/705300_rehaussement_marin/5- Rapports/LOT3/Moulin2.png',dpi=300)  


# %% using the linear regression to reconstruct the missing water levels at Chicoutimi station

pth3 = os.path.join('/home/mohammad/Dossier_travail/705300_rehaussement_marin/3- Data/LOT3/Moulin/data_wl.csv')
fit_Chicoutimi['recons'].to_csv(pth3,mode='w',index=True)










