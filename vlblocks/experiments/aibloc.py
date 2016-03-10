import vlfeat
from vlblocks.generics import glb
from vlblocks import generics
import vlblocks
import numpy as np

import pdb


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
    #print ex['dbpart']['tag']
    ex['dbpart']['fg_cat']     =  param['fg_cat']
    ex['dbpart']['db_prefix']  =  ex['db']['db_prefix']
    ex['dbpart']['db_type']    =  ex['db']['db_type']

    ex['dbpart']=vlblocks.bkplug(ex['dbpart'], 'db',ex['db']['tag'])
    ex['dbpart']=vlblocks.block_dbpart(ex['dbpart'])

    #print vlblocks.bktag(ex['dbpart'])

    
    ###################################################
    # partition training data
    '''
    if param['partition_data'] == True:
        #rand
        db = bkfetch(ex['dbpart'], 'db')
        seg_ids = [n for n in range(len(db['segs'])) if db['segs'][n]['flag'] ==db['TRAIN']]
        dict_seg_ids=[]
        for cat_id = in db['cat_ids']:
            cat_ids

    '''




    #####################################################
    # trainning dictionary
    ex['dict'] = vlblocks.block_dictionary()
    if param['partition_data'] == True:
        param['dict_tag'] = '%s_part'%(param['dict_tag'])
    ex['dict']['tag']  = 'dict@%s%s%s'%(vlblocks.bkver(ex['dbpart']), param['feat_tag'], param['dict_tag'])
    ex['dict']['dictionary']  = param['dict_dictionary']
    ex['dict']['nfeats']  = 2*50000
    ex['dict']['rand_seed']  = 1
    ex['dict']['ntrials']  = param['dict_ntrials']
    ex['dict']['split']  = ex['dict']['ntrials']

    if param['partition_data'] == True:
        ex['dict']['seg_ids']  = dict_segs_ids

    ex['dict']['ikm_nwords']  = param['dict_ikm_nwords']
    ex['dict']['hikm_K']  = param['dict_hikm_K']
    ex['dict']['hikm_nleaves']  = param['dict_hikm_nleaves']
    ex['dict']['hikm_only_leaves']  = param['dict_hikm_only_leaves']

    ex['dict']['ikm_at_once']  = param['dict_at_once']

    ex['dict'] = vlblocks.bkplug( ex['dict'],'db' ,  ex['dbpart']['tag'] )
    ex['dict'] = vlblocks.bkplug( ex['dict'],'feat' ,ex['feat']['tag'] )

    #print ex['dict']
    ex['dict'] = vlblocks.block_dictionary(ex['dict'])

    ########################################################
    # repeat kernels, learn svms, test svms,
    for trial in range(param['dict_ntrials']):
        #####################################################
        # select a dictionary
        ex['dictsel'] = vlblocks.block_dict_sel()
        ex['dictsel']['tag'] = 'dictsel@%s_tri%d'%(vlblock.bkver(ex['dict']['tag']),trial)
        ex['dictsel']['selection'] = trial

        ex['dictsel'] = vlblocks.bkplug(ex['dictsel'], ex['dict']['tag'])
        ex['dictsel'] = vlblocks.block_dict_sel(ex['dictsel'])
        
        
        #####################################################
        # compute histograms
        ex['hist'] = vlblocks.block_hist()
        if param['use_segs']:
            ex['hist']['tag'] = 'hist@%s_seg'%(vlblock.bkver(ex['dictsel']['tag']))
            ex['hist']['seg_prefix'] = param['db_seg_prefix']
            ex['hist']['seg_ext'] = 'png'
            ex['hist']['fg_id'] = param['fg_id']
            ex['hist']['fg_cat'] = param['fg_cat']
        else:
            ex['hist']['tag'] = 'hist@%s'%(vlblock.bkver(ex['dictsel']['tag']))

        ex['hist']['split'] = 30
        ex['hist']['min_sigma'] = param['hist_min_sigma']
        ex['hist'] = vlblock.bkplug(ex['hist'], 'db',   ex['depart']['tag'])
        ex['hist'] = vlblock.bkplug(ex['hist'], 'feat', ex['feat']['tag'])
        ex['hist'] = vlblock.bkplug(ex['hist'], 'dict', ex['dictsel']['tag'])
        ex['hist'] = vlblock.block_hist(ex['hist'])

        if param['use_aib'] == True:
            ex['aib'] = vlblock.block_aib()
            ex['aib']['tag'] = 'aib@%s'%(ex['hist']['tag'])
            if param['partition_data'] ==True:
                ex['aib']['sed_ids'] = dict_seg_ids
            ex['aib'] = vlblock.bkplug(ex['aib'], 'db' ,ex['dbpart']['tag'])
            ex['aib'] = vlblock.bkplug(ex['aib'], 'hist' ,ex['hist']['tag'])

            ex['aibdict'] = vlblock.block_aibdict()
            ex['aibdict']['nwords'] = param['aib_nwords']
            ex['aibdict']['tag']    = 'aibdict@%s_aib%d'%(vlblock.bkver(ex['aib']), param['aib_nwords'])
            ex['aibdict'] = vlblock.bkplug(ex['aibdict'], 'aib', ex['aib']['tag'])
            ex['aibdict'] = vlblock.bkplug(ex['aibdict'], 'dict', ex['dict']['tag'])
            ex['aibdict'] = vlblock.block_aibdict(ex['aibdict'])

            ex['hist_noaib'] = ex['hist']
            ex['hist'] = vlblock.block_hist()
            if param['use_segs'] == True:
                ex['hist']['tag'] = 'hist@%s_seg'%(vlblock.bkver(ex['aibdict']['tag']))
                ex['hist']['seg_prefix'] = param['db_seg_prefix']
                ex['hist']['seg_ext'] = 'png'
                ex['hist']['fg_id'] = param['fg_id']
                ex['hist']['fg_cat'] = param['fg_cat']
            else:
                ex['hist']['tag'] = 'hist@%s'%(vlblock.bkver(ex['aibdict']['tag']))
            ex['hist']['split'] = 30
            ex['hist']['min_sigma'] = param['hist_min_sigma']
            ex['hist'] = vlblock.bkplug(ex['hist'], 'db', ex['dbpart']['tag'])
            ex['hist'] = vlblock.bkplug(ex['hist'], 'feat', ex['feat']['tag'])
            ex['hist'] = vlblock.bkplug(ex['hist'], 'dict', ex['aibdict']['tag'])
            ex['hist'] = vlblock.block_hist(ex['hist'])
            
        #####################################################
        # compute kernel

        #####################################################
        # test SVM

        #####################################################
        #

        #####################################################
        #

        
        pass


    
    ########################################################
    return ex
