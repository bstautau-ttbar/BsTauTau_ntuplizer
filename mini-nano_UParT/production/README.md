# CRAB production
First sources the CRAB client (`/cvmfs/cms.cern.ch/crab3/crab.sh`) and starts a voms proxy:
```bash
source setupCRAB.sh
```
Do this once per session, before running `dasgoclient` queries or submitting jobs.

## Fill in the `.yaml` files with dataset information

Samples are described in a `.yaml` file under `../dataset/` (see [`mc_RunIIUL18-miniAODv2.yaml`](../dataset/mc_RunIIUL18-miniAODv2.yaml) as a reference). The file has two top-level blocks:

```yaml
common:
  mc:                                       # defaults applied to every isMC: True sample
    splitting: 1                            # default CRAB unitsPerJob
    globaltag: 150X_mc2018_realistic_v1
    campaign: RunIIUL18                     # used to build the outputDatasetTag

samples:
  <sample_key>:                             # used as CRAB requestName / process name
    dataset: /A/B/MINIAODSIM                # full DAS dataset path (input to CRAB)
    isMC: True                              # True -> uses common.mc, False -> common.data
    splitting: 1                            # optional, overrides common.<mc|data>.splitting
    name: short_label                       # short label (not used for the moment)
```

Guidelines:
- `<sample_key>` (e.g. `ttbarToBsToTauTau-ext`) is what you pass to
  `multisubmitter_CRAB.py --filter` to select which sample(s) to submit.
- `dataset` must be the exact DAS path of the MINIAODSIM/MINIAOD dataset.
- Add a new entry per sample/extension you want to produce; group them under
  comments (`# TTBAR`, `# DY`, ...) as done in the example file.
- Add a `data:` block under `common` the same way as `mc:` if/when data
  samples are added (`isMC: False`).
- Check if the dataset exists and tune the splitting using `fetch_info_dataset.py`. It warns if a dataset has more files than CRAB can handle in a single task
(`MAXCRABFILES = 10000`), in which case you'll need to split the submission. See the examples below.

Query one or more samples defined in the dataset `.yaml`:
```bash
python3 fetch_info_dataset.py --dataset_yml ../dataset/mc_RunIIUL18-miniAODv2.yaml \
    --dataset_keys ttbarToBsToTauTau-ext TTToSemiLeptonic
```
Or query a single DAS dataset path directly, without a `.yaml` file:
```bash
python3 fetch_info_dataset.py --central_dataset /TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM
```

## Submit on CRAB

`multisubmitter_CRAB.py` loops over the samples in the `.yaml` file (matching `--filter`) and submits one CRAB task per sample, using the same PSet config (`--config`, produced as described in the main [README](../README.md)) for all of them.

Example: submit only the `ttbarToBsToTauTau` simulated sample(s) as production `v1`:
```bash
python3 multisubmitter_CRAB.py --dataset ../dataset/mc_RunIIUL18-miniAODv2.yaml \
    --filter="ttbarToBsToTauTau*" \
    --config ../test/run_nanoUL18_150X_mc_cfg.py \
    --output_dir /store/group/cmst3/group/bpark/bstautau/nanoAODv15_<some-folder>/ \
    -v 1
```
Example: submit only the `SingleMuon` dataset containing data as production `v1`:
```bash
python3 multisubmitter_CRAB.py --dataset ../dataset/data_RunIIUL18-miniAODv2.yaml \
  --filter="SingleMuon*" \
  --config ../test/run_nanoUL18_150X_data_cfg.py \
  --output_dir /store/group/cmst3/group/bpark/bstautau/nanoAODv15_<some-folder>/ \
  -v 1
```
Add `--dryrun` first to sanity-check the generated CRAB configuration before actually submitting.
