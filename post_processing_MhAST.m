clc; clear all;
cd(fullfile('/exec/mbizhani'))
outlet = 'Moulin';
% serie = 'WLcondQ';
serie = 'QcondWL';
% horizon = 'historic';
horizon = 'future';
copula_type = 'independent';
selected_copula = 'Clayton';
DesignRP = 100;

cd(fullfile('/exec/mbizhani',outlet,horizon,serie,'100/Results'))
%This bloack loads the necessary dataset for univariate frequencyanalysis.
if strcmp(horizon, 'historic')
    loadfun_historic(outlet,serie);
    load('data.mat')
elseif strcmp(horizon, 'future')
    loadfun_RM(outlet,serie);
    load('data.mat')
end

 
% calculation loop    


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
    [RP_UV_names,RP_UV_values] = RP_UV(numPV1,data,variable,serie,handles,PD_U1,PD_U2,D_U1,D_U2);
    S.Univariate.RPQ_Names = RP_UV_names;
    S.Univariate.RPQ_Values(2,:) = RP_UV_values;
    
    
    %Univariate Frequency Analysis: variable 2 (H)
    numPV2 = PD_U2{1,1}.NumParameters;
    variable = 'Conditional';
    [RP_UV_names,RP_UV_values] = RP_UV(numPV2,data,variable,serie,handles,PD_U1,PD_U2,D_U1,D_U2);
    S.Univariate.RPH_Names = RP_UV_names;
    S.Univariate.RPH_Values(2,:) = RP_UV_values;
    
    % calculating the 5% and 95% percentiles of Q and H
    
    numPV1 = size(S.Univariate.Q_Paramci(1,:),2);
    variable = 'Principal';
    par1 = S.Univariate.Q_Paramci(1,:);
    [~,RP_UV_values_5] = RP_UV5(numPV1,data,variable,serie,handles,par1,PD_U1,PD_U2,D_U1,D_U2);
    S.Univariate.RPQ_Values(1,:) = RP_UV_values_5;
    
    numPV1 = size(D_U2(1).Paramci(1,:),2);
    variable = 'Conditional';
    par1 = D_U2(1).Paramci(1,:);
    [~,RP_UV_values_5] = RP_UV5(numPV1,data,variable,serie,handles,par1,PD_U1,PD_U2,D_U1,D_U2);
    S.Univariate.RPH_Values(1,:) = RP_UV_values_5;
    
    numPV1 = size(S.Univariate.Q_Paramci(1,:),2);
    variable = 'Principal';
    par1 = S.Univariate.Q_Paramci(2,:);
    [~,RP_UV_values_95] = RP_UV95(numPV1,data,variable,serie,handles,par1,PD_U1,PD_U2,D_U1,D_U2);
    S.Univariate.RPQ_Values(3,:) = RP_UV_values_95;
    
    numPV2 = size(D_U2(1).Paramci(1,:),2);
    variable = 'Conditional';
    par1 = D_U2(1).Paramci(2,:);
    [~,RP_UV_values_95] = RP_UV95(numPV2,data,variable,serie,handles,par1,PD_U1,PD_U2,D_U1,D_U2);
    S.Univariate.RPH_Values(3,:) = RP_UV_values_95;
    %Load the PD_U1,PD_U2, D_U1, D_U2 corresponding to the dataset
    if strcmp(horizon,'historic')
        f = fullfile('/exec/mbizhani',outlet,'historic',serie,'100/Results/MhAST_Results.mat');
        load(f);
    elseif strcmp(horizon,'future')
        f = fullfile('/exec/mbizhani',outlet,'future',serie,'100/Results/MhAST_Results.mat');
        load(f);
    end
    
    
    % Bivariate frequency analsis (AND-based copula results)
    S.Bivariate.CopulaType = copula_type;
    S.Bivariate.serie = 'WLcondQ';
%     if strcmp(copula_type,'dependent')
%         S.Bivariate.DesignRP = DesignRP;
%     end
    S.Bivariate.serie = serie;
    [QH_bivariate_allQH,QH_Design,Copula_Pars,desvarnames] = RPBivariate(copula_type,selected_copula,Design_Variables,serie, S,DesignRP,data,handles,Copula_Variables,outlet,horizon);
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
    [RP_UV_names,RP_UV_values] = RP_UV(numPV1,data,variable,serie,handles,PD_U1,PD_U2,D_U1,D_U2);
    S.Univariate.RPH_Names = RP_UV_names;
    S.Univariate.RPH_Values(2,:) = RP_UV_values;
    
    
    %Univariate Frequency Analysis: variable 2 (Q)
    numPV2 = PD_U1{1,1}.NumParameters;
    variable = 'Conditional';
    [RP_UV_names,RP_UV_values] = RP_UV(numPV2,data,variable,serie,handles,PD_U1,PD_U2,D_U1,D_U2);
    S.Univariate.RPQ_Names = RP_UV_names;
    S.Univariate.RPQ_Values(2,:) = RP_UV_values;
    
    % calculating the 5% and 95% percentiles of Q and H
    
    numPV1 = size(S.Univariate.H_Paramci(1,:),2);
    variable = 'Principal';
    par1 = S.Univariate.H_Paramci(1,:);
    [~,RP_UV_values_5] = RP_UV5(numPV1,data,variable,serie,handles,par1,PD_U1,PD_U2,D_U1,D_U2);
    S.Univariate.RPH_Values(1,:) = RP_UV_values_5;
    
    numPV1 = size(D_U1(1).Paramci(1,:),2);
    variable = 'Conditional';
    par1 = D_U1(1).Paramci(1,:);
    [~,RP_UV_values_5] = RP_UV5(numPV1,data,variable,serie,handles,par1,PD_U1,PD_U2,D_U1,D_U2);
    S.Univariate.RPQ_Values(1,:) = RP_UV_values_5;
    
    numPV1 = size(S.Univariate.H_Paramci(1,:),2);
    variable = 'Principal';
    par1 = S.Univariate.H_Paramci(2,:);
    [~,RP_UV_values_95] = RP_UV95(numPV1,data,variable,serie,handles,par1,PD_U1,PD_U2,D_U1,D_U2);
    S.Univariate.RPH_Values(3,:) = RP_UV_values_95;
    
    numPV2 = size(D_U1(1).Paramci(1,:),2);
    variable = 'Conditional';
    par1 = D_U1(1).Paramci(2,:);
    [~,RP_UV_values_95] = RP_UV95(numPV2,data,variable,serie,handles,par1,PD_U1,PD_U2,D_U1,D_U2);
    S.Univariate.RPQ_Values(3,:) = RP_UV_values_95;
    %Load the PD_U1,PD_U2, D_U1, D_U2 corresponding to the dataset
    if strcmp(horizon,'historic')
        f = fullfile('/exec/mbizhani',outlet,'historic',serie,'100/Results/MhAST_Results.mat');
        load(f);
    elseif strcmp(horizon,'future')
        f = fullfile('/exec/mbizhani',outlet,'future',serie,'100/Results/MhAST_Results.mat');
        load(f);
    end

    
    % Bivariate frequency analsis (AND-based copula results)
    S.Bivariate.CopulaType = copula_type;
    S.Bivariate.serie = 'QcondWL';
%     if strcmp(copula_type,'dependent')
%         S.Bivariate.DesignRP = DesignRP;
%     end
    S.Bivariate.serie = serie;
    [QH_bivariate_allQH,QH_Design,Copula_Pars,desvarnames] = RPBivariate(copula_type,selected_copula,Design_Variables,serie, S,DesignRP,data,handles,Copula_Variables,outlet,horizon);
    if strcmp(copula_type,'dependent')
        S.Bivariate.DesVarNames = desvarnames;
        S.Bivariate.DesVarValuesall = QH_bivariate_allQH;
    end
    S.Bivariate.DesVarValues = QH_Design;
    
end

if strcmp(horizon,'historic')
    historic = S;
elseif strcmp(horizon,'future')
    future = S;
end


cd(fullfile('/exec/mbizhani',outlet,horizon,serie,'100/Results'))
clearvars -except historic future horizon serie outlet
eval(['save',' ', horizon,'_',serie,'_',outlet])
delete data.mat


% Functions
function loadfun_historic(outlet,serie)
if strcmp(serie,'WLcondQ')
    f = fullfile('/exec/mbizhani',outlet,'historic',serie,'100/Results/MhAST_Results.mat');
    load(f);
    g = fullfile('/exec/mbizhani',outlet,'historic','QcondWL','100/Results/MhAST_Results.mat'); 
    load(g,'PD_U2','D_U2');
    save('data.mat')
elseif strcmp(serie,'QcondWL')
    
    f = fullfile('/exec/mbizhani',outlet,'historic',serie,'100/Results/MhAST_Results.mat');
    load(f);
    g = fullfile('/exec/mbizhani',outlet,'historic','WLcondQ','100/Results/MhAST_Results.mat'); 
    load(g,'PD_U1','D_U1');
    save('data.mat')
end
end

function loadfun_RM(outlet,serie)
if strcmp(serie,'WLcondQ')
    f = fullfile('/exec/mbizhani',outlet,'future',serie,'100/Results/MhAST_Results.mat');
    load(f);
    g = fullfile('/exec/mbizhani',outlet,'future','QcondWL','100/Results/MhAST_Results.mat'); 
    load(g,'PD_U2','D_U2');
    save('data.mat')
elseif strcmp(serie,'QcondWL')
    
    f = fullfile('/exec/mbizhani',outlet,'future',serie,'100/Results/MhAST_Results.mat');
    load(f);
    g = fullfile('/exec/mbizhani',outlet,'future','WLcondQ','100/Results/MhAST_Results.mat'); 
    load(g,'PD_U1','D_U1');
    save('data.mat')
end
end



function [RP_V1_percentileNames,RP_V1] = RP_UV(npar,data,variable,serie,handles,PD_U1,PD_U2,D_U1,D_U2)

if strcmp(serie,'WLcondQ')
    if strcmp(variable,'Principal')
        RP_V1_percentileNames = {'Q2','Q5','Q10','Q20','Q50','Q100','Q350'};
        par = handles.PD_U1{1,1}.ParameterValues;
        dist = handles.PD_U1{1,1};
        DD = data(:,1);
        
    elseif strcmp(variable,'Conditional')
        RP_V1_percentileNames = {'H2','H5','H10','H20','H50','H100','H350'};
        par = PD_U2{1,1}.ParameterValues;
        dist = PD_U2{1,1};
        DD = data(:,2);
    end
elseif strcmp(serie,'QcondWL')
    if strcmp(variable,'Principal')
        RP_V1_percentileNames = {'H2','H5','H10','H20','H50','H100','H350'};
        par = handles.PD_U2{1,1}.ParameterValues;
        dist = handles.PD_U2{1,1};
        DD = data(:,2);
    elseif strcmp(variable,'Conditional')
        RP_V1_percentileNames = {'Q2','Q5','Q10','Q20','Q50','Q100','Q350'};
        par = PD_U1{1,1}.ParameterValues;
        dist = PD_U1{1,1};
        DD = data(:,1);
    end
end
            
if npar ==1

    a = sort(DD,'ascend');
    Q_star = a(1);
    Q2 = icdf(dist,0.5,par(1));
    Q5 = icdf(dist,0.80,par(1));
    Q10 = icdf(dist,0.9,par(1));
    Q20 = icdf(dist,0.95,par(1));
    Q25 = icdf(dist,(1-1/25),par(1));
    Q50 = icdf(dist,0.98,par(1));
    Q100 = icdf(dist,0.99,par(1));
    Q350 = icdf(dist,(1-1/350),par(1));
    RP_V1 = [Q2 Q5 Q10 Q20 Q50 Q100 Q350];
    
    
elseif npar ==2
    
    a = sort(DD,'ascend');
    Q_star = a(1);
    Q2 = icdf(dist,0.5,par(1),par(2));
    Q5 = icdf(dist,0.80,par(1),par(2));
    Q10 = icdf(dist,0.9,par(1),par(2));
    Q20 = icdf(dist,0.95,par(1),par(2));
    Q25 = icdf(dist,(1-1/25),par(1),par(2));
    Q50 = icdf(dist,0.98,par(1),par(2));
    Q100 = icdf(dist,0.99,par(1),par(2));
    Q350 = icdf(dist,(1-1/350),par(1),par(2));
    RP_V1 = [Q2 Q5 Q10 Q20 Q50 Q100 Q350];
    
elseif npar ==3

    a = sort(DD,'ascend');
    Q_star = a(1);
    Q2 = icdf(dist,0.5,par(1),par(2),par(3));
    Q5 = icdf(dist,0.80,par(1),par(2),par(3));
    Q10 = icdf(dist,0.9,par(1),par(2),par(3));
    Q20 = icdf(dist,0.95,par(1),par(2),par(3));
    Q25 = icdf(dist,(1-1/25),par(1),par(2),par(3));
    Q50 = icdf(dist,0.98,par(1),par(2),par(3));
    Q100 = icdf(dist,0.99,par(1),par(2),par(3));
    Q350 = icdf(dist,(1-1/350),par(1),par(2),par(3));
    RP_V1 = [Q2 Q5 Q10 Q20 Q50 Q100 Q350];
end
end



function [RP_V1_percentileNames,RP_V1] = RP_UV5(npar,data,variable,serie,handles,par,PD_U1,PD_U2,D_U1,D_U2)

if strcmp(serie,'WLcondQ')
    if strcmp(variable,'Principal')
        RP_V1_percentileNames = {'Q2','Q5','Q10','Q20','Q50','Q100','Q350'};
%         par = historic.Univariate.Q_Paramci(1,:);
        dist = handles.PD_U1{1,1};
        DD = data(:,1);
        
    elseif strcmp(variable,'Conditional')
        RP_V1_percentileNames = {'H2','H5','H10','H20','H50','H100','H350'};
%         par = historic.Univariate.H_Paramci(1,:);
        dist = PD_U2{1,1};
        DD = data(:,2);
    end
elseif strcmp(serie,'QcondWL')
    if strcmp(variable,'Principal')
        RP_V1_percentileNames = {'H2','H5','H10','H20','H50','H100','H350'};
%         par = historic.Univariate.H_Paramci(1,:);
        dist = handles.PD_U2{1,1};
        DD = data(:,2);
    elseif strcmp(variable,'Conditional')
        RP_V1_percentileNames = {'Q2','Q5','Q10','Q20','Q50','Q100','Q350'};
%         par = historic.Univariate.Q_Paramci(1,:);
        dist = PD_U1{1,1};
        DD = data(:,1);
    end
end
            
if npar ==1

    a = sort(DD,'ascend');
    Q_star = a(1);
    Q2 = icdf(dist,0.5,par(1));
    Q5 = icdf(dist,0.80,par(1));
    Q10 = icdf(dist,0.9,par(1));
    Q20 = icdf(dist,0.95,par(1));
    Q25 = icdf(dist,(1-1/25),par(1));
    Q50 = icdf(dist,0.98,par(1));
    Q100 = icdf(dist,0.99,par(1));
    Q350 = icdf(dist,(1-1/350),par(1));
    RP_V1 = [Q2 Q5 Q10 Q20 Q50 Q100 Q350];
    
    
elseif npar ==2
    
    a = sort(DD,'ascend');
    Q_star = a(1);
    Q2 = icdf(dist,0.5,par(1),par(2));
    Q5 = icdf(dist,0.80,par(1),par(2));
    Q10 = icdf(dist,0.9,par(1),par(2));
    Q20 = icdf(dist,0.95,par(1),par(2));
    Q25 = icdf(dist,(1-1/25),par(1),par(2));
    Q50 = icdf(dist,0.98,par(1),par(2));
    Q100 = icdf(dist,0.99,par(1),par(2));
    Q350 = icdf(dist,(1-1/350),par(1),par(2));
    RP_V1 = [Q2 Q5 Q10 Q20 Q50 Q100 Q350];
    
elseif npar ==3

    a = sort(DD,'ascend');
    Q_star = a(1);
    Q2 = icdf(dist,0.5,par(1),par(2),par(3));
    Q5 = icdf(dist,0.80,par(1),par(2),par(3));
    Q10 = icdf(dist,0.9,par(1),par(2),par(3));
    Q20 = icdf(dist,0.95,par(1),par(2),par(3));
    Q25 = icdf(dist,(1-1/25),par(1),par(2),par(3));
    Q50 = icdf(dist,0.98,par(1),par(2),par(3));
    Q100 = icdf(dist,0.99,par(1),par(2),par(3));
    Q350 = icdf(dist,(1-1/350),par(1),par(2),par(3));
    RP_V1 = [Q2 Q5 Q10 Q20 Q50 Q100 Q350];
end
end


function [RP_V1_percentileNames,RP_V1] = RP_UV95(npar,data,variable,serie,handles,par,PD_U1,PD_U2,D_U1,D_U2)

if strcmp(serie,'WLcondQ')
    if strcmp(variable,'Principal')
        RP_V1_percentileNames = {'Q2','Q5','Q10','Q20','Q50','Q100','Q350'};
%         par = historic.Univariate.Q_Paramci(1,:);
        dist = handles.PD_U1{1,1};
        DD = data(:,1);
        
    elseif strcmp(variable,'Conditional')
        RP_V1_percentileNames = {'H2','H5','H10','H20','H50','H100','H350'};
%         par = historic.Univariate.H_Paramci(1,:);
        dist = PD_U2{1,1};
        DD = data(:,2);
    end
elseif strcmp(serie,'QcondWL')
    if strcmp(variable,'Principal')
        RP_V1_percentileNames = {'H2','H5','H10','H20','H50','H100','H350'};
%         par = historic.Univariate.H_Paramci(1,:);
        dist = handles.PD_U2{1,1};
        DD = data(:,2);
    elseif strcmp(variable,'Conditional')
        RP_V1_percentileNames = {'Q2','Q5','Q10','Q20','Q50','Q100','Q350'};
%         par = historic.Univariate.Q_Paramci(1,:);
        dist = PD_U1{1,1};
        DD = data(:,1);
    end
end
            
if npar ==1

    a = sort(DD,'ascend');
    Q_star = a(1);
    Q2 = icdf(dist,0.5,par(1));
    Q5 = icdf(dist,0.80,par(1));
    Q10 = icdf(dist,0.9,par(1));
    Q20 = icdf(dist,0.95,par(1));
    Q25 = icdf(dist,(1-1/25),par(1));
    Q50 = icdf(dist,0.98,par(1));
    Q100 = icdf(dist,0.99,par(1));
    Q350 = icdf(dist,(1-1/350),par(1));
    RP_V1 = [Q2 Q5 Q10 Q20 Q50 Q100 Q350];
    
    
elseif npar ==2
    
    a = sort(DD,'ascend');
    Q_star = a(1);
    Q2 = icdf(dist,0.5,par(1),par(2));
    Q5 = icdf(dist,0.80,par(1),par(2));
    Q10 = icdf(dist,0.9,par(1),par(2));
    Q20 = icdf(dist,0.95,par(1),par(2));
    Q25 = icdf(dist,(1-1/25),par(1),par(2));
    Q50 = icdf(dist,0.98,par(1),par(2));
    Q100 = icdf(dist,0.99,par(1),par(2));
    Q350 = icdf(dist,(1-1/350),par(1),par(2));
    RP_V1 = [Q2 Q5 Q10 Q20 Q50 Q100 Q350];
    
elseif npar ==3

    a = sort(DD,'ascend');
    Q_star = a(1);
    Q2 = icdf(dist,0.5,par(1),par(2),par(3));
    Q5 = icdf(dist,0.80,par(1),par(2),par(3));
    Q10 = icdf(dist,0.9,par(1),par(2),par(3));
    Q20 = icdf(dist,0.95,par(1),par(2),par(3));
    Q25 = icdf(dist,(1-1/25),par(1),par(2),par(3));
    Q50 = icdf(dist,0.98,par(1),par(2),par(3));
    Q100 = icdf(dist,0.99,par(1),par(2),par(3));
    Q350 = icdf(dist,(1-1/350),par(1),par(2),par(3));
    RP_V1 = [Q2 Q5 Q10 Q20 Q50 Q100 Q350];
end
end




function [QH_bivariate,QH_Design,Copula_pars,desvarnames] = RPBivariate(copula_type,selected_copula,Design_Variables,serie,historic,DesignRP,data,handles,Copula_Variables,outlet,horizon)

if strcmp(copula_type,'dependent')
    desvarnames = {'Q','H'};
     [Copula_pars,QH_Design,QH_bivariate] = find_bivariate_results(selected_copula,Copula_Variables,Design_Variables);
     RP100.desvarnames = desvarnames;
     RP100.Copula_pars = Copula_pars;
     RP100.selected_copula = selected_copula;
     RP100.QH_Design = QH_Design;
     RP100.QH_bivariate_all = QH_bivariate;

    % Now find the DesignRP for 2 year return period
    % step1: load the data
    f = fullfile('/exec/mbizhani',outlet,horizon,serie,'2/Results/MhAST_Results.mat');
    load(f,'Copula_Variables','Design_Variables')
    
    desvarnames = {'Q','H'};
    [Copula_pars,QH_Design,QH_bivariate] = find_bivariate_results(selected_copula,Copula_Variables,Design_Variables);
    RP2.desvarnames = desvarnames;
    RP2.Copula_pars = Copula_pars;
    RP2.selected_copula = selected_copula;
    RP2.QH_Design = QH_Design;
    RP2.QH_bivariate_all = QH_bivariate;
    
    % now for RP350
    f = fullfile('/exec/mbizhani',outlet,horizon,serie,'350/Results/MhAST_Results.mat');
    load(f,'Copula_Variables','Design_Variables')
    
    desvarnames = {'Q','H'};
    [Copula_pars,QH_Design,QH_bivariate] = find_bivariate_results(selected_copula,Copula_Variables,Design_Variables);
    RP350.desvarnames = desvarnames;
    RP350.Copula_pars = Copula_pars;
    RP350.selected_copula = selected_copula;
    RP350.QH_Design = QH_Design;
    RP350.QH_bivariate_all = QH_bivariate;
    
    
    QH_Design = struct('RP2',RP2,'RP100',RP100,'RP350',RP350);
    QH_bivariate = 'NaN'; %we already save the variable inside QH_Design
    Copula_pars = RP350.Copula_pars;
    
elseif strcmp(copula_type,'independent')
    % 2, 100, and 350 years are calculated regardless of specified DesignRP value.   
%     if DesignRP == 2
         desvarnames = {'Q_star','H2','Q1.2','H1.7','Q1.4','H1.4','Q1.7','H1.2','Q2','H_star'};
%         selected_copula = 'independent';
%         Copula_pars = 'NaN';
%         if strcmp(serie,'WLcondQ')
            npar = handles.PD_U1{1,1}.NumParameters;
            if npar ==1
                par = handles.PD_U1{1,1}.ParameterValues;
                dist = handles.PD_U1{1,1};
                a = sort(data(:,1),'ascend');
                Q_star = a(1);
                Q1_2 = icdf(dist,1-1/1.2,par(1));
                Q1_4 = icdf(dist,1-1/1.4,par(1));
                Q1_7 = icdf(dist,1-1/1.7,par(1));
                Q2 = icdf(dist,0.5,par(1));
                RP_QB2 = [Q_star Q1_2 Q1_4 Q1_7 Q2];                
                
            elseif npar ==2
                par = handles.PD_U1{1,1}.ParameterValues;
                dist = handles.PD_U1{1,1};
                a = sort(data(:,1),'ascend');
                Q_star = a(1);
                Q1_2 = icdf(dist,1-1/1.2,par(1),par(2));
                Q1_4 = icdf(dist,1-1/1.4,par(1),par(2));
                Q1_7 = icdf(dist,1-1/1.7,par(1),par(2));
                Q2 = icdf(dist,0.5,par(1),par(2));
                RP_QB2 = [Q_star Q1_2 Q1_4 Q1_7 Q2];
                
            elseif npar ==3
                par = handles.PD_U1{1,1}.ParameterValues;
                dist = handles.PD_U1{1,1};
                a = sort(data(:,1),'ascend');
                Q_star = a(1);
                Q1_2 = icdf(dist,1-1/1.2,par(1),par(2),par(3));
                Q1_4 = icdf(dist,1-1/1.4,par(1),par(2),par(3));
                Q1_7 = icdf(dist,1-1/1.7,par(1),par(2),par(3));
                Q2 = icdf(dist,0.5,par(1),par(2),par(3));
                RP_QB2 = [Q_star Q1_2 Q1_4 Q1_7 Q2];
            end
            
            %Univariate Frequency Analysis: variable 2
            npar = handles.PD_U2{1,1}.NumParameters;
            if npar ==1
                par = handles.PD_U2{1,1}.ParameterValues;
                dist = handles.PD_U2{1,1};
                a = sort(data(:,2),'ascend');
                H_star = a(1);
                H1_2 = icdf(dist,1-1/1.2,par(1));
                H1_4 = icdf(dist,1-1/1.4,par(1));
                H1_7 = icdf(dist,1-1/1.7,par(1));
                H2 = icdf(dist,0.5,par(1));
                RP_HB2 = [H_star H1_2 H1_4 H1_7 H2];
                
            elseif npar ==2
                par = handles.PD_U2{1,1}.ParameterValues;
                dist = handles.PD_U2{1,1};
                a = sort(data(:,2),'ascend');
                H_star = a(1);
                H1_2 = icdf(dist,1-1/1.2,par(1),par(2));
                H1_4 = icdf(dist,1-1/1.4,par(1),par(2));
                H1_7 = icdf(dist,1-1/1.7,par(1),par(2));
                H2 = icdf(dist,0.5,par(1),par(2));
                RP_HB2 = [H_star H1_2 H1_4 H1_7 H2];
                
            elseif npar ==3
                par = handles.PD_U2{1,1}.ParameterValues;
                dist = handles.PD_U2{1,1};
                a = sort(data(:,2),'ascend');
                H_star = a(1);
                H1_2 = icdf(dist,1-1/1.2,par(1),par(2),par(3));
                H1_4 = icdf(dist,1-1/1.4,par(1),par(2),par(3));
                H1_7 = icdf(dist,1-1/1.7,par(1),par(2),par(3));
                H2 = icdf(dist,0.5,par(1),par(2),par(3));
                RP_HB2 = [H_star H1_2 H1_4 H1_7 H2];
            end
            QH_bivariate = Design_Variables.DesignValue_MaxDens.Copula_based_AND(6).WeightedSample;
            QH_Design = ones(1,10);
            QH_Design(1,1) = RP_QB2(1,1);
            QH_Design(1,3) = RP_QB2(1,2);
            QH_Design(1,5) = RP_QB2(1,3);
            QH_Design(1,7) = RP_QB2(1,4);
            QH_Design(1,9) = RP_QB2(1,5);
            
            QH_Design(1,10) = RP_HB2(1,1);
            QH_Design(1,8) = RP_HB2(1,2);
            QH_Design(1,6) = RP_HB2(1,3);
            QH_Design(1,4) = RP_HB2(1,4);
            QH_Design(1,2) = RP_HB2(1,5);

    RP2.desvarnames = desvarnames;
    RP2.Copula_pars = 'NaN';
    RP2.selected_copula = 'independent';
    RP2.QH_bivariate = QH_Design;

%     elseif DesignRP == 100
         desvarnames = {'Q_star','H100','Q2','H50','Q5','H20','Q10','H10','Q20','H5','Q50','H2','Q100','H_star'};
%         selected_copula = 'independent';
%         Copula_pars = 'NaN';
        npar = handles.PD_U1{1,1}.NumParameters;
        if npar ==1
            par = handles.PD_U1{1,1}.ParameterValues;
            dist = handles.PD_U1{1,1};
            a = sort(data(:,1),'ascend');
            Q_star = a(1);
            Q2 = icdf(dist,0.5,par(1));
            Q5 = icdf(dist,1-1/5,par(1));
            Q10 = icdf(dist,1-1/10,par(1));
            Q20 = icdf(dist,1-1/20,par(1));
            Q50 = icdf(dist,1-1/50,par(1));
            Q100 = icdf(dist,1-1/100,par(1));
            RP_QB100 = [Q_star Q2 Q5 Q10 Q20 Q50 Q100];
            
        elseif npar ==2
            par = handles.PD_U1{1,1}.ParameterValues;
            dist = handles.PD_U1{1,1};
            a = sort(data(:,1),'ascend');
            Q_star = a(1);
            Q2 = icdf(dist,0.5,par(1),par(2));
            Q5 = icdf(dist,1-1/5,par(1),par(2));
            Q10 = icdf(dist,1-1/10,par(1),par(2));
            Q20 = icdf(dist,1-1/20,par(1),par(2));
            Q50 = icdf(dist,1-1/50,par(1),par(2));
            Q100 = icdf(dist,1-1/100,par(1),par(2));
            RP_QB100 = [Q_star Q2 Q5 Q10 Q20 Q50 Q100];
            
        elseif npar ==3
            par = handles.PD_U1{1,1}.ParameterValues;
            dist = handles.PD_U1{1,1};
            a = sort(data(:,1),'ascend');
            Q_star = a(1);
            Q2 = icdf(dist,0.5,par(1),par(2),par(3));
            Q5 = icdf(dist,1-1/5,par(1),par(2),par(3));
            Q10 = icdf(dist,1-1/10,par(1),par(2),par(3));
            Q20 = icdf(dist,1-1/20,par(1),par(2),par(3));
            Q50 = icdf(dist,1-1/50,par(1),par(2),par(3));
            Q100 = icdf(dist,1-1/100,par(1),par(2),par(3));
            RP_QB100 = [Q_star Q2 Q5 Q10 Q20 Q50 Q100];
            
        end
        
        %Univariate Frequency Analysis: variable 2
        npar = handles.PD_U2{1,1}.NumParameters;
        if npar ==1
            par = handles.PD_U2{1,1}.ParameterValues;
            dist = handles.PD_U2{1,1};
            a = sort(data(:,2),'ascend');
            H_star = a(1);
            H2 = icdf(dist,0.5,par(1));
            H5 = icdf(dist,1-1/5,par(1));
            H10 = icdf(dist,1-1/10,par(1));
            H20 = icdf(dist,1-1/20,par(1));
            H50 = icdf(dist,1-1/50,par(1));
            H100 = icdf(dist,1-1/100,par(1));
            RP_HB100 = [H_star H2 H5 H10 H20 H50 H100];
            
        elseif npar ==2
            par = handles.PD_U2{1,1}.ParameterValues;
            dist = handles.PD_U2{1,1};
            a = sort(data(:,2),'ascend');
            H_star = a(1);
            H2 = icdf(dist,0.5,par(1),par(2));
            H5 = icdf(dist,1-1/5,par(1),par(2));
            H10 = icdf(dist,1-1/10,par(1),par(2));
            H20 = icdf(dist,1-1/20,par(1),par(2));
            H50 = icdf(dist,1-1/50,par(1),par(2));
            H100 = icdf(dist,1-1/100,par(1),par(2));
            RP_HB100 = [H_star H2 H5 H10 H20 H50 H100];
            
        elseif npar ==3
            par = handles.PD_U2{1,1}.ParameterValues;
            dist = handles.PD_U2{1,1};
            a = sort(data(:,2),'ascend');
            H_star = a(1);
            H2 = icdf(dist,0.5,par(1),par(2),par(3));
            H5 = icdf(dist,1-1/5,par(1),par(2),par(3));
            H10 = icdf(dist,1-1/10,par(1),par(2),par(3));
            H20 = icdf(dist,1-1/20,par(1),par(2),par(3));
            H50 = icdf(dist,1-1/50,par(1),par(2),par(3));
            H100 = icdf(dist,1-1/100,par(1),par(2),par(3));
            RP_HB100 = [H_star H2 H5 H10 H20 H50 H100];
        end
        
        
        QH_bivariate = Design_Variables.DesignValue_MaxDens.Copula_based_AND(6).WeightedSample;
        QH_Design = ones(1,14);
        QH_Design(1,1) = RP_QB100(1,1);
        QH_Design(1,3) = RP_QB100(1,2);
        QH_Design(1,5) = RP_QB100(1,3);
        QH_Design(1,7) = RP_QB100(1,4);
        QH_Design(1,9) = RP_QB100(1,5);
        QH_Design(1,11) = RP_QB100(1,6);
        QH_Design(1,13) = RP_QB100(1,7);
        
        QH_Design(1,14) = RP_HB100(1,1);
        QH_Design(1,12) = RP_HB100(1,2);
        QH_Design(1,10) = RP_HB100(1,3);
        QH_Design(1,8) = RP_HB100(1,4);
        QH_Design(1,6) = RP_HB100(1,5);
        QH_Design(1,4) = RP_HB100(1,6);
        QH_Design(1,2) = RP_HB100(1,7);
        
    RP100.desvarnames = desvarnames;
    RP100.Copula_pars = 'NaN';
    RP100.selected_copula = 'independent';
    RP100.QH_bivariate = QH_Design;
        
%     elseif DesignRP ==350
        
        desvarnames = {'Q_star','H350','Q3.74','H93.54','Q9.35','H37.42','Q18.71','H18.71','Q37.42','H9.35','Q93.54','H3.74','Q350','H_star'};
%         selected_copula = 'independent';
%         Copula_pars = 'NaN';
    npar = handles.PD_U1{1,1}.NumParameters;
        if npar ==1
            par = handles.PD_U1{1,1}.ParameterValues;
            dist = handles.PD_U1{1,1};
            a = sort(data(:,1),'ascend');
            Q_star = a(1);
            Q3_74 = icdf(dist,1-1/3.74,par(1));
            Q9_35 = icdf(dist,1-1/9.35,par(1));
            Q18_71 = icdf(dist,1-1/18.71,par(1));
            Q37_42 = icdf(dist,1-1/37.42,par(1));
            Q93_54 = icdf(dist,1-1/93.54,par(1));
            Q350 = icdf(dist,1-1/350,par(1));
            RP_QB350 = [Q_star Q3_74 Q9_35 Q18_71 Q37_42 Q93_54 Q350];
            
        elseif npar ==2
            par = handles.PD_U1{1,1}.ParameterValues;
            dist = handles.PD_U1{1,1};
            a = sort(data(:,1),'ascend');
            Q_star = a(1);
            Q3_74 = icdf(dist,1-1/3.74,par(1),par(2));
            Q9_35 = icdf(dist,1-1/9.35,par(1),par(2));
            Q18_71 = icdf(dist,1-1/18.71,par(1),par(2));
            Q37_42 = icdf(dist,1-1/37.42,par(1),par(2));
            Q93_54 = icdf(dist,1-1/93.54,par(1),par(2));
            Q350 = icdf(dist,1-1/350,par(1),par(2));
            RP_QB350 = [Q_star Q3_74 Q9_35 Q18_71 Q37_42 Q93_54 Q350];
            
        elseif npar ==3
            par = handles.PD_U1{1,1}.ParameterValues;
            dist = handles.PD_U1{1,1};
            a = sort(data(:,1),'ascend');
            Q_star = a(1);
            Q3_74 = icdf(dist,1-1/3.74,par(1),par(2),par(3));
            Q9_35 = icdf(dist,1-1/9.35,par(1),par(2),par(3));
            Q18_71 = icdf(dist,1-1/18.71,par(1),par(2),par(3));
            Q37_42 = icdf(dist,1-1/37.42,par(1),par(2),par(3));
            Q93_54 = icdf(dist,1-1/93.54,par(1),par(2),par(3));
            Q350 = icdf(dist,1-1/350,par(1),par(2),par(3));
            RP_QB350 = [Q_star Q3_74 Q9_35 Q18_71 Q37_42 Q93_54 Q350];
            
        end
        
        %Univariate Frequency Analysis: variable 2
        npar = handles.PD_U2{1,1}.NumParameters;
        if npar ==1
            par = handles.PD_U2{1,1}.ParameterValues;
            dist = handles.PD_U2{1,1};
            a = sort(data(:,2),'ascend');
            H_star = a(1);
            H3_74 = icdf(dist,1-1/3.74,par(1));
            H9_35 = icdf(dist,1-1/9.35,par(1));
            H18_71 = icdf(dist,1-1/18.71,par(1));
            H37_42 = icdf(dist,1-1/37.42,par(1));
            H93_54 = icdf(dist,1-1/93.54,par(1));
            H350 = icdf(dist,1-1/350,par(1));
            RP_HB350 = [H_star H3_74 H9_35 H18_71 H37_42 H93_54 H350];
            
        elseif npar ==2
            par = handles.PD_U2{1,1}.ParameterValues;
            dist = handles.PD_U2{1,1};
            a = sort(data(:,2),'ascend');
            H_star = a(1);
            H3_74 = icdf(dist,1-1/3.74,par(1),par(2));
            H9_35 = icdf(dist,1-1/9.35,par(1),par(2));
            H18_71 = icdf(dist,1-1/18.71,par(1),par(2));
            H37_42 = icdf(dist,1-1/37.42,par(1),par(2));
            H93_54 = icdf(dist,1-1/93.54,par(1),par(2));
            H350 = icdf(dist,1-1/350,par(1),par(2));
            RP_HB350 = [H_star H3_74 H9_35 H18_71 H37_42 H93_54 H350];
            
        elseif npar ==3
            par = handles.PD_U2{1,1}.ParameterValues;
            dist = handles.PD_U2{1,1};
            a = sort(data(:,2),'ascend');
            H_star = a(1);
            H3_74 = icdf(dist,1-1/3.74,par(1),par(2),par(3));
            H9_35 = icdf(dist,1-1/9.35,par(1),par(2),par(3));
            H18_71 = icdf(dist,1-1/18.71,par(1),par(2),par(3));
            H37_42 = icdf(dist,1-1/37.42,par(1),par(2),par(3));
            H93_54 = icdf(dist,1-1/93.54,par(1),par(2),par(3));
            H350 = icdf(dist,1-1/350,par(1),par(2),par(3));
            RP_HB350 = [H_star H3_74 H9_35 H18_71 H37_42 H93_54 H350];
        end
        
        
        QH_bivariate = Design_Variables.DesignValue_MaxDens.Copula_based_AND(6).WeightedSample;
        QH_Design = ones(1,14);
        QH_Design(1,1) = RP_QB350(1,1);
        QH_Design(1,3) = RP_QB350(1,2);
        QH_Design(1,5) = RP_QB350(1,3);
        QH_Design(1,7) = RP_QB350(1,4);
        QH_Design(1,9) = RP_QB350(1,5);
        QH_Design(1,11) = RP_QB350(1,6);
        QH_Design(1,13) = RP_QB350(1,7);
        
        QH_Design(1,14) = RP_HB350(1,1);
        QH_Design(1,12) = RP_HB350(1,2);
        QH_Design(1,10) = RP_HB350(1,3);
        QH_Design(1,8) = RP_HB350(1,4);
        QH_Design(1,6) = RP_HB350(1,5);
        QH_Design(1,4) = RP_HB350(1,6);
        QH_Design(1,2) = RP_HB350(1,7);
    RP350.desvarnames = desvarnames;
    RP350.Copula_pars = 'NaN';
    RP350.selected_copula = 'independent';
    RP350.QH_bivariate = QH_Design;
%     end
QH_Design = struct('RP2',RP2,'RP100',RP100,'RP350',RP350);
Copula_pars = 'NaN';

    
end
end


function [Copula_pars,QH_Design,QH_bivariate] = find_bivariate_results(selected_copula,Copula_Variables,Design_Variables)
switch selected_copula
    case 'Gaussian'
        Copula_pars = Copula_Variables.PAR.MC(1,1);
        QH_Design = Design_Variables.DesignValue_MaxDens.Copula_based_AND(1).MaxDens;
        QH_bivariate = Design_Variables.DesignValue_MaxDens.Copula_based_AND(1).WeightedSample;
    case 't'
        Copula_pars = Copula_Variables.PAR.MC(2,1:2);
        QH_Design = Design_Variables.DesignValue_MaxDens.Copula_based_AND(2).MaxDens;
        QH_bivariate = Design_Variables.DesignValue_MaxDens.Copula_based_AND(2).WeightedSample;
    case 'Clayton'
        Copula_pars = Copula_Variables.PAR.MC(3,1);
        QH_Design = Design_Variables.DesignValue_MaxDens.Copula_based_AND(3).MaxDens;
        QH_bivariate = Design_Variables.DesignValue_MaxDens.Copula_based_AND(3).WeightedSample;
    case 'Frank'
        Copula_pars = Copula_Variables.PAR.MC(4,1);
        QH_Design = Design_Variables.DesignValue_MaxDens.Copula_based_AND(4).MaxDens;
        QH_bivariate = Design_Variables.DesignValue_MaxDens.Copula_based_AND(4).WeightedSample;
    case 'Gumbel'
        Copula_pars = Copula_Variables.PAR.MC(5,1);
        QH_Design = Design_Variables.DesignValue_MaxDens.Copula_based_AND(5).MaxDens;
        QH_bivariate = Design_Variables.DesignValue_MaxDens.Copula_based_AND(5).WeightedSample;
    case 'Independence' % Copula #6 % DOUBLE-CHEKCED
        % Based on Wikipedia: https://en.wikipedia.org/wiki/Copula_(probability_theory)
        Copula_pars = Copula_Variables.PAR.MC(6,1);
        QH_Design = Design_Variables.DesignValue_MaxDens.Copula_based_AND(6).MaxDens;
        QH_bivariate = Design_Variables.DesignValue_MaxDens.Copula_based_AND(6).WeightedSample;
        
    case 'AMH' % 'Ali-Mikhail-Haq' % Copula #7 % DOUBLE-CHEKCED
        Copula_pars = Copula_Variables.PAR.MC(7,1);
        QH_Design = Design_Variables.DesignValue_MaxDens.Copula_based_AND(7).MaxDens;
        QH_bivariate = Design_Variables.DesignValue_MaxDens.Copula_based_AND(7).WeightedSample;
        
    case 'Joe' % Copula #8 % DOUBLE-CHEKCED
        Copula_pars = Copula_Variables.PAR.MC(8,1);
        QH_Design = Design_Variables.DesignValue_MaxDens.Copula_based_AND(8).MaxDens;
        QH_bivariate = Design_Variables.DesignValue_MaxDens.Copula_based_AND(8).WeightedSample;
        
    case 'FGM' % 'Farlie-Gumbel-Morgenstern' % Copula #9 % DOUBLE-CHECKED with Nelsen 2003
        Copula_pars = Copula_Variables.PAR.MC(9,1);
        QH_Design = Design_Variables.DesignValue_MaxDens.Copula_based_AND(9).MaxDens;
        QH_bivariate = Design_Variables.DesignValue_MaxDens.Copula_based_AND(9).WeightedSample;
        
    case 'Plackett' % Copula #10 % DOUBLE-CHEKCED
        Copula_pars = Copula_Variables.PAR.MC(10,1);
        QH_Design = Design_Variables.DesignValue_MaxDens.Copula_based_AND(10).MaxDens;
        QH_bivariate = Design_Variables.DesignValue_MaxDens.Copula_based_AND(10).WeightedSample;
        
    case 'Cuadras-Auge' % Copula #11 %DOUBLE-CHECKED
        Copula_pars = Copula_Variables.PAR.MC(11,1);
        QH_Design = Design_Variables.DesignValue_MaxDens.Copula_based_AND(11).MaxDens;
        QH_bivariate = Design_Variables.DesignValue_MaxDens.Copula_based_AND(11).WeightedSample;
        
    case 'Raftery' % Copula #12 %DOUBLE-CHECKED
        Copula_pars = Copula_Variables.PAR.MC(12,1);
        QH_Design = Design_Variables.DesignValue_MaxDens.Copula_based_AND(12).MaxDens;
        QH_bivariate = Design_Variables.DesignValue_MaxDens.Copula_based_AND(12).WeightedSample;
        
    case 'Shih-Louis' % Copula #13  %DOUBLE-CHECKED
        Copula_pars = Copula_Variables.PAR.MC(13,1);
        QH_Design = Design_Variables.DesignValue_MaxDens.Copula_based_AND(13).MaxDens;
        QH_bivariate = Design_Variables.DesignValue_MaxDens.Copula_based_AND(13).WeightedSample;
        
    case 'Linear-Spearman' % Copula #14 %DOUBLE-CHECKED
        Copula_pars = Copula_Variables.PAR.MC(14,1);
        QH_Design = Design_Variables.DesignValue_MaxDens.Copula_based_AND(14).MaxDens;
        QH_bivariate = Design_Variables.DesignValue_MaxDens.Copula_based_AND(14).WeightedSample;
        
    case 'Cubic' % Copula #15 %DOUBLE-CHECKED
        Copula_pars = Copula_Variables.PAR.MC(15,1);
        QH_Design = Design_Variables.DesignValue_MaxDens.Copula_based_AND(15).MaxDens;
        QH_bivariate = Design_Variables.DesignValue_MaxDens.Copula_based_AND(15).WeightedSample;
        
    case 'Burr' % Copula #16 %DOUBLE-CHECKED
        Copula_pars = Copula_Variables.PAR.MC(16,1);
        QH_Design = Design_Variables.DesignValue_MaxDens.Copula_based_AND(16).MaxDens;
        QH_bivariate = Design_Variables.DesignValue_MaxDens.Copula_based_AND(16).WeightedSample;
        
    case 'Nelsen' % Copula #17 %DOUBLE-CHECKED
        Copula_pars = Copula_Variables.PAR.MC(17,1);
        QH_Design = Design_Variables.DesignValue_MaxDens.Copula_based_AND(17).MaxDens;
        QH_bivariate = Design_Variables.DesignValue_MaxDens.Copula_based_AND(17).WeightedSample;
        
    case 'Galambos' % Copula #18  % DOUBLE-CHEKCED
        Copula_pars = Copula_Variables.PAR.MC(18,1);
        QH_Design = Design_Variables.DesignValue_MaxDens.Copula_based_AND(18).MaxDens;
        QH_bivariate = Design_Variables.DesignValue_MaxDens.Copula_based_AND(18).WeightedSample;
        
        % Two parameter copulas
    case 'Marshal-Olkin' % Copula #19 %DOUBLE-CHECKED
        Copula_pars = Copula_Variables.PAR.MC(19,1:2);
        QH_Design = Design_Variables.DesignValue_MaxDens.Copula_based_AND(19).MaxDens;
        QH_bivariate = Design_Variables.DesignValue_MaxDens.Copula_based_AND(19).WeightedSample;
        
    case 'Fischer-Hinzman' % Copula #20 %DOUBLE-CHECKED
        Copula_pars = Copula_Variables.PAR.MC(20,1:2);
        QH_Design = Design_Variables.DesignValue_MaxDens.Copula_based_AND(20).MaxDens;
        QH_bivariate = Design_Variables.DesignValue_MaxDens.Copula_based_AND(20).WeightedSample;
        
    case 'Roch-Alegre' % Copula #21 %DOUBLE-CHECKED
        Copula_pars = Copula_Variables.PAR.MC(21,1:2);
        QH_Design = Design_Variables.DesignValue_MaxDens.Copula_based_AND(21).MaxDens;
        QH_bivariate = Design_Variables.DesignValue_MaxDens.Copula_based_AND(21).WeightedSample;
        
    case 'Fischer-Kock' % Copula #22 %DOUBLE-CHECKED
        Copula_pars = Copula_Variables.PAR.MC(22,1:2);
        QH_Design = Design_Variables.DesignValue_MaxDens.Copula_based_AND(22).MaxDens;
        QH_bivariate = Design_Variables.DesignValue_MaxDens.Copula_based_AND(22).WeightedSample;
        
    case 'BB1' % Copula #23 % DOUBLE-CHEKCED
        Copula_pars = Copula_Variables.PAR.MC(23,1:2);
        QH_Design = Design_Variables.DesignValue_MaxDens.Copula_based_AND(23).MaxDens;
        QH_bivariate = Design_Variables.DesignValue_MaxDens.Copula_based_AND(23).WeightedSample;
        
    case 'BB5' % Copula #24 % DOUBLE-CHEKCED
        Copula_pars = Copula_Variables.PAR.MC(24,1:2);
        QH_Design = Design_Variables.DesignValue_MaxDens.Copula_based_AND(24).MaxDens;
        QH_bivariate = Design_Variables.DesignValue_MaxDens.Copula_based_AND(24).WeightedSample;
        
        
        % Three parameter copulas
    case 'Tawn' % Copula #25 %DOUBLE-CHECKED
        Copula_pars = Copula_Variables.PAR.MC(2,1:3);
        QH_Design = Design_Variables.DesignValue_MaxDens.Copula_based_AND(25).MaxDens;
        QH_bivariate = Design_Variables.DesignValue_MaxDens.Copula_based_AND(25).WeightedSample;
end

end