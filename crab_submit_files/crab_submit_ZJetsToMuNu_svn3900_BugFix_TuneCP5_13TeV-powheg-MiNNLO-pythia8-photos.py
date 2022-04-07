from CRABClient.UserUtilities import config, getUsernameFromCRIC

config = config()

config.General.requestName = "NanoGen_ZJetsToMuNu_svn3900_BugFix_TuneCP5_13TeV-powheg-MiNNLO-pythia8-photos"
config.General.workArea = "ZJetsToMuNu_svn3900_BugFix_TuneCP5_13TeV-powheg-MiNNLO-pythia8-photos"
config.General.transferLogs = True
config.General.transferOutputs = True

config.JobType.pluginName = "PrivateMC"
config.JobType.psetName = "../configs/config_ZJetsToMuNu_svn3900_BugFix_TuneCP5_13TeV-powheg-MiNNLO-pythia8-photos.py"
#config.JobType.maxMemoryMB = 4000
config.JobType.numCores = 4

config.Data.outputPrimaryDataset = "v1_ZJetsToMuNu_svn3900_BugFix_TuneCP5_13TeV-powheg-MiNNLO-pythia8-photos"
config.Data.outLFNDirBase = "/store/user/%s/" % (getUsernameFromCRIC())#FIXME
config.Data.outputDatasetTag = "RunII20UL17_NanoGen"
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = 10000
NJOBS = 500
config.Data.totalUnits = config.Data.unitsPerJob * NJOBS
config.Data.publication = True

#config.Site.storageSite = "T2_CH_CERN"
config.Site.storageSite = "T2_IT_Pisa"
