# MiniAOD → NanoAOD ntuplizer for $B_s\to\tau\tau$

1. `mini-nano_UParT` : convert miniAOD to custom nanoAOD adding the jet-branch with the *boosted di-tau tagger* score
1. `nanoSkimmer`: skim the resulting nanoAOD and split the dataset into $t\bar t$ channels

## One-time setup
USe `lxplus8` or access the singularity with `cmssw-el8`
```bash
mkdir <my-working-dir>
cd <my-working-dir> 
```

```bash
export SCRAM_ARCH=el8_amd64_gcc12
cmsrel CMSSW_15_0_18
cd CMSSW_15_0_18/src/
cmsenv
git cms-init

git cms-addpkg PhysicsTools/NanoAOD
git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
git cms-addpkg PhysicsTools/PatAlgos
git cms-addpkg RecoBTag

# changes with new parT branches
git cms-merge-topic -u elenavernazza:MyParT_CMSSW_15_0_18

# IMPORTANT: get this repo and save it in BsTauTau folder 
git clone --recursive git@github.com:bstautau-ttbar/BsTauTau_ntuplizer.git -n nanoAODv15 BsTauTau

# compile
scram b -j8
```

