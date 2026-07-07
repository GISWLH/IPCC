#! /usr/bin/env python

# correct obvious  DRS errors in CMIP6 dataset list after application of tidy.py and before compileList.py

"""Correct obvious DRS errors in CMIP6 dataset list after application of tidy.py and compileList.py on CMIP6 dataset lists for chapters provided by TSU WGI (Robin) at https://drive.google.com/drive/folders/1oq_MdqGTOId-oMn8_2WzmZrloEYsF-sk for LTA in DDC AR6
Version: V0.1 2022-04-22, stockhause@dkrz.de"""

# Usage: ./CMIP6correct.py <input dir> 

import sys,os,re,logging
import copy,json
from operator import itemgetter

mydir = os.path.abspath(os.getcwd())
mydate = os.popen('date +%F').read().strip()

# read option
if len(sys.argv)<1:
    print "Usage: ./CMIP6correct.py <input dir>"
    sys.exit()
indir = sys.argv[1]
outdir= mydir+'/'+indir+'_corr'

conffile=mydir+'/CMIP6correct.conf'

LOG_FILENAME = mydir+'/log/CMIP6correct_'+mydate+'.log'
log = logging.getLogger()
console=logging.FileHandler(LOG_FILENAME)
formatter=logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
simple_formatter=logging.Formatter('%(message)s')
console.setFormatter(formatter)
log.setLevel(logging.INFO)
log.addHandler(console)

log.info('Call: %s' % ' '.join(sys.argv))

#test_drs=['CMIP6.CMIP.CAS.FGOALS-g3.ssp585.r1i1p1f1.Amon.pr.gn.20190818',
#'CMIP6.ScenarioMIP.BCC.BCC-ESM1.ssp370.r1i1p1f1.Amon.tas.gn.20190314',
#'CMIP6.ScenarioMIP AerChemMIP.BCC.BCC-ESM1.ssp370.r1i1p1f1.Amon.pr.gn.20190314',
#'CMIP6.CMIP.MPI-M.MPI-ESM-1-2-HAM.ssp126.r1i1p1f1.Omon.mlotst.gn.20190627',
#'CMIP6.ScenarioMIP AerChemMIP.AWI.AWI-CM-1-1-MR.ssp370.r1i1p1f1.day.tas.gn.20190529',
#'CMIP6.ScenarioMIP.MPI-M.MPI-ESM1-2-HR.ssp126.r2i1p1f1.day.tas.gn.20190529',
#'CMIP6.ScenarioMIP.MPI-M.MPI-ESM1-2-HR.ssp370.r2i1p1f1.day.pr.gn.20190529',
#'CMIP6.PMIP.AWI.AWI-ESM-1-1-LR.piControl.r1i1p1f1.Omon.tos.gn.20200212',
#'CMIP6.AerChemMIP.MPI-M.MPI-ESM1-2-HAM.ssp370-lowNTCF.r1i1p1f1.Amon.tas.gn.20190627',
#'CMIP6.CDRMIP.CNRM-CERFACS.CNRM-ESM2-1.piControl.r1i1p1f2.Simon.siconc.gr.20181115',
#'CMIP6.ScenarioMIP.BCC.BCC-ESM1.ssp370.r1i1p1f1.Amon.tas.gn.20190314']

# 1. Read corrections from CMIP6correct.conf
casestrs=[]
corrs=[]

for r in open(conffile,'r').readlines():
    if len(r.strip())==0 or re.search('^#',r):
        continue
    #print r.strip()
    #print re.split(' ',r.strip())
    (case,corr)=re.split(' ',r.strip())
    dumcases=re.split(';',re.sub('!',' ',case.strip()))
    casestr=dumcases[0]
    for d in dumcases[1:]:
        casestr += ' and '+d
    casestrs.append(casestr)
    corrs.append(corr)
#print casestrs
#print corrs
#sys.exit()

# 2. Read CMIP6 dataset list 
drslist=[]
drserrlist=[]
outdrsfile = outdir+'/cmip6_drs_'+mydate+'.txt'
errdrsfile = outdir+'/cmip6_drs_'+mydate+'.err'

os.chdir(indir)
for root, dirs, files in os.walk(".", topdown=False):
    for f in files:
        #print f
        #print('files ',os.path.join(root, f))
        #if not re.search('cmip6',f) and re.search('.json',f):
        if re.search('cmip6',f):
            #print f
            try:
                incmip6 = json.loads(open(f,'r').read())
            except:
                print 'Error in reading %s' % f
            outcmip6 = [[]]
            outfile  = outdir+'/'+f

            # 2. Walk throough json and apply corrections
            # DRS_keys: CMIP6.<mip>.<inst>.<model>.<exp>.<ens>.<frequ>.<var>.<grid>

            for i in incmip6[0]:
                delete=''
                drs=i["data_ref_syntax"]
                (dum,mip,inst,model,exp,ens,frequ,var,grid,version)=re.split('\.',i["data_ref_syntax"])
                for c,n in zip(casestrs,corrs):
                    mycorr=re.split('=',n)
                    if (eval(c)):
                        if mycorr[0]=='mip':
                            mip=re.split('\'',mycorr[1])[1]
                        elif mycorr[0]=='model':
                            model=re.split('\'',mycorr[1])[1]
                        elif mycorr[0]=='inst':
                            inst=re.split('\'',mycorr[1])[1]
                        elif mycorr[0]=='exp':
                            exp=re.split('\'',mycorr[1])[1]
                        elif mycorr[0]=='ens':
                            ens=re.split('\'',mycorr[1])[1]
                        elif mycorr[0]=='frequ':
                            frequ=re.split('\'',mycorr[1])[1]
                        elif mycorr[0]=='var':
                            var=re.split('\'',mycorr[1])[1]
                        elif mycorr[0]=='grid':
                            grid=re.split('\'',mycorr[1])[1]
                        elif mycorr[0]=='version':
                            version=re.split('\'',mycorr[1])[1]
                        elif mycorr[0]=='DELETE':
                            delete=re.split('\'',mycorr[1])[1]

                drsout=dum+'.'+mip+'.'+inst+'.'+model+'.'+exp+'.'+ens+'.'+frequ+'.'+var+'.'+grid+'.'+version
                if len(delete)>0:
                    drsout='DELETE'
                if re.search('mpi-ge',drs): # just in the unlikely case of applied corrections on MPI-GE datasets
                    drsout=drs
                if drs != drsout:
                    i["data_ref_syntax"]=drsout
                    log.error('%s --> %s',drs,drsout)
                if len(delete)>0: # delete entry
                    drserrlist.append('%s:%s' % (drs,re.sub('_',' ',delete)))
                else:
                    outcmip6[0].append(i)
                    if not re.search('mpi-ge',drs):
                       drslist.append(drsout)

            # 3. Write output file
            with open(outfile,'w') as ff:
                json.dump(outcmip6,ff,indent=4)
            log.info('Processed: input=%s output=%s' % (f,outfile))

# 4. Write DRS list and DRS exclude list
open(outdrsfile,'w').write('\n'.join(drslist))
open(errdrsfile,'w').write('\n'.join(drserrlist))
log.info('Written: CMIP6 DRS list=%s' % outdrsfile)
