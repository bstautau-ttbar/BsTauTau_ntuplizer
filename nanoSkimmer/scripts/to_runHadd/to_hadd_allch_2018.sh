# $!/bin/bash
BASE=$CMSSW_BASE/src/BsTauTau/nanoSkimmer/scripts/
DATADIR_BASE=/eos/cms/store/cmst3/group/bpark/bstautau/nanov15_skim/
CHANNEL=("emu" "mumu" "ee" "e" "mu")
CHANNEL=("e")
YEAR="2018"
TAG="tagMreg"
#TOFORCE="--force"

for channel in "${CHANNEL[@]}"
do
    echo "---- Processing channel: $channel ----"
    DATADIR="${DATADIR_BASE}/${channel}_${YEAR}_${TAG}"
    OUTDIR=$DATADIR
    ## - Bs->tau tau -
    python3 ${BASE}runHadd.py --inputDir="${DATADIR}/ttbarToBsToTauTau/ttbarToBsToTauTau_RunIIUL18_nanoAODv15_0000_${channel}/"      -o ${OUTDIR}/ttbarToBsToTauTau.root $TOFORCE
    python3 ${BASE}runHadd.py --inputDir="${DATADIR}/ttbarToBsToTauTau-ext/ttbarToBsToTauTau-ext_RunIIUL18_nanoAODv15_0000_${channel}/" -o ${OUTDIR}/ttbarToBsToTauTau_ext.root $TOFORCE
    ### - DY -
    #python3 ${BASE}runHadd.py --inputDir="${DATADIR}/crab_dy_000*_emu/"    -o ${OUTDIR}/DY.root $TOFORCE
    #python3 ${BASE}runHadd.py --inputDir="${DATADIR}/crab_dyext_000*_emu/" -o ${OUTDIR}/DY_ext.root $TOFORCE
    ### - SINGLE TOP -
    #python3 ${BASE}runHadd.py --inputDir="${DATADIR}/crab_st_s_000*_emu/"      -o ${OUTDIR}/ST_s.root $TOFORCE
    ##python3 ${BASE}runHadd.py --inputDir="${DATADIR}/crab_st_t_000*_emu/"      -o ${OUTDIR}/ST_t_top.root $TOFORCE
    #python3 ${BASE}runHadd.py --inputDir="${DATADIR}/crab_st_antit_000*_emu/"  -o ${OUTDIR}/ST_t_antitop.root $TOFORCE
    #python3 ${BASE}runHadd.py --inputDir="${DATADIR}/crab_st_tw_000*_emu/"     -o ${OUTDIR}/ST_tW.root $TOFORCE
    #python3 ${BASE}runHadd.py --inputDir="${DATADIR}/crab_st_antitw_000*_emu/" -o ${OUTDIR}/ST_tW_antitop.root $TOFORCE
    ## - TTBAR -
    python3 ${BASE}runHadd.py --inputDir="${DATADIR}/TTTo2L2Nu/TTTo2L2Nu_RunIIUL18_nanoAODv15_000*_${channel}/"                 -o ${OUTDIR}/TTTo2L2Nu.root $TOFORCE
    python3 ${BASE}runHadd.py --inputDir="${DATADIR}/TTToSemiLeptonic/TTToSemiLeptonic_RunIIUL18_nanoAODv15_000*_${channel}/"   -o ${OUTDIR}/TTToSemileptonic.root $TOFORCE
    python3 ${BASE}runHadd.py --inputDir="${DATADIR}/TTToHadronic/TTToHadronic_RunIIUL18_nanoAODv15_000*_${channel}/"           -o ${OUTDIR}/TTToHadronic.root $TOFORCE
    ### - W+jets -
    #python3 ${BASE}runHadd.py --inputDir="${DATADIR}/crab_w_000*_emu/"    -o ${OUTDIR}/W.root $TOFORCE
    #python3 ${BASE}runHadd.py --inputDir="${DATADIR}/crab_wext_000*_emu/" -o ${OUTDIR}/W_ext.root $TOFORCE
    ### - DIBOSON -
    #python3 ${BASE}runHadd.py --inputDir="${DATADIR}/crab_ww_000*_emu/" -o ${OUTDIR}/WW.root $TOFORCE
    #python3 ${BASE}runHadd.py --inputDir="${DATADIR}/crab_wz_000*_emu/" -o ${OUTDIR}/WZ.root $TOFORCE
    #python3 ${BASE}runHadd.py --inputDir="${DATADIR}/crab_zz_000*_emu/" -o ${OUTDIR}/ZZ.root $TOFORCE
    #
    ## - DATA -
    #python3 ${BASE}runHadd.py --inputDir="${DATADIR}/crab_SingleMuA_000*_emu/" -o ${OUTDIR}/SingleMuonA.root $TOFORCE
    #python3 ${BASE}runHadd.py --inputDir="${DATADIR}/crab_SingleMuB_000*_emu/" -o ${OUTDIR}/SingleMuonB.root $TOFORCE
    #python3 ${BASE}runHadd.py --inputDir="${DATADIR}/crab_SingleMuC_000*_emu/" -o ${OUTDIR}/SingleMuonC.root $TOFORCE
    #python3 ${BASE}runHadd.py --inputDir="${DATADIR}/crab_SingleMuD_000*_emu/" -o ${OUTDIR}/SingleMuonD.root $TOFORCE
    #
    #python3 ${BASE}runHadd.py --inputDir="${DATADIR}/crab_egammaA_000*_emu/" -o ${OUTDIR}/EGammaA.root $TOFORCE
    #python3 ${BASE}runHadd.py --inputDir="${DATADIR}/crab_egammaB_000*_emu/" -o ${OUTDIR}/EGammaB.root $TOFORCE
    #python3 ${BASE}runHadd.py --inputDir="${DATADIR}/crab_egammaC_000*_emu/" -o ${OUTDIR}/EGammaC.root $TOFORCE
    #python3 ${BASE}runHadd.py --inputDir="${DATADIR}/crab_egammaD_000*_emu/" -o ${OUTDIR}/EGammaD.root $TOFORCE
    #
    #python3 ${BASE}runHadd.py --inputDir="${DATADIR}/crab_muonEGA_0000_emu/" -o ${OUTDIR}/MuonEGA.root $TOFORCE
    #python3 ${BASE}runHadd.py --inputDir="${DATADIR}/crab_muonEGB_0000_emu/" -o ${OUTDIR}/MuonEGB.root $TOFORCE
    #python3 ${BASE}runHadd.py --inputDir="${DATADIR}/crab_muonEGC_0000_emu/" -o ${OUTDIR}/MuonEGC.root $TOFORCE
    #python3 ${BASE}runHadd.py --inputDir="${DATADIR}/crab_muonEGD_0000_emu/" -o ${OUTDIR}/MuonEGD.root $TOFORCE
    echo ""
done   
