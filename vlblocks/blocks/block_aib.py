from bkinit import bkinit
from bkbegin import bkbegin
from bkend import bkend
from bkfetch import bkfetch

import vlfeat

from vlblocks.generics import glb
from vlblocks.generics.ensuredir import ensuredir

import numpy as np
import pdb

import cPickle as pickle
import os


def block_aib(bk=''):
    '''
    this block uses agglomerative information bottleneck as proposeed 
    in slonim et. al 2000
    '''
    if bk == '':
        bk = bkinit('aib', 'hist', 'db')
        bk['normalize_hists'] = 1
        bk['fetch'] = fetch__
        bk['rand_seed'] = []
        bk['seg_ids'] = []
        return bk

    bk, dirty = bkbegin(bk)
    if not dirty:
        print ("block_aib not dirty")
        return bk

    bkdb   = bkfetch(bk['db']['tag'])
    bkhist = bkfetch(bk['hist']['tag'])
    db       = bkfetch(bkdb, 'db')

    
    if len(bk['seg_ids']) > 0:
        sel_train = bk['seg_ids']
    else:
        sel_train = [n for n in range(len(db['segs'])) if db['segs'][n]['flag'] == db['TRAIN']]


    train_seg_ids = [db['segs'][n]['seg'] for n in sel_train]
    
    hist = bkfetch(bkhist, 'histogram', train_seg_ids[0])
    nclasses = len(db['cat_ids'])

    P = np.zeros([len(hist), nclasses])

    #pdb.set_trace()
    
    for t in range(len(train_seg_ids)):
        segid = train_seg_ids[t]
        class_ = [n for n in range(len(db['cat_ids']))  if db['segs'][sel_train[t]]['cat'] == db['cat_ids'][n]  ]
        hist     =  bkfetch(bkhist, 'histogram', segid)
        if bk['normalize_hists']:
            hist = hist/(hist+np.finfo(float).eps).sum()

        P[:, class_] = P[:, class_] + hist

    #pdb.set_trace()
    
    P = P.transpose()
    parents,cost = vlfeat.vl_aib(P)

    path_dir = os.path.join(glb.wrd['prefix'], bk['tag'])
    ensuredir(path_dir)
    
    path_parents = os.path.join(path_dir, 'data.plk')
    pickle.dump(parents, open(path_parents, 'wb'))
    path_P = os.path.join(path_dir, 'data.P.plk')
    pickle.dump(P, open(path_P, 'wb'))
    
    #pdb.set_trace()
    bk=bkend(bk)
    return bk



##############################################
def fetch__(bk, what, *varargin):
    if what.lower() == 'pcx':
        data= []
        return data
    elif what.lower() == 'tree':
        data=[]
        return data
    else:
        raise TypeError('block_aib.fetch__(): Unknow %s'%(what))
