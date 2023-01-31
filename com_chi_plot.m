warning off
clear all
outlet = {'Batiscan','Becancour','Saint_Maurice','Nicolet','du_Loup',...
    'Maskinonge','Saint_Francois','Yamaska','Richelieu','Assomption','Chateauguay'};

label = {'Batiscan','Becancour','Saint Maurice','Nicolet','du Loup',...
    'Maskinonge','Saint Francois','Yamaska','Richelieu','Assomption','Chateauguay'};

% serie = 'WLcondQ';
serie = 'QcondWL';
horizon = 'historic';
id=0;
for i=1:11
    id = id+1;
    try
        cd(fullfile('U:\Dossier_travail\705300_rehaussement_marin\3- Data\Results',outlet{i},horizon,serie,'100\Results'))
        load ('MhAST_Results.mat','U1','U2','EP_emp')
    catch
        cd(fullfile('U:\Dossier_travail\705300_rehaussement_marin\3- Data\Results',outlet{i},horizon,serie,'\Results'))
        load ('MhAST_Results.mat','U1','U2','EP_emp')
    end
    
    n = size(EP_emp,1);
    for i=1:n
        r11 = find(EP_emp(:,1) < EP_emp(i,1));
        r22 = find(EP_emp(:,2) < EP_emp(i,2));
        hn(i,1) = length(intersect(r11,r22));
        r11 = 0; r22 = 0;
    end
    Hn = hn./(n-1);
    
    F=0;
    G=0;
    
    % Find data ranks
    for i = 1:n
        F(i,1) = sum(U1(:,1) <= U1(i,1));
        G(i,1) = sum(U2(:,1) <= U2(i,1));
    end
    FF = (F-1)./(n-1);
    GG = (G-1)./(n-1);
    
    dd(1:n,1) = (FF-0.5).^2;
    dd(:,2) = (GG-0.5).^2;
    ddd = max(dd,[],2);
    
    for i=1:n
        lambda(i,1) = 4 * sign((FF(i,1) - 0.5) * (GG(i,1) - 0.5)) * ddd(i,1);
    end
    
    bounds = [-1.78/sqrt(n), 1.78/sqrt(n)];
    
    
    mU1 = mean(U1);
    mU2 = mean(U2);
    
    r11=0; r22=0;
    
    r11 = find(U1(:,1) > mU1);
    r22 = find(U2(:,1) > mU2);
    r33 = intersect(r11,r22);
    r44 = find(lambda>0);
    r55 = intersect(r33, r44);
    
    lambda_up = lambda(r55);
    FF_up = FF(r55);
    GG_up = GG(r55);
    Hn_up = Hn(r55);
    
    chi_up = (Hn_up - (FF_up .* GG_up))./sqrt(FF_up .* (1 - FF_up) .* GG_up .* (1 - GG_up));
    
    xx = linspace(-1,1,100);
    
    gg = zeros(size(xx));
    
    hh = bounds(1,1)* ones(size(xx));
    ii = bounds(1,2)* ones(size(xx));
    
    subplot(4,3,id)
    scatter(lambda_up, chi_up,20,'b')
    if id==1
        xlabel('\lambda')
        ylabel('\chi')
    end
    
    % hold on
    % scatter(lambda_low, chi_low,'r')
    hold on
    plot(gg,xx, '--','Color', 'k')
    xlim([-1 1])
    ylim([-1 1])
    hold on
    plot(xx,hh, '--','Color', 'k')
    hold on
    plot(xx,ii, '--','Color', 'k')

    set(gcf,'color','w');
    box on

%     grid on
    set(gcf,'PaperPositionMode','auto')
    title(label{id});
    clearvars -except outlet id horizon serie label
    
    
end

print('Chi-plot_QcondWL','-dpng','-r300')