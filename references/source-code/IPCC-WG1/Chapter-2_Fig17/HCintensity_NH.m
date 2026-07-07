function createfigure(getcolumn1, YMatrix1)
%CREATEFIGURE(getcolumn1, YMatrix1)
%  GETCOLUMN1:  vector of x data
%  YMATRIX1:  matrix of y data

% Create figure
figure1 = figure('Color',[1 1 1]);

% Create axes
axes1 = axes('Parent',figure1,...
    'Position',[0.13 0.2 0.78 0.7]);
hold(axes1,'on');
ax = gca;
ax.LineWidth = 2;
set(gcf,'Position',[200,200,1000,600],'PaperPositionMode','Auto')

load('HCintensity_2.mat');
t=HCintensity(:,1);
% Create multiple lines using matrix input to plot
plot1 = plot(t,HCintensity(:,[2:5]),'LineWidth',3,'Parent',axes1);
set(plot1(1),'DisplayName','ERA-Interim','Color',[0.3294 0.5725 0.8039]);
set(plot1(2),'DisplayName','JRA-55','Color',[0.7686 0.4745 0]);
set(plot1(3),'DisplayName','MERRA2','Color',[0.5020 0.5020 0.5020]);
set(plot1(4),'DisplayName','ERA5','Color',[0 0 0]);

% Create ylabel
ylabel('Intensity (10^1^1 kgs^-^1)','FontSize',24);
% Create title
title('NH','FontSize', 30, 'FontWeight', 'bold','Visible','on')
% Uncomment the following line to preserve the X-limits of the axes
xlim(axes1,[1979 2019]);
% Uncomment the following line to preserve the Y-limits of the axes
ylim(axes1,[80000000000 150000000000]);
box(axes1,'off');
% Set the remaining axes properties
set(axes1,'FontSize',24,'XGrid','off','YGrid','off');
% Create legend
legend1 = legend(axes1,'show');
legend('boxoff')
set(legend1,...
    'Position',[0.287178889106056 0.0206348703335917 0.412024146888471 0.0548093598264962],...
    'Orientation','horizontal',...
    'FontSize',24);
print('HC_int_NH.eps', '-depsc')

