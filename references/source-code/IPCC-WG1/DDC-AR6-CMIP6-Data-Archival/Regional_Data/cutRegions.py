#! /usr/bin/env python

import sys,os,re

logfile = open("cutRegions.log", "a")
mydir = os.path.abspath(os.getcwd())
indir  = '/work/bm0146/k204082/AR6regions/cera2_data/'
outdir = '/work/bm0146/k204082/AR6regions'
# outdir structure: <region>/<var>/<experiment>

regions = {'Africa':'-35,72,-58,40', 'South_Pole':'0,360,-90,-57', 'Central_Pacific':'120,290,-20,20',
           'Asia':'26,-168,3,83', 'Australia':'68,-115,-58,8', 'Europe':'-60,60,30,75',
           'North_America':'-170,-45,5,85','North_Pole':'0,360,60,90', 'South_America':'-120,-30,-58,15'}

exps = {'historical','ssp126','ssp245','ssp370','ssp585'}

vars = {'orog','sftlf','sftgif','psl','tas','tasmin','tasmax','uas','vas','pr','rsds','huss'}
#vars = {'orog','sftlf','sftgif'}

cdo ='cdo -s sellonlatbox,%s %s %s/%s/%s/%s/%s'

os.chdir(indir)

for root, dirs, files in os.walk(".", topdown=False):
    for f in files:

        if not re.search('.nc',f):
            continue
        
        print(f)
        logfile.write('FILE: %s\n' % f)
        for v in vars:
            if re.search(v+'_',f):
                myvar = v

        for e in exps:
            if re.search(e+'_',f):
                myexp = e

        for r,c in regions.items():

            if not os.path.exists('%s/%s/%s/%s' % (outdir,r,myvar,myexp)):
                os.makedirs('%s/%s/%s/%s' % (outdir,r,myvar,myexp))

            #print(cdo % (c,f,outdir,r,myvar,myexp,f))
            logfile.write(cdo % (c,f,outdir,r,myvar,myexp,f)+'\n')
            os.system(cdo % (c,f,outdir,r,myvar,myexp,f))
        #sys.exit()
