#********************************************************************************
#
# GatherData.py
#
# version 1
#
# This script gathers the available .nc data files for zostoga from the CMIP and
# DAMIP experiments and creates xml files. It also creates an html file as well
# as a dictionary to keep track of them.
#
# Written by Krishna AchutaRao
#
#            08 January 2021
#
#********************************************************************************
import os, string, time

def createTimeStamp(x=1):
    import time
    x = time.localtime()
    TimeStamp = str(x.tm_year) + '-' + str(x.tm_mon) + '-' + str(x.tm_mday) + ' ' + \
        str(x.tm_hour) + ':' + str(x.tm_min ) + ':' + str(x.tm_sec)
    return TimeStamp

#********************************************************************************
#
OVERWRITE = True
#OVERWRITE = False
#
if OVERWRITE: 
    print 'OVERWRITE Flag is set true. ALL FILES WILL BE OVERWRITTEN!!'
else:
    print 'OVERWRITE Flag is set false. No files will be overwritten.'
# end of if OVERWRITE: 



limit_scen_list = ['hist-GHG', 'hist-aer', 'hist-nat', 'historical', 'piControl']


#********************************************************************************
#
# Start Crawling Data Directories
#
DOWNLOAD_DATA_DIR = '../CMIP6/'
#
OUT_DICT_FILE = 'zostogaAvailableDataDict.py'
OUT_HTML_FILE = 'DataTable.html'
#
all_dirs = os.listdir(DOWNLOAD_DATA_DIR)

avail_data_dict = {}
short_data_dict = {}


all_proj_list = []
for d in all_dirs: 
    if os.path.isdir(DOWNLOAD_DATA_DIR + d):
        #print (d, ' is a directory')
        all_proj_list.append(d)
        avail_data_dict[d] = {}
    else:
        #print (d, ' is NOT a directory')
        pass
    # end of if os.path.isdir(DOWNLOAD_DATA_DIR +):
# end of for d in all_dirs: 

all_proj_list.sort()
print 'Found Projects:', all_proj_list


for proj in all_proj_list:
    all_centers_list = []
    #
    current_dir = DOWNLOAD_DATA_DIR + proj + '/'
    all_dirs = os.listdir(current_dir)
    #
    for d in all_dirs:
        if os.path.isdir(current_dir+d):
            #print (d, ' is a directory')
            if d not in all_centers_list: all_centers_list.append(d)
            avail_data_dict[proj][d] = {}
        else:
            # print (d, ' is NOT a directory')
            pass
        # end of if os.path.isdir(DOWNLOAD_DATA_DIR +):
    # end of for d in all_dirs:
# end of for proj in all_proj_list:

print 'Found Modeling Centers:', all_centers_list

all_mods_list = []
for proj in all_proj_list:
    for center in all_centers_list:
        #
        current_dir = DOWNLOAD_DATA_DIR + proj + '/' + center + '/'
        all_dirs = os.listdir(current_dir)
        #
        for d in all_dirs:
            if os.path.isdir(current_dir+d):
                #print (d, ' is a directory')
                if d not in all_mods_list: all_mods_list.append(d)
                avail_data_dict[proj][center][d] = {}
            else:
                # print (d, ' is NOT a directory')
                pass
            # end of if os.path.isdir(DOWNLOAD_DATA_DIR +):
        # end of for d in all_dirs:
    # end of for center in all_centers_list:
# end of for proj in all_proj_list:

print 'Found Models:', all_mods_list




all_expts_list = []

print 'Found Experiments:', all_expts_list
for proj in all_proj_list:
    for center in all_centers_list:
        for model in all_mods_list:
            #
            current_dir = DOWNLOAD_DATA_DIR + proj + '/' + center + '/' + model + '/'
            if os.path.isdir(current_dir):
                all_dirs = os.listdir(current_dir)
                #
                for d in all_dirs:
                    if os.path.isdir(current_dir+d):
                        #print (d, ' is a directory')
                        if d not in all_expts_list: all_expts_list.append(d)
                        avail_data_dict[proj][center][model][d] = {}
                    else:
                        # print (d, ' is NOT a directory')
                        pass
                    # end of if os.path.isdir(DOWNLOAD_DATA_DIR +):
                # end of for d in all_dirs:
            else:
                pass
            # if os.path.isdir(current_dir):
        # end of for model in all_mods_list:
    # end of for center in all_centers_list:
# end of for proj in all_proj_list:

all_expts_list.sort()
print 'Found Experiments:', all_expts_list

all_rels_list = []
for proj in all_proj_list:
    for center in all_centers_list:
        for model in all_mods_list:
            for expt in all_expts_list:
                #
                current_dir = DOWNLOAD_DATA_DIR + proj + '/' + center + '/' + model + '/' + expt + '/'
                if os.path.isdir(current_dir):
                    all_dirs = os.listdir(current_dir)
                    #
                    for d in all_dirs:
                        if os.path.isdir(current_dir+d):
                            all_rels_list.append(d)
                            avail_data_dict[proj][center][model][expt][d] = {}
                            avail_data_dict[proj][center][model][expt][d]['Omon'] = {}
                            avail_data_dict[proj][center][model][expt][d]['Omon']['zostoga'] = {}
                        else:
                            # print (d, ' is NOT a directory')
                            pass
                        # end of if os.path.isdir(DOWNLOAD_DATA_DIR +):
                # end of for d in all_dirs:
            else:
                pass
            # end of if os.path.isdir(current_dir):
        # end of for model in all_mods_list:
    # end of for center in all_centers_list:
# end of for proj in all_proj_list:


# CMIP/NASA-GISS/GISS-E2-1-G/piControl/r1i1p1f1/Omon/zostoga/gn/v20180824
# file_name = zostoga_Omon_GISS-E2-1-G_piControl_r1i1p1f1

misc_list1 = []
for proj in all_proj_list:
    for center in all_centers_list:
        for model in all_mods_list:
            for expt in all_expts_list:
                for rel in all_rels_list:
                    #
                    current_dir = DOWNLOAD_DATA_DIR + proj + '/' + center + '/' + model + '/' + expt + '/' + rel + '/Omon/zostoga/'
                    #
                    if os.path.isdir(current_dir):
                        all_dirs = os.listdir(current_dir)
                        #
                        for d in all_dirs:
                            if os.path.isdir(current_dir+d):
                                misc_list1.append(d)
                                avail_data_dict[proj][center][model][expt][rel]['Omon']['zostoga'][d] = {}
                                ## Last layer? ##
                                #
                                new_cur_dir = current_dir + d + '/'
                                all_dirs1 = os.listdir(new_cur_dir)
                                for d1 in all_dirs1:
                                    if os.path.isdir(new_cur_dir + d1 + '/'):
                                        avail_data_dict[proj][center][model][expt][rel]['Omon']['zostoga'][d][d1] = {}
                                        final_dir_list = os.listdir(new_cur_dir + d1)
                                        #
                                        for f2 in final_dir_list:
                                            final_test_for_dir = new_cur_dir + d1 + '/' + f2
                                            if os.path.isdir(final_test_for_dir):
                                                print 'Why is there a directory here', final_test_for_dir
                                            else:
                                                #print 'Ok. File found'
                                                if final_test_for_dir[-3:] == '.nc':
                                                    if 'NCFILES' not in avail_data_dict[proj][center][model][expt][rel]['Omon']['zostoga'][d][d1].keys():
                                                        WORKING_DIR = new_cur_dir + d1 + '/'
                                                        #
                                                        avail_data_dict[proj][center][model][expt][rel]['Omon']['zostoga'][d][d1]['DIRECTORY'] = WORKING_DIR
                                                        avail_data_dict[proj][center][model][expt][rel]['Omon']['zostoga'][d][d1]['NCFILES'] = []
                                                        #
                                                        xmlfile = WORKING_DIR + string.joinfields(['zostoga_Omon', model, expt, rel, d, d1], '_') + '.xml'
                                                        #print xmlfile
                                                        avail_data_dict[proj][center][model][expt][rel]['Omon']['zostoga'][d][d1]['XMLFILE'] = xmlfile
                                                        #
                                                        scancmd = 'cdscan -x %s %s' %(xmlfile, WORKING_DIR + '*.nc')
                                                        #print scancmd + '\n'
                                                        avail_data_dict[proj][center][model][expt][rel]['Omon']['zostoga'][d][d1]['scancmd'] = scancmd
                                                        #
                                                        if expt not in short_data_dict.keys(): short_data_dict[expt] = {}
                                                        if model not in short_data_dict[expt].keys(): short_data_dict[expt][model] = {}
                                                        if rel not in short_data_dict[expt][model].keys(): short_data_dict[expt][model][rel] = {}
                                                        short_data_dict[expt][model][rel]['XMLFILE'] = xmlfile
                                                        short_data_dict[expt][model][rel]['scancmd'] = scancmd
                                                        #
                                                    # end of if if 'NCFILES' not in keys()
                                                    avail_data_dict[proj][center][model][expt][rel]['Omon']['zostoga'][d][d1]['NCFILES'].append(f2)
                                                else:
                                                    if final_test_for_dir[-3:] != 'xml': print 'Not a .nc or .xml file?', final_test_for_dir
                                                # end of if final_test_for_dir[-3:] == '.nc':
                                            # end of if os.path.isdir(final_test_for_dir):
                                        # end of for f2 in final_dir_list:
                                        """
                                                # end of if final_test_for_dir[-3:] == 'nc':
                                            # end of if os.path.isdir(final_test_for_dir):
                                        # end of for d2 in final_dir_list:
v                                        """
                                    # end of if os.path.isdir(new_cur_dir + d1 + '/'):
                                # end of for d1 in all_dirs1:
                            else:
                                # print (d, ' is NOT a directory')
                                pass
                            # end of if os.path.isdir(current_dir+d):
                        # end of for d in all_dirs:
                    else:
                        pass
                    # end of if os.path.isdir(current_dir):
                # end of for rel in all_rels_list:
            # end of for expt in all_expts_list:
        # end of for model in all_mods_list:
    # end of for center in all_centers_list:
# end of for proj in all_proj_list:

#print short_data_dict


#********************************************************************************
# 
# Part - II
#
# Write out the dictionary to a file
#
print 'Writing dictionaries and lists to file'
fdict = open(OUT_DICT_FILE, 'w')
fdict.write('#CMIP6 Data lists and dictionaries\n')
fdict.write('#\n')
ts = createTimeStamp(1)
fdict.write('#Created on %s\n' %ts)
fdict.write('#\n')
fdict.write('all_proj_list = ' + repr(all_proj_list)+'\n')
fdict.write('all_expts_list = ' + repr(all_expts_list)+'\n')
fdict.write('all_mods_list = ' + repr(all_mods_list)+'\n')
fdict.write('avail_data_dict = ' + repr(avail_data_dict)+'\n')
fdict.write('short_data_dict = ' + repr(short_data_dict)+'\n')
fdict.close()
#
#********************************************************************************


#********************************************************************************
# 
# Part - III
#
# Perform cdscan operation
#
print '#################### Entering scan execution ####################'
#


for expt in short_data_dict.keys():
    print 'Experiment: ', expt
    avail_mods = short_data_dict[expt].keys()
    #
    for mod in avail_mods:
        # print '...Model:', mod
        avail_rels = short_data_dict[expt][mod].keys()
        #
        for rel in avail_rels:
            # print '......Realization:', rel
            #
            scancmd = short_data_dict[expt][mod][rel]['scancmd']
            xmlfile = short_data_dict[expt][mod][rel]['XMLFILE']
            #
            if not(os.path.isfile(xmlfile)) or OVERWRITE == True:
                print '\t\tExecuting scancmd'
                try:
                    os.system(scancmd)
                    print '\t\t...Trying os.system(scancmd)'
                except:
                    os.popen(scancmd)
                    print '\t\t...Trying os.popen(scancmd)'
                # end of try:
            else:
                print '\t\txmlfile already exists AND OVERWRITE == False'
            # end of if not(os.path.isfile(xmlfile)) or OVERWRITE == True:
        # end of for rel in avail_rels
    # end of for mod in avail_mods:
# end of for expt in short_data_dict.keys():





#********************************************************************************
# 
# Part - IV
#
# Create HTML table
#
# Experiment, model, realization
#
all_expts_list.sort()
print "Showing Experiments:", all_expts_list

all_mods_list.sort()
print "All Models:", all_mods_list

print '##### Creating html file ####'
fhtml = open(OUT_HTML_FILE, 'w')
fhtml.write("<HTML>\n")
fhtml.write("<CENTER>\n")
fhtml.write("<H1>Available Simulations</H1>\n")
fhtml.write("<h5>Created on %s</h5>\n" % time.asctime())
fhtml.write("<TABLE border=1 cellpadding=3 cellspacing=3>\n")

fhtml.write("<TR>\n")
fhtml.write("<TD bgcolor=#aaaaaa>Model</TD>\n")
for expt in all_expts_list:
    #print 'Experiment: ', expt
    fhtml.write("<TD>%s</TD>\n" % expt)
# end of for expt in all_expts_list:
fhtml.write("</TR>\n")


fhtml.write("<TR>\n")
for mod in all_mods_list:
    #print 'Model: ', mod
    fhtml.write("<TR>\n")
    fhtml.write("<TD>%s</TD>" % mod)
    #
    for expt in all_expts_list:
        #print '\tExperiment ', expt
        if expt not in short_data_dict.keys():
            #print '\t\t\tNo data'
            fhtml.write("<TD>N/A</TD>\n")
        elif mod not in short_data_dict[expt].keys():
            #print '\t\t\tNo data'
            fhtml.write("<TD>N/A</TD>\n")
        elif short_data_dict[expt][mod].keys() == []:
            #print '\t\t\tNo data'
            fhtml.write("<TD>N/A</TD>\n")
        else:
            rel_list = short_data_dict[expt][mod].keys()
            rel_list.sort()
            #print '\t\t\t' + str(len(reallist)) + ': ',
            #for rls in reallist: print rls,
            #print
            fhtml.write("<TD valign=\"top\">\n")
            for rls in rel_list: 
                fhtml.write("%s<br/>" % rls)
            # for rls in rel_list: 
            fhtml.write("</TD>\n")
            #
        # end of if expt not in short_data_dict.keys():
    # end of for expt in all_expts_list:
    fhtml.write("</TR>\n")
# end of for mod in all_mods_list:

fhtml.write("</TABLE>\n")
fhtml.write("</CENTER>\n")
fhtml.write("</HTML>\n")
fhtml.close()
print 'html file written'

