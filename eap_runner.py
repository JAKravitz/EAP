#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 12:29:45 2021

@author: jakravit
"""
import sys
import time
import datetime
import logging
import argparse
import os

import numpy as np
import pandas as pd
from EAP import EAP
import pickle
import random
import itertools
import time

def main():
    """The main driver routine."""
    parser = argparse.ArgumentParser(usage="%(prog)s [options]", \
                                description='runs a single task group')
    parser.add_argument("--log", type=str, help="A logfile, full path.", default=None)
    parser.add_argument("work", type=str, help="The work set, i.e. file1, file2", nargs=1)
    args = parser.parse_args()

    logging.basicConfig(filename=args.log, level=logging.DEBUG)

    fls_log_msg = " ".join([args.work[0]])
    t_start = datetime.datetime.now()
    logging.info("workset \"%s\", start %s", fls_log_msg, t_start.strftime("%Y%j%H.%M.%S") )
    
    ##########
    
    p = args.work[0]
    logging.debug("running %s  ...", p)
    
    phytodata = pd.read_csv('phyto_data_v1101.csv',index_col=0)
    outPath = '/nobackup/jakravit/data/EAP_batch_outputs/'
    l = np.arange(.4, .901, .001).astype(np.float32) 
    
    def pandafy (array, Deff):
        out = pd.DataFrame(array, index=Deff)
        return out
    
    optics = {}
    optics[p] = {}
    k = phytodata.loc[p,:]    
    im = k.filter(regex='^[0-9]')
    meta = k.filter(regex='^[A-Za-z]+')
    Deff = np.arange(k.Dmin, k.Dmax, k.Dint)
    ncoreX = [1.04]
    nshellX = np.round(np.linspace(k.nshellmin, k.nshellmax,3),2)
    VsX = [.2, .5]
    VeffX = [.6]
    ciX = [2, 3, 5, 7, 9, 12]
    if k.Size_class == 'pico':
        psdX = [np.arange(.2, 10.2, .2)]
    else:
        psdX = [np.arange(1,102,2)] 
    
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
        optics[p][rname] = []
            
        # RUN EAP
        result = EAP(l, im, Deff, ncore, nshell, Vs, Veff, ci*1e6, psd)
            
        # pandafy params so Deff is index
        for param in ['Qc','Sigma_c','cstar','Qb','Sigma_b','bstar','Qa','Sigma_a','astar','Qbb','Sigma_bb','bbstar',]:
            result[param] = pandafy(result[param], Deff)
            
        # add run info to dataframe
        result['Deff'] = Deff
        result['ncore'] = ncore
        result['nshell'] = nshell
        result['Vs'] = Vs
        result['Veff'] = Veff
        result['ci'] = ci
        result['psd'] = psd
        result['PFT1'] = meta.PFT1
        result['PFT2'] = meta.PFT2
        result['PFT3'] = meta.PFT3
        result['lambda'] = l
            
        optics[p][rname] = result
        out = outPath + p + '.p'
        with open(out, 'wb') as f:
            pickle.dump(optics,f)

    # cleanup
    time.sleep(2)
    logging.info("performing post file cleanup...")
    
    # report on exec time
    t_delt = datetime.datetime.now() - t_start
    logging.info("runtime \"%0.1f\" minutes, seconds %d", float(t_delt.seconds)/60.0, t_delt.seconds) 
                   
    return 0

if __name__ == '__main__':
    sys.exit(main())