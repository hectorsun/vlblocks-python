 
from vlblocks.generics import glb
from bkinit            import bkinit
from bkfetch           import bkfetch
from bkbegin           import bkbegin
from bkend             import bkend


import numpy as np
import vlfeat

import pdb

import os
import cPickle as pickle


def block_dictionary(bk = '', *varargin):
    '''
    block_dictionary(bk) construct a dictionary
    This block learn a dictionary form a database and a set of 
    feature
    options :
    bk['ikm_nwrods']: 
    bk['hikm_K']: 

    bk['push']: func PUSH(DICT, DATA)
                pushes the data through the dictionary
    '''
    if bk=='':
        bk = bkinit('dictionary','db','feat')
        bk['fetch']            = fetch__
        bk['push']             = [] 

        bk['dictionary']       = 'ikm'
        bk['nfeats']           = 1000
        bk['rand_seed']        = []
        bk['ntrials']          = 1
        bk['split']            = 0

        bk['seg_ids']          = []
        
        bk['ikm_nwords']       = 100
        bk['ikm_at_once']      = 0
        bk['hikm_K']           = 10
        bk['hikm_nleaves']     = 100
        bk['hikm_only_leaves'] = 0
        return bk

    if bk['dictionary'] == 'hikm':
        bk['push'] = hikm_push__
    else:
        bk['push'] = ikm_push__

    #############################################
    # check load inputs
    bk, dirty = bkbegin(bk)
    if not dirty:
        print('block_dictionary not dirty')
        return bk


    print bk

    #pdb.set_trace()
    db_cfg = bkfetch(bk['db']['tag'])
    db = bkfetch(bk['db']['tag'], 'db')

    #pdb.set_trace()
    
    #############################################
    # Do computation
    for t in range(bk['ntrials']):
        #if len(bk['rand_seed']) == 0:
        #    pass
        #setrandseeds(bk['rand_seed']+t)
        dict_=[]

        if bk['dictionary'] == 'ikm' and bk['ikm_at_once']!=True:
            #learn one dict per categories
            if c in range(db['ca_ids']):
                if len(bk[seq_ids]>0):
                    sel_train = []
                else:
                    sel_train = []
                    
            print('block_dictionary: processing category: ''%s'''%
                  (db['cat_name'][c]))
            descr = collect_features(bk, db, sel_train)
            dict_.append(learn(bk, descr))
        else: #hikm
            # lean one dict for all categories
            if len(bk['seg_ids']) >0:
                sel_train = bk['seg_ids']
            else:
                sel_train = []# id in db['segs'] to train
                #pdb.set_trace()
                if db['segs'][0].has_key('obj_ids'):
                    for i in range(len(db['segs'])):
                        if db['segs'][i]['flag'] == db['TRAIN']  and\
                           len(set(db['cat_ids']) & \
                               set(db['segs'][i]['obj_ids'])) > 0:
                            sel_train.append(i)
                else:
                    for cat_id in db['cat_ids']:
                        intsec = [n for n in range(len(db['segs']) )
                                  if db['segs'][n]['cat']==cat_id and\
                                     db['segs'][n]['flag'] == db['TRAIN'] ]
                        sel_train.extend(intsec)
                ##end if end 
            # if len(bk...
            
            #pdb.set_trace()
            descr = collect_features(bk, db, sel_train)
            #pdb.set_trace()
            dict_ = learn(bk, descr)
        #end if bk[]


        
        ###################################################
        # save
        path = os.path.join(glb.wrd['prefix'], bk['tag'], 'dict-%02d.pkl'%t)
        pickle.dump(dict_,open(path,'wb'))
        print('block_dictionary: dictionary saved.')

            
    #################
    #
    bk = bkend(bk)
    return bk

########
def collect_features(bk, db, sel_train):
    feat_cfg = bkfetch(bk['feat']['tag'])
    ntrain   = len(sel_train)
    d        = bkfetch(feat_cfg, 'descriptors',
                       db['segs'][sel_train[0]]['seg'])
    fdims    = d.shape[0]
    descr    = np.zeros([fdims, bk['nfeats']], dtype=np.uint8)
    
    print('block_dictionary: === Collecting Features ===')
    print('block_dictionary: num training features: %d'%
          (bk['nfeats']))
    print('block_dictionary: num training images  : %d'%
          (ntrain) )
    print('block_dictionary: buffer size :      %.3gMB'%(0))

    #pdb.set_trace()
    ###############################################
    # scan sel_train to count availabl features
    nfeats = np.zeros(ntrain, dtype=np.int)
    for j in range(ntrain):
        seg_id = db['segs'][sel_train[j]]['seg']
        d = bkfetch(feat_cfg, 'descriptors', seg_id)
        nfeats[j] = d.shape[1]

        print('block_dictionary: scannd %3.1f%%:shape=%s'%
              (100.0*(j+1)/ntrain, str(d.shape)))
    print('')


    # totol number of features in sel_train
    av_nfeats = nfeats.sum()

    #pdb.set_trace()

    ################################################
    # randomly extract nfeats from av_feats available features
    which_feats = np.random.permutation(int(av_nfeats))
    which_feats = which_feats[0:min(bk['nfeats'], which_feats.shape[0])]
    which_feats.sort()
    #which_feats = np.asarray(which_feats, dtype=np.int)

    #pdb.set_trace()
    
    if which_feats.shape[0] < bk['nfeats']:
        print('block_dictionary: found only %.3f k features'%(l))
        descr = np.zeros(fdim, which_feats.shape, type='uint8')

    #pdb.set_trace()

    
    # which_feat indexes n enumeration of all the features of the
    # category (across multiple images). We scan 
    bg = 0
    curr_seg = 0
    while True:
        # get name of feature descriptors file
        seg_id     = db['segs'][sel_train[curr_seg]]['seg']
        d          = bkfetch(feat_cfg, 'descriptors', seg_id)

        # last feature in the current image
        last_feat  = nfeats[curr_seg]

        # features sampled from this image
        sel_feats  = which_feats[which_feats < last_feat]
        sel_nfeats = sel_feats.shape[0]
        #print('sel_nfeats=%d'%(sel_nfeats))
        
        # add them to descr buffer
        descr[:, bg:bg+sel_nfeats] = d[:, sel_feats]
        bg = bg+sel_nfeats

        print('block_dictionary: loaded %.1f %%'%(100.0*bg/bk['nfeats']))

        #stop?
        if which_feats.shape[0] == sel_nfeats:
            break

        ##go on
        which_feats = which_feats[sel_nfeats+1:] - last_feat
        cur_seg = curr_seg+1

    ####
    print('')
    return descr

def learn(bk, descr):
    if   bk['dictionary'] == 'ikm':
        print('block_dictionary: === Running IKM ===')
        print('block_dictionary: num words (K): %d'%(bk['ikm_nwords']))
        dict_ = vlfeat.vl_ikmeans(descr,
                                  bk['ikm_nwords'],
                                  verbosity=1,
                                  method='elkan')
        print('block_dictionary: IKM done')
    elif bk['dictionary'] == 'hikm':
        print('block_dictionary: === Runnining HIKM ===')
        print('block_dictionary: num leaves:      %d'%(bk['hikm_nleaves']))
        print('block_dictionary: branching (K):   %d'%(bk['hikm_K']))
        print('block_dictionary: only_leaves:     %d'%(bk['hikm_only_leaves']))
        dict_,asgn = vlfeat.vl_hikmeans(descr,
                                        bk['hikm_K'],
                                        bk['hikm_nleaves'],
                                        verbosity=1 ,
                                        method='elkan')
        print('block_dictionary: HIKM done')
    else:
        raise TypeError('block_dictionary.py :learn() unknown dictionary type')

    return dict_
        
def ikm_push__(bk, dict_, d):
    w = vl_ikmeanspush(d, dict_)
    h = vlblock.vl_ikmeanshist(dict_.shape[1], w)
    sel = np.arange(w.shape[0])
    return w, h,sel


def hikm_push__(bk, dict_, d):
    #pdb.set_trace()
    
    w=vlfeat.vl_hikmeanspush(dict_, d)
    ndescriptors = d.shape[1]
    
    if bk['hikm_only_leaves']==True:
        # convert PATH to leaves to leaf ids
        temp = np.zeros([1,w.shape[1]],dtype=np.double)
        for d_ in range(dict_['depth']):
            temp = tmp * dict_['K']
            temp = tmp + w[d_,:] -1

        w = tmp + 1
        hist = vlfeat.vl_ikemeanshift(dict_[K]^dict_[detph],w)
        sel=np.arange(ndescriptors)
    else:
        wtmp = w.copy()
        nodes = np.zeros([dict_['depth']+1, w.shape[1]], dtype=np.int)
        nodes[0,:] = 1 # Root node
        #pdb.set_trace()
        for d in range(dict_['depth']):
            if d >0:
                wtmp[0:d-1, :] = wtmp[0:d-1, :]*dict_['K']
                nodes[d+1,:] = wtmp[0:d+1, :].sum() + 1
            else:
                nodes[d+1,:] = wtmp[0,:] + 1

        #pdb.set_trace()
        hist = vlfeat.vl_hikmeanshist(dict_, w)
        sel = np.tile(np.arange(ndescriptors) ,(dict_['depth']+1, 1))
        sel = sel.flatten()
    return w, hist, sel

def fetch__(bk, what, *varargin):
    if what == 'type':
        return bk['dictionary']
    elif what in ('dict','dictionary'):
        if len(varargin) == 0:
            n = 0
        else:
            n = varargin[0]

        path = os.path.join(glb.wrd['prefix'], bk['tag'], 'dict-%02d.pkl'%n)
        return pickle.load(open(path,'rb'))
    else:
        print('unknown varargin')
    
