
#nohup cmsRun fitMuonIso_TChannel_MC.py cutname=PFIsoTight tightid=False tagtight=False >& outmc_iso_15_Medium_allprobes 
nohup cmsRun fitMuonIso_TChannel.py cutname=PFIsoTight tightid=False tagtight=False >& outdata_iso_15_Medium_allprobes 

nohup cmsRun fitMuonIso_TChannel_MC.py cutname=PFIsoVeryTight tightid=False tagtight=False >& outmc_iso_06_Medium_allprobes 
nohup cmsRun fitMuonIso_TChannel.py cutname=PFIsoVeryTight tightid=False tagtight=False >& outdata_iso_06_Medium_allprobes 

nohup cmsRun fitMuonTrigger_TChannel_MC.py cutname=IsoMu20OrIsoTkMu20  >& outmc_trigger_15_Or 
nohup cmsRun fitMuonTrigger_TChannel.py cutname=IsoMu20OrIsoTkMu20  >& outdata_trigger_15_Or_range1 
nohup cmsRun fitMuonTrigger_TChannel.py cutname=IsoMu20OrIsoTkMu20 runrange2=True  >& outdata_trigger_15_Or_range2 

nohup cmsRun fitMuonTrigger_TChannel_MC.py isolation=0.06  >& outmc_trigger_06 
nohup cmsRun fitMuonTrigger_TChannel.py isolation=0.06 >& outdata_trigger_06_range1 
nohup cmsRun fitMuonTrigger_TChannel.py runrange2=True isolation=0.06  >& outdata_trigger_06_range2 

