# BsTauTauAnalyzer

## Setup

```
mkdir MyWorkingDirectory
cd MyWorkingDirectory
cmsrel CMSSW_15_0_10
cd CMSSW_15_0_10/src/
cmsenv
git cms-init
git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
git clone https://github.com/cecilecaillol/BsTauTauAnalyzer.git -b Run3
scram b -j 8
```
> IMPORTANT In order to add **pileup weights** do the following (currently working only for Run2 UL)

Edit `$CMSSW_BASE/src/PhysicsTools/NanoAODTools/scripts/nano_postproc.py` insert this line after `L2`:
```python
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
```
and after `L72` insert
```python
    # PU weights - Run2 only -
    for mod, names in options.imports:
        if "mc" in names or "sig" in names:
            if "2018" in names:
                modules.append(puAutoWeight_UL2018())
            if "2017" in names:
                modules.append(puAutoWeight_UL2017())
            if "2016" in names:
                modules.append(puAutoWeight_UL2016())
```
Edit `L63` of `$CMSSW_BASE/src/PhysicsTools/NanoAODTools/python/postprocessing/modules/common/puWeightProducer.py` into `hist.SetDirectory(ROOT.nullptr)`.

## Run locally

Run the skimmer command locally, e.g. for a signal MC file in the `emu` $t\bar t$-channel. The `-I` options accept any module defined at the end of the [python/Flattener_analysis.py](python/Flattener_analysis.py) script.

```bash
python3 $CMSSW_BASE/src/PhysicsTools/NanoAODTools/scripts/nano_postproc.py \
 output \
 /eos/cms/store/group/phys_bphys/cbasile/BsTauTau-ttbar/nanov15_UParTditau/crabjobs_2026Jul11/ttbarToBsToTauTau_BsFilter_TauTauFilter_TuneCP5_13TeV-pythia8-evtgen/ttbarToBsToTauTau_RunIIUL18_nanoAODv15_v1/260710_222737/0000/step_nanoAODv15_10.root \
 --bi $CMSSW_BASE/src/BsTauTau/nanoSkimmer/scripts/keep_in.txt \
 --bo $CMSSW_BASE/src/BsTauTau/nanoSkimmer/scripts/keep_out.txt \
 -c "(nMuon>0&&nElectron>0&&nJet>0)" -I BsTauTau.nanoSkimmer.Flattener_analysis analysis_emumc2018 -N 1000
```

## Submit jobs via condor

Submit the skimmer on `HTCondor` via `runNtuplizer.py`. Reads the input datasets form a text file, each line points to a directory containing the .root files to process.
One Condor job is built per directory and per $t\bar t$-channel (`e`, `mu`, `ee`, `emu`, `mumu`).

Each job is written into a
`FarmLocalNtuple_<year>[_<tag>]_<timestamp>/` directory (condor `.sub` + worker script + logs),
alongside a `submitter.sh` that submits them all.

### Options

| Option | Description | Default |
|---|---|---|
| `-i`, `--input` | text file listing input dataset directories (one EOS path per line, no trailing `/`, `#` = comment) | `listSamplesMC2018.txt` |
| `-y`, `--year` | data-taking year — selects trigger/GRL/cuts from `EraConfig.py` | `2018` |
| `-o`, `--out` | output EOS directory for the skimmed ntuples | `/eos/.../test2018/` |
| `-n`, `--nfiles` | max number of files to process per dataset (`-1` = all) | `-1` |
| `--isdata` | run on data (applies GRL + data trigger) instead of MC | off |
| `--filter` | glob filter (fnmatch) applied to dataset lines in the input list | `*` |
| `-t`, `--tag` | extra tag appended to the Farm directory name | none |
| `-s`, `--submit` | actually `condor_submit` the jobs (otherwise dry-run only) | off |
| `-f`, `--force` | force resubmission (currently unused / FIXME in the script) | off |

**Example: skim a demo MC dataset list for 2018 (2 files/dataset, dry-run)**

```bash
cd scripts
voms-proxy-init --voms=cms --valid=48:0
python3 runNtuplizer.py \
  --input ../dataset/mc/nanoAODmc2018_ParTedge_Jul26-demo.txt \
  -y 2018 \
  --out /eos/cms/store/group/phys_bphys/cbasile/BsTauTau-ttbar/nanov15_skim/ \
  -n 2
```

This generates `FarmLocalNtuple_2018_<timestamp>/` with one condor submission file and
worker script per dataset/channel found in the input list, plus a `submitter.sh`.
Without `-s`/`--submit` nothing is actually sent to condor — inspect the generated
files, then either add `-s` to the command or run `source submitter.sh` yourself.

Input dataset lists live under `dataset/mc/` (MC) and `dataset/` (data), one EOS
directory per line — see e.g. `dataset/mc/nanoAODmc2018_ParTedge_Jul26-demo.txt`.

### Post-job checks and output `hadd`

Check if all jobs were succesful and produced the expected output using [scripts/runPostJob.py](scripts/runPostJob.py). It takes the same input txt file as `runNtuplizer.py` and cheks if all the files were produced and if they are broken.
```bash
python3 runPostJob.py --input ../dataset/mc/nanoAODmc2018_ParTedge_Jul26-demo.txt --channel mumu --filter="*TTToBsToTauTau*" -o /eos/cms/store/group/phys_bphys/cbasile/BsTauTau-ttbar/nanov15_skim/
```
If all the jobs are succesful you can `hadd` the output with the scripts contained in [scripts/to_runHadd/](scripts/to_runHadd/)
