import cdms2, cdutil, numpy, os, cdtime, genutil
from zostogaAvailableDataDict import short_data_dict
cdms2.setNetcdf4Flag(1)
cdms2.setNetcdfShuffleFlag(0)
cdms2.setNetcdfDeflateFlag(0)
cdms2.setNetcdfDeflateLevelFlag(1)

OUT_ROOT_DIR = '../PROCESSED_DATA/'

OUT_ROOT_DIR1  = OUT_ROOT_DIR + 'zostoga_AnnualMean/'
OUT_ROOT_DIR2  = OUT_ROOT_DIR + 'zostoga_AnnualMean_dedrifted/'

OVERWRITE = True
__DEBUG__ = False

all_expts = short_data_dict.keys()
all_expts.remove('piControl')

for expt in all_expts:
    print '\nExperiment: ', expt
    #
    #
    all_mods = short_data_dict[expt].keys()
    all_mods.sort()
    #
    #
    #for mod in ['IPSL-CM6A-LR']:
    for mod in all_mods:
        print '\n\tModel: ', mod
        all_rels = short_data_dict[expt][mod].keys()
        #
        for rel in all_rels:
            print '\n\t\t**** Realisation: ', rel
            #
            OUTDIR1 = OUT_ROOT_DIR1 + expt + '/' + mod + '/' + rel + '/'
            OUTDIR2 = OUT_ROOT_DIR2 + expt + '/' + mod + '/' + rel + '/'
            #
            xmlfilename = short_data_dict[expt][mod][rel]['XMLFILE']
            if __DEBUG__: print '\t\t', xmlfilename
            #
            last_slash_index = -1 * xmlfilename[::-1].index('/')
            xml_filename_only = xmlfilename[last_slash_index:]
            outfilename1 = xml_filename_only[:-4] + '_AnnualMean.nc'
            outfilename2 = xml_filename_only[:-4] + '_AnnualMean_dedrifted.nc'
            #
            if not os.path.isfile(OUTDIR1 + outfilename1) or not os.path.isfile(OUTDIR2 + outfilename2) or OVERWRITE:
                #
                print '\t\tCreating outfiles 1 & 2'
                print '\t\toutfilename1', outfilename1
                print '\t\toutfilename2', outfilename2
                #
                # First open the experiment xml file
                #
                f = cdms2.open(xmlfilename)
                slr_var = f['zostoga']
                if __DEBUG__: print '\t\tShape of slr_var :', slr_var.shape
                taxis = slr_var.getTime()
                #if taxis.getCalendar() == cdtime.Calendar360
                #
                print '&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& getCalendar returns ', taxis.getCalendar()
                print '&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& taxis.calendar is set as ', taxis.calendar
                #
                C1 = cdtime.reltime(taxis[0], taxis.units).tocomp()
                if __DEBUG__: print '\t\tStarting time of slr_var = ', C1
                #
                if C1.year != 1850 or C1.month != 1: print '\t\t$$$$$ DOES NOT START AT 1850-1 $$$$$ but at', C1
                #
                global_att_list = f.listglobal()
                #
                #********************************************************************************
                #
                # Part - I
                #
                # Create Annual Means and write them out without removing drift from corresponding piControl segment.
                #
                AnnualMean = cdutil.YEAR(slr_var(squeeze=1))
                if __DEBUG__: print '\t\tShape of AnnualMean :', AnnualMean.shape
                AnnualMean.id = 'zostoga'
                AnnualMean.units = slr_var.units
                #
                #
                #********************************************************************************
                #
                # Part -II
                #
                piC_rel = f.getglobal('parent_variant_label')
                if __DEBUG__: print '\t\t\tParent piControl realization from which branched ', piC_rel
                #
                # Check if model piControl exists
                #
                if mod not in short_data_dict['piControl'].keys():
                    print '*************************'
                    print '*'
                    print '*'
                    print '*'
                    print '*'
                    print '*'
                    print 'piControl NOT FOUND for', mod
                    print '*'
                    print 'Parent piControl realization from which branched ', piC_rel
                    print '*'
                    print '*'
                    print '*'
                    print '*'
                    print '*'
                    print '*************************'
                    break
                # end of if mod not in short_data_dict['piControl'].keys():
                #
                # Check if particular realization exists
                #
                if piC_rel not in short_data_dict['piControl'][mod].keys():
                    print '\t\t****', piC_rel, ' piControl realization NOT FOUND for model', mod
                    break
                # end of if piC_rel not in short_data_dict['piControl'][mod].keys():
                #
                # Extract piControl xml file name
                #
                piControl_xmlfilename = short_data_dict['piControl'][mod][piC_rel]['XMLFILE']
                if __DEBUG__: print '\t\t\tpiControl_xmlfilename = ', piControl_xmlfilename
                if __DEBUG__: print "'\t\t\t\tf.getglobal('branch_time_in_child')", f.getglobal('branch_time_in_child')
                if __DEBUG__: print "'\t\t\t\tf.getglobal('branch_time_in_parent')", f.getglobal('branch_time_in_parent')
                if __DEBUG__: print "'\t\t\t\tf.getglobal('parent_time_units')", f.getglobal('parent_time_units')
                if __DEBUG__: print "'\t\t\t\tpiC branch start time:", cdtime.reltime(f.getglobal('branch_time_in_parent'), f.getglobal('parent_time_units')).tocomp()
                #
                # Open piControl xml file
                #
                f_piC = cdms2.open(piControl_xmlfilename)
                slr_piC = f_piC['zostoga']
                #
                piC_time_axis = slr_piC.getTime()
                piC_file_start_time = cdtime.reltime(piC_time_axis[0], piC_time_axis.units).tocomp()
                piC_file_end_time = cdtime.reltime(piC_time_axis[-1], piC_time_axis.units).tocomp()
                if __DEBUG__: print '\t\t\tIN THE FILE: piC_file_start_time =', piC_file_start_time, 'piC_file_end_comp = ', piC_file_end_time
                #
                C2 = cdtime.reltime(f.getglobal('branch_time_in_parent'), f.getglobal('parent_time_units')).tocomp()
                piC_start_comp = cdtime.comptime(C2.year, 1, 1)
                piC_end_comp = piC_start_comp.add(len(AnnualMean)*12, cdtime.Months)
                #
                if __DEBUG__: print '\t\t\tLOOKING FOR piC_start_comp =', piC_start_comp, 'piC_end_comp = ', piC_end_comp
                #
                # This is now using the entire piControl length to compute secular drift that will be removed.
                #
                slr_piC = f_piC('zostoga', squeeze=1)
                


                """
                #
                CASE = 999
                #
                try:
                    slr_piC = f_piC('zostoga', time=(piC_start_comp, piC_end_comp), squeeze=1)
                    #
                    yr,mo = divmod(len(slr_piC), 12)
                    if __DEBUG__: print '\t\t\tLength of piControl extracted =', len(slr_piC), '. Number of Years & months =', yr, mo
                    #
                    if mo == 0:
                        len_annual_mean = yr
                    else:
                        len_annual_mean = yr-1
                    # end of if mo == 0:
                    #
                    if __DEBUG__: print '\t\t\tLength of piControl Annual Mean will be', len_annual_mean
                except:
                    #
                    CASE = 0
                    print '\t\t\t********** piControl data could not be extracted **********'
                # end of try:
                #
                if CASE != 0:
                    #
                    if len_annual_mean != len(AnnualMean):
                        #
                        print '\t\t\t##### LENGTHS OF ANNUAL MEANS DO NOT MATCH #####'
                        #
                        if piC_file_start_time.cmp(piC_start_comp) == -1:
                            print '\t\t\t###### Checking for CASE 3; File starts earlier than required # This is ok'
                        else:
                            print '\t\t\t##### CASE = 3. #File starts later than required # This is NOT OK'
                            CASE = 3
                            #
                            # Case 3: piControl begins after the required date
                            #
                            # Solution: Delay the start date
                            #
                            print '\t\t\tCase 3: Delay the start date'
                            new_piC_start_comp = cdtime.comptime(piC_file_start_time.year +1, 1)
                            new_piC_end_comp = new_piC_start_comp.add(len(AnnualMean)*12, cdtime.Months)
                            slr_piC = f_piC('zostoga', time=(new_piC_start_comp, new_piC_end_comp), squeeze=1)
                        # end of if piC_file_start_time.cmp(piC_start_comp) == -1:
                        #
                        if piC_end_comp.cmp(piC_file_end_time) == -1:
                            print '\t\t\t###### Checking for CASE 2; File ends later than required. #This is ok.'
                        else:
                            print '\t\t\t##### CASE = 2. #File ends earlier than required # This is NOT OK'
                            CASE = 2
                            #
                            # Case 2: piControl run ends before the required time
                            #
                            # Solution: Take the required length by advancing the start date
                            #
                            print '\t\t\tCase 2: Take the required length by advancing the start date'
                            new_piC_end_comp = cdtime.comptime(piC_file_end_time.year, 12)
                            new_piC_start_comp = new_piC_end_comp.sub(len(AnnualMean)*12, cdtime.Months)
                            #
                            slr_piC = f_piC('zostoga', time=(new_piC_start_comp, new_piC_end_comp), squeeze=1)
                            #
                        # end of if piC_end_comp.cmp(piC_file_end_time) == -1:
                        #
                        if piC_file_end_time.cmp(piC_file_start_time.add(len(AnnualMean)*12, cdtime.Months)) == -1:
                            #
                            # Actual length of data is less than required
                            #
                            print '\t\t\t#####  CASE = 1. Actual length of data is less than required'
                            CASE = 1
                            #
                            # Case 1: Total length of piControl is less than that of the experiment
                            #
                            # Solution: Take the entire length of the piControl run
                            #
                            print '\t\t\tCase 1: Take the entire length of the piControl run'
                            slr_piC = f_piC('zostoga', squeeze=1)
                            #
                        else:
                            print '\t\t\t###### Checking for CASE 1; #This is ok.'
                        # end of if piC_file_end_time.cmp(piC_file_start_time.add(len(AnnualMean)*12, cdtime.Months)):
                        #
                    else:
                        if CASE != 0: print '\t\t\t----- LENGTHS OK -----'
                    # end of if len_annual_mean != len(AnnualMean):
                    """

                #


                    
                #
                # Compute Annual Mean of piControl segment extracted.
                #
                slr_piC_AnnualMean = cdutil.YEAR(slr_piC)
                """
                #
                # Check One More time to see if lengths match
                #
                if len(slr_piC_AnnualMean) != len(AnnualMean):
                    if CASE != 1:
                        print '\t\t\t%%%%% LENGTHS OF ANNUAL MEANS STILL MISMATCHED %%%%%'
                        print '\t\t\t%%%%% len(slr_piC_AnnualMean), len(AnnualMean)', len(slr_piC_AnnualMean), len(AnnualMean)
                    # end of if CASE != 1:
                # end of if len(slr_piC_AnnualMean) != len(AnnualMean):
                """
                #
                # Compute linear trend of the piControl Annual Means
                #
                linear_trend, intercept = genutil.statistics.linearregression(slr_piC_AnnualMean)
                print '\t\tLinear Trend = ', linear_trend
                #
                #print '\t\t\tslr_piC_AnnualMean Time units, AnnualMean Time units = ', slr_piC_AnnualMean.getTime().units, AnnualMean.getTime().units
                assert slr_piC_AnnualMean.getTime().units[:4] == AnnualMean.getTime().units[:4]
                #
                # Now compute the trend line that will be subtracted.
                #
                final_AnnualMeanTaxis = AnnualMean.getTime()
                tarray = final_AnnualMeanTaxis[:] - final_AnnualMeanTaxis[0]
                trendarray = linear_trend.filled() * tarray
                #print trendarray[:]
                dedrifted_AnnualMean = AnnualMean - trendarray
                #print dedrifted_AnnualMean[:]
                dedrifted_AnnualMean.id = 'zostoga'
                dedrifted_AnnualMean.units = slr_var.units


                #
                # Write out the Annual Mean (before dedrifting)
                #
                if not os.path.isdir(OUTDIR1): os.makedirs(OUTDIR1)
                #
                if __DEBUG__: print '\t\tWriting out to ', OUTDIR1 + outfilename1
                #
                g1 = cdms2.open(OUTDIR1 + outfilename1, 'w')
                g1.write(AnnualMean)
                for att in global_att_list:
                    if __DEBUG__: print '\t\t\t', att, f.getglobal(att)
                    setattr(g1, att, f.getglobal(att))
                # end of for att in global_att_list:
                setattr(g1, 'AnnualMeanComment1', 'Annual means created using cdms2. Dedrifting NOT done')
                setattr(g1, 'AnnualMeanComment2', 'Created by Krishna AchutaRao')
                g1.close()

                #
                # Write out the Annual Mean (AFTER dedrifting)
                #
                if not os.path.isdir(OUTDIR2): os.makedirs(OUTDIR2)
                #
                print '\t\tWriting out to ', OUTDIR2 + outfilename2
                #
                g2 = cdms2.open(OUTDIR2 + outfilename2, 'w')
                g2.write(dedrifted_AnnualMean)
                #
                for att in global_att_list:
                    #print '\t\t\t', att, f.getglobal(att)
                    setattr(g2, att, f.getglobal(att))
                # end of for att in global_att_list:
                #
                final_piC_taxis = slr_piC_AnnualMean.getTime()
                start_stamp = cdtime.reltime(final_piC_taxis[0], final_piC_taxis.units).tocomp()
                end_stamp = cdtime.reltime(final_piC_taxis[-1], final_piC_taxis.units).tocomp()
                commentString = 'Annual means created using cdms2. Dedrifting done using ' + piC_rel + '. ' + str(start_stamp) + ' to ' + str(end_stamp)
                setattr(g2, 'AnnualMeanComment1', commentString)
                setattr(g2, 'AnnualMeanComment2', 'Created by Krishna AchutaRao')
                g2.close()
                #
            else:
                print '\t\t*******Already Exists. Skipping'
            # end of if not os.path.isfile(OUTDIR + outfilename) or OVERWRITE:
        # end of for rel in all_rels:
    # end of for mod in all_mods:
# end of for expt in all_expts:
