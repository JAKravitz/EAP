#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 15:43:31 2022

@author: jakravit
"""
#%%
import pickle 
with open('/Users/jakravit/git/EAP_phyto_optics.p', 'rb') as fp:
    data0 = pickle.load(fp)

with open('/Users/jakravit/git/EAP_phyto_optics1.p', 'rb') as fp:
    data1 = pickle.load(fp)

with open('/Users/jakravit/git/EAP_phyto_optics2.p', 'rb') as fp:
    data2 = pickle.load(fp)

with open('/Users/jakravit/git/EAP_phyto_optics3.p', 'rb') as fp:
    data3 = pickle.load(fp)

with open('/Users/jakravit/git/EAP_phyto_optics4.p', 'rb') as fp:
    data4 = pickle.load(fp)

with open('/Users/jakravit/git/EAP_phyto_optics5.p', 'rb') as fp:
    data5 = pickle.load(fp)

#%%
def keys(d):
    sp = []
    for i,k in d.items():
        print (i)
        for ii,kk in k.items():
            print (ii)
            sp.append(ii)
    return sp

sp = keys(data0)
print('\n')
print (len(sp))
# keys(data4)

# data1['Diatoms'].update(data2['Diatoms'])

# keys(data1)

#%%
classes = ['Green_algae', 'Cryptophytes', 'Diatoms', 'Dinoflagellates',
           'Heterokonts', 'Haptophytes', 'Cyano_blue', 'Cyano_red', 'Rhodophytes']
dlist = [data1, data2, data3, data4, data5]

for data in dlist:
    for cl in classes:
        data0[cl].update(data[cl])

#%%
import pandas as pd
pdata = pd.read_csv('/Users/jakravit/git/EAP/phyto_data.csv')
sp2 = list(pdata.Species.values)

s = set(sp) - set(sp2)
#%%
with open('/Users/jakravit/git/EAP_phyto_optics.p', 'wb') as fp:
    pickle.dump(data0,fp)

#%%
import json
with open('/Users/jakravit/Desktop/data1.json','w') as f:
    json.dump(data1,f)





