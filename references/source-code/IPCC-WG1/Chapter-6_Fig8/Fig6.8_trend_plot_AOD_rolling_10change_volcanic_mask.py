import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt

def rolling_window(a, window):
    shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
    strides = a.strides + (a.strides[-1],)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)

ACCESS_CM2_3_file      = Dataset('../input/mixeddata/od550aer_AERmon_ACCESS-CM2_historical_r3i1p1f1_gn_global_mean_185001-201212.nc','r')
BCC_ESM1_1_file        = Dataset('../input/mixeddata/od550aer_AERmon_BCC-ESM1_historical_r1i1p1f1_global_mean_1850-2014.nc','r')
CanESM5_10_file        = Dataset('../input/mixeddata/od550aer_AERmon_CanESM5_historical_r10i1p1f1_gn_global_mean_185001-201212.nc','r')
CanESM5_11_file        = Dataset('../input/mixeddata/od550aer_AERmon_CanESM5_historical_r11i1p1f1_gn_global_mean_185001-201212.nc','r')
CanESM5_12_file        = Dataset('../input/mixeddata/od550aer_AERmon_CanESM5_historical_r12i1p1f1_gn_global_mean_185001-201212.nc','r')
CanESM5_13_file        = Dataset('../input/mixeddata/od550aer_AERmon_CanESM5_historical_r13i1p1f1_gn_global_mean_185001-201212.nc','r')
CanESM5_14_file        = Dataset('../input/mixeddata/od550aer_AERmon_CanESM5_historical_r14i1p1f1_gn_global_mean_185001-201212.nc','r')
CanESM5_15_file        = Dataset('../input/mixeddata/od550aer_AERmon_CanESM5_historical_r15i1p1f1_gn_global_mean_185001-201212.nc','r')
CanESM5_16_file        = Dataset('../input/mixeddata/od550aer_AERmon_CanESM5_historical_r16i1p1f1_gn_global_mean_185001-201212.nc','r')
CanESM5_17_file        = Dataset('../input/mixeddata/od550aer_AERmon_CanESM5_historical_r17i1p1f1_gn_global_mean_185001-201212.nc','r')
CanESM5_18_file        = Dataset('../input/mixeddata/od550aer_AERmon_CanESM5_historical_r18i1p1f1_gn_global_mean_185001-201212.nc','r')
CanESM5_19_file        = Dataset('../input/mixeddata/od550aer_AERmon_CanESM5_historical_r19i1p1f1_gn_global_mean_185001-201212.nc','r')
CESM2_FV2_1_file       = Dataset('../input/mixeddata/od550aer_AERmon_CESM2-FV2_historical_r1i1p1f1_gn_global_mean_185001-201212.nc','r')
CESM2_FV2_2_file       = Dataset('../input/mixeddata/od550aer_AERmon_CESM2-FV2_historical_r2i1p1f1_gn_global_mean_185001-201212.nc','r')
CESM2_FV2_3_file       = Dataset('../input/mixeddata/od550aer_AERmon_CESM2-FV2_historical_r3i1p1f1_gn_global_mean_185001-201212.nc','r')
CESM2_1_file           = Dataset('../input/mixeddata/od550aer_AERmon_CESM2_historical_r1i1p1f1_global_mean_1850-2014.nc','r')
CESM2_2_file           = Dataset('../input/mixeddata/od550aer_AERmon_CESM2_historical_r2i1p1f1_global_mean_1850-2014.nc','r')
CESM2_3_file           = Dataset('../input/mixeddata/od550aer_AERmon_CESM2_historical_r3i1p1f1_global_mean_1850-2014.nc','r')
CESM2_4_file           = Dataset('../input/mixeddata/od550aer_AERmon_CESM2_historical_r4i1p1f1_global_mean_1850-2014.nc','r')
CESM2_5_file           = Dataset('../input/mixeddata/od550aer_AERmon_CESM2_historical_r5i1p1f1_global_mean_1850-2014.nc','r')
CESM2_6_file           = Dataset('../input/mixeddata/od550aer_AERmon_CESM2_historical_r6i1p1f1_global_mean_1850-2014.nc','r')
CESM2_7_file           = Dataset('../input/mixeddata/od550aer_AERmon_CESM2_historical_r7i1p1f1_global_mean_1850-2014.nc','r')
CESM2_8_file           = Dataset('../input/mixeddata/od550aer_AERmon_CESM2_historical_r8i1p1f1_global_mean_1850-2014.nc','r')
CESM2_9_file           = Dataset('../input/mixeddata/od550aer_AERmon_CESM2_historical_r9i1p1f1_global_mean_1850-2014.nc','r')
CESM2_10_file          = Dataset('../input/mixeddata/od550aer_AERmon_CESM2_historical_r10i1p1f1_global_mean_1850-2014.nc','r')
CESM2_11_file          = Dataset('../input/mixeddata/od550aer_AERmon_CESM2_historical_r11i1p1f1_global_mean_1850-2014.nc','r')
CESM2_WACCM_1_file     = Dataset('../input/mixeddata/od550aer_AERmon_CESM2-WACCM_historical_r1i1p1f1_global_mean_1850-2014.nc','r')
CESM2_WACCM_2_file     = Dataset('../input/mixeddata/od550aer_AERmon_CESM2-WACCM_historical_r2i1p1f1_global_mean_1850-2014.nc','r')
CESM2_WACCM_3_file     = Dataset('../input/mixeddata/od550aer_AERmon_CESM2-WACCM_historical_r3i1p1f1_global_mean_1850-2014.nc','r')
CNRM_CM6_1_1_file      = Dataset('../input/mixeddata/od550aer_AERmon_CNRM-CM6-1_historical_r1i1p1f2_global_mean_1850-2014.nc','r')
CNRM_CM6_1_2_file      = Dataset('../input/mixeddata/od550aer_AERmon_CNRM-CM6-1_historical_r2i1p1f2_global_mean_1850-2014.nc','r')
CNRM_CM6_1_3_file      = Dataset('../input/mixeddata/od550aer_AERmon_CNRM-CM6-1_historical_r3i1p1f2_global_mean_1850-2014.nc','r')
CNRM_CM6_1_4_file      = Dataset('../input/mixeddata/od550aer_AERmon_CNRM-CM6-1_historical_r4i1p1f2_global_mean_1850-2014.nc','r')
CNRM_CM6_1_5_file      = Dataset('../input/mixeddata/od550aer_AERmon_CNRM-CM6-1_historical_r5i1p1f2_global_mean_1850-2014.nc','r')
CNRM_CM6_1_6_file      = Dataset('../input/mixeddata/od550aer_AERmon_CNRM-CM6-1_historical_r6i1p1f2_global_mean_1850-2014.nc','r')
CNRM_CM6_1_11_file     = Dataset('../input/mixeddata/od550aer_AERmon_CNRM-CM6-1_historical_r11i1p1f2_global_mean_1850-2014.nc','r')
CNRM_CM6_1_12_file     = Dataset('../input/mixeddata/od550aer_AERmon_CNRM-CM6-1_historical_r12i1p1f2_global_mean_1850-2014.nc','r')
CNRM_CM6_1_13_file     = Dataset('../input/mixeddata/od550aer_AERmon_CNRM-CM6-1_historical_r13i1p1f2_global_mean_1850-2014.nc','r')
CNRM_CM6_1_14_file     = Dataset('../input/mixeddata/od550aer_AERmon_CNRM-CM6-1_historical_r14i1p1f2_global_mean_1850-2014.nc','r')
CNRM_CM6_1_15_file     = Dataset('../input/mixeddata/od550aer_AERmon_CNRM-CM6-1_historical_r15i1p1f2_global_mean_1850-2014.nc','r')
CNRM_CM6_1_16_file     = Dataset('../input/mixeddata/od550aer_AERmon_CNRM-CM6-1_historical_r16i1p1f2_global_mean_1850-2014.nc','r')
CNRM_CM6_1_17_file     = Dataset('../input/mixeddata/od550aer_AERmon_CNRM-CM6-1_historical_r17i1p1f2_global_mean_1850-2014.nc','r')
CNRM_CM6_1_18_file     = Dataset('../input/mixeddata/od550aer_AERmon_CNRM-CM6-1_historical_r18i1p1f2_global_mean_1850-2014.nc','r')
CNRM_CM6_1_19_file     = Dataset('../input/mixeddata/od550aer_AERmon_CNRM-CM6-1_historical_r19i1p1f2_global_mean_1850-2014.nc','r')
CNRM_CM6_1_20_file     = Dataset('../input/mixeddata/od550aer_AERmon_CNRM-CM6-1_historical_r20i1p1f2_global_mean_1850-2014.nc','r')
CNRM_CM6_1_21_file     = Dataset('../input/mixeddata/od550aer_AERmon_CNRM-CM6-1_historical_r21i1p1f2_global_mean_1850-2014.nc','r')
CNRM_CM6_1_22_file     = Dataset('../input/mixeddata/od550aer_AERmon_CNRM-CM6-1_historical_r22i1p1f2_global_mean_1850-2014.nc','r')
CNRM_CM6_1_23_file     = Dataset('../input/mixeddata/od550aer_AERmon_CNRM-CM6-1_historical_r23i1p1f2_global_mean_1850-2014.nc','r')
CNRM_CM6_1_24_file     = Dataset('../input/mixeddata/od550aer_AERmon_CNRM-CM6-1_historical_r24i1p1f2_global_mean_1850-2014.nc','r')
CNRM_CM6_1_25_file     = Dataset('../input/mixeddata/od550aer_AERmon_CNRM-CM6-1_historical_r25i1p1f2_global_mean_1850-2014.nc','r')
CNRM_CM6_1_26_file     = Dataset('../input/mixeddata/od550aer_AERmon_CNRM-CM6-1_historical_r26i1p1f2_global_mean_1850-2014.nc','r')
CNRM_CM6_1_27_file     = Dataset('../input/mixeddata/od550aer_AERmon_CNRM-CM6-1_historical_r27i1p1f2_global_mean_1850-2014.nc','r')
CNRM_CM6_1_28_file     = Dataset('../input/mixeddata/od550aer_AERmon_CNRM-CM6-1_historical_r28i1p1f2_global_mean_1850-2014.nc','r')
CNRM_CM6_1_29_file     = Dataset('../input/mixeddata/od550aer_AERmon_CNRM-CM6-1_historical_r29i1p1f2_global_mean_1850-2014.nc','r')
CNRM_CM6_1_30_file     = Dataset('../input/mixeddata/od550aer_AERmon_CNRM-CM6-1_historical_r30i1p1f2_global_mean_1850-2014.nc','r')
CNRM_ESM2_1_1_file     = Dataset('../input/mixeddata/od550aer_AERmon_CNRM-ESM2-1_historical_r1i1p1f2_global_mean_1850-2014.nc','r')
CNRM_ESM2_1_2_file     = Dataset('../input/mixeddata/od550aer_AERmon_CNRM-ESM2-1_historical_r2i1p1f2_global_mean_1850-2014.nc','r')
CNRM_ESM2_1_3_file     = Dataset('../input/mixeddata/od550aer_AERmon_CNRM-ESM2-1_historical_r3i1p1f2_global_mean_1850-2014.nc','r')
CNRM_ESM2_1_4_file     = Dataset('../input/mixeddata/od550aer_AERmon_CNRM-ESM2-1_historical_r4i1p1f2_global_mean_1850-2014.nc','r')
CNRM_ESM2_1_5_file     = Dataset('../input/mixeddata/od550aer_AERmon_CNRM-ESM2-1_historical_r5i1p1f2_global_mean_1850-2014.nc','r')
CNRM_ESM2_1_8_file     = Dataset('../input/mixeddata/od550aer_AERmon_CNRM-ESM2-1_historical_r8i1p1f2_global_mean_1850-2014.nc','r')
CNRM_ESM2_1_9_file     = Dataset('../input/mixeddata/od550aer_AERmon_CNRM-ESM2-1_historical_r9i1p1f2_global_mean_1850-2014.nc','r')
CNRM_ESM2_1_10_file    = Dataset('../input/mixeddata/od550aer_AERmon_CNRM-ESM2-1_historical_r10i1p1f2_global_mean_1850-2014.nc','r')
E3SM_1_0_1_file        = Dataset('../input/mixeddata/od550aer_AERmon_E3SM-1-0_historical_r1i1p1f1_global_mean_1850-2014.nc','r')
E3SM_1_0_2_file        = Dataset('../input/mixeddata/od550aer_AERmon_E3SM-1-0_historical_r2i1p1f1_global_mean_1850-2014.nc','r')
E3SM_1_0_3_file        = Dataset('../input/mixeddata/od550aer_AERmon_E3SM-1-0_historical_r3i1p1f1_global_mean_1850-2014.nc','r')
E3SM_1_0_4_file        = Dataset('../input/mixeddata/od550aer_AERmon_E3SM-1-0_historical_r4i1p1f1_global_mean_1850-2014.nc','r')
E3SM_1_0_5_file        = Dataset('../input/mixeddata/od550aer_AERmon_E3SM-1-0_historical_r5i1p1f1_global_mean_1850-2014.nc','r')
E3SM_1_1_1_file        = Dataset('../input/mixeddata/od550aer_AERmon_E3SM-1-1_historical_r1i1p1f1_global_mean_1850-2014.nc','r')
E3SM_1_1_ECA_1_file    = Dataset('../input/mixeddata/od550aer_AERmon_E3SM-1-1-ECA_historical_r1i1p1f1_global_mean_1850-2014.nc','r')
GFDL_CM4_1_file        = Dataset('../input/mixeddata/od550aer_AERmon_GFDL-CM4_historical_r1i1p1f1_global_mean_1850-2014.nc','r')
GFDL_ESM4_1_file       = Dataset('../input/mixeddata/od550aer_AERmon_GFDL-ESM4_historical_r1i1p1f1_gr1_global_mean_185001-201212.nc','r')
GISS_E2_1_G_1_file     = Dataset('../input/mixeddata/od550aer_AERmon_GISS-E2-1-G_historical_r1i1p3f1_global_mean_1850-2014.nc','r')
GISS_E2_1_G_2_file     = Dataset('../input/mixeddata/od550aer_AERmon_GISS-E2-1-G_historical_r2i1p3f1_global_mean_1850-2014.nc','r')
GISS_E2_1_G_3_file     = Dataset('../input/mixeddata/od550aer_AERmon_GISS-E2-1-G_historical_r3i1p3f1_global_mean_1850-2014.nc','r')
GISS_E2_1_G_4_file     = Dataset('../input/mixeddata/od550aer_AERmon_GISS-E2-1-G_historical_r4i1p3f1_global_mean_1850-2014.nc','r')
GISS_E2_1_G_5_file     = Dataset('../input/mixeddata/od550aer_AERmon_GISS-E2-1-G_historical_r5i1p3f1_global_mean_1850-2014.nc','r')
GISS_E2_1_G_6_file     = Dataset('../input/mixeddata/od550aer_AERmon_GISS-E2-1-G_historical_r6i1p3f1_global_mean_1850-2014.nc','r')
GISS_E2_1_G_7_file     = Dataset('../input/mixeddata/od550aer_AERmon_GISS-E2-1-G_historical_r7i1p3f1_global_mean_1850-2014.nc','r')
GISS_E2_1_H_1_file     = Dataset('../input/mixeddata/od550aer_AERmon_GISS-E2-1-H_historical_r1i1p3f1_global_mean_1850-2014.nc','r')
GISS_E2_1_H_2_file     = Dataset('../input/mixeddata/od550aer_AERmon_GISS-E2-1-H_historical_r2i1p3f1_global_mean_1850-2014.nc','r')
GISS_E2_1_H_3_file     = Dataset('../input/mixeddata/od550aer_AERmon_GISS-E2-1-H_historical_r3i1p3f1_global_mean_1850-2014.nc','r')
GISS_E2_1_H_4_file     = Dataset('../input/mixeddata/od550aer_AERmon_GISS-E2-1-H_historical_r4i1p3f1_global_mean_1850-2014.nc','r')
GISS_E2_1_H_5_file     = Dataset('../input/mixeddata/od550aer_AERmon_GISS-E2-1-H_historical_r5i1p3f1_global_mean_1850-2014.nc','r')
HadGEM3_GC31_LL_1_file = Dataset('../input/mixeddata/od550aer_AERmon_HadGEM3-GC31-LL_historical_r1i1p1f3_global_mean_1850-2014.nc','r')
HadGEM3_GC31_LL_2_file = Dataset('../input/mixeddata/od550aer_AERmon_HadGEM3-GC31-LL_historical_r2i1p1f3_global_mean_1850-2014.nc','r')
HadGEM3_GC31_LL_3_file = Dataset('../input/mixeddata/od550aer_AERmon_HadGEM3-GC31-LL_historical_r3i1p1f3_global_mean_1850-2014.nc','r')
HadGEM3_GC31_LL_4_file = Dataset('../input/mixeddata/od550aer_AERmon_HadGEM3-GC31-LL_historical_r4i1p1f3_global_mean_1850-2014.nc','r')
HadGEM3_GC31_MM_1_file = Dataset('../input/mixeddata/od550aer_AERmon_HadGEM3-GC31-MM_historical_r1i1p1f3_global_mean_1850-2014.nc','r')
HadGEM3_GC31_MM_2_file = Dataset('../input/mixeddata/od550aer_AERmon_HadGEM3-GC31-MM_historical_r2i1p1f3_global_mean_1850-2014.nc','r')
INM_CM4_8_1_file       = Dataset('../input/mixeddata/od550aer_AERmon_INM-CM4-8_historical_r1i1p1f1_global_mean_1850-2014.nc','r')
IPSL_CM6A_LR_1_file    = Dataset('../input/mixeddata/od550aer_AERmon_IPSL-CM6A-LR_historical_r1i1p1f1_global_mean_1850-2014.nc','r')
IPSL_CM6A_LR_2_file    = Dataset('../input/mixeddata/od550aer_AERmon_IPSL-CM6A-LR_historical_r2i1p1f1_global_mean_1850-2014.nc','r')
IPSL_CM6A_LR_3_file    = Dataset('../input/mixeddata/od550aer_AERmon_IPSL-CM6A-LR_historical_r3i1p1f1_global_mean_1850-2014.nc','r')
IPSL_CM6A_LR_4_file    = Dataset('../input/mixeddata/od550aer_AERmon_IPSL-CM6A-LR_historical_r4i1p1f1_global_mean_1850-2014.nc','r')
IPSL_CM6A_LR_5_file    = Dataset('../input/mixeddata/od550aer_AERmon_IPSL-CM6A-LR_historical_r5i1p1f1_global_mean_1850-2014.nc','r')
IPSL_CM6A_LR_6_file    = Dataset('../input/mixeddata/od550aer_AERmon_IPSL-CM6A-LR_historical_r6i1p1f1_global_mean_1850-2014.nc','r')
IPSL_CM6A_LR_7_file    = Dataset('../input/mixeddata/od550aer_AERmon_IPSL-CM6A-LR_historical_r7i1p1f1_global_mean_1850-2014.nc','r')
IPSL_CM6A_LR_8_file    = Dataset('../input/mixeddata/od550aer_AERmon_IPSL-CM6A-LR_historical_r8i1p1f1_global_mean_1850-2014.nc','r')
IPSL_CM6A_LR_9_file    = Dataset('../input/mixeddata/od550aer_AERmon_IPSL-CM6A-LR_historical_r9i1p1f1_global_mean_1850-2014.nc','r')
IPSL_CM6A_LR_10_file   = Dataset('../input/mixeddata/od550aer_AERmon_IPSL-CM6A-LR_historical_r10i1p1f1_global_mean_1850-2014.nc','r')
IPSL_CM6A_LR_11_file   = Dataset('../input/mixeddata/od550aer_AERmon_IPSL-CM6A-LR_historical_r11i1p1f1_global_mean_1850-2014.nc','r')
IPSL_CM6A_LR_12_file   = Dataset('../input/mixeddata/od550aer_AERmon_IPSL-CM6A-LR_historical_r12i1p1f1_global_mean_1850-2014.nc','r')
IPSL_CM6A_LR_13_file   = Dataset('../input/mixeddata/od550aer_AERmon_IPSL-CM6A-LR_historical_r13i1p1f1_global_mean_1850-2014.nc','r')
IPSL_CM6A_LR_14_file   = Dataset('../input/mixeddata/od550aer_AERmon_IPSL-CM6A-LR_historical_r14i1p1f1_global_mean_1850-2014.nc','r')
IPSL_CM6A_LR_15_file   = Dataset('../input/mixeddata/od550aer_AERmon_IPSL-CM6A-LR_historical_r15i1p1f1_global_mean_1850-2014.nc','r')
IPSL_CM6A_LR_16_file   = Dataset('../input/mixeddata/od550aer_AERmon_IPSL-CM6A-LR_historical_r16i1p1f1_global_mean_1850-2014.nc','r')
IPSL_CM6A_LR_17_file   = Dataset('../input/mixeddata/od550aer_AERmon_IPSL-CM6A-LR_historical_r17i1p1f1_global_mean_1850-2014.nc','r')
IPSL_CM6A_LR_18_file   = Dataset('../input/mixeddata/od550aer_AERmon_IPSL-CM6A-LR_historical_r18i1p1f1_global_mean_1850-2014.nc','r')
IPSL_CM6A_LR_19_file   = Dataset('../input/mixeddata/od550aer_AERmon_IPSL-CM6A-LR_historical_r19i1p1f1_global_mean_1850-2014.nc','r')
IPSL_CM6A_LR_20_file   = Dataset('../input/mixeddata/od550aer_AERmon_IPSL-CM6A-LR_historical_r20i1p1f1_global_mean_1850-2014.nc','r')
IPSL_CM6A_LR_21_file   = Dataset('../input/mixeddata/od550aer_AERmon_IPSL-CM6A-LR_historical_r21i1p1f1_global_mean_1850-2014.nc','r')
IPSL_CM6A_LR_22_file   = Dataset('../input/mixeddata/od550aer_AERmon_IPSL-CM6A-LR_historical_r22i1p1f1_global_mean_1850-2014.nc','r')
IPSL_CM6A_LR_23_file   = Dataset('../input/mixeddata/od550aer_AERmon_IPSL-CM6A-LR_historical_r23i1p1f1_global_mean_1850-2014.nc','r')
IPSL_CM6A_LR_24_file   = Dataset('../input/mixeddata/od550aer_AERmon_IPSL-CM6A-LR_historical_r24i1p1f1_global_mean_1850-2014.nc','r')
IPSL_CM6A_LR_25_file   = Dataset('../input/mixeddata/od550aer_AERmon_IPSL-CM6A-LR_historical_r25i1p1f1_global_mean_1850-2014.nc','r')
IPSL_CM6A_LR_26_file   = Dataset('../input/mixeddata/od550aer_AERmon_IPSL-CM6A-LR_historical_r26i1p1f1_global_mean_1850-2014.nc','r')
IPSL_CM6A_LR_27_file   = Dataset('../input/mixeddata/od550aer_AERmon_IPSL-CM6A-LR_historical_r27i1p1f1_global_mean_1850-2014.nc','r')
IPSL_CM6A_LR_28_file   = Dataset('../input/mixeddata/od550aer_AERmon_IPSL-CM6A-LR_historical_r28i1p1f1_global_mean_1850-2014.nc','r')
IPSL_CM6A_LR_29_file   = Dataset('../input/mixeddata/od550aer_AERmon_IPSL-CM6A-LR_historical_r29i1p1f1_global_mean_1850-2014.nc','r')
IPSL_CM6A_LR_30_file   = Dataset('../input/mixeddata/od550aer_AERmon_IPSL-CM6A-LR_historical_r30i1p1f1_global_mean_1850-2014.nc','r')
IPSL_CM6A_LR_31_file   = Dataset('../input/mixeddata/od550aer_AERmon_IPSL-CM6A-LR_historical_r31i1p1f1_global_mean_1850-2014.nc','r')
IPSL_CM6A_LR_32_file   = Dataset('../input/mixeddata/od550aer_AERmon_IPSL-CM6A-LR_historical_r32i1p1f1_global_mean_1850-2014.nc','r')
KACE_1_0_G_1_file      = Dataset('../input/mixeddata/od550aer_AERmon_KACE-1-0-G_historical_r1i1p1f1_global_mean_1850-2014.nc','r')
MIROC_ES2L_1_file      = Dataset('../input/mixeddata/od550aer_AERmon_MIROC-ES2L_historical_r1i1p1f2_global_mean_1850-2014.nc','r')
MIROC_ES2L_2_file      = Dataset('../input/mixeddata/od550aer_AERmon_MIROC-ES2L_historical_r2i1p1f2_global_mean_1850-2014.nc','r')
MIROC_ES2L_3_file      = Dataset('../input/mixeddata/od550aer_AERmon_MIROC-ES2L_historical_r3i1p1f2_global_mean_1850-2014.nc','r')
MPI_ESM_1_2_HAM_1_file = Dataset('../input/mixeddata/od550aer_AERmon_MPI-ESM-1-2-HAM_historical_r1i1p1f1_gn_global_mean_185001-201212.nc','r')
MPI_ESM_1_2_HAM_2_file = Dataset('../input/mixeddata/od550aer_AERmon_MPI-ESM-1-2-HAM_historical_r2i1p1f1_gn_global_mean_185001-201212.nc','r')
MPI_ESM1_2_LR_1_file   = Dataset('../input/mixeddata/od550aer_AERmon_MPI-ESM1-2-LR_historical_r1i1p1f1_global_mean_1850-2014.nc','r')
MPI_ESM1_2_LR_2_file   = Dataset('../input/mixeddata/od550aer_AERmon_MPI-ESM1-2-LR_historical_r2i1p1f1_global_mean_1850-2014.nc','r')
MPI_ESM1_2_LR_3_file   = Dataset('../input/mixeddata/od550aer_AERmon_MPI-ESM1-2-LR_historical_r3i1p1f1_global_mean_1850-2014.nc','r')
MPI_ESM1_2_LR_4_file   = Dataset('../input/mixeddata/od550aer_AERmon_MPI-ESM1-2-LR_historical_r4i1p1f1_global_mean_1850-2014.nc','r')
MPI_ESM1_2_LR_5_file   = Dataset('../input/mixeddata/od550aer_AERmon_MPI-ESM1-2-LR_historical_r5i1p1f1_global_mean_1850-2014.nc','r')
MPI_ESM1_2_LR_6_file   = Dataset('../input/mixeddata/od550aer_AERmon_MPI-ESM1-2-LR_historical_r6i1p1f1_global_mean_1850-2014.nc','r')
MPI_ESM1_2_LR_7_file   = Dataset('../input/mixeddata/od550aer_AERmon_MPI-ESM1-2-LR_historical_r7i1p1f1_global_mean_1850-2014.nc','r')
MPI_ESM1_2_LR_8_file   = Dataset('../input/mixeddata/od550aer_AERmon_MPI-ESM1-2-LR_historical_r8i1p1f1_global_mean_1850-2014.nc','r')
MPI_ESM1_2_LR_9_file   = Dataset('../input/mixeddata/od550aer_AERmon_MPI-ESM1-2-LR_historical_r9i1p1f1_global_mean_1850-2014.nc','r')
MPI_ESM1_2_LR_10_file  = Dataset('../input/mixeddata/od550aer_AERmon_MPI-ESM1-2-LR_historical_r10i1p1f1_global_mean_1850-2014.nc','r')
MRI_ESM2_0_1_file      = Dataset('../input/mixeddata/od550aer_AERmon_MRI-ESM2-0_historical_r1i1p1f1_gn_global_mean_185001-201212.nc','r')
MRI_ESM2_0_2_file      = Dataset('../input/mixeddata/od550aer_AERmon_MRI-ESM2-0_historical_r2i1p1f1_gn_global_mean_185001-201212.nc','r')
NorESM2_LM_1_file      = Dataset('../input/mixeddata/od550aer_AERmon_NorESM2-LM_historical_r1i1p1f1_gn_global_mean_185001-201212.nc','r')
UKESM1_0_LL_1_file     = Dataset('../input/mixeddata/od550aer_AERmon_UKESM1-0-LL_historical_r1i1p1f2_global_mean_1850-2014.nc','r')
UKESM1_0_LL_2_file     = Dataset('../input/mixeddata/od550aer_AERmon_UKESM1-0-LL_historical_r2i1p1f2_global_mean_1850-2014.nc','r')
UKESM1_0_LL_3_file     = Dataset('../input/mixeddata/od550aer_AERmon_UKESM1-0-LL_historical_r3i1p1f2_global_mean_1850-2014.nc','r')
UKESM1_0_LL_4_file     = Dataset('../input/mixeddata/od550aer_AERmon_UKESM1-0-LL_historical_r4i1p1f2_global_mean_1850-2014.nc','r')
UKESM1_0_LL_5_file     = Dataset('../input/mixeddata/od550aer_AERmon_UKESM1-0-LL_historical_r5i1p1f3_global_mean_1850-2014.nc','r')
UKESM1_0_LL_6_file     = Dataset('../input/mixeddata/od550aer_AERmon_UKESM1-0-LL_historical_r6i1p1f3_global_mean_1850-2014.nc','r')
UKESM1_0_LL_7_file     = Dataset('../input/mixeddata/od550aer_AERmon_UKESM1-0-LL_historical_r7i1p1f3_global_mean_1850-2014.nc','r')
UKESM1_0_LL_8_file     = Dataset('../input/mixeddata/od550aer_AERmon_UKESM1-0-LL_historical_r8i1p1f2_global_mean_1850-2014.nc','r')
UKESM1_0_LL_9_file     = Dataset('../input/mixeddata/od550aer_AERmon_UKESM1-0-LL_historical_r9i1p1f2_global_mean_1850-2014.nc','r')
UKESM1_0_LL_10_file    = Dataset('../input/mixeddata/od550aer_AERmon_UKESM1-0-LL_historical_r10i1p1f2_global_mean_1850-2014.nc','r')
UKESM1_0_LL_11_file    = Dataset('../input/mixeddata/od550aer_AERmon_UKESM1-0-LL_historical_r11i1p1f2_global_mean_1850-2014.nc','r')
UKESM1_0_LL_12_file    = Dataset('../input/mixeddata/od550aer_AERmon_UKESM1-0-LL_historical_r12i1p1f2_global_mean_1850-2014.nc','r')
UKESM1_0_LL_16_file    = Dataset('../input/mixeddata/od550aer_AERmon_UKESM1-0-LL_historical_r16i1p1f2_global_mean_1850-2014.nc','r')
UKESM1_0_LL_17_file    = Dataset('../input/mixeddata/od550aer_AERmon_UKESM1-0-LL_historical_r17i1p1f2_global_mean_1850-2014.nc','r')
UKESM1_0_LL_18_file    = Dataset('../input/mixeddata/od550aer_AERmon_UKESM1-0-LL_historical_r18i1p1f2_global_mean_1850-2014.nc','r')
UKESM1_0_LL_19_file    = Dataset('../input/mixeddata/od550aer_AERmon_UKESM1-0-LL_historical_r19i1p1f2_global_mean_1850-2014.nc','r')

ACCESS_CM2_3 = ACCESS_CM2_3_file.variables["od550aer"] [:,0,0]
ACCESS_CM2_3[ACCESS_CM2_3 == 1e+20] = np.nan

BCC_ESM1_1 = BCC_ESM1_1_file.variables["od550aer"] [:]
BCC_ESM1_1[BCC_ESM1_1 == 1e+20] = np.nan


CanESM5_10 = CanESM5_10_file.variables["od550aer"] [:,0,0]
CanESM5_10[CanESM5_10 == 1e+20] = np.nan

CanESM5_11 = CanESM5_11_file.variables["od550aer"] [:,0,0]
CanESM5_11[CanESM5_11 == 1e+20] = np.nan

CanESM5_12 = CanESM5_12_file.variables["od550aer"] [:,0,0]
CanESM5_12[CanESM5_12 == 1e+20] = np.nan

CanESM5_13 = CanESM5_13_file.variables["od550aer"] [:,0,0]
CanESM5_13[CanESM5_13 == 1e+20] = np.nan

CanESM5_14 = CanESM5_14_file.variables["od550aer"] [:,0,0]
CanESM5_14[CanESM5_14 == 1e+20] = np.nan

CanESM5_15 = CanESM5_15_file.variables["od550aer"] [:,0,0]
CanESM5_15[CanESM5_15 == 1e+20] = np.nan

CanESM5_16 = CanESM5_16_file.variables["od550aer"] [:,0,0]
CanESM5_16[CanESM5_16 == 1e+20] = np.nan

CanESM5_17 = CanESM5_17_file.variables["od550aer"] [:,0,0]
CanESM5_17[CanESM5_17 == 1e+20] = np.nan

CanESM5_18 = CanESM5_18_file.variables["od550aer"] [:,0,0]
CanESM5_18[CanESM5_18 == 1e+20] = np.nan

CanESM5_19 = CanESM5_19_file.variables["od550aer"] [:,0,0]
CanESM5_19[CanESM5_19 == 1e+20] = np.nan

CESM2_FV2_1 = CESM2_FV2_1_file.variables["od550aer"] [:,0,0]
CESM2_FV2_1[CESM2_FV2_1 == 1e+20] = np.nan

CESM2_FV2_2 = CESM2_FV2_2_file.variables["od550aer"] [:,0,0]
CESM2_FV2_2[CESM2_FV2_2 == 1e+20] = np.nan

CESM2_FV2_3 = CESM2_FV2_3_file.variables["od550aer"] [:,0,0]
CESM2_FV2_3[CESM2_FV2_3 == 1e+20] = np.nan

CESM2_1 = CESM2_1_file.variables["od550aer"] [:]
CESM2_1[CESM2_1 == 1e+20] = np.nan

CESM2_2 = CESM2_2_file.variables["od550aer"] [:]
CESM2_2[CESM2_2 == 1e+20] = np.nan

CESM2_3 = CESM2_3_file.variables["od550aer"] [:]
CESM2_3[CESM2_3 == 1e+20] = np.nan

CESM2_4 = CESM2_4_file.variables["od550aer"] [:]
CESM2_4[CESM2_4 == 1e+20] = np.nan

CESM2_5 = CESM2_5_file.variables["od550aer"] [:]
CESM2_5[CESM2_5 == 1e+20] = np.nan

CESM2_6 = CESM2_6_file.variables["od550aer"] [:]
CESM2_6[CESM2_6 == 1e+20] = np.nan

CESM2_7 = CESM2_7_file.variables["od550aer"] [:]
CESM2_7[CESM2_7 == 1e+20] = np.nan

CESM2_8 = CESM2_8_file.variables["od550aer"] [:]
CESM2_8[CESM2_8 == 1e+20] = np.nan

CESM2_9 = CESM2_9_file.variables["od550aer"] [:]
CESM2_9[CESM2_9 == 1e+20] = np.nan

CESM2_10 = CESM2_10_file.variables["od550aer"] [:]
CESM2_10[CESM2_10 == 1e+20] = np.nan

CESM2_11 = CESM2_11_file.variables["od550aer"] [:]
CESM2_11[CESM2_11 == 1e+20] = np.nan

CESM2_WACCM_1 = CESM2_WACCM_1_file.variables["od550aer"] [:]
CESM2_WACCM_1[CESM2_WACCM_1 == 1e+20] = np.nan

CESM2_WACCM_2 = CESM2_WACCM_2_file.variables["od550aer"] [:]
CESM2_WACCM_2[CESM2_WACCM_2 == 1e+20] = np.nan

CESM2_WACCM_3 = CESM2_WACCM_3_file.variables["od550aer"] [:]
CESM2_WACCM_3[CESM2_WACCM_3 == 1e+20] = np.nan

CNRM_CM6_1_1 = CNRM_CM6_1_1_file.variables["od550aer"] [:]
CNRM_CM6_1_1[CNRM_CM6_1_1 == 1e+20] = np.nan

CNRM_CM6_1_2 = CNRM_CM6_1_2_file.variables["od550aer"] [:]
CNRM_CM6_1_2[CNRM_CM6_1_2 == 1e+20] = np.nan

CNRM_CM6_1_3 = CNRM_CM6_1_3_file.variables["od550aer"] [:]
CNRM_CM6_1_3[CNRM_CM6_1_3 == 1e+20] = np.nan

CNRM_CM6_1_4 = CNRM_CM6_1_4_file.variables["od550aer"] [:]
CNRM_CM6_1_4[CNRM_CM6_1_4 == 1e+20] = np.nan

CNRM_CM6_1_5 = CNRM_CM6_1_5_file.variables["od550aer"] [:]
CNRM_CM6_1_5[CNRM_CM6_1_5 == 1e+20] = np.nan

CNRM_CM6_1_6 = CNRM_CM6_1_6_file.variables["od550aer"] [:]
CNRM_CM6_1_6[CNRM_CM6_1_6 == 1e+20] = np.nan

CNRM_CM6_1_11 = CNRM_CM6_1_11_file.variables["od550aer"] [:]
CNRM_CM6_1_11[CNRM_CM6_1_11 == 1e+20] = np.nan

CNRM_CM6_1_12 = CNRM_CM6_1_12_file.variables["od550aer"] [:]
CNRM_CM6_1_12[CNRM_CM6_1_12 == 1e+20] = np.nan

CNRM_CM6_1_13 = CNRM_CM6_1_13_file.variables["od550aer"] [:]
CNRM_CM6_1_13[CNRM_CM6_1_13 == 1e+20] = np.nan

CNRM_CM6_1_14 = CNRM_CM6_1_14_file.variables["od550aer"] [:]
CNRM_CM6_1_14[CNRM_CM6_1_14 == 1e+20] = np.nan

CNRM_CM6_1_15 = CNRM_CM6_1_15_file.variables["od550aer"] [:]
CNRM_CM6_1_15[CNRM_CM6_1_15 == 1e+20] = np.nan

CNRM_CM6_1_16 = CNRM_CM6_1_16_file.variables["od550aer"] [:]
CNRM_CM6_1_16[CNRM_CM6_1_16 == 1e+20] = np.nan

CNRM_CM6_1_17 = CNRM_CM6_1_17_file.variables["od550aer"] [:]
CNRM_CM6_1_17[CNRM_CM6_1_17 == 1e+20] = np.nan

CNRM_CM6_1_18 = CNRM_CM6_1_18_file.variables["od550aer"] [:]
CNRM_CM6_1_18[CNRM_CM6_1_18 == 1e+20] = np.nan

CNRM_CM6_1_19 = CNRM_CM6_1_19_file.variables["od550aer"] [:]
CNRM_CM6_1_19[CNRM_CM6_1_19 == 1e+20] = np.nan

CNRM_CM6_1_20 = CNRM_CM6_1_20_file.variables["od550aer"] [:]
CNRM_CM6_1_20[CNRM_CM6_1_20 == 1e+20] = np.nan

CNRM_CM6_1_21 = CNRM_CM6_1_21_file.variables["od550aer"] [:]
CNRM_CM6_1_21[CNRM_CM6_1_21 == 1e+20] = np.nan

CNRM_CM6_1_22 = CNRM_CM6_1_22_file.variables["od550aer"] [:]
CNRM_CM6_1_22[CNRM_CM6_1_22 == 1e+20] = np.nan

CNRM_CM6_1_23 = CNRM_CM6_1_23_file.variables["od550aer"] [:]
CNRM_CM6_1_23[CNRM_CM6_1_23 == 1e+20] = np.nan

CNRM_CM6_1_24 = CNRM_CM6_1_24_file.variables["od550aer"] [:]
CNRM_CM6_1_24[CNRM_CM6_1_24 == 1e+20] = np.nan

CNRM_CM6_1_25 = CNRM_CM6_1_25_file.variables["od550aer"] [:]
CNRM_CM6_1_25[CNRM_CM6_1_25 == 1e+20] = np.nan

CNRM_CM6_1_26 = CNRM_CM6_1_26_file.variables["od550aer"] [:]
CNRM_CM6_1_26[CNRM_CM6_1_26 == 1e+20] = np.nan

CNRM_CM6_1_27 = CNRM_CM6_1_27_file.variables["od550aer"] [:]
CNRM_CM6_1_27[CNRM_CM6_1_27 == 1e+20] = np.nan

CNRM_CM6_1_28 = CNRM_CM6_1_28_file.variables["od550aer"] [:]
CNRM_CM6_1_28[CNRM_CM6_1_28 == 1e+20] = np.nan

CNRM_CM6_1_29 = CNRM_CM6_1_29_file.variables["od550aer"] [:]
CNRM_CM6_1_29[CNRM_CM6_1_29 == 1e+20] = np.nan

CNRM_CM6_1_30 = CNRM_CM6_1_30_file.variables["od550aer"] [:]
CNRM_CM6_1_30[CNRM_CM6_1_30 == 1e+20] = np.nan

CNRM_ESM2_1_1 = CNRM_ESM2_1_1_file.variables["od550aer"] [:]
CNRM_ESM2_1_1[CNRM_ESM2_1_1 == 1e+20] = np.nan

CNRM_ESM2_1_2 = CNRM_ESM2_1_2_file.variables["od550aer"] [:]
CNRM_ESM2_1_2[CNRM_ESM2_1_2 == 1e+20] = np.nan

CNRM_ESM2_1_3 = CNRM_ESM2_1_3_file.variables["od550aer"] [:]
CNRM_ESM2_1_3[CNRM_ESM2_1_3 == 1e+20] = np.nan

CNRM_ESM2_1_4 = CNRM_ESM2_1_4_file.variables["od550aer"] [:]
CNRM_ESM2_1_4[CNRM_ESM2_1_4 == 1e+20] = np.nan

CNRM_ESM2_1_5 = CNRM_ESM2_1_5_file.variables["od550aer"] [:]
CNRM_ESM2_1_5[CNRM_ESM2_1_5 == 1e+20] = np.nan

CNRM_ESM2_1_8 = CNRM_ESM2_1_8_file.variables["od550aer"] [:]
CNRM_ESM2_1_8[CNRM_ESM2_1_8 == 1e+20] = np.nan

CNRM_ESM2_1_9 = CNRM_ESM2_1_9_file.variables["od550aer"] [:]
CNRM_ESM2_1_9[CNRM_ESM2_1_9 == 1e+20] = np.nan

CNRM_ESM2_1_10 = CNRM_ESM2_1_10_file.variables["od550aer"] [:]
CNRM_ESM2_1_10[CNRM_ESM2_1_10 == 1e+20] = np.nan

E3SM_1_0_1 = E3SM_1_0_1_file.variables["od550aer"] [:]
E3SM_1_0_1[E3SM_1_0_1 == 1e+20] = np.nan

E3SM_1_0_2 = E3SM_1_0_2_file.variables["od550aer"] [:]
E3SM_1_0_2[E3SM_1_0_2 == 1e+20] = np.nan

E3SM_1_0_3 = E3SM_1_0_3_file.variables["od550aer"] [:]
E3SM_1_0_3[E3SM_1_0_3 == 1e+20] = np.nan

E3SM_1_0_4 = E3SM_1_0_4_file.variables["od550aer"] [:]
E3SM_1_0_4[E3SM_1_0_4 == 1e+20] = np.nan

E3SM_1_0_5 = E3SM_1_0_5_file.variables["od550aer"] [:]
E3SM_1_0_5[E3SM_1_0_5 == 1e+20] = np.nan

E3SM_1_1_1 = E3SM_1_1_1_file.variables["od550aer"] [:]
E3SM_1_1_1[E3SM_1_1_1 == 1e+20] = np.nan

E3SM_1_1_ECA_1 = E3SM_1_1_ECA_1_file.variables["od550aer"] [:]
E3SM_1_1_ECA_1[E3SM_1_1_ECA_1 == 1e+20] = np.nan

GFDL_CM4_1 = GFDL_CM4_1_file.variables["od550aer"] [:]
GFDL_CM4_1[GFDL_CM4_1 == 1e+20] = np.nan

GFDL_ESM4_1 = GFDL_ESM4_1_file.variables["od550aer"] [:,0,0]
GFDL_ESM4_1[GFDL_ESM4_1 == 1e+20] = np.nan

GISS_E2_1_G_1 = GISS_E2_1_G_1_file.variables["od550aer"] [:]
GISS_E2_1_G_1[GISS_E2_1_G_1 == 1e+20] = np.nan

GISS_E2_1_G_2 = GISS_E2_1_G_2_file.variables["od550aer"] [:]
GISS_E2_1_G_2[GISS_E2_1_G_2 == 1e+20] = np.nan

GISS_E2_1_G_3 = GISS_E2_1_G_3_file.variables["od550aer"] [:]
GISS_E2_1_G_3[GISS_E2_1_G_3 == 1e+20] = np.nan

GISS_E2_1_G_4 = GISS_E2_1_G_4_file.variables["od550aer"] [:]
GISS_E2_1_G_4[GISS_E2_1_G_4 == 1e+20] = np.nan

GISS_E2_1_G_5 = GISS_E2_1_G_5_file.variables["od550aer"] [:]
GISS_E2_1_G_5[GISS_E2_1_G_5 == 1e+20] = np.nan

GISS_E2_1_G_6 = GISS_E2_1_G_6_file.variables["od550aer"] [:]
GISS_E2_1_G_6[GISS_E2_1_G_6 == 1e+20] = np.nan

GISS_E2_1_G_7 = GISS_E2_1_G_7_file.variables["od550aer"] [:]
GISS_E2_1_G_7[GISS_E2_1_G_7 == 1e+20] = np.nan

GISS_E2_1_H_1 = GISS_E2_1_H_1_file.variables["od550aer"] [:]
GISS_E2_1_H_1[GISS_E2_1_H_1 == 1e+20] = np.nan

GISS_E2_1_H_2 = GISS_E2_1_H_2_file.variables["od550aer"] [:]
GISS_E2_1_H_2[GISS_E2_1_H_2 == 1e+20] = np.nan

GISS_E2_1_H_3 = GISS_E2_1_H_3_file.variables["od550aer"] [:]
GISS_E2_1_H_3[GISS_E2_1_H_3 == 1e+20] = np.nan

GISS_E2_1_H_4 = GISS_E2_1_H_4_file.variables["od550aer"] [:]
GISS_E2_1_H_4[GISS_E2_1_H_4 == 1e+20] = np.nan

GISS_E2_1_H_5 = GISS_E2_1_H_5_file.variables["od550aer"] [:]
GISS_E2_1_H_5[GISS_E2_1_H_5 == 1e+20] = np.nan

HadGEM3_GC31_LL_1 = HadGEM3_GC31_LL_1_file.variables["od550aer"] [:]
HadGEM3_GC31_LL_1[HadGEM3_GC31_LL_1 == 1e+20] = np.nan

HadGEM3_GC31_LL_2 = HadGEM3_GC31_LL_2_file.variables["od550aer"] [:]
HadGEM3_GC31_LL_2[HadGEM3_GC31_LL_2 == 1e+20] = np.nan

HadGEM3_GC31_LL_3 = HadGEM3_GC31_LL_3_file.variables["od550aer"] [:]
HadGEM3_GC31_LL_3[HadGEM3_GC31_LL_3 == 1e+20] = np.nan

HadGEM3_GC31_LL_4 = HadGEM3_GC31_LL_4_file.variables["od550aer"] [:]
HadGEM3_GC31_LL_4[HadGEM3_GC31_LL_4 == 1e+20] = np.nan

HadGEM3_GC31_MM_1 = HadGEM3_GC31_MM_1_file.variables["od550aer"] [:]
HadGEM3_GC31_MM_1[HadGEM3_GC31_MM_1 == 1e+20] = np.nan

HadGEM3_GC31_MM_2 = HadGEM3_GC31_MM_2_file.variables["od550aer"] [:]
HadGEM3_GC31_MM_2[HadGEM3_GC31_MM_2 == 1e+20] = np.nan

INM_CM4_8_1 = INM_CM4_8_1_file.variables["od550aer"] [:]
INM_CM4_8_1[INM_CM4_8_1 == 1e+20] = np.nan

IPSL_CM6A_LR_1 = IPSL_CM6A_LR_1_file.variables["od550aer"] [:]
IPSL_CM6A_LR_1[IPSL_CM6A_LR_1 == 1e+20] = np.nan

IPSL_CM6A_LR_2 = IPSL_CM6A_LR_2_file.variables["od550aer"] [:]
IPSL_CM6A_LR_2[IPSL_CM6A_LR_2 == 1e+20] = np.nan

IPSL_CM6A_LR_3 = IPSL_CM6A_LR_3_file.variables["od550aer"] [:]
IPSL_CM6A_LR_3[IPSL_CM6A_LR_3 == 1e+20] = np.nan

IPSL_CM6A_LR_4 = IPSL_CM6A_LR_4_file.variables["od550aer"] [:]
IPSL_CM6A_LR_4[IPSL_CM6A_LR_4 == 1e+20] = np.nan

IPSL_CM6A_LR_5 = IPSL_CM6A_LR_5_file.variables["od550aer"] [:]
IPSL_CM6A_LR_5[IPSL_CM6A_LR_5 == 1e+20] = np.nan

IPSL_CM6A_LR_6 = IPSL_CM6A_LR_6_file.variables["od550aer"] [:]
IPSL_CM6A_LR_6[IPSL_CM6A_LR_6 == 1e+20] = np.nan

IPSL_CM6A_LR_7 = IPSL_CM6A_LR_7_file.variables["od550aer"] [:]
IPSL_CM6A_LR_7[IPSL_CM6A_LR_7 == 1e+20] = np.nan

IPSL_CM6A_LR_8 = IPSL_CM6A_LR_8_file.variables["od550aer"] [:]
IPSL_CM6A_LR_8[IPSL_CM6A_LR_8 == 1e+20] = np.nan

IPSL_CM6A_LR_9 = IPSL_CM6A_LR_9_file.variables["od550aer"] [:]
IPSL_CM6A_LR_9[IPSL_CM6A_LR_9 == 1e+20] = np.nan

IPSL_CM6A_LR_10 = IPSL_CM6A_LR_10_file.variables["od550aer"] [:]
IPSL_CM6A_LR_10[IPSL_CM6A_LR_10 == 1e+20] = np.nan

IPSL_CM6A_LR_11 = IPSL_CM6A_LR_11_file.variables["od550aer"] [:]
IPSL_CM6A_LR_11[IPSL_CM6A_LR_11 == 1e+20] = np.nan

IPSL_CM6A_LR_12 = IPSL_CM6A_LR_12_file.variables["od550aer"] [:]
IPSL_CM6A_LR_12[IPSL_CM6A_LR_12 == 1e+20] = np.nan

IPSL_CM6A_LR_13 = IPSL_CM6A_LR_13_file.variables["od550aer"] [:]
IPSL_CM6A_LR_13[IPSL_CM6A_LR_13 == 1e+20] = np.nan

IPSL_CM6A_LR_14 = IPSL_CM6A_LR_14_file.variables["od550aer"] [:]
IPSL_CM6A_LR_14[IPSL_CM6A_LR_14 == 1e+20] = np.nan

IPSL_CM6A_LR_15 = IPSL_CM6A_LR_15_file.variables["od550aer"] [:]
IPSL_CM6A_LR_15[IPSL_CM6A_LR_15 == 1e+20] = np.nan

IPSL_CM6A_LR_16 = IPSL_CM6A_LR_16_file.variables["od550aer"] [:]
IPSL_CM6A_LR_16[IPSL_CM6A_LR_16 == 1e+20] = np.nan

IPSL_CM6A_LR_17 = IPSL_CM6A_LR_17_file.variables["od550aer"] [:]
IPSL_CM6A_LR_17[IPSL_CM6A_LR_17 == 1e+20] = np.nan

IPSL_CM6A_LR_18 = IPSL_CM6A_LR_18_file.variables["od550aer"] [:]
IPSL_CM6A_LR_18[IPSL_CM6A_LR_18 == 1e+20] = np.nan

IPSL_CM6A_LR_19 = IPSL_CM6A_LR_19_file.variables["od550aer"] [:]
IPSL_CM6A_LR_19[IPSL_CM6A_LR_19 == 1e+20] = np.nan

IPSL_CM6A_LR_20 = IPSL_CM6A_LR_20_file.variables["od550aer"] [:]
IPSL_CM6A_LR_20[IPSL_CM6A_LR_20 == 1e+20] = np.nan

IPSL_CM6A_LR_21 = IPSL_CM6A_LR_21_file.variables["od550aer"] [:]
IPSL_CM6A_LR_21[IPSL_CM6A_LR_21 == 1e+20] = np.nan

IPSL_CM6A_LR_22 = IPSL_CM6A_LR_22_file.variables["od550aer"] [:]
IPSL_CM6A_LR_22[IPSL_CM6A_LR_22 == 1e+20] = np.nan

IPSL_CM6A_LR_23 = IPSL_CM6A_LR_23_file.variables["od550aer"] [:]
IPSL_CM6A_LR_23[IPSL_CM6A_LR_23 == 1e+20] = np.nan

IPSL_CM6A_LR_24 = IPSL_CM6A_LR_24_file.variables["od550aer"] [:]
IPSL_CM6A_LR_24[IPSL_CM6A_LR_24 == 1e+20] = np.nan

IPSL_CM6A_LR_25 = IPSL_CM6A_LR_25_file.variables["od550aer"] [:]
IPSL_CM6A_LR_25[IPSL_CM6A_LR_25 == 1e+20] = np.nan

IPSL_CM6A_LR_26 = IPSL_CM6A_LR_26_file.variables["od550aer"] [:]
IPSL_CM6A_LR_26[IPSL_CM6A_LR_26 == 1e+20] = np.nan

IPSL_CM6A_LR_27 = IPSL_CM6A_LR_27_file.variables["od550aer"] [:]
IPSL_CM6A_LR_27[IPSL_CM6A_LR_27 == 1e+20] = np.nan

IPSL_CM6A_LR_28 = IPSL_CM6A_LR_28_file.variables["od550aer"] [:]
IPSL_CM6A_LR_28[IPSL_CM6A_LR_28 == 1e+20] = np.nan

IPSL_CM6A_LR_29 = IPSL_CM6A_LR_29_file.variables["od550aer"] [:]
IPSL_CM6A_LR_29[IPSL_CM6A_LR_29 == 1e+20] = np.nan

IPSL_CM6A_LR_30 = IPSL_CM6A_LR_30_file.variables["od550aer"] [:]
IPSL_CM6A_LR_30[IPSL_CM6A_LR_30 == 1e+20] = np.nan

IPSL_CM6A_LR_31 = IPSL_CM6A_LR_31_file.variables["od550aer"] [:]
IPSL_CM6A_LR_31[IPSL_CM6A_LR_31 == 1e+20] = np.nan

IPSL_CM6A_LR_32 = IPSL_CM6A_LR_32_file.variables["od550aer"] [:]
IPSL_CM6A_LR_32[IPSL_CM6A_LR_32 == 1e+20] = np.nan

KACE_1_0_G_1 = KACE_1_0_G_1_file.variables["od550aer"] [:]
KACE_1_0_G_1[KACE_1_0_G_1 == 1e+20] = np.nan

MIROC_ES2L_1 = MIROC_ES2L_1_file.variables["od550aer"] [:]
MIROC_ES2L_1[MIROC_ES2L_1 == 1e+20] = np.nan

MIROC_ES2L_2 = MIROC_ES2L_2_file.variables["od550aer"] [:]
MIROC_ES2L_2[MIROC_ES2L_2 == 1e+20] = np.nan

MIROC_ES2L_3 = MIROC_ES2L_3_file.variables["od550aer"] [:]
MIROC_ES2L_3[MIROC_ES2L_3 == 1e+20] = np.nan

MPI_ESM_1_2_HAM_1 = MPI_ESM_1_2_HAM_1_file.variables["od550aer"] [:,0,0]
MPI_ESM_1_2_HAM_1[MPI_ESM_1_2_HAM_1 == 1e+20] = np.nan

MPI_ESM_1_2_HAM_2 = MPI_ESM_1_2_HAM_2_file.variables["od550aer"] [:,0,0]
MPI_ESM_1_2_HAM_2[MPI_ESM_1_2_HAM_2 == 1e+20] = np.nan

MPI_ESM1_2_LR_1 = MPI_ESM1_2_LR_1_file.variables["od550aer"] [:]
MPI_ESM1_2_LR_1[MPI_ESM1_2_LR_1 == 1e+20] = np.nan

MPI_ESM1_2_LR_2 = MPI_ESM1_2_LR_2_file.variables["od550aer"] [:]
MPI_ESM1_2_LR_2[MPI_ESM1_2_LR_2 == 1e+20] = np.nan

MPI_ESM1_2_LR_3 = MPI_ESM1_2_LR_3_file.variables["od550aer"] [:]
MPI_ESM1_2_LR_3[MPI_ESM1_2_LR_3 == 1e+20] = np.nan

MPI_ESM1_2_LR_4 = MPI_ESM1_2_LR_4_file.variables["od550aer"] [:]
MPI_ESM1_2_LR_4[MPI_ESM1_2_LR_4 == 1e+20] = np.nan

MPI_ESM1_2_LR_5 = MPI_ESM1_2_LR_5_file.variables["od550aer"] [:]
MPI_ESM1_2_LR_5[MPI_ESM1_2_LR_5 == 1e+20] = np.nan

MPI_ESM1_2_LR_6 = MPI_ESM1_2_LR_6_file.variables["od550aer"] [:]
MPI_ESM1_2_LR_6[MPI_ESM1_2_LR_6 == 1e+20] = np.nan

MPI_ESM1_2_LR_7 = MPI_ESM1_2_LR_7_file.variables["od550aer"] [:]
MPI_ESM1_2_LR_7[MPI_ESM1_2_LR_7 == 1e+20] = np.nan

MPI_ESM1_2_LR_8 = MPI_ESM1_2_LR_8_file.variables["od550aer"] [:]
MPI_ESM1_2_LR_8[MPI_ESM1_2_LR_8 == 1e+20] = np.nan

MPI_ESM1_2_LR_9 = MPI_ESM1_2_LR_9_file.variables["od550aer"] [:]
MPI_ESM1_2_LR_9[MPI_ESM1_2_LR_9 == 1e+20] = np.nan

MPI_ESM1_2_LR_10 = MPI_ESM1_2_LR_10_file.variables["od550aer"] [:]
MPI_ESM1_2_LR_10[MPI_ESM1_2_LR_10 == 1e+20] = np.nan

MRI_ESM2_0_1 = MRI_ESM2_0_1_file.variables["od550aer"] [:,0,0]
MRI_ESM2_0_1[MRI_ESM2_0_1 == 1e+20] = np.nan

MRI_ESM2_0_2 = MRI_ESM2_0_2_file.variables["od550aer"] [:,0,0]
MRI_ESM2_0_2[MRI_ESM2_0_2 == 1e+20] = np.nan

NorESM2_LM_1 = NorESM2_LM_1_file.variables["od550aer"] [:,0,0]
NorESM2_LM_1[NorESM2_LM_1 == 1e+20] = np.nan

UKESM1_0_LL_1 = UKESM1_0_LL_1_file.variables["od550aer"] [:]
UKESM1_0_LL_1[UKESM1_0_LL_1 == 1e+20] = np.nan

UKESM1_0_LL_2 = UKESM1_0_LL_2_file.variables["od550aer"] [:]
UKESM1_0_LL_2[UKESM1_0_LL_2 == 1e+20] = np.nan

UKESM1_0_LL_3 = UKESM1_0_LL_3_file.variables["od550aer"] [:]
UKESM1_0_LL_3[UKESM1_0_LL_3 == 1e+20] = np.nan

UKESM1_0_LL_4 = UKESM1_0_LL_4_file.variables["od550aer"] [:]
UKESM1_0_LL_4[UKESM1_0_LL_4 == 1e+20] = np.nan

UKESM1_0_LL_5 = UKESM1_0_LL_5_file.variables["od550aer"] [:]
UKESM1_0_LL_5[UKESM1_0_LL_5 == 1e+20] = np.nan

UKESM1_0_LL_6 = UKESM1_0_LL_6_file.variables["od550aer"] [:]
UKESM1_0_LL_6[UKESM1_0_LL_6 == 1e+20] = np.nan

UKESM1_0_LL_7 = UKESM1_0_LL_7_file.variables["od550aer"] [:]
UKESM1_0_LL_7[UKESM1_0_LL_7 == 1e+20] = np.nan

UKESM1_0_LL_8 = UKESM1_0_LL_8_file.variables["od550aer"] [:]
UKESM1_0_LL_8[UKESM1_0_LL_8 == 1e+20] = np.nan

UKESM1_0_LL_9 = UKESM1_0_LL_9_file.variables["od550aer"] [:]
UKESM1_0_LL_9[UKESM1_0_LL_9 == 1e+20] = np.nan

UKESM1_0_LL_10 = UKESM1_0_LL_10_file.variables["od550aer"] [:]
UKESM1_0_LL_10[UKESM1_0_LL_10 == 1e+20] = np.nan

UKESM1_0_LL_11 = UKESM1_0_LL_11_file.variables["od550aer"] [:]
UKESM1_0_LL_11[UKESM1_0_LL_11 == 1e+20] = np.nan

UKESM1_0_LL_12 = UKESM1_0_LL_12_file.variables["od550aer"] [:]
UKESM1_0_LL_12[UKESM1_0_LL_12 == 1e+20] = np.nan

UKESM1_0_LL_16 = UKESM1_0_LL_16_file.variables["od550aer"] [:]
UKESM1_0_LL_16[UKESM1_0_LL_16 == 1e+20] = np.nan

UKESM1_0_LL_17 = UKESM1_0_LL_17_file.variables["od550aer"] [:]
UKESM1_0_LL_17[UKESM1_0_LL_17 == 1e+20] = np.nan

UKESM1_0_LL_18 = UKESM1_0_LL_18_file.variables["od550aer"] [:]
UKESM1_0_LL_18[UKESM1_0_LL_18 == 1e+20] = np.nan

UKESM1_0_LL_19 = UKESM1_0_LL_19_file.variables["od550aer"] [:]
UKESM1_0_LL_19[UKESM1_0_LL_19 == 1e+20] = np.nan

ACCESS_ave=ACCESS_CM2_3
BCC_ave=BCC_ESM1_1
CanESM5_ave=(CanESM5_10+CanESM5_11+CanESM5_12+CanESM5_13+CanESM5_14+CanESM5_15+CanESM5_16+CanESM5_17+CanESM5_18+CanESM5_19)/10.
CESM2_FV2_ave=(CESM2_FV2_1+CESM2_FV2_3)/2.
CESM2_ave=(CESM2_1+CESM2_2+CESM2_3+CESM2_4+CESM2_5+CESM2_6+CESM2_7+CESM2_8+CESM2_9+CESM2_10+CESM2_11)/11.
CESM2_WACCM_ave=(CESM2_WACCM_1+CESM2_WACCM_2+CESM2_WACCM_3)/3.
CNRM_CM6_ave=(CNRM_CM6_1_1+CNRM_CM6_1_2+CNRM_CM6_1_3+CNRM_CM6_1_4+CNRM_CM6_1_5+CNRM_CM6_1_6+CNRM_CM6_1_11+CNRM_CM6_1_12+CNRM_CM6_1_13+CNRM_CM6_1_14+CNRM_CM6_1_15+CNRM_CM6_1_16+CNRM_CM6_1_17+CNRM_CM6_1_18+CNRM_CM6_1_19+CNRM_CM6_1_20+CNRM_CM6_1_21+CNRM_CM6_1_22+CNRM_CM6_1_23+CNRM_CM6_1_24+CNRM_CM6_1_25+CNRM_CM6_1_26+CNRM_CM6_1_27+CNRM_CM6_1_28+CNRM_CM6_1_29+CNRM_CM6_1_30)/26.
CNRM_ESM2_ave=(CNRM_ESM2_1_1+CNRM_ESM2_1_2+CNRM_ESM2_1_3+CNRM_ESM2_1_4+CNRM_ESM2_1_5+CNRM_ESM2_1_8+CNRM_ESM2_1_9+CNRM_ESM2_1_10)/8.
E3SM_ave=(E3SM_1_0_1+E3SM_1_0_2+E3SM_1_0_3+E3SM_1_0_4+E3SM_1_0_5)/5.
GFDL_CM4_ave=GFDL_CM4_1
GFDL_ESM4_ave=GFDL_ESM4_1
GISS_E2_1_G_ave=(GISS_E2_1_G_1+GISS_E2_1_G_2+GISS_E2_1_G_3+GISS_E2_1_G_4+GISS_E2_1_G_5+GISS_E2_1_G_6)/6.
GISS_E2_1_H_ave=(GISS_E2_1_H_1+GISS_E2_1_H_2+GISS_E2_1_H_3+GISS_E2_1_H_4+GISS_E2_1_H_5)/5.
HadGEM3_LL_ave=(HadGEM3_GC31_LL_1+HadGEM3_GC31_LL_2+HadGEM3_GC31_LL_3+HadGEM3_GC31_LL_4)/4.
HadGEM3_MM_ave=(HadGEM3_GC31_MM_1+HadGEM3_GC31_MM_2)/2.
INM_CM4_ave=INM_CM4_8_1
IPSL_CM6A_ave=(IPSL_CM6A_LR_1+IPSL_CM6A_LR_2+IPSL_CM6A_LR_3+IPSL_CM6A_LR_4+IPSL_CM6A_LR_5+IPSL_CM6A_LR_6+IPSL_CM6A_LR_7+IPSL_CM6A_LR_8+IPSL_CM6A_LR_9+IPSL_CM6A_LR_10+IPSL_CM6A_LR_11+IPSL_CM6A_LR_12+IPSL_CM6A_LR_13+IPSL_CM6A_LR_14+IPSL_CM6A_LR_15+IPSL_CM6A_LR_16+IPSL_CM6A_LR_17+IPSL_CM6A_LR_18+IPSL_CM6A_LR_19+IPSL_CM6A_LR_20+IPSL_CM6A_LR_21+IPSL_CM6A_LR_22+IPSL_CM6A_LR_23+IPSL_CM6A_LR_24+IPSL_CM6A_LR_25+IPSL_CM6A_LR_26+IPSL_CM6A_LR_27+IPSL_CM6A_LR_28+IPSL_CM6A_LR_29+IPSL_CM6A_LR_30+IPSL_CM6A_LR_31+IPSL_CM6A_LR_32)/32.
KACE_ave=KACE_1_0_G_1
MIROC_ave=(MIROC_ES2L_1+MIROC_ES2L_2+MIROC_ES2L_3)/3.
MPI_HAM_ave=(MPI_ESM_1_2_HAM_1+MPI_ESM_1_2_HAM_2)/2.
MPI_LR_ave=(MPI_ESM1_2_LR_1+MPI_ESM1_2_LR_2+MPI_ESM1_2_LR_3+MPI_ESM1_2_LR_4+MPI_ESM1_2_LR_5+MPI_ESM1_2_LR_6+MPI_ESM1_2_LR_7+MPI_ESM1_2_LR_8+MPI_ESM1_2_LR_9+MPI_ESM1_2_LR_10)/10.
MRI_ave=(MRI_ESM2_0_1+MRI_ESM2_0_2)/2.
NorESM2_ave=NorESM2_LM_1
UKESM1_ave=(UKESM1_0_LL_1+UKESM1_0_LL_2+UKESM1_0_LL_3+UKESM1_0_LL_4+UKESM1_0_LL_5+UKESM1_0_LL_6+UKESM1_0_LL_7+UKESM1_0_LL_8+UKESM1_0_LL_9+UKESM1_0_LL_10+UKESM1_0_LL_11+UKESM1_0_LL_12+UKESM1_0_LL_16+UKESM1_0_LL_17+UKESM1_0_LL_18+UKESM1_0_LL_19)/16.
#
volcanic=[3,4,5,11,12,13,23,24,25,26,32,33,34,35,36,37,38,40,41,52,53,54,57,58,62,63,64,65,74,75,82,83,84,105,106,107,108,113,114,115,130,131,132,133,134,141,142,143,144,161,162]
for v in volcanic:
   BCC_ave[v]=np.nan
   MRI_ave[v]=np.nan
   MPI_HAM_ave[v]=np.nan
   MPI_LR_ave[v]=np.nan
   CESM2_WACCM_ave[v]=np.nan
#
#multimodel mean
MODELS_AVE=np.nanmean((ACCESS_ave,BCC_ave,CanESM5_ave,CESM2_FV2_ave,CESM2_ave,CESM2_WACCM_ave,CNRM_CM6_ave,CNRM_ESM2_ave,E3SM_ave,GFDL_CM4_ave,GFDL_ESM4_ave,GISS_E2_1_G_ave,GISS_E2_1_H_ave,HadGEM3_LL_ave,HadGEM3_MM_ave,INM_CM4_ave,IPSL_CM6A_ave,KACE_ave,MIROC_ave,MPI_HAM_ave,MPI_LR_ave,MRI_ave,NorESM2_ave,UKESM1_ave),axis=0)
#
one=ACCESS_ave*0. + 1.
print(one)
ACCESS_pre     =one*np.nanmean(ACCESS_ave[0:9])
BCC_pre        =one*np.nanmean(BCC_ave[0:9])
CanESM5_pre    =one*np.nanmean(CanESM5_ave[0:9])
CESM2_FV2_pre  =one*np.nanmean(CESM2_FV2_ave[0:9])
CESM2_pre      =one*np.nanmean(CESM2_ave[0:9])
CESM2_WACCM_pre=one*np.nanmean(CESM2_WACCM_ave[0:9])
CNRM_CM6_pre   =one*np.nanmean(CNRM_CM6_ave[0:9])
CNRM_ESM2_pre  =one*np.nanmean(CNRM_ESM2_ave[0:9])
E3SM_pre       =one*np.nanmean(E3SM_ave[0:9])
GFDL_CM4_pre   =one*np.nanmean(GFDL_CM4_ave[0:9])
GFDL_ESM4_pre  =one*np.nanmean(GFDL_ESM4_ave[0:9])
GISS_E2_1_G_pre=one*np.nanmean(GISS_E2_1_G_ave[0:9])
GISS_E2_1_H_pre=one*np.nanmean(GISS_E2_1_H_ave[0:9])
HadGEM3_LL_pre =one*np.nanmean(HadGEM3_LL_ave[0:9])
HadGEM3_MM_pre =one*np.nanmean(HadGEM3_MM_ave[0:9])
INM_CM4_pre    =one*np.nanmean(INM_CM4_ave[0:9])
IPSL_CM6A_pre  =one*np.nanmean(IPSL_CM6A_ave[0:9])
KACE_pre       =one*np.nanmean(KACE_ave[0:9])
MIROC_pre      =one*np.nanmean(MIROC_ave[0:9])
MPI_HAM_pre    =one*np.nanmean(MPI_HAM_ave[0:9])
MPI_LR_pre     =one*np.nanmean(MPI_LR_ave[0:9])
MRI_pre        =one*np.nanmean(MRI_ave[0:9])
NorESM2_pre    =one*np.nanmean(NorESM2_ave[0:9])
UKESM1_pre     =one*np.nanmean(UKESM1_ave[0:9])
MODELS_PRE     =one*np.nanmean(MODELS_AVE[0:9])
#
ACCESS=ACCESS_ave-ACCESS_pre
BCC=BCC_ave-BCC_pre
CanESM5=CanESM5_ave-CanESM5_pre
CESM2_FV2=CESM2_FV2_ave-CESM2_FV2_pre
CESM2=CESM2_ave-CESM2_pre
CESM2_WACCM=CESM2_WACCM_ave-CESM2_WACCM_pre
CNRM_CM6=CNRM_CM6_ave-CNRM_CM6_pre
CNRM_ESM2=CNRM_ESM2_ave-CNRM_ESM2_pre
E3SM=E3SM_ave-E3SM_pre
GFDL_CM4=GFDL_CM4_ave-GFDL_CM4_pre
GFDL_ESM4=GFDL_ESM4_ave-GFDL_ESM4_pre
GISS_E2_1_G=GISS_E2_1_G_ave-GISS_E2_1_G_pre
GISS_E2_1_H=GISS_E2_1_H_ave-GISS_E2_1_H_pre
HadGEM3_LL=HadGEM3_LL_ave-HadGEM3_LL_pre
HadGEM3_MM=HadGEM3_MM_ave-HadGEM3_MM_pre
INM_CM4=INM_CM4_ave-INM_CM4_pre
IPSL_CM6A=IPSL_CM6A_ave-IPSL_CM6A_pre
KACE=KACE_ave-KACE_pre
MIROC=MIROC_ave-MIROC_pre
MPI_HAM=MPI_HAM_ave-MPI_HAM_pre
MPI_LR=MPI_LR_ave-MPI_LR_pre
MRI=MRI_ave-MRI_pre
NorESM2=NorESM2_ave-NorESM2_pre
UKESM1=UKESM1_ave-UKESM1_pre
MODELS=MODELS_AVE-MODELS_PRE
#
R_ACCESS=np.nanmean(rolling_window(ACCESS, 10), -1)
R_BCC=np.nanmean(rolling_window(BCC, 10), -1)
R_CanESM5=np.nanmean(rolling_window(CanESM5, 10), -1)
R_CESM2_FV2=np.nanmean(rolling_window(CESM2_FV2, 10), -1)
R_CESM2=np.nanmean(rolling_window(CESM2, 10), -1)
R_CESM2_WACCM=np.nanmean(rolling_window(CESM2_WACCM, 10), -1)
R_CNRM_CM6=np.nanmean(rolling_window(CNRM_CM6, 10), -1)
R_CNRM_ESM2=np.nanmean(rolling_window(CNRM_ESM2, 10), -1)
R_E3SM=np.nanmean(rolling_window(E3SM, 10), -1)
R_GFDL_CM4=np.nanmean(rolling_window(GFDL_CM4, 10), -1)
R_GFDL_ESM4=np.nanmean(rolling_window(GFDL_ESM4, 10), -1)
R_GISS_E2_1_G=np.nanmean(rolling_window(GISS_E2_1_G, 10), -1)
R_GISS_E2_1_H=np.nanmean(rolling_window(GISS_E2_1_H, 10), -1)
R_HadGEM3_LL=np.nanmean(rolling_window(HadGEM3_LL, 10), -1)
R_HadGEM3_MM=np.nanmean(rolling_window(HadGEM3_MM, 10), -1)
R_INM_CM4=np.nanmean(rolling_window(INM_CM4, 10), -1)
R_IPSL_CM6A=np.nanmean(rolling_window(IPSL_CM6A, 10), -1)
R_KACE=np.nanmean(rolling_window(KACE, 10), -1)
R_MIROC=np.nanmean(rolling_window(MIROC, 10), -1)
R_MPI_HAM=np.nanmean(rolling_window(MPI_HAM, 10), -1)
R_MPI_LR=np.nanmean(rolling_window(MPI_LR, 10), -1)
R_MRI=np.nanmean(rolling_window(MRI, 10), -1)
R_NorESM2=np.nanmean(rolling_window(NorESM2, 10), -1)
R_UKESM1=np.nanmean(rolling_window(UKESM1, 10), -1)
R_MODELS=np.nanmean(rolling_window(MODELS, 10), -1)
#
plt.figure(figsize=(16,9))
plt.subplots_adjust(bottom=0.14)
plt.rcParams.update({'font.size': 30})
plt.tick_params(top='off', right='off', which='both')
plt.tick_params(axis='x', pad=20)
plt.tick_params(axis='y', pad=10)
plt.tick_params(size=6,width=3, which='both')
#
xp = np.arange(1855,2011, 1.0)
print(len(xp))
print(len(CanESM5))
#
plt.ioff()
fig = plt.figure(1)
palette = plt.get_cmap('tab20')
plt.plot(xp,R_ACCESS,      c='grey' , linewidth=2.0,label='CMIP6 models') #,label='ACCESS-CM2')
plt.plot(xp,R_BCC,         c='grey' , linewidth=2.0) #,label='BCC-ESM1')
plt.plot(xp,R_CanESM5,     c='grey' , linewidth=2.0) #,label='CanESM5')
plt.plot(xp,R_CESM2_FV2,   c='grey' , linewidth=2.0) #,label='CESM2-FV2')
plt.plot(xp,R_CESM2,       c='grey' , linewidth=2.0) #,label='CESM2')
plt.plot(xp,R_CESM2_WACCM, c='grey' , linewidth=2.0) #,label='CESM2-WACCM')
plt.plot(xp,R_CNRM_CM6,    c='grey' , linewidth=2.0) #,label='CNRM-CM6')
plt.plot(xp,R_CNRM_ESM2,   c='grey' , linewidth=2.0) #,label='CNRM-ESM2')
plt.plot(xp,R_E3SM,        c='grey' , linewidth=2.0) #,label='E3SM-1-0')
plt.plot(xp,R_GFDL_CM4,    c='grey' , linewidth=2.0) #,label='GFDL_CM4')
plt.plot(xp,R_GFDL_ESM4,   c='grey' , linewidth=2.0) #,label='GFDL-ESM4')
plt.plot(xp,R_GISS_E2_1_G, c='grey' , linewidth=2.0) #,label='GISS-E2-1-G')
plt.plot(xp,R_GISS_E2_1_H, c='grey' , linewidth=2.0) #,label='GISS-E2-1-H')
plt.plot(xp,R_HadGEM3_LL,  c='grey' , linewidth=2.0) #,label='HadGEM3-GC31-LL')
plt.plot(xp,R_HadGEM3_MM,  c='grey' , linewidth=2.0) #,label='HadGEM3-GC31-MM')
plt.plot(xp,R_INM_CM4,     c='grey' , linewidth=2.0) #,label='INM-CM4-8')
plt.plot(xp,R_IPSL_CM6A,   c='grey' , linewidth=2.0) #,label='IPSL-CM6A-LR')
plt.plot(xp,R_KACE,        c='grey' , linewidth=2.0) #,label='KACE-1-0_G')
plt.plot(xp,R_MIROC,       c='grey' , linewidth=2.0) #,label='MIROC-ES2L')
plt.plot(xp,R_MPI_HAM,     c='grey' , linewidth=2.0) #,label='MPI-ESM-1-2-HAM')
plt.plot(xp,R_MPI_LR,      c='grey' , linewidth=2.0) #,label='MPI-ESM1-2-LR')
plt.plot(xp,R_MRI,         c='grey' , linewidth=2.0) #,label='MRI-ESM2-0')
plt.plot(xp,R_NorESM2,     c='grey' , linewidth=2.0) #,label='NorESM2-LM')
plt.plot(xp,R_UKESM1,      c='grey' , linewidth=2.0) #,label='UKESM1_0_LL')
plt.plot(xp,R_MODELS,      c='black', linewidth=3.0,label='Multimodel mean') #,label='Multimodel mean')
plt.legend(bbox_to_anchor=(0.02, 0.75, 0.35,0.02), loc='lower left',
           ncol=1, mode="expand", borderaxespad=0.,fontsize=20)
x1,x2,y1,y2 = plt.axis()
cmin=-0.01
cmax=0.1
chead=0.95*cmax
plt.axis((1855,2010,cmin,cmax))
plt.xlabel('Year',fontweight='bold')
plt.ylabel('AOD550 Change',fontweight='bold')
fig.savefig('AOD_trend.png',bbox_inches='tight')
plt.show()
 


