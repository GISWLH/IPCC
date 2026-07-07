%%% ch02_fig2_plotting_code.m

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%                                                                                                        %%%
%%%  DESCRIPTION                                                                                           %%%
%%%                                                                                                        %%%    
%%%  This is a Matlab script to produce IPCC AR6 WG-I Figure 2.8                                           %%%
%%%  Creator: Owen R. Cooper, Senior Research Scientist, CIRES, University of Colorado Boulder             %%%  
%%%  Last updated on November 4, 2020                                                                      %%%                                                                     
%%%                                                                                                        %%%
%%%  The script simply plots the decadal ozone trends reported by several publications in the              %%%
%%%  peer-reviewed literature.  All trend values are found in the script below and no other files are      %%%
%%%  required to generate the plots.                                                                       %%%
%%%                                                                                                        %%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%  Information on the version of Matlab used to produce the figure 
%%% ----------------------------------------------------------------------------------------------------
%%% MATLAB Version: 8.6.0.267246 (R2015b)
%%% Operating System: Linux 2.6.32-754.27.1.el6.x86_64 #1 SMP Wed Jan 8 05:56:42 EST 2020 x86_64
%%% Java Version: Java 1.7.0_60-b19 with Oracle Corporation Java HotSpot(TM) 64-Bit Server VM mixed mode
%%% ----------------------------------------------------------------------------------------------------




clear
format short g

%%% Data for panel (a)
%%% list decadal ozone trends for the 27 remote surface sites reported by   
%%% Cooper et al., 2020, including the dry and moist subsets at Mauna Loa
%%%
%%% Cooper, O. R., M. G. Schultz, S. Schröder, K.-L. Chang, A. Gaudel, G. Carbajal Benítez, E. Cuevas,
%%% M. Fröhlich, I. E. Galbally, D. Kubistin, X. Lu, A. McClure-Begley, S. Molloy, P. Nédélec, 
%%% J. O’Brien, S. J. Oltmans, I. Petropavlovskikh, L. Ries, I. Senik, K. Sjöberg, S. Solberg, 
%%% T. G. Spain, W. Spangl, M. Steinbacher, D. Tarasick, V. Thouret, X. Xu (2020), Multi-decadal 
%%% surface ozone trends at globally distributed remote locations, Elem Sci Anth, 8(1), p.23 
%%% DOI: http://doi.org/10.1525/elementa.420
%%%
%%%     site_number  latitude   longitude     elevation      slope      p-value  
surface_slope_decade=[
            1         82.5        -62.5          210         -0.5         0.29  %% 'Alert'
            2         78.9         11.9          474          0.3         0.52  %% 'Zeppelin'
            3         71.3       -156.6           11          0.8         0.08  %% 'Barrow'
            4         67.9         21.1          524            0         0.92  %% 'Esrange'
            5         65.8         13.9          439         -0.6         0.12  %% 'Tustervatn'
            6         63.7         -149          663          0.7         0.14  %% 'Denali'
            7         57.7         -4.8          266         -0.4         0.42  %% 'Strath_Vaich_Dam'
            8         53.3         -9.9            5          0.7         0.08  %% 'Mace_Head'
            9         47.4           11         2800         -0.8            0  %% 'Zugspitze'
           10         47.1           13         3106           -1            0  %% 'Sonnblick'
           11         46.5            8         3580          0.2         0.45  %% 'Jungfraujoch'
           12         43.7         42.7         2096         -1.1         0.17  %% 'Kislovodsk'
           13         41.4       -106.2         3175         -1.5         0.01  %% 'Centennial'
           14           39       -114.2         2058          0.2         0.67  %% 'Great_Basin'
           15           39         -107         2915         -1.9            0  %% 'Gothic'
           16         36.3        100.9         3810          1.7            0  %% 'Mt_Waliguan'
           17         36.1       -112.2         2073         -1.5            0  %% 'Grand_Canyon'
           18         28.3        -16.5         2367          0.5         0.28  %% 'Izana'
           19         24.3          154            8         -0.4         0.35  %% 'Minamitorishima' 
           20         19.5       -155.6         3397          0.9          0.2  %% 'Mauna_Loa_(all)' 
           21         19.5       -155.6         3397          2.4            0  %% 'Mauna_Loa_(dry)'
           22         19.5       -155.6         3397          0.6         0.16  %% 'Mauna_Loa_(moist)'
           23        -14.3       -171.6           42          1.5            0  %% 'American_Samoa'
           24        -34.4         18.5          230          1.2            0  %% 'Cape_Point_(onshore_flow)'
           25        -40.7        144.7           94          0.3         0.08  %% 'Cape_Grim'
           26        -54.8        -68.3           18         -0.9            0  %% 'Ushuaia'
           27        -70.7         -8.3           42            1            0  %% 'Neumayer'
           28          -90           59         2840          1.5            0  %% 'South_Pole'
           32        -30.2        -70.8         2220          0.2         0.52  %% 'El_Tololo'
];


%%% Data for panel (a)
%%% List the decadal ozone trend for onshore transport conditions at the Hok Tsui surface site  
%%% south of Hong Kong, as reported by Wang et al. [2019] 
%%%
%%% Wang, T., Dai, J., Lam, K.S., Nan Poon, C., Brasseur, G.P., 2019. Twenty-Five Years of Lower Tropospheric 
%%% Ozone Observations in Tropical East Asia: The Influence of Emissions and Weather Patterns. 
%%% Geophys. Res. Lett. https://doi.org/10.1029/2019GL084459
%%%
%%% Hok Tsui
%%% latitude, longitude, altitude
map_site_info_other =[
22.2    114.3      60
 ];

other_slope_decade=[
3.6             %% p=0.00
];



%%% Data for panel (a)
%%% List the decadal ozone trends for the 11  
%%% IAGOS regions at 650 hPa, reported by Gaudel et al. [2020] 
%%%
%%% Gaudel, A., O. R. Cooper, K.-L. Chang, I. Bourgeois, J. R. Ziemke, S. A. Strode, L. D. Oman, 
%%% P. Sellitto, P. Nédélec, R. Blot, V. Thouret, C. Granier (2020), Aircraft observations since 
%%% the 1990s reveal increases of tropospheric ozone at multiple locations across the Northern 
%%% Hemisphere. Sci. Adv. 6, eaba8272, DOI: 10.1126/sciadv.aba8272
%%%
%%% western Europe
%%% NE USA
%%% Persian Gulf 
%%% India
%%% SE Asia
%%% Malaysia/Indonesia
%%% China/Korea
%%% SE USA
%%% northern S. America (600 hPa)
%%% Gulf of Guinea, Africa
%%% western North America

%%% latitude, longitude, altitude
map_site_info_iagos =[
51      7.5      3600
41      -75      3600
26       52      3600
20       78      3600		     
16      104      3600
 0      107      3600
39      118      3600
33      -91      3600
7.5     -70      4200
5.5     5.5      3600
45     -124      3600
 ];

iagos_slope_decade=[
1.1              %% p<0.01
1.2              %% p<0.01
3.9              %% p<0.01
3.2              %% p=0.01
6.3              %% p<0.01
4.9              %% p<0.01
2.3              %% p<0.01
0.5              %% p=0.14
0.5              %% p=0.33
2.7              %% p=0.00
1.3              %% p=0.01
];


%%% Data for panel (b)
%%% List the decadal ozone trends for the 11  
%%% IAGOS regions at 700-300 hPa, reported by Gaudel et al. [2020] 
%%%
%%% Gaudel, A., O. R. Cooper, K.-L. Chang, I. Bourgeois, J. R. Ziemke, S. A. Strode, L. D. Oman, 
%%% P. Sellitto, P. Nédélec, R. Blot, V. Thouret, C. Granier (2020), Aircraft observations since 
%%% the 1990s reveal increases of tropospheric ozone at multiple locations across the Northern 
%%% Hemisphere. Sci. Adv. 6, eaba8272, DOI: 10.1126/sciadv.aba8272
%%%
%%% Also list the decadal mid-tropospheric ozone trend at Hilo, Hawaii from Chang et al., 2020
%%% The mean altitude for these observations is set at 5500 m.
%%%
%%% Chang, K.-L., O. R. Cooper, A. Gaudel, I. Petropavlovskikh and V. Thouret (2020), Statistical 
%%% regularization for trend detection: An integrated approach for detecting long-term trends from 
%%% sparse tropospheric ozone profiles, Atmos. Chem. Phys., 20, 9915–9938, 
%%% https://doi.org/10.5194/acp-20-9915-2020
%%%
%%% Europe
%%% NE USA
%%% Persian Gulf 
%%% India
%%% SE Asia
%%% Malaysia/Indonesia
%%% China/Korea
%%% SE USA
%%% northern S. America (600 hPa)
%%% Gulf of Guinea, Africa
%%% western North America
%%% Hilo, Hawaii

%%% latitude, longitude, altitude
map_site_info_midtrop =[
51        7.5    5500
41      -75      5500
26       52      5500
20       78      5500		     
16      104      5500
 0      107      5500
39      118      5500
33      -91      5500
7.5     -70      5500
5.5     5.5      5500
45     -124      5500
20     -156      5500
 ];

iagos_midtrop_slope_decade=[
1.3              %% p<0.01
1.7              %% p<0.01
3.0              %% p<0.01
3.6              %% p<0.01
5.6              %% p<0.01
3.5              %% p<0.01
1.7              %% p<0.01
1.3              %% p<0.01
1.5              %% p<0.01
1.2              %% p=0.07
2.8              %% p<0.01
0.64             %% p=0.35
];


%%% Data for panel (b)
%%% List the decadal ozone trends for the 7
%%% IAGOS regions in the upper troposphere, from Cohen et al. [2018] 
%%%
%%% Cohen, Y., et al. (2018), Climatology and long-term evolution of ozone and carbon monoxide 
%%% in the upper troposphere-lower stratosphere (UTLS) at northern midlatitudes, as seen by IAGOS 
%%% from 1995 to 2013, Atmos. Chem. Phys., 18, 5415-5453, https://doi.org/10.5194/acp-18-5415-2018, 2018.

%%% Eastern USA
%%% North Atlantic
%%% Europe
%%% Western Mediterranean 
%%% Middle East
%%% Siberia
%%% Northeast Asia

%%% latitude, longitude, altitude
map_site_info_uppertrop =[
43    -75       12000
55    -35       12000
50      0       12000
40      5       12000		     
40     40       12000
58     80       12000
40    125       12000
 ];

iagos_uppertrop_slope_decade=[
3.4              %% p=0.01
2.4              %% p=0.07, personal communication from lead-author Y. Cohen on December 19, 2019
3.1              %% p<0.01
4.2              %% p<0.01
2.5              %% p=0.04
3.7              %% p<0.01
4.5              %% p<0.01
];



%%% Official IPCC AR6 colors, providing a single color scale for use with 
%%% all trend values, whether positive or negative. 
%%% These colors are from palette ssequential_5_r_rgb 
trend_colors=[
              0.6471  0.0588  0.0824       %%% dark red             1
              0.8706  0.1765  0.1490       %%% red                  2
              0.9843  0.4157  0.2902       %%% orange               3
              0.9882  0.6824  0.5686       %%% light orange         4
              0.9843  0.4157  0.2902       %%% orange               5
              0.8706  0.1765  0.1490       %%% red                  6            
              0.6471  0.0588  0.0824       %%% dark red             7            
];





%%%
%%% Panel (a):  Plot the decadal ozone trends for the surface sites and for the IAGOS observations at 650 hPa
%%%

figure(1)
fig1=figure(1)
clf
set(fig1,'PaperOrientation','portrait','PaperUnits','centimeters','PaperPosition',[0 0   11 14  ],'Position',[100 100 420  560])

keep_hi_elev=find(surface_slope_decade(:,4)>1500);
keep_pos_p1=find(surface_slope_decade(:,6)<=0.05 & surface_slope_decade(:,5)>0);
keep_pos_p2=find(surface_slope_decade(:,6)<=0.1  & surface_slope_decade(:,6)>0.05   & surface_slope_decade(:,5)>0);
keep_pos_p3=find(surface_slope_decade(:,6)<=0.34 & surface_slope_decade(:,6)>0.1    & surface_slope_decade(:,5)>0);
keep_p4=find(surface_slope_decade(:,6)>0.34);
keep_neg_p1=find(surface_slope_decade(:,6)<=0.05 & surface_slope_decade(:,5)<0);
keep_neg_p2=find(surface_slope_decade(:,6)<=0.1  & surface_slope_decade(:,6)>0.05   & surface_slope_decade(:,5)<0);
keep_neg_p3=find(surface_slope_decade(:,6)<=0.34 & surface_slope_decade(:,6)>0.1    & surface_slope_decade(:,5)<0);


axes('Units','centimeters','position',[1.7,2.0 ,9, 12   ])
hold on
plot([0 0],[-90 90],'k-','Color',[.3 .3 .3],'LineWidth',[2]);
plot([-3 8  ],[0 0],'k-','LineWidth',[.8],'Color',[.6 .6 .6])
plot([-3 8  ],[23.44 23.44],'k--','LineWidth',[.99],'Color',[.6 .6 .6])
plot([-3 8  ],[-23.44 -23.44],'k--','LineWidth',[.99],'Color',[.6 .6 .6])
plot(iagos_slope_decade, map_site_info_iagos(:,1),'kv','MarkerSize',[11],'LineWidth',[1.5])
plot(surface_slope_decade(keep_hi_elev,5),surface_slope_decade(keep_hi_elev,2),'k^','MarkerSize',[11],'LineWidth',[1.5])

plot(surface_slope_decade(keep_pos_p1,5),surface_slope_decade(keep_pos_p1,2),'k.','Color',trend_colors(7,:),'LineStyle','none','LineWidth',[10],'Marker','.','MarkerSize',[25])
plot(surface_slope_decade(keep_pos_p2,5),surface_slope_decade(keep_pos_p2,2),'k.','Color',trend_colors(6,:),'LineStyle','none','LineWidth',[10],'Marker','.','MarkerSize',[25])
plot(surface_slope_decade(keep_pos_p3,5),surface_slope_decade(keep_pos_p3,2),'k.','Color',trend_colors(5,:),'LineStyle','none','LineWidth',[10],'Marker','.','MarkerSize',[25])

plot(surface_slope_decade(keep_p4,5),surface_slope_decade(keep_p4,2),'k.','Color',trend_colors(4,:),'LineStyle','none','LineWidth',[10],'Marker','.','MarkerSize',[25])

plot(surface_slope_decade(keep_neg_p3,5),surface_slope_decade(keep_neg_p3,2),'k.','Color',trend_colors(3,:),'LineStyle','none','LineWidth',[10],'Marker','.','MarkerSize',[25])
plot(surface_slope_decade(keep_neg_p2,5),surface_slope_decade(keep_neg_p2,2),'k.','Color',trend_colors(2,:),'LineStyle','none','LineWidth',[10],'Marker','.','MarkerSize',[25])
plot(surface_slope_decade(keep_neg_p1,5),surface_slope_decade(keep_neg_p1,2),'k.','Color',trend_colors(1,:),'LineStyle','none','LineWidth',[10],'Marker','.','MarkerSize',[25])

plot(iagos_slope_decade, map_site_info_iagos(:,1),    'k.','Color',trend_colors(7,:),'LineStyle','none','LineWidth',[10],'Marker','.','MarkerSize',[25])
plot(iagos_slope_decade([8 9],1), map_site_info_iagos([8 9],1),    'k.','Color',trend_colors(5,:),'LineStyle','none','LineWidth',[10],'Marker','.','MarkerSize',[25])

plot(other_slope_decade, map_site_info_other(:,1),    'k.','Color',trend_colors(7,:),'LineStyle','none','LineWidth',[10],'Marker','.','MarkerSize',[25])

%%% legend for symbols
plot([3.5],[82 ],'ko','LineWidth',[1.5],'MarkerSize',[7])
plot([3.5],[73.5 ],'k^','LineWidth',[1.5],'MarkerSize',[10])
plot([3.5],[65 ],'kv','LineWidth',[1.5],'MarkerSize',[10])
text(4,82,['low elevation'],'FontSize',[11],'FontName','arial','Color',[0 0 0],'FontWeight','normal')
text(4,73.5,['high elevation'],'FontSize',[11],'FontName','arial','Color',[0 0 0],'FontWeight','normal')
text(4,65,['IAGOS aircraft'],'FontSize',[11],'FontName','arial','Color',[0 0 0],'FontWeight','normal')

%%% legend for p-value colors
plot([2.5 2.5 8 8 ],[-90 -53 -53 -90],'k-','LineWidth',[.8])
shiftx=-.9;  shifty=-57;

plot([4.05]+shiftx  ,[-27.0 ]+shifty,'k.','Color',trend_colors(4,:),'LineStyle','none','LineWidth',[10],'Marker','.','MarkerSize',[25])
plot([3.7 ]+shiftx  ,[-19.0 ]+shifty,'k.','Color',trend_colors(5,:),'LineStyle','none','LineWidth',[10],'Marker','.','MarkerSize',[25])
plot([3.7 ]+shiftx  ,[-11.0 ]+shifty,'k.','Color',trend_colors(6,:),'LineStyle','none','LineWidth',[10],'Marker','.','MarkerSize',[25])
plot([3.7 ]+shiftx  ,[ -3.0 ]+shifty,'k.','Color',trend_colors(7,:),'LineStyle','none','LineWidth',[10],'Marker','.','MarkerSize',[25])
plot([4.3 ]+shiftx  ,[-19.0 ]+shifty,'k.','Color',trend_colors(3,:),'LineStyle','none','LineWidth',[10],'Marker','.','MarkerSize',[25])
plot([4.3 ]+shiftx  ,[-11.0 ]+shifty,'k.','Color',trend_colors(2,:),'LineStyle','none','LineWidth',[10],'Marker','.','MarkerSize',[25])
plot([4.3 ]+shiftx  ,[- 3.0 ]+shifty,'k.','Color',trend_colors(1,:),'LineStyle','none','LineWidth',[10],'Marker','.','MarkerSize',[25])
text(4.7    +shiftx ,-3+shifty,['p <= 0.05'],'FontSize',[11],'FontName','arial','Color',[0 0 0],'FontWeight','normal')
text(4.7    +shiftx ,-11+shifty,['0.05 < p <= 0.10'],'FontSize',[11],'FontName','arial','Color',[0 0 0],'FontWeight','normal')
text(4.7    +shiftx ,-19+shifty,['0.10 < p < 0.34'],'FontSize',[11],'FontName','arial','Color',[0 0 0],'FontWeight','normal')
text(4.7    +shiftx ,-27+shifty,['p >= 0.34'],'FontSize',[11],'FontName','arial','Color',[0 0 0],'FontWeight','normal')

hold off
axis([-3 8   -90 90 ])
xlabel('Ozone trend (ppbv decade^-^1)')
ylabel('Latitude')

text(-1.5, 96,['Surface and lower troposphere'],'FontSize',[12],'FontName','arial','Color',[0 0 0],'FontWeight','normal')

set(gca,'FontSize',[11],'FontWeight','demi','FontName','helvetica','TickLength',[.005 .005],'Color',[1 1 1 ],'XColor',[0 0 0],'YColor',[0 0 0],'YTick',[-90:10:90],'XTick',[-5:1:8],'Box','off','Clipping','off','LineWidth',[1],'TickDir','out');
set(gcf,'InvertHardCopy','off','Color',[1 1 1])

print_name=[ 'IPCC_decadal_trend_for_ozone_at_the_surface_and_lower_troposphere.eps' ];
print('-depsc',print_name)






%%%
%%% Panel (b): Plot ozone trends for the mid-troposphere (700-300 hPa) and the upper troposphere
%%%

figure(2)
fig2=figure(2)
clf
set(fig2,'PaperOrientation','portrait','PaperUnits','centimeters','PaperPosition',[0 0   11 14  ],'Position',[100 100 420  560])

axes('Units','centimeters','position',[1.7,2.0 ,9, 12   ])
hold on
plot([0 0],[-90 65],'k-','Color',[.3 .3 .3],'LineWidth',[2]);
plot([-3 8  ],[0 0],'k-','LineWidth',[.8],'Color',[.6 .6 .6])
plot([-3 8  ],[23.44 23.44],'k--','LineWidth',[.99],'Color',[.6 .6 .6])
plot([-3 8  ],[-23.44 -23.44],'k--','LineWidth',[.99],'Color',[.6 .6 .6])

plot(iagos_midtrop_slope_decade,         map_site_info_midtrop(:,1),       'k.','Color',trend_colors(7,:),'LineStyle','none','LineWidth',[10],'Marker','.','MarkerSize',[25])
plot(iagos_midtrop_slope_decade([10],1), map_site_info_midtrop([10],1),    'k.','Color',trend_colors(6,:),'LineStyle','none','LineWidth',[10],'Marker','.','MarkerSize',[25])
plot(iagos_midtrop_slope_decade([12],1), map_site_info_midtrop([12],1),    'k.','Color',trend_colors(4,:),'LineStyle','none','LineWidth',[10],'Marker','.','MarkerSize',[25])
plot(iagos_midtrop_slope_decade([12],1), map_site_info_midtrop([12],1),    'ks','Color',trend_colors(4,:),'LineStyle','none','LineWidth',[8],'MarkerSize',[6])

plot(iagos_uppertrop_slope_decade,         map_site_info_uppertrop(:,1),       'k^','Color',trend_colors(7,:),'LineStyle','none','LineWidth',[3],'MarkerSize',[8])
plot(iagos_uppertrop_slope_decade(2,1),    map_site_info_uppertrop(2,1),       'k^','Color',trend_colors(6,:),'LineStyle','none','LineWidth',[3],'MarkerSize',[8])

text(-1.0, 96,['Mid- and upper troposphere'],'FontSize',[12],'FontName','arial','Color',[0 0 0],'FontWeight','normal')

plot([-2.5],[84 ],'ko','LineWidth',[1.5],'MarkerSize',[7])
plot([-2.5],[77 ],'k^','LineWidth',[1.5],'MarkerSize',[8])
plot([-2.5],[70 ],'ks','LineWidth',[1.5],'MarkerSize',[9])
text(-2,84,['IAGOS aircraft, mid-trop., 1994-2016'],'FontSize',[10],'FontName','arial','Color',[0 0 0],'FontWeight','normal')
text(-2,77,['IAGOS aircraft, upper trop., 1994-2013'],'FontSize',[10],'FontName','arial','Color',[0 0 0],'FontWeight','normal')
text(-2,70,['Hilo ozonesondes, mid-trop., 1994-2018'],'FontSize',[10],'FontName','arial','Color',[0 0 0],'FontWeight','normal')

hold off
axis([-3 8   -90 90 ])
xlabel('Ozone trend (ppbv decade^-^1)')
%ylabel('Latitude')

set(gca,'FontSize',[11],'FontWeight','demi','FontName','helvetica','TickLength',[.005 .005],'Color',[1 1 1 ],'XColor',[0 0 0],'YColor',[0 0 0],'YTick',[-90:10:90],'XTick',[-5:1:8],'Box','off','Clipping','off','LineWidth',[1],'YTickLabel',[],'TickDir','out');
set(gcf,'InvertHardCopy','off','Color',[1 1 1])


print_name=[ 'IPCC_decadal_trend_for_ozone_in_mid_and_upper_troposphere.eps' ];
print('-depsc',print_name)





%%%
%%%  Panel (c): Plot the decadal tropospheric column ozone trends based on the TOST ozonesonde product and several satellite products
%%%
%%%  TOST ozonesonde product values are reported by: 
%%%  Gaudel, A., et al. (2018), Tropospheric Ozone Assessment Report:  Present-day distribution and trends of tropospheric 
%%%  ozone relevant to climate and global atmospheric chemistry model evaluation, 
%%%  Elem. Sci. Anth., 6(1):39, DOI: https://doi.org/10.1525/elementa.291
%%%
%%%  (Sat1) Tropical satellite ozone trends using the TOR method and based on TOMS and OMI/MLS are reported by:
%%%  Ziemke, J. R., et al. (2019), Trends in Global Tropospheric Ozone Inferred from a Composite Record of TOMS/OMI/MLS/OMPS Satellite 
%%%  Measurements and the MERRA-2 GMI Simulation, Atmos. Chem. Phys., 19, 3257-3269, https://doi.org/10.5194/acp-19-3257-2019
%%%
%%%  Tropical satellite ozone trends are reported by two other studies: 
%%%  (Sat2) Heue, K-P, et al., (2016) Trends of tropical tropospheric ozone from 20 years of European satellite measureÂ­ments and perspectives 
%%%  for the Sentinel-5 Precursor. Atmos. Meas. Tech. 9: 5037-5051. DOI: https://doi. org/10.5194/amt-9-5037-2016
%%%
%%%  (Sat3) Leventidou, E., Weber, M., Eichmann, K.-U., Burrows, J. P., Heue, K.-P., Thompson, A. M., and Johnson, B. J. (2018), Harmonisation 
%%%  and trends of 20-year tropical tropospheric ozone data, Atmos. Chem. Phys., 18, 9189-9205, https://doi.org/10.5194/acp-18-9189-2018.
%%%
%%%  Ozone trends originally reported in units of DU decade-1 are converted to ppbv decade-1 (representing a tropospheric weighted 
%%%  average ozone mixing ratio) using ratios derived from the OMI/MLS satellite record available at:
%%%  https://acd-ext.gsfc.nasa.gov/Data_services/cloud_slice/new_data.html 
%%%
%%%  These conversion ratios for 4 latitude bands are:
%%%  30 - 60 N:  1.71
%%%   0 - 30 N:  1.44
%%%   0 - 30 S:  1.43
%%%  30 - 60 S:  1.61
%%%  These conversion ratios appear in the "plot" lines below and are multiplied against the Dobson decade-1 values to yield ppbv decade-1 values 


figure(3)
fig3=figure(3)
clf
set(fig3,'PaperOrientation','portrait','PaperUnits','centimeters','PaperPosition',[0 0   11 14  ],'Position',[100 100 420  560])

axes('Units','centimeters','position',[1.7,2.0 ,9, 12   ])
hold on
plot([0 0],[-90 90],'k-','Color',[.3 .3 .3],'LineWidth',[2]);
plot([-3 8  ],[0 0],'k-','LineWidth',[.8],'Color',[.6 .6 .6])
plot([-3 8  ],[23.44 23.44],'k--','LineWidth',[.99],'Color',[.6 .6 .6])
plot([-3 8  ],[-23.44 -23.44],'k--','LineWidth',[.99],'Color',[.6 .6 .6])

%% plot the vertical bars
plot([1.7 1.7]*1.71,[30 60],'k-','Color',trend_colors(7,:),'LineWidth',[5])     %% TOST 30-60 N
plot([3.1 3.1]*1.44,[0 30],'k-','Color',trend_colors(7,:),'LineWidth',[5])      %% TOST  0-30 N
plot([4.8 4.8]*1.43,[0 -30],'k-','Color',trend_colors(7,:),'LineWidth',[5])     %% TOST  0-30 S
plot([0.4 0.4]*1.61,[-30 -60],'k-','Color',trend_colors(5,:),'LineWidth',[5])   %% TOST 30-60 S 

plot([2.1 2.1]*1.44,[0  30],'k-','Color',trend_colors(7,:),'LineWidth',[5])     %% TOR (Sat1) 0-30 N
plot([1.2 1.2]*1.43,[0 -30],'k-','Color',trend_colors(7,:),'LineWidth',[5])     %% TOR (Sat1) 0-30 S

plot([0.7 0.7]*1.435,[20 -20],'k-','Color',trend_colors(7,:),'LineWidth',[5])   %% Heue (Sat2) 20S - 20 N
plot([-.2 -.2]*1.435,[15 -15],'k-','Color',trend_colors(4,:),'LineWidth',[5])   %% Leventidou (Sat3) 15 S - 15 N


%% plot the horizontal uncertainty ranges
plot([1.7-0.4 1.7+0.4]*1.71,[45 45],'k-','Color',trend_colors(7,:),'LineWidth',[2])     %% TOST 30-60 N 
plot([3.1-.9  3.1+0.9]*1.44,[16 16],'k-','Color',trend_colors(7,:),'LineWidth',[2])     %% TOST  0-30 N
plot([4.8-0.8 4.8+0.8]*1.43,[-15 -15],'k-','Color',trend_colors(7,:),'LineWidth',[2])   %% TOST  0-30 S
plot([0.4-0.3 0.4+0.3]*1.61,[-45 -45],'k-','Color',trend_colors(5,:),'LineWidth',[2])   %% TOST 30-60 S

plot([2.1-1.2 2.1+1.2]*1.44,[ 13  13], 'k-','Color',trend_colors(7,:),'LineWidth',[2])  %% TOR (Sat1) 0-30 N
plot([1.2-1.1  1.2+1.1]*1.43,[-15 -15],'k-','Color',trend_colors(7,:),'LineWidth',[2])  %% TOR (Sat1) 0-30 S

plot([ 0.7-0.1  0.7+0.1]*1.435,[0 0],'k-','Color',trend_colors(7,:),'LineWidth',[2])    %% Heue (Sat2) 20S - 20 N
plot([-.2-0.6  -.2+0.6 ]*1.435,[0 0],'k-','Color',trend_colors(4,:),'LineWidth',[2])    %% Leventidou (Sat3) 15 S - 15 N


%% add labels to each bar
text(1.5,57,['TOST'],'FontSize',[10],'FontName','arial','Color',[0 0 0],'FontWeight','normal')
text(3.4*1.4,28,['TOST'],'FontSize',[10],'FontName','arial','Color',[0 0 0],'FontWeight','normal')
text(5.5,-4,['TOST'],'FontSize',[10],'FontName','arial','Color',[0 0 0],'FontWeight','normal')
text(0.9,-58,['TOST'],'FontSize',[10],'FontName','arial','Color',[0 0 0],'FontWeight','normal')

text(1.5*1.3,-28,['Sat1'],'FontSize',[10],'FontName','arial','Color',[0 0 0],'FontWeight','normal')
text(1.9,20.5,['Sat1'],'FontSize',[10],'FontName','arial','Color',[0 0 0],'FontWeight','normal')
text(0.85*1.435,6,['Sat2'],'FontSize',[10],'FontName','arial','Color',[0 0 0],'FontWeight','normal')
text(-1.4,7,['Sat3'],'FontSize',[10],'FontName','arial','Color',[0 0 0],'FontWeight','normal')

text(-1.2, 96,['Tropospheric column average'],'FontSize',[12],'FontName','arial','Color',[0 0 0],'FontWeight','normal')

text(.2,82,['TOST ozonesondes: 1998-2012'],'FontSize',[11],'FontName','arial','Color',[0 0 0],'FontWeight','normal')
text(3.2,74,['  Sat1:  1979-2016'],'FontSize',[11],'FontName','arial','Color',[0 0 0],'FontWeight','normal')
text(3.2,66,['  Sat2:  1995-2015'],'FontSize',[11],'FontName','arial','Color',[0 0 0],'FontWeight','normal')
text(3.2,58,['  Sat3:  1995-2015'],'FontSize',[11],'FontName','arial','Color',[0 0 0],'FontWeight','normal')


hold off
axis([-3 8   -90 90 ])
xlabel('Ozone trend (ppbv decade^-^1)')
%ylabel('Latitude')

set(gca,'FontSize',[11],'FontWeight','demi','FontName','arial','TickLength',[.005 .005],'Color',[1 1 1 ],'XColor',[0 0 0],'YColor',[0 0 0],'YTick',[-90:10:90],'XTick',[-5:1:8],'Box','off','Clipping','off','LineWidth',[0.5],'YTickLabel',[],'TickDir','out');
set(gcf,'InvertHardCopy','off','Color',[1 1 1])

print_name=[ 'IPCC_decadal_trend_for_tropospheric_column_ozone.eps' ];
print('-depsc',print_name)

quit




















