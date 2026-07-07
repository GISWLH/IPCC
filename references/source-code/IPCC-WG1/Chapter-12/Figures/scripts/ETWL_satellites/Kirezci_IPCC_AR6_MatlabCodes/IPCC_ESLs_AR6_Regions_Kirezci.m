% IPCC_ESLs_AR6_regions_Kirezci.m
% Processing code for Figure SM 12.6 in the IPCC Working Group I Contribution to the Sixth Assessment Report: Chapter 12

% Computes regional averages of extreme sea level (ESL) for the AR6 regions from the Kirezci et al (2020) dataset (Kirezci, E., Young, I.R., Ranasinghe, R. et al. Projections of global-scale extreme sea levels and resulting episodic coastal flooding over the 21st Century. Sci Rep 10, 11629 (2020). https://doi.org/10.1038/s41598-020-67736-6). ESL data from Kirezci et al (2020) are stored as values per segment of coastline, and here the weighted mean of these coastline lengths per AR6 region is calculated. The 5th (lo), 50th (ce) and 95th (up) percentile estimates of the extreme sea level are available. In chapter 12 we use the the ce estimate as the median value(dots) in Figure S12.6 and the uncertainty bars span from the 5th to 95th percentiles.

% Inputs required are the files ESLs and Coastlines_Table_newAR6.mat which are archived here alongside the code.

% Creator: Ebru Kirezci (e.kirezci@unimelb.edu.au)


clc
clear all

cd('C:\Users\username\Desktop\IPCC AR6 ESL Figures\IPCC_AR6_MatlabCodes')
load('C:\Users\username\Desktop\IPCC AR6 ESL Figures\IPCC_AR6_MatlabCodes\ESLs')
load('C:\Users\username\Desktop\IPCC AR6 ESL Figures\IPCC_AR6_MatlabCodes\Coastlines_Table_newAR6.mat')

CoastlinestablenewAR6.Input_FID=CoastlinestablenewAR6.Input_FID+1;
FID=CoastlinestablenewAR6.Input_FID;

%present

ESLs_present=[FID lo_ESL_present(FID,3) mean_ESL_present(FID,3) u_ESL_present(FID,3)];
    
%2050

ESLs_SLR45_2050=[FID lo_ESL_SLR45_2050(FID,3)  mean_ESL_SLR45_2050(FID,3)  u_ESL_SLR45_2050(FID,3)];
                 
ESLs_SLR85_2050=[FID lo_ESL_SLR85_2050(FID,3) mean_ESL_SLR85_2050(FID,3)  u_ESL_SLR85_2050(FID,3)];
                 
%2100

ESLs_SLR45_2100=[FID lo_ESL_SLR45_2100(FID,3) mean_ESL_SLR45_2100(FID,3) u_ESL_SLR45_2100(FID,3)];
                 
ESLs_SLR85_2100=[FID lo_ESL_SLR85_2100(FID,3) mean_ESL_SLR85_2100(FID,3) u_ESL_SLR85_2100(FID,3)];
    
CoastlinestablenewAR6.Name = categorical(CoastlinestablenewAR6.Name);
[G,Regions]=findgroups(CoastlinestablenewAR6.Name);
                 
for k=2:4
W_Mean_ESLs_present(:,k-1)=splitapply(@sum,(ESLs_present(:,k).*CoastlinestablenewAR6.LENGTH./CoastlinestablenewAR6.LENGTH1),G);
end

%%% 2050 SLR45
for k=2:4
W_Mean_ESLs_SLR45_2050(:,k-1)=splitapply(@sum,(ESLs_SLR45_2050(:,k).*CoastlinestablenewAR6.LENGTH./CoastlinestablenewAR6.LENGTH1),G);
end


%%% 2050 SLR85
for k=2:4
W_Mean_ESLs_SLR85_2050(:,k-1)=splitapply(@sum,(ESLs_SLR85_2050(:,k).*CoastlinestablenewAR6.LENGTH./CoastlinestablenewAR6.LENGTH1),G);
end


%%% 2100 SLR45
for k=2:4
W_Mean_ESLs_SLR45_2100(:,k-1)=splitapply(@sum,(ESLs_SLR45_2100(:,k).*CoastlinestablenewAR6.LENGTH./CoastlinestablenewAR6.LENGTH1),G);
end



%%% 2050 SLR85
for k=2:4
W_Mean_ESLs_SLR85_2100(:,k-1)=splitapply(@sum,(ESLs_SLR85_2100(:,k).*CoastlinestablenewAR6.LENGTH./CoastlinestablenewAR6.LENGTH1),G);
end


%%

Table_Names={'lo_ESL','ce_ESL','up_ESL'};

W_Mean_ESLs_present=array2table(W_Mean_ESLs_present,'VariableNames',Table_Names);
W_Mean_ESLs_SLR45_2050=array2table(W_Mean_ESLs_SLR45_2050,'VariableNames',Table_Names);
W_Mean_ESLs_SLR85_2050=array2table(W_Mean_ESLs_SLR85_2050,'VariableNames',Table_Names);
W_Mean_ESLs_SLR45_2100=array2table(W_Mean_ESLs_SLR45_2100,'VariableNames',Table_Names);
W_Mean_ESLs_SLR85_2100=array2table(W_Mean_ESLs_SLR85_2100,'VariableNames',Table_Names);


W_Mean.ESLs_present=addvars(W_Mean_ESLs_present,Regions,'Before','lo_ESL');

W_Mean.ESLs_SLR45_2050=addvars(W_Mean_ESLs_SLR45_2050,Regions,'Before','lo_ESL');

W_Mean.ESLs_SLR85_2050=addvars(W_Mean_ESLs_SLR85_2050,Regions,'Before','lo_ESL');

W_Mean.ESLs_SLR45_2100=addvars(W_Mean_ESLs_SLR45_2100,Regions,'Before','lo_ESL');

W_Mean.ESLs_SLR85_2100=addvars(W_Mean_ESLs_SLR85_2100,Regions,'Before','lo_ESL');


clearvars  -except W_Mean 

