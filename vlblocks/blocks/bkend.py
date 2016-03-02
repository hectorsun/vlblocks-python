import os

from vlblocks import generics
from vlblocks.generics import glb
import cPickle as pickle



def bkend(bk):
    bk_file = os.path.join(glb.wrd['prefix'], bk['tag'], 'cfg.pkl')
    pickle.dump(bk, open(bk_file,'wb'))
    return bk
