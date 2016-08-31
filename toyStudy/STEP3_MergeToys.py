from ROOT import *
from array import array
from math import *
from decimal import *

def mergeToys(indir,outdir,m4ltype,fs,proc):

  # Load some libraries                                 
  gSystem.AddIncludePath("-I$CMSSW_BASE/src/ ")
  #gSystem.Load("$CMSSW_BASE/lib/slc6_amd64_gcc530/libHiggsAnalysisCombinedLimit.so")
  gSystem.Load("/scratch/osg/dsperka/Run2/HZZ4l/CMSSW_8_0_10/lib/slc6_amd64_gcc530/libHiggsAnalysisCombinedLimit.so")
  gSystem.AddIncludePath("-I$ROOFITSYS/include")
  gSystem.AddIncludePath("-Iinclude/")

  f_workspace = TFile(indir+"/hzz4l_"+fs+"S_13TeV_"+m4ltype+".input.root");
  ws = f_workspace.Get("w").Clone()
  
  f_sig = TFile(indir+"/toys_"+(m4ltype.split('_'))[1]+"_"+fs+"_mH_125_"+fs+"Skim.root",'READ')
  f_qqzz = TFile(indir+"/toys_"+(m4ltype.split('_'))[1]+"_"+fs+"_qqZZ_LowMassSkim_"+fs+"Skim.root",'READ')
  f_zx = TFile(indir+"/toys_"+(m4ltype.split('_'))[1]+"_"+fs+"_Data_2016_4lLowMassSkim_"+fs+"Skim.root",'READ')

  ntoys_sig=0; ntoys_qqzz=0; ntoys_zx=0;
  for key in f_qqzz.GetListOfKeys():
    cl = gROOT.GetClass(key.GetClassName())
    if (not cl.InheritsFrom("RooDataSet")): continue;
    ntoys_qqzz+=1;     
  for key in f_zx.GetListOfKeys():
    cl = gROOT.GetClass(key.GetClassName())
    if (not cl.InheritsFrom("RooDataSet")): continue;
    ntoys_zx+=1;
  for key in f_sig.GetListOfKeys():
    cl = gROOT.GetClass(key.GetClassName())
    if (not cl.InheritsFrom("RooDataSet")): continue;
    ntoys_sig+=1

  toyn_qqzz=0; toyn_zx=0;
  ntotalave=0.0;

  if (proc=="sig" or proc=="all"):
    d_tot = f_sig.Get("toy_0") # normal
  if (proc=="QQZZ"):
    d_tot = f_qqzz.Get("toy_0") # for qqzz only
  if (proc=="ZX"):
    d_tot = f_zx.Get("toy_0") # for zx only

  for i in range(0,ntoys_sig):

    if (i%1000==0): print fs,m4ltype,i,"/",ntoys_sig

    d_sig = f_sig.Get("toy_"+str(i))
    d_qqzz = f_qqzz.Get("toy_"+str(toyn_qqzz))
    d_zx = f_zx.Get("toy_"+str(toyn_zx))
    
    ### NORMAL
    if (proc=="all"):
      if (i>0): d_tot.append(d_sig)
      d_tot.append(d_qqzz)         
      d_tot.append(d_zx)           
      d_sig.append(d_qqzz)
      d_sig.append(d_zx)
      getattr(ws,'import')(d_sig);
      ntotalave+=float(d_sig.sumEntries())

    ### Sig Only
    if (proc=="sig"):
      if (i>0): d_tot.append(d_sig)
      getattr(ws,'import')(d_sig);
      ntotalave+=float(d_sig.sumEntries())
    
    ### QQZZ ONLY
    if (proc=="QQZZ"):
      if (i>0): d_tot.append(d_qqzz)
      getattr(ws,'import')(d_qqzz);
      ntotalave+=float(d_qqzz.sumEntries())

    ### ZX ONLY
    if (proc=="ZX"):
      if (i>0): d_tot.append(d_zx)
      getattr(ws,'import')(d_zx);
      ntotalave+=float(d_zx.sumEntries())

    ### Bkg ONLY
    #if (i>0): d_tot.append(d_qqzz)
    #d_tot.append(d_zx)
    #d_qqzz.append(d_zx)
    #getattr(ws,'import')(d_qqzz);
    #ntotalave+=float(d_qqzz.sumEntries())

    toyn_qqzz+=1; toyn_zx+=1;
    if (toyn_qqzz>(ntoys_qqzz-1)): 
      toyn_qqzz=0
      #if (proc=="QQZZ"): break
    if (toyn_zx>(ntoys_zx-1)): 
      toyn_zx=0
      #if (proc=="ZX"): break
  
  d_tot.SetName("toy_total")
  d_tot.SetTitle("toy_total")
  getattr(ws,'import')(d_tot);

  d_tot_clone = d_tot.Clone("d_tot_clone")

  if (proc=="sig" or proc=="all"):
    wFunc = RooRealVar("weight","event weight",float(1.0/float(ntoys_sig))) # normal
  if (proc=="QQZZ"):
    wFunc = RooRealVar("weight","event weight",float(1.0/float(ntoys_qqzz))) # qqzz only
  if (proc=="ZX"):
    wFunc = RooRealVar("weight","event weight",float(1.0/float(ntoys_zx))) # zx only

  weight = d_tot_clone.addColumn(wFunc)
  d_tot_w = RooDataSet("toy_total","toy_total",d_tot_clone,d_tot_clone.get(),"",weight.GetName())
  d_tot_w.SetName("toy_total_w")
  d_tot_w.SetTitle("toy_total_w")
  getattr(ws,'import')(d_tot_w);

  if (proc=="all"):
    ws.writeToFile(outdir+"/hzz4l_"+fs+"S_13TeV_"+m4ltype+"_withToys.input.root");
  if (proc=="sig"):
    ws.writeToFile(outdir+"/hzz4l_"+fs+"S_13TeV_"+m4ltype+"_withSigToys.input.root");
  if (proc=="QQZZ"):
    ws.writeToFile(outdir+"/hzz4l_"+fs+"S_13TeV_"+m4ltype+"_withQQZZToys.input.root");
  if (proc=="ZX"):
    ws.writeToFile(outdir+"/hzz4l_"+fs+"S_13TeV_"+m4ltype+"_withZXToys.input.root");

  if (proc=="sig" or proc=="all"):
    print fs,"ntotalave",float(ntotalave)/float(ntoys_sig) # normal
  if (proc=="QQZZ"):
    print fs,"ntotalave",float(ntotalave)/float(ntoys_qqzz) # qqzz only
  if (proc=="ZX"):
    print fs,"ntotalave",float(ntotalave)/float(ntoys_zx) # zx only

  print fs,"ntotal weighted:",d_tot_w.sumEntries()

for fs in ["4mu","4e","2e2mu"]:
    for m4ltype in ["1D_reco", "1D_refit", "1Debe_reco", "1Debe_refit"]:
#        mergeToys("../Toys_BkgSmear1pct4mu_FixShape_FixZX",m4ltype,fs,"all")
        mergeToys("../STEP2_Toys_BkgSmear1pct4mu_FixShape_FixZX","../STEP3_mergedToys_BkgSmear1pct4mu_FixShape_FixZX", m4ltype,fs,"all")

#mergeToys("../Toys_BkgSmear1pct4mu_FixShape_FixZX","reco","4mu","all")
#mergeToys("../Toys_BkgSmear1pct4mu_FixShape_FixZX","reco","4e","all")
#mergeToys("../Toys_BkgSmear1pct4mu_FixShape_FixZX","reco","2e2mu","all")
#mergeToys("../Toys_BkgSmear1pct4mu_FixShape_FixZX","refit","4mu","all")
#mergeToys("../Toys_BkgSmear1pct4mu_FixShape_FixZX","refit","4e","all")
#mergeToys("../Toys_BkgSmear1pct4mu_FixShape_FixZX","refit","2e2mu","all")

#mergeToys("Toys1D_BkgSmear1pct4mu_FixShape_FixZX","reco","4mu","all")
#mergeToys("Toys1D_BkgSmear1pct4mu_FixShape_FixZX","reco","4e","all")
#mergeToys("Toys1D_BkgSmear1pct4mu_FixShape_FixZX","reco","2e2mu","all")
#mergeToys("Toys1D_BkgSmear1pct4mu_FixShape_FixZX","refit","4mu","all")
#mergeToys("Toys1D_BkgSmear1pct4mu_FixShape_FixZX","refit","4e","all")
#mergeToys("Toys1D_BkgSmear1pct4mu_FixShape_FixZX","refit","2e2mu","all")

#mergeToys("Toys2D_BkgSmear1pct4mu_FixShape","reco","4mu","QQZZ")
#mergeToys("Toys2D_BkgSmear1pct4mu_FixShape","reco","4e","QQZZ")
#mergeToys("Toys2D_BkgSmear1pct4mu_FixShape","reco","2e2mu","QQZZ")
#mergeToys("Toys2D_BkgSmear1pct4mu_FixShape","refit","4mu","QQZZ")
#mergeToys("Toys2D_BkgSmear1pct4mu_FixShape","refit","4e","QQZZ")
#mergzxseToys("Toys2D_BkgSmear1pct4mu_FixShape","refit","2e2mu","QQZZ")

#mergeToys("Toys2D_BkgSmear1pct4mu_FixShape","reco","4mu","ZX")
#mergeToys("Toys2D_BkgSmear1pct4mu_FixShape","reco","4e","ZX")
#mergeToys("Toys2D_BkgSmear1pct4mu_FixShape","reco","2e2mu","ZX")
#mergeToys("Toys2D_BkgSmear1pct4mu_FixShape","refit","4mu","ZX")
#mergeToys("Toys2D_BkgSmear1pct4mu_FixShape","refit","4e","ZX")
#mergeToys("Toys2D_BkgSmear1pct4mu_FixShape","refit","2e2mu","ZX")

#mergeToys("Toys2D_NoBkgSmearRaw_FixShape","reco","4mu","QQZZ")
#mergeToys("Toys2D_NoBkgSmearRaw_FixShape","reco","4e","QQZZ")
#mergeToys("Toys2D_NoBkgSmearRaw_FixShape","reco","2e2mu","QQZZ")
#mergeToys("Toys2D_NoBkgSmearRaw_FixShape","refit","4mu","QQZZ")
#mergeToys("Toys2D_NoBkgSmearRaw_FixShape","refit","4e","QQZZ")
#mergeToys("Toys2D_NoBkgSmearRaw_FixShape","refit","2e2mu","QQZZ")

#mergeToys("Toys2D_NoBkgSmearRaw_FixShape","reco","4mu","ZX")
#mergeToys("Toys2D_NoBkgSmearRaw_FixShape","reco","4e","ZX")
#mergeToys("Toys2D_NoBkgSmearRaw_FixShape","reco","2e2mu","ZX")
#mergeToys("Toys2D_NoBkgSmearRaw_FixShape","refit","4mu","ZX")
#mergeToys("Toys2D_NoBkgSmearRaw_FixShape","refit","4e","ZX")
#mergeToys("Toys2D_NoBkgSmearRaw_FixShape","refit","2e2mu","ZX")

