#!/bin/bash -x
#PBS -l select=5:ncpus=28:model=bro
#PBS -q normal
#PBS -l walltime=2:00:00
#PBS -N test

cd $PBS_O_WORKDIR

module purge

# load the module and environment
module -a use /swbuild/analytix/tools/modulefiles
module load miniconda3/v4
source activate EAP

# run python script
python run_single_EAP.py

# deactivate environment
conda deactivate

# end of script
