from ROOT import *
import numpy as np

#myFile = TFile('../rootData/uniform50GeV_2.root', 'read')
myFile = TFile('../rootData/uniform50GeV_0.1m.root', 'read')
myTree = myFile.Get('crystal')

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

#######################################################################################

def draw_plot(tree):
  readout_total = []
  for entry in tree:
	for value in entry.energy_deposit:
	  readout_total.append(value)

  plt.figure(figsize=(10,10))
  bins = np.linspace(30, 50, 100)
  hist = plt.hist(readout_total, bins=bins, histtype='step', label='$e^+$ 10,000 events', alpha=0.8, linewidth=3, color='navy')
  plt.xlabel('energy_deposit(GeV)')
  plt.legend(loc='upper right', fontsize=15)
  plt.grid(linestyle='--')
  plt.show()

##draw_plot(myTree)

#######################################################################################

def plot_image(tree, num_img):
  i = 0
  ##fig = plt.figure(figsize=(8,8))
  for entry in tree:
	i = i + 1
	fig = plt.figure(figsize=(8,8))
	im = plt.imshow(np.array(entry.energy_deposit).reshape(9,9), aspect=float(9)/9, interpolation='nearest', norm=LogNorm(None, None))
	cbar = plt.colorbar(fraction=0.0455)
	cbar.set_label(r'Energy (MeV)', y=0.83)
	cbar.ax.tick_params()
	plt.show()
	if i == num_img:
	  return 0

plot_image(myTree, 20)

#######################################################################################
#######################################################################################

def get_nxn(readout, n):
  error = bool(n%2 == 0)
  if error:
	raise TypeError("Type wrong n of n x n")

  center_x = readout.shape[0]/2
  center_y = readout.shape[1]/2
  return readout[center_x-(n/2):center_x+(n/2)+1, center_y-(n/2):center_y+(n/2)+1]


energy_list_3x3 = []
energy_list_5x5 = []

for entry in myTree:
  readout = np.array(entry.energy_deposit).reshape(9,9)
  reco_energy_3x3 = get_nxn(readout, 3).sum()
  reco_energy_5x5 = get_nxn(readout, 5).sum()
  energy_list_3x3.append(reco_energy_3x3)
  energy_list_5x5.append(reco_energy_5x5)

##  print "------------readout---------------"
##  print readout
##  print "------------5x5---------------"
##  print get_nxn(readout,5)
##  print "------------3x3---------------"
##  print get_nxn(readout,3)
##  print "--------------------------------------------------"


#####################################nxn plot###########################################

def draw_nxn_plot(energy_list_1, energy_list_2):
  plt.figure(figsize=(10,10))
  bins = np.linspace(45, 50, 100)
  hist_3x3 = plt.hist(energy_list_1, bins=bins, histtype='step', label='$e^+$ 3x3 area', alpha=0.8, linewidth=3, color='navy')
  hist_5x5 = plt.hist(energy_list_2, bins=bins, histtype='step', label='$e^+$ 5x5 area',  alpha=0.8, linewidth=3, color='firebrick')
  plt.xlabel('energy_deposit (GeV)')
  plt.legend(loc='upper left', fontsize=15)
  plt.grid()

  plt.show()

##draw_nxn_plot(energy_list_3x3, energy_list_5x5)

#####################################energy loss#########################################


#####################################9x9x10 plot#########################################


