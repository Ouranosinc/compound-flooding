function loadfun_historic(pth_base,outlet,serie)
if strcmp(serie,'WLcondQ')
    f = fullfile(pth_base,outlet,'historic',serie,'\Results\MhAST_Results.mat');
    load(f);
    g = fullfile(pth_base,outlet,'historic','QcondWL','\Results\MhAST_Results.mat'); 
    load(g,'PD_U2','D_U2');
    h = fullfile(pth_base,outlet,'historic',serie,'\Results\data.mat');
    save(h)
elseif strcmp(serie,'QcondWL')
    
    f = fullfile(pth_base,outlet,'historic',serie,'\Results\MhAST_Results.mat');
    load(f);
    g = fullfile(pth_base,outlet,'historic','WLcondQ','\Results\MhAST_Results.mat'); 
    load(g,'PD_U1','D_U1');
    h = fullfile(pth_base,outlet,'historic',serie,'\Results\data.mat');
    save(h)
end

