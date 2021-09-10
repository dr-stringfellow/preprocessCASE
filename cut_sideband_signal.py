import h5py
import numpy as np
from re import sub
import sys
import pathlib

deta_jj = 1.4

filename = sys.argv[1]
outdir = sys.argv[2]

with h5py.File(filename, "r") as f:

    path = pathlib.PurePath(filename)
    lastFolder = path.parent.name

    fshort = filename.split("/")[-1]
    f_sig = sub('\.h5$', '_sig.h5', fshort)
    f_side = sub('\.h5$', '_side.h5', fshort)
    
    dir_sig = outdir+'/'+lastFolder+'_sig/'
    dir_side = outdir+'/'+lastFolder+'_side/'

    for d in [dir_sig,dir_side]:
        if not os.path.exists(d):
            os.makedirs(d)

    sig_hf = h5py.File(dir_sig+f_sig, 'w')
    side_hf = h5py.File(dir_side+f_side, 'w')

    # List all groups
    #print("Keys: %s" % f.keys())
    #print(f["jet_kinematics"][:,1:2][:,0])

    # Input categories explained here
    # https://github.com/case-team/CASEUtils/tree/master/H5_maker

    sig_mask = (f["jet_kinematics"][:,1:2][:,0] < deta_jj)
    side_mask = (f["jet_kinematics"][:,1:2][:,0] > deta_jj)

    # Preparing signal region files
    sig_pf1 = np.array(f["jet1_PFCands"])[sig_mask].astype(np.float16)
    sig_pf2 = np.array(f["jet2_PFCands"])[sig_mask].astype(np.float16)
    sig_jj = np.array(f["jet_kinematics"])[sig_mask].astype(np.float16)
    sig_truth = np.array(f["truth_label"])[sig_mask].astype(np.float16)
    side_pf1 = np.array(f["jet1_PFCands"])[side_mask].astype(np.float16)
    side_pf2 = np.array(f["jet2_PFCands"])[side_mask].astype(np.float16)
    side_jj = np.array(f["jet_kinematics"])[side_mask].astype(np.float16)
    side_truth = np.array(f["truth_label"])[side_mask].astype(np.float16)

    sig_hf.create_dataset('jet1_PFCands', data=sig_pf1)
    sig_hf.create_dataset('jet1_PFCands_shape', data=sig_pf1.shape)
    sig_hf.create_dataset('jet2_PFCands', data=sig_pf2)
    sig_hf.create_dataset('jet2_PFCands_shape', data=sig_pf2.shape)
    sig_hf.create_dataset('jet_kinematics', data=sig_jj)
    sig_hf.create_dataset('jet_kinematics_shape', data=sig_jj.shape)
    sig_hf.create_dataset('truth_label', data=sig_truth)
    sig_hf.create_dataset('truth_label_shape', data=sig_truth.shape)

    side_hf.create_dataset('jet1_PFCands', data=side_pf1)
    side_hf.create_dataset('jet1_PFCands_shape', data=side_pf1.shape)
    side_hf.create_dataset('jet2_PFCands', data=side_pf2)
    side_hf.create_dataset('jet2_PFCands_shape', data=side_pf2.shape)
    side_hf.create_dataset('jet_kinematics', data=side_jj)
    side_hf.create_dataset('jet_kinematics_shape', data=side_jj.shape)
    side_hf.create_dataset('truth_label', data=side_truth)
    side_hf.create_dataset('truth_label_shape', data=side_truth.shape)

    sig_hf.close()
    side_hf.close()

