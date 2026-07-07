function createfigure(YMatrix1)
%CREATEFIGURE(YMatrix1)
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
set(gcf,'Position',[200,200,1200,600],'PaperPositionMode','Auto')

load('sam_reconst.mat');
t=sam_a(:,1);

% Create multiple lines using matrix input to plot
plot1 = plot(t,sam_a(:,[2:8]),'LineWidth',3,'Parent',axes1);
set(plot1(1),'LineWidth',1,'Color',[0.3294 0.5725 0.8039],'DisplayName','SAM Abram et al. (2014)');
set(plot1(2),'LineWidth',3,'Color',[0 0.2039 0.4],'DisplayName','');
set(plot1(3),'LineWidth',1,'Color',[0.8745 0.7608 0.4902],'DisplayName','SAM Villalba et al. (2012)');
set(plot1(4),'LineWidth',3,'Color',[0.7686 0.4745 0],'DisplayName','');
set(plot1(5),'LineWidth',1,'Color',[0.6627 0.8157 0.5569],'DisplayName','SAM Dätwyler et al. (2018)');
set(plot1(6),'LineWidth',3,'Color',[0 0.5 0],'DisplayName','');
set(plot1(7),'LineWidth',1,'LineStyle','--','Color',[0.5020 0.5020 0.5020],'DisplayName','');

% Create ylabel
ylabel('SAM index','FontWeight','bold',...
    'FontSize',24);

% Uncomment the following line to preserve the X-limits of the axes
xlim(axes1,[1000 2010]);
ylim([-5.5 2.5]);
box(axes1,'off');
%ax.XAxis.Visible = 'off'; % remove x-axis
% Set the remainig axes properties
set(axes1,'FontSize',24);
% Create legend
%legend1 = legend(axes1,'show');
%set(legend1,...
%    'Position',[0.287178889106055 0.0206348703335917 0.412024146888471 0.0548093598264962],'Orientation','vertical',...
%    'FontSize',20);
print('sam_timeseriesdjf.eps', '-depsc')

