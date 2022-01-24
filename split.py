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

with open('/Users/jakravit/git/EAP_phyto_optics7.p', 'rb') as fp:
    data7 = pickle.load(fp)

with open('/Users/jakravit/git/EAP_phyto_optics8.p', 'rb') as fp:
    data8 = pickle.load(fp)

#%%
def keys(d):
    sp = []
    for i,k in d.items():
        print (i)
        for ii,kk in k.items():
            print (ii)
            sp.append(ii)
    return sp

#%%

data0 = {'Green_algae': {},
         'Cryptophytes': {},
         'Diatoms': {},
         'Dinoflagellates': {},
         'Heterokonts': {},
         'Haptophytes': {},
         'Cyano_blue': {},
         'Cyano_red': {},
         'Rhodophytes': {}
         }

classes = ['Green_algae', 'Cryptophytes', 'Diatoms', 'Dinoflagellates',
            'Heterokonts', 'Haptophytes', 'Cyano_blue', 'Cyano_red', 'Rhodophytes']

# for cl in classes:
    
#     with open('/Users/jakravit/EAP_phytoplankton_dataset/{}.p'.format(cl), 'rb') as fp:
#         pickle.dump(data0[cl], fp)

dlist = [data1, data2, data3, data4, data5, data6, data7, data8]

for data in dlist:
    for cl in classes:
        data0[cl].update(data[cl])

sp = keys(data0)
print('\n')
print (len(sp))

#%%
# with open('/Users/jakravit/git/EAP_phyto_optics_final.p', 'wb') as fp:
#     pickle.dump(data0,fp)

for cl in classes:
    
    # with open('/Users/jakravit/EAP_phytoplankton_dataset/{}.p'.format(cl), 'wb') as fp:
    #     pickle.dump(data0[cl], fp)
    
    with open('/Users/jakravit/EAP_phytoplankton_dataset/{}.p'.format(cl), 'wb') as fp:
        pickle.dump(data0[cl], fp)


#%%
# import pandas as pd
# pdata = pd.read_csv('/Users/jakravit/git/EAP/phyto_data.csv')
# sp2 = list(pdata.Species.values)

# s = set(sp) - set(sp2)
#%%





