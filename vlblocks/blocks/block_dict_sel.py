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
        


def push__(dict_, d):
    bkdict = bkfetch(bk['dict']['tag'])
    dict_  = bkfetch(bkdict, 'dictionary', bk['selection'])
    w,h,sel= bkdict['push'](dict_, d)
    return w,h,sel


def fetch__(bk, what, *varargin):
    if what == 'type':
        return bkfetch(bk['dict']['tag'], 'type')
    elif what in ('dict', 'dictionary'):
        return bkfetch(bk['dict']['tag'], bk['selection'])
    else:
        print('unknown %s'%(what))
