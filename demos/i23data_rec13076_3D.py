#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
# reading and reconstructing I23 data, sample 13076, fly-scan 
"""
# reading i23 data
import h5py
import numpy as np
import matplotlib.pyplot as plt
from tomobar.supp.suppTools import normaliser
from tomobar.methodsDIR import RecToolsDIR
from tomobar.methodsIR import RecToolsIR

vert_tuple = [i for i in range(500,650)] # selection of vertical slice
#vert_tuple = [i for i in range(0,1600)] # selection of vertical slice

h5py_list = h5py.File('/dls/i23/data/2019/nr23017-1/processing/tomography/rotated/13076/13076.nxs','r')

darks = h5py_list['/entry1/instrument/flyScanDetector/data'][0:19,vert_tuple,:]
flats = h5py_list['/entry1/instrument/flyScanDetector/data'][20:39,vert_tuple,:]

data_raw = h5py_list['/entry1/instrument/flyScanDetector/data'][40:-1-20,vert_tuple,:]
angles = h5py_list['/entry1/tomo_entry/data/rotation_angle'][:] # extract angles
angles_rad = angles[40:-1-20]*np.pi/180.0

h5py_list.close()

fig= plt.figure()
plt.rcParams.update({'font.size': 21})
plt.subplot(131)
plt.imshow(flats[18,:,:], vmin=250, vmax=50000, cmap="gray")
plt.title('Flat field image')
plt.subplot(132)
plt.imshow(darks[18,:,:], vmin=0, vmax=1000, cmap="gray")
plt.title('Dark field image')
plt.subplot(133)
plt.imshow(data_raw[0,:,:],  cmap="gray")
plt.title('First raw projection')
plt.show()
#%%
# normalising the data
starind = 150 # index to start
addSlices = 50 # slices to add to start index
vert_select = [i for i in range(starind,starind+addSlices)] # selection for normalaiser
data_norm = normaliser(data_raw[:,vert_select,:], flats[:,vert_select,:], darks[:,vert_select,:], log='log')
#data_norm = normaliser(data_raw, flats, darks, log='log')

plt.figure()
plt.imshow(data_norm[0,:,:], vmin=0, vmax=1.8, cmap="gray")
plt.title('Normalised projection')
#%%
# One can crop automatically the normalised data
from tomobar.supp.suppTools import autocropper
cropped_data = autocropper(data_norm, addbox=20, backgr_pix1=20)

plt.figure()
plt.imshow(cropped_data[0,:,:], vmin=0, vmax=1.8, cmap="gray")
plt.title('Cropped normalised projection')

# swapping axis to satisfy the reconstructor
cropped_data = np.swapaxes(cropped_data,0,1)
slices, anglesNum, detectHorizCrop = np.shape(cropped_data)
del data_raw, darks, flats
#%%
# Reconstructing normalised data with FBP
RectoolsDIR = RecToolsDIR(DetectorsDimH = detectHorizCrop,  # DetectorsDimH # detector dimension (horizontal)
                    DetectorsDimV = slices,  # DetectorsDimV # detector dimension (vertical) for 3D case only
                    CenterRotOffset = 27.0, # Center of Rotation (CoR) scalar (for 3D case only)
                    AnglesVec = angles_rad, # array of angles in radians
                    ObjSize = detectHorizCrop, # a scalar to define reconstructed object dimensions
                    device='gpu')

FBP = RectoolsDIR.FBP(cropped_data)

plt.figure()
plt.imshow(FBP[4,:,:], vmin=-0.001, vmax=0.005, cmap="gray")
plt.title('FBP reconstruction')
plt.show()
#%%
#data_raw_norm = cropped_data/np.max(cropped_data)

# set parameters and initiate a class object
Rectools = RecToolsIR(DetectorsDimH = detectHorizCrop,  # DetectorsDimH # detector dimension (horizontal)
                    DetectorsDimV = slices,  # DetectorsDimV # detector dimension (vertical) for 3D case only
                    CenterRotOffset = 27.0, # Center of Rotation (CoR) scalar (for 3D case only)
                    AnglesVec = angles_rad, # array of angles in radians
                    ObjSize = detectHorizCrop, # a scalar to define reconstructed object dimensions
                    datafidelity='LS',# data fidelity, choose LS, PWLS
                    nonnegativity='ENABLE', # enable nonnegativity constraint (set to 'ENABLE')
                    OS_number = 12, # the number of subsets, NONE/(or > 1) ~ classical / ordered subsets
                    tolerance = 1e-09, # tolerance to stop outer iterations earlier
                    device='gpu')

lc = Rectools.powermethod() # calculate Lipschitz constant (run once to initilise)
#%%
RecFISTA = Rectools.FISTA(cropped_data, \
                          iterationsFISTA = 15, \
                          regularisation = 'FGP_TV', \
                          regularisation_parameter = 0.0000015,\
                          regularisation_iterations = 350,\
                          lipschitz_const = lc)

plt.figure()
plt.imshow(RecFISTA[3,:,:], vmin=-0.001, vmax=0.005, cmap="gray")
plt.title('Iterative FISTA-TV reconstruction')
plt.show()
#%%
from ccpi.filters.regularisers import PatchSelect

print ("Pre-calculating weights for non-local patches using FBP image...")

pars = {'algorithm' : PatchSelect, \
        'input' : FBP,\
        'searchwindow': 7, \
        'patchwindow': 2,\
        'neighbours' : 15 ,\
        'edge_parameter':0.0008}
H_i, H_j, Weights = PatchSelect(pars['input'], pars['searchwindow'], pars['patchwindow'], pars['neighbours'],
              pars['edge_parameter'],'gpu')

plt.figure()
plt.imshow(Weights[0,:,:], vmin=0, vmax=1, cmap="gray")
plt.colorbar(ticks=[0, 0.5, 1], orientation='vertical')
#%%
RecFISTA_NLTV_os = Rectools.FISTA(cropped_data, 
                              weights=data_raw_norm, \
                              huber_data_threshold = 0.017,\
                              iterationsFISTA = 12, \
                              regularisation = 'NLTV', \
                              regularisation_parameter = 0.000005,\
                              regularisation_iterations = 30,\
                              NLTV_H_i = H_i,\
                              NLTV_H_j = H_j,\
                              NLTV_Weights = Weights,\
                              lipschitz_const = lc)
plt.figure()
plt.imshow(RecFISTA_NLTV_os, vmin=0, vmax=0.008, cmap="gray")
plt.show()
#%%
#%%
"""
h5f = h5py.File('i23_13076.h5', 'w')
h5f.create_dataset('data_norm', data=data_norm)
#h5f.create_dataset('flats', data=flats)
#h5f.create_dataset('darks', data=darks)
h5f.create_dataset('angles_rad', data=angles_rad)
h5f.close()
"""

