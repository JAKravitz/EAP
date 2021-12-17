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

phytodata = pd.read_csv('/Users/jakravit/pyProjects/EAP/phyto_data.csv',
                        index_col=0)
outpath = '/Users/jakravit/pyProjects/EAP/optics.p'

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
    
    with open(outpath, 'rb') as fp:
        data = pickle.load(fp)
        
        data[k.PFT1][i] = {}
                               
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
            
            data[k.PFT1][i][rname] = []
            print (rname)
    
            # RUN EAP
            result = EAP(l, im, Deff, ncore, nshell, Vs, Veff, ci, psd)
            
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
            # result['Ci'] = Ci
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

