#This script contains three functions:
# - convert_T: Converts K into degree Celsius or degree Fahrenheit
# - get_humidity: Calculates vapour pressure and relative humidity
# - HI_NOAA: Calculates NOAA heat index

import sys
import numpy as np
import xarray as xr


#Check temperature units and convert temperature if required
#Input:
#  - T:    Temperature in K
#  - conv: Temperature in which T should be converted
#Output:
#  - T_out: converted temperature (degree Celsius or degree Fahrenheit)
def convert_T(T, conv):
    
    #Check that T is in Kelvin
    check = np.mean(T)<150
    if check==True:
        print('Temperature is not given in Kelvin!')
        sys.exit(1)
    
    #Convert T if required
    if conv=='Celsius':
        T_out = T - 273.15
    elif conv=='Fahrenheit':
        T_out = 9/5 * (T - 273.15) + 32
    else:
        T_out = T
    
    return T_out
    
    
# Calculate vapour pressure and relative humidity from specific humidity
#Input:
#  - huss: specific humidity
#  - p:    pressure (Pa)
#  - T:    Temperature (K)
#Output:
#  - e:  vapour pressure (Pa)
#  - RH: relative humidity
def get_humidity(huss, p, T):

    T_C = convert_T(T, 'Celsius')

    M_H2O = 18.01528/1000 # kg/mol
    M_air = 28.964/1000 # kg/mol for dry air

    # Calculate vapour pressure according to August-Roche-Magnus equation (in Pa)
    e = huss * p * M_air / M_H2O

    # Saturation vapor pressure (in Pa)
    e_s = 610.94 * np.exp(17.625 * T_C / (T_C + 243.04) )
    
    # Relative humidty
    RH = 100 * e / e_s

    #Set RH larger than 100 to 100
    RH = RH.where(RH<=100, 100)
    
    return e, RH


#Calculate Heat index according to NOAA (Rothfusz 1990, Steadman 1979)
#Input:
#  - T:  temperature (K)
#  - RH: relative humidity
#Output:
#  - HI_C: NOAA heat index (degC)
def HI_NOAA(T, RH):

    #Convert T to Fahrenheit
    T_F = convert_T(T, 'Fahrenheit')

    #Calculate heat index
    c    = [-42.379, 2.04901523, 10.14333127, -0.22475541, -0.00683783, -0.05481717, 0.00122874, 0.00085282, -0.00000199]
    HI_F = c[0] + c[1]*T_F + c[2]*RH + c[3]*T_F*RH +c[4]*T_F*T_F + c[5]*RH*RH + \
           c[6]*T_F*T_F*RH + c[7]*T_F*RH*RH + c[8]*T_F*T_F*RH*RH

    #Adjustments to HI
    radicand = (17 - np.abs(T_F - 95)) / 17
    radicand = xr.where(radicand<0, np.NaN, radicand)
    HI_adj1 =  (13 - RH) / 4 * np.sqrt(radicand)
    HI_adj2 =  (RH - 85) * (87 - T_F) / 50
    HI_simple = 0.5 * (T_F + 61.0 + ((T_F - 68.0) * 1.2) + (RH * 0.094))    
    HI_F = xr.where((RH<13) & (T_F>80) & (T_F<112), HI_F - HI_adj1, HI_F) #Adjustment 1
    HI_F = xr.where((RH>85) & (T_F>80) & (T_F<87), HI_F + HI_adj2, HI_F)  #Adjustment 2
    HI_F = xr.where(HI_simple<80, HI_simple, HI_F) #Adjustment 3

    #Convert to degCelsius
    HI_C = (HI_F - 32) * 5/9

    return HI_C
