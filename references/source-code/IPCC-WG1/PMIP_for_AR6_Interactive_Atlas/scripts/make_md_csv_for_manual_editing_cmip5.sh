#!/bin/bash


ls /data/CMIP/*/o*/*/*/*/mon/atmos/Amon/r*/v*/pr_Amon_* > ../metadata_files/lspr_cmip5.csv
sed -i 's:/data/CMIP/::g' ../metadata_files/lspr_cmip5.csv
sed -i 's:/mon/atmos/Amon/:,mon,atmos,Amon,:g' ../metadata_files/lspr_cmip5.csv
sed -i 's:/v:,v:g' ../metadata_files/lspr_cmip5.csv
sed -i 's:_Amon:,:g' ../metadata_files/lspr_cmip5.csv
sed -i 's:/pr:,pr:g' ../metadata_files/lspr_cmip5.csv
sed -i 's:/tas:,tas:g' ../metadata_files/lspr_cmip5.csv
sed -i 's:/:.:g' ../metadata_files/lspr_cmip5.csv


ls /data/CMIP/*/o*/*/*/*/mon/atmos/Amon/r*/v*/tas_Amon_* > ../metadata_files/lstas_cmip5.csv
sed -i 's:/data/CMIP/::g' ../metadata_files/lstas_cmip5.csv
sed -i 's:/mon/atmos/Amon/:,mon,atmos,Amon,:g' ../metadata_files/lstas_cmip5.csv
sed -i 's:/v:,v:g' ../metadata_files/lstas_cmip5.csv
sed -i 's:_Amon:,:g' ../metadata_files/lstas_cmip5.csv
sed -i 's:/pr:,pr:g' ../metadata_files/lstas_cmip5.csv
sed -i 's:/tas:,tas:g' ../metadata_files/lstas_cmip5.csv
sed -i 's:/:.:g' ../metadata_files/lstas_cmip5.csv
