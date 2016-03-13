from vlblocks.generics import glb
from bkinit import bkinit
from bkbegin import bkbegin
from bkfetch import bkfetch
from bkend import bkend




def block_dict_sel(bk=''):
    if bk=='':
        bk = bkinit('dict_sel', 'dict')
        bk['fetch'] = fetch__
        bk['push']  = []
        bk['selection'] = True
        return bk

    bk['push'] = push__

    bk,dirty = bkbegin(bk)
    if not dirty:
        print('block_dict_sel is not dirty')
        return bk

    bk=bkend(bk)
    return bk
#end def 
        


def push__(bk,dict_, d):
    bkdict = bkfetch(bk['dict']['tag'])
    dict_1  = bkfetch(bkdict, 'dictionary', bk['selection'])
    w,h,sel= bkdict['push'](bkdict, dict_, d)
    return w,h,sel


def fetch__(bk, what, *varargin):
    if what == 'type':
        return bkfetch(bk['dict']['tag'], 'type')
    elif what =='dict'or what=='dictionary' :
        return bkfetch(bk['dict']['tag'], 'dictionary', bk['selection'])
    else:
        raise TypeError('unknown %s'%(what))
