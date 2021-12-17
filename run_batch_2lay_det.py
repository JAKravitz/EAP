#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 11:57:11 2021

@author: jakravit
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from twolay_det import twolay_det
import pickle
import statsmodels.api as sm
import random
from scipy.interpolate import griddata


# sample info
#rho = np.random.uniform(.2e6, .5e6, 3)
rho = [.2e6, .35e6, .5e6]
#nreal = np.random.uniform(1.03, 1.05, 3)
nreal = [1.03, 1.04, 1.05]
#jexp = np.random.uniform(3.4, 4.6, 3)
jexp = [3.6, 4, 4.4]
dmax = [10.1, 50.1, 100.1]
l = np.arange(.4, .9025, .0025).astype(np.float32)
kcore = 0.010658 * np.exp(-0.007186* (l*1000)) #Stramski 2001 

final = {}
for n in nreal:
    for j in jexp:
        for r in rho:
            for d in dmax:
        
                # name
                #rho = (n - 0.7717) / 0.1475e-6 # (wozniak & stramski, 2004 > more for min)
                rname = '{:.2f}_{:.2f}_{:.2f}_{}'.format(n, r, j, d)
                final[rname] = {}
                
                # EAP run
                print ('------ {} ------'.format(rname))
                result = twolay_det(l, kcore, n, r, j, d)
                
                # add additional run info
                result['nreal'] = n
                result['rho'] = r
                result['j'] = j
                result['dmax'] = d
                
                # add run to final dict
                final[rname] = result
                
            
with open('/Users/jakravit/pyProjects/EAP/build/det.p', 'wb') as fp:
    pickle.dump(final,fp)    


