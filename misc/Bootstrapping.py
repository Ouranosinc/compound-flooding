import pandas as pd
from sklearn.utils import resample
import numpy as np
import scipy.stats as st
from lmoments3 import distr,stats
import lmoments3 as lm

n_iterations = 10000
sample_size = len(Q_annual_max)
data_BS_Q = Q_annual_max[['50']].values
# dd = data_BS_Q.values
ns = len(data_BS_Q)
RP = []
for i in range(n_iterations):
    # b1 = np.floor(np.random.rand(sample_size)*len(dd)).astype(int)
    # sample = dd[b1]
    sample = resample(data_BS_Q, n_samples = ns, replace=True)
    ss = pd.DataFrame(sample,columns=['50'])
    paras_GUM_Q = distr.gum.lmom_fit(ss) # this will give the parameters of Gumbel distrinbution
    param_m_Q = {"loc": paras_GUM_Q['loc'],"scale": paras_GUM_Q['scale']}
    ddm = distr.gum(**param_m_Q)
    T = np.arange(1,350,1) +1
    gevRP_m = ddm.ppf(1.0-1./T)
    RP.append(gevRP_m)





