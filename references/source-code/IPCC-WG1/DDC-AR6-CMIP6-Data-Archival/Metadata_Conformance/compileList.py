#! /usr/bin/env python

# compile single CMIP6 dataset list out of chapter lists provided by TSU WGI (Robin) at https://drive.google.com/drive/folders/1oq_MdqGTOId-oMn8_2WzmZrloEYsF-sk

"""Compile single CMIP6 dataset list out of chapter lists provided by TSU WGI (Robin) at https://drive.google.com/drive/folders/1oq_MdqGTOId-oMn8_2WzmZrloEYsF-sk for LTA in DDC AR6
Version: V0.1 2022-02-22, stockhause@dkrz.de"""

# Usage: ./compileList.py <input dir> <cmip6|cordex|cmip5>

import sys,os,re,logging
import copy,json
from operator import itemgetter

mydir = os.path.abspath(os.getcwd())
mydate = os.popen('date +%F').read().strip()
#print mydate,mydir

# read option
#print 'Call: %s' % ' '.join(sys.argv)
if len(sys.argv)<2:
    print "Usage: ./compileList.py <input dir> <cmip6|cordex|cmip5>"
    sys.exit()
indir = sys.argv[1]
project = sys.argv[2]
outfile  = mydir+'/output/'+project+'_list_'+mydate+'.json'
if project == 'cmip6':
    outfile2 = mydir+'/output/mpi_ge_list_'+mydate+'.json'

LOG_FILENAME = mydir+'/log/compileList_'+mydate+'.log'
#logging.basicConfig(filename=self.LOG_FILENAME,level=logging.DEBUG)#,format='%(asctime)s - %(levelname)s: %(message)s')
log = logging.getLogger()
console=logging.FileHandler(LOG_FILENAME)
formatter=logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
simple_formatter=logging.Formatter('%(message)s')
console.setFormatter(formatter)
log.setLevel(logging.INFO)
#logging.getLogger('').addHandler(self.console)
log.addHandler(console)

log.info('Call: %s' % ' '.join(sys.argv))

# 1. Read input datasets

# identify CMIP6 lists
os.chdir(indir)
readfiles = {}
for root, dirs, files in os.walk(".", topdown=False):
    for f in files:
        #print('files ',os.path.join(root, f))
        if re.search(project,f) and re.search('json',f):
            #print f
            try:
                readfiles[f] = json.loads(open(f,'r').read())
            except:
                print 'Error in reading %s' % f

myfiles=sorted(readfiles.items())
counter=0

for (k,v) in myfiles:
    #print 'C1',counter
    if counter == 0:
        outjson = copy.deepcopy(myfiles[0])
        log.info('%s: COPY all files' % k)
        counter +=1
        continue

    for i in v[0]:
        if i["data_ref_syntax"] not in [value['data_ref_syntax'] for value in outjson[1][0]]:
            #print 'ADD', i["data_ref_syntax"]
            #print outjson[1][0]
            log.info('%s: ADD %s' % (k,i["data_ref_syntax"]))
            outjson[1][0].append(i)
            #print outjson
            #print outjson[1][0]
            #sys.exit()
        else:
            #print 'MERGE', i["data_ref_syntax"]
            log.info('%s: MERGE %s' % (k,i["data_ref_syntax"]))
            for o in outjson[1][0]:
                if i["data_ref_syntax"] == o["data_ref_syntax"]:
                    #print "FOUND", i["data_ref_syntax"], o["data_ref_syntax"]
                    #print i
                    #print o
                    #tracking_id_nc, checksum_nc,report_figures,report_subpanels
                    #print o
                    for t in i['tracking_id_nc']:
                        if t not in o['tracking_id_nc']:
                            o['tracking_id_nc'].append(t)
                    try:
                        if not re.search(i['checksum_nc'],o['checksum_nc']):
                            o['checksum_nc'] += ' '+i['checksum_nc']
                    except:
                        pass
                    o['report_figures'].extend(i['report_figures'])
                    o['report_subpanels'].extend(i['report_subpanels'])
                    #o['status'] += '; MERGE'
                    break
                    #print i
                    #print o
                    #sys.exit()
    counter +=1
    #print 'C2',counter

# split outjson
if project == 'cmip6':
    outj1 = [[]]
    outj2 = [[]]
    for v in outjson[1][0]:
        if re.search('CMIP6',v["data_ref_syntax"]):
            outj1[0].append(v)
        elif re.search('mpi-ge',v["data_ref_syntax"]):
            outj2[0].append(v)
        else:
            log.info('%s not sorted' %  v["data_ref_syntax"])

    with open(outfile,'w') as f:
        json.dump(outj1,f,indent=4)
    with open(outfile2,'w') as f:
        json.dump(outj2,f,indent=4)
else:
    with open(outfile,'w') as f:
        json.dump(outjson[1],f,indent=4)

sys.exit()
