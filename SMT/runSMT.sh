#!/usr/bin/env bash

# creatin proper filenames
inputDir="/data/" 
data="$inputDir$1"
bval="$inputDir$2"
bvec="$inputDir$3"
mask="$inputDir$4"
output="${inputDir}smt_{}.nii"

#Executing SMT
smt-0.4-linux-x64/bin/fitmcmicro --bvals $bval --bvecs $bvec --mask $mask $data $output
