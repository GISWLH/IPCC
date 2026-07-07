#! /usr/bin/env python
"""provide information for call of publish_record.py
Version: V0.1 2024-02-07: initial version; call of publish_record ok (stockhause@dkrz.de),
Version: V1.0 2025-03-06: version used to publish Zenodo records (stockhause@dkrz.de)"""

import sys,os,os.path,re,getopt
import json
import requests
import logging
import publish_record

mydir=os.path.dirname(os.path.realpath(__file__))
mydate=os.popen('date +%Y%m%d').read().strip()


code_version='1.0'
help = """
Register Zenodo Record (Version: """+code_version+""")

Usage:
"""+sys.argv[0]+""" [-h/--help] [-r/--request=request] [-d/--directory=directory] [-o/--olddir=old_version_directory] [-t/--test]
    
with:
--directory/-d   directory with Zenodo metadata and files      
--olddir/-o      directory with old version (required for request=PUT)
--request/-r     request parameter (GET,PUT,POST,DELETE): default = 'GET'
--test/-t        test mode
--help           help message
"""

# 1. read and check call
keyw = ['directory=','help','olddir=','request=','test']
cmd  = 'd:ho:r:t'
    
opt=getopt.getopt(sys.argv[1:],cmd,keyw)

if len(sys.argv)<3:
    print(help)
    sys.exit()
    
request    = 'GET'
test       = ''
testflag   = 0
directory  = ''
olddir     = ''
old_dep_id = 0

if opt[1]!=[]:
    file=opt[1][-1]
for o,p in opt[0]:
    if o in ['--request','-r']:
        request=str.upper(p)
        if request not in ('POST','PUT','GET','DELETE'):
            print("Unknown request")
            print(help)
            sys.exit()
        
    if o in ['--directory','-d']:
        directory=os.path.abspath(p)
        if not os.path.isdir(directory):
            print("Specified directory \'%s\' not found." % directory)
            sys.exit()

    if o in ['--olddir','-d']:
        olddir=os.path.abspath(p)
        if not os.path.isdir(directory):
            print("Specified olddir \'%s\' not found." % olddir)
            sys.exit()
            
    if o in ['--test','-t']:
        testflag=1

    if o in ['--help','-h','-?']:
        print(help)
        sys.exit()


# 2. initialize logging
formatter=logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
if testflag == 0:
    LOG_FILENAME = "/home/k/k204082/export/AR6_figures/call_publish_"+mydate+".log"
else:
    LOG_FILENAME = "/home/k/k204082/export/AR6_figures/call_publish_test_"+mydate+".log"
log = logging.getLogger('log')
log.setLevel(logging.INFO)
console1=logging.FileHandler(LOG_FILENAME)
console1.setLevel(logging.INFO)
sconsole1=logging.StreamHandler()
sconsole1.setLevel(logging.WARN)
console1.setFormatter(formatter)
log.addHandler(console1)
log.addHandler(sconsole1)
log.propagate = False

log.info('Call: %s on %s' % (' '.join(sys.argv),mydate))
if testflag == 1:
    log.info('Test in Zenodo sandbox')

# 3. gather information for call of publish_record: mdfile,request,testflag,old_dep_id
# 3a. get list of input files from directory: zenmd* for GET and DELETE, otherwise md*
myfilelist = []
for root, dirs, files in os.walk(directory):
    for name in files:
        if re.search('^zenmd',name) and request in ('GET','DELETE'):
            myfilelist.append(os.path.join(root,name))
        elif re.search('^md',name) and request in ('PUT','POST'):
            myfilelist.append(os.path.join(root,name))

pr = publish_record.PublishRecord()

for mdfile in myfilelist:
    # mdfile,request,testflag,old_dep_id
    if request == 'PUT':   # get old_dep_id
        (p, n) = os.path.split(mdfile)
        myoldfile=olddir+'/zen'+n
        # skip published updates 
        myzenfile=p+'/zen'+n
        if os.path.isfile(myzenfile):
            continue
                
        if os.path.isfile(myoldfile):
            with open(myoldfile,'r') as f:
                oldjson=json.loads(f.read())
                old_dep_id = oldjson["id"]
            (retmess, retcode) = pr.pub_record(mdfile,request,testflag,old_dep_id)
            if retcode<= 300:
                log.info('Response:%s:%s - request:%s - %s' % (mdfile,old_dep_id,request,retmess))
            else:
                log.error('Response:%s:%s - request:%s - %s:%s' % (mdfile,old_dep_id,request,retcode,retmess))
        else:
            continue
        
    else:   # not 'PUT'
        if request in ('POST'): # skip if zenmd file already exists, i.e. version has been registered
            (p, n) = os.path.split(mdfile)
            myzenfile=p+'/zen'+n
            if os.path.isfile(myzenfile):
                continue

        (retmess, retcode) = pr.pub_record(mdfile,request,testflag,old_dep_id)
        if retcode<= 300:
            if request != 'GET':
                log.info('Response:%s - request:%s - %s' % (mdfile,request,retmess))
            else:
                log.info('Response:%s - request:%s' % (mdfile,request))
                print(retmess)
        else:
            log.error('Response:%s - request:%s - %s:%s' % (mdfile,request,retcode,retmess))
        
sys.exit()


