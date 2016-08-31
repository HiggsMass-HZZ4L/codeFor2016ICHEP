import sys, os, pwd, commands
import optparse

#define function for parsing options                                                                                                                                        
def parseOptions():
    global observalbesTags, modelTags, runAllSteps

    usage = ('usage: %prog [options]\n'
             + '%prog -h for help')
    parser = optparse.OptionParser(usage)
    
    # input options
    parser.add_option('-t', '--type', dest='TYPE', type='string',default='reco', help='reco or refit')
    parser.add_option('-j', '--job', dest='JOB', type=int, default=0, help='job number')
    parser.add_option('-f', '--firsttoy', dest='FIRST', type=int, default=0, help='first toy')
    parser.add_option('-l', '--lasttoy', dest='LAST', type=int, default=10, help='last toy')

    # store options and arguments as global variables
    global opt, args
    (opt, args) = parser.parse_args()

def processCmd(cmd, quite = 0):
  #    print cmd                                                                                                                                                          
  status, output = commands.getstatusoutput(cmd)
  if (status !=0 and not quite):
    print 'Error in processing command:\n   ['+cmd+']'
    print 'Output:\n   ['+output+'] \n'
  return output

# parse the arguments and options
global opt, args
parseOptions()

m4ltype=opt.TYPE
first=opt.FIRST
last=opt.LAST


results = {}
for i in range(first,last+1):

  cmd = "text2workspace.py hzz4l_allS_13TeV.txt -P HiggsAnalysis.CombinedLimit.PhysicsModel:floatingHiggsMass --PO higgsMassRange=115,135 --PO=muAsPOI -D toy_"+str(i)+" -o FloatMass_comb_hzz2D_1Debe_"+m4ltype+"_toy_"+str(i)+".root"
  #cmd = "text2workspace.py hzz4l_allS_13TeV_NoXH.txt -P HiggsAnalysis.CombinedLimit.PhysicsModel:floatingHiggsMass --PO higgsMassRange=115,135 --PO=muAsPOI -D toy_"+str(i)+" -o FloatMass_comb_hzz2D_1Debe_"+m4ltype+"_toy_"+str(i)+".root"
  #print cmd
  output = processCmd(cmd)
  cmd = "combine -n 1Debe_"+m4ltype+"_toy"+str(i)+" -M MultiDimFit FloatMass_comb_hzz2D_1Debe_"+m4ltype+"_toy_"+str(i)+".root -D toy_"+str(i)+" -m 125.0 -P MH --floatOtherPOIs=1 -v 9 --robustFit 1 --stepSize 0.01 --minimizerTolerance 0.01 --algo=singles --cl=0.68"
  #cmd = "combine -n 1Debe_"+m4ltype+"_toy"+str(i)+" -M MultiDimFit FloatMass_comb_hzz2D_1Debe_"+m4ltype+"_toy_"+str(i)+".root -D toy_"+str(i)+" -m 125.0 -P MH --floatOtherPOIs=1 -v 9 -S 0"
  #cmd = "combine -n 1Debe_"+m4ltype+"_toy"+str(i)+" -M MultiDimFit FloatMass_comb_hzz2D_1Debe_"+m4ltype+"_toy_"+str(i)+".root -D toy_"+str(i)+" -m 125.0 -P r --floatOtherPOIs=0 -v 9"
  #print cmd
  output = processCmd(cmd)


  #cmd = "text2workspace.py hzz4l_4muS_13TeV.txt -P HiggsAnalysis.CombinedLimit.PhysicsModel:floatingHiggsMass --PO higgsMassRange=115,135 --PO=muAsPOI -D toy_"+str(i)+" -o FloatMass_4mu_hzz2D_1Debe_"+m4ltype+"_toy_"+str(i)+".root"
  #output = processCmd(cmd)
  #cmd = "combine -n 4mu_1Debe_"+m4ltype+"_toy"+str(i)+" -M MultiDimFit FloatMass_4mu_hzz2D_1Debe_"+m4ltype+"_toy_"+str(i)+".root -D toy_"+str(i)+" -m 125.0 -P MH --floatOtherPOIs=1 --robustFit 1 -v 9"
  #output = processCmd(cmd)

  if (len(output.split("   MH :"))<2): continue
  #if (len(output.split("   r :"))<2): continue

  massressult =  output.split("   MH :")[1]
  mass = massressult.split()[0].replace('+','')
  #mass =125.0
  uncdn = massressult.split()[1].split('/')[0].replace('-','') 
  uncup = massressult.split()[1].split('/')[1].replace('+','')
#  uncdn=0.0
#  uncup=0.0

  if ("CMS_zz4l_mean_e_sig\t  = " in output):
    meane = output.split("CMS_zz4l_mean_e_sig\t  = ")[1].split(" +")[0].replace(" ","")
    sigmae = output.split("CMS_zz4l_sigma_e_sig\t  = ")[1].split(" +")[0].replace(" ","")
  else:
    meane = 0.0
    sigmae = 0.0
  if ("CMS_zz4l_mean_m_sig\t  = " in output):
    meanm = output.split("CMS_zz4l_mean_m_sig\t  = ")[1].split(" +")[0].replace(" ","")
    sigmam = output.split("CMS_zz4l_sigma_m_sig\t  = ")[1].split(" +")[0].replace(" ","")
  else:
    meanm = 0.0
    sigmam = 0.0
  if ("RooRealVar::r = " in output):
    r = output.split("RooRealVar::r = ")[1].split(" +")[0].replace(" ","")
  else:
    r = 0.0
    sigmam = 0.0

  print i,mass,'+',uncup,'-',uncdn
  print meane,meanm,sigmae,sigmam,r

  results[i] = {"mass":float(mass),"uncdn":float(uncdn),"uncup":float(uncup), \
                "meane":float(meane),"meanm":float(meanm),"sigmae":float(sigmae),"sigmam":float(sigmam),"r":float(r)}

  output = processCmd("rm FloatMass_*_hzz2D_1Debe_"+m4ltype+"_toy_"+str(i)+".root")
  output = processCmd("rm higgsCombine*1Debe_"+m4ltype+"_toy"+str(i)+".MultiDimFit.mH125.root")

with open('results/results_toys_'+str(opt.JOB)+'.py','w') as f:
  f.write('results_toys = '+str(results)+'\n')

