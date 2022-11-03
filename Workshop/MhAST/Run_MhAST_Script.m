clc; clear;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% MATLAB code developed by Mojtaba Sadegh (mojtabasadegh@gmail.com) and Amir AghaKouchak,
% Center for Hydrometeorology and Remote Sensing (CHRS)
% University of California, Irvine
%
% Last modified on December 20, 2016
%
% Please reference to:
% Sadegh, M., E. Ragno, and A. AghaKouchak (2017), MvDAT: Multivariate
% Dependence Analysis Toolbox, Water Resources Research, 53, doi:10.1002/2016WR020242.
% Link: http://onlinelibrary.wiley.com/doi/10.1002/2016WR020242/epdf
%
% Please contact Mojtaba Sadegh (mojtabasadegh@gmail.com) with any issue.
%
% Disclaimer:
% This program (hereafter, software) is designed for instructional, educational and research use only.
% Commercial use is prohibited. The software is provided 'as is' without warranty
% of any kind, either express or implied. The software could include technical or other mistakes,
% inaccuracies or typographical errors. The use of the software is done at your own discretion and
% risk and with agreement that you will be solely responsible for any damage and that the authors
% and their affiliate institutions accept no responsibility for errors or omissions in the software
% or documentation. In no event shall the authors or their affiliate institutions be liable to you or
% any third parties for any special, indirect or consequential damages of any kind, or any damages whatsoever.
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% User Input
% Data file name
datafile = 'WLcondQ.txt';
handles.title = 'WLcondQ';
% handles.title = 'QcondWL';

% Sampling frequency (how many samples per year?)
handles.SF = 1;
% Design Return Period
handles.DesignRP = 100;
% Number of weighted samples on the design return period curve
handles.WeightedSampleSize = 2000;
% Uncertainty requested?
handles.DesignUnc = 0;
% Name of the variables
handles.U1_name = 'Discharge (m^3/s)';
handles.U2_name = 'Water level (m)';

% Local optimization or Global
handles.Optimization = 'MCMC'; % Local: local optimization; MCMC: both local & global optimization

% Which Copulas to run? Select any combination
% 1: Gaussian, 2: t, 3: Clayton, 4: Frank, 5: Gumbel, 6: Independence, 7: Ali-Mikhail-Haq (AMH), 8: Joe
% 9: Farlie-Gumbel-Morgenstern (FGM), 10: Gumbel-Barnet, 11: Plackett, 12: Cuadras-Auge, 13: Raftery
% 14: Shih-Louis, 15: Linear-Spearman, 16: Cubic, 17: Burr, 18: Nelson, 19: Galambos, 20: Marshal-Olkin
% 21: Fischer-Hinzmann, 22: Roch-Alegre, 23: Fischer-Kock, 24: BB1, 25: BB5, 26: Tawn
handles.ID_CHOSEN = [6];
% handles.ID_CHOSEN = [1:25];

% Calculate pvalues or not? 0: no pvalue; 1: pvalue for the best copula
% selected according to BIC; 2: pvalue for all chosen copulas
handles.pvalue = 2;

handles.Kendall=0;
handles.empiricalcopula = 0; % 1 = add the empirical copula plot to the return periods or 0 (not)
%% Run MhAST
% Load data
if ismac
    addpath([pwd,'/Data'])
elseif ispc
    addpath([pwd,'\Data'])
elseif isunix
    addpath([pwd,'/Data'])
end

try
    handles.data = xlsread(datafile);
catch
    handles.data = load(datafile);
end

% Conversion from IGLD85 --> CGVD28
handles.data(:,2) = handles.data(:,2) + 0.01;

% Run main MvCAT function
[ID_ML,ID_AIC,ID_BIC,Family] = MhAST_main(handles);

