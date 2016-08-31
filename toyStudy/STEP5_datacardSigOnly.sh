for dir_l1 in ../STEP4_getMass_asimov/ ../STEP4_getMass_toy/
do
    for dir_l2 in 1D_reco 1D_refit 1Debe_reco 1Debe_refit 2D_reco 2D_refit 2Debe_reco 2Debe_refit
    do
        cd ${dir_l1}cards_sm13_${dir_l2}_2p7fb_CB/HCG/125
        mkdir results
        for fs in 4mu 4e 2e2mu
        do 
            sed -i "/observation/c\observation -1" hzz4l_${fs}S_13TeV.txt
            yields=`grep "rate" hzz4l_${fs}S_13TeV.txt | awk -F " " '$7=$8=$9="0.0000000036"'`
            echo ${yields}
            sed -i "s/^rate.*/$yields/g" hzz4l_${fs}S_13TeV.txt
            combineCards.py hzz4l_13TeV_4mu=hzz4l_4muS_13TeV.txt hzz4l_13TeV_4e=hzz4l_4eS_13TeV.txt hzz4l_13TeV_2e2mu=hzz4l_2e2muS_13TeV.txt  > hzz4l_allS_13TeV.txt
        done
        cd -
    done
done
