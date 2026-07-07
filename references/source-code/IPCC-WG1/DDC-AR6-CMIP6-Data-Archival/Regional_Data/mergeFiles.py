#! /usr/bin/env python

import sys,os,re,glob

logfile = open("mergeFiles.log", "a")
mydir = os.path.abspath(os.getcwd())
filedir = '/work/bm0146/k204082/AR6regions/dump'

cdo ='cdo -s mergetime *.nc %s'

os.chdir(filedir)

for root, dirs, files in os.walk(".", topdown=False):
    for f in files:

        if not re.search('.zip',f):
            continue
        
        print(f)
        logfile.write('FILE: %s\n' % f)
        os.system('unzip %s' % f)
        ncfiles = []
        for g in glob.glob("*.nc"):
            ncfiles.append(g)
        mindate = 999999
        maxdate = 0
        #print(ncfiles)
        for n in ncfiles:
            #if not re.search('.nc',n):
            #    continue
            (min,max)=re.split('-',re.split('\.',re.split('_',n)[-1])[0])
            if int(min)<mindate:
                mindate=int(min)
            if int(max)>maxdate:
                maxdate=int(max)
            #print(n,mindate,maxdate)
        outfile = '_'.join(re.split('_',n)[:-1])+'_'+str(mindate)+'-'+str(maxdate)+'.nc'
        print(cdo % outfile)
        logfile.write(cdo % (outfile)+'\n')
        os.system(cdo % outfile)
        os.system('mv %s ../cera2_data/' % outfile)
        os.system('rm *.nc')
        #sys.exit()
