import glob, sys
import numpy
from ROOT import *

gStyle.SetOptTitle(0)
gStyle.SetOptStat(2210)
gStyle.SetOptFit(1)

var = "mass"

sys.path.append('./results')
results = glob.glob("results/results_toys_*.py")

if (var=="mass"): hist = TH1D('hist','hist',100,115.0,135.0)
if (var=="r"): hist = TH1D('hist','hist',100,0.0,3.0)
else: hist = TH1D('hist','hist',80,-4.0,4.0)
hist.SetLineColor(4)
hist.SetMarkerColor(4)
hist.SetMarkerSize(1.2)
hist.SetMarkerStyle(20)

values=[]
for result in results:
  _temp = __import__(result.split('/')[1].replace('.py',''), globals(), locals(), -1)
  results_toys = _temp.results_toys
  for toy in results_toys:
    if (not var in results_toys[toy]): continue
    hist.Fill(results_toys[toy][var])
    values.append(results_toys[toy][var])

central=numpy.percentile(numpy.array(values),50)
low=numpy.percentile(numpy.array(values),16)
high=numpy.percentile(numpy.array(values),84)
print central,"+",(high-central),"-",(central-low)
#print "histo mean: ",hist.GetMean(),high,low

c1 = TCanvas("c1","c1",800,800)
c1.SetTopMargin(0.06)
c1.SetRightMargin(0.06)
c1.SetLogy()
c1.cd()
hist.GetXaxis().SetTitle("measured "+var)
hist.GetYaxis().SetTitle("Frequency")
hist.Draw("ep")
#f1 = TF1("f1","gaus",115.0,135.0)
#f1.SetParameter(0,hist.Integral()/sqrt(2*TMath.Pi()))
#f1.SetParameter(1,125.0)
#f1.SetParameter(2,0.9)
#hist.Fit("f1","R0")
#f1.Draw("same")
gPad.Update()
st = hist.FindObject("stats")
st.SetX1NDC(0.6)
st.SetY1NDC(0.6)
st.SetX2NDC(0.9)
st.SetY2NDC(0.9)

latex2 = TLatex()
latex2.SetNDC()
latex2.SetTextSize(0.7*c1.GetTopMargin())
latex2.SetTextFont(42)
latex2.SetTextAlign(31) # align right                                                                                             
latex2.DrawLatex(0.92, 0.95,"10.0 fb^{-1} (13 TeV)")
latex2.SetTextSize(0.8*c1.GetTopMargin())
latex2.SetTextFont(62)
latex2.SetTextAlign(11) # align right                                                                                             
latex2.DrawLatex(0.13, 0.95, "CMS")
latex2.SetTextSize(0.7*c1.GetTopMargin())
latex2.SetTextFont(52)
latex2.SetTextAlign(11)
latex2.DrawLatex(0.24, 0.95, "Preliminary")

c1.SaveAs("toys_reco_"+var+".pdf")
