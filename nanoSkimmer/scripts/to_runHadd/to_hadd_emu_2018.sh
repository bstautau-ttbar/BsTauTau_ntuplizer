# $!/bin/bash
DATADIR=/eos/cms/store/group/phys_bphys/cbasile/BsTauTau-ttbar/test2018-v2
OUTDIR=/eos/cms/store/group/phys_bphys/cbasile/BsTauTau-ttbar/test2018-v2/flat_ntuples/ntuples_emu_2018_ParT
TOFORCE="--force"

## - Bs->tau tau -
python2 runHadd.py --inputDir="${DATADIR}/crab_bstautau_0000_emu/" -o ${OUTDIR}/ttbarToBsToTauTau.root $TOFORCE
## - DY -
python2 runHadd.py --inputDir="${DATADIR}/crab_dy_000*_emu/"    -o ${OUTDIR}/DY.root $TOFORCE
python2 runHadd.py --inputDir="${DATADIR}/crab_dyext_000*_emu/" -o ${OUTDIR}/DY_ext.root $TOFORCE
## - SINGLE TOP -
python2 runHadd.py --inputDir="${DATADIR}/crab_st_s_000*_emu/"      -o ${OUTDIR}/ST_s.root $TOFORCE
#python2 runHadd.py --inputDir="${DATADIR}/crab_st_t_000*_emu/"      -o ${OUTDIR}/ST_t_top.root $TOFORCE
python2 runHadd.py --inputDir="${DATADIR}/crab_st_antit_000*_emu/"  -o ${OUTDIR}/ST_t_antitop.root $TOFORCE
python2 runHadd.py --inputDir="${DATADIR}/crab_st_tw_000*_emu/"     -o ${OUTDIR}/ST_tW.root $TOFORCE
python2 runHadd.py --inputDir="${DATADIR}/crab_st_antitw_000*_emu/" -o ${OUTDIR}/ST_tW_antitop.root $TOFORCE
## - TTBAR -
python2 runHadd.py --inputDir="${DATADIR}/crab_tt_fullylep_000*_emu/"  -o ${OUTDIR}/TTTo2L2Nu.root $TOFORCE
python2 runHadd.py --inputDir="${DATADIR}/crab_tt_semilep_000*_emu/"   -o ${OUTDIR}/TTToSemileptonic.root $TOFORCE
python2 runHadd.py --inputDir="${DATADIR}/crab_tt_had_000*_emu/"       -o ${OUTDIR}/TTToHadronic.root $TOFORCE
## - W+jets -
python2 runHadd.py --inputDir="${DATADIR}/crab_w_000*_emu/"    -o ${OUTDIR}/W.root $TOFORCE
python2 runHadd.py --inputDir="${DATADIR}/crab_wext_000*_emu/" -o ${OUTDIR}/W_ext.root $TOFORCE
## - DIBOSON -
python2 runHadd.py --inputDir="${DATADIR}/crab_ww_000*_emu/" -o ${OUTDIR}/WW.root $TOFORCE
python2 runHadd.py --inputDir="${DATADIR}/crab_wz_000*_emu/" -o ${OUTDIR}/WZ.root $TOFORCE
python2 runHadd.py --inputDir="${DATADIR}/crab_zz_000*_emu/" -o ${OUTDIR}/ZZ.root $TOFORCE

# - DATA -
python2 runHadd.py --inputDir="${DATADIR}/crab_SingleMuA_000*_emu/" -o ${OUTDIR}/SingleMuonA.root $TOFORCE
python2 runHadd.py --inputDir="${DATADIR}/crab_SingleMuB_000*_emu/" -o ${OUTDIR}/SingleMuonB.root $TOFORCE
python2 runHadd.py --inputDir="${DATADIR}/crab_SingleMuC_000*_emu/" -o ${OUTDIR}/SingleMuonC.root $TOFORCE
python2 runHadd.py --inputDir="${DATADIR}/crab_SingleMuD_000*_emu/" -o ${OUTDIR}/SingleMuonD.root $TOFORCE

python2 runHadd.py --inputDir="${DATADIR}/crab_egammaA_000*_emu/" -o ${OUTDIR}/EGammaA.root $TOFORCE
python2 runHadd.py --inputDir="${DATADIR}/crab_egammaB_000*_emu/" -o ${OUTDIR}/EGammaB.root $TOFORCE
python2 runHadd.py --inputDir="${DATADIR}/crab_egammaC_000*_emu/" -o ${OUTDIR}/EGammaC.root $TOFORCE
python2 runHadd.py --inputDir="${DATADIR}/crab_egammaD_000*_emu/" -o ${OUTDIR}/EGammaD.root $TOFORCE

python2 runHadd.py --inputDir="${DATADIR}/crab_muonEGA_0000_emu/" -o ${OUTDIR}/MuonEGA.root $TOFORCE
python2 runHadd.py --inputDir="${DATADIR}/crab_muonEGB_0000_emu/" -o ${OUTDIR}/MuonEGB.root $TOFORCE
python2 runHadd.py --inputDir="${DATADIR}/crab_muonEGC_0000_emu/" -o ${OUTDIR}/MuonEGC.root $TOFORCE
python2 runHadd.py --inputDir="${DATADIR}/crab_muonEGD_0000_emu/" -o ${OUTDIR}/MuonEGD.root $TOFORCE
