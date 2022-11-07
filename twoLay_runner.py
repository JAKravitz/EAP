#!/usr/bin/env python
# coding: utf-8
import numpy as np
import pandas as pd
from twoLay import twolay
import pickle
import random
import itertools
import time
import pickle
import sys
from scipy.interpolate import griddata

import sys
import time
import datetime
import logging
import argparse
import os

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
    l = np.arange(.4, .901, .001).astype(np.float32) 
    outPath = '/nobackup/jakravit/data/twoLay_batch_outputs/'
    nprimepath = 'stramski_2007_mineral_nprime.csv'
    nprime = pd.read_csv(nprimepath,index_col=0)
    
    optics = {}
    optics[p] = {}
    if p == 'DET':
        nrealX = [1.03, 1.05]
        jexpX = [3.4, 4, 4.6]
        dmaxX = [10.1, 50.1, 100.1]
        rhoX = [.3e6, .5e6, .7e6]  
        kcore = 0.010658 * np.exp(-0.007186* (l*1000)) #Stramski 2001 
        kcore = kcore.squeeze()
    else:    
        nrealX = [1.1, 1.4]
        jexpX = [3.4, 4, 4.6]
        dmaxX = [10.1, 50.1, 100.1]
        rhoX = [.75e6, 2e6, 4e6]
        kcore = nprime[p].values.copy()  
        im_wv = nprime.index.values / 1000
        last = kcore[-1:]
        kcore = griddata(im_wv, kcore, l, 'linear',fill_value=last)
        kcore = kcore.squeeze()  
            
    for run in itertools.product(nrealX, jexpX, dmaxX, rhoX):
        nreal = run[0]
        jexp = run[1]
        dmax = run[2]
        rho = run[3]
        rname = '{}_{:.2f}_{:.2f}_{:.2f}_{}'.format(p,
                                                    nreal,
                                                    jexp,
                                                    dmax,
                                                    rho)
   
        optics[p][rname] = []
            
        # RUN twoLay
        result = twolay(l, kcore, nreal, jexp, dmax, rho)
        
        # add run info to dataframe
        result['nreal'] = nreal
        result['jexp'] = jexp
        result['dmax'] = dmax
        result['rho'] = rho
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
    

    
    
