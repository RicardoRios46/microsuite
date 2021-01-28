"""
Simple script that tuns WMTI model from DIPY.


"""

import numpy as np
import nibabel as nib
import sys

from dipy.io import read_bvals_bvecs
from dipy.core.gradients import gradient_table

import dipy.reconst.dki_micro as dki_micro


def doWMTI(input_data_filename, bval_filename, bvec_filename, mask_data_filename):
    # Loading data
    img = nib.load(input_data_filename)
    data = img.get_fdata()
    bvals, bvecs = read_bvals_bvecs( bval_filename, bvec_filename)
    gtab = gradient_table(bvals,  bvecs)

    # Loading mask
    img_masked = nib.load(mask_data_filename)
    roi_mask = img_masked.get_fdata()

    # Fitting WMTI
    dki_micro_model = dki_micro.KurtosisMicrostructureModel(gtab)
    dki_micro_fit = dki_micro_model.fit(data, mask=roi_mask)

    # Extracting WMTI parameters
    AWF = dki_micro_fit.awf
    TORT = dki_micro_fit.tortuosity

    # Saving map results
    img_AWF = nib.Nifti1Image(AWF, img.affine)
    img_TORT = nib.Nifti1Image(TORT, img.affine)
    nib.save(img_AWF, '/data/wmti_awf.nii.gz') 
    nib.save(img_TORT, '/data/wmti_tort.nii.gz')

if __name__ == '__main__':
    input_data_filename = '/data/' + str(sys.argv[1])
    bval_filename = '/data/' + str(sys.argv[2])
    bvec_filename = '/data/' + str(sys.argv[3])
    mask_data_filename = '/data/' + str(sys.argv[4])
    
    doWMTI(input_data_filename, bval_filename, bvec_filename,  mask_data_filename)
