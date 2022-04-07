from CRABClient.UserUtilities import config, getUsernameFromCRIC

config = config()

config.General.requestName = "###REQUESTNAME###"
config.General.workArea = "###WORKAREA###"
config.General.transferLogs = True
config.General.transferOutputs = True

config.JobType.pluginName = "PrivateMC"
config.JobType.psetName = "###RUNCFGFILE###"
#config.JobType.maxMemoryMB = 4000
config.JobType.numCores = 4

config.Data.outputPrimaryDataset = "###OUTPUTPRIMARYDATASET###"
config.Data.outLFNDirBase = "/store/user/%s/" % (getUsernameFromCRIC())#FIXME
config.Data.outputDatasetTag = "###INPUTDATASETTAG###"
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = ###UNITSPERJOB###
NJOBS = ###NJOBS###
config.Data.totalUnits = config.Data.unitsPerJob * NJOBS
config.Data.publication = True

#config.Site.storageSite = "T2_CH_CERN"
config.Site.storageSite = "T2_IT_Pisa"
