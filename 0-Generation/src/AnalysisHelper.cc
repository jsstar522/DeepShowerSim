// ********************************************************************
// * License and Disclaimer                                           *
// *                                                                  *
// * The  Geant4 software  is  copyright of the Copyright Holders  of *
// * the Geant4 Collaboration.  It is provided  under  the terms  and *
// * conditions of the Geant4 Software License,  included in the file *
// * LICENSE and available at  http://cern.ch/geant4/license .  These *
// * include a list of copyright holders.                             *
// *                                                                  *
// * Neither the authors of this software system, nor their employing *
// * institutes,nor the agencies providing financial support for this *
// * work  make  any representation or  warranty, express or implied, *
// * regarding  this  software system or assume any liability for its *
// * use.  Please see the license in the file  LICENSE  and URL above *
// * for the full disclaimer and the limitation of liability.         *
// *                                                                  *
// * This  code  implementation is the result of  the  scientific and *
// * technical work of the GEANT4 collaboration.                      *
// * By using,  copying,  modifying or  distributing the software (or *
// * any work based  on the software)  you  agree  to acknowledge its *
// * use  in  resulting  scientific  publications,  and indicate your *
// * acceptance of all terms of the Geant4 Software license.          *
// ********************************************************************

// User Classes
#include "AnalysisHelper.hh"

// G4 Classes
#include "G4Run.hh"
#include "G4Event.hh"
#include "G4Step.hh"

// 
#include "globals.hh"
#include "G4SystemOfUnits.hh"

// ROOT Classes
#include "TFile.h"
#include "TTree.h"
#include "TString.h"
#include "TSystem.h"
#include "TDatime.h"

//
#include <sstream>

AnalysisHelper* AnalysisHelper::singleton = nullptr;


AnalysisHelper* AnalysisHelper::GetInstance() {
  if ( singleton == nullptr ) {
    static AnalysisHelper helper;
    singleton = &helper;
  }
  return singleton;
}


AnalysisHelper::AnalysisHelper() {

}


AnalysisHelper::~AnalysisHelper() {}


void AnalysisHelper::PrepareRun(const char* out_path, const char* tree_name) {
  root_file_ = TFile::Open(out_path, "RECREATE");

  tree_ = new TTree(tree_name, tree_name);
  tree_->SetDirectory(root_file_);
  MakeBranch();
  ResetBranch();
}

void AnalysisHelper::DoBeginOfRunAction(const G4Run* /*run*/) {
  return ;
}


void AnalysisHelper::DoEndOfRunAction(const G4Run* /*run*/) {
  PrintRunSummary();

  root_file_->Write();
  // FIXME
  root_file_->Close();

  delete root_file_;
  return ;
}


void AnalysisHelper::DoBeginOfEventAction(const G4Event* /*event*/) {
  ResetBranch();
  return ;
}


void AnalysisHelper::DoEndOfEventAction(const G4Event* event) {
  G4PrimaryVertex* primary_vertex = event->GetPrimaryVertex();
  G4PrimaryParticle* primary_particle = primary_vertex->GetPrimary();

  // Branch
  // MeV to GeV
  total_energy_ = primary_particle->GetKineticEnergy() / GeV;

  tree_->Fill();
  return ;
}


void AnalysisHelper::DoSteppingAction(const G4Step* step) {
  G4double energy_deposit = step->GetTotalEnergyDeposit();
  G4StepPoint* pre_point = step->GetPreStepPoint();
  G4int index = pre_point->GetPhysicalVolume()->GetCopyNo();

  // index = volumeId (0~80 cells)
  energy_deposit_[index] += energy_deposit / GeV;

}

void AnalysisHelper::MakeBranch() {
  // Start Make Branch
  // int total_cell = 81;
  // for(G4int i = 0; i < total_cell; ++i) {
  //  tree_->Branch(Form("crystal_%i", i), &energy_deposit_[i], Form("crystal_%i/D",i));
  // }
  tree_->Branch("energy_deposit", &energy_deposit_, "energy_deposit[8100]/D");
  tree_->Branch("total_energy",   &total_energy_, "total_energy/D");
}

void AnalysisHelper::ResetBranch() { 
  for(G4int i = 0; i < kNumCrystals; i++) {
    energy_deposit_[i] = 0.0;
  }
  total_energy_ = 0.0;
  return ;
}

void AnalysisHelper::PrintRunSummary() {
  tree_->Print();
}
