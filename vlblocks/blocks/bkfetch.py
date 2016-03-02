from vlblocks.generics import glb
from vlblocks import generics
import cPickle as pickle


def bkfetch(bk,*varargin):
    '''
    bk = bkfetch(bk)  return bk unchanged
    bk = bkfetch(TAG) returns the block bk corresonding to TAG
    '''
    if isinstance(bk, dict):
        if bk.has_key('tag'):
            raise TypeError

    if isinstance(bk, str):
        if bk == '':
            raise TypeError

    if len(varargin)==0:
        if isinstance(bk, dict):
            return bk
        else:
            file = os.path.join(glb.wrd['prefix'],bktag[bk], 'cfg.pkl')
            if not os.path.exists(file):
                raise IOError
            return pickle.load(open(file, 'rb'))
    else:
        if isinstance(bk, str):
            bk=bkfetch(bk)
        return bk['fetch'](bk,varargin)
    #if len(varargin)==0
            
