from netCDF4 import Dataset
import urllib
import glob
import pandas as pd
import xmltodict

fnames=glob.glob("../netcdfs/annClim/PMIP3/tas_annClim*nc")
numncfiles=len(fnames)

for i in range(0,numncfiles):
  file = fnames[i]
  #Step 1 load the netcdf file and get the values of several global attributes
  r = Dataset(file, mode='r')
  pid = getattr(r,'tracking_id')
  project_id = getattr(r,'project_id')
  product=getattr(r,'product')
  institute_id = getattr(r,'institute_id')
  model_id = getattr(r,'model_id')
  experiment_id = getattr(r,'experiment_id')
  frequency = getattr(r,'frequency')
  table_id = getattr(r,'table_id')
  realization = getattr(r,'realization')
  initialization_method = getattr(r,'initialization_method')
  physics_version = getattr(r,'physics_version')
  tracking_id = getattr(r,'tracking_id')
  r.close()
  
  data_ref_syntax = project_id+'.'+product+'.'+institute_id+'.'+model_id+'.'+experiment_id
  ens_mem='r'+str(realization)+'i'+str(initialization_method)+'p'+str(physics_version)

  version_number=str(-999)
  datasetpidurl = 'https://esgf-node.llnl.gov/esg-search/search?type=File&tracking_id='+tracking_id 
  print(datasetpidurl)
  readurl = urllib.request.urlopen(datasetpidurl).read() 
  print(readurl)
  data_xml = xmltodict.parse(readurl) 
  try: 
      file_full_name = data_xml['response']['result']['doc'][3]['str'][5]['#text'] 
  except: 
      try: 
          file_full_name = data_xml['response']['result']['doc'][2]['str'][5]['#text'] 
      except: 
          try: 
              file_full_name = data_xml['response']['result']['doc'][1]['str'][5]['#text'] 
          except: 
              file_full_name = data_xml['response']['result']['doc']['str'][5]['#text'] 
  version_number = file_full_name [9]
  
  if i == 0:
    print('DATA_REF_SYNTAX,FREQUENCY,MODELING_REALM,TABLE_ID,ENSEMBLE_MEMBER,VERSION_NO,VAR_NAME,HANDLE,SUBPANEL')
    print(data_ref_syntax+','+frequency+',atmos,Amon,'+ens_mem+','+version_number+',tas,'+pid+',') 
  else:
    print(data_ref_syntax+','+frequency+',atmos,Amon,'+ens_mem+','+version_number+',tas,'+pid+',')
