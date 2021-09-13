import h5py
import numpy as np
from re import sub
import sys

filename = sys.argv[1]
deta_jj = 1.4

def xyze_to_eppt(constituents):
    ''' converts an array [N x 100, 4] of particles
from px, py, pz, E to eta, phi, pt (mass omitted)
    '''
    PX, PY, PZ, E = range(4)
    pt = np.sqrt(np.float_power(constituents[:,:,PX], 2) + np.float_power(constituents[:,:,PY], 2), dtype='float32') # numpy.float16 dtype -> float power to avoid overflow
    eta = np.arcsinh(np.divide(constituents[:,:,PZ], pt, out=np.zeros_like(pt), where=pt!=0.), dtype='float32')
    phi = np.arctan2(constituents[:,:,PY], constituents[:,:,PX], dtype='float32')

    return np.stack([pt, eta, phi], axis=2)

with h5py.File(filename, "r") as f:

    f_sig = sub('\.h5$', '_sig.h5', filename)
    f_side = sub('\.h5$', '_side.h5', filename)
    sig_hf = h5py.File(f_sig, 'w')
    side_hf = h5py.File(f_side, 'w')

    # List all groups
    #print("Keys: %s" % f.keys())
    #a_group_key = list(f.keys())[0]
    #print(f["jet_kinematics"][:,1:2][:,0])

    sig_mask = (f["jet_kinematics"][:,1:2][:,0] < deta_jj)
    side_mask = (f["jet_kinematics"][:,1:2][:,0] > deta_jj)

    #print(f["jet_kinematics"][:,1:2][:,0])
    #print(np.reshape(f["jet_kinematics"][:,2],(-1,1)))
    # Preparing signal region files

    # First jet
    pf1 = xyze_to_eppt(np.array(f["jet1_PFCands"]))
    pf1[:,:,0] = pf1[:,:,0]/np.reshape(np.array(f["jet_kinematics"][:,2]),(-1,1))
    pf1[:,:,1] = pf1[:,:,1]-np.reshape(np.array(f["jet_kinematics"][:,3]),(-1,1))
    pf1[:,:,2] = pf1[:,:,2]-np.reshape(np.array(f["jet_kinematics"][:,4]),(-1,1))
    pf1 = pf1.astype(np.float32)
    sig_pf1 = pf1[sig_mask].astype(np.float32)
    side_pf1 = pf1[side_mask].astype(np.float32)

    # Second jet
    pf2 = xyze_to_eppt(np.array(f["jet2_PFCands"]))
    pf2[:,:,0] = pf2[:,:,0]/np.reshape(np.array(f["jet_kinematics"][:,6]),(-1,1))
    pf2[:,:,1] = pf2[:,:,1]-np.reshape(np.array(f["jet_kinematics"][:,7]),(-1,1))
    pf2[:,:,2] = pf2[:,:,2]-np.reshape(np.array(f["jet_kinematics"][:,8]),(-1,1))
    pf2 = pf2.astype(np.float32)
    sig_pf2 = pf2[sig_mask].astype(np.float32)
    side_pf2 = pf2[side_mask].astype(np.float32)

    sig_jj = np.array(f["jet_kinematics"])[sig_mask].astype(np.float32)
    sig_truth = np.array(f["truth_label"])[sig_mask].astype(np.float32)
    side_jj = np.array(f["jet_kinematics"])[side_mask].astype(np.float32)
    side_truth = np.array(f["truth_label"])[side_mask].astype(np.float32)

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

    # Get the data
    #data = list(f[a_group_key])
    #for i in data:
    #   print(i)

    #sig_idx = []
    #side_idx = []
    #data = list(f['jet_kinematics'])
    #counter = 0
    #for i in data:
    #    print(i[1:2][0])
    #    if i[1:2][0] > 1.4:
    #        side_idx.append(counter)
    #    else:
    #        sig_idx.append(counter)
    #    counter +=1 
