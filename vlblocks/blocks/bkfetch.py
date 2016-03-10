from vlblocks.generics import glb
from vlblocks import generics
import cPickle as pickle
import os

from bktag import bktag

import pdb
def bkfetch(bk,*varargin):
    '''
    bk = bkfetch(bk)  return bk unchanged
    bk = bkfetch(TAG) returns the block bk corresonding to TAG
    '''
    if isinstance(bk, dict):
        if not bk.has_key('tag'):
            raise TypeError('BK structure malformed has no .TAG field')

    if isinstance(bk, str):
        if bk == '':
            raise TypeError('Tag name empty')

    if len(varargin)==0:
        if isinstance(bk, dict):
            return bk
        else:
            f = os.path.join(glb.wrd['prefix'], bktag(bk), 'cfg.pkl')
            if not os.path.exists(f):
                raise IOError('bloock %s does not exist'%(f))
            return pickle.load(open(f, 'rb'))
    else:
        if isinstance(bk, str):
            bk=bkfetch(bk)
        varargout =  bk['fetch'](bk,varargin[0], varargin[1:])
        #pdb.set_trace()
        return varargout
    #if len(varargin)==0
            
