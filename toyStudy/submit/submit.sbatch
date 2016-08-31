#!/bin/sh
#SBATCH --job-name=${dir}_%A-%a # Job name
#SBATCH --mail-type=ALL # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=mhl0116@ufl.edu # Where to send mail	
#SBATCH --nodes=1 # Use one node
#SBATCH --ntasks=1 # Run a single task	
#SBATCH --cpus-per-task=1 # Number of CPU cores per task
#SBATCH --mem=4gb # Total memory limit
#SBATCH --time=01:00:00 # Time limit hrs:min:sec
#SBATCH --output=${dir}_%A-%a.out # Standard output and error log
#SBATCH --array=1-200%50 # Array range

pwd; hostname; date
 
module load gcc/5.2.0 
date

export SCRAM_ARCH=slc6_amd64_gcc491
export OSG_APP=/osg/app
export VO_CMS_SW_DIR=${OSG_APP}/cmssoft/cms
export CMS_PATH=${VO_CMS_SW_DIR}
. ${CMS_PATH}/cmsset_default.sh

cd ${CMSSWDIR} #/scratch/osg/mhl/Run2/HZZ4L/PereventMassErrCorr_2016ICHEP/getCorrection_ICHEP2016/toyStudy_test/CreateDatacards_ICHEP2016_expected_toy/CMSSW_7_1_5/src
cmsenv

cd ${WORKDIR}

firstToy=`expr $SLURM_ARRAY_TASK_ID - 1 `
firstToy=`expr $firstToy \* $nToysPerJob`
echo $firstToy
lastToy=`expr $SLURM_ARRAY_TASK_ID \* $nToysPerJob - 1`
echo $lastToy

python -u runToys.py -t reco -f ${firstToy} -l ${lastToy} -j $SLURM_ARRAY_TASK_ID #>& results/test${SLURM_ARRAY_TASK_ID}.log

echo This is task $SLURM_ARRAY_TASK_ID
