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

