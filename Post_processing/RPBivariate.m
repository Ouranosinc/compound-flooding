

function [QH_bivariate,QH_Design,Copula_pars,desvarnames] = RPBivariate(pth_base,outlet,copula_type,selected_copula,Design_Variables,serie,horizon,data,handles,Copula_Variables)
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
    f = fullfile(pth_base,outlet,horizon,serie,'\2\Results\MhAST_Results.mat');
    load(f,'Copula_Variables','Design_Variables')
    
    desvarnames = {'Q','H'};
    [Copula_pars,QH_Design,QH_bivariate] = find_bivariate_results(selected_copula,Copula_Variables,Design_Variables);
    RP2.desvarnames = desvarnames;
    RP2.Copula_pars = Copula_pars;
    RP2.selected_copula = selected_copula;
    RP2.QH_Design = QH_Design;
    RP2.QH_bivariate_all = QH_bivariate;
    
    % now for RP350
    f = fullfile(pth_base,outlet,horizon,serie,'\350\Results\MhAST_Results.mat');
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
    RP2.QH_Design = QH_Design;

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
    RP100.QH_Design = QH_Design;
        
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
    RP350.QH_Design = QH_Design;
%     end
QH_Design = struct('RP2',RP2,'RP100',RP100,'RP350',RP350);
Copula_pars = 'NaN';

    
end
end