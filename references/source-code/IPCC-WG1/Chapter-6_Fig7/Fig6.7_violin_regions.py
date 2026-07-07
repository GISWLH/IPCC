import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt


regionnum=1 #Southern Asia 
#regionnum=2 #Europe
#regionnum=3 #Africa
#regionnum=4 #South-East Asia and Developing Pacific
#regionnum=5 #Latin America and Caribbean
#regionnum=6 #Eurasia
#regionnum=7 #Asia-Pacific Developed
#regionnum=8 #Middle East
#regionnum=9 #North America rural
#regionnum=10 #Eastern Asia 
#regionnum=11 #North America urban
#regionnum=12 #example 

AR6_file = Dataset('../input/AR6WG3_Atlas_IntermedRegions_1.0x1.0.nc','r')
AR6 = AR6_file.variables["AR6WG3RegionIntm"][:,:]
lat_in = AR6_file.variables['latitude'][:]
lon_in = AR6_file.variables['longitude'][:]

if regionnum==12:

   SO4_file = Dataset('../input/Europe/EMEP/Aas/SO4mm_month_2000-2018_pm25.nc','r')

   SO4 = SO4_file.variables["DATA"][:,:]
   LON_SO4 = SO4_file.variables["LON"][:,:]
   LAT_SO4 = SO4_file.variables["LAT"][:,:]

   LAT=LAT_SO4
   LON=LON_SO4
   print(len(LAT[0,:]))
   regi_SO4=LAT*0
   for lt in range(len(lat_in[:])):
     for ln in range(len(lon_in[:])):
       for j in range(len(LAT[0,:])):
            if lat_in[lt] <= (LAT[0,j]+0.5) and lat_in[lt] >= (LAT[0,j]-0.5) and lon_in[ln] >= (LON[0,j]-0.5) and lon_in[ln] <= (LON[0,j]+0.5):
                 regi_SO4[:,j]=AR6[lt,ln]
   
if regionnum==1 or regionnum==3 or regionnum==5 or regionnum==8:

   NH4_file = Dataset('../input/SPARTAN/NH4_month_2013-2019.nc','r')
   NO3_file = Dataset('../input/SPARTAN/NO3_month_2013-2019.nc','r')
   SO4_file = Dataset('../input/SPARTAN/SO4_month_2013-2019.nc','r')
   Na_file  = Dataset('../input/SPARTAN/Na_month_2013-2019.nc','r')

   LON = SO4_file.variables["LON"][:,:]
   LAT = SO4_file.variables["LAT"][:,:]
   NH4 = NH4_file.variables["DATA"][:,:]
   Na  = Na_file.variables["DATA"][:,:]
   NO3 = NO3_file.variables["DATA"][:,:]
   SO4 = SO4_file.variables["DATA"][:,:]

   print(len(LAT[0,:]))
   regi=LAT*0
   for lt in range(len(lat_in[:])):
     for ln in range(len(lon_in[:])):
       for j in range(len(LAT[0,:])):
            if lat_in[lt] <= (LAT[0,j]+0.5) and lat_in[lt] >= (LAT[0,j]-0.5) and lon_in[ln] >= (LON[0,j]-0.5) and lon_in[ln] <= (LON[0,j]+0.5):
                 regi[:,j]=AR6[lt,ln]
   
if regionnum==2:

   OC_file  = Dataset('../input/Europe/EMEP/Aas/OC_month_2000-2018_pm25.nc','r')
   NH4_file = Dataset('../input/Europe/EMEP/Aas/NH4p_month_2000-2018_pm25.nc','r')
   Na_file  = Dataset('../input/Europe/EMEP/Aas/Nap_month_2000-2018_pm25.nc','r')
   Cl_file  = Dataset('../input/Europe/EMEP/Aas/Clm_month_2000-2018_pm25.nc','r')
   NO3_file = Dataset('../input/Europe/EMEP/Aas/NO3m_month_2000-2018_pm25.nc','r')
   SO4_file = Dataset('../input/Europe/EMEP/Aas/SO4mm_month_2000-2018_pm25.nc','r')
   EC_file  = Dataset('../input/Europe/EMEP/Aas/EC_month_2000-2018_pm25.nc','r')

   ORG = OC_file.variables["DATA"][:,:]
   LON_ORG = OC_file.variables["LON"][:,:]
   LAT_ORG = OC_file.variables["LAT"][:,:]
   NH4 = NH4_file.variables["DATA"][:,:]
   LON_NH4 = NH4_file.variables["LON"][:,:]
   LAT_NH4 = NH4_file.variables["LAT"][:,:]
   Na  = Na_file.variables["DATA"][:,:]
   LON_Na = Na_file.variables["LON"][:,:]
   LAT_Na = Na_file.variables["LAT"][:,:]
   Cl  = Cl_file.variables["DATA"][:,:]
   LON_Cl = Cl_file.variables["LON"][:,:]
   LAT_Cl = Cl_file.variables["LAT"][:,:]
   NO3 = NO3_file.variables["DATA"][:,:]
   LON_NO3 = NO3_file.variables["LON"][:,:]
   LAT_NO3 = NO3_file.variables["LAT"][:,:]
   SO4 = SO4_file.variables["DATA"][:,:]
   LON_SO4 = SO4_file.variables["LON"][:,:]
   LAT_SO4 = SO4_file.variables["LAT"][:,:]
   EC  = EC_file.variables["DATA"][:,:]
   LON_EC = EC_file.variables["LON"][:,:]
   LAT_EC = EC_file.variables["LAT"][:,:]

   LAT=LAT_ORG
   LON=LON_ORG
   print(len(LAT[0,:]))
   regi_ORG=LAT*0
   for lt in range(len(lat_in[:])):
     for ln in range(len(lon_in[:])):
       for j in range(len(LAT[0,:])):
            if lat_in[lt] <= (LAT[0,j]+0.5) and lat_in[lt] >= (LAT[0,j]-0.5) and lon_in[ln] >= (LON[0,j]-0.5) and lon_in[ln] <= (LON[0,j]+0.5):
                 regi_ORG[:,j]=AR6[lt,ln]

   LAT=LAT_NH4
   LON=LON_NH4
   print(len(LAT[0,:]))
   regi_NH4=LAT*0
   for lt in range(len(lat_in[:])):
     for ln in range(len(lon_in[:])):
       for j in range(len(LAT[0,:])):
            if lat_in[lt] <= (LAT[0,j]+0.5) and lat_in[lt] >= (LAT[0,j]-0.5) and lon_in[ln] >= (LON[0,j]-0.5) and lon_in[ln] <= (LON[0,j]+0.5):
                 regi_NH4[:,j]=AR6[lt,ln]

   LAT=LAT_Na
   LON=LON_Na 
   print(len(LAT[0,:]))
   regi_Na=LAT*0
   for lt in range(len(lat_in[:])):
     for ln in range(len(lon_in[:])):
       for j in range(len(LAT[0,:])):
            if lat_in[lt] <= (LAT[0,j]+0.5) and lat_in[lt] >= (LAT[0,j]-0.5) and lon_in[ln] >= (LON[0,j]-0.5) and lon_in[ln] <= (LON[0,j]+0.5):
                 regi_Na[:,j]=AR6[lt,ln]

   LAT=LAT_Cl
   LON=LON_Cl 
   print(len(LAT[0,:]))
   regi_Cl=LAT*0
   for lt in range(len(lat_in[:])):
     for ln in range(len(lon_in[:])):
       for j in range(len(LAT[0,:])):
            if lat_in[lt] <= (LAT[0,j]+0.5) and lat_in[lt] >= (LAT[0,j]-0.5) and lon_in[ln] >= (LON[0,j]-0.5) and lon_in[ln] <= (LON[0,j]+0.5):
                 regi_Cl[:,j]=AR6[lt,ln]

   LAT=LAT_NO3
   LON=LON_NO3
   print(len(LAT[0,:]))
   regi_NO3=LAT*0
   for lt in range(len(lat_in[:])):
     for ln in range(len(lon_in[:])):
       for j in range(len(LAT[0,:])):
            if lat_in[lt] <= (LAT[0,j]+0.5) and lat_in[lt] >= (LAT[0,j]-0.5) and lon_in[ln] >= (LON[0,j]-0.5) and lon_in[ln] <= (LON[0,j]+0.5):
                 regi_NO3[:,j]=AR6[lt,ln]

   LAT=LAT_SO4
   LON=LON_SO4
   print(len(LAT[0,:]))
   regi_SO4=LAT*0
   for lt in range(len(lat_in[:])):
     for ln in range(len(lon_in[:])):
       for j in range(len(LAT[0,:])):
            if lat_in[lt] <= (LAT[0,j]+0.5) and lat_in[lt] >= (LAT[0,j]-0.5) and lon_in[ln] >= (LON[0,j]-0.5) and lon_in[ln] <= (LON[0,j]+0.5):
                 regi_SO4[:,j]=AR6[lt,ln]

   LAT=LAT_EC
   LON=LON_EC 
   print(len(LAT[0,:]))
   regi_EC=LAT*0
   for lt in range(len(lat_in[:])):
     for ln in range(len(lon_in[:])):
       for j in range(len(LAT[0,:])):
            if lat_in[lt] <= (LAT[0,j]+0.5) and lat_in[lt] >= (LAT[0,j]-0.5) and lon_in[ln] >= (LON[0,j]-0.5) and lon_in[ln] <= (LON[0,j]+0.5):
                 regi_EC[:,j]=AR6[lt,ln]

if regionnum==4 or regionnum==10:

   NH4_spar = Dataset('../input/SPARTAN/NH4_month_2013-2019.nc','r')
   NO3_spar = Dataset('../input/SPARTAN/NO3_month_2013-2019.nc','r')
   SO4_spar = Dataset('../input/SPARTAN/SO4_month_2013-2019.nc','r')
   Na_spar = Dataset('../input/SPARTAN/Na_month_2013-2019.nc','r')

   LONs = SO4_spar.variables["LON"][:,:]
   LATs = SO4_spar.variables["LAT"][:,:]
   NH4s = NH4_spar.variables["DATA"][:,:]
   Nas  =  Na_spar.variables["DATA"][:,:]
   NO3s = NO3_spar.variables["DATA"][:,:]
   SO4s = SO4_spar.variables["DATA"][:,:]

   LAT=LATs
   LON=LONs
   print(len(LAT[0,:]))
   regi=LAT*0
   for lt in range(len(lat_in[:])):
     for ln in range(len(lon_in[:])):
       for j in range(len(LAT[0,:])):
            if lat_in[lt] <= (LAT[0,j]+0.5) and lat_in[lt] >= (LAT[0,j]-0.5) and lon_in[ln] >= (LON[0,j]-0.5) and lon_in[ln] <= (LON[0,j]+0.5):
                 regi[:,j]=AR6[lt,ln]

   OC_file  = Dataset('../input/Asia/EANET/TotOC_month_2001-2010.nc','r')
   NH4_file = Dataset('../input/Asia/EANET/NH4p_month_2001-2017.nc','r')
   Na_file  = Dataset('../input/Asia/EANET/Nap_month_2001-2017.nc','r')
   Cl_file  = Dataset('../input/Asia/EANET/Clm_month_2001-2017.nc','r')
   NO3_file = Dataset('../input/Asia/EANET/NO3m_month_2001-2017.nc','r')
   SO4_file = Dataset('../input/Asia/EANET/SO4mm_month_2001-2017.nc','r')

   ORG = OC_file.variables["DATA"][:,:]
   LON_ORG = OC_file.variables["LON"][:,:]
   LAT_ORG = OC_file.variables["LAT"][:,:]
   NH4 = NH4_file.variables["DATA"][:,:]
   LON_NH4 = NH4_file.variables["LON"][:,:]
   LAT_NH4 = NH4_file.variables["LAT"][:,:]
   Na  = Na_file.variables["DATA"][:,:]
   LON_Na = Na_file.variables["LON"][:,:]
   LAT_Na = Na_file.variables["LAT"][:,:]
   Cl  = Cl_file.variables["DATA"][:,:]
   LON_Cl = Cl_file.variables["LON"][:,:]
   LAT_Cl = Cl_file.variables["LAT"][:,:]
   NO3 = NO3_file.variables["DATA"][:,:]
   LON_NO3 = NO3_file.variables["LON"][:,:]
   LAT_NO3 = NO3_file.variables["LAT"][:,:]
   SO4 = SO4_file.variables["DATA"][:,:]
   LON_SO4 = SO4_file.variables["LON"][:,:]
   LAT_SO4 = SO4_file.variables["LAT"][:,:]

   LAT=LAT_ORG
   LON=LON_ORG
   print(len(LAT[0,:]))
   regie_ORG=LAT*0
   for lt in range(len(lat_in[:])):
     for ln in range(len(lon_in[:])):
       for j in range(len(LAT[0,:])):
            if lat_in[lt] <= (LAT[0,j]+0.5) and lat_in[lt] >= (LAT[0,j]-0.5) and lon_in[ln] >= (LON[0,j]-0.5) and lon_in[ln] <= (LON[0,j]+0.5):
                 regie_ORG[:,j]=AR6[lt,ln]

   LAT=LAT_NH4
   LON=LON_NH4
   print(len(LAT[0,:]))
   regieanet=LAT*0
   for lt in range(len(lat_in[:])):
     for ln in range(len(lon_in[:])):
       for j in range(len(LAT[0,:])):
            if lat_in[lt] <= (LAT[0,j]+0.5) and lat_in[lt] >= (LAT[0,j]-0.5) and lon_in[ln] >= (LON[0,j]-0.5) and lon_in[ln] <= (LON[0,j]+0.5):
                 regieanet[:,j]=AR6[lt,ln]

if regionnum==6:

   OC_file  = Dataset('../input/Europe/EMEP/Aas/OC_month_2000-2018_pm25.nc','r')
   NH4_file = Dataset('../input/Europe/EMEP/Aas/NH4p_month_2000-2018_pm25.nc','r')
   Na_file  = Dataset('../input/Europe/EMEP/Aas/Nap_month_2000-2018_pm25.nc','r')
   Cl_file  = Dataset('../input/Europe/EMEP/Aas/Clm_month_2000-2018_pm25.nc','r')
   NO3_file = Dataset('../input/Europe/EMEP/Aas/NO3m_month_2000-2018_pm25.nc','r')
   SO4_file = Dataset('../input/Europe/EMEP/Aas/SO4mm_month_2000-2018_pm25.nc','r')
   EC_file  = Dataset('../input/Europe/EMEP/Aas/EC_month_2000-2018_pm25.nc','r')

   ORG = OC_file.variables["DATA"][:,:]
   LON_ORG = OC_file.variables["LON"][:,:]
   LAT_ORG = OC_file.variables["LAT"][:,:]
   NH4 = NH4_file.variables["DATA"][:,:]
   LON_NH4 = NH4_file.variables["LON"][:,:]
   LAT_NH4 = NH4_file.variables["LAT"][:,:]
   Na  = Na_file.variables["DATA"][:,:]
   LON_Na = Na_file.variables["LON"][:,:]
   LAT_Na = Na_file.variables["LAT"][:,:]
   Cl  = Cl_file.variables["DATA"][:,:]
   LON_Cl = Cl_file.variables["LON"][:,:]
   LAT_Cl = Cl_file.variables["LAT"][:,:]
   NO3 = NO3_file.variables["DATA"][:,:]
   LON_NO3 = NO3_file.variables["LON"][:,:]
   LAT_NO3 = NO3_file.variables["LAT"][:,:]
   SO4 = SO4_file.variables["DATA"][:,:]
   LON_SO4 = SO4_file.variables["LON"][:,:]
   LAT_SO4 = SO4_file.variables["LAT"][:,:]
   EC  = EC_file.variables["DATA"][:,:]
   LON_EC = EC_file.variables["LON"][:,:]
   LAT_EC = EC_file.variables["LAT"][:,:]

   LAT=LAT_ORG
   LON=LON_ORG
   print(len(LAT[0,:]))
   regi_ORG=LAT*0
   for lt in range(len(lat_in[:])):
     for ln in range(len(lon_in[:])):
       for j in range(len(LAT[0,:])):
            if lat_in[lt] <= (LAT[0,j]+0.5) and lat_in[lt] >= (LAT[0,j]-0.5) and lon_in[ln] >= (LON[0,j]-0.5) and lon_in[ln] <= (LON[0,j]+0.5):
                 regi_ORG[:,j]=AR6[lt,ln]

   LAT=LAT_NH4
   LON=LON_NH4
   print(len(LAT[0,:]))
   regi_NH4=LAT*0
   for lt in range(len(lat_in[:])):
     for ln in range(len(lon_in[:])):
       for j in range(len(LAT[0,:])):
            if lat_in[lt] <= (LAT[0,j]+0.5) and lat_in[lt] >= (LAT[0,j]-0.5) and lon_in[ln] >= (LON[0,j]-0.5) and lon_in[ln] <= (LON[0,j]+0.5):
                 regi_NH4[:,j]=AR6[lt,ln]

   LAT=LAT_Na
   LON=LON_Na 
   print(len(LAT[0,:]))
   regi_Na=LAT*0
   for lt in range(len(lat_in[:])):
     for ln in range(len(lon_in[:])):
       for j in range(len(LAT[0,:])):
            if lat_in[lt] <= (LAT[0,j]+0.5) and lat_in[lt] >= (LAT[0,j]-0.5) and lon_in[ln] >= (LON[0,j]-0.5) and lon_in[ln] <= (LON[0,j]+0.5):
                 regi_Na[:,j]=AR6[lt,ln]

   LAT=LAT_Cl
   LON=LON_Cl 
   print(len(LAT[0,:]))
   regi_Cl=LAT*0
   for lt in range(len(lat_in[:])):
     for ln in range(len(lon_in[:])):
       for j in range(len(LAT[0,:])):
            if lat_in[lt] <= (LAT[0,j]+0.5) and lat_in[lt] >= (LAT[0,j]-0.5) and lon_in[ln] >= (LON[0,j]-0.5) and lon_in[ln] <= (LON[0,j]+0.5):
                 regi_Cl[:,j]=AR6[lt,ln]

   LAT=LAT_NO3
   LON=LON_NO3
   print(len(LAT[0,:]))
   regi_NO3=LAT*0
   for lt in range(len(lat_in[:])):
     for ln in range(len(lon_in[:])):
       for j in range(len(LAT[0,:])):
            if lat_in[lt] <= (LAT[0,j]+0.5) and lat_in[lt] >= (LAT[0,j]-0.5) and lon_in[ln] >= (LON[0,j]-0.5) and lon_in[ln] <= (LON[0,j]+0.5):
                 regi_NO3[:,j]=AR6[lt,ln]

   LAT=LAT_SO4
   LON=LON_SO4
   print(len(LAT[0,:]))
   regi_SO4=LAT*0
   for lt in range(len(lat_in[:])):
     for ln in range(len(lon_in[:])):
       for j in range(len(LAT[0,:])):
            if lat_in[lt] <= (LAT[0,j]+0.5) and lat_in[lt] >= (LAT[0,j]-0.5) and lon_in[ln] >= (LON[0,j]-0.5) and lon_in[ln] <= (LON[0,j]+0.5):
                 regi_SO4[:,j]=AR6[lt,ln]

   LAT=LAT_EC
   LON=LON_EC 
   print(len(LAT[0,:]))
   regi_EC=LAT*0
   for lt in range(len(lat_in[:])):
     for ln in range(len(lon_in[:])):
       for j in range(len(LAT[0,:])):
            if lat_in[lt] <= (LAT[0,j]+0.5) and lat_in[lt] >= (LAT[0,j]-0.5) and lon_in[ln] >= (LON[0,j]-0.5) and lon_in[ln] <= (LON[0,j]+0.5):
                 regi_EC[:,j]=AR6[lt,ln]

   NH4e_file = Dataset('../input/Asia/EANET/NH4p_month_2001-2017.nc','r')
   Nae_file  = Dataset('../input/Asia/EANET/Nap_month_2001-2017.nc','r')
   Cle_file  = Dataset('../input/Asia/EANET/Clm_month_2001-2017.nc','r')
   NO3e_file = Dataset('../input/Asia/EANET/NO3m_month_2001-2017.nc','r')
   SO4e_file = Dataset('../input/Asia/EANET/SO4mm_month_2001-2017.nc','r')

   NH4e = NH4e_file.variables["DATA"][:,:]
   LONe_NH4 = NH4e_file.variables["LON"][:,:]
   LATe_NH4 = NH4e_file.variables["LAT"][:,:]
   Nae = Nae_file.variables["DATA"][:,:]
   Cle = Cle_file.variables["DATA"][:,:]
   NO3e = NO3e_file.variables["DATA"][:,:]
   SO4e = SO4e_file.variables["DATA"][:,:]

   LAT=LATe_NH4
   LON=LONe_NH4
   print(len(LAT[0,:]))
   regieanet=LAT*0
   for lt in range(len(lat_in[:])):
     for ln in range(len(lon_in[:])):
       for j in range(len(LAT[0,:])):
            if lat_in[lt] <= (LAT[0,j]+0.5) and lat_in[lt] >= (LAT[0,j]-0.5) and lon_in[ln] >= (LON[0,j]-0.5) and lon_in[ln] <= (LON[0,j]+0.5):
                 regieanet[:,j]=AR6[lt,ln]


if regionnum==7:

   ORGe_file = Dataset('../input/Asia/EANET/TotOC_month_2001-2010.nc','r')
   NH4e_file = Dataset('../input/Asia/EANET/NH4p_month_2001-2017.nc','r')
   Nae_file  = Dataset('../input/Asia/EANET/Nap_month_2001-2017.nc','r')
   Cle_file  = Dataset('../input/Asia/EANET/Clm_month_2001-2017.nc','r')
   NO3e_file = Dataset('../input/Asia/EANET/NO3m_month_2001-2017.nc','r')
   SO4e_file = Dataset('../input/Asia/EANET/SO4mm_month_2001-2017.nc','r')

   ORGe = ORGe_file.variables["DATA"][:,:]
   LONe_ORG = ORGe_file.variables["LON"][:,:]
   LATe_ORG = ORGe_file.variables["LAT"][:,:]
   NH4e = NH4e_file.variables["DATA"][:,:]
   LONe_NH4 = NH4e_file.variables["LON"][:,:]
   LATe_NH4 = NH4e_file.variables["LAT"][:,:]
   Nae = Nae_file.variables["DATA"][:,:]
   Cle = Cle_file.variables["DATA"][:,:]
   NO3e = NO3e_file.variables["DATA"][:,:]
   SO4e = SO4e_file.variables["DATA"][:,:]

   LAT=LATe_NH4
   LON=LONe_NH4
   print(len(LAT[0,:]))
   regieanet=LAT*0
   for lt in range(len(lat_in[:])):
     for ln in range(len(lon_in[:])):
       for j in range(len(LAT[0,:])):
            if lat_in[lt] <= (LAT[0,j]+0.5) and lat_in[lt] >= (LAT[0,j]-0.5) and lon_in[ln] >= (LON[0,j]-0.5) and lon_in[ln] <= (LON[0,j]+0.5):
                 regieanet[:,j]=AR6[lt,ln]

   LAT=LATe_ORG
   LON=LONe_ORG
   print(len(LAT[0,:]))
   regia_ORG=LAT*0
   for lt in range(len(lat_in[:])):
     for ln in range(len(lon_in[:])):
       for j in range(len(LAT[0,:])):
            if lat_in[lt] <= (LAT[0,j]+0.5) and lat_in[lt] >= (LAT[0,j]-0.5) and lon_in[ln] >= (LON[0,j]-0.5) and lon_in[ln] <= (LON[0,j]+0.5):
                 regia_ORG[:,j]=AR6[lt,ln]

if regionnum==9:

   OC_file  = Dataset('../input/North_America/IMPROVE/OC_month_2000-2018.nc','r')
   NH4_file = Dataset('../input/North_America/IMPROVE/NH4_month_2000-2018.nc','r')
   Na_file  = Dataset('../input/North_America/IMPROVE/Na_month_2000-2018.nc','r')
   Cl_file  = Dataset('../input/North_America/IMPROVE/Cl_month_2000-2018.nc','r')
   NO3_file = Dataset('../input/North_America/IMPROVE/NO3_month_2000-2018.nc','r')
   SO4_file = Dataset('../input/North_America/IMPROVE/SO4_month_2000-2018.nc','r')
   EC_file  = Dataset('../input/North_America/IMPROVE/EC_month_2000-2018.nc','r')

   ORG = OC_file.variables["DATA"][:,:]
   LON_ORG = OC_file.variables["LON"][:,:]
   LAT_ORG = OC_file.variables["LAT"][:,:]
   NH4 = NH4_file.variables["DATA"][:,:]
   Na  = Na_file.variables["DATA"][:,:]
   Cl  = Cl_file.variables["DATA"][:,:]
   NO3 = NO3_file.variables["DATA"][:,:]
   SO4 = SO4_file.variables["DATA"][:,:]
   EC  = EC_file.variables["DATA"][:,:]

#   LAT=LAT_ORG
#   LON=LON_ORG
#   print(len(LAT[0,:]))
#   regimprove=LAT*0
#   for lt in range(len(lat_in[:])):
#     for ln in range(len(lon_in[:])):
#       for j in range(len(LAT[0,:])):
#            if lat_in[lt] <= (LAT[0,j]+0.5) and lat_in[lt] >= (LAT[0,j]-0.5) and lon_in[ln] >= (LON[0,j]-0.5) and lon_in[ln] <= (LON[0,j]+0.5):
#                 regimprove[:,j]=AR6[lt,ln]

if regionnum==11:
   NH4_spar = Dataset('../input/SPARTAN/NH4_month_2013-2019.nc','r')
   NO3_spar = Dataset('../input/SPARTAN/NO3_month_2013-2019.nc','r')
   SO4_spar = Dataset('../input/SPARTAN/SO4_month_2013-2019.nc','r')
   Na_spar = Dataset('../input/SPARTAN/Na_month_2013-2019.nc','r')

   LONs = SO4_spar.variables["LON"][:,:]
   LATs = SO4_spar.variables["LAT"][:,:]
   NH4s = NH4_spar.variables["DATA"][:,:]
   Nas  =  Na_spar.variables["DATA"][:,:]
   NO3s = NO3_spar.variables["DATA"][:,:]
   SO4s = SO4_spar.variables["DATA"][:,:]

   LAT=LATs
   LON=LONs
   print(len(LAT[0,:]))
   regi=LAT*0
   for lt in range(len(lat_in[:])):
     for ln in range(len(lon_in[:])):
       for j in range(len(LAT[0,:])):
            if lat_in[lt] <= (LAT[0,j]+0.5) and lat_in[lt] >= (LAT[0,j]-0.5) and lon_in[ln] >= (LON[0,j]-0.5) and lon_in[ln] <= (LON[0,j]+0.5):
                 regi[:,j]=AR6[lt,ln]

   OC_file  = Dataset('../input/North_America/EPA/OC_month_2000-2018.nc','r')
   NH4_file = Dataset('../input/North_America/EPA/NH4_month_2000-2018.nc','r')
   Na_file  = Dataset('../input/North_America/EPA/Na_month_2000-2018.nc','r')
   Cl_file  = Dataset('../input/North_America/EPA/Cl_month_2000-2018.nc','r')
   NO3_file = Dataset('../input/North_America/EPA/NO3_month_2000-2018.nc','r')
   SO4_file = Dataset('../input/North_America/EPA/SO4_month_2000-2018.nc','r')
   EC_file  = Dataset('../input/North_America/EPA/EC_month_2000-2018.nc','r')

   ORG = OC_file.variables["DATA"][:,:]
   LON_ORG = OC_file.variables["LON"][:,:]
   LAT_ORG = OC_file.variables["LAT"][:,:]
   NH4 = NH4_file.variables["DATA"][:,:]
   Na  = Na_file.variables["DATA"][:,:]
   Cl  = Cl_file.variables["DATA"][:,:]
   NO3 = NO3_file.variables["DATA"][:,:]
   SO4 = SO4_file.variables["DATA"][:,:]
   EC  = EC_file.variables["DATA"][:,:]

if regionnum==12:

   sub_SO4=SO4[(regi_SO4==2)]
   
   fl_SO4=sub_SO4.flatten()
   # Filter data using np.isnan
   fl_SO4[fl_SO4 == -1e+34] = np.nan
   
   example_SO4 = 3*fl_SO4[~np.isnan(fl_SO4)]

   #for i in example_SO4:
   #   if i >=1:
   #      little_high_SO4 = 5*example_SO4
   #for i in example_SO4:
   #   if i >=10:
   #      very_high_SO4 = 10*example_SO4
   
   
   for m in example_SO4:
      if m <=10:
         little_low_SO4 = 0.1*example_SO4
   
   for m in example_SO4:
      if m <=1:
         very_low_SO4 = 0.01*example_SO4
   
   
   low_SO4 = np.concatenate((very_low_SO4,little_low_SO4))
   #high_SO4 = np.concatenate((very_high_SO4,little_high_SO4))
   #mask_SO4 = np.concatenate((low_SO4,high_SO4))
   mask_SO4 = np.concatenate((low_SO4,example_SO4))

if regionnum==1 or regionnum==8:

   sub_NH4=NH4[(regi==regionnum)]
   sub_Na = Na[(regi==regionnum)]
   sub_NO3=NO3[(regi==regionnum)]
   sub_SO4=SO4[(regi==regionnum)]
   
   fl_NH4=sub_NH4.flatten()
   fl_Na =sub_Na.flatten()
   fl_NO3=sub_NO3.flatten()
   fl_SO4=sub_SO4.flatten()
   # Filter data using np.isnan
   fl_NH4[fl_NH4 == -1e+34] = np.nan
   fl_Na[fl_Na == -1e+34]   = np.nan
   fl_NO3[fl_NO3 == -1e+34] = np.nan
   fl_SO4[fl_SO4 == -1e+34] = np.nan
   
   spartan_NH4 = fl_NH4[~np.isnan(fl_NH4)]
   spartan_Na  = fl_Na[~np.isnan(fl_Na)]
   spartan_NO3 = fl_NO3[~np.isnan(fl_NO3)]
   spartan_SO4 = fl_SO4[~np.isnan(fl_SO4)]

   mask_NH4 = spartan_NH4
   mask_Na  = spartan_Na 
   mask_NO3 = spartan_NO3
   mask_SO4 = spartan_SO4

if regionnum==2:
   sub_ORG=ORG[(regi_ORG==regionnum)]
   sub_NH4=NH4[(regi_NH4==regionnum)]
   sub_Na = Na[(regi_Na==regionnum)]
   sub_Cl = Cl[(regi_Cl==regionnum)]
   sub_NO3=NO3[(regi_NO3==regionnum)]
   sub_SO4=SO4[(regi_SO4==regionnum)]
   sub_EC=  EC[(regi_EC==regionnum)]
   
   fl_ORG=sub_ORG.flatten()
   fl_NH4=sub_NH4.flatten()
   fl_Na =sub_Na.flatten()
   fl_Cl =sub_Cl.flatten()
   fl_NO3=sub_NO3.flatten()
   fl_SO4=sub_SO4.flatten()
   fl_EC =sub_EC.flatten()
   # Filter data using np.isnan
   fl_ORG[fl_ORG == -1e+34] = np.nan
   fl_NH4[fl_NH4 == -1e+34] = np.nan
   fl_Na[fl_Na == -1e+34]   = np.nan
   fl_Cl[fl_Cl == -1e+34]   = np.nan
   fl_NO3[fl_NO3 == -1e+34] = np.nan
   fl_SO4[fl_SO4 == -1e+34] = np.nan
   fl_EC[fl_EC == -1e+34]   = np.nan
   
   EMEP_ORG = fl_ORG[~np.isnan(fl_ORG)]
   EMEP_NH4 = 18/14*fl_NH4[~np.isnan(fl_NH4)]
   EMEP_Na  = fl_Na[~np.isnan(fl_Na)]
   EMEP_Cl  = fl_Cl[~np.isnan(fl_Cl)]
   EMEP_NO3 = 62/14*fl_NO3[~np.isnan(fl_NO3)]
   EMEP_SO4 = 3*fl_SO4[~np.isnan(fl_SO4)]
   EMEP_EC  = fl_EC[~np.isnan(fl_EC)]
   
   #print(mask_NH4.shape)
   mask_NH4 = EMEP_NH4
   mask_Na  = EMEP_Na 
   mask_NO3 = EMEP_NO3
   mask_SO4 = EMEP_SO4
   mask_Cl  = EMEP_Cl 
   mask_ORG = EMEP_ORG
   mask_EC  = EMEP_EC

if regionnum==3:

   sub_NH4=NH4[(regi==regionnum)]
   sub_Na = Na[(regi==regionnum)]
   sub_NO3=NO3[(regi==regionnum)]
   sub_SO4=SO4[(regi==regionnum)]
   
   fl_NH4=sub_NH4.flatten()
   fl_Na =sub_Na.flatten()
   fl_NO3=sub_NO3.flatten()
   fl_SO4=sub_SO4.flatten()
   # Filter data using np.isnan
   fl_NH4[fl_NH4 == -1e+34] = np.nan
   fl_Na[fl_Na == -1e+34]   = np.nan
   fl_NO3[fl_NO3 == -1e+34] = np.nan
   fl_SO4[fl_SO4 == -1e+34] = np.nan
   
   spartan_NH4 = fl_NH4[~np.isnan(fl_NH4)]
   spartan_Na  = fl_Na[~np.isnan(fl_Na)]
   spartan_NO3 = fl_NO3[~np.isnan(fl_NO3)]
   spartan_SO4 = fl_SO4[~np.isnan(fl_SO4)]

   field_NH4 = np.array([2.3, 4.3, 1.9, 1.15, 4.95, 0.15, 0.23, 0.12, 0.09, 0.11, 0.05, 0.53, 0.24, 0.29])
   field_Na  = np.array([6.3, 6.45, 3.8, 3.45, 6.6, 0.41, 1.02, 0.13, 1.57, 3, 0.88, 0.26, 2.5, 0.29])
   field_Cl  = np.array([10, 19.35, 9.5, 4.6, 18.15, 0.37, 1.06, 0.11, 2.4, 5.1, 1.5, 0.55, 5.2, 0.46])
   field_NO3 = np.array([4.9, 6.45, 5.7, 5.75, 6.6, 0.43, 1.53, 0.18, 0.75, 0.82, 0.34, 0.96, 1.43, 0.62])
   field_ORG = np.array([36.55, 26.6, 26.45, 46.2, 6.5, 11, 3.9, 11, 14, 9.5,])
   field_SO4 = np.array([14.0, 15.05, 13.3, 13.8, 16.5, 0.77, 1.85, 0.41, 2.1, 2.5, 1.44, 1.47, 1.6, 2.14])
   field_EC  = np.array([10.75, 5.7, 5.75, 8.25, 0.46, 0.82, 0.51, 4.3, 4.4, 4.3])

   mask_NH4 = np.concatenate((spartan_NH4,field_NH4))
   mask_Na  = np.concatenate((spartan_Na ,field_Na ))
   mask_NO3 = np.concatenate((spartan_NO3,field_NO3))
   mask_SO4 = np.concatenate((spartan_SO4,field_SO4))
   mask_Cl  = field_Cl
   mask_ORG = field_ORG
   mask_EC  = field_EC

if regionnum==4 or regionnum==10:

   subs_NH4=NH4s[(regi==regionnum)]
   subs_Na = Nas[(regi==regionnum)]
   subs_NO3=NO3s[(regi==regionnum)]
   subs_SO4=SO4s[(regi==regionnum)]
   
   fls_NH4=subs_NH4.flatten()
   fls_Na =subs_Na.flatten()
   fls_NO3=subs_NO3.flatten()
   fls_SO4=subs_SO4.flatten()
   # Filter data using np.isnan
   fls_NH4[fls_NH4 == -1e+34] = np.nan
   fls_Na[fls_Na == -1e+34]   = np.nan
   fls_NO3[fls_NO3 == -1e+34] = np.nan
   fls_SO4[fls_SO4 == -1e+34] = np.nan
   
   spartan_NH4 = fls_NH4[~np.isnan(fls_NH4)]
   spartan_Na  = fls_Na[~np.isnan(fls_Na)]
   spartan_NO3 = fls_NO3[~np.isnan(fls_NO3)]
   spartan_SO4 = fls_SO4[~np.isnan(fls_SO4)]

   sub_ORG=ORG[(regie_ORG==regionnum)]
   sub_NH4=NH4[(regieanet==regionnum)]
   sub_Na = Na[(regieanet==regionnum)]
   sub_Cl = Cl[(regieanet==regionnum)]
   sub_NO3=NO3[(regieanet==regionnum)]
   sub_SO4=SO4[(regieanet==regionnum)]

   fl_ORG=sub_ORG.flatten()
   fl_NH4=sub_NH4.flatten()
   fl_Na =sub_Na.flatten()
   fl_Cl =sub_Cl.flatten()
   fl_NO3=sub_NO3.flatten()
   fl_SO4=sub_SO4.flatten()
   # Filter data using np.isnan
   fl_ORG[fl_ORG == -1e+34] = np.nan
   fl_NH4[fl_NH4 == -1e+34] = np.nan
   fl_Na[fl_Na == -1e+34]   = np.nan
   fl_Cl[fl_Cl == -1e+34]   = np.nan
   fl_NO3[fl_NO3 == -1e+34] = np.nan
   fl_SO4[fl_SO4 == -1e+34] = np.nan
   
   EANET_ORG = fl_ORG[~np.isnan(fl_ORG)]
   EANET_NH4 = fl_NH4[~np.isnan(fl_NH4)]
   EANET_Na  = fl_Na[~np.isnan(fl_Na)]
   EANET_Cl  = fl_Cl[~np.isnan(fl_Cl)]
   EANET_NO3 = fl_NO3[~np.isnan(fl_NO3)]
   EANET_SO4 = fl_SO4[~np.isnan(fl_SO4)]
   #print(mask_NH4.shape)
   if regionnum==10: 
      field_EC  = np.array([17.0,10.0,3.1,18.0,13.0,2.8,28.0,19.0,3.9,1.2,1.5,1.9,1.8,6.6,1.4,1.5,2.0,2.0,6.4,10.4,7.1])
      field_ORG = np.array([39.0,30.0,12.0,45.0,26.0,15.0,77.0,49.0,21.0,22.0,15.0,12.0,37.0,27.0,20.0,27.6,22.7,18.5,45.2,61.7,31.0])
      field_SO4 = np.array([17.0,15.0, 8.7,27.0,17.0,4.2,34.0,24.0,5.8,11.0,9.3,9.4,19.0,15.0,3.5,15.7,14.4,15.6,22.8,17.8,14.0])
      field_NO3 = np.array([27.0, 21.0, 14.0,28.0,21.0,11.0,28.0,21.0,10.0,3.5,3.4,3.5,3.8,12.0,6.1,5.8,6.2,6.0,17.9,17.5,16.0])
      field_NH4 = np.array([19.0, 13.0, 9.00,24.0,13.0,6.6,28.0,13.0,7.0,5.7,6.9,5.6,7.5,10.0,4.7,8.2,9.4,8.0,8.5,7.6,6.4])
      mask_NH4 = np.concatenate((field_NH4,spartan_NH4,EANET_NH4))
      mask_Na  = np.concatenate((spartan_Na,EANET_Na))
      mask_NO3 = np.concatenate((field_NO3,spartan_NO3,EANET_NO3))
      mask_SO4 = np.concatenate((field_SO4,spartan_SO4,EANET_SO4))
      mask_Cl  = EANET_Cl
      mask_EC  = field_EC
      mask_ORG = np.concatenate((field_ORG,EANET_ORG))
   else: 
      mask_NH4 = np.concatenate((spartan_NH4,EANET_NH4))
      mask_Na  = np.concatenate((spartan_Na,EANET_Na)) 
      mask_NO3 = np.concatenate((spartan_NO3,EANET_NO3))
      mask_SO4 = np.concatenate((spartan_SO4,EANET_SO4))
      mask_Cl  = EANET_Cl 
      mask_ORG = EANET_ORG
if regionnum==5:

   sub_NH4=NH4[(regi==regionnum)]
   sub_Na = Na[(regi==regionnum)]
   sub_NO3=NO3[(regi==regionnum)]
   sub_SO4=SO4[(regi==regionnum)]
   
   fl_NH4=sub_NH4.flatten()
   fl_Na =sub_Na.flatten()
   fl_NO3=sub_NO3.flatten()
   fl_SO4=sub_SO4.flatten()
   # Filter data using np.isnan
   fl_NH4[fl_NH4 == -1e+34] = np.nan
   fl_Na[fl_Na == -1e+34]   = np.nan
   fl_NO3[fl_NO3 == -1e+34] = np.nan
   fl_SO4[fl_SO4 == -1e+34] = np.nan
   
   spartan_NH4 = fl_NH4[~np.isnan(fl_NH4)]
   spartan_Na  = fl_Na[~np.isnan(fl_Na)]
   spartan_NO3 = fl_NO3[~np.isnan(fl_NO3)]
   spartan_SO4 = fl_SO4[~np.isnan(fl_SO4)]

   field_NH4 = np.array([0.04, 0.05, 0.02, 0.19, 0.14, 0.09, 1.23, 6.28, 0.94, 2.2, 0.59, 0.19, 0.30, 3.65, 3.11, 6.35, 7.96])
   field_Na  = np.array([2.76, 2.36, 1.94, 0.04, 0.27, 0.12, 0.05, 0.1, 1.73, 0.33, 0.13])
   field_Cl  = np.array([2.05, 2.20, 1.24, 0.03, 0.18, 0.02, 0.01, 0.04, 0.06, 1.26, 0.29, 0.12])
   field_NO3 = np.array([3.34, 3.88, 2.14, 0.1, 0.02, 0.04, 1.20, 0.79, 0.40, 2.49, 0.35, 1.60, 0.15, 0.43, 4.73, 6.42, 17.29, 11.32])
   field_ORG = np.array([2.62, 3.86, 3.09, 37.66, 11.2, 1.99, 45.76, 15.3, 3.96, 12.91, 17.15, 39.67, 34.42])
   field_SO4 = np.array([3.69, 3.32, 2.12, 0.22, 0.69, 3.06, 0.55, 2.45, 2.05, 2.67, 2.56, 2.94, 0.32, 1.20, 2.05, 1.76, 6.12, 6.67])
   field_EC  = np.array([5.40, 5.84, 6.63, 5.87])

   mask_NH4 = np.concatenate((spartan_NH4,field_NH4))
   mask_Na  = np.concatenate((spartan_Na ,field_Na ))
   mask_NO3 = np.concatenate((spartan_NO3,field_NO3))
   mask_SO4 = np.concatenate((spartan_SO4,field_SO4))
   mask_Cl  = field_Cl
   mask_ORG = field_ORG
   mask_EC  = field_EC

if regionnum==6:
   sub_ORG=ORG[(regi_ORG==regionnum)]
   sub_NH4=NH4[(regi_NH4==regionnum)]
   sub_Na = Na[(regi_Na==regionnum)]
   sub_Cl = Cl[(regi_Cl==regionnum)]
   sub_NO3=NO3[(regi_NO3==regionnum)]
   sub_SO4=SO4[(regi_SO4==regionnum)]
   sub_EC=  EC[(regi_EC==regionnum)]
   
   fl_ORG=sub_ORG.flatten()
   fl_NH4=sub_NH4.flatten()
   fl_Na =sub_Na.flatten()
   fl_Cl =sub_Cl.flatten()
   fl_NO3=sub_NO3.flatten()
   fl_SO4=sub_SO4.flatten()
   fl_EC =sub_EC.flatten()
   # Filter data using np.isnan
   fl_ORG[fl_ORG == -1e+34] = np.nan
   fl_NH4[fl_NH4 == -1e+34] = np.nan
   fl_Na[fl_Na == -1e+34]   = np.nan
   fl_Cl[fl_Cl == -1e+34]   = np.nan
   fl_NO3[fl_NO3 == -1e+34] = np.nan
   fl_SO4[fl_SO4 == -1e+34] = np.nan
   fl_EC[fl_EC == -1e+34]   = np.nan
   
   EMEP_ORG = fl_ORG[~np.isnan(fl_ORG)]
   EMEP_NH4 = 18/14*fl_NH4[~np.isnan(fl_NH4)]
   EMEP_Na  = fl_Na[~np.isnan(fl_Na)]
   EMEP_Cl  = fl_Cl[~np.isnan(fl_Cl)]
   EMEP_NO3 = 62/14*fl_NO3[~np.isnan(fl_NO3)]
   EMEP_SO4 = 3*fl_SO4[~np.isnan(fl_SO4)]
   EMEP_EC  = fl_EC[~np.isnan(fl_EC)]
   
   sube_NH4=NH4e[(regieanet==regionnum)]
   sube_Na = Nae[(regieanet==regionnum)]
   sube_Cl = Cle[(regieanet==regionnum)]
   sube_NO3=NO3e[(regieanet==regionnum)]
   sube_SO4=SO4e[(regieanet==regionnum)]

   fle_NH4=sube_NH4.flatten()
   fle_Na =sube_Na.flatten()
   fle_Cl =sube_Cl.flatten()
   fle_NO3=sube_NO3.flatten()
   fle_SO4=sube_SO4.flatten()
   # Filter data using np.isnan
   fle_NH4[fle_NH4 == -1e+34] = np.nan
   fle_Na[fle_Na == -1e+34]   = np.nan
   fle_Cl[fle_Cl == -1e+34]   = np.nan
   fle_NO3[fle_NO3 == -1e+34] = np.nan
   fle_SO4[fle_SO4 == -1e+34] = np.nan
   
   EANET_NH4 = fle_NH4[~np.isnan(fle_NH4)]
   EANET_Na  = fle_Na[~np.isnan(fle_Na)]
   EANET_Cl  = fle_Cl[~np.isnan(fle_Cl)]
   EANET_NO3 = fle_NO3[~np.isnan(fle_NO3)]
   EANET_SO4 = fle_SO4[~np.isnan(fle_SO4)]
   #print(mask_NH4.shape)
   mask_NH4 = np.concatenate((EMEP_NH4,EANET_NH4))
   mask_Na  = np.concatenate((EMEP_Na,EANET_Na)) 
   mask_NO3 = np.concatenate((EMEP_NO3,EANET_NO3))
   mask_SO4 = np.concatenate((EMEP_SO4,EANET_SO4))
   mask_Cl  =  np.concatenate((EMEP_Cl,EANET_Cl)) 
   mask_ORG = EMEP_ORG
   mask_EC  = EMEP_EC 

if regionnum==7:

   sube_ORG=ORGe[(regia_ORG==regionnum)]
   sube_NH4=NH4e[(regieanet==regionnum)]
   sube_Na = Nae[(regieanet==regionnum)]
   sube_Cl = Cle[(regieanet==regionnum)]
   sube_NO3=NO3e[(regieanet==regionnum)]
   sube_SO4=SO4e[(regieanet==regionnum)]

   fle_ORG=sube_ORG.flatten()
   fle_NH4=sube_NH4.flatten()
   fle_Na =sube_Na.flatten()
   fle_Cl =sube_Cl.flatten()
   fle_NO3=sube_NO3.flatten()
   fle_SO4=sube_SO4.flatten()
   # Filter data using np.isnan
   fle_ORG[fle_ORG == -1e+34] = np.nan
   fle_NH4[fle_NH4 == -1e+34] = np.nan
   fle_Na[fle_Na == -1e+34]   = np.nan
   fle_Cl[fle_Cl == -1e+34]   = np.nan
   fle_NO3[fle_NO3 == -1e+34] = np.nan
   fle_SO4[fle_SO4 == -1e+34] = np.nan

   EANET_ORG = fle_ORG[~np.isnan(fle_ORG)]
   EANET_NH4 = fle_NH4[~np.isnan(fle_NH4)]
   EANET_Na  = fle_Na[~np.isnan(fle_Na)]
   EANET_Cl  = fle_Cl[~np.isnan(fle_Cl)]
   EANET_NO3 = fle_NO3[~np.isnan(fle_NO3)]
   EANET_SO4 = fle_SO4[~np.isnan(fle_SO4)]

   field_NH4 = np.array([0.22, 0.31, 0.36, 0.02, 0.22, 0.11])
   field_Na  = np.array([0.31, 1.71, 2.99, 2.27, 1.68, 0.40])
   field_Cl  = np.array([0.14, 3.09, 4.94, 3.38, 2.47, 0.70])
   field_NO3 = np.array([0.45, 0.73, 0.48, 0.74, 1.03, 0.41])
   field_ORG = np.array([14.5, 2.95])
   field_SO4 = np.array([0.66, 1.08, 1.18, 1.29, 1.76, 0.37])
   field_EC  = np.array([5.99, 2.03])

   mask_NH4 = np.concatenate((field_NH4,EANET_NH4))
   mask_Na  = np.concatenate((field_Na,EANET_Na))
   mask_NO3 = np.concatenate((field_NO3,EANET_NO3))
   mask_SO4 = np.concatenate((field_SO4,EANET_SO4))
   mask_Cl  = np.concatenate((field_Cl,EANET_Cl))
   mask_ORG = np.concatenate((field_ORG,EANET_ORG))
   mask_EC  = field_EC

if regionnum==9:
   sub_ORG=ORG
   sub_NH4=NH4
   sub_Na = Na
   sub_Cl = Cl
   sub_NO3=NO3
   sub_SO4=SO4
   sub_EC=  EC
   
   fl_ORG=sub_ORG.flatten()
   fl_NH4=sub_NH4.flatten()
   fl_Na =sub_Na.flatten()
   fl_Cl =sub_Cl.flatten()
   fl_NO3=sub_NO3.flatten()
   fl_SO4=sub_SO4.flatten()
   fl_EC =sub_EC.flatten()
   # Filter data using np.isnan
   fl_ORG[fl_ORG == -1e+34] = np.nan
   fl_NH4[fl_NH4 == -1e+34] = np.nan
   fl_Na[fl_Na == -1e+34]   = np.nan
   fl_Cl[fl_Cl == -1e+34]   = np.nan
   fl_NO3[fl_NO3 == -1e+34] = np.nan
   fl_SO4[fl_SO4 == -1e+34] = np.nan
   fl_EC[fl_EC == -1e+34]   = np.nan
   
   IMPROVE_ORG = fl_ORG[~np.isnan(fl_ORG)]
   IMPROVE_NH4 = fl_NH4[~np.isnan(fl_NH4)]
   IMPROVE_Na  = fl_Na[~np.isnan(fl_Na)]
   IMPROVE_Cl  = fl_Cl[~np.isnan(fl_Cl)]
   IMPROVE_NO3 = fl_NO3[~np.isnan(fl_NO3)]
   IMPROVE_SO4 = fl_SO4[~np.isnan(fl_SO4)]
   IMPROVE_EC  = fl_EC[~np.isnan(fl_EC)]
   
   #print(mask_NH4.shape)
   mask_NH4 = IMPROVE_NH4
   mask_Na  = IMPROVE_Na 
   mask_NO3 = IMPROVE_NO3
   mask_SO4 = IMPROVE_SO4
   mask_Cl  = IMPROVE_Cl 
   mask_ORG = IMPROVE_ORG
   mask_EC  = IMPROVE_EC

if regionnum==11:
   subs_NH4=NH4s[(regi==regionnum)]
   subs_Na = Nas[(regi==regionnum)]
   subs_NO3=NO3s[(regi==regionnum)]
   subs_SO4=SO4s[(regi==regionnum)]

   fls_NH4=subs_NH4.flatten()
   fls_Na =subs_Na.flatten()
   fls_NO3=subs_NO3.flatten()
   fls_SO4=subs_SO4.flatten()
   # Filter data using np.isnan
   fls_NH4[fls_NH4 == -1e+34] = np.nan
   fls_Na[fls_Na == -1e+34]   = np.nan
   fls_NO3[fls_NO3 == -1e+34] = np.nan
   fls_SO4[fls_SO4 == -1e+34] = np.nan

   spartan_NH4 = fls_NH4[~np.isnan(fls_NH4)]
   spartan_Na  = fls_Na[~np.isnan(fls_Na)]
   spartan_NO3 = fls_NO3[~np.isnan(fls_NO3)]
   spartan_SO4 = fls_SO4[~np.isnan(fls_SO4)]

   sub_ORG=ORG
   sub_NH4=NH4
   sub_Na = Na
   sub_Cl = Cl
   sub_NO3=NO3
   sub_SO4=SO4
   sub_EC=  EC
   
   fl_ORG=sub_ORG.flatten()
   fl_NH4=sub_NH4.flatten()
   fl_Na =sub_Na.flatten()
   fl_Cl =sub_Cl.flatten()
   fl_NO3=sub_NO3.flatten()
   fl_SO4=sub_SO4.flatten()
   fl_EC =sub_EC.flatten()
   # Filter data using np.isnan
   fl_ORG[fl_ORG == -1e+34] = np.nan
   fl_NH4[fl_NH4 == -1e+34] = np.nan
   fl_Na[fl_Na == -1e+34]   = np.nan
   fl_Cl[fl_Cl == -1e+34]   = np.nan
   fl_NO3[fl_NO3 == -1e+34] = np.nan
   fl_SO4[fl_SO4 == -1e+34] = np.nan
   fl_EC[fl_EC == -1e+34]   = np.nan
   
   EPA_ORG = fl_ORG[~np.isnan(fl_ORG)]
   EPA_NH4 = fl_NH4[~np.isnan(fl_NH4)]
   EPA_Na  = fl_Na[~np.isnan(fl_Na)]
   EPA_Cl  = fl_Cl[~np.isnan(fl_Cl)]
   EPA_NO3 = fl_NO3[~np.isnan(fl_NO3)]
   EPA_SO4 = fl_SO4[~np.isnan(fl_SO4)]
   EPA_EC  = fl_EC[~np.isnan(fl_EC)]

   mask_NH4 = np.concatenate((spartan_NH4,EPA_NH4))
   mask_Na  = np.concatenate((spartan_Na,EPA_Na))
   mask_NO3 = np.concatenate((spartan_NO3,EPA_NO3))
   mask_SO4 = np.concatenate((spartan_SO4,EPA_SO4))
   mask_Cl  = EPA_Cl
   mask_ORG = EPA_ORG
   mask_EC  = EPA_EC 

if regionnum==12:
   data_to_box = [mask_SO4]
   data_to_violin = [example_SO4]
if regionnum==1 or regionnum==8:
   data_to_box = [mask_SO4,mask_NO3,mask_NH4,mask_Na,0,0,0]
   data_to_violin = [mask_SO4,mask_NO3,mask_NH4,mask_Na,0,0,0]
if regionnum==2 or regionnum==3 or regionnum==5 or regionnum==6 or regionnum==7 or regionnum==9 or regionnum==10 or regionnum==11:
   data_to_box = [mask_SO4,mask_NO3,mask_NH4,mask_Na,mask_Cl,mask_ORG,mask_EC]
   data_to_violin = [mask_SO4,mask_NO3,mask_NH4,mask_Na,mask_Cl,mask_ORG,mask_EC]
if regionnum==4:
   data_to_box = [mask_SO4,mask_NO3,mask_NH4,mask_Na,mask_Cl,0,0]
   data_to_violin = [mask_SO4,mask_NO3,mask_NH4,mask_Na,mask_Cl,0,0]

fig = plt.figure(1, figsize=(16,9))

# Create an axes instance
ax = fig.add_subplot(111)

# Create the boxplot
## add patch_artist=True option to get fill color

if regionnum<=11:
   bp = ax.boxplot(data_to_box,widths=0.7,whis=[10,90],showfliers=False, patch_artist=True)
   print(mask_SO4.shape) 
   print(mask_NO3.shape) 
   print(mask_NH4.shape) 
   print(mask_Na.shape) 
   
   print(np.nanmean(mask_SO4)) 
   print(np.nanmean(mask_NO3)) 
   print(np.nanmean(mask_NH4)) 
   print(np.nanmean(mask_Na)) 

   if regionnum==4:
      print(mask_Cl.shape) 
      print(np.nanmean(mask_Cl)) 

   if regionnum==2 or regionnum==3 or regionnum==5 or regionnum==6 or regionnum==7 or regionnum==9 or regionnum==10 or regionnum==11:
      print(mask_Cl.shape) 
      print(mask_ORG.shape) 
      print(mask_EC.shape) 
   
      print(np.nanmean(mask_Cl)) 
      print(np.nanmean(mask_ORG)) 
      print(np.nanmean(mask_EC)) 

else:
   bp = ax.boxplot(data_to_box,widths=0.3,whis=[10,90],showfliers=False, patch_artist=True)

if regionnum<=11 :
   colors = ['Red','Brown','Orange','rebeccapurple','Blue','Green','Black']
else:
   colors = ['Black']

for patch, color in zip(bp['boxes'], colors):
    patch.set_color(color)

## change color and linewidth of the whiskers
for whisker in bp['whiskers']:
    whisker.set(color='black', linewidth=1)

## change color and linewidth of the caps
for cap in bp['caps']:
    cap.set(color='black', linewidth=1)

for median in bp['medians']:
    median.set(color='white', linewidth=2)

if regionnum<=11:
   vp = ax.violinplot(data_to_violin,widths=0.7,points=10000,showextrema=False,showmedians=False,showmeans=False)
else:
   vp = ax.violinplot(data_to_violin,widths=0.3,points=10000,showextrema=False,showmedians=False,showmeans=False)

for body in vp['bodies']:
    body.set_facecolor('black')
    body.set_alpha(0.3)

plt.yscale('log')
plt.ylim(1.e-3,1.e2)

if regionnum<=11:
   ax.set_xticklabels(['$SO_{4}^{2-}$','$NO_{3}^{-}$','$NH_{4}^{+}$','$Na^{+}$', '$Cl^{-}$', 'OC','EC'],fontsize=30) 
   plt.tick_params(labelsize=30)
   if regionnum==5 or regionnum==9 or regionnum==11:
      plt.ylabel('Concentration $(\mu g\ m^{-3})$',fontsize=30)
else:
#Hide Axis Including Axis label
   plt.tick_params(top=False,bottom=False,left=False,right=False,labelleft=False,labelbottom=False)

# Save the figure
fig.savefig('Southern_Asia.png', bbox_inches='tight')
plt.show()

#

