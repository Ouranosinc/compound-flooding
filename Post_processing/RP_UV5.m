
function [RP_V1_percentileNames,RP_V1] = RP_UV5(npar,data,variable,serie,handles,par,PD_U1,PD_U2)

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