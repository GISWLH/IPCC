function createfigure(X1, YMatrix1)
%CREATEFIGURE(X1, YMatrix1)
%  X1:  vector of x data
%  YMATRIX1:  matrix of y data

% Create figure
figure1 = figure('PaperUnits','centimeters','PaperSize',[150 100],...
    'Color',[1 1 1]);
% Create axes
axes1 = axes('Parent',figure1,...
    'Position',[0.13 0.2 0.78 0.7]);
hold(axes1,'on');
ax = gca;
ax.LineWidth = 2;
set(gcf,'Position',[200,200,1200,500],'PaperPositionMode','Auto')

load('precipglobalavedata2019_4.mat');
t=precipglobalaverage([2 11],1);
% Create multiple lines using matrix input to plot
plot1 = plot(t,precipglobalaverage([2 11],[6:10]),'LineWidth',3,'Parent',axes1);
set(plot1(1),'LineWidth',1,'LineStyle','--','Color',[0.5020 0.5020 0.5020],'DisplayName','');
set(plot1(2),'LineWidth',3,'Color',[0.7686 0.4745 0],'DisplayName','GPCC V2020');
set(plot1(3),'LineWidth',3,'Color',[0.3294 0.5725 0.8039],'DisplayName','CRU TS 4.04');
set(plot1(4),'LineWidth',3,'Color',[0 0 0],'DisplayName','GHCN V4');
set(plot1(5),'LineWidth',3,'LineStyle',':','Color',[0 0.3098 0],'DisplayName','GPCP V2.3');
hold on
t=precipglobalaverage([12 21],1);
plot1 = plot(t,precipglobalaverage([12 21],[6:10]),'LineWidth',3,'Parent',axes1);
set(plot1(1),'LineWidth',1,'LineStyle','--','Color',[0.5020 0.5020 0.5020],'DisplayName','');
set(plot1(2),'LineWidth',3,'Color',[0.7686 0.4745 0],'DisplayName','GPCC V2020');
set(plot1(3),'LineWidth',3,'Color',[0.3294 0.5725 0.8039],'DisplayName','CRU TS 4.04');
set(plot1(4),'LineWidth',3,'Color',[0 0 0],'DisplayName','GHCN V2');
set(plot1(5),'LineWidth',3,'LineStyle',':','Color',[0 0.3098 0],'DisplayName','GPCP V2.3');
hold on
t=precipglobalaverage([22 31],1);
plot1 = plot(t,precipglobalaverage([22 31],[6:10]),'LineWidth',3,'Parent',axes1);
set(plot1(1),'LineWidth',1,'LineStyle','--','Color',[0.5020 0.5020 0.5020],'DisplayName','');
set(plot1(2),'LineWidth',3,'Color',[0.7686 0.4745 0],'DisplayName','GPCC V2020');
set(plot1(3),'LineWidth',3,'Color',[0.3294 0.5725 0.8039],'DisplayName','CRU TS 4.04');
set(plot1(4),'LineWidth',3,'Color',[0 0 0],'DisplayName','GHCN V2');
set(plot1(5),'LineWidth',3,'LineStyle',':','Color',[0 0.3098 0],'DisplayName','GPCP V2.3');
hold on
t=precipglobalaverage([32 41],1);
plot1 = plot(t,precipglobalaverage([32 41],[6:10]),'LineWidth',3,'Parent',axes1);
set(plot1(1),'LineWidth',1,'LineStyle','--','Color',[0.5020 0.5020 0.5020]);
set(plot1(2),'LineWidth',3,'Color',[0.7686 0.4745 0]);
set(plot1(3),'LineWidth',3,'Color',[0.3294 0.5725 0.8039]);
set(plot1(4),'LineWidth',3,'Color',[0 0 0]);
set(plot1(5),'LineWidth',3,'LineStyle',':','Color',[0 0.3098 0]);
hold on
t=precipglobalaverage([42 51],1);
plot1 = plot(t,precipglobalaverage([42 51],[6:10]),'LineWidth',3,'Parent',axes1);
set(plot1(1),'LineWidth',1,'LineStyle','--','Color',[0.5020 0.5020 0.5020]);
set(plot1(2),'LineWidth',3,'Color',[0.7686 0.4745 0]);
set(plot1(3),'LineWidth',3,'Color',[0.3294 0.5725 0.8039]);
set(plot1(4),'LineWidth',3,'Color',[0 0 0]);
set(plot1(5),'LineWidth',3,'LineStyle',':','Color',[0 0.3098 0]);
hold on
t=precipglobalaverage([52 61],1);
plot1 = plot(t,precipglobalaverage([52 61],[6:10]),'LineWidth',3,'Parent',axes1);
set(plot1(1),'LineWidth',1,'LineStyle','--','Color',[0.5020 0.5020 0.5020]);
set(plot1(2),'LineWidth',3,'Color',[0.7686 0.4745 0]);
set(plot1(3),'LineWidth',3,'Color',[0.3294 0.5725 0.8039]);
set(plot1(4),'LineWidth',3,'Color',[0 0 0]);
set(plot1(5),'LineWidth',3,'LineStyle',':','Color',[0 0.3098 0]);
hold on
t=precipglobalaverage([62 71],1);
plot1 = plot(t,precipglobalaverage([62 71],[6:10]),'LineWidth',3,'Parent',axes1);
set(plot1(1),'LineWidth',1,'LineStyle','--','Color',[0.5020 0.5020 0.5020]);
set(plot1(2),'LineWidth',3,'Color',[0.7686 0.4745 0]);
set(plot1(3),'LineWidth',3,'Color',[0.3294 0.5725 0.8039]);
set(plot1(4),'LineWidth',3,'Color',[0 0 0]);
set(plot1(5),'LineWidth',3,'LineStyle',':','Color',[0 0.3098 0]);
hold on
t=precipglobalaverage([72 81],1);
plot1 = plot(t,precipglobalaverage([72 81],[6:10]),'LineWidth',3,'Parent',axes1);
set(plot1(1),'LineWidth',1,'LineStyle','--','Color',[0.5020 0.5020 0.5020]);
set(plot1(2),'LineWidth',3,'Color',[0.7686 0.4745 0]);
set(plot1(3),'LineWidth',3,'Color',[0.3294 0.5725 0.8039]);
set(plot1(4),'LineWidth',3,'Color',[0 0 0]);
set(plot1(5),'LineWidth',3,'LineStyle',':','Color',[0 0.3098 0]);
hold on
t=precipglobalaverage([82 91],1);
plot1 = plot(t,precipglobalaverage([82 91],[6:10]),'LineWidth',3,'Parent',axes1);
set(plot1(1),'LineWidth',1,'LineStyle','--','Color',[0.5020 0.5020 0.5020]);
set(plot1(2),'LineWidth',3,'Color',[0.7686 0.4745 0]);
set(plot1(3),'LineWidth',3,'Color',[0.3294 0.5725 0.8039]);
set(plot1(4),'LineWidth',3,'Color',[0 0 0]);
set(plot1(5),'LineWidth',3,'LineStyle',':','Color',[0 0.3098 0]);
hold on
t=precipglobalaverage([92 101],1);
plot1 = plot(t,precipglobalaverage([92 101],[6:10]),'LineWidth',3,'Parent',axes1);
set(plot1(1),'LineWidth',1,'LineStyle','--','Color',[0.5020 0.5020 0.5020]);
set(plot1(2),'LineWidth',3,'Color',[0.7686 0.4745 0]);
set(plot1(3),'LineWidth',3,'Color',[0.3294 0.5725 0.8039]);
set(plot1(4),'LineWidth',3,'Color',[0 0 0]);
set(plot1(5),'LineWidth',3,'LineStyle',':','Color',[0 0.3098 0]);
hold on
t=precipglobalaverage([102 111],1);
plot1 = plot(t,precipglobalaverage([102 111],[6:10]),'LineWidth',3,'Parent',axes1);
set(plot1(1),'LineWidth',1,'LineStyle','--','Color',[0.5020 0.5020 0.5020]);
set(plot1(2),'LineWidth',3,'Color',[0.7686 0.4745 0]);
set(plot1(3),'LineWidth',3,'Color',[0.3294 0.5725 0.8039]);
set(plot1(4),'LineWidth',3,'Color',[0 0 0]);
set(plot1(5),'LineWidth',3,'LineStyle',':','Color',[0 0.3098 0]);
hold on
t=precipglobalaverage([112 121],1);
plot1 = plot(t,precipglobalaverage([112 121],[6:10]),'LineWidth',3,'Parent',axes1);
set(plot1(1),'LineWidth',1,'LineStyle','--','Color',[0.5020 0.5020 0.5020]);
set(plot1(2),'LineWidth',3,'Color',[0.7686 0.4745 0]);
set(plot1(3),'LineWidth',3,'Color',[0.3294 0.5725 0.8039]);
set(plot1(4),'LineWidth',3,'Color',[0 0 0]);
set(plot1(5),'LineWidth',3,'LineStyle',':','Color',[0 0.3098 0]);
hold on
t=precipglobalaverage([122 131],1);
plot1 = plot(t,precipglobalaverage([122 129],[6:10]),'LineWidth',3,'Parent',axes1);
set(plot1(1),'LineWidth',1,'LineStyle','--','Color',[0.5020 0.5020 0.5020]);
set(plot1(2),'LineWidth',3,'Color',[0.7686 0.4745 0]);
set(plot1(3),'LineWidth',3,'Color',[0.3294 0.5725 0.8039]);
set(plot1(4),'LineWidth',3,'Color',[0 0 0]);
set(plot1(5),'LineWidth',3,'LineStyle',':','Color',[0 0.3098 0]);

% Create ylabel
ylabel('mm yr^-^1','FontWeight','bold',...
    'FontSize',24);

% Uncomment the following line to preserve the X-limits of the axes
xlim(axes1,[1890 2020]);
ylim([-35 35]);
yticks([-30 -20 -10 0 10 20 30])
box(axes1,'off');
% Set the remaining axes properties
set(axes1,'FontSize',24);
% Create legend
%legend1 = legend(axes1,'show');
%set(legend1,...
%    'Position',[0.824672908035948 0.76227613620714 0.166898795511286 0.212305030748377]);
print('globalpp_timeseriesdec_4.eps', '-depsc')

