from vlblocks.generics import glb
from vlblocks import generics
from bkinit import bkinit
from bkbegin import bkbegin
from bkend import bkend
import os
import cPickle as pickle

from skimage.data import imread

def block_db(bk='', ) :
    if bk == '':
        bk = bkinit('db')
        bk['fetch']     =   fetch__
        bk['verb']      =   0
        bk['db_prefix'] =   ''
        bk['db_type']   =   ''
        return bk

    bk,dirty = bkbegin(bk)
    if not dirty:
        print('block_db not dirty')
        return bk

    #################################################
    # scan dataset
    if bk['db_type'] in ('graz02', 'graz02odds'):
        db = generics.dbfrompath(bk['db_prefix'], 'verbose', bk['verb'])
        bg = db['cat_names'].index('none')
        for seg in db['segs']:
            seg['obj_ids'] = [1, seg['cat']]

        #if bk.has_key('seg_prefix'):
        #    for seg in db['segs']:
        #        pathstr,name = os.path.split(seg['path'])
        #        

        if bk.has_key('obj_prefix'):
            pass

        db['class_ids'] = [1,2,0,3]
    else:
        print('unknow data type')
    ###

    
    db['seg_ids'] = range(len(db['segs']))
    db['cat_ids'] = range(len(db['cat_names']))

    #################################################################
    # save
    save_path = os.path.join(glb.wrd['prefix'], bk['tag'], 'db.pkl')
    pickle.dump(db,open(save_path,'wb'))
    bk=bkend(bk)
    
    return bk


def fetch__(bk, what, *varargin):
    if what == 'db':
        save_path = os.path.join(glb.wrd['prefix'], bk['tag'], 'db.pkl')
        return pickle.load(open(save_path, 'rb'))
    elif what == 'image':
        db = bkfeatch('db')
        return imread(varargin[0].path)
    else:
        print('unknow')
    return bk
