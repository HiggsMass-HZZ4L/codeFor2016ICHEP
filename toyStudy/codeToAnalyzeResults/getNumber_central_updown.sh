for dir in 1D_reco 1D_refit 1Debe_reco 1Debe_refit
do
    cd cards_sm13_${dir}_2p7fb_CB/HCG/125
    cp /scratch/osg/mhl/Run2/HZZ4L/PereventMassErrCorr_2016ICHEP/getCorrection_ICHEP2016/toyStudy_test/STEP4_getMass_toy/cards_sm13_1Debe_refit_2p7fb_CB/HCG/125/plotToyResults.py .
    echo ${dir}
    python plotToyResults.py
    cd -
done

