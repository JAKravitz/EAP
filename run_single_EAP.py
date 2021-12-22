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
import itertools

#%
phytos = ['C. polylepis', 'Pavlova sp.', 'F. pinnata']
          # 'F. pinnata', 'T. rotula', 'H. triquetra',
          # 'K. rotundum', 'G. theta', 'R. lens', 'D. tertiolecta1', 'M. pusilla',
          # 'S. elongatus', 'A. marina']
phytodata = pd.read_csv('/Users/jakravit/pyProjects/EAP/phyto_data.csv',
                        index_col=0)
#rundata = phytodata.loc[phyto,:]

def pandafy (array, Deff):
    out = pd.DataFrame(array, index=Deff)
    return out

outpath = '/Users/jakravit/git/EAP/optics_test.p'

#%

l = np.arange(.4, .9025, .0025).astype(np.float32) # wavelength range and resolution (changing this changes your interp value when normalising kshell)
#l = np.arange(.4,.905,.005).astype(np.float32)

optics = {}
with open(outpath, 'wb') as fp:
    pickle.dump(optics, fp) 

for phyto in phytos:
    
    print (phyto)
    with open(outpath, 'rb') as fp:
        data = pickle.load(fp)
        data[phyto] = {}
    
        k = phytodata.loc[phyto,:]    
        im = k.filter(regex='^[0-9]')
        meta = k.filter(regex='^[A-Za-z]+')
        Deff = np.arange(k.Dmin, k.Dmax, k.Dint)
        ncoreX = np.linspace(k.ncoremin, k.ncoremax, 3)
        nshellX = np.round(np.linspace(k.nshellmin, k.nshellmax,4),2)
        VsX = np.round(np.linspace(k.Vsmin, k.Vsmax,4),2)
        VeffX = np.round(np.linspace(k.Veffmin, k.Veffmax, 3),2)
        # CiX = np.round(np.linspace(k.Cimin, k.Cimax,3),2)  
        ciX = np.round(np.linspace(k.cimin, k.cimin,3),2)
        if k.Size_class == 'pico':
            psdX = [np.arange(.2, 10.2, .2)]
        else:
            psdX = [np.arange(1,51,1), np.arange(1,102,2)] 
        
        for run in itertools.product(ncoreX, nshellX, VsX, VeffX, ciX, psdX):
            ncore = run[0]
            nshell = run[1]
            Vs = run[2]
            Veff = run[3]
            # Ci = run[4]
            ci = run[4]
            psd = run[5]
            
            rname = '{:.2f}_{:.2f}_{:.2f}_{:.2f}_{}_{}'.format(ncore,
                                                               nshell,
                                                               Vs,
                                                               Veff,                                                                  
                                                               ci,
                                                               max(psd))    
            
            # RUN EAP
            print (rname)
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
            
            data[phyto] = result
    
    with open(outpath, 'wb') as fp:
        pickle.dump(data,fp)

    
    
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



