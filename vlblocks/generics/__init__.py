#Todo : import function in modules automatically
#       except in exc_list

import os
path = os.path.abspath(__file__)
if os.path.isfile(path):
    path=os.path.dirname(path)
_, cur_ext = os.path.splitext(__file__)

file_list = os.listdir(path)
exc_list=('__init__','glb')#list of module don't import
for fn in file_list:
    f,ext = os.path.splitext(fn)
    if ext == cur_ext:
        if not f in exc_list:
            cmd = 'from .%s import %s'%(f,f)
            #print cmd
            exec(cmd)
