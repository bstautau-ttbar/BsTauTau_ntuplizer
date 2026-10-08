# Run NanoAODs adding our parT branch

## Setup environment
Copy the models in the right directory
```bash
cd $CMSSW_BASE/src/BsTauTau/mini-nano_UParT 
mkdir -p $CMSSW_BASE/src/RecoBTag/Combined/data/UParTAK4/PUPPI/BsTauTau/
cp onnx_models/part_run3_bstautau_btag_edge_sumref.onnx $CMSSW_BASE/src/RecoBTag/Combined/data/UParTAK4/PUPPI/BsTauTau/
cp onnx_models/UParT_v0_mass_reg.onnx $CMSSW_BASE/src/RecoBTag/Combined/data/UParTAK4/PUPPI/BsTauTau/
```

## Run locally
Produce the config file to run on miniAOD and in clude the jet-branch with the UParT models inference. E.g. for **UL 2018 MC** run:
``` bash
cmsDriver.py --step NANO:@BTV \
 --eventcontent NANOAODSIM --datatier NANOAODSIM \
 --customise Configuration/DataProcessing/Utils.addMonitoring \
 --customise_commands 'process.NANOAODSIMoutput.outputCommands += ["drop nanoaodFlatTable_pfCandTable_*_*","drop nanoaodFlatTable_jetPFCandTable_*_*","drop nanoaodFlatTable_fatJetPFCandTable_*_*"]' \
 --nThreads 2 \
 --conditions 150X_mc2018_realistic_v1 --era Run2_2018,run2_nanoAOD_106Xv2 \
 --python_filename run_nanobtvUL18_150X_mc_cfg.py \
 --fileout file:step_nanoAODv15.root \
 --filein "dbs:/ttbarToBsToTauTau_BsFilter_TauTauFilter_TuneCP5_13TeV-pythia8-evtgen/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM" \
 -n 100 --mc --no_exec
```
for **UL 2018 DATA** run:
```bash
cmsDriver.py --step NANO:@BTV \
 --eventcontent NANOAOD --datatier NANOAOD \
 --customise Configuration/DataProcessing/Utils.addMonitoring \
 --customise_commands 'process.NANOAODoutput.outputCommands += ["drop nanoaodFlatTable_pfCandTable_*_*","drop nanoaodFlatTable_jetPFCandTable_*_*","drop nanoaodFlatTable_fatJetPFCandTable_*_*"]' \
 --nThreads 2 \
 --conditions 150X_dataRun2_v1 --era Run2_2018,run2_nanoAOD_106Xv2 \
 --python_filename run_nanobtvUL18_150X_data_cfg.py \
 --fileout file:step_nanoAODv15.root \
 --filein "/store/data/Run2018A/SingleMuon/MINIAOD/UL2018_MiniAODv2_GT36-v2/60000/083624A7-087B-6743-A634-329E30A579DA.root" \
 -n 100 --no_exec
```
and test it with
```bash
 cmsRun run_nanobtvUL18_150X_mc_cfg.py # or run_nanobtvUL18_150X_data_cfg.py
```


The config file already produced are in the `test/` folder you can test them locally with `cmsRun`.

New jet-branches for the di-tau tagger are `Jet_btagMyUParTditaue`, `Jet_btagMyUParTditauh`, `Jet_btagMyUParTditaumu`, `Jet_btagMyUParTprobb`, `Jet_btagMyUParTprobc` and `Jet_btagMyUParTprobother`. 
New jet-branche for the jet mass regression is `Jet_UParTRegMassCentral`.

## Submission on CRAB

If not available, you need to prepare a `.yaml` file with the dataset informations. Use `fetch_info_dataset.py` and `multisubmitter_CRAB.py` in `production/` to check the datasets on DAS and submit one CRAB task per sample. See [`production/README.md`](production/README.md) for the full instructions.
