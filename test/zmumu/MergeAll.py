from ROOT import TFile,  TH1D , TH2D 

fIso = TFile.Open('Isolation.root')
hIso = fIso.Get('h2d').Clone('SFIso')
fTrg1 = TFile.Open('TriggerMenu42.root')
hTrg1 = fTrg1.Get('h2d').Clone('SFTrg42')
fTrg2 = TFile.Open('TriggerMenu43.root')
hTrg2 = fTrg2.Get('h2d').Clone('SFTrg43')

fout = TFile.Open('ScaleFactos.root' , 'RECREATE' )
hIso.Write()
hTrg1.Write()
hTrg2.Write()

hTrg = hTrg1.Clone('SFTrigger_Weighted')
hTrg.Sumw2()
Lumi42 = 393.474
Lumi43 = 1852.852 
Lumi = Lumi42+Lumi43
hTrg.Add( hTrg1 , hTrg2 , Lumi42/Lumi , Lumi43/Lumi )

hTrg.Write()
fout.Close()

