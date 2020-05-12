#!/usr/bin/env python

import sys
import json
import shutil

sys.path.insert(0, 'src') # add library code to path

from get_data import get_listings, clean_listings
# from model import driver 
# etc.

GET_DATA_PARAMS = 'config/get-data-params.json'
# MODEL_PARAMS = 'config/model-params.json'
# etc.

def load_params(fp):
    with open(fp) as fh:
        param = json.load(fh)
    return param


def main(targets):

    if 'clean' in targets:
        shutil.rmtree('data/raw', ignore_errors=True)

    # data ingestion 
    if 'data' in targets:
        cfg = load_params(GET_DATA_PARAMS)
        get_listings(**cfg)

    #if 'model' in targets:
    #    cfg = load_params(MODEL_PARAMS)
    #    driver(**cfg)

    return

if __name__ == '__main__':
    targets = sys.argv[1:]
    main(targets)
    