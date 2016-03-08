from fitMuonIso_TChannel import *

input_files_mc = ["TnPTree_76X_DYLL_M50_MadGraphMLM_part1_New.root" , "TnPTree_76X_DYLL_M50_MadGraphMLM_part2_New.root" ]

process.TnP_Muon_ISO_MC = process.TnP_Muon_ISO_Data.clone()
process.TnP_Muon_ISO_MC.InputFileNames =  [  "%s%s" % (input_dir , infile) for infile in input_files_mc ]
process.TnP_Muon_ISO_MC.OutputFileName = options.outdir + "MC_TnP_Muon_ISO_TChannelMoriond2016_76_" + FileNameExtention()  +".root"

process.TnP_Muon_ISO_MC.Variables = process.TnP_Muon_ISO_MC.Variables.clone(
    weight2_n = cms.vstring("weight2_n","-10","10","") 
    )


process.TnP_Muon_ISO_MC.WeightVariable = cms.string("weight2_n")

for name in process.TnP_Muon_ISO_MC.Efficiencies.parameterNames_():
    getattr( process.TnP_Muon_ISO_MC.Efficiencies , name ).UnbinnedVariables.append( "weight2_n" )
    #print getattr( process.TnP_Muon_ISO_MC.Efficiencies , name ).UnbinnedVariables

process.p1 = cms.Path( process.TnP_Muon_ISO_MC )

