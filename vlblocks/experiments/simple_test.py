import vlblocks
import cPickle as pickle


def simple_test():
    vlblocks.glb.wrd['prefix']='test';
    bk = block_test()
    bk['imsize']=100
    bk['tag']='test@imresiz100'
    #bk = block_test(bk);
    print(bk)


def block_test(bk='',*varargin):
    if bk=='':
        bk=vlblocks.bkinit('test')
        bk['imsize'] = 50
        bk['fetch']  = fetch__;
        return bk

    bk,dirty = vlblocks.bkbegin(bk)
    if not dirty:
        print('not dirty')
        return

    print('dirty')
    output=np.arange(bk['imsize'])

    #save
    path = os.path.join(vlblocks.glb.wrd.prefix, bk['tag'], 'test.pkl')
    pickle.dump(output,open(path,'wb'))
    
    # end
    bk=vlblocks.bkend(bk)
    
    return bk

def fetch__(bk,what,*varargin):
    #vlblocks.glb.wrd
    if what == 'out':
        path = os.path.join(vlblocks.glb.wrd.prefix, bk['tag'], 'test.pkl')
        data = pickle.load(open(path,'rb'))
        return data
    else:
        raise 


if __name__ == '__main__':
    simple_test()
