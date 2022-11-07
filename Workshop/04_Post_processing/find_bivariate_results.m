
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
    case 'Independence' % Copula #6         
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


