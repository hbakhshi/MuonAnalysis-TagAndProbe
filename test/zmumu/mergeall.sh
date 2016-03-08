echo $1

export ParrentDir=$PWD

merge_files(){
    cd $1/$2
    if [ -e Merged.root ]; then
	#rm -f Merged.root
	echo "Already merged" 
    else
	hadd Merged.root *.root
    fi
    cd -
    if [ -h $3 ]
    then
	rm -f $3
    fi
    ln -s $1/$2/Merged.root $3
}

merge_files $1 Iso/15/MC MC_TnP_Muon_ISO_TChannelMoriond2016_76__PFIsoTight_0_notagtight.root
merge_files $1 Iso/15/Data Data_TnP_Muon_ISO_TChannelMoriond2016_76__PFIsoTight_0_notagtight.root
merge_files $1 Iso/06/MC MC_TnP_Muon_ISO_TChannelMoriond2016_76__PFIsoVeryTight_0_notagtight.root
merge_files $1 Iso/06/Data Data_TnP_Muon_ISO_TChannelMoriond2016_76__PFIsoVeryTight_0_notagtight.root

merge_files $1 Trigger/15/Data0 Data_TnP_Muon_Trigger_TChannelMoriond2016_76__IsoMu20OrIsoTkMu20_15_0.root
merge_files $1 Trigger/15/Data1 Data_TnP_Muon_Trigger_TChannelMoriond2016_76__IsoMu20OrIsoTkMu20_15_1.root
merge_files $1 Trigger/15/MC MC_TnP_Muon_Trigger_TChannelMoriond2016_76__IsoMu20OrIsoTkMu20_15_0.root

merge_files $1 Trigger/06/Data0 Data_TnP_Muon_Trigger_TChannelMoriond2016_76__IsoMu20Cut_6_0.root
merge_files $1 Trigger/06/Data1 Data_TnP_Muon_Trigger_TChannelMoriond2016_76__IsoMu20Cut_6_1.root
merge_files $1 Trigger/06/MC MC_TnP_Muon_Trigger_TChannelMoriond2016_76__IsoMu20Cut_6_0.root
