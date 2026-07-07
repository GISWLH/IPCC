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
t=precipglobalaverage(:,1);
% Create multiple lines using matrix input to plot
plot1 = plot(t,precipglobalaverage(:,[2:6]),'LineWidth',3,'Parent',axes1);
set(plot1(1),'LineWidth',3,'Color',[0.7686 0.4745 0],'DisplayName','GPCC V2020');
set(plot1(2),'LineWidth',3,'Color',[0.3294 0.5725 0.8039],'DisplayName','CRU TS 4.04');
set(plot1(3),'LineWidth',3,'Color',[0 0 0],'DisplayName','GHCN V4');
set(plot1(4),'LineWidth',3,'LineStyle',':','Color',[0 0.3098 0],'DisplayName','GPCP V2.3');
set(plot1(5),'LineWidth',1,'LineStyle','--','Color',[0.5020 0.5020 0.5020],'DisplayName','');

% Create ylabel
ylabel('mm yr^-^1','FontWeight','bold',...
    'FontSize',24);

% Uncomment the following line to preserve the X-limits of the axes
xlim(axes1,[1890 2020]);
ylim([-95 95]);
yticks([-75 -50 -25 0 25 50 75])
box(axes1,'off');
% Set the remaining axes properties
set(axes1,'FontSize',24);
% Create legend
legend1 = legend(axes1,'show');
set(legend1,...
    'Position',[0.287178889106055 0.0206348703335917 0.412024146888471 0.0548093598264962],'Orientation','horizontal',...
    'FontSize',20);
print('globalpp_timeseries_3.eps', '-depsc')

