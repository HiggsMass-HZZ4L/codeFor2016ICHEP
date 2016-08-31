//////////////////////////////////////////////////////////////////////////
//
// 'MULTIDIMENSIONAL MODELS' RooFit tutorial macro #308
// 
// Making 2/3 dimensional plots of p.d.f.s and datasets
//
//
//
// 07/2008 - Wouter Verkerke 
// 
/////////////////////////////////////////////////////////////////////////

#ifndef __CINT__
#include "RooGlobalFunc.h"
#endif
#include "RooRealVar.h"
#include "RooDataSet.h"
#include "RooConstVar.h"
#include "RooGaussian.h"
#include "RooProdPdf.h"
#include "TCanvas.h"
#include "TAxis.h"
#include "TH1F.h"
#include "RooPlot.h"
#include "TRandom.h"
#include <iostream>

using namespace RooFit ;


void createToys(TString filename, int fs, float nexp, int isZX=0, int refit=0, TString outputDIR="")
{


    TH1F h_weightedMass("h_weightedMass","weighted;mass;", 100, 110,140);
    TH1F h_noweightMass("h_noweightMass","noweight;mass;", 100, 110,140);
    TH1F h_sumtoysMass("h_sumtoysMass","sumuptoys;mass;", 100, 110,140);
    TH1F h_sumtoysMassW("h_sumtoysMassW","sumuptoysW;mass;", 100, 110,140);
    
    TFile input("../inputTrees/"+filename,"READ");
    TTree* tree;
    tree = (TTree*)input.Get("passedEvents");
    if (!tree) tree = (TTree*)input.Get("Ana/passedEvents");

    TString s_fs;
    if (fs==1) s_fs = "4mu";
    if (fs==2) s_fs = "4e";
    if (fs>=3) s_fs = "2e2mu";

    TString outfilename;
    if (refit) {
        outfilename = outputDIR + "/toys_refit_"+s_fs+"_"+filename;
    } else {
        outfilename = outputDIR + "/toys_reco_"+s_fs+"_"+filename;
    }
    TFile outfile(outfilename,"RECREATE");

    bool passedZ4lSelection, passedZXCRSelection;
    int nZXCRFailedLeptons;
    float mass4l, mass4lErr, mass4lREFIT, mass4lErrREFIT;
    int idL1, idL3;

    tree->SetBranchStatus("*",0);

    tree->SetBranchStatus("passedZ4lSelection",1);
    tree->SetBranchStatus("passedZXCRSelection",1);
    tree->SetBranchStatus("nZXCRFailedLeptons",1);
    tree->SetBranchStatus("idL1",1);
    tree->SetBranchStatus("idL3",1);
    tree->SetBranchStatus("mass4l",1);
    tree->SetBranchStatus("mass4lErr",1);
    tree->SetBranchStatus("mass4lREFIT",1);
    tree->SetBranchStatus("mass4lErrREFIT",1);

    tree->SetBranchAddress("passedZ4lSelection",&passedZ4lSelection);
    tree->SetBranchAddress("passedZXCRSelection",&passedZXCRSelection);
    tree->SetBranchAddress("nZXCRFailedLeptons",&nZXCRFailedLeptons);
    tree->SetBranchAddress("idL1",&idL1);
    tree->SetBranchAddress("idL3",&idL3);
    tree->SetBranchAddress("mass4l",&mass4l);
    tree->SetBranchAddress("mass4lErr",&mass4lErr);
    tree->SetBranchAddress("mass4lREFIT",&mass4lREFIT);
    tree->SetBranchAddress("mass4lErrREFIT",&mass4lErrREFIT);

    TRandom3 rand1;
    rand1.SetSeed(123457);
 
    TRandom3 rand2;
    rand2.SetSeed(754321);

    TRandom3 rand3;
    rand3.SetSeed(321754);

    int toyn=0;
    Long64_t nevents = tree->GetEntriesFast();

    RooRealVar CMS_zz4l_mass("CMS_zz4l_mass","CMS_zz4l_mass",105.0,140.0);
    RooRealVar CMS_zz4l_massErr("CMS_zz4l_massErr","CMS_zz4l_massErr",0.0,100.0);

    RooDataSet* empty_toy = new RooDataSet("empty_toy","empty_toy",RooArgSet(CMS_zz4l_mass,CMS_zz4l_massErr));
    RooDataSet* toy = new RooDataSet("toy","toy",RooArgSet(CMS_zz4l_mass,CMS_zz4l_massErr));
    //RooDataSet* empty_toy = new RooDataSet("empty_toy","empty_toy",RooArgSet(CMS_zz4l_mass));
    //RooDataSet* toy = new RooDataSet("toy","toy",RooArgSet(CMS_zz4l_mass));

    float npassave = 0;

    while(1) {
    
        if (toyn%100==0) cout<<"toy n"<<toyn<<endl;

        if (toyn==10000) break;

        toy = (RooDataSet*)empty_toy->Clone();

        int nexp_poisson = rand1.Poisson(nexp);

        if (nexp_poisson==0) { 
            TString s_toy = std::to_string(toyn);
            toy->SetName("toy_"+s_toy);
            toy->SetTitle("toy_"+s_toy);
            npassave+=toy->sumEntries();
            toy->Write();
            delete toy;
            toyn+=1;
            npass=0;
            continue;
        } else {

            int npass=0;
        
            while (npass<nexp_poisson) {

                int evt = rand2.Integer(nevents);

                tree->GetEntry(evt);

                if (!isZX && !passedZ4lSelection) continue;
                if (isZX && !(passedZXCRSelection && nZXCRFailedLeptons==2)) continue;

                float smearmass; float smearmasserr; float masserr_orig;
                if (!refit) {
                    smearmass = std::max(0.0,mass4l+rand3.Gaus(0.0,0.05*mass4l));
                    float errsmear=0.05;
                    if (fs==1 && !isZX) errsmear=0.01;
                    smearmasserr = std::max(0.0,mass4lErr+rand3.Gaus(0.0,errsmear*mass4lErr));
                    //smearmass = mass4l;
                    //smearmasserr = mass4lErr;
                } else {
                    smearmass = std::max(0.0,mass4lREFIT+rand3.Gaus(0.0,0.05*mass4lREFIT));
                    float errsmear=0.05;
                    if (fs==1 && !isZX) errsmear=0.01;
                    smearmasserr = std::max(0.0,mass4lErrREFIT+rand3.Gaus(0.0,errsmear*mass4lErrREFIT));
                    //smearmass = mass4lREFIT;
                    //smearmasserr = mass4lErrREFIT;
                }

                //cout<<"mass4l: "<<mass4l<<" smearmass: "<<smearmass<<endl;
                if (!(smearmass>105.0 && smearmass<140.0)) continue;
                if ( (smearmasserr/smearmass)>0.1) continue;

                bool correctFS=false;
                if (fs==1 && abs(idL1)==13 && abs(idL3)==13) correctFS=true;
                if (fs==2 && abs(idL1)==11 && abs(idL3)==11) correctFS=true;
                if (fs>=3 && abs(idL1)!=abs(idL3)) correctFS=true;
                if (!correctFS) continue;
                
                npass+=1;
                if (refit) {
                    CMS_zz4l_mass=smearmass; 
                    CMS_zz4l_massErr=(smearmasserr/smearmass);
                }
                else {
                    CMS_zz4l_mass=smearmass; 
                    CMS_zz4l_massErr=smearmasserr/smearmass;
                    //cout<<"toy "<<toyn<<" mass: "<<CMS_zz4l_mass.getVal()<<" massErr: "<<CMS_zz4l_massErr.getVal()<<endl;
                }
                toy->add(RooArgSet(CMS_zz4l_mass,CMS_zz4l_massErr));
                //toy->add(RooArgSet(CMS_zz4l_mass));
            }
             
            TString s_toy = std::to_string(toyn);
            toy->SetName("toy_"+s_toy);
            toy->SetTitle("toy_"+s_toy);
            npassave+=toy->sumEntries();
            toy->Write();
            delete toy;
            toyn+=1;
            continue;
        }

    }

    npassave/=toyn;
    cout<<"ntoys: "<<toyn<<" ave: "<<npassave<<endl;
    
}
