inputDIR="../STEP3_mergedToys_BkgSmear1pct4mu_FixShape_FixZX/"
outputDIR="../STEP4_getMass_toy/"
outputDIR2="../STEP4_getMass_asimov/"

rm -r ${outputDIR} ${outputDIR2}
if [ ! -d "$outputDIR" ]; then

   mkdir $outputDIR;
   cp -r ../STEP1_CreateDatacards_ICHEP2016_expected_toy/cards_sm13_* ${outputDIR}

fi
if [ ! -d "$outputDIR2" ]; then

   mkdir $outputDIR2;
   cp -r ../STEP1_CreateDatacards_ICHEP2016_expected_toy/cards_sm13_* ${outputDIR2}
   echo ${outputDIR2} 
   ls ${outputDIR2}

fi


for m4ltype in 1D_reco 1D_refit 1Debe_reco 1Debe_refit
do
    for fs in 4e 4mu 2e2mu
    do

    cp ${inputDIR}hzz4l_${fs}S_13TeV_${m4ltype}_withSigToys.input.root ${outputDIR}cards_sm13_${m4ltype}_2p7fb_CB/HCG/125/hzz4l_${fs}S_13TeV.input.root
    cp runToys.py ${outputDIR}cards_sm13_${m4ltype}_2p7fb_CB/HCG/125/
    cp runAllToys.sh ${outputDIR}cards_sm13_${m4ltype}_2p7fb_CB/HCG/125/

    echo ${outputDIR}cards_sm13_${m4ltype}_2p7fb_CB/HCG/125 
    ls ${outputDIR}cards_sm13_${m4ltype}_2p7fb_CB/HCG/125
    done
done
