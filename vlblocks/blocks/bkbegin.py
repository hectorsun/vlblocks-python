import os
from vlblocks.generics import glb
from vlblocks import generics
import cPickle as pickle
import pdb

def bkbegin(bk):
    '''
    bkbegin begin a block
    bk,dirty = bkbegin(bk) Begin a block BK by first checking if it exists.
    if the block exists, it chech if any input blocks have changed. It also
    check if any inpit parameters have been changed, added, or removed. 
    if any of these conditions is ture, dirty is set as true, and bk contains 
    the modified block.
    '''
    
    #glb.wrd is the global variable to store global information
    if not isinstance(bk,dict):
        raise TypeError

    if not isinstance(glb.wrd, dict):
        raise TypeError
    
    if not glb.wrd.has_key('bless_all'):
        glb.wrd['bless_all']=False
    if not glb.wrd.has_key('pretend'):
        glb.wrd['pretend']=False

        
    bk_file = os.path.join(glb.wrd['prefix'], bk['tag'],'cfg.pkl')
    dirty=False
    type_=bk['type']

    #check whether we are in pretend mod
    if glb.wrd['pretend']:
        print('block_%s: Pretending [%s]'%(type_,bk['tag']))
        return bk,dirty
    if glb.wrd['bless_all']:
        print('block_%s: Blessing [%s]'%(type_,bk['tag']))    
        # bk=vlblocks.bkbless(bk);
        return bk,dirty

    generics.ensuredir(os.path.join(glb.wrd['prefix'], bk['tag']))

    #pdb.set_trace()
    ##################################################
    #check if configuration has changed
    if os.path.isfile(bk_file):
        try:
            bk_old = pickle.load(open(bk_file,'rb'))
        except:
            bk_old={}
            dirty=True
        
        if not xdiff(type_, bk, bk_old):
            dirty=1
            print('block %s configuration changed'%(type_))
        else:
            bk=bk_old
    else:
        print('block%s: ')%(type_)
        dirty=True

    '''
    ##################################################
    # check if inputs have changed
    for i in range(len(bk.inputs)):
        in_name = bk['inputs'][i]
        in_tag  = bk[in_name].tag

        if in_tag == '':
            print()
            continue
        #end if in_tag=''

        in_ = bkfeatch(in_tag)
        if in_timestamp > bk.(in_name).timestamp:
            dirty = True;

        #end if in_ ...
        bk[in_name].timestamp = in_.timestamp
    #end for i in range(len(bk.inputs))
    '''

    
    if not dirty:
        pass
    else:
        pass
        #bk.started = now
    #end


    return bk,dirty

def xdiff(type_,a,b,path=''):
    '''
    eq = xdiff(a,b) compares configuration a and b
    '''
    #pdb.set_trace()
    eq = True
    import types
    if type(a) != type(b):# type unmatch 
        eq = False
        print '1'
    elif isinstance(a,dict):# a and b are dict
        if len(a) != len(b):
            eq = False,
            print'2'
        else:
            for key in a.keys():
                # iterate all keys
                if key in ('timestamp', 'split','started'):
                    #ignore this fileds
                    continue
                    
                if not b.has_key(key):
                    eq=False,
                    print '3'
                    break
                else:
                    eq = eq & xdiff(type_,a[key],b[key])
            # for key in a.keys()
        #if len(a) !=len(b)
    elif isinstance(a,(int,long,float,complex,str)):
        eq = (0== cmp(a,b))
    elif type(a) is types.FunctionType:
        eq=True
    else:
        raise TypeError
                
    return eq
