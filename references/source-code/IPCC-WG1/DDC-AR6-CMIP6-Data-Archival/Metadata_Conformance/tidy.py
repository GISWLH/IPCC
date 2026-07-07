#! /usr/bin/env python

# Usage: ./tidy.py <input dir> 

import sys,os,re,logging
import copy,json
from operator import itemgetter

mydir = os.path.abspath(os.getcwd())
mydate = os.popen('date +%F').read().strip()
#print mydate,mydir

# read option
#print 'Call: %s' % ' '.join(sys.argv)
if len(sys.argv)<1:
    print "Usage: ./tidy.py <input dir>"
    sys.exit()
indir = sys.argv[1]
outdir = indir+'_tidy'


os.chdir(indir)

for root, dirs, files in os.walk(".", topdown=False):
    for f in files:
        #print f
        #print('files ',os.path.join(root, f))
        #if not re.search('cmip6',f) and re.search('.json',f):
        if re.search('cmip6',f):
            #print f
            try:
                readfile = json.loads(open(f,'r').read())
            except:
                print 'Error in reading %s' % f
            writefile = [[]]
            for l in readfile[0]:
                # 1. test types
                #print type(l['checksum_nc']),l['checksum_nc']
                if not isinstance(l['data_ref_syntax'],unicode):
                    print "error data_ref_syntax",l['data_ref_syntax']
                if not isinstance(l['tracking_id_ds'],unicode):
                    print "error tracking_id_ds",l['tracking_id_ds']
                if not isinstance(l['tracking_id_nc'],list):
                    print "error tracking_id_nc",l['tracking_id_nc']
                if not isinstance(l['checksum_nc'],list):
                    if isinstance(l['checksum_nc'],(unicode,str)):
                        dum=[l['checksum_nc']]
                        l['checksum_nc']=dum
                    #print "error checksum_nc",l['checksum_nc']
                if not isinstance(l['report_figures'],list):
                    print "error report_figures",l['report_figures']
                if not isinstance(l['report_subpanels'],list):
                    print "error report_subpanels",l['report_subpanels']

                #special treatment
                if re.search('cmip5',l['data_ref_syntax']):
                    # not existing - no EC-Earth-Consortium contribution to CMIP5: cmip5.output1.EC-Earth-Consortium.EC-EARTH.historical.day.atmos.day.r1i1p1.handle not found on https://cera-www.dkrz.de/wdcc/cmip5/tracking.jsptracking_id=bb17dd27-e183-4816-802f-cfc0049f4b88.zg"
                    # dataset exists - cmip5.output1.MOHC.HadCM3.historical.day.atmos.day.r1i1p1.handle not found on https://cera-www.dkrz.de/wdcc/cmip5/tracking.jsptracking_id=524d347d-67d5-460f-b09c-0a53993db5e9.zg
                    # cmip5.output1.MOHC.HadCM3.historical.day.atmos.day.r1i1p1.v20140110.zg
                    # checksum: 486981c78e7cbba4749be4c95b8c7dcb14dbe0e50ffdcadc9634ff4d2cc2c0f7, 4aad2eb2f1aedef2a0aaa9d7f9a473723cc511141d2d42d2d626f47010258c8c
                    # tracking_id: 524d347d-67d5-460f-b09c-0a53993db5e9, 17335a11-21d1-497c-90cc-82981e56c055
                    if re.search('cmip5.output1.EC-Earth-Consortium',l['data_ref_syntax']):
                        #print l['data_ref_syntax']
                        continue
                    if re.search('cmip5.output1.MOHC.HadCM3.historical.day.atmos.day.r1i1p1',l['data_ref_syntax']):
                        #print l['data_ref_syntax']
                        l['data_ref_syntax'] = "cmip5.output1.MOHC.HadCM3.historical.day.atmos.day.r1i1p1.v20140110.zg"
                        l['checksum_nc'] = [ "486981c78e7cbba4749be4c95b8c7dcb14dbe0e50ffdcadc9634ff4d2cc2c0f7", "4aad2eb2f1aedef2a0aaa9d7f9a473723cc511141d2d42d2d626f47010258c8c"]
                        l['tracking_id_nc'] = [ "524d347d-67d5-460f-b09c-0a53993db5e9", "17335a11-21d1-497c-90cc-82981e56c055" ]
                        #print l['data_ref_syntax']

                # 2. check drs
                if re.search('cmip6',l['data_ref_syntax']):
                    #print l['data_ref_syntax']
                    l['data_ref_syntax'] = re.sub('cmip6','CMIP6',l['data_ref_syntax'])
                    #print l['data_ref_syntax']
                if re.search('CORDEX',l['data_ref_syntax']):
                    #print l['data_ref_syntax']
                    l['data_ref_syntax'] = re.sub('CORDEX','cordex',l['data_ref_syntax'])
                    l['data_ref_syntax'] = re.sub('REKLIES','reklies',l['data_ref_syntax'])
                    #print l['data_ref_syntax']

                # 3. check tracking_id_ds   "tracking_id_ds": "Miss", 
                if re.search('miss',l['tracking_id_ds'].lower()):
                    l['tracking_id_ds'] = ""
                # 4. check lists
                for ll in l['tracking_id_nc']:
                    dum = []
                    #print ll
                    if isinstance(ll,(unicode,str)):
                        if len(ll)>0 and ll !='""':
                            dum.append(ll)
                    if isinstance(ll,list):
                        for lll in ll:
                            #print lll
                            if len(lll)>0 and lll !='""':
                                dum.append(lll)
                    l['tracking_id_nc']=dum
                    #print l['tracking_id_nc']
                for ll in l['checksum_nc']:
                    dum = []
                    #print ll
                    if isinstance(ll,(unicode,str)):
                        if len(ll)>0 and ll !='""':
                            dum.append(ll)
                    if isinstance(ll,list):
                        for lll in ll:
                            #print lll
                            if len(lll)>0 and lll !='""':
                                dum.append(lll)
                    l['checksum_nc']=dum
                    #print l['tracking_id_nc']
                for ll in l['report_figures']:
                    if isinstance(ll,list):
                        dum = []
                        for lll in ll:
                            dum.append(lll)
                        l['report_figures']=dum
                for ll in l['report_subpanels']:
                    if isinstance(ll,list):
                        dum = []
                        for lll in ll:
                            dum.append(lll)
                        l['report_subpanels']=dum
                writefile[0].append(l)
            with open('../'+outdir+'/'+f,'w') as ff:
                json.dump(writefile,ff,indent=4)
            #sys.exit()

sys.exit()
