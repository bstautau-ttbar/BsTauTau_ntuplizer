import os
""" Year dependent configurations / files """

def getEraConfiguration(era,isData):

    """ defines global tags, depending on the era """

    globalTags = {
        'era2016preVFP' :('',      ''),
        'era2016'       :('',             '106X_dataRun2_v35'),
        'era2017'       :('150X_mc2017_realistic_v1',             ''),
        'era2018'       :('150X_mc2018_realistic_v1',             ''),  
        'era2022'       :('150X_mcRun3_2022_realistic_v2',          '150X_dataRun3_v2'),
        'era2023'       :('150X_mcRun3_2023_realistic_v2',          '150X_dataRun3_v2'),
        'era2024'       :('150X_mcRun3_2024_realistic_v2',          '150X_dataRun3_v2'),
        'era2025'       :('150X_mcRun3_2024_realistic_v2',          '150X_dataRun3_Prompt_v1')
        }

    globalTag = globalTags[era][isData]

    return globalTag
    
ANALYSISTRIGGERMC = {
    '2016': {
        'e'     :'(HLT_Ele27_WPTight_Gsf)',
        'mu'    :'(HLT_IsoTkMu24||HLT_IsoMu24)',
        'ee'    :'(HLT_Ele27_WPTight_Gsf)',
        'emu'   :'(1)',
        'mumu'  :'(HLT_IsoTkMu24||HLT_IsoMu24)'
    },
    '2017': {
        'e'     :'(HLT_Ele27_WPTight_Gsf||HLT_Ele32_WPTight_Gsf||HLT_Ele32_WPTight_Gsf_L1DoubleEG||HLT_Ele35_WPTight_Gsf)',
        'mu'    :'(HLT_IsoMu27)',
        'ee'    :'(HLT_Ele27_WPTight_Gsf||HLT_Ele32_WPTight_Gsf||HLT_Ele32_WPTight_Gsf_L1DoubleEG||HLT_Ele35_WPTight_Gsf)',
        'emu'   :'(1)',
        'mumu'  :'(HLT_IsoMu27)'
    },
    '2018': {
        'e'     :'(HLT_Ele32_WPTight_Gsf)',
        'mu'    :'(HLT_IsoMu24)',
        'ee'    :'(HLT_Ele32_WPTight_Gsf||HLT_DoubleEle25_CaloIdL_MW||HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL)',
        'emu'   :'(1)',
        'mumu'  :'(HLT_IsoMu24||HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8)'
    },
    '2022': {'e':'(HLT_Ele30_WPTight_Gsf)','mu':'(HLT_IsoMu24)','ee':'(HLT_Ele30_WPTight_Gsf||HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL)','emu':'(1)','mumu':'(HLT_IsoMu24||HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8)'},
    '2023': {'e':'(HLT_Ele30_WPTight_Gsf)','mu':'(HLT_IsoMu24)','ee':'(HLT_Ele30_WPTight_Gsf||HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL)','emu':'(1)','mumu':'(HLT_IsoMu24||HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8)'},
    '2024': {'e':'(HLT_Ele30_WPTight_Gsf)','mu':'(HLT_IsoMu24)','ee':'(HLT_Ele30_WPTight_Gsf||HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL)','emu':'(1)','mumu':'(HLT_IsoMu24||HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8)'},
    '2025': {'e':'(HLT_Ele30_WPTight_Gsf)','mu':'(HLT_IsoMu24)','ee':'(HLT_Ele30_WPTight_Gsf||HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL)','emu':'(1)','mumu':'(HLT_IsoMu24||HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8)'}
}

ANALYSISTRIGGERDATA = {
    '2016': {
        'e'     :'(HLT_Ele27_WPTight_Gsf)',
        'mu'    :'(HLT_IsoMu24||HLT_IsoTkMu24)',
        'ee'    :'(HLT_Ele27_WPTight_Gsf)',
        'emu'   :'(1)',
        'mumu'  :'(HLT_IsoMu24||HLT_IsoTkMu24)'
    },
    '2017': {
        'e'     :'(HLT_Ele27_WPTight_Gsf||HLT_Ele32_WPTight_Gsf||HLT_Ele32_WPTight_Gsf_L1DoubleEG||HLT_Ele35_WPTight_Gsf)',
        'mu'    :'(HLT_IsoMu27)',
        'ee'    :'(HLT_Ele27_WPTight_Gsf||HLT_Ele32_WPTight_Gsf||HLT_Ele32_WPTight_Gsf_L1DoubleEG||HLT_Ele35_WPTight_Gsf)',
        'emu'   :'(1)',
        'mumu'  :'(HLT_IsoMu27)'
    },
    '2018': {
        'e'     :'(HLT_Ele32_WPTight_Gsf)',
        'mu'    :'(HLT_IsoMu24)',
        'ee'    :'(HLT_Ele32_WPTight_Gsf||HLT_DoubleEle25_CaloIdL_MW||HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL)',
        'emu'   :'(1)',
        'mumu'  :'(HLT_IsoMu24||HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8)'
    },
    '2022': {'e':'(HLT_Ele30_WPTight_Gsf)','mu':'(HLT_IsoMu24)','ee':'(HLT_Ele30_WPTight_Gsf||HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL)','emu':'(1)','mumu':'(HLT_IsoMu24||HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8)'},
    '2023': {'e':'(HLT_Ele30_WPTight_Gsf)','mu':'(HLT_IsoMu24)','ee':'(HLT_Ele30_WPTight_Gsf||HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL)','emu':'(1)','mumu':'(HLT_IsoMu24||HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8)'},
    '2024': {'e':'(HLT_Ele30_WPTight_Gsf)','mu':'(HLT_IsoMu24)','ee':'(HLT_Ele30_WPTight_Gsf||HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL)','emu':'(1)','mumu':'(HLT_IsoMu24||HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8)'},
    '2025': {'e':'(HLT_Ele30_WPTight_Gsf)','mu':'(HLT_IsoMu24)','ee':'(HLT_Ele30_WPTight_Gsf||HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL)','emu':'(1)','mumu':'(HLT_IsoMu24||HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8)'}
}


ANALYSISCHANNELCUT = { # no spaces!
    'e'     :'(nElectron>0&&nJet>0)',
    'mu'    :'(nMuon>0&&nJet>0)',
    'emu'   :'(nMuon>0&&nElectron>0&&nJet>0)',
    'ee'    :'(nElectron>1&&nJet>0)',
    'mumu'  :'(nMuon>1&&nJet>0)'
}

ANALYSISGRL = {
    '2016': 'Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt', #35.93
    '2017': 'Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt', #41.48
    '2018': 'Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt', # 
    '2022': 'Cert_Collisions2022_355100_362760_Golden.json',
    '2023': 'Cert_Collisions2023_366442_370790_Golden.json',
    '2024': 'Cert_Collisions2024_378981_386951_Golden.json',
    '2025': 'Cert_Collisions2025_391658_398595_Golden.json',

}

cmssw=os.environ['CMSSW_BASE']
ANALYSISCUT={
    '': {
        'e'     : '-c "%s"'%ANALYSISCHANNELCUT['e'], 
        'mu'    : '-c "%s"'%ANALYSISCHANNELCUT['mu'], 
        'ee'    : '-c "%s"'%ANALYSISCHANNELCUT['ee'], 
        'emu'   : '-c "%s"'%ANALYSISCHANNELCUT['emu'], 
        'mumu'  : '-c "%s"'%ANALYSISCHANNELCUT['mumu']
    }
}
# -- MC --
ANALYSISCUT['mc']={}
for y in ANALYSISTRIGGERMC:
    ANALYSISCUT['mc'][y]={}
    for c in ANALYSISTRIGGERMC[y]:
        ANALYSISCUT['mc'][y][c]="--cut %s&&%s"%(ANALYSISTRIGGERMC[y][c],ANALYSISCHANNELCUT[c]) # for MC (no json applied)
# -- DATA --
ANALYSISCUT['data']={}
for y in ANALYSISTRIGGERDATA:
    ANALYSISCUT['data'][y]={}
    for c in ANALYSISTRIGGERDATA[y]:
        ANALYSISCUT['data'][y][c]="--cut %s&&%s --json %s"%(ANALYSISTRIGGERDATA[y][c],ANALYSISCHANNELCUT[c],cmssw+'/src/BsTauTau/nanoSkimmer/dataset/'+ANALYSISGRL[y]) # for data (json applied)
