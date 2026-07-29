class ObjectSelector:
    def __init__(self, _year = "None" ):
        self.year = _year


class GenParticleSelector(ObjectSelector):
    def __init__(self, _year = "None" ):
        self.year = _year

    def evalGenParticle(self, genp):
        return True

class ElectronSelector(ObjectSelector):
    def __init__(self, _minPt = 10):
        self.minPt = _minPt

    def evalElectron(self, el):
        isEBEE = True if abs(el.eta)>1.4442 and abs(el.eta)<1.5660 else False
        if isEBEE: return False       
        if el.pt < self.minPt: return False
        if abs(el.eta) >= 2.5 or abs(el.superclusterEta) >= 2.5: return False 
        if abs(el.eta)<1.4442 and abs(el.dxy) > 0.05: return False
        if abs(el.eta)<1.4442 and abs(el.dz) > 0.10: return False
        if abs(el.eta)>1.5560 and abs(el.dxy) > 0.10: return False
        if abs(el.eta)>1.5560 and abs(el.dz) > 0.20: return False
        if el.cutBased<4: return False #cut-based ID (0:fail, 1:veto, 2:loose, 3:medium, 4:tight), choose tight in SR
        return True

class TauSelector(ObjectSelector):
    def __init__(self, _minPt = 30):
        self.minPt = _minPt

    def evalTau(self, tau):
        if tau.pt < self.minPt: return False
        if abs(tau.eta) > 2.3: return False
        if abs(tau.dz) > 0.2: return False
        if tau.decayMode not in [0,1,10,11]: return False
        if abs(tau.charge)!=1: return False
        if tau.idDeepTau2018v2p5VSe<2: return False # VVLoose
        if tau.idDeepTau2018v2p5VSmu<1: return False # VLoose
        if tau.idDeepTau2018v2p5VSjet<6: return False # Tight

        return True
        
class MuonSelector(ObjectSelector):
    def __init__(self, minPt = 10):
        self.minPt = minPt

    def evalMuon(self, mu):
        if mu.pt < self.minPt: return False
        if abs(mu.eta) > 2.4: return False
        if mu.pfRelIso04_all>0.15: return False # cut at 0.15 in SR
        if abs(mu.dxybs) > 0.05 or abs(mu.dz) > 1.0: return False
        if not mu.tightId: return False
	      
        return True

