function loadfun_RM(pth_base,outlet,serie)
if strcmp(serie,'WLcondQ')
    f = fullfile(pth_base,outlet,'future',serie,'\100\Results\MhAST_Results.mat');
    load(f);
    g = fullfile(pth_base,outlet,'future','QcondWL','\100\Results\MhAST_Results.mat'); 
    load(g,'PD_U2','D_U2');
    h = fullfile(pth_base,outlet,'future',serie,'\100\Results\data.mat');
    save(h)
elseif strcmp(serie,'QcondWL')
    
    f = fullfile(pth_base,outlet,'future',serie,'\100\Results\MhAST_Results.mat');
    load(f);
    g = fullfile(pth_base,outlet,'future','WLcondQ','\100\Results\MhAST_Results.mat'); 
    load(g,'PD_U1','D_U1');
    h = fullfile(pth_base,outlet,'future',serie,'\100\Results\data.mat');
    save(h)
end
end

