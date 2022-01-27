#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 11:57:11 2021

@author: jakravit
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from twolay_min import twolay_min
import pickle
import statsmodels.api as sm
import random
from scipy.interpolate import griddata

species = ['SAH1','OAH1']
nprimepath = '/Users/jakravit/Desktop/eap_truth_iop_data/stramski_2007_mineral_nprime.csv'
nprime = pd.read_csv(nprimepath,index_col=0)

# sample info

nreal = np.linspace(1.1, 1.6, 4)
jexp = [3.2, 4, 4.8]
dmax = [5, 10, 50, 100]
l = np.arange(.4, .9025, .0025).astype(np.float32)

# Run
minerals = {}
for sp in species:
    
    kcore = nprime[sp].values 
    im_wv = nprime.index.values / 1000
    last = kcore[-1:]
    kcore = griddata(im_wv, kcore, l, 'linear',fill_value=last)
    
    final = {}
    for n in nreal:
        for j in jexp:
            for d in dmax:
            
                # name
                rho = (n - 0.7717) / 0.1475e-6 # (wozniak & stramski, 2004)
                rname = '{}_{:.2f}_{:.2f}_{:.2f}_{}'.format(sp, n, rho, j, d)
                final[rname] = {}
                
                # EAP run
                print ('------ {} ------'.format(rname))
                result = twolay_min(l, kcore, n, rho, j, d)
                
                # dict for current run
                result['nreal'] = n
                result['j'] = j
                result['rho'] = rho
                result['dmax'] = d
            
                # add to final dict for mineral                
                final[rname] = result

    # add to total minerals dict
    minerals[sp] = final
                
    with open('/Users/jakravit/git/EAP_mineral_dataset/minerals3.p', 'wb') as fp:
        pickle.dump(minerals,fp)    


