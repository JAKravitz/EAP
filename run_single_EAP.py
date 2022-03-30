#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 12:29:45 2021

@author: jakravit
"""



## Client

if __name__ == '__main__':
    import numpy as np
    import pandas as pd
    from EAP import EAP
    import pickle
    import random
    import itertools
    import time
    #
    import dask
    import dask.dataframe as dd
    from dask.distributed import Client, LocalCluster, progress
    from dask.diagnostics import ProgressBar
    
    cluster = LocalCluster()
    client = Client(cluster)
    # client
    
    #%
    phytos =  ['C. polylepis']# , 'Pavlova sp.']
              # 'F. pinnata', 'T. rotula', 'H. triquetra',
              # 'K. rotundum', 'G. theta', 'R. lens', 'D. tertiolecta1', 'M. pusilla',
              # 'S. elongatus', 'A. marina']
    phytodata = pd.read_csv('/Users/jakravit/pyProjects/EAP/phyto_data.csv')
    
    def pandafy (array, Deff):
        out = pd.DataFrame(array, index=Deff)
        return out
    
    outpath = '/Users/jakravit/git/EAP/optics_test.p'
    
    parameters = ['Qc',
                  'Sigma_c',
                  'cstar',
                  'Qb',
                  'Sigma_b',
                  'bstar',
                  'Qa',
                  'Sigma_a',
                  'astar',
                  'Qbb',
                  'Sigma_bb',
                  'bbstar',
                  'Phy_C',
                  'Ci',
                  'psdvol']
    
    #%
    # wavelength range and resolution (changing this changes your interp value when normalising kshell)
    l = np.arange(.4, .9025, .0025).astype(np.float32) 
    
    # df_phytos = phytodata[(phytodata['Species'] == 'C. polylepis') | (phytodata['Species'] == 'Pavlova sp.')]
    df_phytos = phytodata[phytodata['Species'].isin(phytos)]
    
    # data = {}
    # for phyto in df_phytos['Species']:
    #     data[phyto] = {}
    
    # k = phytodata[phytodata['Species'] == 'Pavlova sp.']#.reset_index(inplace=True, drop=True)
    # k.reset_index(inplace=True, drop=True)
    
    # optics = {}
    # with open(outpath, 'wb') as fp:
    #     pickle.dump(optics, fp) 
    
    # loop through phyto list
    count = 0
    data = {}
    for phyto in df_phytos['Species']:
        
        start = time.time()
        print (phyto)
        # with open(outpath, 'rb') as fp:
        #     data = pickle.load(fp)
        # data[phyto] = {}
        
        #add phyto to dictionary
        data[phyto] = {}
        
        #load phyto data from dataframe
        k = phytodata[phytodata['Species'] == phyto].copy()   
        k.reset_index(inplace=True, drop=True)
        k = k.squeeze()
        im = k.filter(regex='^[0-9]')
        meta = k.filter(regex='^[A-Za-z]+')
        Deff = np.arange(k.Dmin,
                         k.Dmax,
                         k.Dint)
        ncoreX = [1.04]
        nshellX = np.round(np.linspace(k.nshellmin, 
                                       k.nshellmax, 2),2)
        # VsX = [.1, .35, .6]
        VsX = [.35]
        VeffX = [.6]
        # ciX = [2, 3, 5, 7, 9, 12]
        ciX = [3, 7]
        if k.Size_class == 'pico':
            psdX = [np.arange(.2, 10.2, .2)]
        else:
            psdX = [np.arange(1,102,2)]
    
        # k = phytodata.loc[phyto,:]    
        # im = k.filter(regex='^[0-9]').values
        # meta = k.filter(regex='^[A-Za-z]+')
        # Deff = np.arange(k.Dmin, k.Dmax, k.Dint)
        # ncoreX = [1.04]
        # nshellX = np.round(np.linspace(k.nshellmin, k.nshellmax,3),2)
        # VsX = [.1, .35, .6]
        # VeffX = [.6]
        # ciX = [2, 3, 5, 7, 9, 12]
        # if k.Size_class == 'pico':
        #     psdX = [np.arange(.2, 10.2, .2)]
        # else:
        #     psdX = [np.arange(1,102,2)] 
        # #iters = [item for item in itertools.product(ncoreX, nshellX, VsX, VeffX, ciX, psdX)]
    
        #create iterlist
        iterlist = []
        for it in itertools.product(ncoreX, nshellX, VsX, VeffX, ciX, psdX):
            run = {}
            run['ncore'] = it[0]
            run['nshell'] = it[1]
            run['Vs'] = it[2]
            run['Veff'] = it[3]
            run['ci'] = it[4]
            run['psd'] = it[5]
            iterlist.append(run)    
            
        #create dictionary entries
        for i in range(len(iterlist)):
            rname = '{:.2f}_{:.2f}_{:.2f}_{:.2f}_{}_{}'.format(iterlist[i]['ncore'],
                                                           iterlist[i]['nshell'],
                                                           iterlist[i]['Vs'],
                                                           iterlist[i]['Veff'],                                                                  
                                                           iterlist[i]['ci'],
                                                           max(iterlist[i]['psd']))   
            data[phyto][rname] = iterlist[i]    
    
        for rname in data[phyto].keys():
            # print(rname)
    
            # RUN EAP
            result = dask.delayed(EAP)(l, 
                                    im, 
                                    Deff, 
                                    data[phyto][rname]['ncore'], 
                                    data[phyto][rname]['nshell'], 
                                    data[phyto][rname]['Vs'], 
                                    data[phyto][rname]['Veff'], 
                                    data[phyto][rname]['ci']*1e6, 
                                    data[phyto][rname]['psd'])
            data[phyto][rname] = result
        data[phyto] = dask.compute(data[phyto])[0]
    
        # pandafy params so Deff is index
        for rname in data[phyto].keys():
            result = {}
            for param in parameters:
                if param in ['Phy_C','Ci','psdvol']:
                    result[param] = data[phyto][rname][param]
                else:
                    result[param] = pandafy(data[phyto][rname][param], Deff)
            
            # add run info to dataframe
            result['Deff'] = Deff
            result['ncore'] = iterlist[i]['ncore']
            result['nshell'] = iterlist[i]['nshell']
            result['Vs'] = iterlist[i]['nshell']
            result['Veff'] = iterlist[i]['Veff']
            result['ci'] = iterlist[i]['ci']
            result['psd'] = iterlist[i]['psd']
            result['class'] = meta.Class
            result['PFT1'] = meta.PFT1
            result['PFT2'] = meta.PFT2
            result['size_class'] = meta.Size_class
            result['lambda'] = l
    
            data[phyto][rname] = result
        
        #end timer
        end = time.time()
        tleng = end - start
        data[phyto]['time'] = tleng
    
    
    
    
    
        # for run in itertools.product(ncoreX, nshellX, VsX, VeffX, ciX, psdX):
        #     ncore = run[0]
        #     nshell = run[1]
        #     Vs = run[2]
        #     Veff = run[3]
        #     ci = run[4]
        #     psd = run[5]
            
        #     rname = '{:.2f}_{:.2f}_{:.2f}_{:.2f}_{}_{}'.format(ncore,
        #                                                        nshell,
        #                                                        Vs,
        #                                                        Veff,                                                                  
        #                                                        ci,
        #                                                        max(psd))    
        #     data[phyto][rname] = []
        #     print (rname)
            
        #     # RUN EAP
        #     result = EAP(l, im, Deff, ncore, nshell, Vs, Veff, ci*1e6, psd)
            
        #     # pandafy params so Deff is index
        #     for param in ['Qc','Sigma_c','cstar','Qb','Sigma_b','bstar','Qa','Sigma_a','astar','Qbb','Sigma_bb','bbstar',]:
        #         result[param] = pandafy(result[param], Deff)
            
        #     # add run info to dataframe
        #     result['Deff'] = Deff
        #     result['ncore'] = ncore
        #     result['nshell'] = nshell
        #     result['Vs'] = Vs
        #     result['Veff'] = Veff
        #     result['ci'] = ci
        #     result['psd'] = psd
        #     result['class'] = meta.Class
        #     result['PFT1'] = meta.PFT1
        #     result['PFT2'] = meta.PFT2
        #     result['size_class'] = meta.Size_class
        #     result['lambda'] = l
            
        #     data[phyto][rname] = result
        
        # end = time.time()
        # tleng = end - start
        # data[phyto]['time'] = tleng
        # with open(outpath, 'wb') as fp:
        #     pickle.dump(data,fp)

