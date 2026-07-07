#! /usr/bin/env python
"""create, publish, update a single Zenodo record
Version: V0.1 2024-02-07: initial version; PUT not tested (stockhause@dkrz.de),
Version: V1.0 2025-03-06: used for publication of Zenodo records (stockhause@dkrz.de)"""

import os,os.path,re,sys
import json
import requests



class PublishRecord:

    def __init__(self):
        self.return_code=0
        self.return_message='' 
        self.mydir=os.path.dirname(os.path.realpath(__file__))
        self.base_url={'test':'https://sandbox.zenodo.org','zenodo':'https://zenodo.org'}
        self.access_token={'test':open(self.mydir+'/.test_zenodo','r').read().strip(),
                           'zenodo':open(self.mydir+'/.zenodo','r').read().strip()}




    def pub_record(self, mdfile,request,testflag,old_dep_id):
        """analyze request
        """

        # is test?
        if testflag == 0:
            BASE_URL     = self.base_url['zenodo']
            ACCESS_TOKEN = self.access_token['zenodo']
        else:
            BASE_URL     = self.base_url['test']
            ACCESS_TOKEN = self.access_token['test']

        # load md file
        with open(mdfile,'r') as f:
            mdjson=json.loads(f.read())


        # request cases
        if request == 'POST':     # publish new record
            self.post_record(BASE_URL,ACCESS_TOKEN,mdjson,mdfile,testflag)
        elif request == 'PUT':    # update existing record
            self.put_record(BASE_URL,ACCESS_TOKEN,mdjson,mdfile,testflag,old_dep_id)
        elif request == 'DELETE': # delete existing record
            self.delete_record(BASE_URL,ACCESS_TOKEN,mdjson,mdfile)
        elif request == 'GET':    # get existing record
            self.get_record(BASE_URL,ACCESS_TOKEN,mdjson)

        return (self.return_message,self.return_code)


    def get_record(self,BASE_URL,ACCESS_TOKEN,mdjson):
        """get existing record and return json content
        """
        # get record id from mdjson
        dep_id = mdjson["id"] # mdjson["metadata"]["prereserve_doi"]["recid"] 

        # GET /api/deposit/depositions/:id
        r = requests.get('%s/api/deposit/depositions/%s?access_token=%s' % (BASE_URL,dep_id,ACCESS_TOKEN))

        self.return_code=r.status_code
        if r.status_code >= 300:
            self.return_message=r.json()['message']
        else:
            self.return_message=json.dumps(r.json(),indent=4)

        return

    
    def delete_record(self,BASE_URL,ACCESS_TOKEN,mdjson,mdfile):
        """delete existing record (without doi)
        """
        # get record id from mdjson
        dep_id = mdjson["id"] # mdjson["metadata"]["prereserve_doi"]["recid"] 

        # DELETE /api/deposit/depositions/:id
        r = requests.delete('%s/api/deposit/depositions/%s' % (BASE_URL,dep_id),
                params={'access_token': ACCESS_TOKEN})

        self.return_code=r.status_code
        if r.status_code >= 300:
            self.return_message=r.json()['message']
        else:
            self.return_message='Record deleted.'

        # flag file in dir as deleted
        (filedir,myfile) = os.path.split(mdfile)
        os.rename(mdfile,os.path.join(filedir,'deleted_'+myfile))
        
        return

    
    def post_record(self,BASE_URL,ACCESS_TOKEN,mdjson,mdfile,testflag):
        """post new record and store published record as file
        """
        # NOTE: Publish step 4. to be tested in production system

        headers = {"Content-Type": "application/json"}
        params  = {'access_token': ACCESS_TOKEN}

        
        # 0. get files for upload and set filename for output
        (filedir,myfile) = os.path.split(mdfile)
        files=[re.split('\.',re.sub('md_','',myfile))[0]+'.json',re.split('\.',re.sub('md_','',myfile))[0]+'.csv']
        outzen=filedir+'/zen'+myfile
        
        # 1. create empty record
        r = requests.post('%s/api/deposit/depositions' % BASE_URL,
                   params=params,
                   json={},
                   headers=headers)
        if r.status_code >= 300:
            self.return_message=r.json()['message']
            self.return_code=r.status_code
            return
            
        dep_id = r.json()["metadata"]["prereserve_doi"]["recid"] #r.json()["id"]
        doi = r.json()["metadata"]["prereserve_doi"]["doi"]
        bucket_url = r.json()["links"]["bucket"]
        # add doi to json-ld file
        with open(filedir+'/'+files[0],'r') as f2:
            jsonld=json.loads(f2.read())
            jsonld['@id']='https://doi.org/'+doi
            jsonld['identifier']='https://doi.org/'+doi
        with  open(filedir+'/'+files[0],'w') as f3:
            f3.write(json.dumps(jsonld,indent=4))

        # 2. upload files
        for file in files:
            with open(filedir+'/'+file, "rb") as fp:
                r = requests.put(
                    "%s/%s" % (bucket_url, file),
                    data=fp,
                    params=params,
                )
            if r.status_code >= 300:
                self.return_message=r.json()['message']
                self.return_code=r.status_code
                return

        # 3. upload metadata
        r = requests.put('%s/api/deposit/depositions/%s' % (BASE_URL,dep_id),
                         params={'access_token': ACCESS_TOKEN}, data=json.dumps(mdjson),
                         headers=headers)

        if r.status_code >= 300:
            self.return_message=r.json()['message']
            self.return_code=r.status_code
            return

        # 4. publish: not possible in sandbox, 405 for operation; community=ipcc-ar6 not working -> comment out and set manually
        #if testflag == 0:
        #    r = requests.put('%s/api/deposit/depositions/%s/actions/publish' % (BASE_URL,dep_id),
        #                 params={'access_token': ACCESS_TOKEN} )
        #    if r.status_code >= 300:
        #        self.return_message=r.json()['message']
        #        self.return_code=r.status_code
        #        return

        self.return_code=r.status_code
        
        js = open(outzen,'w')
        js.write(json.dumps(r.json(),indent=4))
        js.close()

        return

    
    def put_record(self,BASE_URL,ACCESS_TOKEN,mdjson,mdfile,testflag,old_dep_id):
        """update record (publish as new version) store updated record as file 
        (requires published doi and is therefore only available in production not in sandbox/test environment)
        """
        # NOTE: To be thouroughly tested in production system because unavailable in test environment 
        
        headers = {"Content-Type": "application/json"}
        params  = {'access_token': ACCESS_TOKEN}

        
        # 0. get files for upload, set filename for output and create minimal metadata update json
        (filedir,myfile) = os.path.split(mdfile)
        files=[re.split('\.',re.sub('md_','',myfile))[0]+'.json',re.split('\.',re.sub('md_','',myfile))[0]+'.csv']
        outzen=filedir+'/zen'+myfile
        updmd={"metadata":{"publication_date":mdjson["metadata"]["publication_date"],"version":mdjson["metadata"]["version"],"dates":mdjson["metadata"]["dates"]}}

        # 1. new version of record incl. files and md; get old files and bucket_url
        # NOTES: - The response body of this action is NOT the new version deposit, but the original resource.
        # The new version deposition can be accessed through the "latest_draft" under "links" in the response body.
        # - The id used to create this new version has to be the id of the latest version.
        # It is not possible to use the global id that references all the versions.
        r = requests.post('%s/api/deposit/depositions/%s/actions/newversion' % (BASE_URL,old_dep_id),
                          params={'access_token': ACCESS_TOKEN})
        if r.status_code >= 300:
            self.return_message=r.json()['message']
            self.return_code=r.status_code
            return
        new_version_url = r.json()["links"]["latest_draft"]
        dep_id=re.split('/',new_version_url)[-1]

        r = requests.get('%s/api/deposit/depositions/%s?access_token=%s' % (BASE_URL,dep_id,ACCESS_TOKEN))
        if r.status_code >= 300:
            self.return_message=r.json()['message']
            self.return_code=r.status_code
            return
            
        doi = r.json()["metadata"]["prereserve_doi"]["doi"]
        bucket_url = r.json()["links"]["bucket"]
        oldfiles = []
        # add doi to json-ld file
        with open(filedir+'/'+files[0],'r') as f2:
            jsonld=json.loads(f2.read())
            jsonld['@id']='https://doi.org/'+doi
            jsonld['identifier']='https://doi.org/'+doi
        with  open(filedir+'/'+files[0],'w') as f3:
            f3.write(json.dumps(jsonld,indent=4))

        for l in r.json()["files"]:
            old_files.append(l["id"])

        
        # 2. delete existing and upload new files
        for ofile in oldfiles:            
            r = requests.delete('%s/api/deposit/depositions/%s/files/%s' % (BASE_URL,dep_id,ofile),
                                params={'access_token': ACCESS_TOKEN})
            if r.status_code >= 300:
                self.return_message=r.json()['message']
                self.return_code=r.status_code
                return

        for file in files:
            with open(filedir+'/'+file, "rb") as fp:
                r = requests.put(
                    "%s/%s" % (bucket_url, file),
                    data=fp,
                    params=params,
                )
            if r.status_code >= 300:
                self.return_message=r.json()['message']
                self.return_code=r.status_code
                return

        # 3. upload updated metadata
        r = requests.put('%s/api/deposit/depositions/%s' % (BASE_URL,dep_id),
                         params={'access_token': ACCESS_TOKEN}, data=json.dumps(updmd),
                         headers=headers)

        if r.status_code >= 300:
            self.return_message=r.json()['message']
            self.return_code=r.status_code
            return

        # 4. publish: not possible in sandbox, 405 in operation
        #if testflag == 0:
        #    r = requests.put('%s/api/deposit/depositions/%s/actions/publish' % (BASE_URL,dep_id),
        #             params={'access_token': ACCESS_TOKEN} )
        #    if r.status_code >= 300:
        #        self.return_message=r.json()['message']
        #        self.return_code=r.status_code
        #        return

        self.return_code=r.status_code
        
        js = open(outzen,'w')
        js.write(json.dumps(r.json(),indent=4))
        js.close()

        return

    
                
if __name__ == '__main__':

    old_dep_id=0
    # 1. GET example
    ##mdfile='/home/k/k204082/export/AR6_figures/20250221/zenmd_fig_3_5.json'
    #mdfile='/home/k/k204082/export/AR6_figures/20250221/zenmd_fig_9_15.json'
    #request='GET'
    #testflag=1
    # 2. POST example
    #mdfile='/home/k/k204082/export/AR6_figures/20250221/md_fig_3_5.json'
    #testflag=0
    #mdfile='/home/k/k204082/export/AR6_figures/20250221/md_fig_3_11.json'
    #mdfile='/home/k/k204082/export/AR6_figures/20250221/md_fig_9_15.json'
    #mdfile='/home/k/k204082/export/AR6_figures/20250221/md_fig_9_12.json'
    #mdfile='/home/k/k204082/export/AR6_figures/20250221/md_fig_Atlas_13.json'
    #mdfile='/home/k/k204082/export/AR6_figures/20250221/md_fig_10_11.json'
    mdfile='/home/k/k204082/export/AR6_figures/20250305/md_fig_11_11.json'
    request='POST'
    testflag=1
    # 3. DELETE example
    #mdfile='/home/k/k204082/export/AR6_figures/20250221/zenmd_fig_3_5.json'
    #mdfile='/home/k/k204082/export/AR6_figures/20250221/zenmd_fig_3_11.json'
    #mdfile='/home/k/k204082/export/AR6_figures/20250221/zenmd_fig_9_15.json'
    #request='DELETE'
    #testflag=1
    # 4. PUT example
    #mdfile='/home/k/k204082/export/AR6_figures/20250221/md_fig_3_5.json'
    #old_dep_id=27171
    #request='PUT'
    #testflag=1
    
    pr = PublishRecord()
    (retmess, retcode) = pr.pub_record(mdfile,request,testflag,old_dep_id)
    print(retmess)
    print(retcode)
