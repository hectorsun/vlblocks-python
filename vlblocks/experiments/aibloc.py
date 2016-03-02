import vlfeat
from vlblocks.generics import glb
from vlblocks import generics
import vlblocks
import numpy as np



def aibloc(param):
    defparam = {'prefix'                 : '',
                'db_path'                : '',
                'db_seg_prefix'          : '',
                'db_type'                : 'graz02',
                'db_tag'                 : 'gz',
                'fg_cat'                 : 'bike',
                'feat_tag'               : '',
                'feat_detector'          : 'ipld',
                'feat_descriptor'        : 'simipld',
                'feat_min_sigma'         : 0,
                'feat_rescale'           : 6,
                'feat_ref_size'          : [],
                'feat_patchwidth'        : 16,
                'feat_spacing'           : 4,
                'feat_scales'            : 1,
                'hist_min_sigma'         : 2.5,
                'ker_tag'                : '_chi2',
                'ker_type'               : 'dchi2',
                'ker_normalize'          : '11',
                'ker_metric'             : 1,
                'dict_ntrials'           : 1,
                'dict_tag'               : '',
                'dict_size'              : 200,
                'dict_dictionary'        : 'ikm',
                'dict_ikm_nwords'        : 200,
                'dict_hikm_K'            : 10,
                'dict_hikm_nleaves'      : 10000,
                'dict_hikm_only_leaves'  : 1,
                'dict_at_once'           : 0,
                'use_aib'                : 0,
                'aib_nwords'             : 40,
                'use_segs'               : 0,
                'partition_data'         : 0 
    }

    param = generics.vl_override(defparam, param)
    
    glb.wrd.clear()
    glb.wrd['prefix']=param['prefix']
    glb.wrd['enable_split']=True
    glb.wrd['bless_all']=0
    glb.wrd['pretend']=0
    cat_ids = (('bike',1),
               ('cars',2),
               ('person',3),
               ('none',0))

    for cat,id in cat_ids:
        if cat == param['fg_cat']:
            param['fg_id'] = id


    #####################################################
    ex = {}
    ######################################################
    # construct databases
    ex['db'] = vlblocks.block_db()
    ex['db']['tag'] = 'db@%s'%(param['db_tag'])
    ex['db']['db_type'] = param['db_type']
    ex['db']['db_prefix'] = param['db_path']

    ex['db'] = vlblocks.block_db(ex['db'])

    
    #######################################################    
    # feature extraction
    ex['feat'] = vlblocks.block_feat()
    ex['feat']['tag'] = 'feat@%s%s'%(param['db_tag'],param['feat_tag'])
    ex['feat']['min_sigma'] = param['feat_min_sigma']
    ex['feat']['rescale'] = param['feat_rescale']
    ex['feat']['ref_size'] = param['feat_ref_size']
    ex['feat']['max_num'] = np.inf
    ex['feat']['detector'] = param['feat_detector']
    ex['feat']['descriptor'] = param['feat_descriptor']
    ex['feat']['spacing'] = param['feat_spacing']
    ex['feat']['scales'] = param['feat_scales']
    ex['feat']['patchwidth'] = param['feat_patchwidth']


    if param['feat_detector'] in ('dsift','dsift-color'):
        ex['feat']['dsift_size'] = 4
        ex['feat']['dsift_step'] = 4
        ex['feat']['dsift_minnorm'] = 0.015
        
    ex['feat']['split'] = 30
    ex['feat']['rand_seed'] =1
    

    ex['feat'] = vlblocks.bkplug(ex['feat'], 'db', ex['db']['tag'])
    ex['feat'] = vlblocks.block_feat(ex['feat'])

    #######################################################
    #


    #########################################################
    #select category/ training/testing
    ex['dbpart'] = vlblocks.block_dbpart()
    ex['dbpart']['tag']        =  'dbpart@%s_%s'%(param['db_tag'],param['fg_cat'])
    ex['dbpart']['fg_cat']     =  param['fg_cat']
    ex['dbpart']['db_prefix']  =  ex['db']['db_prefix']
    ex['dbpart']['db_type']    =  ex['db']['db_type']

    ex['dbpart']=vlblocks.bkplug(ex['dbpart'], 'db',ex['db']['tag'])
    ex['dbpart']=vlblocks.block_dbpart(ex['dbpart'])
    
    return ex
