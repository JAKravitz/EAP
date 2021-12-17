#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 12:29:45 2021

@author: jakravit
"""
import numpy as np
import pandas as pd
from EAP import EAP
import pickle
import random

#%
#phytos = ['C. polylepis']
phytos = ['C. polylepis', 'Pavlova sp.', 'F. pinnata', 'T. rotula', 'H. triquetra',
          'K. rotundum', 'G. theta', 'R. lens', 'D. tertiolecta1', 'M. pusilla',
          'S. elongatus', 'A. marina']
phytodata = pd.read_csv('/Users/jakravit/pyProjects/EAP/phyto_data.csv',
                        index_col=0)
#rundata = phytodata.loc[phyto,:]

def pandafy (array, Deff):
    out = pd.DataFrame(array, index=Deff)
    return out

outpath = '/Users/jakravit/pyProjects/EAP/test/'

#%

l = np.arange(.4, .9025, .0025).astype(np.float32) # wavelength range and resolution (changing this changes your interp value when normalising kshell)
#l = np.arange(.4,.905,.005).astype(np.float32)

for phyto in phytos:
    
    print (phyto)
    rundata = phytodata.loc[phyto,:]    
    
    im = rundata.filter(regex='^[0-9]')
    meta = rundata.filter(regex='^[A-Za-z]+')
    Deff = np.arange(rundata.Dmin, rundata.Dmax, rundata.Dint)
    ncore = np.random.uniform(rundata.ncoremin, rundata.ncoremax, 1)
    nshell = np.random.uniform(rundata.nshellmin, rundata.nshellmax, 1)
    Vs = np.random.uniform(rundata.Vsmin, rundata.Vsmax, 1)
    Veff = np.random.uniform(rundata.Veffmin, rundata.Veffmax, 1)
    # Ci = np.random.uniform(rundata.Cimin, rundata.Cimax, 1)
    ci = np.random.uniform(rundata.cimin, rundata.cimax, 1)
    if rundata.Size_class == 'pico':
        psd = np.arange(.1, 10, .2)
    else:
        k = random.randint(0, 1)
        if k == 0:
            psd = np.arange(1,51,1) 
        else: 
            psd = np.arange(1,102,2)
    
    # RUN EAP
    result = EAP(l, im, Deff, ncore, nshell, Vs, Veff, ci*1e6, psd)
    
    # pandafy params so Deff is index
    for param in ['Qc','Sigma_c','cstar','Qb','Sigma_b','bstar','Qa','Sigma_a','astar','Qbb','Sigma_bb','bbstar',]:
        result[param] = pandafy(result[param], Deff)
    
    # add run info to dataframe
    result['Deff'] = Deff
    result['ncore'] = ncore
    result['nshell'] = nshell
    result['Vs'] = Vs
    result['Veff'] = Veff
    # result['Ci'] = Ci
    result['ci'] = ci
    result['psd'] = psd
    result['class'] = meta.Class
    result['PFT1'] = meta.PFT1
    result['PFT2'] = meta.PFT2
    result['size_class'] = meta.Size_class
    result['lambda'] = l
    
    with open(outpath+phyto, 'wb') as fp:
        pickle.dump(result,fp)

    
    
#%%
# import matplotlib.pyplot as plt
# from scipy.signal import savgol_filter

# with open(outpath+phyto, 'rb') as fp:
#     foo = pickle.load(fp)
    
# plt.figure(0)
# a = foo['a']
# plt.plot(l,a.T)
# plt.figure(1)
# bb = foo['bb']
# plt.plot(l,bb.T)
# plt.figure(2)
# b = foo['b']
# plt.plot(l,b.T)



