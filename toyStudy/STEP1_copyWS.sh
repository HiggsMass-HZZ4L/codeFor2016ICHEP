#!/bin/bash

tag="BkgSmear1pct4mu_FixShape_FixZX"

outputDir="../STEP2_Toys_"$tag"/"
if [ ! -d "$outputDir" ]; then
   mkdir $outputDir
fi
nextOutputDir="../STEP3_mergedToys_"$tag"/"
if [ ! -d "$nextoutputDir" ]; then
   mkdir $nextoutputDir
fi


for dir in 1Debe_refit 1Debe_reco 1D_refit 1D_reco
do

    inputDir="/scratch/osg/mhl/Run2/HZZ4L/PereventMassErrCorr_2016ICHEP/getCorrection_ICHEP2016/toyStudy_test/STEP1_CreateDatacards_ICHEP2016_expected_toy/cards_sm13_"$dir"_2p7fb_CB/HCG/125/"

    for fs in 2e2mu 4mu 4e
    do

#        outputDir="../STEP2_Toys_"$tag"/"
#        if [ ! -d "$outputDir" ]; then
#           mkdir $outputDir
#        fi
        cp $inputDir"hzz4l_"$fs"S_13TeV.input.root" $outputDir"hzz4l_"$fs"S_13TeV_"$dir".input.root"

    done
#cp /scratch/osg/mhl/Run2/HZZ4L/PereventMassErrCorr_2016ICHEP/getCorrection_ICHEP2016/Mass_ICHEP2016/CreateDatacards_ICHEP2016_unblinded_12.9_v2/cards_sm13_1Debe_refit_2p7fb_CB/HCG/125/hzz4l_2e2muS_13TeV.input.root Toys2D_BkgSmear1pct4mu_FixShape_FixZX_test/hzz4l_2e2muS_13TeV_refit.input.root

done


