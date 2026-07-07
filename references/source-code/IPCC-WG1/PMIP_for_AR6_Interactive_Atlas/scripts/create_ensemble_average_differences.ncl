; These scripts aim to:
;   1. Create monthly climatologies of each cal-adj simulation (this script)
;   2. Compute differences in these climatologies from the piControl climatology
;   3. Regrid each climate difference onto a 1x1 grid
;   4. Combine into an ensemble file

; Required metadata to be taken from each file:
;   tracking_id of piControl file
;   tracking_id of expt file
;   name of model
;   X resolution of model
;   Y resolution of model

; This particular script does steps 2-4, but requires create_monClim_annClim_files.ncl to have been run beforehand

;;;;;;;;;;;;;;;;;;;
;===================================================================================================
; First define some useful functions 
; read in latlon variable from two files
; compute the difference in them
; interpolate onto a common 1x1 grid (to help with ensemble averaging)
undef("read_diff_latlon_var")
function read_diff_latlon_var(filehandle_a,filehandle_b,variable_name:string,PERCENTAGE:logical)
; path for TS file(s), variable name
local filehandle_a,filehandle_b,variable_name,fil
begin
  ;read in variable and perform some checks.
  if .not.isfilevar(filehandle_a,variable_name) then
    ;Hard exit if not correct, as only valid files should have been selected with find_files_wVar  
    print("There is not a "+variable_name+" variable in filehandle_a")
    exit
  end if
  var_in_a = filehandle_a->$variable_name$
  if .not.isfilevar(filehandle_b,variable_name) then
    ;Hard exit if not correct, as only valid files should have been selected with find_files_wVar  
    print("There is not a "+variable_name+" variable in filehandle_b")
    exit
  end if
  var_in_b = filehandle_b->$variable_name$
  diff_in=var_in_a
  if PERCENTAGE then
    var_in_b=where(var_in_b.ne.0,var_in_b,var_in_b@_FillValue);needed to avoid dividing by 0
    diff_in=100.*(var_in_a-var_in_b)/var_in_b
    diff_in@units="percentage"
  else
    diff_in=var_in_a-var_in_b
  end if

  ;rename the (x,y) variables for later compatibility
  if diff_in!0.eq."latitude" then
    diff_in!0="lat"
  end if
  if diff_in!1.eq."longitude" then
    diff_in!1="lon"
  end if
  
  ; REGRID
  a = addfile("../netcdfs/land_sea_mask_1degree.nc4","r")
  ;This file is taken from the ATLAS repository under referenceGrids
  lsdata = a->sftlf
  lat=lsdata&lat
  lat@axis = "Y"
  lon=lsdata&lon
  lon@axis = "X"
  diff_in=lonFlip(diff_in)
  diff_out=linint2_Wrap(diff_in&lon,diff_in&lat,diff_in,True,lon,lat,0)
  diff_out@regrid="regridded from native grid using bilinear interpolation"

  return(diff_out)
end;read_diff_latlon_var 

;===================================================================================================
; read in latlon variable from a file
; optionally interpolate onto a common 1x1 grid (to help with ensemble averaging)
undef("read_latlon_var")
function read_latlon_var(name_wfullpath:string,variable_name:string)
local name_wfullpath,variable_name,fil
begin
  ;read in variable and perform some checks.
  if .not.isfilepresent(name_wfullpath) then
    ;Hard exit if not correct, as only valid files should have been selected with find_files_wVar  
    print("There is not a appropriate file called "+name_wfullpath)
    exit
  end if
  fil=addfile(name_wfullpath,"r")
  if .not.isfilevar(fil,variable_name) then
    ;Hard exit if not correct, as only valid files should have been selected with find_files_wVar  
    print("There is not a "+variable_name+" variable in "+name_wfullpath)
    exit
  end if
  var_in = fil->$variable_name$

  ;rename the (x,y) variables for later compatibility
  if var_in!0.eq."latitude" then
    var_in!0="lat"
  end if
  if var_in!1.eq."longitude" then
    var_in!1="lon"
  end if
  
  
  ; REGRID
  a = addfile("../netcdfs/land_sea_mask_1degree.nc4","r")
  ;This file is taken from the ATLAS repository under referenceGrids
  lsdata = a->sftlf
  lat=lsdata&lat
  lat@axis = "Y"
  lon=lsdata&lon
  lon@axis = "X"
  var_in=lonFlip(var_in)
  var_out=linint2_Wrap(var_in&lon,var_in&lat,var_in,True,lon,lat,0)
  var_out@regrid="regridded from native grid using bilinear interpolation"
  
  return(var_out)
end;read_latlon_var

;=================================================================================================
; find netcdf files that contain a desired variable and fit a filename string. 
;
undef("find_files_wVar")
function find_files_wVar(data_dir:string,name_str:string,variable_name:string,PMIP4_not_PMIP3:logical)
local data_dir,name_str,variable_name,fil,PMIP4_not_PMIP3
begin
  if isatt(data_dir,"quiet") then
    QUIET=data_dir@quiet
  else
    QUIET=False
  end if
  PMIP3_search_string="{bcc-csm1-1,CCSM4,CNRM-CM5,COSMOS-ASO,CSIRO-Mk3-6-0,CSIRO-Mk3L-1-2,EC-EARTH-2-2,FGOALS-g2,FGOALS-s2,GISS-E2-R,HadGEM2-CC,HadGEM2-ES,IPSL-CM5A-LR,MIROC-ESM,MPI-ESM-P,MRI-CGCM3}"
  PMIP4_search_string="{ACCESS-ESM1-5,AWI-ESM-1-1-LR,CESM2,CNRM-CM6-1,EC-Earth3-LR,FGOALS-f3-L,FGOALS-g3,GISS-E2-1-G,HadGEM3-GC31-LL,INM-CM4-8,IPSL-CM6A-LR,MIROC-ES2L,MPI-ESM1-2-LR,MRI-ESM2-0,NESM3,NorESM1-F,NorESM2-LM}"
  if PMIP4_not_PMIP3 then
    ncfiles=systemfunc("ls "+data_dir+"/*_"+PMIP4_search_string+"*_[0-9]*-*.nc")
  else
    ncfiles=systemfunc("ls "+data_dir+"/*_"+PMIP3_search_string+"*_[0-9]*-*.nc")
  end if
  if any(ismissing(ncfiles)) then
    if .not.QUIET then
     print("find_files_wVar: There are no cvdp_data netcdf files in "+data_dir+"/")
    end if
    ncfiles_wVar="missing"
  else
    if any(ismissing(str_match_ind(ncfiles,name_str))) then
      if .not.QUIET then
        print("find_files_wVar: There are no cvdp_data netcdf files in "+data_dir+"/ containing the string "+name_str)
      end if
      ncfiles_wVar="missing"
    else
      ncfiles_match=str_match(ncfiles,name_str)
      relevant=new((/dimsizes(ncfiles_match),dimsizes(variable_name)/),logical)
      relevant=(/False/)
      do i=0,dimsizes(ncfiles_match)-1
        this_file=ncfiles_match(i)
        if isfilepresent(this_file) then
          fil = addfile (this_file, "r")
          do var_i=0,dimsizes(variable_name)-1
            if isfilevar(fil,variable_name(var_i)) then
              relevant(i,var_i) = True
            end if
          end do
        end if
      end do
      if all(.not.(dim_num(relevant).eq.dimsizes(variable_name))) then
        ncfiles_wVar="missing"
        if .not.QUIET then
          print("find_files_wVar: There are no cvdp_data netcdf files that contain "+name_str+" and have the requested variable")    
        end if
      else
        ncfiles_wVar=ncfiles_match(ind(dim_num(relevant).eq.dimsizes(variable_name)))
      end if
    end if
  end if
  return(ncfiles_wVar)
end;find_files_wVar

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
undef("find_pair_files_wVar")
function find_pair_files_wVar(data_dir:string,name_str_a:string,name_str_b:string,variable_name:string,PMIP4_not_PMIP3:logical)
local data_dir,name_str_a,name_str_b,variable_name,ncfile_wVar_a,ncfiles_wVar_b,match_count,name_i,ncfiles_wVar_both
begin
  if isStrSubset(name_str_b,name_str_a).or.isStrSubset(name_str_a,name_str_b) then
    print("find_pair_files_wVar: This program cannot work with one name string being a subset of the other")
    print("find_pair_files_wVar:  You may want to rename your cvdp_data files")
    exit
  end if
  ncfiles_wVar_a=find_files_wVar(data_dir,name_str_a,variable_name,PMIP4_not_PMIP3)
  ncfiles_wVar_b=find_files_wVar(data_dir,name_str_b,variable_name,PMIP4_not_PMIP3)
  ncfiles_wVar_both=new((/dimsizes(ncfiles_wVar_a),2/),string) ;create a holding array for the matching ones
  match_count=0
  do name_i=0,dimsizes(ncfiles_wVar_a)-1
    a_nopath=str_get_field(ncfiles_wVar_a(name_i),str_fields_count(ncfiles_wVar_a(name_i),"/"),"/")
    gcm=str_get_field(str_sub_str(a_nopath,name_str_a,":"),1,":")
    if .not.any(ismissing(str_match_ind(ncfiles_wVar_b,gcm))) then
      if dimsizes(str_match_ind(ncfiles_wVar_b,gcm)).ne.1 then
        print("find_pair_files_wVar: I've found multiple gcm id matches for "+gcm+" in "+name_str_a)
        print("find_pair_files_wVar:  I'm not sure how to continue.")
        print("find_pair_files_wVar:   matches = "+str_match(ncfiles_wVar_b,gcm))
        exit
      else
        ncfiles_wVar_both(match_count,0)=ncfiles_wVar_a(name_i)
        ncfiles_wVar_both(match_count,1)=str_match(ncfiles_wVar_b,gcm)
        match_count=match_count+1
      end if
    end if
  end do

  if match_count.eq.0 then
    print("find_pair_files_wVar: No matches found for cvdp_data names that differ solely by having "+name_str_b+" instead of "+name_str_a+" at the end")
    ncfiles_wVar="missing"
  else
    ncfiles_wVar=ncfiles_wVar_both(ind(.not.ismissing(ncfiles_wVar_both(:,0))),:)
  end if
  
  return(ncfiles_wVar)
end;find_pair_files_wVar

;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
undef("write_ensemble_difference_file")
procedure write_ensemble_difference_file(out_file_name:string,input_file_paths:string,variable_name:string,MONTHLY:logical,PMIP4_not_PMIP3:logical,PERCENTAGE:logical)
local out_file_name,input_file_paths,variable_name,MONTHLY,PMIP4_not_PMIP3,PERCENTAGE,n_gcms,piControl_tracking_id,tracking_id,model_name,\
      resX,resY,piControl_url,further_info_url
begin
  n_gcms=dimsizes(input_file_paths(:,0))
  piControl_tracking_id=new(n_gcms, string)
  piControl_tracking_id!0="model"
  tracking_id=new(n_gcms, string)
  tracking_id!0="model"
  model_name=new(n_gcms, string)
  model_name!0="model"
  resX=new(n_gcms, integer)
  resX!0="model"
  resY=new(n_gcms, integer)
  resY!0="model"
  years_averaged=new(n_gcms,string)
  years_averaged!0="model"
  piControl_url=new(n_gcms,string)
  piControl_url!0="model"
  piControl_years_averaged=new(n_gcms,string)
  piControl_years_averaged!0="model"
  further_info_url=new(n_gcms,string)
  further_info_url!0="model"
  if MONTHLY then
    ensemble_differences=new((/n_gcms,12,180,360/),float)
    ensemble_differences!0="model"
    ensemble_differences!1="month"
    ensemble_differences!2="lat"
    ensemble_differences!3="lon"
  else
    ensemble_differences=new((/n_gcms,180,360/),float)
    ensemble_differences!0="model"
    ensemble_differences!1="lat"
    ensemble_differences!2="lon"
  end if

  do gcm_i=0,n_gcms-1
    str_frags=str_split(input_file_paths(gcm_i,0),"/")
    f1=str_frags(4)
    f1_c=stringtocharacter(str_frags(4))
    years_averaged(gcm_i)=tostring(f1_c(str_index_of_substr(f1,".nc", -1)-13:str_index_of_substr(f1,".nc", -1)-1))
    delete([/str_frags,f1_c/])
    str_frags=str_split(input_file_paths(gcm_i,1),"/")
    f1=str_frags(4)
    f1_c=stringtocharacter(str_frags(4))
    piControl_years_averaged(gcm_i)=tostring(f1_c(str_index_of_substr(f1,".nc", -1)-13:str_index_of_substr(f1,".nc", -1)-1))
    delete([/str_frags,f1_c/])
    fila=addfile(input_file_paths(gcm_i,0),"r")
    tracking_id(gcm_i)=fila@tracking_id
    X=fila->lat
    resX(gcm_i)=dimsizes(X)
    Y=fila->lon
    resY(gcm_i)=dimsizes(Y)
    delete([/X,Y/])
    filb=addfile(input_file_paths(gcm_i,1),"r")
    if PMIP4_not_PMIP3 then
      model_name(gcm_i)=fila@source_id
      piControl_url(gcm_i)=filb@further_info_url
      further_info_url(gcm_i)=fila@further_info_url
    else
      model_name(gcm_i)=fila@model_id
    end if
    piControl_tracking_id(gcm_i)=filb@tracking_id
    if gcm_i.eq.0
      diff=read_diff_latlon_var(fila,filb,variable_name,PERCENTAGE)
      ensemble_differences&lat=diff&lat
      ensemble_differences&lon=diff&lon
      if MONTHLY then 
        ensemble_differences(gcm_i,:,:,:)=(/diff/)
      else
        ensemble_differences(gcm_i,:,:)=(/diff/)
      end if
      delete(diff)
    else 
      if MONTHLY then 
        ensemble_differences(gcm_i,:,:,:)=(/read_diff_latlon_var(fila,filb,variable_name,PERCENTAGE)/)
      else
        ensemble_differences(gcm_i,:,:)=(/read_diff_latlon_var(fila,filb,variable_name,PERCENTAGE)/)
      end if
    end if
    delete([/fila,filb/])
  end do 

  ;write out to file  
  if fileexists(out_file_name) then
    system("rm "+out_file_name)
  end if
  setfileoption("nc", "Format",  "NetCDF4")
  outfil=addfile(out_file_name,"c")
  outfil->$variable_name$=ensemble_differences
  outfil->piControl_tracking_id=piControl_tracking_id
  outfil->tracking_id=tracking_id
  outfil->model_name=model_name
  outfil->resX=resX
  outfil->resY=resY
  outfil->piControl_url=piControl_url
  outfil->further_info_url=further_info_url
  outfil->piControl_years_averaged=piControl_years_averaged
  outfil->years_averaged=years_averaged
  delete(outfil)

  delete([/n_gcms,ensemble_differences,piControl_tracking_id,piControl_url,tracking_id,model_name,resX,resY,further_info_url/])
end;write_ensemble_difference_file

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
undef("write_ensemble_combined_file")
procedure write_ensemble_combined_file(out_file_name:string,input_file_paths:string,variable_name:string,MONTHLY:logical,PMIP4_not_PMIP3:logical)
local out_file_name,input_file_paths,variable_name,MONTHLY,PMIP4_not_PMIP3,n_gcms,tracking_id,model_name,resX,resY,further_info_url
begin
  n_gcms=dimsizes(input_file_paths)
  if dimsizes(n_gcms).ne.1 then
    print("write_ensemble_combined_file: expecting input_file_paths to only have 1 dimension (i.e. experiment) not two")
    exit
  end if
  tracking_id=new(n_gcms, string)
  tracking_id!0="model"
  model_name=new(n_gcms, string)
  model_name!0="model"
  resX=new(n_gcms, integer)
  resX!0="model"
  resY=new(n_gcms, integer)
  resY!0="model"
  years_averaged=new(n_gcms,string)
  years_averaged!0="model"
  further_info_url=new(n_gcms,string)
  further_info_url!0="model"
  if MONTHLY then
    ensemble_combined=new((/n_gcms,12,180,360/),float)
    ensemble_combined!0="model"
    ensemble_combined!1="month"
    ensemble_combined!2="lat"
    ensemble_combined!3="lon"
  else
    ensemble_combined=new((/n_gcms,180,360/),float)
    ensemble_combined!0="model"
    ensemble_combined!1="lat"
    ensemble_combined!2="lon"
  end if

  do gcm_i=0,n_gcms-1
    str_frags=str_split(input_file_paths(gcm_i),"/")
    f1=str_frags(4)
    f1_c=stringtocharacter(str_frags(4))
    years_averaged(gcm_i)=tostring(f1_c(str_index_of_substr(f1,".nc", -1)-13:str_index_of_substr(f1,".nc", -1)-1))
    delete([/str_frags,f1_c/])
    fil=addfile(input_file_paths(gcm_i),"r")
    tracking_id(gcm_i)=fil@tracking_id
    X=fil->lat
    resX(gcm_i)=dimsizes(X)
    Y=fil->lon
    resY(gcm_i)=dimsizes(Y)
    delete([/X,Y/])
    if PMIP4_not_PMIP3 then
      model_name(gcm_i)=fil@source_id
      further_info_url(gcm_i)=fil@further_info_url
    else
      model_name(gcm_i)=fil@model_id
    end if
    if gcm_i.eq.0 then
      this_field=read_latlon_var(input_file_paths(gcm_i),variable_name)
      ensemble_combined&lat=this_field&lat
      ensemble_combined&lon=this_field&lon
      if MONTHLY then 
        ensemble_combined(gcm_i,:,:,:)=(/this_field/)
      else
        ensemble_combined(gcm_i,:,:)=(/this_field/)
      end if
      delete(this_field)
    else 
      if MONTHLY then 
        ensemble_combined(gcm_i,:,:,:)=(/read_latlon_var(input_file_paths(gcm_i),variable_name)/)
      else
        ensemble_combined(gcm_i,:,:)=(/read_latlon_var(input_file_paths(gcm_i),variable_name)/)
      end if
    end if
    delete([/fil/])
  end do 

  ;write out to file  
  if fileexists(out_file_name) then
    system("rm "+out_file_name)
  end if
  setfileoption("nc", "Format",  "NetCDF4")
  outfil=addfile(out_file_name,"c")
  outfil->$variable_name$=ensemble_combined
  outfil->tracking_id=tracking_id
  outfil->model_name=model_name
  outfil->resX=resX
  outfil->resY=resY
  outfil->further_info_url=further_info_url
  outfil->years_averaged=years_averaged
  delete(outfil)

  delete([/n_gcms,ensemble_combined,tracking_id,model_name,resX,resY,further_info_url/])
end;write_ensemble_combined_file


;;;;;;;;;;;;;;;;;;;;;

DATA_DIR="/data/CMIP/curated_ESGF_replica"
monClim_DIR="../netcdfs/monClim"
annClim_DIR="../netcdfs/annClim"
OVERWRITE_EXISTING=False

; Start by creating climatologies on the native grids...
expt_names=(/"lgm","lig127k","midHolocene","midPliocene-eoi400"/)
var_names=(/"tas","pr"/)
PMIP4=(/True,False/)
PMIP_names=(/"PMIP4","PMIP3"/)

do expt_i = 0,dimsizes(expt_names)-1
  do PMIPgen = 0,1
    do var_i=0,dimsizes(var_names)-1
      ;Generate an output file name for annual means
      ensemble_file_name="../netcdfs/ensemble_differences/"+var_names(var_i)+"_annClim_"+PMIP_names(PMIPgen)+"_"+expt_names(expt_i)+"-piControl.nc"
      print("Creating "+ensemble_file_name)
      percentage_file_name="../netcdfs/ensemble_differences/"+var_names(var_i)+"_annClim_"+PMIP_names(PMIPgen)+"_"+expt_names(expt_i)+"-piControl_percentage.nc"
      combined_exp_file_name="../netcdfs/ensemble_combined/"+var_names(var_i)+"_annClim_"+PMIP_names(PMIPgen)+"_"+expt_names(expt_i)+".nc"
      combined_pi_file_name="../netcdfs/ensemble_combined/"+var_names(var_i)+"_annClim_"+PMIP_names(PMIPgen)+"_piControl_for_"+expt_names(expt_i)+".nc"
      ; identify relevant pairs of annual mean files
      file_paths=find_pair_files_wVar(annClim_DIR+"/"+PMIP_names(PMIPgen),expt_names(expt_i),"piControl",var_names(var_i),PMIP4(PMIPgen))
      file_paths@_FillValue="missing"
      if .not.all(ismissing(file_paths)) then
        if OVERWRITE_EXISTING.or.(.not.fileexists(ensemble_file_name)) then
          if fileexists(ensemble_file_name) then
            system("rm "+ensemble_file_name)
          end if
          write_ensemble_difference_file(ensemble_file_name,file_paths,var_names(var_i),False,PMIP4(PMIPgen),False)
        end if; create annClim_difference
        if OVERWRITE_EXISTING.or.(.not.fileexists(combined_exp_file_name)) then
          if fileexists(combined_exp_file_name) then
            system("rm "+combined_exp_file_name)
          end if
          write_ensemble_combined_file(combined_exp_file_name,file_paths(:,0),var_names(var_i),False,PMIP4(PMIPgen))
        end if; create annClim_expt file
        if OVERWRITE_EXISTING.or.(.not.fileexists(combined_pi_file_name)) then
          if fileexists(combined_pi_file_name) then
            system("rm "+combined_pi_file_name)
          end if
          write_ensemble_combined_file(combined_pi_file_name,file_paths(:,1),var_names(var_i),False,PMIP4(PMIPgen))
        end if; create annClim_piControl
        if var_names(var_i).eq."pr" then
          if OVERWRITE_EXISTING.or.(.not.fileexists(percentage_file_name)) then
            system("rm "+percentage_file_name)
          end if
          write_ensemble_difference_file(percentage_file_name,file_paths,var_names(var_i),False,PMIP4(PMIPgen),True)
        end if; create annClim_difference
      end if
      delete([/file_paths/])

      ;Generate an output file names for monthly climatologies
      ensemble_file_name="../netcdfs/ensemble_differences/"+var_names(var_i)+"_monClim_"+PMIP_names(PMIPgen)+"_"+expt_names(expt_i)+"-piControl.nc"
      percentage_file_name="../netcdfs/ensemble_differences/"+var_names(var_i)+"_monClim_"+PMIP_names(PMIPgen)+"_"+expt_names(expt_i)+"-piControl_percentage.nc"
      combined_exp_file_name="../netcdfs/ensemble_combined/"+var_names(var_i)+"_monClim_"+PMIP_names(PMIPgen)+"_"+expt_names(expt_i)+".nc"
      combined_pi_file_name="../netcdfs/ensemble_combined/"+var_names(var_i)+"_monClim_"+PMIP_names(PMIPgen)+"_piControl_for_"+expt_names(expt_i)+".nc"
      ; identify relevant pairs of monthly climatology files
      file_paths=find_pair_files_wVar(monClim_DIR+"/"+PMIP_names(PMIPgen),expt_names(expt_i),"piControl",var_names(var_i),PMIP4(PMIPgen))
      file_paths@_FillValue="missing"
      if .not.all(ismissing(file_paths)) then
        if OVERWRITE_EXISTING.or.(.not.fileexists(ensemble_file_name)) then
          if OVERWRITE_EXISTING.and.fileexists(ensemble_file_name) then
            system("rm "+ensemble_file_name)
          end if
          write_ensemble_difference_file(ensemble_file_name,file_paths,var_names(var_i),True,PMIP4(PMIPgen),False)
        end if
        if OVERWRITE_EXISTING.or.(.not.fileexists(combined_exp_file_name)) then
          if fileexists(combined_exp_file_name) then
            system("rm "+combined_exp_file_name)
          end if
          write_ensemble_combined_file(combined_exp_file_name,file_paths(:,0),var_names(var_i),True,PMIP4(PMIPgen))
        end if; create monClim_expt file
        if OVERWRITE_EXISTING.or.(.not.fileexists(combined_pi_file_name)) then
          if fileexists(combined_pi_file_name) then
            system("rm "+combined_pi_file_name)
          end if
          write_ensemble_combined_file(combined_pi_file_name,file_paths(:,1),var_names(var_i),True,PMIP4(PMIPgen))
        end if; create monClim_piControl
        if var_names(var_i).eq."pr" then
          if OVERWRITE_EXISTING.or.(.not.fileexists(percentage_file_name)) then
            if OVERWRITE_EXISTING.and.fileexists(percentage_file_name) then
              system("rm "+percentage_file_name)
            end if
            write_ensemble_difference_file(percentage_file_name,file_paths,var_names(var_i),True,PMIP4(PMIPgen),True)
          end if
        end if; create monClim_difference
      end if; all missing
      delete([/file_paths/])
    end do;var_names
  end do;PMIPgen
end do;expt_names
