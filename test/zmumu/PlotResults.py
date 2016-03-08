from ROOT import TFile, TCanvas, TGraphAsymmErrors, TList, kBlue, kWhite, TH1D , TH2D , TVirtualPad, TPad, TLine , kBlack, gStyle, gROOT
from array import array
from math import sqrt
from os import path
import os

class TnPBinnedVariable :
    def __init__(self , name , value ):
        self.Name = name
        self.Range = value

        self.Canvas = None
        self.Graph = None

    def ReadFromFile( self, directory , appendix , data_mc_appendix ):
        self.Canvas = ( directory.Get( self.Name + appendix ) )
        for i in range( 0 ,  self.Canvas.GetListOfPrimitives().GetSize() ):
            if self.Canvas.GetListOfPrimitives().At(i).ClassName() == "TGraphAsymmErrors" :
                self.Graph = self.Canvas.GetListOfPrimitives().At(i).Clone(  self.Name + appendix + data_mc_appendix )


class TnPEfficiency :
    def __init__(self, Efficiency , name ):
        self.Name = name 
        self.BinnedVariables = []
        self.Categories = {}
        for varname in Efficiency.BinnedVariables.parameterNames_() :
            if len( getattr( Efficiency.BinnedVariables , varname ) ) > 2 :
                self.BinnedVariables.append( TnPBinnedVariable( varname ,  getattr( Efficiency.BinnedVariables , varname ).value() ) )
            elif len( getattr( Efficiency.BinnedVariables , varname ) ) == 1 :
                self.Categories[ varname ] = getattr( Efficiency.BinnedVariables , varname )[0]
                               
                

    def ReadFromFile( self , directory , appendix_data_mc ):
        appendix = "_PLOT"
        appendix_tags = ""
        for cat in sorted(self.Categories) :
            if cat[0:4] == "tag_" :
                appendix_tags += "_" + cat + "_" + self.Categories[cat] + "_&"
            else:
                appendix += "_" + cat + "_" + self.Categories[cat] + "_&"

        for binnedvar in self.BinnedVariables :
            binnedvar.ReadFromFile( directory , (appendix+appendix_tags)[:-2] , appendix_data_mc )

class TnPResuls :
    def __init__(self , TagProbeFitTreeAnalyzer , isData):
        self.Appendix = "_MC"
        if isData :
            self.Appendix = "_Data"
        self.DirectoryName = TagProbeFitTreeAnalyzer.InputDirectoryName.value()
        self.Efficiencies = {}

        self.FileName = TagProbeFitTreeAnalyzer.OutputFileName.value()
        self.File = TFile.Open( self.FileName )

        self.FileDir = "./"
        if os.path.islink( self.FileName ):
            self.FileDir = os.path.dirname(os.path.realpath( os.readlink( self.FileName ) ))
        print self.FileDir

        for name in TagProbeFitTreeAnalyzer.Efficiencies.parameterNames_():
            self.Efficiencies[name] =  TnPEfficiency( getattr( TagProbeFitTreeAnalyzer.Efficiencies , name ) , name ) 
            self.Efficiencies[name].ReadFromFile( self.File.GetDirectory( self.DirectoryName + "/" + name + "/fit_eff_plots/") , self.Appendix  )                                     
class TnPMCDataPlots :
    def __init__(self , data , mc , eff , varname , outdir):
        self.DataInfo = data
        self.Data = data.Graph 
        self.MC = mc.Graph
        self.Eff = eff
        self.Var = varname
        self.OutDir = outdir

    def Plot(self, save=False):
        self.Canvas = TCanvas( "c1_" + self.Eff + "_" + self.Var , "c1_" + self.Eff + "_" + self.Var , 200,10,600,600  )
        
        self.Pad1 = TPad( "Upper1_" + self.Eff + "_" + self.Var , "" , 0.01 ,  0.21 ,  0.98 , 0.98 )
        self.Pad1.Draw()
        self.Pad1.cd()

        self.Pad1.SetGridx(20)
        self.Pad1.SetGridy(20)

        self.MC.SetLineColor( kBlue )
        self.MC.SetMarkerColor( kBlue )
        self.MC.SetFillColor( kWhite )
        self.MC.SetTitle( "MC (amcatnloFXFX)" )

        vals = [self.MC.GetY()[i] for i in range(0, self.MC.GetN() ) ]
        
        minEff = min( vals )*0.9
        print minEff
        maxEff = max( vals )*1.2

        minEff = 0.48
        maxEff = 1.2

        self.MC.GetHistogram().GetYaxis().SetRangeUser( minEff , maxEff )
        self.MC.GetHistogram().GetXaxis().SetRangeUser( self.DataInfo.Range[0] , sorted(self.DataInfo.Range)[-1] )
        self.MC.Draw("AP")

        self.Data.SetFillColor( kWhite )
        self.Data.SetTitle( "Data (2015D)" )

        self.Data.Draw("SAME P")

        self.Pad1.BuildLegend()
        

        self.Canvas.cd()
        self.Pad2 = TPad( "Lower1_" + self.Eff + "_" + self.Var  , "" , 0.01 ,  0.01 , 0.98 , 0.2  )
        self.Pad2.Draw()
        self.Pad2.cd()
        self.Pad2.SetGrid(0, 1);
        gStyle.SetGridStyle(3);

        runArray = array('d',sorted(self.DataInfo.Range) )
        self.DataOverMC = TH1D("DataOverMC_" + self.Data.GetName() , "" , self.Data.GetN() , runArray )
        self.DataOverMC.SetStats(0)
        self.ScaleFactors = []
        self.ScaleFactorErrors = []

        sfVar=0.0
        for bin in range( 1 , self.Data.GetN()+1 ):
            a = self.Data.GetY()[bin-1]
            d_a = self.Data.GetErrorY(bin-1)
            b = self.MC.GetY()[bin-1] 
            d_b = self.MC.GetErrorY(bin-1)

            value = 0.0
            if( b != 0 ):
                value = a / b
                
            if sfVar < abs( 1.0-value ) :
                sfVar = abs( 1.0-value )

            self.DataOverMC.SetBinContent( bin , value )
            self.ScaleFactors.append( value )

            error = 0
            if( a != 0 and b != 0 ):
                error = value*sqrt ( ( d_a*d_a / (a*a) ) + (d_b*d_b/(b*b)) )
            self.DataOverMC.SetBinError( bin , error )
            self.ScaleFactorErrors.append( error )

        sfVar *= 1.1
        if sfVar > 0.2 :
            sfVar = 0.15
        
        sfVar = 0.02*int(sfVar / 0.02)
        sfVar = 0.1

        self.DataOverMC.SetLineWidth( 2 )
        self.DataOverMC.SetMarkerStyle( 20 )
        self.DataOverMC.SetMarkerSize( 0.8 )
        self.DataOverMC.SetMarkerColor( kBlack )
        self.DataOverMC.SetLineWidth( 2 )
        self.DataOverMC.SetLineColor( kBlack )

        if( sfVar < 0.1 ):
            self.DataOverMC.GetYaxis().SetNdivisions(200+1*int(sfVar / 0.01))
        else :
            self.DataOverMC.GetYaxis().SetNdivisions(200+2*int(sfVar / 0.02))
        self.DataOverMC.GetYaxis().SetLabelFont(61)
        self.DataOverMC.GetYaxis().SetLabelSize(0.1)
        self.DataOverMC.GetYaxis().SetRangeUser( 1-sfVar , 1+sfVar )
        self.DataOverMC.Draw("E0")

        self.Line1 = TLine( self.DataInfo.Range[0] , 1.0 ,  sorted(self.DataInfo.Range)[-1] , 1.0 )
        self.Line1.SetLineStyle( 2 )
        self.Line1.SetLineWidth( 2 )
        self.Line1.SetLineColor( 17 )
        #self.Line1.Draw()

        if save :
            self.Canvas.SaveAs( self.OutDir + "/" + self.Canvas.GetName()+FileNameExtention()+".png")


class TnPCompPlots :
    def __init__(self , dataAnalyzer , mcAnalyzer ):
        gStyle.SetOptTitle( 0 )
        gStyle.SetStatBorderSize(0)
        #gStyle.SetStatBorderColor(kWhite)

        self.DataInfo = TnPResuls( dataAnalyzer , True )
        self.MCInfo = TnPResuls( mcAnalyzer , False )

        self.AllEffPlots = {}

        for eff in self.DataInfo.Efficiencies :
            #print eff 
            varname =  self.DataInfo.Efficiencies[ eff ].BinnedVariables[0].Name
            dataGraph = self.DataInfo.Efficiencies[ eff ].BinnedVariables[0]
            mcGraph = self.MCInfo.Efficiencies[ eff ].BinnedVariables[0]
            #print dataGraph.Graph.GetName()
            #print mcGraph.Graph.GetName()

            self.AllEffPlots[eff] = TnPMCDataPlots( dataGraph , mcGraph , eff , varname , self.DataInfo.FileDir )
               

from FWCore.ParameterSet.VarParsing import VarParsing
gROOT.SetBatch(True)

option___ = VarParsing ('analysis')
option___.register ('catname',
                  '',
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.string,
                  "")
option___.register ('cutname',
                    'PFIsoTight',
                    VarParsing.multiplicity.singleton,
                    VarParsing.varType.string,
                    "the cut name")
option___.register ('tightid',
                    False,
                    VarParsing.multiplicity.singleton,
                    VarParsing.varType.bool,
                    "uses tight id instead of medium")
option___.register ('isolation',
                    0.15,
                    VarParsing.multiplicity.singleton,
                    VarParsing.varType.float,
                    "isolation")
option___.register ('runrange2',
                    False,
                    VarParsing.multiplicity.singleton,
                    VarParsing.varType.bool,
                    "usr run range 2 ?")
option___.register('tagtight',
                   True,
                   VarParsing.multiplicity.singleton,
                   VarParsing.varType.bool,
                   "uses tight id for tag leg")                 

option___.parseArguments()

plotter = None

if option___.catname == "isolation" :
    from fitMuonIso_TChannel_MC import *
    plotter = TnPCompPlots( process.TnP_Muon_ISO_Data , process.TnP_Muon_ISO_MC )
elif option___.catname == "trigger" :
    from fitMuonTrigger_TChannel_MC import *
    plotter = TnPCompPlots( process.TnP_Muon_Trigger_Data , process.TnP_Muon_Trigger_MC )

outdir = plotter.DataInfo.FileDir

plot2D = False
ptRange = None
etaRange = None
h2d = None
for (eff, plotit) in AllEfficiencies:
    if eff == ('%s_vs_pt_21abseta24' % (options.catname)):
        plot2D = plotit

if plot2D :
    ptRange = array('d',sorted(plotter.AllEffPlots['%s_vs_pt_21abseta24' % (options.catname) ].DataInfo.Range ) )
    etaRange = array('d', [0,0.9,1.2,2.1,2.4] ) #sorted(plotter.AllEffPlots['%s_vs_coarseabseta' % (options.catname) ].DataInfo.Range )
    
    h2d = TH2D( "h2d" , "Isolation Scale Factors;p_{T};|#eta|" , len(ptRange)-1 , ptRange , len(etaRange)-1 , etaRange )
    h2d.SetStats(0)

import re
for eff in plotter.AllEffPlots :
    plotter.AllEffPlots[ eff ].Plot(True)
    if not plot2D :
        continue

    match = re.match ( r'.*_vs_pt_(\d*)abseta(\d*)' , eff , re.M|re.I )
    #print eff
    if match:
        #print match.groups()
        centraleta = float( int(match.group(1)) + int(match.group(2)) ) / 20
        #print centraleta
        for ptbin in range( 0 , len(ptRange)-1 ):
            pt = (ptRange[ptbin] + ptRange[ptbin+1])/2.0
            #print pt
            binid = h2d.FindBin( pt , centraleta )
            val =plotter.AllEffPlots[eff].ScaleFactors[ ptbin ]
            #val = int(100*val)/100.0 #round it
            h2d.SetBinContent( binid , val )
            h2d.SetBinError( binid , plotter.AllEffPlots[eff].ScaleFactorErrors[ ptbin ] )

c = None
if plot2D :
    c = TCanvas()
    h2d.Draw("COLZ TEXT")
    h2d.SaveAs("%s/%s_%s_2d.root" % (outdir , option___.catname , FileNameExtention() ) )
    c.SaveAs("%s/%s_%s_2d.png" % (outdir , option___.catname , FileNameExtention() ) )

