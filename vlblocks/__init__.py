# Todo do lazy-import 

# import all modules in blocks
__all__=[]
import os
path=os.path.abspath(__file__)
if os.path.isfile(path):
    path=os.path.dirname(path)
_,cur_ext = os.path.splitext(__file__)

blocks_path=os.path.join(path,'blocks')
#print blocks_path

file_list=os.listdir(blocks_path)
exc_list=('__init__')
for fn in file_list:
    #print fn
    f,ext=os.path.splitext(fn)
    #print fn
    if ext == cur_ext:
        if not f in exc_list:
            cmd = 'from .blocks.%s import %s'%(f,f)
            exec(cmd)
            __all__.append(f)



from .generics import glb

glb.wrd['package']='vlblocks-python'

__package__='vlblocks-python'

del _
del path
del cur_ext
del blocks_path
del file_list
del exc_list
del fn
del cmd
del ext
del f
