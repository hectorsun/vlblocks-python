
from bktag import bktag
import re


def bkver(bk):
    tag = bktag(bk)
    #t = re.match(tag, '^w*@(.*)$')
    match =  re.findall(r'^\w*@(.*)$', tag)[0]
    if match is not None:
        #print('bkver: %s')%(match)
        return match
    else:
        print('no match')
        return ''
