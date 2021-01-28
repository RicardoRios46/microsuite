import os
import amico
import numpy as np
from dipy.io.gradients import read_bvals_bvecs
from dipy.core.geometry import normalized_vector
import shutil


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
    context.set_progress(message='Setting up AMICO.')
    amico.core.setup()

    ae = amico.Evaluation(root_path, '.')

    [_, bvecs] = read_bvals_bvecs(None, bvecs_file_path)
    bvecs_norm = normalized_vector(bvecs)
    bvecs_norm[0] = [0, 0, 0]
    np.savetxt('/root/grad_norm.txt', np.matrix.transpose(bvecs_norm), fmt='%.3f')

    amico.util.fsl2scheme(bvalues_file_path, '/root/grad_norm.txt', '/root/grad.scheme')

    ae.load_data(dwi_filename=dwi_file_path,
                 scheme_filename='grad.scheme', mask_filename=mask_file_path, b0_thr=30)

    ae.set_model('NODDI')
    ae.generate_kernels()
    ae.load_kernels()
    context.set_progress(message='Fitting NODDI maps.')
    ae.fit()

    ae.save_results()

    output_file_path = os.path.join(root_path, 'AMICO_NODDI.zip')
    shutil.make_archive(output_file_path[:-4], 'zip',
                        os.path.join(root_path, 'AMICO/NODDI/FIT_ICVF.nii.gz'))

    ###################
    # Upload the data #
    ###################

    context.set_progress(message='Uploading results...')
    context.upload_file(output_file_path,
                        'results.zip')

