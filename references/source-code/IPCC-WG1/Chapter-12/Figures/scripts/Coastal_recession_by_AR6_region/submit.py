# -- Submit jobs
import os

jobscript = '/home/jservon/Chapter12_IPCC/scripts/Coastal_recession_by_AR6_region/job_CR_AR6_regions.sh'
for scenario in ['RCP45']:
    for horizon in ['2100','2050']:
        cmd = 'qsub -q h12 -v scenario='+scenario+',horizon='+horizon+' -j eo '+jobscript
        print cmd
        os.system(cmd)
