import os

def dbfrompath(path, *varargin):

    do_stuffle = False
    verbose = False
    file_filt=('.png', '.PNG', '.jpg' ,'.JPG', '.gif', '.GIF',
               '.bmp', '.BMP', '.pgm', '.PGM', '.pbm', '.PBM',
               '.ppm', '.PPM')

    dir_filt = '.*'

    k=0 #object path
    c=0 #category index
    
    db = {'segs'       : [],
          'depth'      : 1 ,
          'obj_names'  : [],
          'cat_names'  : [],
          'images_path' : path,
          'TRAIN'      : 0,
          'TEST'       : 1,
          'VALIDATION' : 2
    }

    dir_list = os.listdir(path)
    dir_list.sort()
    for dir_name in dir_list:
        if dir_name in ('.', '..'):
            continue

        dir_path = os.path.join(path, dir_name)
        
        if not os.path.isdir(dir_path):
            continue

        db['cat_names'].append(dir_name)

        file_list = os.listdir(dir_path)
        file_list.sort()
        for fn in file_list:
            file_path = os.path.join(dir_path,fn)
            if not os.path.isfile(file_path):
                continue
            
            _,ext = os.path.splitext(file_path)
            if not ext in  file_filt:
                continue
            file_path_ = os.path.join(dir_name, fn) 
            db['segs'].append({'seg' :k,
                            'obj' :k,
                            'cat' :c,
                            'path':file_path_
                        })
            db['obj_names'].append(file_path_)

            k = k+1

            
        c=c+1

    db['aspects'] = db['segs']
    return db
