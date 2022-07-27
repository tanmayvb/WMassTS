import numpy as np
import ROOT
import array
import glob
import argparse
import os


#infile_path= "/afs/cern.ch/work/t/tsarkar/public/Tanmay-MATRIX+REDISH-OutPut/ppz01_MATRIX+RadISH/NNLO-run/MATRIX+RadISH/"

def ReadFile(infile_path):
	mylist = []
	myhist= []

	for root, subFolder, files in os.walk(infile_path):
		for item in files:
			if item.endswith(".dat") :
				fileNamePath = str(os.path.join(root,item))
				#print(fileNamePath)
				mylist.append(fileNamePath)
				if (item.find('+')):
					item = item.replace('+','Plus')
				if (item.find('__')):
					item = item.replace('__','_').replace('.dat','')
					print item
					myhist.append(item)
	return mylist, myhist
#print (len(mylist))


def CreateHist(infile_path, save_dir):
	if not os.path.exists(save_dir):
		os.mkdir(save_dir)
	mylist, myhist = ReadFile(infile_path)

	f = ROOT.TFile(save_dir+'/'+'RedIshMatrix.root',"recreate");

	for i in range (len(mylist)):
		sed = np.loadtxt(mylist[i], unpack = True)

		central_hist_name = myhist[i]
		nbins = len(sed[0])-1
		varbins = np.array(sed[0])
		central_hist = ROOT.TH1D(central_hist_name, central_hist_name, nbins, varbins)
		central_hist_scaleDown = central_hist.Clone(central_hist_name + '_scaleDown')
		central_hist_scaleDown.Reset()
		central_hist_scaleUp = central_hist.Clone(central_hist_name + '_scaleUp')
		central_hist_scaleUp.Reset()

		for i in range (len(sed[0])):
			if(sed[1][i]>0):
				central_hist.SetBinContent(i+1, sed[1][i])
				central_hist.SetBinError(i+1, sed[2][i])
			central_hist_scaleDown.SetBinContent(i+1, sed[3][i])
			central_hist_scaleDown.SetBinError(i+1, sed[4][i])
			central_hist_scaleUp.SetBinContent(i+1, sed[5][i])
			central_hist_scaleUp.SetBinError(i+1, sed[6][i])
			#print sed[1][i], ' ', sed[2][i]

		HistSettings(central_hist,central_hist_name, save_dir)
		HistSettings(central_hist_scaleDown,central_hist_name+'scaleDown', save_dir)
		HistSettings(central_hist_scaleUp,central_hist_name+'scaleUp', save_dir)
	f.Close();

def HistSettings(histIn, central_hist_name, save_dir):
	hist = ROOT.TH1D(histIn)
	hist.Write();
	canvas = ROOT.TCanvas("canvas", "canvas")
	hist.SetMinimum(hist.GetMinimum()*.9)
	hist.SetMaximum(hist.GetMaximum()*1.1)
	hist.SetMarkerStyle(4)
	hist.SetMarkerColor(ROOT.kRed)
	#central.SetMarkerSize(1)
	#central.Scale(1/central.Integral())
	hist.GetXaxis().SetRange(0,30)
	hist.Draw("P e1")
	print 'Creating and writing histogram ', hist
	#hist.Write();
	canvas.Print(save_dir+'/'+central_hist_name+'.pdf')
	

def main():
        from argparse import ArgumentParser
        import argparse
        parser = ArgumentParser(description="Do -h to see usage")
        parser.add_argument('-i', '--path', type=str)
        parser.add_argument('-o', '--dire', type=str)

        args = parser.parse_args()

        print(args)

        CreateHist(args.path, args.dire)


if __name__ == "__main__":
        main()
