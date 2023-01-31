warning off
outlet = {'Au_Renard','York','Petite_Cascapedia','Ristigouche','Mitis',...
    'Matane','Outardes','Gouffre','RivSud','Saint_Charles',...
    'Montmorency','Etchemin','Chaudiere','Jacques_Cartier','Batiscan',...
    'Sainte_Anne','Becancour','Saint_Maurice','Nicolet','du_Loup',...
    'Maskinonge','Saint_Francois','Yamaska','Richelieu','Assomption','Chateauguay'};

label = {'Au Renard','York','Petite Cascapedia','Ristigouche','Mitis',...
    'Matane','Outardes','Gouffre','du Sud','Saint Charles',...
    'Montmorency','Etchemin','Chaudiere','Jacques Cartier','Batiscan',...
    'Sainte Anne','Becancour','Saint Maurice','Nicolet','du Loup',...
    'Maskinonge','Saint Francois','Yamaska','Richelieu','Assomption','Chateauguay'};

tau_WLcondQ = [-0.04,0.03,0.21,0.15,-0.08,...
    .02,0.05,0.07,-0.02,-0.07,...
    0.08,0.08,0.12,0.04,0.32,...
    0.11,0.21,0.5,0.24,0.52,...
    0.46,0.36,0.18,0.3,0.27,0.36];
tau_QcondWL = [-0.21,-0.14,-0.25,-0.31,-0.01,...
    0.003,0.07,-0.15,-0.16,-0.16,...
    -0.22,-0.06,0.01,0.02,0.27,...
    0.11,0.2,0.17,0.17,0.32,...
    0.34,0.25,0.17,0.25,0.4,23];
serie = 'WLcondQ';
% serie = 'QcondWL';
horizon = 'historic';
id = 0;
for i=1:7
    id = id +1;
    try
        cd(fullfile('U:\Dossier_travail\705300_rehaussement_marin\3- Data\Results',outlet{i},horizon,serie,'100\Results'))
        load ('MhAST_Results.mat','EP_emp')
    catch
        cd(fullfile('U:\Dossier_travail\705300_rehaussement_marin\3- Data\Results',outlet{i},horizon,serie,'\Results'))
        load ('MhAST_Results.mat','EP_emp')
    end
    
    n = size(EP_emp,1);
    for i=1:n
        r11 = find(EP_emp(:,1) < EP_emp(i,1));
        r22 = find(EP_emp(:,2) < EP_emp(i,2));
        hn(i,1) = length(intersect(r11,r22));
        r11 = 0; r22 = 0;
    end
    Hn = hn./(n-1);
    
    Wn = ((n - 1) * Hn + 1)/n;
    
    Hn_sort = (sort(Hn)).';
    
    for i=1:n
        fun = @(w) w .* (-log(w)) .* (w - w .* log(w)).^(i - 1) .* (1 - w + w .* log(w)).^(n - i);
        F = integral(fun,0,1);
        b = nchoosek(n-1,i-1);
        W_in(i)= n * b * F;
        
    end
    
    x = linspace(0,1,100);
    g = x;
    
    %Now plot!
    subplot(3,1,1)
    if id ==1
        plot(x,g,'k','LineWidth',2)
        hold on
    end

    scatter(W_in, Hn_sort,'filled')

    xlabel('W_{(1:n)}')
    ylabel('H_i')

    grid on
    set(gcf,'PaperPositionMode','auto')
    set(gcf,'color','w');
    title("Lower Estuary and Golf: WLcondQ");

    legend('Independent',[label{1} + " (\tau ="+ sprintf('%.2f',tau_WLcondQ(1)) + ")"],[label{2} + " (\tau ="+ sprintf('%.2f',tau_WLcondQ(2)) + ")"],...
        [label{3} + " (\tau ="+ sprintf('%.2f',tau_WLcondQ(3)) + ")"],[label{4} + " (\tau ="+ sprintf('%.2f',tau_WLcondQ(4)) + ")"],...
        [label{5} + " (\tau ="+ sprintf('%.2f',tau_WLcondQ(5)) + ")"],[label{6} + " (\tau ="+ sprintf('%.2f',tau_WLcondQ(6)) + ")"],...
        [label{7} + " (\tau ="+ sprintf('%.2f',tau_WLcondQ(7)) + ")"])
    clear EP_emp r11 r22 hn Hn Wn Hn_sort fun F b W_in x g aa
    
    
end

hold on
id = 0;

for i=8:16
    id = id +1;
    try
        cd(fullfile('U:\Dossier_travail\705300_rehaussement_marin\3- Data\Results',outlet{i},horizon,serie,'100\Results'))
        load ('MhAST_Results.mat','EP_emp')
    catch
        cd(fullfile('U:\Dossier_travail\705300_rehaussement_marin\3- Data\Results',outlet{i},horizon,serie,'\Results'))
        load ('MhAST_Results.mat','EP_emp')
    end
    
    n = size(EP_emp,1);
    for i=1:n
        r11 = find(EP_emp(:,1) < EP_emp(i,1));
        r22 = find(EP_emp(:,2) < EP_emp(i,2));
        hn(i,1) = length(intersect(r11,r22));
        r11 = 0; r22 = 0;
    end
    Hn = hn./(n-1);
    
    Wn = ((n - 1) * Hn + 1)/n;
    
    Hn_sort = (sort(Hn)).';
    
    for i=1:n
        fun = @(w) w .* (-log(w)) .* (w - w .* log(w)).^(i - 1) .* (1 - w + w .* log(w)).^(n - i);
        F = integral(fun,0,1);
        b = nchoosek(n-1,i-1);
        W_in(i)= n * b * F;
        
    end
    
    x = linspace(0,1,100);
    g = x;
    
    %Now plot!
    subplot(3,1,2)
    if id ==1
        plot(x,g,'k','LineWidth',2)
        hold on
    end

    scatter(W_in, Hn_sort,'filled')

    xlabel('W_{(1:n)}')
    ylabel('H_i')

    grid on
    set(gcf,'PaperPositionMode','auto')
    set(gcf,'color','w');
    title("Upper and Fluvial Estuary: WLcondQ");
%     aa = sprintf('%.2f',tau_WLcondQ(subplotid));
%     title([label{subplotid} + " (\tau ="+ aa + ")"]);
    legend('Independent',[label{8} + " (\tau ="+ sprintf('%.2f',tau_WLcondQ(8)) + ")"],[label{9} + " (\tau ="+ sprintf('%.2f',tau_WLcondQ(9)) + ")"],...
        [label{10} + " (\tau ="+ sprintf('%.2f',tau_WLcondQ(10)) + ")"],[label{11} + " (\tau ="+ sprintf('%.2f',tau_WLcondQ(11)) + ")"],...
        [label{12} + " (\tau ="+ sprintf('%.2f',tau_WLcondQ(12)) + ")"],[label{13} + " (\tau ="+ sprintf('%.2f',tau_WLcondQ(13)) + ")"],...
        [label{14} + " (\tau ="+ sprintf('%.2f',tau_WLcondQ(14)) + ")"],[label{15} + " (\tau ="+ sprintf('%.2f',tau_WLcondQ(15)) + ")"],...
        [label{16} + " (\tau ="+ sprintf('%.2f',tau_WLcondQ(16)) + ")"])
    clear EP_emp r11 r22 hn Hn Wn Hn_sort fun F b W_in x g aa
    
    
end

hold on

serie = 'WLcondQ';
id = 0;


for i=17:26
    id = id +1;
    try
        cd(fullfile('U:\Dossier_travail\705300_rehaussement_marin\3- Data\Results',outlet{i},horizon,serie,'100\Results'))
        load ('MhAST_Results.mat','EP_emp')
    catch
        cd(fullfile('U:\Dossier_travail\705300_rehaussement_marin\3- Data\Results',outlet{i},horizon,serie,'\Results'))
        load ('MhAST_Results.mat','EP_emp')
    end
    
    n = size(EP_emp,1);
    for i=1:n
        r11 = find(EP_emp(:,1) < EP_emp(i,1));
        r22 = find(EP_emp(:,2) < EP_emp(i,2));
        hn(i,1) = length(intersect(r11,r22));
        r11 = 0; r22 = 0;
    end
    Hn = hn./(n-1);
    
    Wn = ((n - 1) * Hn + 1)/n;
    
    Hn_sort = (sort(Hn)).';
    
    for i=1:n
        fun = @(w) w .* (-log(w)) .* (w - w .* log(w)).^(i - 1) .* (1 - w + w .* log(w)).^(n - i);
        F = integral(fun,0,1);
        b = nchoosek(n-1,i-1);
        W_in(i)= n * b * F;
        
    end
    
    x = linspace(0,1,100);
    g = x;
    
    %Now plot!
    subplot(3,1,3)
    if id ==1
        plot(x,g,'k','LineWidth',2)
        hold on
    end

    scatter(W_in, Hn_sort,'filled')

    xlabel('W_{(1:n)}')
    ylabel('H_i')

    grid on
    set(gcf,'PaperPositionMode','auto')
    set(gcf,'color','w');
    title("Fluvial section: WLcondQ");
%     aa = sprintf('%.2f',tau_WLcondQ(subplotid));
%     title([label{subplotid} + " (\tau ="+ aa + ")"]);
    legend('Independent',[label{17} + " (\tau ="+ sprintf('%.2f',tau_WLcondQ(17)) + ")"],[label{18} + " (\tau ="+ sprintf('%.2f',tau_WLcondQ(18)) + ")"],...
        [label{19} + " (\tau ="+ sprintf('%.2f',tau_WLcondQ(19)) + ")"],[label{20} + " (\tau ="+ sprintf('%.2f',tau_WLcondQ(20)) + ")"],...
        [label{21} + " (\tau ="+ sprintf('%.2f',tau_WLcondQ(21)) + ")"],[label{22} + " (\tau ="+ sprintf('%.2f',tau_WLcondQ(22)) + ")"],...
        [label{23} + " (\tau ="+ sprintf('%.2f',tau_WLcondQ(23)) + ")"],[label{24} + " (\tau ="+ sprintf('%.2f',tau_WLcondQ(24)) + ")"],...
        [label{25} + " (\tau ="+ sprintf('%.2f',tau_WLcondQ(25)) + ")"],[label{26} + " (\tau ="+ sprintf('%.2f',tau_WLcondQ(26)) + ")"])
    clear EP_emp r11 r22 hn Hn Wn Hn_sort fun F b W_in x g aa
    
    
end


print('K-plot_WLcondQ','-dpng','-r300')

%% Same plot, but for QcondW

% serie = 'WLcondQ';
serie = 'QcondWL';
horizon = 'historic';
id = 0;
for i=1:7
    id = id +1;
    try
        cd(fullfile('U:\Dossier_travail\705300_rehaussement_marin\3- Data\Results',outlet{i},horizon,serie,'100\Results'))
        load ('MhAST_Results.mat','EP_emp')
    catch
        cd(fullfile('U:\Dossier_travail\705300_rehaussement_marin\3- Data\Results',outlet{i},horizon,serie,'\Results'))
        load ('MhAST_Results.mat','EP_emp')
    end
    
    n = size(EP_emp,1);
    for i=1:n
        r11 = find(EP_emp(:,1) < EP_emp(i,1));
        r22 = find(EP_emp(:,2) < EP_emp(i,2));
        hn(i,1) = length(intersect(r11,r22));
        r11 = 0; r22 = 0;
    end
    Hn = hn./(n-1);
    
    Wn = ((n - 1) * Hn + 1)/n;
    
    Hn_sort = (sort(Hn)).';
    
    for i=1:n
        fun = @(w) w .* (-log(w)) .* (w - w .* log(w)).^(i - 1) .* (1 - w + w .* log(w)).^(n - i);
        F = integral(fun,0,1);
        b = nchoosek(n-1,i-1);
        W_in(i)= n * b * F;
        
    end
    
    x = linspace(0,1,100);
    g = x;
    
    %Now plot!
    subplot(3,1,1)
    if id ==1
        plot(x,g,'k','LineWidth',2)
        hold on
    end

    scatter(W_in, Hn_sort,'filled')

    xlabel('W_{(1:n)}')
    ylabel('H_i')

    grid on
    set(gcf,'PaperPositionMode','auto')
    set(gcf,'color','w');
    title("Lower Estuary and Golf: QcondWL");

    legend('Independent',[label{1} + " (\tau ="+ sprintf('%.2f',tau_QcondWL(1)) + ")"],[label{2} + " (\tau ="+ sprintf('%.2f',tau_QcondWL(2)) + ")"],...
        [label{3} + " (\tau ="+ sprintf('%.2f',tau_QcondWL(3)) + ")"],[label{4} + " (\tau ="+ sprintf('%.2f',tau_QcondWL(4)) + ")"],...
        [label{5} + " (\tau ="+ sprintf('%.2f',tau_QcondWL(5)) + ")"],[label{6} + " (\tau ="+ sprintf('%.2f',tau_QcondWL(6)) + ")"],...
        [label{7} + " (\tau ="+ sprintf('%.2f',tau_QcondWL(7)) + ")"])
    clear EP_emp r11 r22 hn Hn Wn Hn_sort fun F b W_in x g aa
    
    
end

hold on
id = 0;

for i=8:16
    id = id +1;
    try
        cd(fullfile('U:\Dossier_travail\705300_rehaussement_marin\3- Data\Results',outlet{i},horizon,serie,'100\Results'))
        load ('MhAST_Results.mat','EP_emp')
    catch
        cd(fullfile('U:\Dossier_travail\705300_rehaussement_marin\3- Data\Results',outlet{i},horizon,serie,'\Results'))
        load ('MhAST_Results.mat','EP_emp')
    end
    
    n = size(EP_emp,1);
    for i=1:n
        r11 = find(EP_emp(:,1) < EP_emp(i,1));
        r22 = find(EP_emp(:,2) < EP_emp(i,2));
        hn(i,1) = length(intersect(r11,r22));
        r11 = 0; r22 = 0;
    end
    Hn = hn./(n-1);
    
    Wn = ((n - 1) * Hn + 1)/n;
    
    Hn_sort = (sort(Hn)).';
    
    for i=1:n
        fun = @(w) w .* (-log(w)) .* (w - w .* log(w)).^(i - 1) .* (1 - w + w .* log(w)).^(n - i);
        F = integral(fun,0,1);
        b = nchoosek(n-1,i-1);
        W_in(i)= n * b * F;
        
    end
    
    x = linspace(0,1,100);
    g = x;
    
    %Now plot!
    subplot(3,1,2)
    if id ==1
        plot(x,g,'k','LineWidth',2)
        hold on
    end

    scatter(W_in, Hn_sort,'filled')

    xlabel('W_{(1:n)}')
    ylabel('H_i')

    grid on
    set(gcf,'PaperPositionMode','auto')
    set(gcf,'color','w');
    title("Upper and Fluvial Estuary: QcondWL");
%     aa = sprintf('%.2f',tau_QcondWL(subplotid));
%     title([label{subplotid} + " (\tau ="+ aa + ")"]);
    legend('Independent',[label{8} + " (\tau ="+ sprintf('%.2f',tau_QcondWL(8)) + ")"],[label{9} + " (\tau ="+ sprintf('%.2f',tau_QcondWL(9)) + ")"],...
        [label{10} + " (\tau ="+ sprintf('%.2f',tau_QcondWL(10)) + ")"],[label{11} + " (\tau ="+ sprintf('%.2f',tau_QcondWL(11)) + ")"],...
        [label{12} + " (\tau ="+ sprintf('%.2f',tau_QcondWL(12)) + ")"],[label{13} + " (\tau ="+ sprintf('%.2f',tau_QcondWL(13)) + ")"],...
        [label{14} + " (\tau ="+ sprintf('%.2f',tau_QcondWL(14)) + ")"],[label{15} + " (\tau ="+ sprintf('%.2f',tau_QcondWL(15)) + ")"],...
        [label{16} + " (\tau ="+ sprintf('%.2f',tau_QcondWL(16)) + ")"])
    clear EP_emp r11 r22 hn Hn Wn Hn_sort fun F b W_in x g aa
    
    
end

hold on

serie = 'QcondWL';
id = 0;


for i=17:26
    id = id +1;
    try
        cd(fullfile('U:\Dossier_travail\705300_rehaussement_marin\3- Data\Results',outlet{i},horizon,serie,'100\Results'))
        load ('MhAST_Results.mat','EP_emp')
    catch
        cd(fullfile('U:\Dossier_travail\705300_rehaussement_marin\3- Data\Results',outlet{i},horizon,serie,'\Results'))
        load ('MhAST_Results.mat','EP_emp')
    end
    
    n = size(EP_emp,1);
    for i=1:n
        r11 = find(EP_emp(:,1) < EP_emp(i,1));
        r22 = find(EP_emp(:,2) < EP_emp(i,2));
        hn(i,1) = length(intersect(r11,r22));
        r11 = 0; r22 = 0;
    end
    Hn = hn./(n-1);
    
    Wn = ((n - 1) * Hn + 1)/n;
    
    Hn_sort = (sort(Hn)).';
    
    for i=1:n
        fun = @(w) w .* (-log(w)) .* (w - w .* log(w)).^(i - 1) .* (1 - w + w .* log(w)).^(n - i);
        F = integral(fun,0,1);
        b = nchoosek(n-1,i-1);
        W_in(i)= n * b * F;
        
    end
    
    x = linspace(0,1,100);
    g = x;
    
    %Now plot!
    subplot(3,1,3)
    if id ==1
        plot(x,g,'k','LineWidth',2)
        hold on
    end

    scatter(W_in, Hn_sort,'filled')

    xlabel('W_{(1:n)}')
    ylabel('H_i')

    grid on
    set(gcf,'PaperPositionMode','auto')
    set(gcf,'color','w');
    title("Fluvial section: QcondWL");
%     aa = sprintf('%.2f',tau_QcondWL(subplotid));
%     title([label{subplotid} + " (\tau ="+ aa + ")"]);
    legend('Independent',[label{17} + " (\tau ="+ sprintf('%.2f',tau_QcondWL(17)) + ")"],[label{18} + " (\tau ="+ sprintf('%.2f',tau_QcondWL(18)) + ")"],...
        [label{19} + " (\tau ="+ sprintf('%.2f',tau_QcondWL(19)) + ")"],[label{20} + " (\tau ="+ sprintf('%.2f',tau_QcondWL(20)) + ")"],...
        [label{21} + " (\tau ="+ sprintf('%.2f',tau_QcondWL(21)) + ")"],[label{22} + " (\tau ="+ sprintf('%.2f',tau_QcondWL(22)) + ")"],...
        [label{23} + " (\tau ="+ sprintf('%.2f',tau_QcondWL(23)) + ")"],[label{24} + " (\tau ="+ sprintf('%.2f',tau_QcondWL(24)) + ")"],...
        [label{25} + " (\tau ="+ sprintf('%.2f',tau_QcondWL(25)) + ")"],[label{26} + " (\tau ="+ sprintf('%.2f',tau_QcondWL(26)) + ")"])
    clear EP_emp r11 r22 hn Hn Wn Hn_sort fun F b W_in x g aa
    
    
end


print('K-plot_QcondWL','-dpng','-r300')




