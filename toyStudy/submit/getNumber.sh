for m4l_type in 1D_reco 1D_refit 1Debe_reco 1Debe_refit
do

    mean=`grep "+" workdir/*out | grep ${m4l_type} | awk -F " " {'print $2'} | awk '{ sum+=$1} END {print sum/NR}'`
    up=`grep "+" workdir/*out | grep ${m4l_type} | awk -F " " {'print $4'} | awk '{ sum+=$1} END {print sum/NR}'`
    down=`grep "+" workdir/*out | grep ${m4l_type} | awk -F " " {'print $6'} | awk '{ sum+=$1} END {print sum/NR}'`
    ntoy=`grep "+" workdir/*out | grep ${m4l_type} | awk -F " " {'print $6'} | awk '{ sum+=$1} END {print NR}'`

    echo ${m4l_type}": "${mean}" +"${up}"-"${down}" ("${ntoy}" toys)"

done
