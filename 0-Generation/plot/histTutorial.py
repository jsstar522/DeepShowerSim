#-*- coding: utf-8 -*-

import ROOT
import numpy as np
import matplotlib.pyplot as plt

## TObject의 TH는 히스토그램을 사용하기 위한 기본적인 클래스다
## TH[차원][데이터타입](히스토그램 이름, discription;x축이름;y축이름, x축 빈개수, x축 범위 시작, x축 범위 끝)


##h = ROOT.TH1F("energy deposit", "energy deposit", 55, 0, 55)
##c1 = ROOT.TCanvas('c1', 'hello', 200, 10, 700, 500)
#3c1.cd(1)
##h.Draw()

myFile = ROOT.TFile('../rootData/test2.root', 'read')
myTree = myFile.crystal

for entry in myTree:
  readout = np.array(entry.energy_deposit).reshape(9,9)
  print(readout)



## root_file = ROOT.TFile.Open("../rootData/test2.root", "READ")
## tree = root_file.crystal

## h = ROOT.TH1F("energy deposit", "energy deposit", 55, 0, 55)

#for entry in tree:
#  readout = np.array(entry.energy_deposit)
#  ## num_event
#  print(entry)
#  h.Fill(readout.sum())
#  
#h.Draw("hist")
