% IPCC AR6 - Chapter 5
% CumC vs warming 
% Author: Joeri Rogelj, j.rogelj@imperial.ac.uk

% set parent folder
startfolder = cd;
pfolder = [startfolder '\Transfer_data_Ch5FGD'];

CtoCO2_conv = 3.664;

%% assessed human induced warming between 1850-1900 and 2010-2019
AR6_HIW = 1.07; %°C
AR6_HIW_range = [0.8 1.3]; %°C
AR6_HIW_colour = [255,127,80]/255;

%% 
AR6_scen_colour.SSP119 = [30 150 132]/256;
AR6_scen_colour.SSP126 = [29 51 84]/256;
AR6_scen_colour.SSP245 = [234 221 61]/256;
AR6_scen_colour.SSP370 = [242 17 17]/256;
AR6_scen_colour.SSP585 = [132 11 34]/256;

%% assessed TCRE
AR6_TCRE = [1.0 2.3]; % °C/EgC

%% CMIP6 TAS, diagnosed C, and ScenarioMIP LU CO2

CMIP6_tas_folder = [pfolder '\CMIP6_GSAT_Liddicoat'];
CMIP6_C_folder = [pfolder '\CMIP6_DiagnosedEmissions_Liddicoat'];
CMIP6_LUC_folder = [pfolder '\CMIP6_emissiondata'];
CMIP6_tas_files = {'global_mean_TAS_K_HistoricalSsp119'
    'global_mean_TAS_K_HistoricalSsp126'
    'global_mean_TAS_K_HistoricalSsp245'
    'global_mean_TAS_K_HistoricalSsp370'
    'global_mean_TAS_K_HistoricalSsp585'};
CMIP6_C_files = {'ffEmsHistoricalSsp119_GtCyr.txt'
    'ffEmsHistoricalSsp126_GtCyr.txt'
    'ffEmsHistoricalSsp245_GtCyr.txt'
    'ffEmsHistoricalSsp370_GtCyr.txt'
    'ffEmsHistoricalSsp585_GtCyr.txt'};
CMIP6_scen_IDs = {'SSP119'
    'SSP126'
    'SSP245'
    'SSP370'
    'SSP585'};
CMIP6_LUC_file = 'SSP_ScenarioMIP_LU_CO2.xlsx';

for i = 1:length(CMIP6_tas_files)
        
    CMIP6_TAS.(CMIP6_scen_IDs{i}) = readtable(fullfile(CMIP6_tas_folder,CMIP6_tas_files{i}));
    
end


for i = 1:length(CMIP6_C_files)
        
    DiagnosedC.(CMIP6_scen_IDs{i}) = readtable(fullfile(CMIP6_C_folder,CMIP6_C_files{i})); 
    % unit = PgC
    DiagnosedC.unit = 'PgC/yr';
end
     
% express warming relative to 2010-2019
for i = 1:length(CMIP6_scen_IDs)
    
    yr_vector = CMIP6_TAS.(CMIP6_scen_IDs{i}){:,1};
    CMIP6_refperiod_yr_ID = yr_vector>=2010 & yr_vector<=2019;
    cur_TAS = CMIP6_TAS.(CMIP6_scen_IDs{i}){:,2:end-1};
    CMIP6_TAS_data_recentoffset = mean(cur_TAS(CMIP6_refperiod_yr_ID,:),1);
    CMIP6_TAS_rel2010_2019.(CMIP6_scen_IDs{i}) = cur_TAS - repmat(CMIP6_TAS_data_recentoffset,size(cur_TAS,1),1);

end

CMIP6_TAS.years = yr_vector;
CMIP6_TAS_rel2010_2019.years = yr_vector;

% add orginal SSP land-use CO2 emissions
% read SSP data
[SSP_LUC_data,SSP_LUC_txt] = xlsread(fullfile(CMIP6_LUC_folder,CMIP6_LUC_file)); 

% assign data to scenario
SSP_LUC.years = SSP_LUC_data(1,:);
SSP_LUC.data.SSP119 = SSP_LUC_data(3,:);
SSP_LUC.data.SSP126 = SSP_LUC_data(4,:);
SSP_LUC.data.SSP245 = SSP_LUC_data(5,:);
SSP_LUC.data.SSP370 = SSP_LUC_data(2,:);
SSP_LUC.data.SSP585 = SSP_LUC_data(6,:);

SSP_LUC.label.SSP119 = SSP_LUC_txt(3,2);
SSP_LUC.label.SSP126 = SSP_LUC_txt(4,2);
SSP_LUC.label.SSP245 = SSP_LUC_txt(5,2);
SSP_LUC.label.SSP370 = SSP_LUC_txt(2,2);
SSP_LUC.label.SSP585 = SSP_LUC_txt(6,2);

SSP_LUC.unit = 'MtCO2/yr';

% cumulate C from 2015 onward

for i = 1:length(CMIP6_scen_IDs)
    
    yr_vector = DiagnosedC.(CMIP6_scen_IDs{i}){:,1};
    cur_diagnosed_emis = DiagnosedC.(CMIP6_scen_IDs{i}){:,2:end-1};
    Diagnosed_cumC.(CMIP6_scen_IDs{i}) = cumsum(cur_diagnosed_emis,1);
    Diagnosed_cumC_from2015.(CMIP6_scen_IDs{i}) = cumsum(cur_diagnosed_emis(yr_vector>=2015,:),1);
    
    % add LUC and cumulate again
    LUC_addition = repmat(interp1(SSP_LUC.years,SSP_LUC.data.(CMIP6_scen_IDs{i}),2015:2100)',1,size(cur_diagnosed_emis,2));
    % convert from MtCO2/yr to PgC/yr
    LUC_addition = LUC_addition/(CtoCO2_conv*1000);
    
    cur_diagnosed_and_LUC_emis_from2015 = cur_diagnosed_emis(yr_vector>=2015,:) + LUC_addition; 
    Diagnosed_and_LUC_cumC_from2015.(CMIP6_scen_IDs{i}) = cumsum(cur_diagnosed_and_LUC_emis_from2015,1);

end

Diagnosed_and_LUC_cumC_from2015.years = yr_vector;

%% Read ScenarioMIP SSP emissions total CO2

ScenMIP_SSP_folder = [pfolder '\CMIP6_emissiondata'];
ScenMIP_CO2tot_file = 'ScenarioMIP_SSP_emissions_iamc_db_SPMselection.xlsx';

[ScenMIP_num,ScenMIP_txt,~] = xlsread(fullfile(ScenMIP_SSP_folder, ScenMIP_CO2tot_file),'data');

ScenMIP.yr = ScenMIP_num(1,:);
ScenMIP.CO2tot = ScenMIP_num(2:end,:)/1000; % converted to GtCO2
ScenMIP.labels = ScenMIP_txt(2:end,2);

% interpolate
ScenMIP.yr_interp = ScenMIP.yr(1):ScenMIP.yr(end);
ScenMIP.CO2tot_interp = interp1(ScenMIP.yr,ScenMIP.CO2tot',ScenMIP.yr_interp)';

% cumulate
ScenMIP.cumCO2tot_interp = cumsum(ScenMIP.CO2tot_interp,2);

%% AR6 assessed GSAT ranges
AR6_SSPassessedGSATproj_folder = [pfolder '\Constrained GSAT - Ch4\FGD'];
AR6_SSPassessedGSATproj_files = {'assessed_ssp119'
    'assessed_ssp126'
    'assessed_ssp245'
    'assessed_ssp370'
    'assessed_ssp585'};

clear AR6_SSPassessedGSATproj_data

for i = 1:length(AR6_SSPassessedGSATproj_files)
    
    tempdat_GSAT = readtable(fullfile(AR6_SSPassessedGSATproj_folder,[AR6_SSPassessedGSATproj_files{i} '_central.csv']),...
        'Format','%{yyyy-MM-dd}D %f','Delimiter',',','ReadVariableNames',true);
    tempdat_GSAT_lower = readtable(fullfile(AR6_SSPassessedGSATproj_folder,[AR6_SSPassessedGSATproj_files{i} '_05.csv']),...
        'Format','%{yyyy-MM-dd}D %f','Delimiter',',','ReadVariableNames',true);   
    tempdat_GSAT_higher = readtable(fullfile(AR6_SSPassessedGSATproj_folder,[AR6_SSPassessedGSATproj_files{i} '_95.csv']),...
        'Format','%{yyyy-MM-dd}D %f','Delimiter',',','ReadVariableNames',true);
    
    AR6_SSPassessedGSATproj_data.(CMIP6_scen_IDs{i}).med = tempdat_GSAT{:,2};
    AR6_SSPassessedGSATproj_data.(CMIP6_scen_IDs{i}).lower = tempdat_GSAT_lower{:,2};
    AR6_SSPassessedGSATproj_data.(CMIP6_scen_IDs{i}).higher = tempdat_GSAT_higher{:,2};
    
end
    
AR6_SSPassessedGSATproj_data.yr = year(tempdat_GSAT{1,1}):year(tempdat_GSAT{end,1});

% express warming relative to 2010-2019
% info from Sebastian: Data format: 
% Everything is relative to 1995–2014. Assessed GSAT is reported for
% running 20-year means. The first time step in the files corresponds to
% 2000–2019, the last time step to the period 2081–2100. The time axis in
% the netcdf files gives the central year rounded up to the next year.
% Ignore the month and day. 

% The sixth (6) datapoint in this data set thus provides the projection for the 
% 2005-2024 period, and therewith the best match with the 10-yr period of
% 2010-2019 base period of this figure 

clear AR6_SSPassessedGSAT_data_figrange 

for i = 1:length(AR6_SSPassessedGSATproj_files)
    
    AR6_SSPassessedGSAT_data_figrange.(CMIP6_scen_IDs{i}).med = AR6_SSPassessedGSATproj_data.(CMIP6_scen_IDs{i}).med(6:end);
    AR6_SSPassessedGSAT_data_figrange.(CMIP6_scen_IDs{i}).lower = AR6_SSPassessedGSATproj_data.(CMIP6_scen_IDs{i}).lower(6:end);
    AR6_SSPassessedGSAT_data_figrange.(CMIP6_scen_IDs{i}).higher = AR6_SSPassessedGSATproj_data.(CMIP6_scen_IDs{i}).higher(6:end);
    
end

%% GSAT GWI import
dir_GWI = [pfolder '\Global Warming Index'];
file_GWI = 'AWI_all_Tmean_1850_1900_Quant_SEP19_BEhadCW3_GSAT.xlsx';
sheet_GWI = 'AWI_all_Tmean_1850_1900_Quant_S';

% Read GSAT GWI data
[GWI_num,GWI_str,~] = xlsread(fullfile(dir_GWI,file_GWI),sheet_GWI);

obs_unc_color = [238,134,64]/255; 

% average onto annual values
avyr_tags = floor(GWI_num(:,2)); 

GWI_annual_data = [];
GWI_annual_unc_low = [];
GWI_annual_unc_high = [];
GWI_annual_yr = [];

for i = min(avyr_tags):max(avyr_tags)
   
    curyr_ID = avyr_tags==i; 
    
    GWI_annual_data = [GWI_annual_data mean(GWI_num(curyr_ID,4))];
    GWI_annual_unc_low = [GWI_annual_unc_low mean(GWI_num(curyr_ID,8))];
    GWI_annual_unc_high = [GWI_annual_unc_high mean(GWI_num(curyr_ID,9))];
    
    GWI_annual_yr = [GWI_annual_yr i];
    
end

%% Chapter 2 GSAT estimate
dir_Ch2GSAT = [pfolder '\Assessed hist GSAT'];
file_Ch2GSAT = 'Cross chapter box 2.3 provisional GMST and GSAT series.xlsx';
sheet_Ch2GSAT = 'Sheet1';

% Read GSAT Chapter 2 data
[Ch2GSAT_num,Ch2GSAT_str,~] = xlsread(fullfile(dir_Ch2GSAT,file_Ch2GSAT),sheet_Ch2GSAT);

Ch2GSAT_yr = Ch2GSAT_num(:,1);
Ch2GSAT_vals = Ch2GSAT_num(:,12);

%% historical emissions import
dir_GCP = [pfolder '\GlobalCarbonBudget']; 
file_GCP = 'Global_Carbon_Budget_2019v1.0.xlsx';
sheet_GCP = 'Historical Budget'; 

% Read GCP data
[GCP_num,GCP_str,~] = xlsread(fullfile(dir_GCP,file_GCP),sheet_GCP);

GCP_yr = GCP_num(:,1);
% extract 1850 to 2018
yr_select_ID = GCP_yr>=1850;
GCP_yr = GCP_yr(yr_select_ID);
GCP_FFI = GCP_num(yr_select_ID,2);
GCP_LU = GCP_num(yr_select_ID,3);

% add 2019 values from data received by Julia Pongratz
GCP_FFI(end + 1) = GCP_FFI(end);
GCP_LU(end + 1) = 1.72;
GCP_yr(end + 1) = 2019; 

% cumulate starting from 1875
GCP_CO2_tot = GCP_FFI + GCP_LU; 

GCP_cumCO2_tot = cumsum(GCP_CO2_tot);
GCP_cumCO2_tot_rel1850 = cumsum(GCP_CO2_tot(GCP_yr>=1850)); % start accumulating from 1850 onward
GCP_cumCO2_tot_rel1875 = GCP_cumCO2_tot - GCP_cumCO2_tot(GCP_yr==1874); % set 1874 to zero so emissions start accumulating from 1875 onward

% %% test plot
% figure
% plot(GWI_num(:,2),GWI_num(:,3),'-k','linewidth',0.25)
% hold on
% % original GWI data
% patch([GWI_num(:,2)' fliplr(GWI_num(:,2)')],[(GWI_num(:,4)+GWI_num(:,8))' fliplr((GWI_num(:,4)+GWI_num(:,9))')],obs_unc_color,'facealpha',0.5)
% plot(GWI_num(:,2),GWI_num(:,4),'-k','linewidth',2,'color',obs_unc_color)
% % annualized GWI data
% patch([GWI_annual_yr fliplr(GWI_annual_yr)],[(GWI_annual_data+GWI_annual_unc_low) fliplr((GWI_annual_data+GWI_annual_unc_high))],obs_unc_color,'facealpha',0.5)
% plot(GWI_annual_yr,GWI_annual_data,'--k','linewidth',2,'color',obs_unc_color)
% 
% % Ch2 GSAT estimate
% plot(Ch2GSAT_yr,Ch2GSAT_vals,'-r','linewidth',0.5)

%% CumC vs warming plot
SPM_cumCfig = figure('Position', [100, 100, 700, 450]);

%
edge_alpha = 0;
patch_alpha = 0.2;

% plot historical observations vs historical warming
plot(GCP_cumCO2_tot_rel1850(GCP_yr<=2018)*CtoCO2_conv,Ch2GSAT_vals(Ch2GSAT_yr<=2018),'k','linewidth',0.25)
hold on

% % plot range and central estimate of human induced warming on top 
patch([GCP_cumCO2_tot_rel1850(GCP_yr<=2019)' fliplr(GCP_cumCO2_tot_rel1850(GCP_yr<=2019)')]*CtoCO2_conv,...
    [[GWI_annual_data(GWI_annual_yr<=2019) + GWI_annual_unc_low(GWI_annual_yr<=2019)] ...
    fliplr([GWI_annual_data(GWI_annual_yr<=2019) + GWI_annual_unc_high(GWI_annual_yr<=2019)])],obs_unc_color,'facealpha',patch_alpha)
plot(GCP_cumCO2_tot_rel1850(GCP_yr<=2019)'*CtoCO2_conv,GWI_annual_data(GWI_annual_yr<=2019),'--k','linewidth',2,'color',obs_unc_color)

% add AR6 assessed HIW since 1850-1900
plot([1 1]*GCP_cumCO2_tot_rel1850(GCP_yr==2014)*CtoCO2_conv,AR6_HIW_range,'k','linewidth',2,'color',AR6_HIW_colour)
plot(GCP_cumCO2_tot_rel1850(GCP_yr==2014)*CtoCO2_conv,AR6_HIW,'ok','linewidth',2,'color',AR6_HIW_colour)

% plot AR6 TCRE assessment cone
x_GtCO2_conelim = 1500*CtoCO2_conv; % GtC
TCRE_xvals = GCP_cumCO2_tot_rel1850(GCP_yr==2014) + [0 x_GtCO2_conelim x_GtCO2_conelim]; % GtC
TCRE_yvals = AR6_HIW + [0 AR6_TCRE(1)*x_GtCO2_conelim/1000 AR6_TCRE(2)*x_GtCO2_conelim/1000];
patch(TCRE_xvals*CtoCO2_conv,TCRE_yvals,[0 0 0],'edgealpha',0.25,'facealpha',0.25)

% plot AR6 assessed GSAT ranges
SSPs2plot = {'SSP119'
    'SSP126'
    'SSP245'
    'SSP370'
    'SSP585'};

for i = length(SSPs2plot):-1:1
    
    % plot central line
    CO2_yrs2plot_ID = ScenMIP.yr_interp>=2015 & ScenMIP.yr_interp<=2091;
    plot((GCP_cumCO2_tot_rel1850(GCP_yr==2014)*CtoCO2_conv + ScenMIP.cumCO2tot_interp(i,CO2_yrs2plot_ID)), ...
        AR6_HIW + AR6_SSPassessedGSAT_data_figrange.(CMIP6_scen_IDs{i}).med - AR6_SSPassessedGSAT_data_figrange.(CMIP6_scen_IDs{i}).med(1),'k','linewidth',2,'color',AR6_scen_colour.(SSPs2plot{i}))
    % plot decadal markers
    % mark specific years with O 
    markeryears = [2020 2050];
    markerstypes = {'o-k','x-k'};
    for j = 1:length(markeryears)
        [~,yrs2plot_ID,~] = intersect(ScenMIP.yr_interp,[markeryears(j)]);
        AssessedGSAT_yr_ID = markeryears(j) - 2015 + 1; % first data point in AR6_SSPassessedGSAT_data_figrange corresponds to 2005-2024 period (central 2015)
        plot((GCP_cumCO2_tot_rel1850(GCP_yr==2014)*CtoCO2_conv + ScenMIP.cumCO2tot_interp(i,yrs2plot_ID)), ...
            AR6_HIW + AR6_SSPassessedGSAT_data_figrange.(CMIP6_scen_IDs{i}).med(AssessedGSAT_yr_ID) ...
            - AR6_SSPassessedGSAT_data_figrange.(CMIP6_scen_IDs{i}).med(1),markerstypes{j},'color',AR6_scen_colour.(SSPs2plot{i}))
    end

    % plot separate patch for positive and negative values
    if any(ScenMIP.CO2tot_interp(i,:)<0)
        % positive branch
        posCO2_orig_yr_ID = ScenMIP.CO2tot_interp(i,:)>=0;
        posCO2_orig_yrs = ScenMIP.yr_interp(posCO2_orig_yr_ID);
        posCO2_yrs2plot = intersect(ScenMIP.yr_interp(CO2_yrs2plot_ID),posCO2_orig_yrs);
        [~,posCO2_plot_yr_ID,~] = intersect(ScenMIP.yr_interp,posCO2_yrs2plot);
        
        % for all positive CO2 emission values (cumCO2 is increasing)
        patch(GCP_cumCO2_tot_rel1850(GCP_yr==2014)*CtoCO2_conv + ...
            [ScenMIP.cumCO2tot_interp(i,posCO2_plot_yr_ID) fliplr(ScenMIP.cumCO2tot_interp(i,posCO2_plot_yr_ID))],...
            [(AR6_HIW + AR6_SSPassessedGSAT_data_figrange.(CMIP6_scen_IDs{i}).lower(posCO2_plot_yr_ID) ...
            - AR6_SSPassessedGSAT_data_figrange.(CMIP6_scen_IDs{i}).med(1))' ...
            fliplr((AR6_HIW + AR6_SSPassessedGSAT_data_figrange.(CMIP6_scen_IDs{i}).higher(posCO2_plot_yr_ID) ...
            - AR6_SSPassessedGSAT_data_figrange.(CMIP6_scen_IDs{i}).med(1))')],...
            AR6_scen_colour.(SSPs2plot{i}),'edgealpha',patch_alpha,'facealpha',patch_alpha)
        
        % negative branch
        negCO2_orig_yr_ID = ScenMIP.CO2tot_interp(i,:)<0;
        negCO2_orig_yrs = ScenMIP.yr_interp(negCO2_orig_yr_ID);
        negCO2_yrs2plot = intersect(ScenMIP.yr_interp(CO2_yrs2plot_ID),negCO2_orig_yrs);
        [~,negCO2_plot_yr_ID,~] = intersect(ScenMIP.yr_interp,negCO2_yrs2plot);
        
        % for all negatiev CO2 emission values (cumCO2 is decreasing)
        patch(GCP_cumCO2_tot_rel1850(GCP_yr==2014)*CtoCO2_conv + ...
            [ScenMIP.cumCO2tot_interp(i,negCO2_plot_yr_ID) fliplr(ScenMIP.cumCO2tot_interp(i,negCO2_plot_yr_ID))],...
            [(AR6_HIW + AR6_SSPassessedGSAT_data_figrange.(CMIP6_scen_IDs{i}).lower(negCO2_plot_yr_ID) ...
            - AR6_SSPassessedGSAT_data_figrange.(CMIP6_scen_IDs{i}).med(1))' ...
            fliplr((AR6_HIW + AR6_SSPassessedGSAT_data_figrange.(CMIP6_scen_IDs{i}).higher(negCO2_plot_yr_ID) ...
            - AR6_SSPassessedGSAT_data_figrange.(CMIP6_scen_IDs{i}).med(1))')],...
            AR6_scen_colour.(SSPs2plot{i}),'edgealpha',patch_alpha,'facealpha',patch_alpha)
        
    else
        patch(GCP_cumCO2_tot_rel1850(GCP_yr==2014)*CtoCO2_conv + ...
            [ScenMIP.cumCO2tot_interp(i,CO2_yrs2plot_ID) fliplr(ScenMIP.cumCO2tot_interp(i,CO2_yrs2plot_ID))],...
            [(AR6_HIW + AR6_SSPassessedGSAT_data_figrange.(CMIP6_scen_IDs{i}).lower(CO2_yrs2plot_ID) ...
            - AR6_SSPassessedGSAT_data_figrange.(CMIP6_scen_IDs{i}).med(1))' ...
            fliplr((AR6_HIW + AR6_SSPassessedGSAT_data_figrange.(CMIP6_scen_IDs{i}).higher(CO2_yrs2plot_ID) ...
            - AR6_SSPassessedGSAT_data_figrange.(CMIP6_scen_IDs{i}).med(1))')],...
            AR6_scen_colour.(SSPs2plot{i}),'edgealpha',patch_alpha,'facealpha',patch_alpha)
    end
end

% plot CMIP6 SSP results
for i = length(SSPs2plot):-1:1
    plot((GCP_cumCO2_tot_rel1850(GCP_yr==2014) + ...
        Diagnosed_and_LUC_cumC_from2015.(CMIP6_scen_IDs{i}))*CtoCO2_conv, ...
        AR6_HIW + CMIP6_TAS_rel2010_2019.(CMIP6_scen_IDs{i})(CMIP6_TAS_rel2010_2019.years>=2015,:),'k',...
        'color',AR6_scen_colour.(SSPs2plot{i}),'linewidth',0.25)
end

x_axis_lims = [0 GCP_cumCO2_tot_rel1850(GCP_yr==2014)*CtoCO2_conv + x_GtCO2_conelim];
xlim(x_axis_lims)
xlabel('Cum carbon emissions since 1850 [GtCO2]')
ylabel('Global mean temperature increase since 1850-1900 [°C - GSAT]')
box off
% grid on

% add second axis on top
ax1 = gca;
ax1_pos = ax1.Position; % position of first axes
ax2 = axes('Position',ax1_pos,...
    'XAxisLocation','top',...
    'YAxisLocation','right',...
    'Color','none',...
    'Ytick',[]);
xlim(x_axis_lims/CtoCO2_conv)
xlabel('Cum carbon emissions since 1850 [PgC]')
