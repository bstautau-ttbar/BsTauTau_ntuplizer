from WMCore.Configuration import Configuration
config = Configuration()
config.section_('General')
config.General.workArea = 'crabjobs_v0_2026Nov12'
config.General.transferOutputs = True
config.General.transferLogs = True
config.General.requestName = 'EGamma_2018D_nanoAODv15_v0'
config.section_('JobType')
config.JobType.disableAutomaticOutputCollection = True
config.JobType.psetName = '../test/run_nanobtvUL18_150X_data_cfg.py'
config.JobType.outputFiles = ['step_nanoAODv15.root']
config.JobType.numCores = 2
config.JobType.maxMemoryMB = 5000
config.JobType.pluginName = 'Analysis'
config.JobType.allowUndistributedCMSSW = True
config.section_('Data')
config.Data.inputDataset = '/EGamma/Run2018D-UL2018_MiniAODv2_GT36-v3/MINIAOD'
config.Data.unitsPerJob = 2
config.Data.outLFNDirBase = ''
config.Data.publication = False
config.Data.inputDBS = 'global'
config.Data.outputDatasetTag = 'EGamma_2018D_RunIIUL18_nanoAODv15'
config.Data.totalUnits = 20000
config.Data.splitting = 'FileBased'
config.section_('Site')
config.Site.storageSite = 'T2_CH_CERN'
config.Site.blacklist = ['T2_BE_IIHE', 'T2_CH_CSCS']
config.section_('User')
config.section_('Debug')

