from subprocess import call
import sys
#root -l -q -b createToys.C\(\"mH_125_4muSkim.root\",1,y_mH125_4mu,0,0,\"$outputDIR\"\) >& reco_ggH_4mu.log &

def AddArguments(argList):
    argString = ''
    for arg in argList:
        argString += arg
        if not argList.index(arg) == len(argList)-1:
           argString += ','
    return argString

outputDIR = '\\"../STEP2_Toys_BkgSmear1pct4mu_FixShape_FixZX\\"'

fsS = {"4mu":'1', "4e":'2', "2e2mu":'3'}
inputFileBase = {"mH125": "mH_125_", "irrBkg":"qqZZ_LowMassSkim_", "redBkg":"Data_2016_4lLowMassSkim_"}
isZX = {"mH125":'0', "irrBkg":'0', "redBkg":'1'}
doSmear = {"mH125":'0', "irrBkg":'1', "redBkg":'1'}
processes = ["mH125", "irrBkg", "redBkg"]

for fs in ["4mu","4e","2e2mu"]:
    for process in processes:
        for isREFIT in ['0','1']:

            fsIndex = fsS[fs]
            exp = [line.strip() for line in open("../STEP2_expectedYields/yields_"+fs+".txt", 'r')][processes.index(process)]
            iszx = isZX[process]
            dosmear = doSmear[process]

            inputRoot = '\\"'+inputFileBase[process]+fs+'Skim.root\\"'

            if isREFIT == '1': 
               tag = "refit_" + process + "_" + fs 
            else: 
               tag = "reco_" + process + "_" + fs

            cmd = "root -l -q -b createToys.C\("+AddArguments([inputRoot, str(fsIndex), exp, iszx, isREFIT, dosmear, outputDIR])+"\) >& ../logs/"+tag+".log& "
            print cmd
            call(cmd, shell=True)

#        isREFIT = str(1)
#        tag = "refit_" + process + "_" + fs
#        cmd = "root -l -q -b createToys.C\("+AddArguments([inputRoot, str(fsIndex), exp, iszx, isREFIT, dosmear, outputDIR])+"\) >& ../logs/"+tag+".log& "
#        print cmd
#        call(cmd, shell=True)

