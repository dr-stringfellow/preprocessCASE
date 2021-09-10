import h5py
import numpy as np
from re import sub
import sys

deta_jj = 1.4

filename = sys.argv[1]

with h5py.File(filename, "r") as f:

    f_sig = sub('\.h5$', '_sig.h5', filename)
    f_side = sub('\.h5$', '_side.h5', filename)
    sig_hf = h5py.File(f_sig, 'w')
    side_hf = h5py.File(f_side, 'w')

    # List all groups
    #print("Keys: %s" % f.keys())
    #print(f["jet_kinematics"][:,1:2][:,0])

    # Input categories explained here
    # https://github.com/case-team/CASEUtils/tree/master/H5_maker

    sig_mask = (f["jet_kinematics"][:,1:2][:,0] < deta_jj)
    side_mask = (f["jet_kinematics"][:,1:2][:,0] > deta_jj)
    #print(mask)

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

