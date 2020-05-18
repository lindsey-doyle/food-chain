#!/usr/bin/env python

import sys
import json
import shutil
import time
import pickle

sys.path.insert(0, 'src') # add library code to path

from get_data import etl
from model import driver 

DATA_PARAMS = 'config/data-params.json'
MODEL_PARAMS = 'config/model-params.json'
TEST_PARAMS = 'config/test-params.json'

ENV = 'config/env.json'


def load_params(fp):
    with open(fp) as fh:
        param = json.load(fh)

    return param

def main(targets):

    # to time the function
    start_time = time.time()

    # make the clean target
    if 'clean' in targets:
        shutil.rmtree('data/temp',ignore_errors=True)
        shutil.rmtree('data/out',ignore_errors=True)
        shutil.rmtree('data/raw',ignore_errors=True)

    # make the data target
    if 'data' in targets:
        cfg = load_params(DATA_PARAMS)
        etl(**cfg)
        # This line above replaces the two lines below once we edit 
        # the etl() method in get_data.py to output them to 'data/raw' directly 
        #  -  df, target = etl(**cfg)
        #  -  total = pd.concat([df, target])

    
    if 'model' in targets:
        cfg = load_params(MODEL_PARAMS)
        driver(**cfg)

    # make the test target
    if 'test-project' in targets:
        cfg = load_params(TEST_PARAMS)
        # run through project pipeline
        # using data stored in 'data_test'
    

    #env = load_params(ENV)

    print('Finished in: {} seconds'.format(time.time() - start_time))
    return


if __name__ == '__main__':
    targets = sys.argv[1:]
    main(targets)
