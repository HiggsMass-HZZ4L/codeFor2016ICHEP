inputDIR="/scratch/osg/mhl/Run2/HZZ4L/PereventMassErrCorr_2016ICHEP/getCorrection_ICHEP2016/toyStudy_test/STEP1_CreateDatacards_ICHEP2016_expected_toy/cards_sm13_1D_reco_2p7fb_CB/HCG/125/"

if [  -d "../STEP2_expectedYields" ]; then
   rm -r ../STEP2_expectedYields;
fi
mkdir ../STEP2_expectedYields
for fs in 4mu 4e 2e2mu
do
    echo "get expected yields for "${fs}" channel"
    python printWS.py ${inputDIR}hzz4l_${fs}S_13TeV.input.root | grep norm | awk -F "=" {'print $4'} |  awk '{ sum+=$1} END {print sum}' >> ../STEP2_expectedYields/yields_${fs}.txt
    grep rate ${inputDIR}hzz4l_${fs}S_13TeV.txt | awk -F " " {'print $7, $8'} | awk '{ sum+=$1} END {print sum}' >> ../STEP2_expectedYields/yields_${fs}.txt
    grep rate ${inputDIR}hzz4l_${fs}S_13TeV.txt | awk -F " " {'print $9'} | awk '{ sum+=$1} END {print sum}' >> ../STEP2_expectedYields/yields_${fs}.txt

done

echo "#line: 1, signal; 2, irrBkg; 3, redBkg" > ../STEP2_expectedYields/README.txt

head ../STEP2_expectedYields/yields*txt
