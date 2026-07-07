"""
Module for calculating metrics from CH4.

Author: Bill Collins (UK)
Adapted by Chris Smith
"""

import numpy as np
from .constants import M_ATMOS, M_AIR, M_CH4
from fair.forcing.ghg import meinshausen
from fair.defaults.thermal import q, d


# TODO: make better variable names
def ch4_analytical(H, co2=409.85, ch4=1866.3275, n2o=332.091, ch4_ra=-0.14, ch4_o3=1.4e-4, ch4_h2o=0.00004, d=d, q=q, alpha_ch4=11.8):
    """Calculates metrics for a 1 ppb CH4 perturbation.
    
    Inputs:
    -------
    H : float or `np.ndarray`
        time horizon(s) of interest
    co2 : float, optional
        baseline concentrations of CO2, ppmv
    ch4: float, optional
        baseline concentrations of CH4, ppbv
    n2o : float, optional
        baseline concentrations of N2O, ppbv
    ch4_ra : float, optional
        tropospheric rapid adjustment enhancement of CH4 forcing
    ch4_o3 : float, optional
        radiative efficiency increase of CH4 emissions due to O3 formation, W m-2 (ppb CH4)-1
    ch4_h2o : float, optional
        radiative efficiency increase of CH4 emissions due to stratospheric H2O formation, W m-2 (ppb CH4)-1 
    d : `np.ndarray`, optional
        2-element array of fast and slow timescales to climate warming impulse response function
    q : `np.ndarray`, optional
        2-element array of fast and slow contributions to climate warming impulse response function
    alpha_ch4 : float
        perturbation lifetime of CH4, years
    
    Returns:
    --------
    (rf, agwp, agtp, iagtp) : tuple of float or `np.ndarray`
        rf : Effective radiative forcing from a 1 ppbv increase in CH4
        agwp : Absolute global warming potential of CH4, W m-2 yr kg-1
        agtp : Absolute global temperature change potential of CH4, K kg-1
        iagtp : Integrated absolute global temperature change potential, K kg-1
    """
    re = meinshausen(np.array([co2, ch4+1, n2o]), np.array([co2, ch4, n2o]), scale_F2x=False)[1] * (1+ch4_ra)
    ppb2kg = 1e-9*(M_CH4/M_AIR)*M_ATMOS
    A = (re + ch4_o3 + ch4_h2o)/ppb2kg

    agtp = H*0.
    iagtp = H*0.
    rf = H*0.
    agwp = H*0.

    rf = rf+A*np.exp(-H/(alpha_ch4))
    agwp = agwp+A*alpha_ch4*(1-np.exp(-H/alpha_ch4))
    for j in np.arange(2):
        agtp = agtp+A*alpha_ch4*q[j] *\
            (np.exp(-H/(alpha_ch4)) -
             np.exp(-H/d[j]))/(alpha_ch4-d[j])
        iagtp = iagtp+A*alpha_ch4*q[j] * \
            (alpha_ch4*(1-np.exp(-H/(alpha_ch4))) -
             d[j]*(1-np.exp(-H/d[j]))) / \
            (alpha_ch4-d[j])
    return rf, agwp, agtp, iagtp
