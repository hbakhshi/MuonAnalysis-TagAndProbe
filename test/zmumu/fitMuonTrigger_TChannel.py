import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing

options = VarParsing ('analysis')
options.register ('cutname',
                    'IsoMu20Cut',
                    VarParsing.multiplicity.singleton,
                    VarParsing.varType.string,
                    "the cut name")
options.register ('isolation',
                    0.15,
                    VarParsing.multiplicity.singleton,
                    VarParsing.varType.float,
                    "isolation")
options.register ('runrange2',
                    False,
                    VarParsing.multiplicity.singleton,
                    VarParsing.varType.bool,
                    "usr run range 2 ?")
options.register ('catname',
                  'isolation',
                    VarParsing.multiplicity.singleton,
                    VarParsing.varType.string,
                    "it has been fixed for further uses")

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

runrange = cms.vdouble( 0 , 257819.5 )
if( options.runrange2 ):
    runrange = cms.vdouble( 257819.5 , 258750.5 )

def FileNameExtention():
    a = '_%s_%d_%d' % (options.cutname , int(100*options.isolation) , options.runrange2)
    
    for efff in options.efficiencies:
        a += "_" + efff 
    
    return a

process = cms.Process("TagProbe")

process.load('FWCore.MessageService.MessageLogger_cfi')
process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

input_dir = "file:/home/fynu/hbakhshiansohi/storage/TnP/76x/"
input_files_data = [ "TnPTree_v41_76X_RunD_part%d.root" % (i)  for i in range(1,8) ]

process.TnP_Muon_Trigger_Data = cms.EDAnalyzer("TagProbeFitTreeAnalyzer",
    ## Input, output 
    InputFileNames = cms.vstring(["%s%s" % (input_dir , infile) for infile in input_files_data]  ), 

    OutputFileName = cms.string(options.outdir + "Data_TnP_Muon_Trigger_TChannelMoriond2016_76_" + FileNameExtention() + ".root"),
    InputDirectoryName = cms.string("tpTree"),  
    InputTreeName = cms.string("fitter_tree"), 

    Expressions = cms.PSet(
        IsoMu20OrTk = cms.vstring( "IsoMu20OrTk" , "(IsoMu20 > 0.5) || (IsoTkMu20 > 0.5)" , "IsoMu20" , "IsoTkMu20" )
        ),
    ## Variables for binning
    Variables = cms.PSet(
        mass   = cms.vstring("Tag-muon Mass", "50", "130", "GeV/c^{2}"),
        pt     = cms.vstring("muon p_{T}", "0", "1000", "GeV/c"),
        abseta = cms.vstring("muon |#eta|", "0", "2.5", ""),
        eta = cms.vstring("muon #eta", "-2.4", "2.4", ""),
        pair_dz = cms.vstring("#Deltaz between two muons", "-100", "100", "cm"),
        combRelIsoPF04dBeta = cms.vstring("PF Combined Relative Iso", "-100", "99999", ""),
        tag_nVertices       = cms.vstring("N(vertices)", "0", "99", ""),
        dzPV = cms.vstring("dz" , "0" , "99" , "cm" ),

        run = cms.vstring("run number" , "0" , "1000000" , "" ),

        tag_pt = cms.vstring("tag muon p_{T}", "0", "1000", "GeV/c"),
        tag_combRelIsoPF04dBeta = cms.vstring("tag PF Combined Relative Iso", "-100", "99999", ""),
        tag_dzPV = cms.vstring("tag dz" , "0" , "99" , "cm" ),
        pair_probeMultiplicity = cms.vstring("probe-multiplicity per tag" , "0" , "99" , "" ),

        pair_nJets30 = cms.vstring("number of jets" , "0" , "30" , "" )
    ),
    ## Flags you want to use to define numerator and possibly denominator
    Categories = cms.PSet(
        IsoTkMu20 = cms.vstring("iso mu 20" , "dummy[pass=1,fail=0]" ),
        IsoMu20 = cms.vstring("iso mu 20 _" , "dummy[pass=1,fail=0]" ),
        PF = cms.vstring("PF Muon", "dummy[pass=1,fail=0]"),
        Tight2012 = cms.vstring("is tight" , "dummy[pass=1,fail=0]" ),
        Medium = cms.vstring("medium-id" , "dummy[pass=1,fail=0]" ),
        Loose = cms.vstring("loose-id" , "dummy[pass=1,fail=0]" ),

        tag_IsoMu24_eta2p1 = cms.vstring("PF Muon", "dummy[pass=1,fail=0]"),
        tag_Tight2012 = cms.vstring("tag is tight" , "dummy[pass=1,fail=0]" ),
        tag_IsoMu20 = cms.vstring("tag iso mu 20" , "dummy[pass=1,fail=0]" ),
    ),
    ## Cuts: name, variable, cut threshold
    Cuts = cms.PSet(
        IsoMu20OrIsoTkMu20 = cms.vstring("IsoMu20OrIsoTkMu20" , "IsoMu20OrTk" , "0.5" ),
        IsoMu20Cut = cms.vstring("IsoMu20Cut" , "IsoMu20" , "0.5" )
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
    ('trigger_vs_njets01_234inf_allpairs', True ):
        cms.PSet(  
        UnbinnedVariables = cms.vstring("mass"),
        EfficiencyCategoryAndState = cms.vstring(options.cutname , 'above'), 
        BinnedVariables = cms.PSet(
            pair_nJets30 = cms.vdouble( -0.5 , 1.5 , 2.5 , 3.5 , 30 ),
            pt     = cms.vdouble( 22,  120 ),
            eta = cms.vdouble( -2.4 ,  2.4 ),
            Tight2012 = cms.vstring("pass"),
            combRelIsoPF04dBeta = cms.vdouble( -0.5 , options.isolation ),
            dzPV = cms.vdouble( -0.5 , 0.5 ),

            tag_IsoMu20 = cms.vstring("pass"),
            tag_Tight2012 = cms.vstring("pass"),
            tag_pt = cms.vdouble( 22 , 1000 ),
            
            #pair_probeMultiplicity = cms.vdouble( 0.5 , 1.5 ),

            run = runrange
            ),
        BinToPDFmap = cms.vstring("vpvPlusExpo"), ## PDF to use, as defined below
        ),
    ('trigger_vs_njets01_2inf', False ):
        cms.PSet(  
        UnbinnedVariables = cms.vstring("mass"),
        EfficiencyCategoryAndState = cms.vstring(options.cutname , 'above'), 
        BinnedVariables = cms.PSet(
            pair_nJets30 = cms.vdouble( -0.5 , 1.5 , 30 ),
            pt     = cms.vdouble( 22,  120 ),
            eta = cms.vdouble( -2.4 ,  2.4 ),
            Tight2012 = cms.vstring("pass"),
            combRelIsoPF04dBeta = cms.vdouble( -0.5 , options.isolation ),
            dzPV = cms.vdouble( -0.5 , 0.5 ),

            tag_IsoMu20 = cms.vstring("pass"),
            tag_Tight2012 = cms.vstring("pass"),
            tag_pt = cms.vdouble( 22 , 1000 ),
            
            pair_probeMultiplicity = cms.vdouble( 0.5 , 1.5 ),

            run = runrange
            ),
        BinToPDFmap = cms.vstring("vpvPlusExpo"), ## PDF to use, as defined below
        ),
    ('trigger_vs_njets01_23inf', False ):
        cms.PSet(  
        UnbinnedVariables = cms.vstring("mass"),
        EfficiencyCategoryAndState = cms.vstring(options.cutname , 'above'), 
        BinnedVariables = cms.PSet(
            pair_nJets30 = cms.vdouble( -0.5 , 1.5 , 2.5 , 30 ),
            pt     = cms.vdouble( 22,  120 ),
            eta = cms.vdouble( -2.4 ,  2.4 ),
            Tight2012 = cms.vstring("pass"),
            combRelIsoPF04dBeta = cms.vdouble( -0.5 , options.isolation ),
            dzPV = cms.vdouble( -0.5 , 0.5 ),

            tag_IsoMu20 = cms.vstring("pass"),
            tag_Tight2012 = cms.vstring("pass"),
            tag_pt = cms.vdouble( 22 , 1000 ),
            
            pair_probeMultiplicity = cms.vdouble( 0.5 , 1.5 ),

            run = runrange
            ),
        BinToPDFmap = cms.vstring("vpvPlusExpo"), ## PDF to use, as defined below
        ),
    ('trigger_vs_njets01_234inf', False ):
        cms.PSet(  
        UnbinnedVariables = cms.vstring("mass"),
        EfficiencyCategoryAndState = cms.vstring(options.cutname , 'above'), 
        BinnedVariables = cms.PSet(
            pair_nJets30 = cms.vdouble( -0.5 , 1.5 , 2.5 , 3.5 , 30 ),
            pt     = cms.vdouble( 22,  120 ),
            eta = cms.vdouble( -2.4 ,  2.4 ),
            Tight2012 = cms.vstring("pass"),
            combRelIsoPF04dBeta = cms.vdouble( -0.5 , options.isolation ),
            dzPV = cms.vdouble( -0.5 , 0.5 ),

            tag_IsoMu20 = cms.vstring("pass"),
            tag_Tight2012 = cms.vstring("pass"),
            tag_pt = cms.vdouble( 22 , 1000 ),
            
            pair_probeMultiplicity = cms.vdouble( 0.5 , 1.5 ),

            run = runrange
            ),
        BinToPDFmap = cms.vstring("vpvPlusExpo"), ## PDF to use, as defined below
        ),
    ('trigger_vs_njets', False ):
        cms.PSet(  
        UnbinnedVariables = cms.vstring("mass"),
        EfficiencyCategoryAndState = cms.vstring(options.cutname , 'above'), 
        BinnedVariables = cms.PSet(
            pair_nJets30 = cms.vdouble( -0.5 , 0.5 , 1.5 , 2.5 , 3.5 , 4.5 , 5.5 , 6.5 , 7.5 , 30 ),
            pt     = cms.vdouble( 22,  120 ),
            eta = cms.vdouble( -2.4 ,  2.4 ),
            Tight2012 = cms.vstring("pass"),
            combRelIsoPF04dBeta = cms.vdouble( -0.5 , options.isolation ),
            dzPV = cms.vdouble( -0.5 , 0.5 ),

            tag_IsoMu20 = cms.vstring("pass"),
            tag_Tight2012 = cms.vstring("pass"),
            tag_pt = cms.vdouble( 22 , 1000 ),
            
            pair_probeMultiplicity = cms.vdouble( 0.5 , 1.5 ),

            run = runrange
            ),
        BinToPDFmap = cms.vstring("vpvPlusExpo"), ## PDF to use, as defined below
        ),
    ('trigger_vs_eta',False):
        cms.PSet(  #plot page 14 , upper left
        UnbinnedVariables = cms.vstring("mass"),
        EfficiencyCategoryAndState = cms.vstring(options.cutname , 'above'), ## variable is below cut value 
        BinnedVariables = cms.PSet(
            pt     = cms.vdouble( 22,  120 ),
            eta = cms.vdouble( -2.4 , -2.1 , -1.6 , -1.2 , -0.9 , -0.3 , -0.2 , 0.2 , 0.3 , 0.9 , 1.2 , 1.6 , 2.1 , 2.4 ),
            Tight2012 = cms.vstring("pass"),
            combRelIsoPF04dBeta = cms.vdouble( -0.5 , options.isolation ),
            dzPV = cms.vdouble( -0.5 , 0.5 ),

            tag_IsoMu20 = cms.vstring("pass"),
            tag_Tight2012 = cms.vstring("pass"),
            tag_pt = cms.vdouble( 22 , 1000 ),
            
            pair_probeMultiplicity = cms.vdouble( 0.5 , 1.5 ),

            run = runrange
            ),
        BinToPDFmap = cms.vstring("vpvPlusExpo"), ## PDF to use, as defined below
        ),
    ('trigger_vs_nprobes',False):
        cms.PSet(  #plot page 14 , upper left
        UnbinnedVariables = cms.vstring("mass"),
        EfficiencyCategoryAndState = cms.vstring(options.cutname , 'above'), ## variable is below cut value 
        BinnedVariables = cms.PSet(
            pt     = cms.vdouble( 22,  120 ),
            eta = cms.vdouble( -2.4 , 2.4 ),
            Tight2012 = cms.vstring("pass"),
            combRelIsoPF04dBeta = cms.vdouble( -0.5 , options.isolation ),
            dzPV = cms.vdouble( -0.5 , 0.5 ),

            tag_IsoMu20 = cms.vstring("pass"),
            tag_Tight2012 = cms.vstring("pass"),
            tag_pt = cms.vdouble( 22 , 1000 ),
            
            pair_probeMultiplicity = cms.vdouble( 0.0 , 0.5 , 1.5 , 2.5 , 3.5 , 4.5, 5.5 , 6.5 ),

            run = runrange
            ),
        BinToPDFmap = cms.vstring("vpvPlusExpo"), ## PDF to use, as defined below
        ),
    ('trigger_vs_nVertices',False) :
        cms.PSet(  #plot page 14 , lower left
        UnbinnedVariables = cms.vstring("mass"),
        EfficiencyCategoryAndState = cms.vstring(options.cutname , 'above'), ## variable is below cut value 
        BinnedVariables = cms.PSet(
            tag_nVertices = cms.vdouble(0.5,2.5,4.5,6.5,8.5,10.5,12.5,14.5,16.5,18.5,20.5,22.5,24.5,26.5,28.5,30.5),
            pt     = cms.vdouble( 22 , 120 ),
            eta = cms.vdouble( -2.4 , 2.4 ),
            Tight2012 = cms.vstring("pass"),
            combRelIsoPF04dBeta = cms.vdouble( -0.5 ,  options.isolation ),
            dzPV = cms.vdouble( -0.5 , 0.5 ),

            tag_IsoMu20 = cms.vstring("pass"),
            tag_Tight2012 = cms.vstring("pass"),
            tag_pt = cms.vdouble( 22 , 1000 ),
            
            pair_probeMultiplicity = cms.vdouble( 0.5 , 1.5 ),

            run = runrange
            ),
        BinToPDFmap = cms.vstring("vpvPlusExpo"), ## PDF to use, as defined below
        ),
    ('trigger_vs_pt',False) :
        cms.PSet(  #plot page 14 , right
        UnbinnedVariables = cms.vstring("mass"),
        EfficiencyCategoryAndState = cms.vstring(options.cutname , 'above'), ## variable is below cut value 
        BinnedVariables = cms.PSet(
            pt     = cms.vdouble( 0 , 10 , 15 , 18 , 20 , 22 , 25 , 30 , 40 , 50 , 60 , 80 , 120 ),
            eta = cms.vdouble( -2.4 , 2.4 ),
            Tight2012 = cms.vstring("pass"),
            combRelIsoPF04dBeta = cms.vdouble( -0.5 ,  options.isolation ),
            dzPV = cms.vdouble( -0.5 , 0.5 ),

            tag_IsoMu20 = cms.vstring("pass"),
            tag_Tight2012 = cms.vstring("pass"),
            tag_pt = cms.vdouble( 22 , 1000 ),
            
            pair_probeMultiplicity = cms.vdouble( 0.5 , 1.5 ),

            run = runrange
            ),
        BinToPDFmap = cms.vstring("vpvPlusExpo"), ## PDF to use, as defined below
        ),
    ('trigger_vs_pt_0abseta9',False):
        cms.PSet(  #plot page 14 , right
        UnbinnedVariables = cms.vstring("mass"),
        EfficiencyCategoryAndState = cms.vstring(options.cutname , 'above'), ## variable is below cut value 
        BinnedVariables = cms.PSet(
            pt     = cms.vdouble( 22 , 25 , 30 , 40 , 50 , 60 , 120 ),
            abseta = cms.vdouble( 0.0 , 0.9 ),
            Tight2012 = cms.vstring("pass"),
            combRelIsoPF04dBeta = cms.vdouble( -0.5 , options.isolation ),
            dzPV = cms.vdouble( -0.5 , 0.5 ),
            
            tag_IsoMu20 = cms.vstring("pass"),
            tag_Tight2012 = cms.vstring("pass"),
            tag_pt = cms.vdouble( 22 , 1000 ),
            
            pair_probeMultiplicity = cms.vdouble( 0.5 , 1.5 ),
            
            run = runrange
            ),
        BinToPDFmap = cms.vstring("vpvPlusExpo"), ## PDF to use, as defined below
        ),
    ('trigger_vs_pt_9abseta12',False):
        cms.PSet(  #plot page 14 , right
        UnbinnedVariables = cms.vstring("mass"),
        EfficiencyCategoryAndState = cms.vstring(options.cutname , 'above'), ## variable is below cut value 
        BinnedVariables = cms.PSet(
            pt     = cms.vdouble( 22 , 25 , 30 , 40 , 50 , 60 , 120 ),
            abseta = cms.vdouble( 0.9 , 1.2 ),
            Tight2012 = cms.vstring("pass"),
            combRelIsoPF04dBeta = cms.vdouble( -0.5 , options.isolation ),
            dzPV = cms.vdouble( -0.5 , 0.5 ),
            
            tag_IsoMu20 = cms.vstring("pass"),
            tag_Tight2012 = cms.vstring("pass"),
            tag_pt = cms.vdouble( 22 , 1000 ),
            
            pair_probeMultiplicity = cms.vdouble( 0.5 , 1.5 ),
            
            run = runrange
            ),
        BinToPDFmap = cms.vstring("vpvPlusExpo"), ## PDF to use, as defined below
        ),
    ('trigger_vs_pt_12abseta21',False):
        cms.PSet(  #plot page 14 , right
        UnbinnedVariables = cms.vstring("mass"),
        EfficiencyCategoryAndState = cms.vstring(options.cutname , 'above'), ## variable is below cut value 
        BinnedVariables = cms.PSet(
            pt     = cms.vdouble( 22 , 25 , 30 , 40 , 50 , 60 , 120 ),
            abseta = cms.vdouble( 1.2 , 2.1 ),
            Tight2012 = cms.vstring("pass"),
            combRelIsoPF04dBeta = cms.vdouble( -0.5 , options.isolation ),
            dzPV = cms.vdouble( -0.5 , 0.5 ),
            
            tag_IsoMu20 = cms.vstring("pass"),
            tag_Tight2012 = cms.vstring("pass"),
            tag_pt = cms.vdouble( 22 , 1000 ),
            
            pair_probeMultiplicity = cms.vdouble( 0.5 , 1.5 ),
            
            run = runrange
            ),
        BinToPDFmap = cms.vstring("vpvPlusExpo"), ## PDF to use, as defined below
        ),
    ('trigger_vs_pt_21abseta24',False):
        cms.PSet(  #plot page 14 , right
        UnbinnedVariables = cms.vstring("mass"),
        EfficiencyCategoryAndState = cms.vstring(options.cutname , 'above'), ## variable is below cut value 
        BinnedVariables = cms.PSet(
            pt     = cms.vdouble( 22 , 25 , 30 , 40 , 50 , 60 , 120 ),
            abseta = cms.vdouble( 2.1 , 2.4 ),
            Tight2012 = cms.vstring("pass"),
            combRelIsoPF04dBeta = cms.vdouble( -0.5 , options.isolation ),
            dzPV = cms.vdouble( -0.5 , 0.5 ),
            
            tag_IsoMu20 = cms.vstring("pass"),
            tag_Tight2012 = cms.vstring("pass"),
            tag_pt = cms.vdouble( 22 , 1000 ),
            
            pair_probeMultiplicity = cms.vdouble( 0.5 , 1.5 ),
            
            run = runrange
            ),
        BinToPDFmap = cms.vstring("vpvPlusExpo"), ## PDF to use, as defined below
        )
    }


for (eff,plotit) in AllEfficiencies:
    if eff in options.efficiencies or len(options.efficiencies)==0 :
        setattr( process.TnP_Muon_Trigger_Data.Efficiencies , eff , AllEfficiencies[(eff,plotit)] )

print "Efficiencies will be provided as :"
for eff in process.TnP_Muon_Trigger_Data.Efficiencies.parameterNames_():
    print '\t' + eff


process.p1 = cms.Path(process.TnP_Muon_Trigger_Data)
