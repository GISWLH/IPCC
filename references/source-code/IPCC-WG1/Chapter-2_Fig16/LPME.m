function createfigure(getcolumn1, YMatrix1)
%CREATEFIGURE(getcolumn1, YMatrix1)
%  GETCOLUMN1:  vector of x data
%  YMATRIX1:  matrix of y data

% Create figure
figure1 = figure('Color',[1 1 1]);

% Create axes
axes1 = axes('Parent',figure1,...
    'Position',[0.13 0.15 0.83 0.78]);
hold(axes1,'on');
ax = gca;
ax.LineWidth = 2;
set(gcf,'Position',[200,200,1000,500],'PaperPositionMode','Auto')
set(gca, 'ActivePositionProperty', 'OuterPosition');

load('LPME2.mat');
t=LPMEd(:,1);
% Create multiple lines using matrix input to plot
plot1 = plot(t,LPMEd(:,[2:9]),'LineWidth',4,'Parent',axes1);
set(plot1(1),'DisplayName','20CRv3','Color',[0.7686 0.4745 0]);
set(plot1(2),'DisplayName','CFSR','Color',[0.3294 0.5725 0.8039]);
set(plot1(3),'DisplayName','ERA5','Color',[0 0 0]);
set(plot1(4),'DisplayName','ERA20C','Color',[0.5020 0.5020 0.5020]);
set(plot1(5),'DisplayName','ERA20CM','Color',[0 0.2039 0.4]);
set(plot1(6),'DisplayName','JRA-55','Color',[0 0.3098 0]);
set(plot1(7),'DisplayName','MERRA','Color',[0.8745 0.7608 0.4902]);
set(plot1(8),'DisplayName','MERRA-2','Color',[0.6627 0.8157 0.5569]);

% Create ylabel
ylabel('P-E (mm/day1)','FontSize',30);
% Create title
title('Land','FontSize', 30, 'FontWeight', 'bold','Visible','on')
% Uncomment the following line to preserve the X-limits of the axes
xlim(axes1,[1979 2017]);
box(axes1,'on');
% Set the remaining axes properties
set(axes1,'FontSize',24);
% Create legend
legend1 = legend(axes1,'show');
set(legend1,'Location','eastoutside','FontSize',24);

