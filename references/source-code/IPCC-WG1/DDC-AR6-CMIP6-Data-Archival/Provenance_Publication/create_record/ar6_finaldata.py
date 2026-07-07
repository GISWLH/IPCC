#! /usr/bin/env python

import sys,os,os.path,re
import json, copy
from string import Template

try:
    import oracledb
except:
    print("Cannot import module oracledb")
    sys.exit()

os.environ['NLS_LANG']="AMERICAN_AMERICA.AL32UTF8"
os.environ['LANG']="en_US.UTF-8"
os.environ['LC_CTYPE']="en_US.UTF-8"
os.environ['LC_NUMERIC']="en_US.UTF-8"
os.environ['LC_TIME']="en_US.UTF-8"
os.environ['LC_COLLATE']="en_US.UTF-8"
os.environ['LC_MONETARY']="en_US.UTF-8"
os.environ['LC_MESSAGES']="en_US.UTF-8"
os.environ['LC_PAPER']="en_US.UTF-8"
os.environ['LC_NAME']="en_US.UTF-8"
os.environ['LC_ADDRESS']="en_US.UTF-8"
os.environ['LC_TELEPHONE']="en_US.UTF-8"
os.environ['LC_MEASUREMENT']="en_US.UTF-8"
os.environ['LC_IDENTIFICATION']="en_US.UTF-8"
os.environ['LC_ALL']="" 

mydir = '/'.join(re.split('/',os.path.abspath(sys.argv[0]).strip())[:-1])
mydate=os.popen('date +%Y-%m-%d').read().strip()
outdir = os.path.abspath(os.path.expanduser("~/export/AR6_figures/"+re.sub('-','',mydate)))
if not os.path.isdir(outdir):        
    os.mkdir(outdir)

def getColumns(gcur):
    col_names=[]
    for i in range(0, len(gcur.description)):
        col_names.append(gcur.description[i][0])
    return col_names


# 1. Read sql selects and json output template
sqls={}
for l in open(mydir+'/ar6_finaldata_sql.conf','r').readlines():
    if re.match(r'^(\#)',l.strip()) or len(l.strip()) == 0:
        continue            
    key  = re.split(':',l.strip())[0]
    value = ':'.join(re.split(':',l.strip())[1:]).strip()
    sqls[key]=value

with open(mydir+'/zenodo_md_template.json','r') as f:
    templ_mdr=Template(f.read())
with open(mydir+'/zenodo_file_template.json','r') as f:
    templ_filer=Template(f.read())


# 2. Connect to db
cuser  = "meta_select"
cpw    = open(mydir+'/.meta_select','r').read().strip()
try:
    sdbfile2 =  cuser+'/'+cpw+'@'+'( DESCRIPTION = ( ADDRESS_LIST = ( ADDRESS = ( PROTOCOL = TCP ) ( HOST = cera-db.dkrz.de ) ( PORT = 1521 ) ) ) ( CONNECT_DATA = ( SERVER = DEDICATED ) ( SERVICE_NAME = pcera ) ))'
    
except IOError:
    print("\nCannot connect to DB=\'%s\'. Check password in file .meta_select\n" % cuser)
    raise
try:
    iconn = oracledb.connect(sdbfile2)
    cur = iconn.cursor()
except IOError as err:
    print("\nDB not found: %s :\n%s" % (':'.join(re.split(':',sdbfile2)[:2]),err))
    raise

# 3. get list of existing figures
figlist = []
try:
    cur.execute(sqls['FIG_LIST'])
except oracledb.DatabaseError as err:
    print("DB sql select error:",err)
    raise

data = cur.fetchall()
if not data:
    print("No results returned for FIG_LIST:\n%s" % sqls['FIG_LIST'])

col_names=getColumns(cur)
for d in data:
    line = {}
    for k2,v2 in zip(col_names,d):
        line[str.upper(k2)]=str(v2)
    figlist.append(line)
print('Number of figures: %s' % len(figlist))
    
# 4. get figure information
for f in figlist:
    outfigjson   = outdir+'/md_fig_'+re.sub('\.','_',f['FIGURE'])+'.json'
    outfigcsv    = outdir+'/fig_'+re.sub('\.','_',f['FIGURE'])+'.csv'
    outfigjson2  = outdir+'/fig_'+re.sub('\.','_',f['FIGURE'])+'.json'
    repl_md={'fig_no':f['FIGURE'],'pubdate':mydate,'version':re.sub('-','',mydate)}
    templ_md=json.loads(templ_mdr.substitute(repl_md))
    figinfo    = []
    myselect   = sqls['FIG_INFO']
    templ = dict(citation_id=f['CITATION_ID'])
    myselect=Template(sqls['FIG_INFO']).safe_substitute(templ)
    try:
        cur.execute(myselect)
    except oracledb.DatabaseError as err:
        print("DB sql select error:",err)
        raise

    data = cur.fetchall()
    if not data:
        print("No results returned for FIG_INFO:citation_id=%s" % (f['CITATION_ID']))
        myselect   = sqls['FIG_INFO2']
        templ = dict(citation_id=f['CITATION_ID'])
        myselect=Template(sqls['FIG_INFO2']).safe_substitute(templ)

        try:
            cur.execute(myselect)
        except oracledb.DatabaseError as err:
            print("DB sql select error:",err)
            raise

        data = cur.fetchall()
        if not data:
            print("No results returned for FIG_INFO2:citation_id=%s" % (f['CITATION_ID']))
            myselect   = sqls['FIG_INFO3']
            templ = dict(citation_id=f['CITATION_ID'])
            myselect=Template(sqls['FIG_INFO3']).safe_substitute(templ)

            try:
                cur.execute(myselect)
            except oracledb.DatabaseError as err:
                print("DB sql select error:",err)
                raise

            data = cur.fetchall()
            if not data:
                print("No results returned for FIG_INFO3:citation_id=%s" % (f['CITATION_ID']))
                continue
        
    col_names=getColumns(cur)
    for d in data:
        line = {}
        for k2,v2 in zip(col_names,d):
            line[str.upper(k2)]=str(v2)
        figinfo.append(line)

    print('Number of datasets for figure %s: %s' % (f['FIGURE'],len(figinfo)))

    # 5a. create csv 
    csv_cols=['DATASET','DS_PID','RELATION','DOI_COLLECTION','AR6_CMIP6_DOI','CMIP6_DOI']
    csv = open(outfigcsv,'w')
    csv.write(','.join(csv_cols))
    csv.write('\n')
    for l in figinfo:
        myvals=[]
        for ll in csv_cols:
            if ll=='RELATION':
                myvals.append('isPartOf')
            elif re.search('10\.',l[ll]):
                myvals.append('https://doi.org/'+l[ll])
            elif l[ll]=='None':
                myvals.append('')
            else:
                myvals.append(l[ll])

        csv.write(','.join(myvals))
        csv.write('\n')
    csv.close()

    # 5b. create json-ld file for upload 
    js2 = open(outfigjson2,'w')
    repl_file={'fig_no':f['FIGURE'],'pubdate':mydate,'version':re.sub('-','',mydate)}
    myrels=[]
    mydois=[]
    myhdls=[]
    last_line={}

    for l in figinfo:
        if l['CMIP6_DOI'] not in mydois:
            if len(myhdls)>0:
                # 1. CMIP6 DOI -> Hdl
                if last_line['AR6_CMIP6_DOI']=='None':
                    myrels.append({'source':last_line['DOI_COLLECTION'],'source_id':last_line['CMIP6_DOI'],'targets':myhdls})
                else:
                    myrels.append({'source':last_line['DOI_COLLECTION'],'source_id':last_line['CMIP6_DOI'],'ar6':last_line['AR6_CMIP6_DOI'],'targets':myhdls})
                # 2. AR6 DOI -> Hdl
                myhdls=[]

            myhdls.append({'target':l['DATASET'],'target_id':l['DS_PID']})
            mydois.append(l['CMIP6_DOI'])
        else:
            myhdls.append({'relation':'hasPart','target':l['DATASET'],'target_id':l['DS_PID']})
        last_line=l

    
    # 5c. create md json
    myrel2s=[]
    mydois=[]
    myhdls=[]
    for l in figinfo:
        if l['CMIP6_DOI'] not in mydois:
            mydois.append(l['CMIP6_DOI'])
            myrel2s.append({'identifier':l['CMIP6_DOI'],'relation':'cites','resource_type':'dataset'})  #'input data'
            if l['AR6_CMIP6_DOI']=='None':
                pass
            else:
                myrel2s.append({'identifier':l['AR6_CMIP6_DOI'],'relation':'cites','resource_type':'dataset'})  #'input data'
        if l['DS_PID'] not in myhdls:
            myhdls.append(l['DS_PID'])
            myrel2s.append({'identifier':l['DS_PID'],'relation':'cites','resource_type':'dataset'})   #'input dataset'
    myfig={'identifier':figinfo[0]['FIGURE_DOI'],'relation':'isCitedBy','resource_type':'dataset'}   #'final data'
    repl_file['findata_doi']='https://doi.org/'+figinfo[0]['FIGURE_DOI']
    myrel2s.append(myfig)
    myrel2s.append({'identifier':figinfo[0]['FIG_URL'],'relation':'isCitedBy','resource_type':'image'})
    repl_file['fig_url']=figinfo[0]['FIG_URL']
    if 'CODE_DOI' in figinfo[0]:
        myrel2s.append({'identifier':figinfo[0]['CODE_DOI'],'relation':'isCitedBy','resource_type':'software'})
    else:
        print('No code doi for figure %s' % f['FIGURE'])
    if 'CODE_GIT' in figinfo[0]:
        myrel2s.append({'identifier':figinfo[0]['CODE_GIT'],'relation':'isCitedBy','resource_type':'software'})
    else:
        print('No code in github for figure %s' % f['FIGURE'])

    # RDA Complex Citation WG - Use Case IPCC
    myrel2s.append({'identifier':'10.5281/zenodo.7684260','relation':'isDocumentedBy','resource_type':'presentation'})
    repl_file['usecase_doi']='https://doi.org/10.5281/zenodo.7684260'
    templ_md['metadata']['related_identifiers']=myrel2s
    # CMIP6 paper reference
    myrel2s.append({'identifier':'10.5194/gmd-9-1937-2016','relation':'cites','resource_type':'publication'})
    repl_file['c6paper_doi']='https://doi.org/10.5194/gmd-9-1937-2016'
    # CCO paper reference
    myrel2s.append({'identifier':'10.5281/zenodo.14106602','relation':'cites','resource_type':'publication'})
    repl_file['cco_doi']='https://doi.org/10.5281/zenodo.14106602'
    # AR6 WGI chapter reference
    myrel2s.append({'identifier':f['CHAPTER'],'relation':'isCitedBy','resource_type':'publication'})
    repl_file['ar6ch_doi']='https://doi.org/'+f['CHAPTER']
    
    js = open(outfigjson,'w')
    js.write(json.dumps(templ_md,indent=4))
    js.close()

    # 5b.  write json-ld
    templ_file=json.loads(templ_filer.substitute(repl_file))
    templ_c=copy.deepcopy(templ_file['citation'])
    if 'CODE_DOI' in figinfo[0]:
        templ_file['@reverse']['citation'].append({"@type": "SoftwareSourceCode", "@id": 'https://doi.org/'+figinfo[0]['CODE_DOI']})
    if 'CODE_GIT' in figinfo[0]:
        templ_file['@reverse']['citation'].append({"@type": "SoftwareSourceCode", "@id": figinfo[0]['CODE_GIT']})

    mycits=[]

    for c in myrels:
        templ_cit=copy.deepcopy(templ_c)
        templ_cit[0]['name']=c['source']
        templ_cit[0]['@id']='https://doi.org/'+c['source_id']
        
        myhdls=[]
        for t in c['targets']:
            myhdls.append({'@type': 'Dataset', 'name': t['target'], '@id': t['target_id'], 'additionalType':'Provenance'})
        if 'ar6' in c:
            templ_cit[0]['hasPart'][1]['name']=c['source']
            templ_cit[0]['hasPart'][1]['@id']='https://doi.org/'+c['ar6']
            templ_cit[0]['hasPart'][1]['hasPart']=myhdls
            templ_cit[0]['hasPart'][:-1]=myhdls
        else:
            templ_cit[0]['hasPart']=myhdls
        mycits += templ_cit

    templ_file['citation']=mycits

    js2.write(json.dumps(templ_file,indent=4))
    js2.close()
    
sys.exit()
