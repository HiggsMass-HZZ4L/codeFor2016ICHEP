CMSSWdir="/scratch/osg/mhl/Run2/HZZ4L/PereventMassErrCorr_2016ICHEP/getCorrection_ICHEP2016/toyStudy_test/STEP1_CreateDatacards_ICHEP2016_expected_toy/CMSSW_7_1_5/src/"
NToysPerJob=20

#N_totalToy=10000, 200 tasks per dir

for dir in 1D_reco 1D_refit 1Debe_reco 1Debe_refit
do
    workDIR="/scratch/osg/mhl/Run2/HZZ4L/PereventMassErrCorr_2016ICHEP/getCorrection_ICHEP2016/toyStudy_test/STEP4_getMass_toy/cards_sm13_"${dir}"_2p7fb_CB/HCG/125/"

    sbatch --workdir=workdir --array=1-500%50 --job-name="toy_"${dir}_%A-%a.run --output="toy_"${dir}_%A-%a.out --export=dir=${dir},CMSSWDIR=${CMSSWdir},WORKDIR=${workDIR},nToysPerJob=${NToysPerJob} submit.sbatch
    
done
