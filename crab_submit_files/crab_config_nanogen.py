import os
import sys
import random
import argparse
import json
import shutil
import subprocess

def create_jobs(input_jsonfile):
	cmsdriver_sh = open("create_confg_run_crab.sh","w")
	cmsdriver_sh.write("#!/bin/bash\n")
	crab_file_list=[]
	with open(input_jsonfile) as data_file:    
		data = json.load(data_file)
		for sample, sample_cfg in data.items():		
			print "fname = ", sample_cfg["fragmentname"], ' ',sample_cfg["Nevents"]
			cfg_file="../configs/config_"+sample_cfg["CfgFile"]+".py"
			cmsdriver_p = "cmsDriver.py "+sample_cfg["fragmentname"]+" --fileout file:WminusJetsToMuNu_svn3900_BugFix.root --mc --eventcontent NANOAODSIM --datatier NANOAOD --conditions auto:mc --step LHE,GEN,NANOGEN --python_filename "+cfg_file+" --customise_commands process.RandomNumberGeneratorService.externalLHEProducer.initialSeed="+str(random.randint(1, 100000))+" nprocess.externalLHEProducer.generateConcurrently=True --nThreads 4 -n 30 --no_exec"
		
			cmsdriver_sh.write(cmsdriver_p+"\n\n")
			crab_file="crab_submit_"+sample_cfg["CfgFile"]+".py"
			print(crab_file)
			#os.system('cp skeleton/crab_basefile.py '+crab_file)
			shutil.copyfile("../skeleton/crab_nanogen_basefile.py",crab_file)
			subprocess.call(["sed -i 's|###REQUESTNAME###|" + sample_cfg["RequestName"] + "|g' " + crab_file], shell=True)
			subprocess.call(["sed -i 's|###WORKAREA###|" + sample_cfg["WorkArea"] + "|g' " + crab_file], shell=True)
			subprocess.call(["sed -i 's|###RUNCFGFILE###|" + cfg_file + "|g' " + crab_file], shell=True)
			subprocess.call(["sed -i 's|###OUTPUTPRIMARYDATASET###|" + sample_cfg["OutputPrimaryDataset"] + "|g' " + crab_file], shell=True)
			subprocess.call(["sed -i 's|###INPUTDATASETTAG###|" + sample_cfg["OutputDatasetTag"] + "|g' " + crab_file], shell=True)
			subprocess.call(["sed -i 's|###UNITSPERJOB###|" + str(int(sample_cfg["Nevents"])) + "|g' " + crab_file], shell=True)
			subprocess.call(["sed -i 's|###NJOBS###|" + sample_cfg["Njobs"] + "|g' " + crab_file], shell=True)
			crab_file_list.append(crab_file)
	  	

	print(len(crab_file_list))
	for i in range(len(crab_file_list)):
		print crab_file_list[i]
		cmsdriver_sh.write("crab submit "+crab_file_list[i]+"\n")	
	cmsdriver_sh.close()


def main():
        from argparse import ArgumentParser
        import argparse
        parser = ArgumentParser(description="Do -h to see usage")

        #parser.add_argument('-i', '--txt', action='store_true', help='input txt file name')
        #parser.add_argument('-f', '--txt',help='txt file input',type=argparse.FileType('r'),)
        #parser.add_argument('--f', type=open)

        parser.add_argument('-i', '--json', type=str)

        args = parser.parse_args()

        print(args)

        create_jobs(args.json)


if __name__ == "__main__":
        main()
