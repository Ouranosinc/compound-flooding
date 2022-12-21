function merge_mats (pth_base, outlet,pth_out)

%example:
% outlet = 'Batiscan';
% pth_base = 'U:\Dossier_travail\705300_rehaussement_marin\3- Data\Results';
% pth_out = 'U:\Dossier_travail\705300_rehaussement_marin\5- Rapports\LOT3\Livrable_2';
% merge_mats(pth_base,outlet,pth_out)


name1 = sprintf('historic_WLcondQ_%s.mat',outlet);
name2 = sprintf('historic_QcondWL_%s.mat',outlet);
name3 = sprintf('future_WLcondQ_%s.mat',outlet);
name4 = sprintf('future_QcondWL_%s.mat',outlet);

fname1 = fullfile(pth_base,outlet,'historic','WLcondQ','\100\Results\',name1);
fname2 = fullfile(pth_base,outlet,'historic','QcondWL','\100\Results\',name2);
fname3 = fullfile(pth_base,outlet,'future','WLcondQ','\100\Results\',name3);
fname4 = fullfile(pth_base,outlet,'future','QcondWL','\100\Results\',name4);

WLcondQ_historic = load(fname1); 
QcondWL_historic = load(fname2); 
WLcondQ_future =load(fname3); 
QcondWL_future = load(fname4);

% foutput = fullfile(pth_base,outlet,'\');
cd (pth_out)
save (outlet, 'WLcondQ_historic','QcondWL_historic','WLcondQ_future','QcondWL_future')

end