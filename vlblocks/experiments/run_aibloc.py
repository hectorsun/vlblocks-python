from aibloc import aibloc
from vlblocks import generics

#cats=['bike', 'cars', 'person']
cats=['bike']


detector_types=['dsift-color']

reg_params=[[15,4,1],[16,4,5]]
atonce=True
onlyleaves=False

dictionary_types=['hikm']


#aib_types=(0, 5, 40, 200, 400)
aib_types=[0]

param={'prefix':'/home/sh/tmp/run_aibloc/',
       'db_path':'/home/sh/Data/TestData/Graz-02/data',
       'db_seg_prefix':'~/data/graz02/cats',
       'ikm_nwords':100,
       'dict_hikm_K':10,
       'dict_hikm_nleaves':1000,
       'db_tag':'gz',
       'partition_data':0,
}


param['use_segs']=True
for c in cats:
    for d in detector_types:
        for q in dictionary_types:
            for a in aib_types:
                param['use_aib'] = (a>0)
                param['aib_nwords']=a
                param['dict_dictionary']=a
                param['dict_tag']='_%s'%(q)

                if param['dict_dictionary'] == 'hikm':
                    param['dict_tag'] = '%sK%02d'%(param['dict_tag'],param['dict_hikm_K'])
                elif param['dict_dictionary'] == 'ikm':
                    param['dict_tag'] = '_ikm%03d'%(param['ikm_nwords'])

                if param['dict_dictionary'] == 'ikm' and atonce == True:
                    param['dict_tag'] = '%s_atonce'%(param['dict_tag'])
                    param['dict_at_once'] = True
                else:
                    param['dict_at_once'] = False

                if param['dict_dictionary'] == 'hikm' and onlyleaves == False:
                    param['dict_hikm_only_leaves'] = False
                    param['dict_tag'] = '%_fulltree'%(param['dict_tag'])
                else:
                    param['dict_hikm_only_leaves'] = True

                if param['use_aib']==True and param['dict_dictionary']=='ikm':
                    continue

                if param['use_aib']==False and param['dict_dictionary']=='hikm':
                    continue

                param['feat_detector']=d
                if d=='dsift':
                    param['feat_descriptor']='dsift'
                elif param['feat_detector']=='dsift-color':
                    param['feat_descriptor']='dsift-color'
                else:
                    param['feat_descriptor']='simipid'


                param['fg_cat'] = c
                param = generics.clearfields(param, 'feat_scales', 'feat_spacing',
                                             'feat_patchwidth','hist_min_sigma','dict_at_once')

                if d == 'regular':
                    for r in reg_params:
                        param['feat_patchwidth']=r[0]
                        param['feat_spacing']=r[1]
                        param['feat_scles']=r[2]
                        param['feat_tag']='regular_%d_%d_%d'%(r[0],r[1],r[2])
                        param['hist_min_sigma']=0
                elif d in ('dsift','dsift-color'):
                    param['feat_tag']=param['feat_detector']
                    param['hist_min_sigma']=0
                else:
                    param['feat_tag']=param['feat_detector']
                    
                ex = aibloc(param)

