# SampleProduction NaNoGen From GridPack
## Setup framework

Setup a CMSSW release:
```
mkdir GenProduction
cd GenProduction
cmsrel CMSSW_10_6_27   ##### Should be > CMSSW_10_6_20

cd CMSSW_10_6_27/src
cmsenv
```
Checkout this framework and switch to this branch:
```
git clone -b NanoGen_Production https://github.com/tanmayvb/WMassTS.git
cd WMassTS

cmsenv
sh set_script.sh 
```
Then compile:
```
scram b -j4
```
## STEP1: Prepare Configuration file
```
cd ../Configuration/GenProduction/python
```
 Run: 
```
python createFragments_2017.py -i input_create_baseline_config.json
  
```  
#### Change this file, name of gridpack etc... It will create cfg file from different gridpack within specified directory name.

```
cd ${CMSSW_BASE}/src
```
and then compile again:
```scram b -j4```

Set proxy:
```
voms-proxy-init --voms cms -valid 192:00
```
## STEP2: Create and submit Crab jobs
```
cd WMassTS
```
In next step: 
1. change storage path in the file **skeleton/crab_nanogen_basefile.py** .
2. cd crab_submit_files
3. change/create new **.json** file to change gridpack location, name, input data tag, Nevents, Njobs etc... One can put many sample name in the same json file.

Run:
```crab_config_nanogen.py -i input_nanogen_step.json```  with input the above created json file.

It will create a script file **create_confg_run_crab.sh** which contain everyting and will submit crab jobs.

To run and submit crab job: ```sh create_confg_run_crab.sh```


















