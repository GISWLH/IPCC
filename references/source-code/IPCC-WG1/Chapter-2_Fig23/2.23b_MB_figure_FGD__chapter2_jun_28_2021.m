clear all
clc
format long g

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Description
% Script to generate the  annual and decadal global glacier mass change (Gt yr-1) from 1961 until 2018
% for Figure 2.23. I
% Includes the global annual mass balance from Zemp et al. (2019/2020), global mass balance between 2002-2016
% from Wouters et al. (2019), global mass balance between 2006-2015 from SROCC and decadal (2000-2010 and 2010-2020)
% global mass balance from Hugonnet et al. (2021)

%Ranges show the 90% confidence  interval.

% script create by Lucas Ruiz (LA chapter 9) for Chapter 2 of AR6 WGI.

% Files you need:

% IPCC color scheme = 'colorscheme.mat' 

% Global results of Zemp et al (2019) = 'Zemp_etal_results_global.csv'

% Global results of Wouters et al (2019) = 'annual_MB_Gtyr.mat'

% File preparated by Romain Hugonnet for Chapter 9 = 'table_hugonnet_regions_10yr_ar6period.xlsx'

% shadedplot.m matlab function


%% Data input for the figure 
 % Please include the correct path
 
 path_to_figure_folder = 'c:\Users\lcsru\OneDrive\Documents\IPCC-AR6\09-FGD\Chapter2_figure\'
 
  
 % Zemp et al. (2019) time series of global mass balance changes 
  % (supplementary materials)
file_Zemp_sm =[path_to_figure_folder, 'INPUT_FILES\Zemp_etal_results_global.csv'];
 
 % Location of xlsx file of Hugonnet et al 2020 10yr period pofr AR6
 file_hugonnet = [path_to_figure_folder,'INPUT_FILES\table_hugonnet_regions_10yr_ar6period.xlsx'];
 
 %% Figure format
 
 %Define Figure filename for  eps and pdf file
 figure_filename= 'raw_MB_figure_FGD__chapter2_jun_28_2021';
 
% Define extent and position of  the figure 
% Figure width [cm]
w_fig = 18; 
% Figure height [cm]
h_fig = 14; 
 
 %Define the color of each line and shaded area to be ploted in the figure
 % following IPCC Color scheme
 load('colorscheme.mat')

%Shaded colors
shade_rgb =  colorscheme_RGB. shade_0_RGB;
% Line color
line_rgb =  colorscheme_RGB. line_6_RGB;

clear colorscheme_RGB
 
 % Define Zemp data colors
Zemp_shading = [shade_rgb(4,:)]; 
Zemp_line = [line_rgb(4,:)];

% Define SROCC data colors
SROCC_shading = [shade_rgb(3,:)]; 
SROCC_line =[line_rgb(3,:)]; 

% Define GRACE (Wouters) data colors
Wouters_shading = [shade_rgb(5,:)]; 
Wouters_line =[line_rgb(5,:)]; 

% Define Hugonet data colors
Hugonet_shading = [shade_rgb(6,:)]; 
Hugonet_line = [line_rgb(6,:)]; 

% Define point sizes for the figure
p_size =5;

% define time period
time_period = [1960:10:2020];
%create xticks label from time period
for j = 1:1:length(time_period);
tick_time(1,j) = {num2str(time_period(j))};
end


%% Read Zemp et al 2019 time series 
   % raw table
   M = csvread(file_Zemp_sm,20,0);
    time =M(:,1);
    sel_time =find(time>=1962);
    
    % # Year: hydrological year   
    zemp_time = time(sel_time);
    % Area
    area_km2 = M(sel_time,2);
    % # dM_INT_Gt: global mass change (Gt yr-1) based on spatial interpolation                       #
    int_gt = M(sel_time,3); 
    % # sig_Total_Gt: Total uncertainty of regional mass change (Gt yr-1)                            # 
     e_int_gt = M(sel_time,9);
    % # sig_Glac_Gt: uncertainty related to glaciological variability (Gt yr-1)    
     e_glac_gt  = M(sel_time,4);
     % # sig_Geod_Gt: uncertainty related to geodetic value (Gt yr-1)                    
     e_geod_gt =  M(sel_time,5);
     % # sig_Int_Gt: uncertainty related to regional interpolation (Gt yr-1)                     
     e_int_gt = M(sel_time,6);
     
     clear M
     clear sel_time
     
  % Add manually the values for 2016/2017and 2017/2018 from Zemp et al
  % (2020) Table 1
     zemp_time = [zemp_time;2017;2018];
     area_km2 = [area_km2;669223;666946];
     int_gt = [int_gt;-316;-502];
     e_int_gt = [e_int_gt;240;197];
     e_glac_gt = [e_glac_gt;e_glac_gt(end);e_glac_gt(end)];
     e_geod_gt = [e_geod_gt;e_geod_gt(end);e_geod_gt(end)];
     
   % Loop to calculate the mean value for each 10 yr period
      for k =1:1:length(time_period)-1;
      sel_time = find(zemp_time>=time_period(k) & zemp_time<=time_period(k+1));%%%%%%%%%%%%%%%%%%%%
    
             mean_mb_period(1,k) = mean(int_gt(sel_time,1));
                      e_glac = (sqrt(sum(e_glac_gt(sel_time,1).^2)))/length(sel_time);
                      e_geod = sum(e_geod_gt(sel_time,1))/length(sel_time);
                      e_int = (sqrt(sum(e_int_gt(sel_time,1).^2)))/length(sel_time);
             mean_mb_period(2,k) = sqrt(e_glac^2+e_geod^2+e_int^2);
             clear e_glac e_geod e_int
      end
      
 
     
%% Read Wouters et al (2019) data
% load file_wouters no implemented
% Here I just declare the values taken from Table 1 of Wouters et al.
% (2019)
% Average GRACE mass trends for April 2002-August 2016 and uncertainty
wouter_global = [-198.5 32.4]; 
% Time range
wouter_time = [2002 2016];

%% Read SROCC Annex 2 table value
% Mean global mass balance and uncertainty as 90% CI
SROCC_global = [-278 113];
% Time range
SROCC_time = [2006 2015];

 %% Read Hugonnet et al 2020 decadal values

%raw data
 [raw,text,all] = xlsread(file_hugonnet,1,'A2:F58');
 
 % time periods
 time_periods = cell2mat(text(1:end,1));
  [time_idx,time_label] = grp2idx(time_periods);
 t_1 = str2num(time_periods(:,1:4));
 t_2 = str2num(time_periods(:,12:15));
 time_window = [t_1 t_2];
 
 % Regions
    regions_file = raw(:,1);
 % mass balance kg m-2 yr-1
  mass_balance_kg = raw(:,5:6);
  % mass balance Gt yr-1
  mass_balance_gt = raw(:,3:4);
  clear raw text all
  % first period selection
 p1_hugonnet = 1:3:55;
 % second period selection
 p2_hugonnet = 2:3:56;

 % Global value 10 yr period 
 global_mb_gt(1,1) = sum(mass_balance_gt(p1_hugonnet,1),1);
 global_mb_gt(1,2) = sqrt(sum((mass_balance_gt(p1_hugonnet,2)).^2,1));
 global_mb_gt(2,1) = sum(mass_balance_gt(p2_hugonnet,1),1);
 global_mb_gt(2,2) = sqrt(sum((mass_balance_gt(p2_hugonnet,2)).^2,1));
 t1_hugonnet = [2000 2010];
 t2_hugonnet = [2010 2019];
 
   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
   %% Start figure
     figure(1)
     %size of figure defined by IPCC visual style guide [cm]
     figSize = [1 1 w_fig h_fig]; 
     
     % set size and position
     set(gcf,'units','centimeters','position',figSize,'paperposition',figSize);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
 % define the width of the lines
    line_width =3

     
 % Plot decadal Zemp et al 2019 uncertainty    
 %Change the last value of decadal vlaue to the last data vlaue
 time_period_z = time_period;
 time_period_z(end) = 2018;

     for t_idx = 1:1:length(time_period)-1;
    
     % plot shade mb per time period
     y_zemp1 =  (mean_mb_period(1,t_idx)+mean_mb_period(2,t_idx)).*ones(1,2);
     y_zemp2 = (mean_mb_period(1,t_idx)-mean_mb_period(2,t_idx)).*ones(1,2);
     shadedplot(time_period_z(1,t_idx:t_idx+1), y_zemp1, y_zemp2,Zemp_shading.*1.2);
     hold on
     
     end
     
   
            
     
   % Plot annual Zemp et al 2019/2020 time series  uncertainty shaded area
  y_zemp1_annual =  (int_gt+e_int_gt);
  y_zemp2_annual = (int_gt-e_int_gt);
     shadedplot(zemp_time, y_zemp1_annual', y_zemp2_annual',Zemp_shading);
     hold on
     
     
     % Plot annual Zemp et al 2019/2020 time series  value
  p_zemp_annual = plot(zemp_time,int_gt,...
         'LineStyle', '-','Color',Zemp_line,'LineWidth',2);
     hold on
     
 
     
  % Plot Wouter et al 2019  uncertainty shaded area
  % upper curve of uncertainty
     y_1_wouters = (wouter_global(1,1)+wouter_global(1,2)).*ones(1,2);
      % lower curve of uncertainty
     y_2_wouters =(wouter_global(1,1)-wouter_global(1,2)).*ones(1,2);
     %Plot uncertainty as grey  shaded area
     shadedplot(wouter_time, y_1_wouters, y_2_wouters,Wouters_shading);
        
     hold on
     
   % Plot SROCC Chapter 2 uncertainty shaded area
   % upper curve of uncertainty
     y_1_srocc = (SROCC_global(1,1)+SROCC_global(1,2)).*ones(1,2);
      % lower curve of uncertainty
     y_2_srocc =(SROCC_global(1,1)-SROCC_global(1,2)).*ones(1,2);
     %Plot uncertainty as grey  shaded area
     shadedplot( SROCC_time, y_1_srocc, y_2_srocc,SROCC_shading);
      hold on
         
     % Plot Hugonnet et al (submitted) first period
     % upper curve of uncertainty
     y_1_hugo =(global_mb_gt(1,1)+global_mb_gt(1,2))*ones(1,2);
      % lower curve of uncertainty
     y_2_hugo =(global_mb_gt(1,1)-global_mb_gt(1,2))*ones(1,2);
     %Plot uncertainty as grey  shaded area
     shadedplot(t1_hugonnet , y_1_hugo, y_2_hugo,Hugonet_shading);
     hold on
     
     % Plot Hugonnet et al (submitted) second period
     % upper curve of uncertainty
     y_1_hugo =(global_mb_gt(2,1)+global_mb_gt(2,2))*ones(1,2);
      % lower curve of uncertainty
     y_2_hugo =(global_mb_gt(2,1)-global_mb_gt(2,2))*ones(1,2);
     %Plot uncertainty as grey  shaded area
     shadedplot(t2_hugonnet , y_1_hugo, y_2_hugo,Hugonet_shading);
     hold on
              
         
       % Plot decadal Zemp et al 2019 values    
      for t_idx = 1:1:length(time_period)-1;
     
     % plot line mb per time period
     p_zemp = plot(time_period_z(1,t_idx:t_idx+1),mean_mb_period(1,t_idx).*ones(1,2),...
         'LineStyle', '-','Color',Zemp_line.*0.4,'LineWidth',line_width);
     hold on
      end
     
  % Plot Wouter et al 2019  value     
      p_wouter = plot( wouter_time, wouter_global(1,1).*ones(1,2),'Color',Wouters_line,'LineWidth',line_width);
      hold on
    
    % Plot SROCC Chapter 2 value
    p_srocc = plot( SROCC_time,SROCC_global(1,1).*ones(1,2),'Color',SROCC_line,'LineWidth',line_width);
    hold on
     
     % Plot Hugonnet et al (2021)    
    p_hugo = plot( t1_hugonnet, global_mb_gt(1,1).*ones(1,2),'Color',Hugonet_line,'LineWidth',line_width);
     hold on
   p_hugo = plot( t2_hugonnet, global_mb_gt(2,1).*ones(1,2),'Color',Hugonet_line,'LineWidth',line_width);
   hold on


     
%  Set yticks and ylabel font size and values
%      set(gca,'FontSize',9,'YTick',[-1000 -500  250 0 250 500],'YTickLabel',...
%            {'-'-500';'-250';'0' },'YLim', [-700 50])
%       
         ylabel(['Mass change (Gt yr^-^1)'],'FontName','Arial','FontSize',11 );
   
   
%   Set xticks and ylabel font size and values
        set(gca, 'FontName','Arial','FontSize',9,'XTick', time_period,'XTickLabel',...
          tick_time,'XLim', [time_period(1) time_period(end)])
      
      xlabel('Years','FontName','Arial','FontSize',11) 

 % Set legend
       legend1 =  legend( [p_zemp p_wouter p_srocc p_hugo], {'Zemp et al. (2019/2020)','Wouters et al. (2019)','SROCC','Hugonnet et al. (2021)'});
       set(legend1, 'FontName','Arial','FontSize',9)
        
 

 %%  Print figure (uncommet to create files)
fig1=gcf;
% Figure as eps to be customized
set(fig1,'PaperUnits','centimeters');
set(fig1,'PaperSize',[figSize(3) figSize(4)]);
set(fig1,'PaperPosition',[0. 0. figSize(3) figSize(4)]);
%Figure as eps
print(fig1,'-depsc',[path_to_figure_folder, 'OUTPUT_FIGURE\',figure_filename])
%Figure as pdf
print(fig1,'-dpdf',[path_to_figure_folder, 'OUTPUT_FIGURE\',figure_filename])
display('Figure printed as eps & pdf')
