"""
Simple script that runs CHARMED model from MDT.


"""

import numpy as np
import nibabel as nib
import sys

import mdt


def doCHARMED(input_data_filename, bval_filename, bvec_filename, mask_data_filename,TE):
    protocol = mdt.create_protocol(
        bvecs='bvec_filename.bvec', bvals='bval_filename.bval',
        out_file='mdt.prtcl',
        TE=TE)
    
    input_data = mdt.load_input_data(
        'input_data_filename',
        'mdt.prtcl',
        'mask_data_filename')
    
    mdt.fit_model('CHARMED_r1', input_data, 'charmed_')

if __name__ == '__main__':
    data_path = '/data/'
    #data_path = '/home/ricardo/brainhack-variations'
    
    input_data_filename = data_path + str(sys.argv[1])
    bval_filename = data_path + str(sys.argv[2])
    bvec_filename = data_path + str(sys.argv[3])
    mask_data_filename = data_path + str(sys.argv[4])
    TE = float(sys.argv[5])
    
    doCHARMED(input_data_filename, bval_filename, bvec_filename,  mask_data_filename, TE)
