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
        'inputs'    :  {},
    }
    
    return bk
