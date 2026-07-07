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

load('sam_obs.mat');
t=sam_c(:,1);

% Create multiple lines using matrix input to plot
plot1 = plot(t,sam_c(:,[2:6]),'LineWidth',3,'Parent',axes1);
set(plot1(1),'LineWidth',2,'Color',[0.8745 0.7608 0.4902],'DisplayName','SAM Fogt');
set(plot1(2),'LineWidth',2,'Color',[0.7686 0.4745 0],'DisplayName','SAM 20CRv2c');
set(plot1(3),'LineWidth',2,'Color',[0 0 0],'DisplayName','SAM Marshall');
set(plot1(4),'LineWidth',2,'Color',[0.3294 0.5725 0.8039],'DisplayName','SAM NCEP');
set(plot1(5),'LineWidth',1,'LineStyle','--','Color',[0.5020 0.5020 0.5020],'DisplayName','');

% Create ylabel
ylabel('SAM Index','FontWeight','bold',...
    'FontSize',24);

% Uncomment the following line to preserve the X-limits of the axes
xlim(axes1,[1900 2020]);
ylim([-5 4.5]);
box(axes1,'off');
%ax.XAxis.Visible = 'off'; % remove x-axis
% Set the remainig axes properties
set(axes1,'FontSize',24);
% Create legend
%legend1 = legend(axes1,'show');
%set(legend1,...
%    'Position',[0.287178889106055 0.0206348703335917 0.412024146888471 0.0548093598264962],'Orientation','horizontal',...
%    'FontSize',16);
print('sam_timeseriescent.eps', '-depsc')

