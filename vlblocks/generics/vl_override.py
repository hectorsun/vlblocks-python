def vl_override(config, update, *varargin) :
    if not isinstance(config,dict):
        return update

    if not isinstance(update,dict):
        return update

    #if len(config) != len(update):
    #    return update    

    for key in update.keys():
        if not config.has_key(key):
            print('config has not key: %s'%(str(key)))
        config[key] = update[key]    
    return config
