import LaunchOnCondor

import urllib
import string
import os
import sys
import glob



cpVersion = "V4"
FarmDirectory = "TnP_"+cpVersion
JobName = "Fit_"+cpVersion

if not os.path.isdir( "/home/fynu/hbakhshiansohi/scratch/FARMS/" + FarmDirectory ):
    os.makedirs( "/home/fynu/hbakhshiansohi/scratch/FARMS/" + FarmDirectory )

if os.path.islink( "./" + FarmDirectory ):
    os.remove( "./" + FarmDirectory)
elif os.path.isdir( "./" + FarmDirectory ):
    os.rename( "./" + FarmDirectory , "./" + FarmDirectory + "_OLD" )
    print "old is renamed"
os.symlink( "/home/fynu/hbakhshiansohi/scratch/FARMS/" + FarmDirectory , "./" + FarmDirectory )

LaunchOnCondor.Jobs_FinalCmds.append('echo "damet-garm" \n')
LaunchOnCondor.SendCluster_Create(FarmDirectory, JobName)

if not os.path.isdir(  "./" +  FarmDirectory + "/outputs/Trigger/06/MC" ):
    os.makedirs( "./" +  FarmDirectory + "/outputs/Trigger/06/MC")
if not os.path.isdir( "./" +  FarmDirectory + "/outputs/Trigger/06/Data1"):
    os.makedirs( "./" +  FarmDirectory + "/outputs/Trigger/06/Data1")
if not os.path.isdir( "./" +  FarmDirectory + "/outputs/Trigger/06/Data0"):
    os.makedirs( "./" +  FarmDirectory + "/outputs/Trigger/06/Data0")

if not os.path.isdir( "./" +  FarmDirectory + "/outputs/Iso/06/MC"):
    os.makedirs( "./" +  FarmDirectory + "/outputs/Iso/06/MC")
if not os.path.isdir( "./" +  FarmDirectory + "/outputs/Iso/06/Data"):
    os.makedirs( "./" +  FarmDirectory + "/outputs/Iso/06/Data")

if not os.path.isdir( "./" +  FarmDirectory + "/outputs/Trigger/15/MC"):
    os.makedirs( "./" +  FarmDirectory + "/outputs/Trigger/15/MC")
if not os.path.isdir( "./" +  FarmDirectory + "/outputs/Trigger/15/Data1"):
    os.makedirs( "./" +  FarmDirectory + "/outputs/Trigger/15/Data1")
if not os.path.isdir( "./" +  FarmDirectory + "/outputs/Trigger/15/Data0"):
    os.makedirs( "./" +  FarmDirectory + "/outputs/Trigger/15/Data0")

if not os.path.isdir( "./" +  FarmDirectory + "/outputs/Iso/15/MC"):
    os.makedirs( "./" +  FarmDirectory + "/outputs/Iso/15/MC")
if not os.path.isdir( "./" +  FarmDirectory + "/outputs/Iso/15/Data"):
    os.makedirs( "./" +  FarmDirectory + "/outputs/Iso/15/Data")


from fitMuonIso_TChannel_MC import AllEfficiencies as isoEffs 
for (eff,plotit) in isoEffs:
    if not plotit:
        continue
    print 'adding isolation jobs for %s' % (eff)
    LaunchOnCondor.SendCluster_Push(["BASH", "cmsRun fitMuonIso_TChannel_MC.py cutname=PFIsoTight tightid=False tagtight=False efficiencies=%s outdir=%s" % (eff ,  "./" +  FarmDirectory + "/outputs/Iso/15/MC/" ) ])
    LaunchOnCondor.SendCluster_Push(["BASH", "cmsRun fitMuonIso_TChannel.py cutname=PFIsoTight tightid=False tagtight=False efficiencies=%s outdir=%s" % (eff ,  "./" +  FarmDirectory + "/outputs/Iso/15/Data/") ])
    LaunchOnCondor.SendCluster_Push(["BASH", "cmsRun fitMuonIso_TChannel_MC.py cutname=PFIsoVeryTight tightid=False tagtight=False efficiencies=%s  outdir=%s" % (eff ,  "./" +  FarmDirectory + "/outputs/Iso/06/MC/") ])
    LaunchOnCondor.SendCluster_Push(["BASH", "cmsRun fitMuonIso_TChannel.py cutname=PFIsoVeryTight tightid=False tagtight=False efficiencies=%s  outdir=%s" % (eff ,  "./" +  FarmDirectory + "/outputs/Iso/06/Data/") ])

from fitMuonTrigger_TChannel_MC import AllEfficiencies as trgEffs
for (eff,plotit) in trgEffs:
    if not plotit:
        continue
    print 'adding trigger jobs for %s' % (eff)
    LaunchOnCondor.SendCluster_Push(["BASH", "cmsRun fitMuonTrigger_TChannel_MC.py cutname=IsoMu20OrIsoTkMu20 efficiencies=%s  outdir=%s" % (eff,  "./" +  FarmDirectory + "/outputs/Trigger/15/MC/") ] )
    LaunchOnCondor.SendCluster_Push(["BASH", "cmsRun fitMuonTrigger_TChannel.py cutname=IsoMu20OrIsoTkMu20 efficiencies=%s  outdir=%s" % (eff,  "./" +  FarmDirectory + "/outputs/Trigger/15/Data0/") ])
    LaunchOnCondor.SendCluster_Push(["BASH", "cmsRun fitMuonTrigger_TChannel.py cutname=IsoMu20OrIsoTkMu20 runrange2=True efficiencies=%s  outdir=%s" % (eff,  "./" +  FarmDirectory + "/outputs/Trigger/15/Data1/") ])
    LaunchOnCondor.SendCluster_Push(["BASH", "cmsRun fitMuonTrigger_TChannel_MC.py isolation=0.06 efficiencies=%s  outdir=%s" % (eff ,  "./" +  FarmDirectory + "/outputs/Trigger/06/MC/") ])
    LaunchOnCondor.SendCluster_Push(["BASH", "cmsRun fitMuonTrigger_TChannel.py isolation=0.06 efficiencies=%s  outdir=%s" % (eff,  "./" +  FarmDirectory + "/outputs/Trigger/06/Data0/") ])
    LaunchOnCondor.SendCluster_Push(["BASH", "cmsRun fitMuonTrigger_TChannel.py runrange2=True isolation=0.06 efficiencies=%s  outdir=%s" % (eff,  "./" +  FarmDirectory + "/outputs/Trigger/06/Data1/") ])

LaunchOnCondor.SendCluster_Submit()
