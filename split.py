#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 15:43:31 2022

@author: jakravit
"""
#%%
import pickle 
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

with open('/Users/jakravit/git/EAP_phyto_optics6.p', 'rb') as fp:
    data6 = pickle.load(fp)

#%%
def keys(d):
    for i,k in d.items():
        print (i)
        for ii,kk in k.items():
            print (ii)

keys(data1)
print('\n')
keys(data2)

data1['Diatoms'].update(data2['Diatoms'])

keys(data1)

#%%
classes = ['Green_algae', 'Cryptophytes', 'Diatoms', 'Dinoflagellates',
           'Heterokonts', 'Haptophytes', 'Cyano_blue', 'Cyano_red', 'Rhodophytes']
dlist = [data2, data3, data4, data5, data6]

for data in dlist:
    for cl in classes:
        data1[cl].update(data[cl])

#%%
with open('/Users/jakravit/git/EAP_phyto_optics.p', 'wb') as fp:
    pickle.dump(data1,fp)

#%%
with open('/Users/jakravit/git/EAP_phyto_optics.p', 'rb') as fp:
    data = pickle.load(fp)
    
    
keys(data)
