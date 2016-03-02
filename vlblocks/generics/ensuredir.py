import os
def ensuredir(path):
    """
    make sure a dictory exists.
    """
    
    if path=='':
        return
    
    path=os.path.realpath(path)
    
    if os.path.exists(path):
        return
    
    print path
    subpath,name=os.path.split(path)
    print subpath,name
    
    ensuredir(subpath)

    if not os.path.exists(path):
        os.mkdir(path)
        
