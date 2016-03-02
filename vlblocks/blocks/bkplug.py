

def bkplug(bk, input_, tag):
    if not input_ in bk['inputs']:
        bk['inputs'].append(input_)
        
    bk[input_]['tag'] = tag
    bk[input_]['timestamp'] = 0
    return bk
        
