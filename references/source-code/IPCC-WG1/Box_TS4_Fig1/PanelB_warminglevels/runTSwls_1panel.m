% 2021-03-02 21:46:47 -0500
fontsize=15;

GSATwl=[1.5 2.0 3.0 4.0 5.0];

GMSLwl2050=[
    0.16 0.19 0.24
    0.17 0.20 0.26
    0.18 0.21 0.27
    0.19 0.22 0.28
    0.22 0.25 0.32
    ];
GMSLwl=[
    0.34 0.44 0.59
    0.40 0.51 0.69
    0.50 0.62 0.81
    0.58 0.70 0.91
    0.68 0.81 1.05
    ];
GMSLLC=[
    0.33 0.45 0.80
    0.63 0.88 1.61];
GMSLLC90=[
    0.26 0.45 1.09
    0.54 0.88 2.28];

        
GMSLcom2000=[
    2 3
    2 6
    4 10
    12 16
    19 22
];

GMSLcom10000=[
    6 7
    8 13
    10 24
    19 33
    28 37
];

colrs=[
    159 0 159
    0 159 0
    0 159 159
    124 130 130
]/255;

Paleo.label={'EECO',sprintf('Mid-Pliocene\nWarm Period'),sprintf('Last\nInterglacial'),''};
Paleo.T=[15 3.25 1.0 0.1];
Paleo.Tsd=[3 0.75 0.5 0.1];
Paleo.sl=[73 15 7.5 0];
Paleo.slsd=[3 10 2.5 0.1];
paleocolor=[124 130 130]/255;

figure;
clf;
for www=1:length(Paleo.T);
    paleopatch(www)=patch([Paleo.T(www)+Paleo.Tsd(www) ...
        Paleo.T(www)-Paleo.Tsd(www) ...
        Paleo.T(www)-Paleo.Tsd(www) ...
        Paleo.T(www)+Paleo.Tsd(www) ...
        Paleo.T(www)+Paleo.Tsd(www)], ...
        [Paleo.sl(www)+Paleo.slsd(www) ...
        Paleo.sl(www)+Paleo.slsd(www) ...
        Paleo.sl(www)-Paleo.slsd(www) ...
        Paleo.sl(www)-Paleo.slsd(www) ...
        Paleo.sl(www)+Paleo.slsd(www)],'k', ...
        'EdgeColor', 'none', 'FaceAlpha', 0.2)
    ht=text(Paleo.T(www)+0*Paleo.Tsd(www),Paleo.sl(www)+Paleo.slsd(www),Paleo.label(www),'FontSize',fontsize-2, ...
    'VerticalAlignment','bottom','HorizontalAlignment','center','FontAngle','italic','Color',[.2 .2 .2]);
end
%             for www=1:length(Paleo.T);
%                 plot(Paleo.T(www)*[1 1]+Paleo.Tsd(www),Paleo.sl(www)*[1 1]+Paleo.slsd(www).*[-1 1],'-','Color',paleocolor);
%                 plot(Paleo.T(www)*[1 1]-Paleo.Tsd(www),Paleo.sl(www)*[1 1]+Paleo.slsd(www).*[-1 1],'-','Color',paleocolor);
%                 plot(Paleo.T(www)*[1 1]+Paleo.Tsd(www).*[-1 1],Paleo.sl(www)*[1 1]-Paleo.slsd(www),'-','Color',paleocolor);
%                 plot(Paleo.T(www)*[1 1]-Paleo.Tsd(www).*[-1 1],Paleo.sl(www)*[1 1]+Paleo.slsd(www),'-','Color',paleocolor);
%                 %plot(Paleo.T(www)*[1 1],Paleo.sl(www)+[-1 1]*Paleo.slsd(www),'-','Color',paleocolor);
%                 %plot(Paleo.T(www)+[1 -1]*Paleo.Tsd(www),Paleo.sl(www)*[1 1],'-','Color',paleocolor);
%             end
%hl=legend(paleopatch(1),'Paleo ranges','Location','Northwest');
hold on;

plot([1 1]*GSATwl(end),GMSLLC90(2,[1 3]),'Color',(colrs(3,:)+3*[1 1 1])/4,'LineWidth',5); hold on;
plot([1 1]*GSATwl(end),GMSLLC(2,[1 3]),'Color',(colrs(3,:)+2*[1 1 1])/3,'LineWidth',10); hold on;
plot([1 1]*GSATwl(2),GMSLLC90(1,[1 3]),'Color',(colrs(3,:)+3*[1 1 1])/4,'LineWidth',5); hold on;
plot([1 1]*GSATwl(2),GMSLLC(1,[1 3]),'Color',(colrs(3,:)+2*[1 1 1])/3,'LineWidth',10); hold on;

for sss=1:length(GSATwl);
    plot([1 1]*GSATwl(sss),GMSLwl(sss,[1 3]),'Color',colrs(3,:),'LineWidth',10);
    plot([1 1]*GSATwl(sss),GMSLwl2050(sss,[1 3]),'Color',colrs(4,:),'LineWidth',10);
end
for sss=1:length(GSATwl);
    plot([1 1]*GSATwl(sss),GMSLcom2000(sss,[1 2]),'Color',colrs(2,:),'LineWidth',10);
    hold on;
    plot([1 1]*GSATwl(sss),GMSLcom10000(sss,[1 2]),'Color',colrs(1,:),'LineWidth',10);
end
xlabel('Peak Global Surface Temperature (\circC)');
box on;
% pos=get(gca,'position');
% pos(2)=pos(2)-.06;
% set(gca,'position',pos);

txt = {sprintf('10,000-yr')};
text(4.5 ,30 ,txt,'FontSize',fontsize, ...
    'Color', colrs(1,:),'HorizontalAlignment','center','FontWeight','bold')

txt = {sprintf('2,000-yr')};
ht=    text(4.5 ,14.5 ,txt,'FontSize',fontsize, ...
        'Color', colrs(2,:),'HorizontalAlignment','center','FontWeight','bold')


txt = {'100-yr'};
text(4.5 ,1 ,txt,'FontSize',fontsize, ...
        'Color', colrs(3,:),'HorizontalAlignment','center','FontWeight','bold')

% for www=1:length(Paleo.T);
%     plot(Paleo.T(www)*[1 1]+Paleo.Tsd(www),Paleo.sl(www)*[1 1]+Paleo.slsd(www).*[-1 1],'-','Color',paleocolor);
%     plot(Paleo.T(www)*[1 1]-Paleo.Tsd(www),Paleo.sl(www)*[1 1]+Paleo.slsd(www).*[-1 1],'-','Color',paleocolor);
%     plot(Paleo.T(www)*[1 1]+Paleo.Tsd(www).*[-1 1],Paleo.sl(www)*[1 1]-Paleo.slsd(www),'-','Color',paleocolor);
%     plot(Paleo.T(www)*[1 1]-Paleo.Tsd(www).*[-1 1],Paleo.sl(www)*[1 1]+Paleo.slsd(www),'-','Color',paleocolor);
%     %plot(Paleo.T(www)*[1 1],Paleo.sl(www)+[-1 1]*Paleo.slsd(www),'-','Color',paleocolor);
%     %plot(Paleo.T(www)+[1 -1]*Paleo.Tsd(www),Paleo.sl(www)*[1 1],'-','Color',paleocolor);
% end

ylabel('GMSL rise (m)');
hl=legend(paleopatch(1),'Paleo ranges','Location','Northwest');
set(gca,'xlim',[0.4 5.3],'xtick',[1 1.5 2:5],'fontsize',fontsize,'ylim',[0 39.5]);
ht=title({'b) Committed sea level rise by warming level and timescale'})

set(gcf,'PaperPosition',[0.3611 2.5833 7.7778 8.2]);

saveas(gcf,'TSwls_1panel.png','png');
print(gcf,'TSwls_1panel.eps','-depsc2', '-painters');
