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
import time
import dask.dataframe as dd
import dask.array as da
import dask

#%
phytos =  ['C. polylepis', 'Pavlova sp.']
          # 'F. pinnata', 'T. rotula', 'H. triquetra',
          # 'K. rotundum', 'G. theta', 'R. lens', 'D. tertiolecta1', 'M. pusilla',
          # 'S. elongatus', 'A. marina']
phytodata = dd.read_csv('/Users/jakravit/pyProjects/EAP/phyto_data.csv')

@dask.delayed()
def pandafy (array, Deff):
    out = pd.DataFrame(array, index=Deff)
    return out

outpath = '/Users/jakravit/git/EAP/optics_test.p'

#%
# wavelength range and resolution (changing this changes your interp value when normalising kshell)
l = np.arange(.4, .9025, .0025).astype(np.float32) 

optics = {}
with open(outpath, 'wb') as fp:
    pickle.dump(optics, fp) 

# loop through phyto list
for phyto in phytos:
    
    start = time.time()
    print (phyto)
    with open(outpath, 'rb') as fp:
        data = pickle.load(fp)
    data[phyto] = {}

    k = phytodata.loc[phyto,:]    
    im = k.filter(regex='^[0-9]').values
    meta = k.filter(regex='^[A-Za-z]+')
    Deff = np.arange(k.Dmin, k.Dmax, k.Dint)
    ncoreX = [1.04]
    nshellX = np.round(np.linspace(k.nshellmin, k.nshellmax,3),2)
    VsX = [.1, .35, .6]
    VeffX = [.6]
    ciX = [2, 3, 5, 7, 9, 12]
    if k.Size_class == 'pico':
        psdX = [np.arange(.2, 10.2, .2)]
    else:
        psdX = [np.arange(1,102,2)] 
    #iters = [item for item in itertools.product(ncoreX, nshellX, VsX, VeffX, ciX, psdX)]
    
    for run in itertools.product(ncoreX, nshellX, VsX, VeffX, ciX, psdX):
        ncore = run[0]
        nshell = run[1]
        Vs = run[2]
        Veff = run[3]
        ci = run[4]
        psd = run[5]
        
        rname = '{:.2f}_{:.2f}_{:.2f}_{:.2f}_{}_{}'.format(ncore,
                                                           nshell,
                                                           Vs,
                                                           Veff,                                                                  
                                                           ci,
                                                           max(psd))    
        data[phyto][rname] = []
        print (rname)
        
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
        result['ci'] = ci
        result['psd'] = psd
        result['class'] = meta.Class
        result['PFT1'] = meta.PFT1
        result['PFT2'] = meta.PFT2
        result['size_class'] = meta.Size_class
        result['lambda'] = l
        
        data[phyto][rname] = result
    
    end = time.time()
    tleng = end - start
    data[phyto]['time'] = tleng
    with open(outpath, 'wb') as fp:
        pickle.dump(data,fp)

