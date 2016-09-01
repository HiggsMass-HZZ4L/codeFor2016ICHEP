from subprocess import call
import argparse

def ParseOption():

    parser = argparse.ArgumentParser(description='submit all')
    parser.add_argument('--index', dest='index', type=float)

    args = parser.parse_args()
    return args

args=ParseOption()

cats = ['sm13_1D_reco', 'sm13_1D_refit', 'sm13_1Debe_reco', 'sm13_1Debe_refit']#, 'sm13_2D_reco', 'sm13_2D_refit', 'sm13_2Debe_reco', 'sm13_2Debe_refit']
#cats = ['sm13_1D_reco', 'sm13_1Debe_reco', 'sm13_2D_reco', 'sm13_2Debe_reco']

fss = ['all']#, '4mu', '4e', '2e2mu']
ss = ['4mu', '4e', '2e2mu']

tag = 'allMass'
call('mkdir savedLog/' + tag, shell=True)

for cat in cats:
    for fs in fss:
        call('./runAsimov.sh ' + tag + ' ' + fs + ' ' + cat + ' &', shell=True) 

#for i in range(10):


#    index  = i+args.index*10
#    seed = int(22345 - index)

#    tmpRun1D = 'run1D_13TeV_v' + str(index)  +  '.sh'
#    print 'cp tmp_run1D_13TeV.sh ' + tmpRun1D
#    print 'sed -i "s/SEED/' + str(seed) + '/g" ' + tmpRun1D
#    print 'sed -i "s/TAG/' + str(index) + '/g" ' + tmpRun1D
#    print './' + tmpRun1D
#    print 'mv ' + tmpRun1D + ' savedScript'

#    tmpRun1D = 'run1D_13TeV_v' + str(index)  +  '.sh'
#    call('cp tmp_run1D_13TeV.sh ' + tmpRun1D, shell=True)
#    call('sed -i "s/SEED/' + str(seed) + '/g" ' + tmpRun1D, shell=True)
#    call('sed -i "s/TAG/' + str(index) + '/g" ' + tmpRun1D, shell=True)
#    call('./' + tmpRun1D, shell=True)
#    call('mv ' + tmpRun1D + ' savedScript', shell=True)

#    tmpRun1Debe = 'run1Debe_13TeV_v' + str(index)  +  '.sh'
#    call('cp tmp_run1Debe_13TeV.sh ' + tmpRun1Debe, shell=True)
#    call('sed -i "s/SEED/' + str(seed) + '/g" ' + tmpRun1Debe, shell=True)
#    call('sed -i "s/TAG/' + str(index) + '/g" ' + tmpRun1Debe, shell=True)
#    call('./' + tmpRun1Debe, shell=True)
#    call('mv ' + tmpRun1Debe + ' savedScript', shell=True)

