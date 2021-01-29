import os
import shutil
import nibabel as nib
import numpy as np
from dmipy.signal_models import cylinder_models, gaussian_models
from dmipy.core.modeling_framework import MultiCompartmentModel
from dmipy.core.acquisition_scheme import acquisition_scheme_from_bvalues



# AnalysisContext documentation: https://docs.qmenta.com/sdk/sdk.html
def run(context):

    ####################################################
    # Get the path to input files  and other parameter #
    ####################################################
    context.set_progress(message='Retrieving data.')
    analysis_data = context.fetch_analysis_data()
    settings = analysis_data['settings']
    root_path = '/root'

    dwi_file_handle = context.get_files('input', modality='DWI')[0]
    dwi_file_path = dwi_file_handle.download(root_path)

    mask_file_handle = context.get_files('input', tags={'wm_mask'})[0]
    mask_file_path = mask_file_handle.download(root_path)

    bvalues_file_handle = context.get_files('input', tags={'bval'})[0]
    bvecs_file_handle = context.get_files('input', tags={'bvec'})[0]
    bvalues_file_path = bvalues_file_handle.download(root_path)
    bvecs_file_path = bvecs_file_handle.download(root_path)

    output_file_path = os.path.join(root_path, 'results.zip')

    #############################
    # Fitting NODDI using AMICO #
    #############################
    context.set_progress(message='Setting up model.')
    ball = gaussian_models.G1Ball()
    stick = cylinder_models.C1Stick()
    BAS_mod = MultiCompartmentModel(models=[stick, ball])

    dwi = nib.load(dwi_file_path)
    dwi_data = dwi.get_fdata()
    mask = nib.load(mask_file_path)
    mask_data = mask.get_fdata()
    bval = np.loadtxt(bvalues_file_path)
    bvec = np.loadtxt(bvecs_file_path)
    grad = acquisition_scheme_from_bvalues(bval, bvec.T)

    BAS_fit = BAS_mod.fit(grad, dwi_data, mask_data > 0)
    fitted_parameters = BAS_fit.fitted_parameters

    results_folder = os.path.join(root_path, 'ball_and_stick')
    os.mkdir(results_folder)
    for name, values in fitted_parameters.items():
        res_filename = os.path.join(results_folder, name + '.nii.gz')
        nib.Nifti1Image(values, mask.affine,
                        mask.header).to_filename(res_filename)

    output_file_path = os.path.join(root_path, 'ball_and_stick.zip')
    shutil.make_archive(output_file_path[:-4], 'zip',
                        os.path.join(root_path, 'ball_and_stick'))

    ###################
    # Upload the data #
    ###################

    context.set_progress(message='Uploading results...')
    context.upload_file(output_file_path,
                        'results.zip')

