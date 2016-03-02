
from bkinit import bkinit
from bkbegin import bkbegin
from bkfetch import bkfetch
from bkend import bkend
import os
import cPickle as pickle


from vlblocks.generics import glb



def block_dbpart(bk=''):
    if bk=='':
        bk=bkinit('dpart', 'db')
        bk['fetch'] = fetch__
        bk['rand_seed'] = []
        bk['db_type'] = ''
        return bk

    ################################
    bk,dirty = bkbegin(bk)
    if not dirty:
        return bk

    db_cfg = bkfetch(bk['db']['tag'])
    db     = bkfetch(bk['db']['tag'], 'db')

    #print db_cfg
    #print db

    #####################################


    
    
    #####################################
    if bk['db_type'] == 'graz02':
        fg = db['cat_names'].index(bk['fg_cat'])
        bg = db['cat_names'].index('none')
        print str(fg)+ str(bg)
        
        segs = db['segs']
        selp = [n for n in range(0, len(segs)) if segs[n]['cat']==fg  ] 
        seln = [n for n in range(0, len(segs)) if segs[n]['cat']==bg  ]
        
        selp = selp[0:150+75]
        seln = seln[0:150+75]

        selp_test = [selp[n] for n in range(0,len(selp),3)]
        seln_test = [seln[n] for n in range(0,len(seln),3)]

        selp_train = [selp[n] for n in range(0,len(selp)) if n%3!=0 ] 
        seln_train = [seln[n] for n in range(0,len(selp)) if n%3!=0 ]

        
        db['segs'] = [db['segs'][n] for n in selp_train ] + [db['segs'][n] for n in seln_train ] +\
                     [db['segs'][n] for n in selp_test ] +  [db['segs'][n] for n in seln_test ]
        
        #print selp_test
        #print '-'*80
        #print seln_test
        #print '-'*80
        #print selp_train
        #print '-'*80
        #print seln_train
        
        for n in range(0,300):
            db['segs'][n]['flag'] = db['TRAIN']

        for n in range(300, 450):
            db['segs'][n]['flag'] = db['TEST']

        #for seg in db['segs']:
        #    print seg

        db['cat_ids'] = [fg, bg]

    
    db['seg_ids'] = [seg['seg'] for seg in db['segs']]
    db['cat_names'] = [db['cat_names'][n] for n in db['cat_ids'] ]

    print db['cat_names']
    
    #######################################################
    # save
    path = os.path.join(glb.wrd['prefix'], bk['tag'], 'db.pkl')
    pickle.dump(db, open(path, 'wb'))

    
    #bk = bkend(bk)
    
    return bk




def fetch__(bk, what, *varargin):
    if what == 'db':
        path = os.path.join(glb.wrd['prefix'], bk['tag'], 'db.pkl')
        return pickle.load(open(path, 'rb'))
    

