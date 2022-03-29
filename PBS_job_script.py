#!/bin/bash -x
#PBS -l select=10:ncpus=28:mpiprocs=28:model=bro
#PBS -q normal
#PBS -l walltime=40:00:00
#PBS -N EAP

cd $PBS_O_WORKDIR

module purge

# load the module and environment
module -a use /swbuild/analytix/tools/modulefiles
module load miniconda3/v4
source activate tf2_7

# run python script
python run_batch_EAP_loc.py

# deactivate environment
conda deactivate

# end of script
