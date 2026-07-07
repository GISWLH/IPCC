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
set(gcf,'Position',[200,200,1200,600],'PaperPositionMode','Auto')

load('tcwv6.mat');
t=tcwv(:,1);
% Create multiple lines using matrix input to plot
plot1 = plot(t,tcwv(:,[2:8]),'LineWidth',3,'Parent',axes1);
set(plot1(1),'LineWidth',3,'Color',[0.3294 0.5725 0.8039],'DisplayName','JRA55');
set(plot1(2),'LineWidth',3,'Color',[0.7686 0.4745 0],'DisplayName','ERA5');
set(plot1(3),'LineWidth',3,'Color',[0 0 0],'DisplayName','20CRv3');
set(plot1(4),'LineWidth',3,'Color',[0 0.3098 0],'DisplayName','HOAPS v4');
set(plot1(5),'LineWidth',3,'LineStyle',':','Color',[0.2627 0.5765 0.7647],'DisplayName','REMSS v7');
set(plot1(6),'LineWidth',3,'Color',[0 0.2039 0.4],'DisplayName','NVAP-M');
set(plot1(7),'LineWidth',1,'LineStyle','--','Color',[0.5020 0.5020 0.5020]);

% Create ylabel
ylabel('Anomaly (mm)','FontWeight','bold',...
    'FontSize',24);

% Uncomment the following line to preserve the X-limits of the axes
xlim(axes1,[1978 2020]);
ylim([-1.50 1.50]);
box(axes1,'off');
% Set the remaining axes properties
set(axes1,'FontSize',24);
% Create legend
%legend1 = legend(axes1,'show');
%set(legend1,...
%    'Position',[0.287178889106055 0.0206348703335917 0.412024146888471 0.0548093598264962],'Orientation','vertical',...
%    'FontSize',20);
print('globaltcwv_timeseries.eps', '-depsc')

