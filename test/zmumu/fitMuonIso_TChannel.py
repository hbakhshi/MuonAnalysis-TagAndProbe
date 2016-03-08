import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing

options = VarParsing ('analysis')
options.register ('cutname',
                    'PFIsoTight',
                    VarParsing.multiplicity.singleton,
                    VarParsing.varType.string,
                    "the cut name")
options.register ('tightid',
                    False,
                    VarParsing.multiplicity.singleton,
                    VarParsing.varType.bool,
                    "uses tight id instead of medium")
options.register ('catname',
                    'isolation',
                    VarParsing.multiplicity.singleton,
                    VarParsing.varType.string,
                    "it has been fixed for further uses")
options.register('tagtight',
                 True,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.bool,
                 "uses tight id for tag leg")                 
options.register ('efficiencies',
                  '',
                    VarParsing.multiplicity.list,
                    VarParsing.varType.string,
                    "it has been fixed for further uses")
options.register ('outdir',
                  './',
                    VarParsing.multiplicity.singleton,
                    VarParsing.varType.string,
                    "")


options.parseArguments()

def FileNameExtention():
    s = '_%s_%d' % ( options.cutname , options.tightid )
    if not options.tagtight :
        s += "_notagtight"

    for efff in options.efficiencies:
        s += "_" + efff 

    return s


process = cms.Process("TagProbe")

process.load('FWCore.MessageService.MessageLogger_cfi')
process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

input_dir = "file:/home/fynu/hbakhshiansohi/storage/TnP/76x/"
input_files_data = [ "TnPTree_v41_76X_RunD_part%d.root" % (i)  for i in range(1,8) ]

process.TnP_Muon_ISO_Data = cms.EDAnalyzer("TagProbeFitTreeAnalyzer",
    ## Input, output 
    InputFileNames = cms.vstring(["%s%s" % (input_dir , infile) for infile in input_files_data] ), 

    OutputFileName = cms.string( options.outdir + "Data_TnP_Muon_ISO_TChannelMoriond2016_76_" + FileNameExtention()  + ".root"),
    InputDirectoryName = cms.string("tpTree"),  
    InputTreeName = cms.string("fitter_tree"), 
    ## Variables for binning
    Variables = cms.PSet(
        mass   = cms.vstring("Tag-muon Mass", "77", "130", "GeV/c^{2}"),
        pt     = cms.vstring("muon p_{T}", "0", "1000", "GeV/c"),
        abseta = cms.vstring("muon |#eta|", "0", "2.5", ""),
        eta = cms.vstring("muon #eta", "-2.4", "2.4", ""),
        pair_dz = cms.vstring("#Deltaz between two muons", "-100", "100", "cm"),
        combRelIsoPF04dBeta = cms.vstring("PF Combined Relative Iso", "-100", "99999", ""),
        tag_nVertices       = cms.vstring("N(vertices)", "0", "99", ""),
        dzPV = cms.vstring("dz" , "0" , "99" , "cm" ),

        tag_pt = cms.vstring("tag muon p_{T}", "0", "1000", "GeV/c"),
        tag_combRelIsoPF04dBeta = cms.vstring("tag PF Combined Relative Iso", "-100", "99999", ""),
        tag_dzPV = cms.vstring("tag dz" , "0" , "99" , "cm" ),
        pair_probeMultiplicity = cms.vstring("probe-multiplicity per tag" , "0" , "99" , "" ),

        pair_nJets30 = cms.vstring("number of jets" , "0" , "30" , "" )
    ),
    ## Flags you want to use to define numerator and possibly denominator
    Categories = cms.PSet(
        PF = cms.vstring("PF Muon", "dummy[pass=1,fail=0]"),
        tag_IsoMu24_eta2p1 = cms.vstring("PF Muon", "dummy[pass=1,fail=0]"),
        Tight2012 = cms.vstring("is tight" , "dummy[pass=1,fail=0]" ),
        Medium = cms.vstring("medium-id" , "dummy[pass=1,fail=0]" ),
        Loose = cms.vstring("loose-id" , "dummy[pass=1,fail=0]" ),

        tag_Tight2012 = cms.vstring("tag is tight" , "dummy[pass=1,fail=0]" ),
        tag_IsoMu20 = cms.vstring("tag iso mu 20" , "dummy[pass=1,fail=0]" ),
    ),
    ## Cuts: name, variable, cut threshold
    Cuts = cms.PSet(
        PFIsoLoose = cms.vstring("PFIsoLoose" ,"combRelIsoPF04dBeta", "0.25"),
        PFIsoTight = cms.vstring("PFIsoTight" ,"combRelIsoPF04dBeta", "0.15"),
        PFIsoVeryTight = cms.vstring("PFIsoVeryTight" ,"combRelIsoPF04dBeta", "0.06"),
    ),
    ## What to fit
    Efficiencies = cms.PSet(
        ),
    ## PDF for signal and background (double voigtian + exponential background)
    PDFs = cms.PSet(
        vpvPlusExpo = cms.vstring(
            "Voigtian::signal1(mass, mean1[90,80,100], width[2.495], sigma1[2,1,3])",
            "Voigtian::signal2(mass, mean2[90,80,100], width,        sigma2[4,2,10])",
            "SUM::signal(vFrac[0.8,0,1]*signal1, signal2)",
            "Exponential::backgroundPass(mass, lp[-0.1,-1,0.1])",
            "Exponential::backgroundFail(mass, lf[-0.1,-1,0.1])",
            "efficiency[0.9,0,1]",
            "signalFractionInPassing[0.9]"
        )
    ),
    ## How to do the fit
    binnedFit = cms.bool(True),
    binsForFit = cms.uint32(40),
    saveDistributionsPlot = cms.bool(True),
    NumCPU = cms.uint32(1), ## leave to 1 for now, RooFit gives funny results otherwise
    SaveWorkspace = cms.bool(False),
)



AllEfficiencies = {
    ('isolation_vs_njets' , True ): 
    cms.PSet(
        UnbinnedVariables = cms.vstring("mass"),
        EfficiencyCategoryAndState = cms.vstring(options.cutname, "below"), ## variable is below cut value 
        BinnedVariables = cms.PSet(
            pair_nJets30 = cms.vdouble( -0.5 , 0.5 , 1.5 , 2.5 , 3.5 , 4.5 , 5.5 , 6.5 , 7.5 , 30 ),
            
            Medium = cms.vstring("pass"),                 ## 
            pt     = cms.vdouble( 20,  500 ),
            abseta = cms.vdouble( 0 , 2.1 ),
                
            tag_IsoMu20 = cms.vstring("pass"),
            tag_pt = cms.vdouble( 21 , 1000 ),
            tag_combRelIsoPF04dBeta = cms.vdouble( -0.5 , 0.2 ),

            pair_probeMultiplicity = cms.vdouble( 0.5 , 1.5 )
            ),
        BinToPDFmap = cms.vstring("vpvPlusExpo"), ## PDF to use, as defined below
        ),
    ('isolation_vs_coarseabseta' , True): 
    cms.PSet(  #plot page 20 , right
        UnbinnedVariables = cms.vstring("mass"),
        EfficiencyCategoryAndState = cms.vstring(options.cutname, "below"), ## variable is below cut value 
        BinnedVariables = cms.PSet(
            Medium = cms.vstring("pass"),                 ## 
            pt     = cms.vdouble( 20,  500 ),
            abseta = cms.vdouble( 0 , 0.9 , 1.2 , 2.1 , 2.4 ),
            
            tag_IsoMu20 = cms.vstring("pass"),
            tag_pt = cms.vdouble( 21 , 1000 ),
            tag_combRelIsoPF04dBeta = cms.vdouble( -0.5 , 0.2 ),

            pair_probeMultiplicity = cms.vdouble( 0.5 , 1.5 )
            ),
        BinToPDFmap = cms.vstring("vpvPlusExpo"), ## PDF to use, as defined below
        ),
    ('isolation_vs_eta' , True ):
        cms.PSet(  #plot page 19 , left
        UnbinnedVariables = cms.vstring("mass"),
        EfficiencyCategoryAndState = cms.vstring(options.cutname, "below"), ## variable is below cut value 
        BinnedVariables = cms.PSet(
            Medium = cms.vstring("pass"),                 ## 
            pt     = cms.vdouble( 20,  500 ),
            eta = cms.vdouble( -2.4 , -2.1 , -1.6 , -1.2 , -0.9 , -0.3 , -0.2 , 0.2 , 0.3 , 0.9 , 1.2 , 1.6 , 2.1 , 2.4 ),
            
            tag_IsoMu20 = cms.vstring("pass"),
            tag_pt = cms.vdouble( 21 , 1000 ),
            tag_combRelIsoPF04dBeta = cms.vdouble( -0.5 , 0.2 ),

            pair_probeMultiplicity = cms.vdouble( 0.5 , 1.5 ),
            ),
        BinToPDFmap = cms.vstring("vpvPlusExpo"), ## PDF to use, as defined below
        ),
    ('isolation_vs_pt' , True):
    cms.PSet(  #plot page 22 , last plot
        UnbinnedVariables = cms.vstring("mass"),
        EfficiencyCategoryAndState = cms.vstring(options.cutname, "below"), ## variable is below cut value 
        BinnedVariables = cms.PSet(
            Medium = cms.vstring("pass"),
            pt     = cms.vdouble( 20,25,30,40,50,60,80,120, 200 ),
            eta = cms.vdouble( -2.4 , 2.4 ),
            
            tag_IsoMu20 = cms.vstring("pass"),
            tag_pt = cms.vdouble( 21 , 1000 ),
            tag_combRelIsoPF04dBeta = cms.vdouble( -0.5 , 0.2 ),

            pair_probeMultiplicity = cms.vdouble( 0.5 , 1.5 ),
            ),
        BinToPDFmap = cms.vstring("vpvPlusExpo"), ## PDF to use, as defined below
        ),
    ('isolation_vs_pt_0abseta9' , True):
        cms.PSet(  #plot page 22 , all but last plot
        UnbinnedVariables = cms.vstring("mass"),
        EfficiencyCategoryAndState = cms.vstring(options.cutname, "below"), ## variable is below cut value 
        BinnedVariables = cms.PSet(
            Medium = cms.vstring("pass"),
            pt     = cms.vdouble( 20,25,30,40,50,60,120 ),
            abseta = cms.vdouble( 0 , 0.9 ),
            
            tag_IsoMu20 = cms.vstring("pass"),
            tag_pt = cms.vdouble( 21 , 1000 ),
            tag_combRelIsoPF04dBeta = cms.vdouble( -0.5 , 0.2 ),

            pair_probeMultiplicity = cms.vdouble( 0.5 , 1.5 ),
            ),
        BinToPDFmap = cms.vstring("vpvPlusExpo"), ## PDF to use, as defined below
        ),
    ('isolation_vs_pt_9abseta12' , True): 
    cms.PSet(  #plot page 22 , all but last plot
        UnbinnedVariables = cms.vstring("mass"),
        EfficiencyCategoryAndState = cms.vstring(options.cutname, "below"), ## variable is below cut value 
        BinnedVariables = cms.PSet(
            Medium = cms.vstring("pass"),
            pt     = cms.vdouble( 20,25,30,40,50,60,120 ),
            abseta = cms.vdouble( 0.9 , 1.2 ),
            
            tag_IsoMu20 = cms.vstring("pass"),
            tag_pt = cms.vdouble( 21 , 1000 ),
            tag_combRelIsoPF04dBeta = cms.vdouble( -0.5 , 0.2 ),

            pair_probeMultiplicity = cms.vdouble( 0.5 , 1.5 ),
            ),
        BinToPDFmap = cms.vstring("vpvPlusExpo"), ## PDF to use, as defined below
        ),
    ('isolation_vs_pt_12abseta21' , True): 
    cms.PSet(  #plot page 22 , all but last plot
        UnbinnedVariables = cms.vstring("mass"),
        EfficiencyCategoryAndState = cms.vstring(options.cutname, "below"), ## variable is below cut value 
        BinnedVariables = cms.PSet(
            Medium = cms.vstring("pass"),
            pt     = cms.vdouble( 20,25,30,40,50,60,120 ),
            abseta = cms.vdouble( 1.2 , 2.1 ),
            
            tag_IsoMu20 = cms.vstring("pass"),
            tag_pt = cms.vdouble( 21 , 1000 ),
            tag_combRelIsoPF04dBeta = cms.vdouble( -0.5 , 0.2 ),

            pair_probeMultiplicity = cms.vdouble( 0.5 , 1.5 ),
            ),
        BinToPDFmap = cms.vstring("vpvPlusExpo"), ## PDF to use, as defined below
        ),
    ('isolation_vs_pt_21abseta24' , True): 
    cms.PSet(  #plot page 22 , all but last plot
        UnbinnedVariables = cms.vstring("mass"),
        EfficiencyCategoryAndState = cms.vstring(options.cutname, "below"), ## variable is below cut value 
        BinnedVariables = cms.PSet(
            Medium = cms.vstring("pass"),
            pt     = cms.vdouble( 20,25,30,40,50,60,120 ),
            abseta = cms.vdouble( 2.1 , 2.4 ),
            
            tag_IsoMu20 = cms.vstring("pass"),
            tag_pt = cms.vdouble( 21 , 1000 ),
            tag_combRelIsoPF04dBeta = cms.vdouble( -0.5 , 0.2 ),

            pair_probeMultiplicity = cms.vdouble( 0.5 , 1.5 ),
            ),
        BinToPDFmap = cms.vstring("vpvPlusExpo"), ## PDF to use, as defined below
        ),
    ('isolation_vs_nVertices' , True): 
    cms.PSet(  #plot page 19 , right side
        UnbinnedVariables = cms.vstring("mass"),
        EfficiencyCategoryAndState = cms.vstring(options.cutname, "below"), ## variable is below cut value 
        BinnedVariables = cms.PSet(
            Medium = cms.vstring("pass"),
            tag_nVertices = cms.vdouble(0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30),
            pt     = cms.vdouble( 20, 500 ),
            eta = cms.vdouble( -2.4 , 2.4 ),
            
            tag_IsoMu20 = cms.vstring("pass"),
            tag_pt = cms.vdouble( 21 , 1000 ),
            tag_combRelIsoPF04dBeta = cms.vdouble( -0.5 , 0.2 ),

            pair_probeMultiplicity = cms.vdouble( 0.5 , 1.5 ),
            ),
        BinToPDFmap = cms.vstring("vpvPlusExpo"), ## PDF to use, as defined below
        )
}

for (eff,plotit) in AllEfficiencies:
    if eff in options.efficiencies or len(options.efficiencies)==0 :
        setattr( process.TnP_Muon_ISO_Data.Efficiencies , eff , AllEfficiencies[(eff,plotit)] )

print "Efficiencies will be provided as :"
for eff in process.TnP_Muon_ISO_Data.Efficiencies.parameterNames_():
    print '\t' + eff
    if( options.tightid ):
        getattr( process.TnP_Muon_ISO_Data.Efficiencies , eff ).BinnedVariables.Tight2012 = cms.vstring("pass") 
    else:
        getattr( process.TnP_Muon_ISO_Data.Efficiencies , eff ).BinnedVariables.Medium = cms.vstring("pass") 

    if( options.tagtight ):
        #print getattr( process.TnP_Muon_ISO_Data.Efficiencies , eff )
        getattr( process.TnP_Muon_ISO_Data.Efficiencies , eff ).BinnedVariables.tag_tight2012 = cms.vstring("pass")
        getattr( process.TnP_Muon_ISO_Data.Efficiencies , eff ).BinnedVariables.tag_dzPV = cms.vdouble( -0.5 , 0.5 )


process.p1 = cms.Path(process.TnP_Muon_ISO_Data )


