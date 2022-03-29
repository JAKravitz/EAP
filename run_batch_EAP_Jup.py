#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 17:39:47 2022

@author: jakravit
"""
#%%
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

phytodata = pd.read_csv('/Users/jakravit/git/EAP/phyto_data.csv',
                        index_col=0)
outpath = '/Users/jakravit/git/EAP_phyto_optics.p'
l = np.arange(.4, .9025, .0025).astype(np.float32) 

def pandafy (array, Deff):
    out = pd.DataFrame(array, index=Deff)
    return out

data = {'Green_algae':{},
          'Cryptophytes':{},
          'Diatoms':{},
          'Dinoflagellates':{},
          'Heterokonts':{},
          'Haptophytes':{},
          'Cyano_blue':{},
          'Cyano_red':{},
          'Rhodophytes':{}}

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
              'bbstar',]

# loop through phyto list
count = 0
data = {}
for phyto in phytodata['Species']:
    
    start = time.time()
    print (phyto)
    
    #load phyto data from dataframe
    k = phytodata[phytodata['Species'] == phyto].copy()   
    k.reset_index(inplace=True, drop=True)
    k = k.squeeze()
    pft = k.PFT1
    im = k.filter(regex='^[0-9]')
    meta = k.filter(regex='^[A-Za-z]+')
    Deff = np.arange(k.Dmin,
                     k.Dmax,
                     k.Dint)
    ncoreX = [1.04]
    nshellX = np.round(np.linspace(k.nshellmin, 
                                   k.nshellmax, 3),2)
    VsX = [.1, .35, .6]
    VeffX = [.2, .6]
    ciX = [2, 3, 5, 7, 9, 12]
    if k.Size_class == 'pico':
        psdX = [np.arange(.2, 10.2, .2)]
    else:
        psdX = [np.arange(1,102,2)]    
    
    #add phyto to dictionary
    data[pft][phyto] = {} 
    
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
        data[pft][phyto][rname] = iterlist[i]    

    for rname in data[pft][phyto].keys():
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
        data[pft][phyto][rname] = result
    data[pft][phyto] = dask.compute(data[pft][phyto])[0]
    
    
    # pandafy params so Deff is index
    for rname in data[pft][phyto].keys():
        result = {}
        for param in parameters:
            result[param] = pandafy(data[pft][phyto][rname][param], Deff)
        
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
        # result['lambda'] = l

        data[pft][phyto][rname] = result
    
    #end timer
    end = time.time()
    tleng = end - start
    data[pft][phyto]['time'] = tleng
    
    
    