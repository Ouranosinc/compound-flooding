% This script is for plotting the results of MhAST bivariate frequency
% analysis

%% section 1: Inputs (user defined)

outlet = 'Batiscan';
serie = 'WLcondQ';
% serie = 'QcondWL';
% horizon = 'historic';
horizon = 'future';
copula_type = 'dependent';
selected_copula = 'Clayton';
DesignRP = 100;
%% Go to the directory

cd(fullfile('/exec/mbizhani',outlet,horizon,serie,'100/Results'))
load ('MhAST_Results.mat','Design_Variables')

%% 
copula = Design_Variables.DesignValue_MaxDens.Copula_based_AND(4).WeightedSample;
copula(:,3) = Design_Variables.DesignValue_MaxDens.Copula_based_AND(4).Dens;

ind = Design_Variables.DesignValue_MaxDens.Copula_based_IND(4).WeightedSample;
ind(:,3) = Design_Variables.DesignValue_MaxDens.Copula_based_IND(4).Dens;

%Maximum Density Q-H values
QH = Design_Variables.DesignValue_MaxDens.Copula_based_AND(4).MaxDens;

plot(handles.data(:,1),handles.data(:,2),'.','color',([0.502 0.502 0.502]),'markersize',15)
grid on
ZZ = zeros(size(copula(:,1)));
col = copula(:,3);  % This is the color, vary with x in this case.
surface([copula(:,1)';copula(:,1)'],[copula(:,2)';copula(:,2)'],[ZZ';ZZ'],[col';col'],...
    'facecol','no',...
    'edgecol','interp',...
    'linew',2);
colormap(jet)
% Set colorbar
cb = colorbar('location','south');
set(cb, 'xlim', [0 1]);
hold on

plot(QH(1), QH(2), 'go', 'markersize', 6, 'linewidth', 2, 'markeredgecolor', 'r', 'markerfacecolor', 'k');
hold on
%plotting the independent copula isoline
ZZ = zeros(size(ind(:,1)));
col = ind(:,3);  % This is the color, vary with x in this case.
surface([ind(:,1)';ind(:,1)'],[ind(:,2)';ind(:,2)'],[ZZ';ZZ'],[col';col'],...
    'facecol','no',...
    'edgecol','interp',...
    'linew',2);
colormap(jet)
% Set colorbar
