# Run NanoAODs adding our parT branch

## Setup environment
Copy the model in the right directory
```bash
cd $CMSSW_BASE/src/BsTauTau 
mkdir -p $CMSSW_BASE/src/RecoBTag/Combined/data/UParTAK4/PUPPI/BsTauTau/
cp onnx_models/part_run3_bstautau_btag_edge_sumref.onnx $CMSSW_BASE/src/RecoBTag/Combined/data/UParTAK4/PUPPI/BsTauTau/
cp onnx_models/UParT_v0_mass_reg.onnx $CMSSW_BASE/src/RecoBTag/Combined/data/UParTAK4/PUPPI/BsTauTau/
```

## Run locally
Produce the config file to run on miniAOD and in clude the jet-branch with the UParT model inference. E.g. for UL 2018 run:
``` bash
cmsDriver.py --step NANO:@BTV \
 --eventcontent NANOAODSIM --datatier NANOAODSIM \
 --customise Configuration/DataProcessing/Utils.addMonitoring \
 --conditions 150X_mc2018_realistic_v1 --era Run2_2018,run2_nanoAOD_106Xv2 \
 --python_filename run_nanobtvUL18_150X_cfg.py \
 --fileout file:step_nanoAODv15.root \
 --filein "dbs:/ttbarToBsToTauTau_BsFilter_TauTauFilter_TuneCP5_13TeV-pythia8-evtgen/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM" \
 -n 100 --mc --no_exec
 # and run it
 cmsRun run_nanobtvUL18_150X_cfg.py
```
The config file already produced are in the `test/` folder you can test them locally with `cmsRun`.

## Submission on CRAB

If not available, you need to prepare a `.yaml` file with the dataset informations. Use `fetch_info_dataset.py` and `multisubmitter_CRAB.py` in `production/` to check the datasets on DAS and submit one CRAB task per sample. See [`production/README.md`](production/README.md) for the full instructions.