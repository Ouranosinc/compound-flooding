function Post_processing_main(pth_base,outlet,serie,horizon,copula_type,selected_copula)
% This is the main function for extracting the outputs of MhAST.

% Put the 2 and 350 year .mat output of the MhAST in the \serie\Results\ as
% RP2.mat and RP350.mat
%example:
%Post_processing_main('U:\Dossier_travail\705300_rehaussement_marin\3- Data\Results\','Mitis','WLcondQ','future','independent','Clayton')


% Post_processing_main('U:\Dossier_travail\705300_rehaussement_marin\3- Data\Results\','Saint_Francois','WLcondQ','historic','dependent','BB1')


%% Part 1
% clear all; clc

%This bloack loads the necessary dataset for univariate frequencyanalysis.
if strcmp(horizon, 'historic')
    loadfun_historic(pth_base,outlet,serie);
    load(fullfile(pth_base,outlet,horizon,serie,'\100\Results\data.mat'));
elseif strcmp(horizon, 'future')
    loadfun_RM(pth_base,outlet,serie);
    load(fullfile(pth_base,outlet,horizon,serie,'\100\Results\data.mat'));
end
%% Part 2

if strcmp(serie,'WLcondQ')
    S.period = horizon;
    S.Univariate.serie = 'WLcondQ';
    S.Univariate.Q = handles.PD_U1{1,1};
    S.Univariate.H = PD_U2{1,1}; %H from QcondWL dataset
    S.Univariate.Q_Paramci = handles.D_U1(1).Paramci; %paramci for Q comes from D_U1 dataset
    S.Univariate.H_Paramci = D_U2(1).Paramci;
    S.Univariate.RPH_Values = zeros(3,7);
    S.Univariate.RPQ_Values = zeros(3,7);
    
    %Univariate Frequency Analysis: variable 1 (Q)
    numPV1 = handles.PD_U1{1,1}.NumParameters;
    variable = 'Principal';
    [RP_UV_names,RP_UV_values] = RP_UV(numPV1,data,variable,serie,handles,PD_U1,PD_U2);
    S.Univariate.RPQ_Names = RP_UV_names;
    S.Univariate.RPQ_Values(2,:) = RP_UV_values;
    
    
    %Univariate Frequency Analysis: variable 2 (H)
    numPV2 = PD_U2{1,1}.NumParameters;
    variable = 'Conditional';
    [RP_UV_names,RP_UV_values] = RP_UV(numPV2,data,variable,serie,handles,PD_U1,PD_U2);
    S.Univariate.RPH_Names = RP_UV_names;
    S.Univariate.RPH_Values(2,:) = RP_UV_values;
    
    % calculating the 5% and 95% percentiles of Q and H
    
    numPV1 = size(S.Univariate.Q_Paramci(1,:),2);
    variable = 'Principal';
    par1 = S.Univariate.Q_Paramci(1,:);
    [~,RP_UV_values_5] = RP_UV5(numPV1,data,variable,serie,handles,par1,PD_U1,PD_U2);
    S.Univariate.RPQ_Values(1,:) = RP_UV_values_5;
    
    numPV1 = size(D_U2(1).Paramci(1,:),2);
    variable = 'Conditional';
    par1 = D_U2(1).Paramci(1,:);
    [~,RP_UV_values_5] = RP_UV5(numPV1,data,variable,serie,handles,par1,PD_U1,PD_U2);
    S.Univariate.RPH_Values(1,:) = RP_UV_values_5;
    
    numPV1 = size(S.Univariate.Q_Paramci(1,:),2);
    variable = 'Principal';
    par1 = S.Univariate.Q_Paramci(2,:);
    [~,RP_UV_values_95] = RP_UV95(numPV1,data,variable,serie,handles,par1,PD_U1,PD_U2);
    S.Univariate.RPQ_Values(3,:) = RP_UV_values_95;
    
    numPV2 = size(D_U2(1).Paramci(1,:),2);
    variable = 'Conditional';
    par1 = D_U2(1).Paramci(2,:);
    [~,RP_UV_values_95] = RP_UV95(numPV2,data,variable,serie,handles,par1,PD_U1,PD_U2);
    S.Univariate.RPH_Values(3,:) = RP_UV_values_95;
    %Load the PD_U1,PD_U2, D_U1, D_U2 corresponding to the dataset
    if strcmp(horizon,'historic')
        f = fullfile(pth_base,outlet,'historic',serie,'\100\Results\MhAST_Results.mat');
        load(f);
    elseif strcmp(horizon,'future')
        f = fullfile(pth_base,outlet,'future',serie,'\100\Results\MhAST_Results.mat');
        load(f);
    end
    
    
    % Bivariate frequency analsis (AND-based copula results)
    S.Bivariate.CopulaType = copula_type;
    S.Bivariate.serie = 'WLcondQ';
%     if strcmp(copula_type,'dependent')
%         S.Bivariate.DesignRP = DesignRP;
%     end
    S.Bivariate.serie = serie;
    [QH_bivariate_allQH,QH_Design,Copula_Pars,desvarnames] = RPBivariate(pth_base,outlet,copula_type,selected_copula,Design_Variables,serie, horizon,data,handles,Copula_Variables);
    if strcmp(copula_type,'dependent')
        S.Bivariate.DesVarNames = desvarnames;
        S.Bivariate.DesVarValuesall = QH_bivariate_allQH;
    end
    S.Bivariate.DesVarValues = QH_Design;
    
    
else
    S.period = horizon;
    S.Univariate.serie = 'QcondWL';
    S.Univariate.Q = PD_U1{1,1}; %Q from WLcondQ dataset
    S.Univariate.H = handles.PD_U2{1,1};
    S.Univariate.Q_Paramci = D_U1(1).Paramci; %paramci for Q comes from D_U1 dataset
    S.Univariate.H_Paramci = handles.D_U2(1).Paramci;
    S.Univariate.RPH_Values = zeros(3,7);
    S.Univariate.RPQ_Values = zeros(3,7);
    
    %Univariate Frequency Analysis: variable 1 (H)
    numPV1 = handles.PD_U2{1,1}.NumParameters;
    variable = 'Principal';
    [RP_UV_names,RP_UV_values] = RP_UV(numPV1,data,variable,serie,handles,PD_U1,PD_U2);
    S.Univariate.RPH_Names = RP_UV_names;
    S.Univariate.RPH_Values(2,:) = RP_UV_values;
    
    
    %Univariate Frequency Analysis: variable 2 (Q)
    numPV2 = PD_U1{1,1}.NumParameters;
    variable = 'Conditional';
    [RP_UV_names,RP_UV_values] = RP_UV(numPV2,data,variable,serie,handles,PD_U1,PD_U2);
    S.Univariate.RPQ_Names = RP_UV_names;
    S.Univariate.RPQ_Values(2,:) = RP_UV_values;
    
    % calculating the 5% and 95% percentiles of Q and H
    
    numPV1 = size(S.Univariate.H_Paramci(1,:),2);
    variable = 'Principal';
    par1 = S.Univariate.H_Paramci(1,:);
    [~,RP_UV_values_5] = RP_UV5(numPV1,data,variable,serie,handles,par1,PD_U1,PD_U2);
    S.Univariate.RPH_Values(1,:) = RP_UV_values_5;
    
    numPV1 = size(D_U1(1).Paramci(1,:),2);
    variable = 'Conditional';
    par1 = D_U1(1).Paramci(1,:);
    [~,RP_UV_values_5] = RP_UV5(numPV1,data,variable,serie,handles,par1,PD_U1,PD_U2);
    S.Univariate.RPQ_Values(1,:) = RP_UV_values_5;
    
    numPV1 = size(S.Univariate.H_Paramci(1,:),2);
    variable = 'Principal';
    par1 = S.Univariate.H_Paramci(2,:);
    [~,RP_UV_values_95] = RP_UV95(numPV1,data,variable,serie,handles,par1,PD_U1,PD_U2);
    S.Univariate.RPH_Values(3,:) = RP_UV_values_95;
    
    numPV2 = size(D_U1(1).Paramci(1,:),2);
    variable = 'Conditional';
    par1 = D_U1(1).Paramci(2,:);
    [~,RP_UV_values_95] = RP_UV95(numPV2,data,variable,serie,handles,par1,PD_U1,PD_U2);
    S.Univariate.RPQ_Values(3,:) = RP_UV_values_95;
    %Load the PD_U1,PD_U2, D_U1, D_U2 corresponding to the dataset
    if strcmp(horizon,'historic')
        f = fullfile(pth_base,outlet,'historic',serie,'\100\Results\MhAST_Results.mat');
        load(f);
    elseif strcmp(horizon,'future')
        f = fullfile(pth_base,outlet,'future',serie,'\100\Results\MhAST_Results.mat');
        load(f);
    end

    
    % Bivariate frequency analsis (AND-based copula results)
    S.Bivariate.CopulaType = copula_type;
    S.Bivariate.serie = 'QcondWL';
%     if strcmp(copula_type,'dependent')
%         S.Bivariate.DesignRP = DesignRP;
%     end
    S.Bivariate.serie = serie;
    [QH_bivariate_allQH,QH_Design,Copula_Pars,desvarnames] = RPBivariate(pth_base,outlet,copula_type,selected_copula,Design_Variables,serie, horizon,data,handles,Copula_Variables);
    if strcmp(copula_type,'dependent')
        S.Bivariate.DesVarNames = desvarnames;
        S.Bivariate.DesVarValuesall = QH_bivariate_allQH;
    end
    S.Bivariate.DesVarValues = QH_Design;
    
end
%% Part 3

if strcmp(horizon,'historic')
    historic = S;
elseif strcmp(horizon,'future')
    future = S;
end

%% Part 4
cd(fullfile(pth_base,outlet,horizon,serie,'\100\Results'))
clearvars -except historic future horizon serie outlet
eval(['save',' ', horizon,'_',serie,'_',outlet])
delete data.mat

cd('U:\Dossier_travail\705300_rehaussement_marin\3- Data\Rehaussement_marine\MhAST_Ver02.05\Post_processing')

end

