#!/bin/bash

# -- Job script to run Compute_averages_AR6_regions_Coastal_recession.py
# -- Jerome Servonnat: jerome.servonnat at lsce.ipsl.fr
set +x

date

python /home/jservon/Chapter12_IPCC/scripts/Coastal_recession_by_AR6_region/Compute_averages_AR6_regions_Coastal_recession.py ${scenario} ${horizon}
