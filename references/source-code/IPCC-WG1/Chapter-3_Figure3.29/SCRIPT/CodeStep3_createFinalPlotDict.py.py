#********************************************************************************
#
# CreateFinalPlotDict.py
#
# Written by Krishna AchutaRao
#
#            05 February 2021
#
# IMPORTANT: RUN THIS CODE AFTER VISUAL CHECK OF DEDRIFTED DATA PLOTS
#
# This code just creates a dictionary with just the models and realizations that
# pass the visual check and contain the path to dedrifted files.
#
# Models/realizations to delete from consideration.
#hist-aer:
#    MRI-ESM2-0
#	    r5i1p1f1 (last time point is funny)
#
#hist-GHG:
#    NorESM2-LM (both realizations start in 1900)
#    MRI-ESM2-0
#	    r5i1p1f1 (last time point is funny)
#    GISS-E2-1-G
#	    r1i1p1f2
#	    r2i1p1f2
#	    r3i1p1f2
#	    r4i1p1f2
#	    r5i1p1f2
#    BCC-CSM2-MR
#
#hist-nat:
#    MRI-ESM2-0
#		r5i1p1f1 (last time point is funny)
#    BCC-CSM2-MR (One strange realization)
#
#historical:
#    NorESM2-LM  (both realizations start in 1900)
#    GISS-E2-1-H  (all realizations strange)
#    GISS-E2-1-G-CC  (One strange realization)
#    GISS-E2-1-G
#    	    r1i1p1f2
#
#********************************************************************************
#
import cdms2, genutil, cdutil, numpy, os


#
# The dedrifted data directory
#
DATA_DIR = '../PROCESSED_DATA/zostoga_AnnualMean_dedrifted/'

exp_list = os.listdir(DATA_DIR)

all_dict = {}

for exp in exp_list:
    #
    print 'Experiment :', exp
    #
    EXP_DIR = DATA_DIR + exp + '/'
    mod_list = os.listdir(EXP_DIR)
    #
    # This model has issues with no piControl run for some realizations'
    if 'NorCPM1' in mod_list: mod_list.remove('NorCPM1')
    #
    
    mod_list.sort()
    #
    all_dict[exp] = {}
    #
    # Step 1. Models that are being completely removed from consideration  for specific experiments
    #
    if exp == 'hist-GHG': mod_list.remove('NorESM2-LM')
    if exp == 'hist-GHG': mod_list.remove('BCC-CSM2-MR')
    if exp == 'hist-nat': mod_list.remove('BCC-CSM2-MR')
    if exp == 'historical': mod_list.remove('NorESM2-LM')
    if exp == 'historical': mod_list.remove('GISS-E2-1-H')
    if exp == 'historical': mod_list.remove('GISS-E2-1-G-CC')
    #
    for mod in mod_list:
        #
        print 'Model :', mod
        #
        MOD_DIR = EXP_DIR + mod + '/'
        #
        rel_list = os.listdir(MOD_DIR)
        #
        #
        # Step 2. Individual realizations from models that are being removed for specific experiments
        #
        #	    
        if exp == 'hist-aer' and mod == 'MRI-ESM2-0': rel_list.remove('r5i1p1f1')
        #
        if exp == 'hist-GHG' and mod == 'MRI-ESM2-0': rel_list.remove('r5i1p1f1')
        if exp == 'hist-GHG' and mod == 'GISS-E2-1-G': rel_list.remove('r1i1p1f2')
        if exp == 'hist-GHG' and mod == 'GISS-E2-1-G': rel_list.remove('r2i1p1f2')
        if exp == 'hist-GHG' and mod == 'GISS-E2-1-G': rel_list.remove('r3i1p1f2')
        if exp == 'hist-GHG' and mod == 'GISS-E2-1-G': rel_list.remove('r4i1p1f2')
        if exp == 'hist-GHG' and mod == 'GISS-E2-1-G': rel_list.remove('r5i1p1f2')
        #
        if exp == 'hist-nat' and mod == 'MRI-ESM2-0': rel_list.remove('r5i1p1f1')
        #
        if exp == 'historical' and mod == 'GISS-E2-1-G': rel_list.remove('r1i1p1f2')
        #
        #
        all_dict[exp][mod] = {}
        #
        iCounter = 0
        #
        for rel in rel_list:
            REL_DIR = DATA_DIR +  exp + '/' + mod + '/' + rel + '/'
            #
            flist = os.listdir(REL_DIR)
            if len(flist) != 1:
                print '************!!! What have we here?', REL_DIR, flist
            else:
                file = flist[0]
            #if len(flist) != 1:
            #
            all_dict[exp][mod][rel] = file
            #
        # end of for rel in rel_list:
    # end of for mod in mod_list[:1]:
# end of for exp in exp_list[:1]:

print all_dict

fout = open('zostogaProcessedPlotDataDict.py', 'w')
fout.write('plotDataDict = '+ repr(all_dict)+'\n')
fout.close()

