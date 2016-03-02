def bktag(bk):
    '''
    bktag(TAG): simply return the TAG
    bktag(bk) returns the tag for a block
    '''
    if isinstance(bk,str):
        return bk
    else:
        return bk['tag']
