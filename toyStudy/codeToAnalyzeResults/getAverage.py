import glob
from subprocess import call,Popen, PIPE
import numpy as np


def PrintMeanAndSigma(fs, dim, ebe, recorefit, uncer_up, uncer_down):

    mean = []
    sigmaLow = []
    sigmaHigh = []

    logs = glob.glob('savedLog/allMass/*' + dim + ebe + '_' + recorefit + '_' + fs + '*')

    tag = "MH :"

    for log in logs:

        proc = Popen('grep "' + str(tag) + '" ' + log, shell=True, stdout=PIPE)

        grepOut = (proc.communicate()[0]).split()

        if len(grepOut) == 0: continue

        m = float(grepOut[2])
        s = grepOut[3].split('/')
        sLow = float(s[0])
        sHigh = float(s[1])

        mean.append(m)
        sigmaLow.append(sLow/m)
        sigmaHigh.append(sHigh/m)

    
#    central=np.percentile(np.array(mean),50)
#    low=np.percentile(np.array(mean),16)
#    high=np.percentile(np.array(mean),84)
#    print central,"+",(high-central),"-",(central-low)


    prec = 3

    mean = round(np.average(mean), prec)
    up = round( np.average(sigmaHigh)*np.average(mean), prec )
    down = round( np.average(sigmaLow)*np.average(mean),prec )
    print fs+'_'+dim+ebe+'_'+recorefit+': '+str((len(logs)-1)*1000) + ' events, ', str(mean) + ' ' + str(down) + '/' + str(up)

    uncer_up.append(up)
    uncer_down.append(down)

def getGain(up, down, i, j):

    gainUp = 1-up[j]/up[i]
    gainDown = 1-down[j]/down[i]
    gain = 0.5*(gainUp+gainDown)

    return str(round(gain,3)*100) + '%'

for fs in ['all','4mu','4e','2e2mu']:

 up = []
 down = []

 PrintMeanAndSigma(fs, '1D', '', 'reco', up, down) #0

 PrintMeanAndSigma(fs, '1D', '', 'refit', up, down) #1
 PrintMeanAndSigma(fs, '1D', 'ebe', 'reco', up, down) #2
# PrintMeanAndSigma(fs, '2D', '', 'reco', up, down) #3

 PrintMeanAndSigma(fs, '1D', 'ebe', 'refit', up, down) #4
# PrintMeanAndSigma(fs, '2D', 'ebe', 'reco', up, down) #5
# PrintMeanAndSigma(fs, '2D', '', 'refit', up, down) #6

# PrintMeanAndSigma(fs, '2D', 'ebe', 'refit', up, down) #7

 print ''

 print 'from m4l to m4lREFIT: ', getGain(up, down, 0, 1)
 print 'from m4l to m4lEBE: ', getGain(up, down, 0, 2)
# print 'from m4l to m4lKD: ', getGain(up, down, 0, 3)
# print 'from m4lREFIT to m4lREFIT_KD: ', getGain(up, down, 1, 6)
# print 'from m4lREFIT to m4lREFIT_EBE: ', getGain(up, down, 1, 4)
# print 'from m4lEBE to m4lEBE_REFIT: ', getGain(up, down, 2, 4)
# print 'from m4lEBE to m4lEBE_KD: ', getGain(up, down, 2, 5)
# print 'from m4lREFIT_KD to m4lREFIT_KD_EBE: ', getGain(up, down, 6, 7)
# print 'from m4lREFIT_EBE to m4lREFIT_EBE_KD: ', getGain(up, down, 4, 7)
# print 'from m4lEBE_REFIT to m4lEBE_REFIT_KD: ', getGain(up, down, 4, 7)
# print 'from m4lEBE_KD to m4lEBE_KD_REFIT: ', getGain(up, down, 5, 7)

 print 'from m4l to m4lREFIT_EBE: ', getGain(up, down, 0, 3)
# print 'from m4l to m4lEBE: ', getGain(up, down, 0, 1)
# print 'from m4l to m4lKD: ', getGain(up, down, 0, 2)
# print 'from m4lEBE to m4lEBE_KD: ', getGain(up, down, 1, 3)

 print '================================================='









