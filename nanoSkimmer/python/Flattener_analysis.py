#!/usr/bin/env python
import os, sys, math
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
import correctionlib as _core

from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection

### Proton selector be replaced by preprocessing module
from BsTauTau.nanoSkimmer.objectSelector import ElectronSelector, MuonSelector, TauSelector, GenParticleSelector

DEBUGMODE=False
class Analysis(Module):
    def __init__(self, channel, isMC, year):
        self.channel       = channel
        self.isMC          = isMC
        self.year          = year

        cmssw=os.environ['CMSSW_BASE']
        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
    
        self.out = wrappedOutputTree

	# declare branches

        if self.channel=="mu" or self.channel=="mumu" or self.channel=="emu":
           self.out.branch("mu1_pt",            "F")
           self.out.branch("mu1_eta",           "F")
           self.out.branch("mu1_phi",           "F")
           self.out.branch("mu1_dxy",           "F")
           self.out.branch("mu1_dz",            "F")
           self.out.branch("mu1_charge",        "F")
           self.out.branch("mu1_tightId",       "I")
           self.out.branch("mu1_iso",           "F")
           self.out.branch("mu1_singletrg",     "I")
           self.out.branch("mu1_crosstrg",      "I")
           self.out.branch("mu1_doubletrg",     "I")

        if self.channel=="mumu":
           self.out.branch("mu2_pt",            "F")
           self.out.branch("mu2_eta",           "F")
           self.out.branch("mu2_phi",           "F")
           self.out.branch("mu2_dxy",           "F")
           self.out.branch("mu2_dz",            "F")
           self.out.branch("mu2_charge",        "F")
           self.out.branch("mu2_tightId",       "I")
           self.out.branch("mu2_iso",           "F")
           self.out.branch("mu2_singletrg",     "I")
           self.out.branch("mu2_crosstrg",      "I")
           self.out.branch("mu2_doubletrg",     "I")

        if self.channel=="e" or self.channel=="ee" or self.channel=="emu":
           self.out.branch("e1_pt",            "F")
           self.out.branch("e1_eta",           "F")
           self.out.branch("e1_phi",           "F")
           self.out.branch("e1_dxy",           "F")
           self.out.branch("e1_dz",            "F")
           self.out.branch("e1_charge",        "F")
           self.out.branch("e1_cutbased",      "I")
           self.out.branch("e1_singletrg",     "I")
           self.out.branch("e1_crosstrg",      "I")
           self.out.branch("e1_doubletrg",     "I")

        if self.channel=="ee":
           self.out.branch("e2_pt",            "F")
           self.out.branch("e2_eta",           "F")
           self.out.branch("e2_phi",           "F")
           self.out.branch("e2_dxy",           "F")
           self.out.branch("e2_dz",            "F")
           self.out.branch("e2_charge",        "F")
           self.out.branch("e2_cutbased",      "I")
           self.out.branch("e2_singletrg",     "I")
           self.out.branch("e2_crosstrg",      "I")
           self.out.branch("e2_doubletrg",     "I")

        self.out.branch("pass_jvm",             "I")

        self.out.branch("nj",                   "I")
        self.out.branch("j_pt",                 "F",  lenVar = "nj")
        self.out.branch("j_eta",                "F",  lenVar = "nj")
        self.out.branch("j_phi",                "F",  lenVar = "nj")
        self.out.branch("j_m",                  "F",  lenVar = "nj")
        self.out.branch("j_area",               "F",  lenVar = "nj")
        self.out.branch("j_corr",               "F",  lenVar = "nj")
        self.out.branch("j_puid",               "F",  lenVar = "nj")
        self.out.branch("j_ParTRawB",           "F",  lenVar = "nj")
        self.out.branch("j_ParTRawC",           "F",  lenVar = "nj")
        self.out.branch("j_ParTRawOther",       "F",  lenVar = "nj")
        self.out.branch("j_ParTRawSingletau",   "F",  lenVar = "nj")
        self.out.branch("j_ParTRawTauhtaue",    "F",  lenVar = "nj")
        self.out.branch("j_ParTRawTauhtauh",    "F",  lenVar = "nj")
        self.out.branch("j_ParTRawTauhtaumu",   "F",  lenVar = "nj")
        self.out.branch("j_ParTRegMass",        "F",  lenVar = "nj") #FIXME better naming
        self.out.branch("j_ParTRegMassFactor",  "F",  lenVar = "nj") #FIXME better naming
        self.out.branch("j_deepflavB",          "F",  lenVar = "nj")
        self.out.branch("j_upartB",             "F",  lenVar = "nj")
        self.out.branch("j_hadronFlavour",      "I",  lenVar = "nj")

        self.out.branch("j_chEmEF",           "F",  lenVar = "nj")
        self.out.branch("j_chHEF",            "F",  lenVar = "nj")
        self.out.branch("j_muEF",             "F",  lenVar = "nj")
        self.out.branch("j_musubf",           "F",  lenVar = "nj")
        self.out.branch("j_neEmEF",           "F",  lenVar = "nj")
        self.out.branch("j_neHEF",            "F",  lenVar = "nj")
        self.out.branch("j_hfsigmaEtaEta",           "F",  lenVar = "nj")
        self.out.branch("j_hfsigmaPhiPhi",           "F",  lenVar = "nj")
        self.out.branch("j_hfcentralEtaStripSize",   "F",  lenVar = "nj")
        self.out.branch("j_hfadjacentEtaStripsSize", "F",  lenVar = "nj")

        self.out.branch("ntau",             "I")
        self.out.branch("tau_pt",           "F",  lenVar = "ntau")
        self.out.branch("tau_eta",          "F",  lenVar = "ntau")
        self.out.branch("tau_phi",          "F",  lenVar = "ntau")
        self.out.branch("tau_charge",       "I",  lenVar = "ntau")

        self.out.branch("nGenCand",                 "I")
        self.out.branch("GenCand_pdgId",            "I",  lenVar = "nGenCand")
        self.out.branch("GenCand_pt",               "F",  lenVar = "nGenCand")
        self.out.branch("GenCand_eta",              "F",  lenVar = "nGenCand")
        self.out.branch("GenCand_phi",              "F",  lenVar = "nGenCand")
        self.out.branch("GenCand_status",           "I",  lenVar = "nGenCand")
        self.out.branch("GenCand_isBsTauTau",       "I",  lenVar = "nGenCand")
        self.out.branch("GenCand_isBsTauTauh",      "I",  lenVar = "nGenCand")
        self.out.branch("GenCand_isBsTauTaue",      "I",  lenVar = "nGenCand")
        self.out.branch("GenCand_isBsTauTaumu",     "I",  lenVar = "nGenCand")
        self.out.branch("GenCand_isBsTauTaulep",    "I",  lenVar = "nGenCand") ## both taus are leptons

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def selectGenParticles(self, event):

        event.selectedGenParticles = []
        genparticles = Collection(event, "GenPart")
        for genp in genparticles:
            event.selectedGenParticles.append(genp)

    def selectElectrons(self, event, elSel):

        event.selectedElectrons = []
        electrons = Collection(event, "Electron")
        for el in electrons:
            if not elSel.evalElectron(el): continue

            #check overlap with selected leptons 
            deltaR_to_leptons=[ el.p4().DeltaR(lep.p4()) for lep in event.selectedMuons ]
            hasLepOverlap=sum( [dR<0.4 for dR in deltaR_to_leptons] )
            if hasLepOverlap>0: continue

            setattr(el, 'id', 11)
            event.selectedElectrons.append(el)
            
        event.selectedElectrons.sort(key=lambda x: x.pt, reverse=True)

    def selectMuons(self, event, muSel):
        ## access a collection in nanoaod and create a new collection based on this

        event.selectedMuons = []
        muons = Collection(event, "Muon")
        for mu in muons:
            if not muSel.evalMuon(mu): continue
            setattr(mu, 'id', 13)
            event.selectedMuons.append(mu)

        event.selectedMuons.sort(key=lambda x: x.pt, reverse=True)

    def selectTaus(self, event, tauSel):

        event.selectedTaus = []
        taus = Collection(event, "Tau")
        for tau in taus:
            if not tauSel.evalTau(tau): continue

            #check overlap with selected leptons 
            deltaR_to_leptons=[ tau.p4().DeltaR(lep.p4()) for lep in event.selectedMuons+event.selectedElectrons ]
            hasLepOverlap=sum( [dR<0.4 for dR in deltaR_to_leptons] )
            if hasLepOverlap>0: continue

            setattr(tau, 'id', 15)
            event.selectedTaus.append(tau)

        event.selectedTaus.sort(key=lambda x: x.pt, reverse=True)

    def selectAK4Jets(self, event):
        ## Selected jets: pT>30, |eta|<4.7, pass tight ID

        event.selectedAK4Jets = []
        ak4jets = Collection(event, "Jet")
        for j in ak4jets:
            if abs(j.eta) > 2.5:      # 5.191 -> extended eta range to value supported by JME (rolled back to compare Run2 nanov15 and v9)
                continue

            # in Run3 PU ID is not recommended -> https://twiki.cern.ch/twiki/bin/view/CMS/JetID
            #if not self.corr_jetid.evaluate(j.eta, j.chHEF, j.neHEF, j.chEmEF, j.neEmEF, j.muEF, j.chMultiplicity, j.neMultiplicity, j.chMultiplicity+j.neMultiplicity): continue #pass jetID, need to recalculate on top of NanoAODv15


            #check overlap with selected leptons 
            deltaR_to_leptons=[ j.p4().DeltaR(lep.p4()) for lep in event.selectedMuons+event.selectedElectrons]
            hasLepOverlap=sum( [dR<0.4 for dR in deltaR_to_leptons] )
            if hasLepOverlap>0: continue

            event.selectedAK4Jets.append(j)

        event.selectedAK4Jets.sort(key=lambda x: x.pt, reverse=True)


    def selectTriggerObjects(self, event):
        event.selectedTriggerObjects = []
        triggerobjects = Collection(event, "TrigObj")
        for to in triggerobjects:
           if to.id!=11 and to.id!=13 and to.id!=15: continue
           event.selectedTriggerObjects.append(to)

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        # Noise filters from JME
        if self.year=="2017" or self.year=="2018":
           if not (event.Flag_goodVertices and event.Flag_globalSuperTightHalo2016Filter and event.Flag_HBHENoiseFilter and event.Flag_HBHENoiseIsoFilter and event.Flag_EcalDeadCellTriggerPrimitiveFilter and event.Flag_BadPFMuonFilter and event.Flag_BadPFMuonDzFilter and event.Flag_hfNoisyHitsFilter and event.Flag_eeBadScFilter and event.Flag_ecalBadCalibFilter):
              return False

        if self.year=="2016" or self.year=="2016pre" or self.year=="2016post":
           if not (event.Flag_goodVertices and event.Flag_globalSuperTightHalo2016Filter and event.Flag_HBHENoiseFilter and event.Flag_HBHENoiseIsoFilter and event.Flag_EcalDeadCellTriggerPrimitiveFilter and event.Flag_BadPFMuonFilter and event.Flag_BadPFMuonDzFilter and event.Flag_hfNoisyHitsFilter and event.Flag_eeBadScFilter and event.Flag_hfNoisyHitsFilter):
              return False
        
        if self.year=="2024" or self.year=="2025":
            if not (event.Flag_goodVertices and event.Flag_globalSuperTightHalo2016Filter and event.Flag_EcalDeadCellTriggerPrimitiveFilter and event.Flag_BadPFMuonFilter and event.Flag_BadPFMuonDzFilter and event.Flag_hfNoisyHitsFilter and event.Flag_eeBadScFilter and event.Flag_ecalBadCalibFilter):
                return False

        if self.year=="2022" or self.year=="2023":
            if not (event.Flag_goodVertices and event.Flag_globalSuperTightHalo2016Filter and event.Flag_EcalDeadCellTriggerPrimitiveFilter and event.Flag_BadPFMuonFilter and event.Flag_BadPFMuonDzFilter and event.Flag_hfNoisyHitsFilter and event.Flag_eeBadScFilter):
                return False

    # ---- PRESELECTION ----  	
        #initiate object selector tools:
        elSel  = ElectronSelector()
        muSel  = MuonSelector()
        tauSel = TauSelector()

        # apply object selection and make channels exclusive based on number of leptons
        self.selectMuons(event, muSel)
        if self.channel=="e" or self.channel=="ee":
            if len(event.selectedMuons)>0: return False
        if self.channel=="mu" or self.channel=="emu":
            if len(event.selectedMuons)!=1: return False
        if self.channel=="mumu":
            if len(event.selectedMuons)!=2: return False

        self.selectElectrons(event, elSel)
        if self.channel=="mu" or self.channel=="mumu":
            if len(event.selectedElectrons)>0: return False
        if self.channel=="e" or self.channel=="emu":
            if len(event.selectedElectrons)!=1: return False
        if self.channel=="ee":
            if len(event.selectedElectrons)!=2: return False

        # apply preliminary loose(r) lepton pt cuts based on trigger:
        if self.channel=="mu":
            if event.selectedMuons[0].pt<29: return False

        if self.channel=="mumu":
            if event.selectedMuons[0].pt<19: return False
            if event.selectedMuons[1].pt<14: return False
            if max(event.selectedMuons[0].pt, event.selectedMuons[1].pt)<24: return False 

        if self.channel=="e":
            if event.selectedElectrons[0].pt<29: return False

        if self.channel=="ee":
            if event.selectedElectrons[0].pt<19: return False
            if event.selectedElectrons[1].pt<14: return False
            if max(event.selectedElectrons[0].pt, event.selectedElectrons[1].pt)<24: return False

        if self.channel=="emu":
            if event.selectedElectrons[0].pt<19: return False
            if event.selectedMuons[0].pt<19: return False
            if max(event.selectedElectrons[0].pt, event.selectedMuons[0].pt)<24: return False

	    # select events with at least one jet
        self.selectAK4Jets(event)
        if len(event.selectedAK4Jets)<1: return False
        event.nbjetL = 0 # FIXME : include b-tagging requirement (?)
        
        # jet veto map (veto the entire event in Run3, veto only the jet in Run2)
        event.pass_jvm=True
        #for j in event.selectedAK4Jets:
        #    if self.corr_jvm.evaluate("jetvetomap",j.eta,j.phi)!=0: event.pass_jvm=False
        
    # ---- GEN LEVEL ----  	

        # select relevant gen particles in simulation
        if self.isMC:
            self.selectGenParticles(event)

        _gen_pdgIDs = [531, 15, 13, 11, 6, 24, 23] #(Bs, tau, mu, e, top, W, Z)
        event.genCand=[]
        event.genIdx=[]
        idx=0
        if self.isMC:        
            for genp in event.selectedGenParticles:
                if (abs(genp.pdgId) in _gen_pdgIDs):
                    if DEBUGMODE: print(" +GenCand ({idx}) PDG-id={id} pt={pt:.2f} eta={eta:.2f} phi={phi:.2f} mother-IDX={motherIdx} statusFlags={status:16b}".format(idx=idx, id=genp.pdgId, pt=genp.pt, eta=genp.eta, phi=genp.phi, motherIdx=genp.genPartIdxMother, status=genp.statusFlags))
                    event.genCand.append(genp)
                    event.genIdx.append(idx)
                idx=idx+1


        gen_id     = [genp.pdgId for genp in event.genCand]
        gen_status = [genp.statusFlags for genp in event.genCand]
        gen_pt     = [genp.pt for genp in event.genCand]
        gen_eta    = [genp.eta for genp in event.genCand]
        gen_phi    = [genp.phi for genp in event.genCand]

        # find Bs->tautau
        gen_isbstt = []
        gen_isbsosc = []
        gen_isbstth = []
        gen_isbstte = []
        gen_isbsttmu = []
        gen_isbsttlep = []

        for k in range(len(event.genCand)):
            is_bstt = 0
            is_bstth = 0
            is_bsttmu = 0
            is_bstte = 0
            is_bsttlep = 0
            taus_from_this_bs = []
            
            if abs(gen_id[k])==531: # Bs
                
                # check if the Bs comes from an oscillation (i.e. if the mother is a B_s-bar)
                bsmother_idx = event.selectedGenParticles[event.genIdx[k]].genPartIdxMother
                gen_isbsosc.append(int(bsmother_idx>=0 and event.selectedGenParticles[bsmother_idx].pdgId == -gen_id[k]))
                if DEBUGMODE: print("  +Bs : idx = {idx} | mother idx = {mother} | oscillation = {osc}".format(idx=event.genIdx[k], mother=bsmother_idx, osc=gen_isbsosc[-1]))
                for tau_idx, genp in enumerate(event.selectedGenParticles):
                    if (
                        abs(genp.pdgId)==15 and
                        (abs(event.selectedGenParticles[genp.genPartIdxMother].pdgId)==531) and
                        (genp.genPartIdxMother == event.genIdx[k])
                    ):
                        taus_from_this_bs.append((tau_idx, genp))
                        is_bstt=1
                        if DEBUGMODE:
                            print("  +Bs->tautau: Bs idx={bs_idx} tau idx={tau_idx} tau pt={tau_pt:.2f} tau eta={tau_eta:.2f} tau phi={tau_phi:.2f}".format(bs_idx=event.genIdx[k], tau_idx=tau_idx, tau_pt=genp.pt, tau_eta=genp.eta, tau_phi=genp.phi))
            

            # tau decay mode classification
            if len(taus_from_this_bs) == 2:
                if DEBUGMODE:
                    print("  +Bs->tautau: found 2 taus from Bs decay, classifying tau decay modes...")
                is_bstt = 1
                
                decay_modes = []
                for tau_idx,tau in taus_from_this_bs:
                    daughters = [d for d in event.selectedGenParticles if d.genPartIdxMother == tau_idx]
                    if any(abs(d.pdgId) == 11 for d in daughters):
                        decay_modes.append("e")
                    elif any(abs(d.pdgId) == 13 for d in daughters):
                        decay_modes.append("mu")
                    else:
                        decay_modes.append("had")

                if decay_modes.count("had") == 2: 
                    is_bstth = 1
                elif decay_modes.count("had") == 1 and decay_modes.count("e") == 1:
                    is_bstte = 1
                elif decay_modes.count("had") == 1 and decay_modes.count("mu") == 1:
                    is_bsttmu = 1
                elif ("e" in decay_modes or "mu" in decay_modes) and decay_modes.count("had") == 0:
                    is_bsttlep = 1
                if DEBUGMODE:
                    print("  +Bs->tautau: tau decay modes classified as: ", decay_modes)
            else: is_bstt = 0

            gen_isbstt.append(is_bstt)
            gen_isbstth.append(is_bstth)
            gen_isbstte.append(is_bstte)
            gen_isbsttmu.append(is_bsttmu)
            gen_isbsttlep.append(is_bsttlep)

    # ---- JETS ----
        jet_pt          = [jet.pt for jet in event.selectedAK4Jets]
        jet_eta         = [jet.eta for jet in event.selectedAK4Jets]
        jet_phi         = [jet.phi for jet in event.selectedAK4Jets]
        jet_m           = [jet.mass for jet in event.selectedAK4Jets]
        jet_deepflavB   = [jet.btagDeepFlavB for jet in event.selectedAK4Jets] # nanoAODv9
        jet_upartB      = [jet.btagUParTAK4B for jet in event.selectedAK4Jets] # nanoAODv15

        if self.isMC: jet_hadronflavour = [jet.hadronFlavour for jet in event.selectedAK4Jets] # 5: b-quark, 4: c-quark, 0: light quark or gluon
        else: jet_hadronflavour = [-1 for jet in event.selectedAK4Jets]
        if self.year=="2024" or self.year=="2025": jet_puid      = [jet.puIdDisc for jet in event.selectedAK4Jets]
        else: jet_puid          = [1.0 for jet in event.selectedAK4Jets]
        
        # boosted ditau tagger
        jet_ParTRawB            = [jet.btagMyUParTprobb for jet in event.selectedAK4Jets]
        jet_ParTRawC            = [jet.btagMyUParTprobc for jet in event.selectedAK4Jets]
        jet_ParTRawOther        = [jet.btagMyUParTprobother for jet in event.selectedAK4Jets]
        jet_ParTRawSingletau    = [0.0 for jet in event.selectedAK4Jets]
        jet_ParTRawTauhtaue     = [jet.btagMyUParTditaue for jet in event.selectedAK4Jets]
        jet_ParTRawTauhtauh     = [jet.btagMyUParTditauh for jet in event.selectedAK4Jets]
        jet_ParTRawTauhtaumu    = [jet.btagMyUParTditaumu for jet in event.selectedAK4Jets]

        # jet mass regression
        jet_ParTRegMassFactor         = [jet.UParTRegMassCentral for jet in event.selectedAK4Jets]
        jet_ParTRegMass               = [jet.UParTRegMassCentral*jet.mass for jet in event.selectedAK4Jets]

        # JEC and noise filtering #FIXME: to check
        jet_area        = [jet.area for jet in event.selectedAK4Jets]
        jet_corr        = [1./(1.0-jet.rawFactor) for jet in event.selectedAK4Jets] # pT-raw = pT-nano*(1-rawFactor)
        jet_chEmEF      = [jet.chEmEF for jet in event.selectedAK4Jets]
        jet_chHEF       = [jet.chHEF for jet in event.selectedAK4Jets]
        jet_muEF        = [jet.muEF for jet in event.selectedAK4Jets]
        jet_musubf      = [jet.muonSubtrFactor for jet in event.selectedAK4Jets]
        jet_neEmEF      = [jet.neEmEF for jet in event.selectedAK4Jets]
        jet_neHEF       = [jet.neHEF for jet in event.selectedAK4Jets]

        jet_hfsigmaEtaEta           = [jet.hfsigmaEtaEta for jet in event.selectedAK4Jets]
        jet_hfsigmaPhiPhi           = [jet.hfsigmaPhiPhi for jet in event.selectedAK4Jets]
        jet_hfcentralEtaStripSize   = [jet.hfcentralEtaStripSize for jet in event.selectedAK4Jets]
        jet_hfadjacentEtaStripsSize = [jet.hfadjacentEtaStripsSize for jet in event.selectedAK4Jets]
    
    # ---- TAU ----
        self.selectTaus(event, tauSel)
        tau_pt     = [tau.pt for tau in event.selectedTaus]
        tau_eta    = [tau.eta for tau in event.selectedTaus]
        tau_phi    = [tau.phi for tau in event.selectedTaus]
        tau_charge = [tau.charge for tau in event.selectedTaus]
    
    # ---- TRIGGER ----
        # trigger matching
        self.selectTriggerObjects(event)
        def is_trigger_matched(pdgid,trigger,lep):
            for to in event.selectedTriggerObjects:
                top4=ROOT.TLorentzVector()
                top4.SetPtEtaPhiM(to.pt,to.eta,to.phi,0)
                if lep.p4().DeltaR(top4)<0.3:
                    if to.id==pdgid:
                        if trigger=="single" and pdgid==11 and (bool(to.filterBits&1) or bool(to.filterBits&2)): return True
                        if trigger=="cross" and pdgid==11 and bool(to.filterBits&6): return True
                        if trigger=="double" and pdgid==11 and (bool(to.filterBits&4) or bool(to.filterBits&5)): return True
                        if trigger=="single" and pdgid==13 and bool(to.filterBits&3): return True
                        if trigger=="cross" and pdgid==13 and bool(to.filterBits&5): return True
                        if trigger=="double" and pdgid==13 and bool(to.filterBits&4): return True
            return False
    
    # ---- OUT BRANCHES ----
	    # lepton branches
        if self.channel=="mu" or self.channel=="mumu" or self.channel=="emu":
            self.out.fillBranch("mu1_pt",             event.selectedMuons[0].pt)
            self.out.fillBranch("mu1_eta",            event.selectedMuons[0].eta)
            self.out.fillBranch("mu1_phi",            event.selectedMuons[0].phi)
            self.out.fillBranch("mu1_dxy",            event.selectedMuons[0].dxy)
            self.out.fillBranch("mu1_dz",             event.selectedMuons[0].dz)
            self.out.fillBranch("mu1_charge",         event.selectedMuons[0].charge)
            self.out.fillBranch("mu1_tightId",        event.selectedMuons[0].tightId)
            self.out.fillBranch("mu1_iso",            event.selectedMuons[0].pfRelIso04_all)
            self.out.fillBranch("mu1_singletrg",      is_trigger_matched(13,"single",event.selectedMuons[0]))
            self.out.fillBranch("mu1_crosstrg",       is_trigger_matched(13,"cross",event.selectedMuons[0]))
            self.out.fillBranch("mu1_doubletrg",      is_trigger_matched(13,"double",event.selectedMuons[0]))
    
        if self.channel=="mumu":
            self.out.fillBranch("mu2_pt",             event.selectedMuons[1].pt)
            self.out.fillBranch("mu2_eta",            event.selectedMuons[1].eta)
            self.out.fillBranch("mu2_phi",            event.selectedMuons[1].phi)
            self.out.fillBranch("mu2_dxy",            event.selectedMuons[1].dxy)
            self.out.fillBranch("mu2_dz",             event.selectedMuons[1].dz)
            self.out.fillBranch("mu2_charge",         event.selectedMuons[1].charge)
            self.out.fillBranch("mu2_tightId",        event.selectedMuons[1].tightId)
            self.out.fillBranch("mu2_iso",            event.selectedMuons[1].pfRelIso04_all)
            self.out.fillBranch("mu2_singletrg",      is_trigger_matched(13,"single",event.selectedMuons[1]))
            self.out.fillBranch("mu2_crosstrg",       is_trigger_matched(13,"cross",event.selectedMuons[1]))
            self.out.fillBranch("mu2_doubletrg",      is_trigger_matched(13,"double",event.selectedMuons[1]))
               
        if self.channel=="e" or self.channel=="ee" or self.channel=="emu":
            self.out.fillBranch("e1_pt",             event.selectedElectrons[0].pt)
            self.out.fillBranch("e1_eta",            event.selectedElectrons[0].eta)
            self.out.fillBranch("e1_phi",            event.selectedElectrons[0].phi)
            self.out.fillBranch("e1_dxy",            event.selectedElectrons[0].dxy)
            self.out.fillBranch("e1_dz",             event.selectedElectrons[0].dz)
            self.out.fillBranch("e1_charge",         event.selectedElectrons[0].charge)
            self.out.fillBranch("e1_cutbased",       event.selectedElectrons[0].cutBased)
            self.out.fillBranch("e1_singletrg",      is_trigger_matched(11,"single",event.selectedElectrons[0]))
            self.out.fillBranch("e1_crosstrg",       is_trigger_matched(11,"cross",event.selectedElectrons[0]))
            self.out.fillBranch("e1_doubletrg",      is_trigger_matched(11,"double",event.selectedElectrons[0]))        
    
        if self.channel=="ee":
            self.out.fillBranch("e2_pt",             event.selectedElectrons[1].pt)
            self.out.fillBranch("e2_eta",            event.selectedElectrons[1].eta)
            self.out.fillBranch("e2_phi",            event.selectedElectrons[1].phi)
            self.out.fillBranch("e2_dxy",            event.selectedElectrons[1].dxy)
            self.out.fillBranch("e2_dz",             event.selectedElectrons[1].dz)
            self.out.fillBranch("e2_charge",         event.selectedElectrons[1].charge)
            self.out.fillBranch("e2_cutbased",       event.selectedElectrons[1].cutBased)
            self.out.fillBranch("e2_singletrg",      is_trigger_matched(11,"single",event.selectedElectrons[1]))
            self.out.fillBranch("e2_crosstrg",       is_trigger_matched(11,"cross",event.selectedElectrons[1]))
            self.out.fillBranch("e2_doubletrg",      is_trigger_matched(11,"double",event.selectedElectrons[1]))

        

        self.out.fillBranch("pass_jvm",       event.pass_jvm)

    	# jet branches
        self.out.fillBranch("nj" ,                len(event.selectedAK4Jets))
        self.out.fillBranch("j_pt",               jet_pt)
        self.out.fillBranch("j_eta",              jet_eta)
        self.out.fillBranch("j_phi",              jet_phi)
        self.out.fillBranch("j_m",                jet_m)
        self.out.fillBranch("j_puid",             jet_puid)
        self.out.fillBranch("j_area",             jet_area)
        self.out.fillBranch("j_corr",             jet_corr)
        self.out.fillBranch("j_deepflavB",        jet_deepflavB)
        self.out.fillBranch("j_upartB",           jet_upartB)
        self.out.fillBranch("j_hadronFlavour",    jet_hadronflavour)
        self.out.fillBranch("j_ParTRawB",         jet_ParTRawB)
        self.out.fillBranch("j_ParTRawC",         jet_ParTRawC)
        self.out.fillBranch("j_ParTRawOther",     jet_ParTRawOther)
        self.out.fillBranch("j_ParTRawSingletau", jet_ParTRawSingletau)
        self.out.fillBranch("j_ParTRawTauhtaue",  jet_ParTRawTauhtaue)
        self.out.fillBranch("j_ParTRawTauhtauh",  jet_ParTRawTauhtauh)
        self.out.fillBranch("j_ParTRawTauhtaumu", jet_ParTRawTauhtaumu)
        self.out.fillBranch("j_ParTRegMass",      jet_ParTRegMass)
        self.out.fillBranch("j_ParTRegMassFactor",jet_ParTRegMassFactor)

        self.out.fillBranch("j_chEmEF",           jet_chEmEF)
        self.out.fillBranch("j_chHEF",            jet_chHEF)
        self.out.fillBranch("j_muEF",             jet_muEF)
        self.out.fillBranch("j_musubf",           jet_musubf)
        self.out.fillBranch("j_neEmEF",           jet_neEmEF)
        self.out.fillBranch("j_neHEF",            jet_neHEF)
        self.out.fillBranch("j_hfsigmaEtaEta",           jet_hfsigmaEtaEta)
        self.out.fillBranch("j_hfsigmaPhiPhi",           jet_hfsigmaPhiPhi)
        self.out.fillBranch("j_hfcentralEtaStripSize",   jet_hfcentralEtaStripSize)
        self.out.fillBranch("j_hfadjacentEtaStripsSize", jet_hfadjacentEtaStripsSize)
        
        # tau branches
        self.out.fillBranch("ntau" ,          len(event.selectedTaus))
        self.out.fillBranch("tau_pt",         tau_pt)
        self.out.fillBranch("tau_eta",        tau_eta)
        self.out.fillBranch("tau_phi",        tau_phi)
        self.out.fillBranch("tau_charge",     tau_charge)

        # GEN branches 
        if self.isMC:
            self.out.fillBranch("nGenCand",                      len(event.genCand))
            self.out.fillBranch("GenCand_pdgId" ,                gen_id)
            self.out.fillBranch("GenCand_pt" ,                   gen_pt)
            self.out.fillBranch("GenCand_eta" ,                  gen_eta)
            self.out.fillBranch("GenCand_phi" ,                  gen_phi)
            self.out.fillBranch("GenCand_status" ,               gen_status)
            self.out.fillBranch("GenCand_isBsTauTau" ,           gen_isbstt)
            self.out.fillBranch("GenCand_isBsTauTauh",           gen_isbstth)
            self.out.fillBranch("GenCand_isBsTauTaue",           gen_isbstte)
            self.out.fillBranch("GenCand_isBsTauTaumu",          gen_isbsttmu)
            self.out.fillBranch("GenCand_isBsTauTaulep",         gen_isbsttlep) ## both taus are leptons
        
        return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
# --- 2018 ---
analysis_emc2018        = lambda : Analysis(channel="e",    isMC=True, year="2018")
analysis_mumc2018       = lambda : Analysis(channel="mu",   isMC=True, year="2018")
analysis_emumc2018      = lambda : Analysis(channel="emu",  isMC=True, year="2018")
analysis_eemc2018       = lambda : Analysis(channel="ee",   isMC=True, year="2018")
analysis_mumumc2018     = lambda : Analysis(channel="mumu", isMC=True, year="2018")

analysis_edata2018      = lambda : Analysis(channel="e",    isMC=False, year="2018")
analysis_mudata2018     = lambda : Analysis(channel="mu",   isMC=False, year="2018")
analysis_emudata2018    = lambda : Analysis(channel="emu",  isMC=False, year="2018")
analysis_eedata2018     = lambda : Analysis(channel="ee",   isMC=False, year="2018")
analysis_mumudata2018   = lambda : Analysis(channel="mumu", isMC=False, year="2018")