#! /usr/bin/env python

# compile list of variables as CMOR_table.variable for DataRequest discussion on priority variable list and experiment.variable for WIP discussion
# based on error corrected CMIP6 dataset list 
# (related to list compiled by Martin Juckes at: https://docs.google.com/spreadsheets/d/1BlVZXvkwlGBTOSkVpTGS67fGw1t0EEQI8gdgg7KCxdg)



"""Compile list of CMOR_table.variables for DataRequest discussion on priority variables and list of experiment.variable for WIP discussion
Version: V0.1 2022-05-17, stockhause@dkrz.de
         V0.2 2022.05-20 output for variable usage per experiment added as additional output file
         V0.3 2023-03-27 output for experiment added upon request from CMIP-IPO"""

# Usage: ./varlist4dreq.py <input list> 

import sys,os,re,logging
import copy,json
from operator import itemgetter

mydir = os.path.abspath(os.getcwd())
mydate = os.popen('date +%F').read().strip()

# read option
if len(sys.argv)<2:
    print "Usage: ./compileList.py <input list>"
    sys.exit()
infile = sys.argv[1]
outfile   = mydir+'/dreq_out/'+re.split('/',re.split('\.',infile)[0])[-1]+'.csv'
outfile2  = mydir+'/dreq_out/'+re.split('/',re.split('\.',infile)[0])[-1]+'_exp.csv'
outfile3  = mydir+'/dreq_out/'+re.split('/',re.split('\.',infile)[0])[-1]+'_exponly.csv'

outlines=[]
outlines.append('# Variable usage in CMIP6 dataset list compiled by WGI TSU based on IPCC author information')
outlines.append('# Call: %s' % ' '.join(sys.argv))
outlines.append('# Date: %s' % mydate)
outlines.append('#')
outlines.append('Variable,Count')
outlines2=[]
outlines2.append('# Variable usage in CMIP6 dataset list compiled by WGI TSU based on IPCC author information')
outlines2.append('# Call: %s' % ' '.join(sys.argv))
outlines2.append('# Date: %s' % mydate)
outlines2.append('#')
outlines2.append('Variable,Count')
outlines3=[]
outlines3.append('# Experiment usage in CMIP6 dataset list compiled by WGI TSU based on IPCC author information')
outlines3.append('# Call: %s' % ' '.join(sys.argv))
outlines3.append('# Date: %s' % mydate)
outlines3.append('#')
outlines3.append('Experiment,Count')

vars  = {}
vars2 = {}
exp = {}

# 1. Read input file
try:
    file = json.loads(open(infile,'r').read())
except:
    print 'Error in reading %s' % infile

# 2. Count variables
#counter=0
for i in file[0]:
    #counter += 1
    drs=i["data_ref_syntax"]
    dum=re.split('\.',i["data_ref_syntax"])
    myvar=dum[6]+'.'+dum[7]
    #myexp=dum[4]
    if myvar in vars.keys():
        for v,c in vars.iteritems():
            if myvar == v:
                vars[myvar] += 1
                break
    else:
        vars[myvar] = 1
    #if counter>10:
    #    break

for i in file[0]:
    #counter += 1
    drs=i["data_ref_syntax"]
    dum=re.split('\.',i["data_ref_syntax"])
    myvar=dum[4]+'.'+dum[7]
    if myvar in vars2.keys():
        for v,c in vars2.iteritems():
            if myvar == v:
                vars2[myvar] += 1
                break
    else:
        vars2[myvar] = 1
    #if counter>10:
    #    break

for i in file[0]:
    #counter += 1
    drs=i["data_ref_syntax"]
    dum=re.split('\.',i["data_ref_syntax"])
    myexp=dum[4]
    if myexp in exp.keys():
        for v,c in exp.iteritems():
            if myexp == v:
                exp[myexp] += 1
                break
    else:
        exp[myexp] = 1
    #if counter>10:
    #    break


# 3. write csv output files
with open(outfile,'w') as o:
    o.write('\n'.join(outlines))
    o.write('\n')
    for (v,c) in sorted(vars.items()): 
        o.write('%s,%i\n' % (v,c))

with open(outfile2,'w') as o:
    o.write('\n'.join(outlines2))
    o.write('\n')
    for (v,c) in sorted(vars2.items()): 
        o.write('%s,%i\n' % (v,c))

with open(outfile3,'w') as o:
    o.write('\n'.join(outlines3))
    o.write('\n')
    for (v,c) in sorted(exp.items()):
        o.write('%s,%i\n' % (v,c))

sys.exit()
