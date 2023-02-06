% This script is for plotting the results of MhAST bivariate frequency
% analysis

% %% section 1: Inputs (user defined)
% 
% outlet = 'Batiscan';
% serie = 'WLcondQ';
% % serie = 'QcondWL';
% horizon = 'historic';
% % horizon = 'future';
% copula_type = 'dependent';
% selected_copula = 'Clayton';
% DesignRP = 100;
% %% Go to the directory
% 
% cd(fullfile('/exec/mbizhani',outlet,horizon,serie,'100/Results'))
% load ('MhAST_Results.mat','Design_Variables')
% 
% %% 
% copula = Design_Variables.DesignValue_MaxDens.Copula_based_AND(4).WeightedSample;
% copula(:,3) = Design_Variables.DesignValue_MaxDens.Copula_based_AND(4).Dens;
% 
% ind = Design_Variables.DesignValue_MaxDens.Copula_based_IND(4).WeightedSample;
% ind(:,3) = Design_Variables.DesignValue_MaxDens.Copula_based_IND(4).Dens;
% 
% %Maximum Density Q-H values
% QH = Design_Variables.DesignValue_MaxDens.Copula_based_AND(4).MaxDens;
% 
% plot(handles.data(:,1),handles.data(:,2),'.','color',([0.502 0.502 0.502]),'markersize',15)
% grid on
% ZZ = zeros(size(copula(:,1)));
% col = copula(:,3);  % This is the color, vary with x in this case.
% surface([copula(:,1)';copula(:,1)'],[copula(:,2)';copula(:,2)'],[ZZ';ZZ'],[col';col'],...
%     'facecol','no',...
%     'edgecol','interp',...
%     'linew',2);
% colormap(jet)
% % Set colorbar
% cb = colorbar('location','south');
% set(cb, 'xlim', [0 1]);
% hold on
% 
% plot(QH(1), QH(2), 'go', 'markersize', 6, 'linewidth', 2, 'markeredgecolor', 'r', 'markerfacecolor', 'k');
% hold on
% %plotting the independent copula isoline
% ZZ = zeros(size(ind(:,1)));
% col = ind(:,3);  % This is the color, vary with x in this case.
% surface([ind(:,1)';ind(:,1)'],[ind(:,2)';ind(:,2)'],[ZZ';ZZ'],[col';col'],...
%     'facecol','no',...
%     'edgecol','interp',...
%     'linew',2);
% colormap(jet)
% % Set colorbar

%% Plot the historic comparison of dependent vs independent copula for river outlets
% 
% get(gcf,'Position')
figure('Position',[-1409   47   1125   916]);
for i=1:11
    Family = {'Gaussian','t','Clayton','Frank','Gumbel','Independence','AMH','Joe','FGM',...
    'Plackett','Cuadras-Auge','Raftery','Shih-Louis','Linear-Spearman','Cubic','Burr','Nelsen','Galambos','Marshal-Olkin',...
    'Fischer-Hinzmann','Roch-Alegre','Fischer-Kock','BB1','BB5','Tawn'};

%     outlet = {'Batiscan','Becancour','Saint_Maurice','Nicolet','du_Loup','Maskinonge','Saint_Francois','Yamaska','Richelieu','Assomption','Chateauguay','Moulin'};
%     labels = {'Batiscan','Becancour','Saint Maurice','Nicolet','du Loup','Maskinonge','Saint Francois','Yamaska','Richelieu','Assomption','Chateauguay','Moulin'};
    
    outlet = {'Batiscan','Becancour','Saint_Maurice','Nicolet','du_Loup','Maskinonge','Saint_Francois','Yamaska','Richelieu','Assomption','Chateauguay'};
    labels = {'Batiscan','Becancour','Saint Maurice','Nicolet','du Loup','Maskinonge','Saint Francois','Yamaska','Richelieu','Assomption','Chateauguay'};
    
    copula_type = [3,18,18,18,23,23,23,18,18,1,4];
    tau =[0.32,0.21,0.5,0.24,0.52,0.46,0.36,0.18,0.3,0.27,0.36];
    
    horizon = 'historic';
    serie = 'WLcondQ';
    cd(fullfile('U:\Dossier_travail\705300_rehaussement_marin\3- Data\Results',outlet{i},horizon,serie,'100\Results'))
    load ('MhAST_Results.mat')
    copula = Design_Variables.DesignValue_MaxDens.Copula_based_AND(copula_type(i)).WeightedSample;
    copula(:,3) = Design_Variables.DesignValue_MaxDens.Copula_based_AND(copula_type(i)).Dens;
    
    ind = Design_Variables.DesignValue_MaxDens.Copula_based_IND(copula_type(i)).WeightedSample;
    ind(:,3) = Design_Variables.DesignValue_MaxDens.Copula_based_IND(copula_type(i)).Dens;
    
    %Maximum Density Q-H values
    QH = Design_Variables.DesignValue_MaxDens.Copula_based_AND(copula_type(i)).MaxDens;
    X_Axis = [min(ind(:,1)) 1.1*max(ind(:,1))];
    Y_Axis = [min(ind(:,2)) 1.1*max(ind(:,2))];
    subplot(4,3,i)
    set(gcf,'color','w');
    ZZ = zeros(size(ind(:,1)));
    col = ind(:,3);  % This is the color, vary with x in this case.
    surface([ind(:,1)';ind(:,1)'],[ind(:,2)';ind(:,2)'],[ZZ';ZZ'],[col';col'],...
        'facecol','no',...
        'edgecol','interp',...
        'linew',2);
    colormap(jet)
    aa = sprintf('%.2f',tau(i));
    title([labels{i} + ":" + (Family(copula_type(i)))]);
    axis([X_Axis Y_Axis])
    rr = Design_Variables.DesignValue_MaxDens.DesignRP_ind(copula_type(i));
    text(1.02*X_Axis(2),1.02*Y_Axis(1),num2str(rr),'Color','b','FontSize',10,'fontweight','bold')
    text(0.8*X_Axis(2),0.98*Y_Axis(2), " \tau ="+ aa + "", 'Horiz','left', 'Vert','top')
    hold on
    scatter(handles.data(:,1),handles.data(:,2),'MarkerFaceColor', [0.8275    0.8275    0.8275], 'MarkerEdgeColor',[0.8275    0.8275    0.8275])
    grid on
    ZZ = zeros(size(copula(:,1)));
    col = copula(:,3);  % This is the color, vary with x in this case.
    surface([copula(:,1)';copula(:,1)'],[copula(:,2)';copula(:,2)'],[ZZ';ZZ'],[col';col'],...
        'facecol','no',...
        'edgecol','interp',...
        'linew',2);
    colormap(jet)

    if i==11
        cb = colorbar('location','south');
        set(cb, 'xlim', [0 1]);
        cb.Label.String = 'Probability Density';
        cb.Label.FontSize = 10;
        X_Axis = [min(ind(:,1)) 1.1*max(ind(:,1))];
        Y_Axis = [min(ind(:,2)) 1.1*max(ind(:,2))];
        
    end
    if i==1
        xlabel('Streamflow (m^3/s)');
        ylabel('Water Level (m)');
    end
    
    % Set colorbar

    hold on
    box off
    
    plot(QH(1), QH(2), 'go', 'markersize', 6, 'linewidth', 2, 'markeredgecolor', 'r', 'markerfacecolor', 'k');
    hold on
    %plotting the independent copula isoline
 
%     legend(' ','Sim.')
    
    clear all;
    
end

print('Figure_hist_WLcondQ_2','-dpng','-r300')

%% plot for QcondWL

figure1=figure('Position',[-1409   47   1125   916],'visible','on');
for i=1:12
    Family = {'Gaussian','t','Clayton','Frank','Gumbel','Independence','AMH','Joe','FGM',...
    'Plackett','Cuadras-Auge','Raftery','Shih-Louis','Linear-Spearman','Cubic','Burr','Nelsen','Galambos','Marshal-Olkin',...
    'Fischer-Hinzmann','Roch-Alegre','Fischer-Kock','BB1','BB5','Tawn'};

    outlet = {'Batiscan','Becancour','Saint_Maurice','Nicolet','du_Loup','Maskinonge','Saint_Francois','Yamaska','Richelieu','Assomption','Chateauguay','Moulin'};
    labels = {'Batiscan','Becancour','Saint Maurice','Nicolet','du Loup','Maskinonge','Saint Francois','Yamaska','Richelieu','Assomption','Chateauguay','Moulin'};
    copula_type = [4,1,23,18,4,4,7,8,8,4,3,6];
    tau =[0.27,0.2,0.17,0.17,0.32,0.34,0.25,0.17,0.25,0.4,0.23,0.07];
    
    horizon = 'historic';
    serie = 'QcondWL';
    cd(fullfile('U:\Dossier_travail\705300_rehaussement_marin\3- Data\Results',outlet{i},horizon,serie,'100\Results'))
    load ('MhAST_Results.mat')
    copula = Design_Variables.DesignValue_MaxDens.Copula_based_AND(copula_type(i)).WeightedSample;
    copula(:,3) = Design_Variables.DesignValue_MaxDens.Copula_based_AND(copula_type(i)).Dens;
    
    ind = Design_Variables.DesignValue_MaxDens.Copula_based_IND(copula_type(i)).WeightedSample;
    ind(:,3) = Design_Variables.DesignValue_MaxDens.Copula_based_IND(copula_type(i)).Dens;
    
    %Maximum Density Q-H values
    QH = Design_Variables.DesignValue_MaxDens.Copula_based_AND(copula_type(i)).MaxDens;
    X_Axis = [min(handles.data(:,1)) 1.1*max(handles.data(:,1))];
    Y_Axis = [min(handles.data(:,2)) 1.1*max(handles.data(:,2))];
    subplot(3,4,i)
    set(gcf,'color','w');
    scatter(handles.data(:,1),handles.data(:,2),'MarkerFaceColor', [0.8275    0.8275    0.8275], 'MarkerEdgeColor',[0.8275    0.8275    0.8275])
    grid on
    %plotting the independent copula isoline
    ZZ = zeros(size(ind(:,1)));
    col = ind(:,3);  % This is the color, vary with x in this case.
    surface([ind(:,1)';ind(:,1)'],[ind(:,2)';ind(:,2)'],[ZZ';ZZ'],[col';col'],...
        'facecol','no',...
        'edgecol','interp',...
        'linew',2);
    colormap(jet)
    aa = sprintf('%.2f',tau(i));
    title([labels{i} + ":" + (Family(copula_type(i)))]);
    axis([X_Axis Y_Axis])
    rr = Design_Variables.DesignValue_MaxDens.DesignRP_ind(copula_type(i));
    text(1.02*X_Axis(2),1.02*Y_Axis(1),num2str(rr),'Color','red','FontSize',10,'fontweight','bold')
    text(0.8*X_Axis(2),0.98*Y_Axis(2), " \tau ="+ aa + "", 'Horiz','left', 'Vert','top')
    hold on
    ZZ = zeros(size(copula(:,1)));
    col = copula(:,3);  % This is the color, vary with x in this case.
    surface([copula(:,1)';copula(:,1)'],[copula(:,2)';copula(:,2)'],[ZZ';ZZ'],[col';col'],...
        'facecol','no',...
        'edgecol','interp',...
        'linew',2);
    colormap(jet)
    if i==11
        cb = colorbar('location','south');
        set(cb, 'xlim', [0 1]);
        cb.Label.String = 'Probability Density';
        cb.Label.FontSize = 10;
        X_Axis = [min(handles.data(:,1)) max(handles.data(:,1))];
        Y_Axis = [min(handles.data(:,2)) max(handles.data(:,2))];
        
    end
    if i==1
        xlabel('Streamflow (m^3/s)');
        ylabel('Water Level (m)');
    end
    
    % Set colorbar
    box off
    
%     if copula_type(i)~=6
    plot(QH(1), QH(2), 'go', 'markersize', 6, 'linewidth', 2, 'markeredgecolor', 'r', 'markerfacecolor', 'k');

%     end
    clear all;
    
end

print('Figure_hist_QcondWL_2','-dpng','-r300')

%% plot the comparison of design values for the historic and future: serie WLcondQ



figure1=figure('Position',[-1409   47   1125   916],'visible','on');
for i=1:10
    serie = 'WLcondQ';
    subplot(3,4,i)
    Family = {'Gaussian','t','Clayton','Frank','Gumbel','Independence','AMH','Joe','FGM',...
        'Plackett','Cuadras-Auge','Raftery','Shih-Louis','Linear-Spearman','Cubic','Burr','Nelsen','Galambos','Marshal-Olkin',...
        'Fischer-Hinzmann','Roch-Alegre','Fischer-Kock','BB1','BB5','Tawn'};
    
    outlet = {'Batiscan','Becancour','Saint_Maurice','Nicolet','du_Loup','Maskinonge','Saint_Francois','Yamaska','Richelieu','Assomption'};
    labels = {'Batiscan','Becancour','Saint Maurice','Nicolet','du Loup','Maskinonge','Saint Francois','Yamaska','Richelieu','Assomption'};
    copula_type = [3,18,18,18,2,23,23,18,8,1];
    
    
    %Maximum Density Q-H values
    cd(fullfile('U:\Dossier_travail\705300_rehaussement_marin\3- Data\Results',outlet{i},'future',serie,'100\Results'))
    load ('MhAST_Results.mat')
    
    X_Axis = [min(handles.data(:,1)) 1.1*max(handles.data(:,1))];
    Y_Axis = [min(handles.data(:,2)) 1.1*max(handles.data(:,2))];
    set(gcf,'color','w');
    scatter(handles.data(:,1),handles.data(:,2),'MarkerFaceColor', [0.8275    0.8275    0.8275], 'MarkerEdgeColor',[0.8275    0.8275    0.8275])
    grid on
    P = [2,5,10,20,50,100];
    for j=1:6

        Dens = ReturnPeriod.AND{1,copula_type(i)}(j).Dens;
        QH_rp = ReturnPeriod.AND{1,copula_type(i)}(j).MaxDens;
        QH_data = ReturnPeriod.AND{1,copula_type(i)}(j).WeightedSample;
    

        ZZ = zeros(size(QH_data(:,1)));
        col = Dens; % This is the color, vary with x in this case.
        surface([QH_data(:,1)';QH_data(:,1)'],[QH_data(:,2)';QH_data(:,2)'],[ZZ';ZZ'],[col';col'],...
            'facecol','no',...
            'edgecol','interp',...
            'linew',2);
%         colormap(viridis)
        title([labels{i} + ":" + (Family(copula_type(i)))]);
        axis([X_Axis Y_Axis])
        if i==11
            cb = colorbar('location','south');
            set(cb, 'xlim', [0 1]);
            cb.Label.String = 'Probability Density';
            cb.Label.FontSize = 10;
        end
        text(1.02*X_Axis(1),max(QH_data(:,2))*1.02,num2str(P(j)),'Color','red','FontSize',12,'fontweight','bold')
        if i==1
            xlabel('Streamflow (m^3/s)');
            ylabel('Water Level (m)');
        end
    
        % Set colorbar
        
        hold on
        box off
    
        
        plot(QH_rp(1), QH_rp(2), 'go', 'markersize', 6, 'linewidth', 2, 'markeredgecolor', 'm', 'markerfacecolor', 'm');
        hold on
        %plotting the historic QH data
        if j==6
            % add historic QH with maximum density
            serie = 'WLcondQ';
            cd(fullfile('U:\Dossier_travail\705300_rehaussement_marin\3- Data\Results',outlet{i},'historic',serie,'100\Results'))
            load ('MhAST_Results.mat')
            QH = Design_Variables.DesignValue_MaxDens.Copula_based_AND(copula_type(i)).MaxDens;
            plot(QH(1), QH(2), '-p', 'markersize', 6, 'linewidth', 2, 'markeredgecolor', 'k', 'markerfacecolor', 'k');
            hold on
        end

    end
    clear all
    
end

print('Figure_future_comparison_WLcondQ','-dpng','-r300')
%% plot the comparison of design values for the historic and future: serie QcondWL



figure1=figure('Position',[-1409   47   1125   916],'visible','on');
for i=1:10
    serie = 'QcondWL';
    subplot(3,4,i)
    Family = {'Gaussian','t','Clayton','Frank','Gumbel','Independence','AMH','Joe','FGM',...
        'Plackett','Cuadras-Auge','Raftery','Shih-Louis','Linear-Spearman','Cubic','Burr','Nelsen','Galambos','Marshal-Olkin',...
        'Fischer-Hinzmann','Roch-Alegre','Fischer-Kock','BB1','BB5','Tawn'};
    
    outlet = {'Batiscan','Becancour','Saint_Maurice','Nicolet','du_Loup','Maskinonge','Saint_Francois','Yamaska','Richelieu','Assomption'};
    labels = {'Batiscan','Becancour','Saint Maurice','Nicolet','du Loup','Maskinonge','Saint Francois','Yamaska','Richelieu','Assomption'};
    copula_type = [4,1,23,18,4,4,7,8,8,4,3,6];
    
    
    %Maximum Density Q-H values
    cd(fullfile('U:\Dossier_travail\705300_rehaussement_marin\3- Data\Results',outlet{i},'future',serie,'100\Results'))
    load ('MhAST_Results.mat')
    
    X_Axis = [min(handles.data(:,1)) 1.1*max(handles.data(:,1))];
    Y_Axis = [min(handles.data(:,2)) 1.1*max(handles.data(:,2))];
    set(gcf,'color','w');
    scatter(handles.data(:,1),handles.data(:,2),'MarkerFaceColor', [0.8275    0.8275    0.8275], 'MarkerEdgeColor',[0.8275    0.8275    0.8275])
    grid on
    P = [2,5,10,20,50,100];
    for j=1:6

        Dens = ReturnPeriod.AND{1,copula_type(i)}(j).Dens;
        QH_rp = ReturnPeriod.AND{1,copula_type(i)}(j).MaxDens;
        QH_data = ReturnPeriod.AND{1,copula_type(i)}(j).WeightedSample;
    

        ZZ = zeros(size(QH_data(:,1)));
        col = Dens; % This is the color, vary with x in this case.
        surface([QH_data(:,1)';QH_data(:,1)'],[QH_data(:,2)';QH_data(:,2)'],[ZZ';ZZ'],[col';col'],...
            'facecol','no',...
            'edgecol','interp',...
            'linew',2);
        colormap(jet)
        title([labels{i} + ":" + (Family(copula_type(i)))]);
        axis([X_Axis Y_Axis])
        if i==11
            cb = colorbar('location','south');
            set(cb, 'xlim', [0 1]);
            cb.Label.String = 'Probability Density';
            cb.Label.FontSize = 10;
        end
        text(1.02*X_Axis(1),max(QH_data(:,2))*1.02,num2str(P(j)),'Color','red','FontSize',12,'fontweight','bold')
        if i==1
            xlabel('Streamflow (m^3/s)');
            ylabel('Water Level (m)');
        end
    
        % Set colorbar
        
        hold on
        box off
    
        
        plot(QH_rp(1), QH_rp(2), 'go', 'markersize', 6, 'linewidth', 2, 'markeredgecolor', 'm', 'markerfacecolor', 'm');
        hold on
        %plotting the historic QH data
        if j==6
            % add historic QH with maximum density
            serie = 'QcondWL';
            cd(fullfile('U:\Dossier_travail\705300_rehaussement_marin\3- Data\Results',outlet{i},'historic',serie,'100\Results'))
            load ('MhAST_Results.mat')
            QH = Design_Variables.DesignValue_MaxDens.Copula_based_AND(copula_type(i)).MaxDens;
            plot(QH(1), QH(2), '-p', 'markersize', 6, 'linewidth', 2, 'markeredgecolor', 'k', 'markerfacecolor', 'k');
            hold on
        end

    end
    clear all
    
end

print('Figure_future_comparison_QcondWL','-dpng','-r300')




%% plot the future versus historic Q-H for riviere du Moulin

Family = {'Gaussian','t','Clayton','Frank','Gumbel','Independence','AMH','Joe','FGM',...
    'Plackett','Cuadras-Auge','Raftery','Shih-Louis','Linear-Spearman','Cubic','Burr','Nelsen','Galambos','Marshal-Olkin',...
    'Fischer-Hinzmann','Roch-Alegre','Fischer-Kock','BB1','BB5','Tawn'};

outlet = {'Batiscan','Becancour','Saint_Maurice','Nicolet','du_Loup','Maskinonge','Saint_Francois','Yamaska','Richelieu','Assomption','Chateauguay'};
labels = {'Batiscan','Becancour','Saint Maurice','Nicolet','du Loup','Maskinonge','Saint Francois','Yamaska','Richelieu','Assomption','Chateauguay'};


figure('Position',[-1409   620   784   343]);

for i=1:2
%     serie = 'QcondWL';
    subplot(1,2,i)
    Family = {'Gaussian','t','Clayton','Frank','Gumbel','Independence','AMH','Joe','FGM',...
        'Plackett','Cuadras-Auge','Raftery','Shih-Louis','Linear-Spearman','Cubic','Burr','Nelsen','Galambos','Marshal-Olkin',...
        'Fischer-Hinzmann','Roch-Alegre','Fischer-Kock','BB1','BB5','Tawn'};
    
%     outlet = {'Batiscan','Becancour','Saint_Maurice','Nicolet','du_Loup','Maskinonge','Saint_Francois','Yamaska','Richelieu','Assomption'};
    labels = {'WL_{cond}Q','Q_{cond}WL','Interpreter','tex'};
    copula_type = [6,6];
    fnames_future = {'U:\Dossier_travail\705300_rehaussement_marin\3- Data\Results\Au_Renard\future\WLcondQ\Results\future_WLcondQ_Au_Renard.mat',...
        'U:\Dossier_travail\705300_rehaussement_marin\3- Data\Results\Au_Renard\future\QcondWL\Results\future_QcondWL_Au_Renard.mat'};
    
    fnames_historic = {'U:\Dossier_travail\705300_rehaussement_marin\3- Data\Results\Au_Renard\historic\WLcondQ\Results\historic_WLcondQ_Au_Renard.mat',...
        'U:\Dossier_travail\705300_rehaussement_marin\3- Data\Results\Au_Renard\historic\QcondWL\Results\historic_QcondWL_Au_Renard.mat'};
    
    pth = {'U:\Dossier_travail\705300_rehaussement_marin\3- Data\Results\Au_Renard\future\WLcondQ\Results\MhAST_Results.mat',...
       'U:\Dossier_travail\705300_rehaussement_marin\3- Data\Results\Au_Renard\future\QcondWL\Results\MhAST_Results.mat'}; 
    
    %Maximum Density Q-H values
%     cd(fullfile('U:\Dossier_travail\705300_rehaussement_marin\5- Rapports\Livrable_2',outlet{i},'future',serie,'100\Results'))
    load (fnames_future{i})
    load (fnames_historic{i})
    load(pth{i})
    
    X_Axis = [min(handles.data(:,1)) 1.1*max(handles.data(:,1))];
    Y_Axis = [min(handles.data(:,2)) 1.1*max(handles.data(:,2))];
    set(gcf,'color','w');
    scatter(handles.data(:,1),handles.data(:,2),'MarkerFaceColor', [0.8275    0.8275    0.8275], 'MarkerEdgeColor',[0.8275    0.8275    0.8275])
    grid on
    P = [2,5,10,20,50,100];
    for j=1:6

        Dens = ReturnPeriod.AND{1,copula_type(i)}(j).Dens;
        QH_rp = ReturnPeriod.AND{1,copula_type(i)}(j).MaxDens;
        QH_data = ReturnPeriod.AND{1,copula_type(i)}(j).WeightedSample;
    

        ZZ = zeros(size(QH_data(:,1)));
        col = Dens; % This is the color, vary with x in this case.
        surface([QH_data(:,1)';QH_data(:,1)'],[QH_data(:,2)';QH_data(:,2)'],[ZZ';ZZ'],[col';col'],...
            'facecol','no',...
            'edgecol','interp',...
            'linew',2);
        colormap(jet)
%         title([labels{i} + ":" + (Family(copula_type(i)))]);
        title('au Renard');
%         title([labels{i}]);
        axis([X_Axis Y_Axis])
        text(1.02*X_Axis(1),max(QH_data(:,2))*1.02,num2str(P(j)),'Color','red','FontSize',12,'fontweight','bold')

        xlabel('Débit (m^3/s)');
        ylabel('Niveau d''eau (m)');

    
        % Set colorbar
        
        hold on
        box off

        %plotting the historic QH data
        if j==6

            QH(1:7,1) = [historic.Bivariate.DesVarValues.RP100.QH_Design(1,1),historic.Bivariate.DesVarValues.RP100.QH_Design(1,3),historic.Bivariate.DesVarValues.RP100.QH_Design(1,5),...
                historic.Bivariate.DesVarValues.RP100.QH_Design(1,7),historic.Bivariate.DesVarValues.RP100.QH_Design(1,9),...
                historic.Bivariate.DesVarValues.RP100.QH_Design(1,11),historic.Bivariate.DesVarValues.RP100.QH_Design(1,13)];
            
            QH(1:7,2) = [historic.Bivariate.DesVarValues.RP100.QH_Design(1,2),historic.Bivariate.DesVarValues.RP100.QH_Design(1,4),...
                historic.Bivariate.DesVarValues.RP100.QH_Design(1,6),historic.Bivariate.DesVarValues.RP100.QH_Design(1,8),...
                historic.Bivariate.DesVarValues.RP100.QH_Design(1,10),historic.Bivariate.DesVarValues.RP100.QH_Design(1,12),historic.Bivariate.DesVarValues.RP100.QH_Design(1,14)];
            
            scatter(QH(:,1), QH(:,2),  'markeredgecolor', 'k', 'markerfacecolor', 'k');
            hold on
            
            
            QH_future(1:7,1) = [future.Bivariate.DesVarValues.RP100.QH_Design(1,1),future.Bivariate.DesVarValues.RP100.QH_Design(1,3),future.Bivariate.DesVarValues.RP100.QH_Design(1,5),...
                future.Bivariate.DesVarValues.RP100.QH_Design(1,7),future.Bivariate.DesVarValues.RP100.QH_Design(1,9),...
                future.Bivariate.DesVarValues.RP100.QH_Design(1,11),future.Bivariate.DesVarValues.RP100.QH_Design(1,13)];
            
            QH_future(1:7,2) = [future.Bivariate.DesVarValues.RP100.QH_Design(1,2),future.Bivariate.DesVarValues.RP100.QH_Design(1,4),...
                future.Bivariate.DesVarValues.RP100.QH_Design(1,6),future.Bivariate.DesVarValues.RP100.QH_Design(1,8),...
                future.Bivariate.DesVarValues.RP100.QH_Design(1,10),future.Bivariate.DesVarValues.RP100.QH_Design(1,12),future.Bivariate.DesVarValues.RP100.QH_Design(1,14)];
            
            scatter(QH_future(:,1), QH_future(:,2),  'markeredgecolor', 'm', 'markerfacecolor', 'm');
            hold on
            
            
        end

    end
    clear all
    
end

% print('Figure_future_comparison_Moulin','-dpng','-r300')






