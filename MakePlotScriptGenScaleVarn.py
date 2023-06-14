import hist
import boost_histogram as bh
import numpy as np
import os
import mplhep as hep
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from utilities import boostHistHelpers as hh, common
from wremnants import histselections as sel
from wremnants import datasets2016
from wremnants import plot_tools
import wremnants
import lz4.frame
import pickle
import h5py
import narf
from argparse import ArgumentParser
from ROOT import TFile
hep.style.use(hep.style.ROOT)

parser = ArgumentParser(description="Do -h to see usages")
parser.add_argument("--plotAll", action='store_true', help="plot all Ai with qt,y and 2dplot")
parser.add_argument("--plotqtbyq", action='store_true', help="plot all Ai with qt by q,y and 2dplot")
parser.add_argument("--test", action='store_true', help="plot all Ai with qt,y and 2dplot")
parser.add_argument("--plot1donly", action='store_true', help="plot all Ai with qt,y")
parser.add_argument("--plot2donly", action='store_true', help="plot all Ai, 2dplot")
parser.add_argument("--plotdiffdist", action='store_true', help="plot all 2dplot qt vs y")
parser.add_argument("--plotbasic", action='store_true', help="plot all 2dplot qt vs y")
parser.add_argument("--plotqcd", action='store_true', help="Make qcd sacle varitation plots")
parser.add_argument("--plotpdfs", action='store_true', help="Make pdf varitation plots")
parser.add_argument("--plotdiffmass", action='store_true', help="Make mass varitation plots")
parser.add_argument("--isrebin", action='store_true', help="rebin qt")
parser.add_argument("-o","--outdir", type=str, help="save all plots")
parser.add_argument('-f', "--rootFile", type=str, help="Output rootFile name")
args = parser.parse_args()

def openFilemain(filename):
	file = h5py.File(filename, "r")
	outfile = narf.ioutils.pickle_load_h5py(file["results"])
	return outfile

def plot(hname,xlabel, ylabel, figname):
	fig, ax1 = plt.subplots()
	ax1.set_xlabel(xlabel,loc='center',)
	ax1.set_ylabel(ylabel,loc='center',)
	#plt.plot(hname);  
	#plt.step(hname.axes[0].centers, hname.values()); 
	hep.histplot(
		hname,
		histtype = "step",
		ax =ax1,
		binwnorm=True,
		#w2=True
		edges =None
		#yerr = True
		)
	plt.savefig(figname+'.pdf')


def plot1d(hname,xlabel, ylabel, figname, savedir):
	fig, ax1 = plt.subplots()
	ax1.set_xlabel(xlabel,loc='center',)
	ax1.set_ylabel(ylabel,loc='center',)
	#ax1.text(hname.axes[0].centers,hname.values(),color="w", ha="center", va="center", fontweight="bold")
	#stat = hname.variances()
	#stat = np.sqrt(abs(hname.values()))/abs(hname.values())
	plt.step(hname.axes[0].centers, hname.values()); 
	#plt.errorbar(hname.axes[0].centers, hname.values(),yerr=stat,marker = ('.'),linestyle=None); 
	#plt.errorbar(hname.axes[0].centers, hname.values(),fmt='o');
	#plt.errorbar(hname.axes[0].centers, hname.values(),yerr=1/np.sqrt(hname.values()), marker = ('o'));  
	#ax1.hist2d(np.array(hname.axes[0]),np.array(hname.axes[1]))
	#print("StatError = ", hname.variances(), "StatError Cross = ", np.sqrt(abs(hname.values())))
	plt.savefig(savedir+'/'+figname+'.pdf')

def plot2d(hname,xlabel, ylabel, figname):
	#print("in plot", hname)
	fig, ax = plt.subplots()
	#pcm = ax.pcolormesh(*hname.axes.edges.T, hname.values().T) 
	pcm = ax.pcolormesh(*hname.axes.edges.T, hname.values().T)
	fig.colorbar(pcm)
	ax.set_xlabel(xlabel,loc='center',)
	ax.set_ylabel(ylabel,loc='center',)
	fig.savefig(figname+'.pdf')

#outfilemain = openFilemain('w_z_gen_dists.hdf5')

##Using Now###
#outfilemain = openFilemain('w_z_gen_dists_scetlib_dyturboCorr.hdf5')
outfilemain = openFilemain('w_z_gen_dists_scetlib_dyturboCorr_eightQbins.hdf5')
#outfilemain = openFilemain('w_z_gen_dists_no_offsets_withQbins_withpdf.hdf5')
##Using Now###


#outfilemain = openFilemain('/home/users/tanmay/WMass/V1/Output/qtbyQ/w_z_gen_ptqvgen_dists.hdf5')

##Using Now###
#wphist= outfilemain["WplusmunuPostVFP"]["output"]["nominal_gen_pdfMSHT20alphaS002_pdfhelicity"]
#wmhist = outfilemain["WminusmunuPostVFP"]["output"]["nominal_gen_pdfMSHT20alphaS002_pdfhelicity"]
#zhist = outfilemain["ZmumuPostVFP"]["output"]["nominal_gen_pdfMSHT20alphaS002_pdfhelicity"]

wphist= outfilemain["WplusmunuPostVFP"]["output"]["helicity_moments_scale"]
wmhist = outfilemain["WminusmunuPostVFP"]["output"]["helicity_moments_scale"]
zhist = outfilemain["ZmumuPostVFP"]["output"]["helicity_moments_scale"]


##Using Now###

Wplushist_main = outfilemain["WplusmunuPostVFP"]["output"]["nominal_gen"]
Wminushist_main = outfilemain["WminusmunuPostVFP"]["output"]["nominal_gen"]
Zhist_main = outfilemain["ZmumuPostVFP"]["output"]["nominal_gen"]


#print(wphist.get())
if not os.path.exists(args.outdir):
  os.mkdir(args.outdir)

#rootfile = TFile("allrootfilemarch31_no_offset_y20bin.root", "RECREATE")
rootfile = TFile(args.outdir+'/'+args.rootFile+'.root', "RECREATE")

bosons = ['wp','wm', 'z']
axis_project = ['ptVgen','y']
muR_scale = [1,2,0.5,1,0.5,2,1]
muF_scale = [1,2,0.5,0.5,1,1,2]
qcd_scalestr = ['oneone','twotwo','point5point5','onepoint5','point5one','twoone','onetwo']
mass_bin = ['binone', 'bintwo', 'binthree','binfour','binfive','binsix','binseven','bineight']
#mass_bin = ['binone', 'bintwo', 'binthree','binfour']


if(args.plotqtbyq):
  axis_project = ['ptqVgen','y']
  strig = 'Qbyq'
else:
  axis_project = ['ptVgen','y']
  strig = 'q'
#print(f"Bining: {common.ptV_binning_diffQDY}")


if args.plotAll or args.plot1donly:
	hist1D_coeff = {}
	for boson in bosons:
		hist1D_coeff[boson] = {}
		for axis in axis_project:
			hist1D_coeff[boson][axis] = {}
			if boson=='wp':
				if axis=='ptVgen' or axis =='ptqVgen':
					if args.isrebin:
						hist1D_coeff[boson][axis] = wremnants.moments_to_angular_coeffs(hh.rebinHist(wphist.get()[{'muRfact': 1.j, 'muFfact': 1.j}].project(axis,"helicity"), axis, common.ptV_binning_diffQ)) if axis=='ptVgen' else wremnants.moments_to_angular_coeffs(wphist.get()[{'muRfact': 1.j, 'muFfact': 1.j}].project(axis,"helicity"))
					else:
						hist1D_coeff[boson][axis] = wremnants.moments_to_angular_coeffs(wphist.get()[{'muRfact': 1.j, 'muFfact': 1.j}].project(axis,"helicity")) if axis=='ptVgen' else wremnants.moments_to_angular_coeffs(wphist.get()[{'muRfact': 1.j, 'muFfact': 1.j}].project(axis,"helicity"))
				else:
					hist1D_coeff[boson][axis] = wremnants.moments_to_angular_coeffs(hh.rebinHist(wphist.get()[{'muRfact': 1.j, 'muFfact': 1.j}].project(axis,"helicity"), "y", 10))

			elif boson=='wm':
				if axis=='ptVgen' or axis =='ptqVgen':
					if args.isrebin:
						hist1D_coeff[boson][axis] = wremnants.moments_to_angular_coeffs(hh.rebinHist(wmhist.get()[{'muRfact': 1.j, 'muFfact': 1.j}].project(axis,"helicity"), axis, common.ptV_binning_diffQ)) if axis=='ptVgen' else wremnants.moments_to_angular_coeffs(wmhist.get()[{'muRfact': 1.j, 'muFfact': 1.j}].project(axis,"helicity"))
					else:
						hist1D_coeff[boson][axis] = wremnants.moments_to_angular_coeffs(wmhist.get()[{'muRfact': 1.j, 'muFfact': 1.j}].project(axis,"helicity")) if axis=='ptVgen' else wremnants.moments_to_angular_coeffs(wmhist.get()[{'muRfact': 1.j, 'muFfact': 1.j}].project(axis,"helicity"))
				else:
					hist1D_coeff[boson][axis] = wremnants.moments_to_angular_coeffs(hh.rebinHist(wmhist.get()[{'muRfact': 1.j, 'muFfact': 1.j}].project(axis,"helicity"), "y", 10))

			else:
				if axis=='ptVgen' or axis =='ptqVgen':
					if args.isrebin:
						hist1D_coeff[boson][axis] = wremnants.moments_to_angular_coeffs(hh.rebinHist(zhist.get()[{'muRfact': 1.j, 'muFfact': 1.j, "massVgen" : 90.j}].project(axis,"helicity"), axis, common.ptV_binning_diffQ)) if axis=='ptVgen' else wremnants.moments_to_angular_coeffs(zhist.get()[{'muRfact': 1.j, 'muFfact': 1.j, "massVgen" : 90.j}].project(axis,"helicity"))
					else:
						hist1D_coeff[boson][axis] = wremnants.moments_to_angular_coeffs(zhist.get()[{'muRfact': 1.j, 'muFfact': 1.j, "massVgen" : 90.j}].project(axis,"helicity")) if axis=='ptVgen' else wremnants.moments_to_angular_coeffs(zhist.get()[{'muRfact': 1.j, 'muFfact': 1.j, "massVgen" : 90.j}].project(axis,"helicity"))
				else:
					hist1D_coeff[boson][axis] = wremnants.moments_to_angular_coeffs(hh.rebinHist(zhist.get()[{'muRfact': 1.j, 'muFfact': 1.j, "massVgen" : 90.j}].project(axis,"helicity"), "y", 10))

	rpaxis = 'Y'
	for boson in bosons:
		for axis in axis_project:
			for prox in range(8):
				name = r'$\bf A_{}$'.format(prox)
				name1 = 'A_{}'.format(prox)
				if axis == 'ptVgen' or axis =='ptqVgen':
					if boson == 'wp':
						xname = r'$\bf {}_{{t}}^{{Wplus}}$'.format(strig)
					elif boson == 'wm':
						xname = r'$\bf {}_{{t}}^{{Wminus}}$'.format(strig)
					else:
						xname = r'$\bf {}_{{t}}^{{Z}}$'.format(strig)
				elif axis == 'y' or 'absy':
					if boson == 'wp':
						xname = r'$\bf {}^{{Wplus}}$'.format(rpaxis)
					elif boson == 'wm':
						xname = r'$\bf {}^{{Wminus}}$'.format(rpaxis)
					else:
						xname = r'$\bf {}^{{Z}}$'.format(rpaxis)
				print(f'{boson} : {axis} : {xname} :{strig}')
        #print(f'{hist1D_coeff[boson][axis][prox]}')
				plot1d(hist1D_coeff[boson][axis][{"helicity" : complex(prox)}],xname, name, f"ang_coeff_{boson}_{axis}_{name1}", args.outdir)
				xx = narf.hist_to_root(hist1D_coeff[boson][axis][{"helicity" : complex(prox)}])
				xx.Write(f"ang_coeff_{boson}_{axis}_{name1}")

if args.plotAll or args.plotdiffmass:
	hist1D_coeff = {}
	for boson in bosons:
		hist1D_coeff[boson] = {}
		for axis in axis_project:
			hist1D_coeff[boson][axis] = {}
			for mass in range(1,len(mass_bin)+1):
				hist1D_coeff[boson][axis][mass] = {}
				if boson=='wp':
					if axis=='ptVgen':
						if args.isrebin:
							hist1D_coeff[boson][axis][mass] =  wremnants.moments_to_angular_coeffs(hh.rebinHist(wphist.get()[{'muRfact': 1.j, 'muFfact': 1.j, 'massVgen': complex(mass)}].project(axis,"helicity"), axis, common.ptV_binning_diffQ))
						else:
							hist1D_coeff[boson][axis][mass] =  wremnants.moments_to_angular_coeffs(wphist.get()[{'muRfact': 1.j, 'muFfact': 1.j, 'massVgen': complex(mass)}].project(axis,"helicity"))
					else:
						hist1D_coeff[boson][axis][mass] = wremnants.moments_to_angular_coeffs(hh.rebinHist(wphist.get()[{'muRfact': 1.j, 'muFfact': 1.j, 'massVgen': complex(mass)}].project(axis,"helicity"), "y", 10))
				elif boson=='wm':
					if axis=='ptVgen':
						if args.isrebin:
							hist1D_coeff[boson][axis][mass] = wremnants.moments_to_angular_coeffs(hh.rebinHist(wmhist.get()[{'muRfact': 1.j, 'muFfact': 1.j, 'massVgen': complex(mass)}].project(axis,"helicity"), axis, common.ptV_binning_diffQ))
						else:
							hist1D_coeff[boson][axis][mass] = wremnants.moments_to_angular_coeffs(wmhist.get()[{'muRfact': 1.j, 'muFfact': 1.j, 'massVgen': complex(mass)}].project(axis,"helicity"))
					else:
						hist1D_coeff[boson][axis][mass] = wremnants.moments_to_angular_coeffs(hh.rebinHist(wmhist.get()[{'muRfact': 1.j, 'muFfact': 1.j, 'massVgen': complex(mass)}].project(axis,"helicity"), "y", 10))

				else:
					if axis=='ptVgen':
						if args.isrebin:
							hist1D_coeff[boson][axis][mass] = wremnants.moments_to_angular_coeffs(hh.rebinHist(zhist.get()[{'muRfact': 1.j, 'muFfact': 1.j, 'massVgen': complex(mass)}].project(axis,"helicity"), axis, common.ptV_binning_diffQ))
						else:
							hist1D_coeff[boson][axis][mass] = wremnants.moments_to_angular_coeffs(zhist.get()[{'muRfact': 1.j, 'muFfact': 1.j, 'massVgen': complex(mass)}].project(axis,"helicity"))
					else:
						hist1D_coeff[boson][axis][mass] = wremnants.moments_to_angular_coeffs(hh.rebinHist(zhist.get()[{'muRfact': 1.j, 'muFfact': 1.j, 'massVgen': complex(mass)}].project(axis,"helicity"), "y", 10))

	strig = 'q'
	rpaxis = 'Y'
	for boson in bosons:
		for axis in axis_project:
			for mass in range(1,len(mass_bin)+1):
				for prox in range(8):
					name = r'$\bf A_{}$'.format(prox)
					name1 = 'A_{}'.format(prox)
					if axis == 'ptVgen':
						if boson == 'wp':
							xname = r'$\bf {xx}_{{t}}^{{Wplus}}$'.format(xx=strig)
						elif boson == 'wm':
							xname = r'$\bf {xx}_{{t}}^{{Wminus}}$'.format(xx=strig)
						else:
							xname = r'$\bf {xx}_{{t}}^{{Z}}$'.format(xx=strig)
					if axis == 'y' or 'absy':
						if boson == 'wp':
							xname = r'$\bf {}^{{Wplus}}$'.format(rpaxis)
						elif boson == 'wm':
							xname = r'$\bf {}^{{Wminus}}$'.format(rpaxis)
						else:
							xname = r'$\bf {}^{{Z}}$'.format(rpaxis)
        #print(f'{boson} : {axis} : {prox}')
        #print(f'{hist1D_coeff[boson][axis][prox]}')
					plot1d(hist1D_coeff[boson][axis][mass][{"helicity" : complex(prox)}],xname, name, f"ang_coeff_{boson}_{axis}_{str(mass_bin[mass-1])}_{name1}",args.outdir)
					xx = narf.hist_to_root(hist1D_coeff[boson][axis][mass][{"helicity" : complex(prox)}])
					xx.Write(f"ang_coeff_{boson}_{axis}_{str(mass_bin[mass-1])}_{name1}")


if args.plotAll or args.plotqcd:
	hist1D_coeff = {}
	for boson in bosons:
		hist1D_coeff[boson] = {}
		for axis in axis_project:
			hist1D_coeff[boson][axis] = {}
			for scale in range(len(muR_scale)):
				hist1D_coeff[boson][axis][scale] = {}
				if boson=='wp':
					if axis=='ptVgen':
						print(f"{complex(0,muR_scale[scale])} : {muF_scale[scale]}")
						muR = muR_scale[scale]
						hist1D_coeff[boson][axis][scale] =	wremnants.moments_to_angular_coeffs(wphist.get()[{'muRfact': complex(0,muR_scale[scale]), 'muFfact': complex(0,muF_scale[scale])}].project(axis,"helicity"))
					else:
								hist1D_coeff[boson][axis][scale] = wremnants.moments_to_angular_coeffs(hh.rebinHist(wphist.get()[{'muRfact': complex(0,muR_scale[scale]), 'muFfact': complex(0,muF_scale[scale])}].project(axis,"helicity"), "y", 10))

				elif boson=='wm':
					if axis=='ptVgen':
						hist1D_coeff[boson][axis][scale] = wremnants.moments_to_angular_coeffs(wmhist.get()[{'muRfact': complex(0,muR_scale[scale]), 'muFfact': complex(0,muF_scale[scale])}].project(axis,"helicity"))
					else:
						hist1D_coeff[boson][axis][scale] = wremnants.moments_to_angular_coeffs(hh.rebinHist(wmhist.get()[{'muRfact': complex(0,muR_scale[scale]), 'muFfact': complex(0,muR_scale[scale])}].project(axis,"helicity"), "y", 10))

				else:
					if axis=='ptVgen':
						hist1D_coeff[boson][axis][scale] = wremnants.moments_to_angular_coeffs(zhist.get()[{'muRfact': complex(0,muR_scale[scale]), 'muFfact': complex(0,muF_scale[scale])}].project(axis,"helicity"))
					else:
						hist1D_coeff[boson][axis][scale] = wremnants.moments_to_angular_coeffs(hh.rebinHist(zhist.get()[{'muRfact': complex(0,muR_scale[scale]), 'muFfact': complex(0,muF_scale[scale])}].project(axis,"helicity"), "y", 10))
	strig = 'q'
	rpaxis = 'Y'
	for boson in bosons:
		for axis in axis_project:
			for scale in range(len(muR_scale)):
				for prox in range(8):
					name = r'$\bf A_{}$'.format(prox)
					name1 = 'A_{}'.format(prox)
					if axis == 'ptVgen':
						if boson == 'wp':
							xname = r'$\bf {xx}_{{t}}^{{Wplus}}$'.format(xx=strig)
						elif boson == 'wm':
							xname = r'$\bf {xx}_{{t}}^{{Wminus}}$'.format(xx=strig)
						else:
							xname = r'$\bf {xx}_{{t}}^{{Z}}$'.format(xx=strig)
					if axis == 'y' or 'absy':
						if boson == 'wp':
							xname = r'$\bf {}^{{Wplus}}$'.format(rpaxis)
						elif boson == 'wm':
							xname = r'$\bf {}^{{Wminus}}$'.format(rpaxis)
						else:
							xname = r'$\bf {}^{{Z}}$'.format(rpaxis)
				#print(f'{boson} : {axis} : {prox}')
				#print(f'{hist1D_coeff[boson][axis][prox]}')
					plot1d(hist1D_coeff[boson][axis][scale][{"helicity" : complex(prox)}],xname, name, f"ang_coeff_{boson}_{axis}_{str(qcd_scalestr[scale])}_{name1}")
					xx = narf.hist_to_root(hist1D_coeff[boson][axis][scale][{"helicity" : complex(prox)}])
					xx.Write(f"ang_coeff_{boson}_{axis}_{str(qcd_scalestr[scale])}_{name1}")

if args.plotAll or args.plotpdfs:
	hist1D_coeff = {}
	for boson in bosons:
		hist1D_coeff[boson] = {}
		for axis in axis_project:
			hist1D_coeff[boson][axis] = {}
			for scale in range(0,63):
				hist1D_coeff[boson][axis][scale] = {}
				if boson=='wp':
					if axis=='ptVgen':
						hist1D_coeff[boson][axis][scale] =	wremnants.moments_to_angular_coeffs(wphist.get()[{'pdf0MSHT20': complex(scale)}].project(axis,"helicity"))
					else:
								hist1D_coeff[boson][axis][scale] = wremnants.moments_to_angular_coeffs(hh.rebinHist(wphist.get()[{'pdf0MSHT20': complex(scale)}].project(axis,"helicity"), "y", 10))

				elif boson=='wm':
					if axis=='ptVgen':
						hist1D_coeff[boson][axis][scale] = wremnants.moments_to_angular_coeffs(wmhist.get()[{'pdf0MSHT20': complex(scale)}].project(axis,"helicity"))
					else:
						hist1D_coeff[boson][axis][scale] = wremnants.moments_to_angular_coeffs(hh.rebinHist(wmhist.get()[{'pdf0MSHT20': complex(scale)}].project(axis,"helicity"), "y", 10))

				else:
					if axis=='ptVgen':
						hist1D_coeff[boson][axis][scale] = wremnants.moments_to_angular_coeffs(zhist.get()[{'massVgen': 90.j, 'pdf0MSHT20': complex(scale)}].project(axis,"helicity"))
					else:
						hist1D_coeff[boson][axis][scale] = wremnants.moments_to_angular_coeffs(hh.rebinHist(zhist.get()[{'massVgen': 90.j, 'pdf0MSHT20': complex(scale)}].project(axis,"helicity"), "y", 10))
	strig = 'q'
	rpaxis = 'Y'
	for boson in bosons:
		for axis in axis_project:
			for scale in range(0,63):
				for prox in range(8):
					name = r'$\bf A_{}$'.format(prox)
					name1 = 'A_{}'.format(prox)
					if axis == 'ptVgen':
						if boson == 'wp':
							xname = r'$\bf {xx}_{{t}}^{{Wplus}}$'.format(xx=strig)
						elif boson == 'wm':
							xname = r'$\bf {xx}_{{t}}^{{Wminus}}$'.format(xx=strig)
						else:
							xname = r'$\bf {xx}_{{t}}^{{Z}}$'.format(xx=strig)
					if axis == 'y' or 'absy':
						if boson == 'wp':
							xname = r'$\bf {}^{{Wplus}}$'.format(rpaxis)
						elif boson == 'wm':
							xname = r'$\bf {}^{{Wminus}}$'.format(rpaxis)
						else:
							xname = r'$\bf {}^{{Z}}$'.format(rpaxis)
				#print(f'{boson} : {axis} : {prox}')
				#print(f'{hist1D_coeff[boson][axis][prox]}')
					plot1d(hist1D_coeff[boson][axis][scale][{"helicity" : complex(prox)}],xname, name, f"ang_coeff_{boson}_{axis}_pdf{str(scale)}_{name1}")
					xx = narf.hist_to_root(hist1D_coeff[boson][axis][scale][{"helicity" : complex(prox)}])
					xx.Write(f"ang_coeff_{boson}_{axis}_pdf{str(scale)}_{name1}")

if args.plotAll or args.plot2donly:
	hist2D_coeff = {}
	for boson in bosons:
		hist2D_coeff[boson] = {}
		if boson=='wp':
			wprbinqt = hh.rebinHist(wphist.get()[{'muRfact': 1.j, 'muFfact': 1.j}].project('y','ptVgen',"helicity"), "ptVgen", common.ptV_binning_diffQ)
			wprbiny = hh.rebinHist(wprbinqt,"y",10)
			hist2D_coeff[boson] = wremnants.moments_to_angular_coeffs(wprbiny)
			#hist2D_coeff[boson] = wremnants.moments_to_angular_coeffs(hh.rebinHist(wphist.get()[{'muRfact': 1.j, 'muFfact': 1.j}].project('y','ptVgen',"helicity"), "ptVgen", common.ptV_binning_diffQ))
		elif boson=='wm':
			wmrbinqt = hh.rebinHist(wmhist.get()[{'muRfact': 1.j, 'muFfact': 1.j}].project('y','ptVgen',"helicity"), "ptVgen", common.ptV_binning_diffQ)
			wmrbiny = hh.rebinHist(wmrbinqt,"y",10)
			hist2D_coeff[boson] = wremnants.moments_to_angular_coeffs(wmrbiny)
			#hist2D_coeff[boson] = wremnants.moments_to_angular_coeffs(hh.rebinHist(wmhist.get()[{'muRfact': 1.j, 'muFfact': 1.j}].project('y','ptVgen',"helicity"), "ptVgen", common.ptV_binning_diffQ))
		else:
			zrbinqt = hh.rebinHist(zhist.get()[{'muRfact': 1.j, 'muFfact': 1.j, "massVgen" : 90.j}].project('y','ptVgen',"helicity"), "ptVgen", common.ptV_binning_diffQ)
			zrbiny = hh.rebinHist(zrbinqt,"y",10)
			#print(f"rebiny = {zrbiny}")
			#hist2D_coeff[boson] = wremnants.moments_to_angular_coeffs(zrbiny[::,:40.j,::])
			hist2D_coeff[boson] = wremnants.moments_to_angular_coeffs(zrbiny)
			print(f"A coeff ", hist2D_coeff[boson])
			#hist2D_coeff[boson] = wremnants.moments_to_angular_coeffs(hh.rebinHist(zhist.get().project('y','ptVgen',"helicity"), "ptVgen", common.ptV_binning_diffQ,"y",5))

	rpaxis = 'Y'
	for boson in bosons:
		for prox in range(8):
			name = r'$\bf A_{}$'.format(prox)
			name1 = 'A_{}'.format(prox)
			if boson == 'wp':
				xname = r'$\bf {}^{{Wplus}}$'.format(rpaxis)
				yname = r'$\bf {xx}_{{t}}^{{Wplus}}$'.format(xx=strig)
			elif boson == 'wm':
				xname = r'$\bf {}^{{Wminus}}$'.format(rpaxis)
				yname = r'$\bf {xx}_{{t}}^{{Wminus}}$'.format(xx=strig)
			else:
				xname = r'$\bf {}^{{Z}}$'.format(rpaxis)
				yname = r'$\bf {xx}_{{t}}^{{Z}}$'.format(xx=strig)
			plot2d(hist2D_coeff[boson][{"helicity" : complex(prox)}], xname, yname, f"ang_coeff_{boson}_y_vs_qt_{name1}")
			plot1d(hist2D_coeff[boson][{"helicity" : complex(prox)}],xname, name, f"ang_coeff_{boson}_test12_{name1}")
			#print ("2d hist ", hist2D_coeff[boson][{"helicity" : prox}].view())
			#plot2d(hist2D_coeff[boson][{"helicity" : prox}], xname, yname, f"ang_coeff_{boson}_y_vs_qt_{name1}")
			xx = narf.hist_to_root(hist2D_coeff[boson][{"helicity" : complex(prox)}])
			xx.Write(f"ang_coeff_{boson}_y_vs_qt_{name1}")
	
if args.test:
#z_coeffs = wremnants.moments_to_angular_coeffs(hh.rebinHist(Zhist_main.get().project("ptVgen","helicity"), "ptVgen", common.ptV_binning_diffQ))
	z_coeffs = wremnants.moments_to_angular_coeffs(hh.rebinHist(zhist.get()[{'muRfact': 1.j, 'muFfact': 1.j, "massVgen" : 90.j}].project("y","helicity"), "y",10))
	#z_coeffs = wremnants.theory_tools.moments_to_ai(hh.rebinHist(zhist.get()[{'muRfact': 1.j, 'muFfact': 1.j, "massVgen" : 90.j}].project("y","helicity"), "y",20))
	#z_coeffs = wremnants.theory_tools.moments_to_ai(zhist.get()[{'muRfact': 1.j, 'muFfact': 1.j, "massVgen" : 90.j}].project("helicity"))
#z_coeffs = wremnants.moments_to_angular_coeffs(hh.rebinHist(Zhist_main.get().project("y","helicity"), "y",5))
	#print("zcoff ", z_coeffs)

	for i in range(1):
		#print("Helicity ", z_coeffs[{"helicity" : complex(i)}], "Cross check ", z_coeffs[:,i])
		name = r'A_{}'.format(i)
		xname = r'$\bf{|Y|^{Z}}$'
		plot1d(z_coeffs[{"helicity" : complex(i)}], xname, name, f"test_y_{i}")
		print(f"zcoff : {z_coeffs[{'helicity' : complex(i)}]}")
		xx = narf.hist_to_root(z_coeffs[{"helicity" : complex(i)}])
		xx.Write(f"ang_coeff_z_y_test_{name}")


if args.plotAll or args.plotdiffdist:
	#print("2d hist :", Wplushist_main.get().project("y","ptVgen"))
	plot2d(Wplushist_main.get().project("y","ptVgen"),r'$\bf{|Y|^{Wplus}}$',r'$\bf {xx}_{{t}}^{{Wplus}}$'.format(xx=strig), 'wplus_2d_y_vs_qt_full_differential')
	wp_rebin = hh.rebinHist(Wplushist_main.get(),'ptVgen',common.ptV_binning_diffQ)
	plot2d(wp_rebin.project("y","ptVgen"),r'$\bf{|Y|^{Wplus}}$',r'$\bf {xx}_{{t}}^{{Wplus}}$'.format(xx=strig),'wplus_2d_y_vs_qt_rbin_differential')
	wp_absy = hh.makeAbsHist(wp_rebin,'y')
	plot2d(wp_absy.project("absy","ptVgen"),r'$\bf{|Y|^{Wplus}}$',r'$\bf {xx}_{{t}}^{{Wplus}}$'.format(xx=strig),'wplus_2d_y_vs_qt_absy_rbin_differential')
	plot2d(Wminushist_main.get().project("y","ptVgen"),r'$\bf{|Y|^{Wminus}}$',r'$\bf {xx}_{{t}}^{{Wminus}}$'.format(xx=strig),'wminus_2d_y_vs_qt_full_differential')
	wm_rebin = hh.rebinHist(Wminushist_main.get(),'ptVgen',common.ptV_binning_diffQ)
	plot2d(wm_rebin.project("y","ptVgen"),r'$\bf{|Y|^{Wminus}}$',r'$\bf {xx}_{{t}}^{{Wminus}}$'.format(xx=strig),'wminus_2d_y_vs_qt_rebin_differential')
	wm_absy = hh.makeAbsHist(wm_rebin,'y')
	plot2d(wm_absy.project("absy","ptVgen"),r'$\bf{|Y|^{Wminus}}$',r'$\bf {xx}_{{t}}^{{Wminus}}$'.format(xx=strig),'wminus_2d_y_vs_qt_absy_rebin_differential')
	plot2d(Zhist_main.get().project("y","ptVgen"),r'$\bf{|Y|^{Z}}$',r'$\bf {xx}_{{t}}^{{Z}}$'.format(xx=strig),'z_2d_y_vs_qt_full_differential')
	z_rebin = hh.rebinHist(Zhist_main.get(),'ptVgen',common.ptV_binning_diffQ)
	plot2d(z_rebin.project("y","ptVgen"),r'$\bf{|Y|^{Z}}$',r'$\bf {xx}_{{t}}^{{Z}}$'.format(xx=strig),'z_2d_y_vs_qt_rebin_differential')
	z_absy = hh.makeAbsHist(z_rebin,'y')
	plot2d(z_absy.project("absy","ptVgen"),r'$\bf{|Y|^{Z}}$',r'$\bf {xx}_{{t}}^{{Z}}$'.format(xx=strig),'z_2d_y_vs_qt_absy_rebin_differential')


if args.plotAll or args.plotbasic:
	plot(Wplushist_main.get().project("ptVgen"),r'$\bf {xx}_{{t}}^{{Wplus}}$'.format(xx=strig),r'$\bf{Event/bin}$','wplus_qt_full')
	wp_rebin = hh.rebinHist(Wplushist_main.get(),'ptVgen',common.ptV_binning_diffQ)
	plot(wp_rebin.project("ptVgen"),r'$\bf {xx}_{{t}}^{{Wplus}}$'.format(xx=strig),r'$\bf{Event/bin}$','wplus_qt_rbin')
	plot(Wplushist_main.get().project("y"),r'$\bf{Y^{Wplus}}$',r'$\bf{Event/bin}$','wplus_y_full')

	plot(Wminushist_main.get().project("ptVgen"),r'$\bf {xx}_{{t}}^{{Wminus}}$'.format(xx=strig),r'$\bf{Event/bin}$','wminus_qt_full')
	wp_rebin = hh.rebinHist(Wminushist_main.get(),'ptVgen',common.ptV_binning_diffQ)
	plot(wp_rebin.project("ptVgen"),r'$\bf {xx}_{{t}}^{{Wminus}}$'.format(xx=strig),r'$\bf{Event/bin}$','wminus_qt_rbin')
	plot(Wminushist_main.get().project("y"),r'$\bf{Y^{Wminus}}$',r'$\bf{Event/bin}$','wminus_y_full')

	plot(Zhist_main.get().project("ptVgen"),r'$\bf {xx}_{{t}}^{{Z}}$'.format(xx=strig),r'$\bf{Event/bin}$','z_qt_full')
	z_rebin = hh.rebinHist(Zhist_main.get(),'ptVgen',common.ptV_binning_diffQ)
	plot(z_rebin.project("ptVgen"),r'$\bf {xx}_{{t}}^{{Z}}$'.format(xx=strig),r'$\bf{Event/bin}$','z_qt_rbin')
	plot(Zhist_main.get().project("y"),r'$\bf{Y^{Z}}$',r'$\bf{Event/bin}$','z_y_full')
