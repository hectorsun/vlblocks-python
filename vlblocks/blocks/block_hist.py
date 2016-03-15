from __future__ import print_function

from bkinit  import bkinit
from bkfetch import bkfetch
from bkend   import bkend
from bkbegin import bkbegin
from vlblocks.generics.ensuredir import ensuredir

from skimage.data import imread

from vlblocks.generics import glb

import numpy as np
import os
import cPickle as pickle
import pdb


def block_hist(bk='', *varargin):
    if bk=='':
        bk = bkinit('hist', 'db', 'feat', 'dict')
        bk['fetch'] = fetch__
        bk['min_sigma'] = 0
        bk['max_num'] =   np.inf
        bk['ref_size'] =  []
        bk['rand_seed'] = []
        return bk
    ###############################################
    # check/load inputs
    bk, dirty = bkbegin(bk)
    if not dirty:
        print('block_hist is not dirty')
        return bk

    bkdb   = bkfetch(bk['db']['tag'])
    bkfeat = bkfetch(bk['feat']['tag'])
    bkdict = bkfetch(bk['dict']['tag'])

    db     = bkfetch(bkdb, 'db')
    #pdb.set_trace()
    dict_  = bkfetch(bkdict, 'dictionary')

    
    ###############################################
    # Do computation
    print('block_hist: ref_size:  %s'%(str(bk['ref_size'])))
    print('block_hist: min_sigma: %s'%(str(bk['min_sigma'])))
    print('block_hist: max_num:   %s'%(str(bk['max_num'])))

    #pdb.set_trace()
    
    if bk.has_key('fg_cat'):
        db_fg_id = 0
        for i in range(len(db['cat_names'])):
            if db['cat_names'][i] == bk['fg_cat']:
                db_fg_id = db['cat_ids'][i]
    #pdb.set_trace()

    for i in range(len(db['segs'])):
        #if not len(bk['rand_seed']):
        #    setrandseed(bk['rand_seed']+i)

        seg_id = db['segs'][i]['seg']
        d = bkfetch(bkfeat, 'descriptors', seg_id)

        # filter features
        sel = np.arange(d.shape[1])

        f = bkfetch(bkfeat, 'frames', seg_id)
        if bk['min_sigma'] >0:
            if len[bk['ref_size']] == 0:
                info = bkfetch(bkdb, 'imageinfo', seg_id)
                rho = bk.ref_size / max(info['Width'], info['Height'])
            else:
                rho = 1
            keep = rho * f[2,:] > bk['min_sigma']
            sel = sel[keep]

        # only ilter training image belonging to the fg category
        #
        if bk.has_key('seg_prefix') and \
           db['segs'][i]['flag'] == db['TRAIN'] and\
           db['segs'][i]['cat'] == db_fg_id:
            S = getseg(bk['seg_prefix'],
                       bk['seg_ext'],
                       db['segs'][i]['path'],
                       bk['fg_id'])
            ind = sub2ind(S.shape, round(f[2,:]), round(f[1,:]))
            keep = find(S(ind))
            sel = sel(keep)

        if sel.shape[0] > bk['max_num']:
            N = numel(sel)
            keep = logical(zeros(1,N))

        d = d[:,sel]

        #pdb.set_trace()
        # project features
        w,h,dsel = bkdict['push'](bkdict,dict_, d)
        sel = sel[dsel]

        
        # save back
        #pdb.set_trace()
        path_dir = os.path.join(glb.wrd['prefix'], bk['tag'], 'data')
        ensuredir(path_dir)
        
        path_w = os.path.join(path_dir,  '%05d.w.pkl'%seg_id)
        pickle.dump(w,open(path_w, 'wb'))
        path_sel = os.path.join(path_dir, '%05d.sel.pkl'%seg_id)
        pickle.dump(sel,open(path_sel, 'wb'))
        path_h = os.path.join(path_dir, '%05d.h.pkl'%seg_id)
        pickle.dump(h, open(path_h, 'wb'))

        print('block_hist: %3.1f%% completed'%(100.0*i/len(db['segs'])))

    bk = bkend(bk)
    return bk

#######################################################
def getseg(gt_prefix, gt_ext, imname, fg_cat):
    path_name, ext = os.path.splitext(imname)
    gt_name = os.path.join(gt_prefix, '%s_gt.%s'%(path_name,gt_ext))
    #pdb.set_trace()
    seg = imread(gt_name)
    seg = [seg == fg_cat]
    return seg
    

#######################################################
def fetch__(bk, what, *varargin):
    if what.lower() == 'db':
        return bkfetch(bk['db']['tag'], 'db')
    elif what.lower() == 'dictionary':
        return bkfetch(bk['dict']['tag'], 'dict')
    elif what.lower() == 'histogram':
        i = varargin[0]
        path = os.path.join(glb.wrd['prefix'],
                            bk['tag'],
                            'data',
                            '%05d.h.pkl'%i)

        return pickle.load(open(path, 'rb'))
    elif what.lower() == 'words':
        i = varargin[0]
        path_w = os.path.join(glb.wrd['prefix'],
                              bk['tag'],
                              'data',
                              '%05d.w.pkl'%i)
        data_w = pickle.load(open(path_w, 'rb'))
        path_sel = os.path.join(glb.wrd['prefix'],
                                bk['tag'],
                                'data',
                                '%05d.sel.pkl'%i)
        data_sel = pickle.load(open(path_sel, 'rb'))
        return data_w, data_sel
    else:
        raise TypeError('Unknown "%s"'%(what))
    
