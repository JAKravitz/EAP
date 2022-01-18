#%%
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Working script

@author: jkravz311
"""
import numpy as np
import pandas as pd
import pickle
from EAP import EAP
import itertools

optics = {'Green_algae':{},
          'Cryptophytes':{},
          'Diatoms':{},
          'Dinoflagellates':{},
          'Heterokonts':{},
          'Haptophytes':{},
          'Cyano_blue':{},
          'Cyano_red':{},
          'Rhodophytes':{}}

phytodata = pd.read_csv('/Users/jakravit/git/EAP/phyto_data.csv',
                        index_col=0)
outpath = '/Users/jakravit/git/EAP_phyto_optics.p'

def pandafy (array, Deff):
    out = pd.DataFrame(array, index=Deff)
    return out


# define where to start in batch list
start = 0 # 0 to start from beginning, else phyto sp name
if start == 0:
    with open(outpath, 'wb') as fp:
        pickle.dump(optics, fp) 
else:
    phytodata = phytodata.loc[start:,:]

# loop through phyto batch list
for i,k in phytodata.iterrows():
    print (i)
       
    l = np.arange(.4, .9025, .0025).astype(np.float32) # wavelength range and resolution (changing this changes your interp value when normalising kshell)
    im = k.filter(regex='^[0-9]')
    meta = k.filter(regex='^[A-Za-z]+')
    Deff = np.arange(k.Dmin, k.Dmax, k.Dint)
    ncoreX = [1.04]
    nshellX = np.round(np.linspace(k.nshellmin, k.nshellmax,3),2)
    VsX = [.1, .35, .6]
    VeffX = [.6]
    ciX = [2,3,5,7,9,12]
    if k.Size_class == 'pico':
        psdX = [np.arange(.2, 10.2, .2)]
    else:
        psdX = [np.arange(1,102,2)] 
    
    with open(outpath, 'rb') as fp:
        data = pickle.load(fp)
        
        data[k.PFT1][i] = {}
                               
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
            
            data[k.PFT1][i][rname] = []
            print (rname)
    
            # RUN EAP
            result = EAP(l, im, Deff, ncore, nshell, Vs, Veff, ci*1e6, psd)
            
            # pandafy params so Deff is index
            for param in ['Qc','Sigma_c','cstar','Qb','Sigma_b','bstar','Qa',
                          'Sigma_a','astar','Qbb','Sigma_bb','bbstar']:
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
            
            data[k.PFT1][i][rname] = result
    
    with open(outpath, 'wb') as fp:
        pickle.dump(data,fp)

