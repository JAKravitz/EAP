#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 12 12:57:05 2022

@author: jakravit
"""
import pickle
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

outpath = '/Users/jakravit/git/EAP/optics_test.p'
l = np.arange(.4, .9025, .0025).astype(np.float32)

with open(outpath, 'rb') as fp:
    data = pickle.load(fp)

#%%

a = []
bb = []
deff = []
ncore = []
nshell = []
Vs = []
ci = []
psd = []

pav = data['Pavlova sp.']
# poly = data['C. polylepis']

for sim, sim_data in pav.items():
    if sim == 'time':
        continue
    a.append(sim_data['astar'])
    bb.append(sim_data['bbstar'])
    deff.append(sim_data['Deff'])
    ncore.append(sim_data['ncore'])
    nshell.append(sim_data['nshell'])
    Vs.append(sim_data['Vs'])
    ci.append(sim_data['ci'])
    psd.append(sim_data['psd'].max())
    dl = len(sim_data['Deff'])

a = pd.concat(a).reset_index(drop=True)
bb = pd.concat(bb).reset_index(drop=True)
deff = pd.Series(np.concatenate(deff)).reset_index(drop=True)
ncore = pd.Series(ncore).repeat(dl).reset_index(drop=True)
nshell = pd.Series(nshell).repeat(dl).reset_index(drop=True)
vs = pd.Series(Vs).repeat(dl).reset_index(drop=True)
ci = pd.Series(ci).repeat(dl).reset_index(drop=True)
psd = pd.Series(psd).repeat(dl).reset_index(drop=True)

cols = list(l) + ['deff','ncore','nshell','vs','ci','psd']
adf = pd.concat([a,deff,ncore,nshell,vs,ci,psd],axis=1)
bbdf = pd.concat([bb,deff,ncore,nshell,vs,ci,psd],axis=1)
adf.columns = cols
bbdf.columns = cols

#%%
# colors = {50: 'b', 101:'r'} # psd
colors = {2:'b', 3:'g', 5:'y', 7:'r', 9:'m', 12:'k'} # ci
# colors = {9:'b', 10:'r', 11:'k', 12:'g', 13:'y'} # deff
# colors = {1.02:'b', 1.04:'r'} # ncore
# colors = {1.08:'b', 1.12:'r', 1.16:'k', 1.2:'g'} # nshell
# colors = {.1:'b', .35:'r', .6:'g'} # Vs

fig, (ax1,ax2) = plt.subplots(1,2, figsize=(10,4))
agrp = adf.groupby('ci')
bgrp = bbdf.groupby('ci')
for i, k in agrp:
    print (i)
    k.iloc[:,:-6].T.plot(ax=ax1, color=colors[i], legend=False)
for i, k in bgrp:
    k.iloc[:,:-6].T.plot(ax=ax2, color=colors[i], legend=False)
