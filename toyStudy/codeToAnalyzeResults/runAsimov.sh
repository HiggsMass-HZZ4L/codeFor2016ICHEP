#!/bin/bash
dirTag=$1
fs=$2
DIR=$3

curdir=`pwd`

for dir in ${DIR} #sm13_1D_reco sm13_1D_refit sm13_1Debe_reco sm13_1Debe_refit sm13_2D_reco sm13_2D_refit sm13_2Debe_reco sm13_2Debe_refit

do

    cd cards_${dir}_2p7fb_CB/HCG/125
    mkdir ${dirTag}_${fs}

    text2workspace.py hzz4l_${fs}S_13TeV.txt -P HiggsAnalysis.CombinedLimit.PhysicsModel:floatingHiggsMass --PO higgsMassRange=115,135 --PO=muAsPOI -o ${dirTag}_${fs}/FloatMass_comb_hzz2D_${dir}_${fs}.root

    cd ${dirTag}_${fs}

    counter=0

    while [ $counter -le 50 ]
    do

          SEED=`expr $counter - 1`
          combine -n ${dir} -M MultiDimFit FloatMass_comb_hzz2D_${dir}_${fs}.root -m 125.0 -P MH --floatOtherPOIs=1 --expectSignal=1 -t -1 --X-rtd TMCSO_PseudoAsimov=1000 --X-rtd  TMCSO_AdaptivePseudoAsimov=0 --saveWorkspace --saveToys --robustFit 1 --stepSize 0.01 --minimizerTolerance 0.01 -s $SEED --algo=singles --cl=0.68 -v 9 > ${curdir}/savedLog/${dirTag}/sm13_${dir}_${fs}_${counter}.log 2>&1

          echo "run " $counter "th times"
          ((counter++))
    done

    cd $curdir

done

