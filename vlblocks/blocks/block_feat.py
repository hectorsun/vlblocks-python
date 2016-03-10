
from bkinit import bkinit
from bkbegin import bkbegin
from bkend import bkend
from bkfetch import bkfetch

from bktag import bktag

from vlblocks import generics
from vlblocks.generics import glb

import os
import cPickle as pickle

import numpy as np

import vlfeat
from skimage import img_as_float
from skimage.data import imread


def block_feat(bk='', *varargin):
    if bk == '':
        bk = bkinit('feat', 'db')
        bk['fetch'] = fetch__
        bk['rand_send'] = []
        bk['detector'] = 'sift'
        bk['descriptor'] = 'siftnosmooth'
        bk['ref_size'] = []
        bk['min_sigma'] = 0;
        bk['max_num'] = np.inf
        bk['rescale'] = 6
        return bk
    
    ############################
    # check/load inputs
    bk, dirty = bkbegin(bk)
    if not dirty:
        print('block_feat not dirty')
        return bk

    db = bkfetch(bk['db']['tag'], 'db')
    
    reduce_ = True
    ##############################
    #
    for seg in db['segs']:
        print('process %s'%(seg['path']))
        ##############################
        # preprocess
        Iorig = imread(os.path.join(db['images_path'], seg['path']))
        I = img_as_float(Iorig)
        M,N,K = I.shape
        if len(bk['ref_size']):
            rho = bk.ref_size / np.max(M,N)
        else:
            rho = 1;
        
        Icolor = I
        
        ##############################
        # Detector

        #############################
        # frame selector


        ###############################
        # Descriptor
        if bk['descriptor'] == 'dsift-color':
            
            RGB=(Icolor.sum(2)+np.finfo(float).eps)
            Irgb=Icolor / np.stack((RGB,RGB,RGB),2)

            
            fr,dr=vlfeat.vl_dsift(Irgb[:,:,0],size=bk['dsift_size'],step=bk['dsift_step'],fast=True,norm=True)
            fr=fr.transpose();
            dr=dr.transpose();

            fg,dg=vlfeat.vl_dsift(Irgb[:,:,1],size=bk['dsift_size'],step=bk['dsift_step'],fast=True,norm=True)
            fg=fg.transpose()
            dg=dg.transpose()
        
            d=np.concatenate((dr,dg),axis=0)
            keep1=(fr[2,:]>bk['dsift_minnorm']) | (fg[2,:]>bk['dsift_minnorm'])

            f=fr[0:2,:]
            f=f[:,keep1]
            d=d[:,keep1]

            sigma=bk['dsift_size']*4/6;
            f=np.concatenate((f,
                              sigma*np.ones((1,f.shape[1])) ,
                              np.pi*np.ones((1,f.shape[1]))),axis=0)
            #rescale=6
            R=f[3,:]*bk['rescale']
            keep2=(f[0,:]-R>=0)&(f[0,:]+R<=N-1) & (f[1,:]-R>=0) &( f[1,:]+R<=M-1)
            f=f[:,keep2]
            d=d[:,keep2]
    

        else:
            print('unkonw descriptor')

        ##############################
        # pose process
        f[0:2,:]=(f[0:2,:]-1)/rho+1;
        f[2,:]=f[2,:]/rho;
        #############################
        # save
        path_d = os.path.join(glb.wrd['prefix'],'data','%05d.d.pkl'%(seg['seg']))
        path_f = os.path.join(glb.wrd['prefix'],'data','%05d.f.pkl'%(seg['seg']))
        pickle.dump(f, open(path_f,'wb'))
        pickle.dump(d, open(path_d,'wb'))

    ###################################
    if reduce_==True:
        bk = bkend(bk)    


    return bk



def fetch__(bk, what, *varargin):
    if what == 'descriptors':
        i = varargin[0]
        path = os.path.join(glb.wrd['prefix'],'data','%05d.d.pkl'%(i))
        varargout = pickle.load(open(path, 'rb'))
    elif what == 'frames':
        i = varargin[0]
        path = os.path.join(glb.wrd['prefix'],'data','%05d.f.pkl'%(i))
        varargout = pickle.load(open(path, 'rb'))
    else:
        raise TypeError

    #pdb.set_trace()
    return varargout
