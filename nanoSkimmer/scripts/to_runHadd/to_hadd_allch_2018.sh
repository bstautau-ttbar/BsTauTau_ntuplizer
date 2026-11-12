# $!/bin/bash
BASE=$CMSSW_BASE/src/BsTauTau/nanoSkimmer/scripts/
DATADIR_BASE=/eos/cms/store/group/phys_bphys/cbasile/BsTauTau-ttbar/nanov15_skim/
YEAR="2018"
TAG="tagMreg-v0"
#TOFORCE="--force"


CHANNEL=()
echo "---- HADDING MC IN ALL CHANNELS ----"
for channel in emu mumu ee e mu; do
#for channel in emu ; do
    echo "---- Processing channel: $channel ----"
    DATADIR="${DATADIR_BASE}/${channel}_${YEAR}_${TAG}"
    OUTDIR=$DATADIR
    ## - Bs->tau tau -
    python3 ${BASE}runHadd.py --inputDir="${DATADIR}/ttbarToBsToTauTau*/ttbarToBsToTauTau[-ext_]*RunIIUL18_nanoAODv15_000*_${channel}/"      -o ${OUTDIR}/ttbarToBsToTauTau.root $TOFORCE
    ## - TTBAR -
    python3 ${BASE}runHadd.py --inputDir="${DATADIR}/TTTo2L2Nu/TTTo2L2Nu_RunIIUL18_nanoAODv15_000*_${channel}/"                 -o ${OUTDIR}/TTTo2L2Nu.root $TOFORCE
    python3 ${BASE}runHadd.py --inputDir="${DATADIR}/TTToSemiLeptonic/TTToSemiLeptonic_RunIIUL18_nanoAODv15_000*_${channel}/"   -o ${OUTDIR}/TTToSemileptonic.root $TOFORCE
    python3 ${BASE}runHadd.py --inputDir="${DATADIR}/TTToHadronic/TTToHadronic_RunIIUL18_nanoAODv15_000*_${channel}/"           -o ${OUTDIR}/TTToHadronic.root $TOFORCE
    ## - SINGLE TOP -
    python3 ${BASE}runHadd.py --inputDir="${DATADIR}/ST/ST_s_RunIIUL18_nanoAODv15_000*_${channel}/"      -o ${OUTDIR}/ST_s.root $TOFORCE
    python3 ${BASE}runHadd.py --inputDir="${DATADIR}/ST/ST_t_RunIIUL18_nanoAODv15_000*_${channel}/"      -o ${OUTDIR}/ST_t_top.root $TOFORCE
    python3 ${BASE}runHadd.py --inputDir="${DATADIR}/ST/ST_antit_RunIIUL18_nanoAODv15_000*_${channel}/"  -o ${OUTDIR}/ST_t_antitop.root $TOFORCE
    python3 ${BASE}runHadd.py --inputDir="${DATADIR}/ST/ST_tw_RunIIUL18_nanoAODv15_000*_${channel}/"     -o ${OUTDIR}/ST_tW.root $TOFORCE
    python3 ${BASE}runHadd.py --inputDir="${DATADIR}/ST/ST_antitw_RunIIUL18_nanoAODv15_000*_${channel}/" -o ${OUTDIR}/ST_tW_antitop.root $TOFORCE
    ## - DY -
    python3 ${BASE}runHadd.py --inputDir="${DATADIR}/DY*/DY[ext_]*RunIIUL18_nanoAODv15_000*_${channel}/"    -o ${OUTDIR}/DY.root $TOFORCE
    ### - W+jets -
    python3 ${BASE}runHadd.py --inputDir="${DATADIR}/W*/W[ext_]*RunIIUL18_nanoAODv15_000*_${channel}/"    -o ${OUTDIR}/W.root $TOFORCE
    ## - DIBOSON -
    python3 ${BASE}runHadd.py --inputDir="${DATADIR}/WW/WW_RunIIUL18_nanoAODv15_000*_${channel}/" -o ${OUTDIR}/WW.root $TOFORCE
    python3 ${BASE}runHadd.py --inputDir="${DATADIR}/WZ/WZ_RunIIUL18_nanoAODv15_000*_${channel}/" -o ${OUTDIR}/WZ.root $TOFORCE
    python3 ${BASE}runHadd.py --inputDir="${DATADIR}/ZZ/ZZ_RunIIUL18_nanoAODv15_000*_${channel}/" -o ${OUTDIR}/ZZ.root $TOFORCE
    echo " "
done


## - DATA -
echo "---- HADDING DATA CHANNEL SPECIFIC ----"
echo "---- EGAMMA ----"
for channel in emu ee e; do
    DATADIR="${DATADIR_BASE}/${channel}_${YEAR}_${TAG}"
    OUTDIR=$DATADIR
    python3 ${BASE}runHadd.py --inputDir="${DATADIR}/EGamma/EGamma_2018A_RunIIUL18_nanoAODv15_00**_${channel}/" -o ${OUTDIR}/EGammaA.root $TOFORCE --isdata
    python3 ${BASE}runHadd.py --inputDir="${DATADIR}/EGamma/EGamma_2018B_RunIIUL18_nanoAODv15_00**_${channel}/" -o ${OUTDIR}/EGammaB.root $TOFORCE --isdata
    python3 ${BASE}runHadd.py --inputDir="${DATADIR}/EGamma/EGamma_2018C_RunIIUL18_nanoAODv15_00**_${channel}/" -o ${OUTDIR}/EGammaC.root $TOFORCE --isdata
    #python3 ${BASE}runHadd.py --inputDir="${DATADIR}/EGamma/EGamma_2018D_RunIIUL18_nanoAODv15_00**_${channel}/" -o ${OUTDIR}/EGammaD.root $TOFORCE --isdata
    echo " "
done
    
echo "---- SINGLE MUON ----"
for channel in emu mumu mu; do
    DATADIR="${DATADIR_BASE}/${channel}_${YEAR}_${TAG}"
    OUTDIR=$DATADIR
    python3 ${BASE}runHadd.py --inputDir="${DATADIR}/SingleMuon/SingleMuon_2018A_RunIIUL18_nanoAODv15_00**_${channel}/" -o ${OUTDIR}/SingleMuonA.root $TOFORCE --isdata
    python3 ${BASE}runHadd.py --inputDir="${DATADIR}/SingleMuon/SingleMuon_2018B_RunIIUL18_nanoAODv15_00**_${channel}/" -o ${OUTDIR}/SingleMuonB.root $TOFORCE --isdata
    python3 ${BASE}runHadd.py --inputDir="${DATADIR}/SingleMuon/SingleMuon_2018C_RunIIUL18_nanoAODv15_00**_${channel}/" -o ${OUTDIR}/SingleMuonC.root $TOFORCE --isdata
    python3 ${BASE}runHadd.py --inputDir="${DATADIR}/SingleMuon/SingleMuon_2018D_RunIIUL18_nanoAODv15_00**_${channel}/" -o ${OUTDIR}/SingleMuonD.root $TOFORCE --isdata
    echo " "
done

echo "---- DOUBLE MUON ----"
for channel in mumu; do
    DATADIR="${DATADIR_BASE}/${channel}_${YEAR}_${TAG}"
    OUTDIR=$DATADIR
    python3 ${BASE}runHadd.py --inputDir="${DATADIR}/DoubleMuon/DoubleMuon_2018A_None_nanoAODv15_000*_${channel}/" -o ${OUTDIR}/DoubleMuonA.root $TOFORCE --isdata
    python3 ${BASE}runHadd.py --inputDir="${DATADIR}/DoubleMuon/DoubleMuon_2018B_None_nanoAODv15_000*_${channel}/" -o ${OUTDIR}/DoubleMuonB.root $TOFORCE --isdata
    python3 ${BASE}runHadd.py --inputDir="${DATADIR}/DoubleMuon/DoubleMuon_2018C_None_nanoAODv15_000*_${channel}/" -o ${OUTDIR}/DoubleMuonC.root $TOFORCE --isdata
    python3 ${BASE}runHadd.py --inputDir="${DATADIR}/DoubleMuon/DoubleMuon_2018D_None_nanoAODv15_000*_${channel}/" -o ${OUTDIR}/DoubleMuonD.root $TOFORCE --isdata
    echo " "
done

echo "---- MUON-EG ----"
for channel in emu; do
    DATADIR="${DATADIR_BASE}/${channel}_${YEAR}_${TAG}"
    OUTDIR=$DATADIR
    python3 ${BASE}runHadd.py --inputDir="${DATADIR}/MuonEG/MuonEG_2018A_None_nanoAODv15_000*_${channel}/" -o ${OUTDIR}/MuonEGA.root $TOFORCE --isdata
    python3 ${BASE}runHadd.py --inputDir="${DATADIR}/MuonEG/MuonEG_2018B_None_nanoAODv15_000*_${channel}/" -o ${OUTDIR}/MuonEGB.root $TOFORCE --isdata
    python3 ${BASE}runHadd.py --inputDir="${DATADIR}/MuonEG/MuonEG_2018C_None_nanoAODv15_000*_${channel}/" -o ${OUTDIR}/MuonEGC.root $TOFORCE --isdata
    python3 ${BASE}runHadd.py --inputDir="${DATADIR}/MuonEG/MuonEG_2018D_None_nanoAODv15_000*_${channel}/" -o ${OUTDIR}/MuonEGD.root $TOFORCE --isdata
    echo " "
done 
echo "-- DONE --"
