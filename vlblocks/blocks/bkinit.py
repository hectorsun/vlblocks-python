def bkinit(type,*varargin):
    '''
    bk = bkinit(type, *varargin) initialize a block of type TYPE.

    e.g.:
    bk=bkinit('TYPE','I1','I2') init
    '''
    bk={'type'      :  type,
        'tag'       :  '',
        'timestamp' :  '',
        'started'   :  '',
        'inputs'    :  [],
    }

    for var in varargin:
        #if not isinstance(var,str):
        #    raise TypeError
        
        bk['inputs'].append(var)
        bk[var]={}
        bk[var]['tag'] = '',
        bk[var]['timestamp'] = 0
    
    return bk
