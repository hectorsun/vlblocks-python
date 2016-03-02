import vlblocks


vlblocks.glb.wrd['prefix']='/home/sh/tmp'


bk=vlblocks.bkinit('helloworld')
bk['tag']='helloworld@default';
bk,dirty = vlblocks.bkbegin(bk)

if dirty:
    print('Hello world')
    bk=vlblocks.bkend(bk)
else:
    print('not dirty')
