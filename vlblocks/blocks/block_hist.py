
import bkinit import bkinit
import bkfetch import bkfetch
import numpy as np


def block_hist(bk=''):
    if bk=='':
        bk = bkinit('hist', 'db', 'feat', 'dict')
        bk['fetch'] = fetch__
        bk['min_sigma'] = 0
        bk['max_num'] =   np.inf
        bk['ref_size'] =  []
        bk['rand_seed'] = []
        return bk

    bk, dirty = bkbegin(bk)
    if not dirty:
        print('block_hist not dirty')
        return bk
