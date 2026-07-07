# Code-only export from IPCC-WG1 notebook.
# Source: Chapter-12/Figures/data/Figure_S12.3/.ipynb_checkpoints/Rewrite_metadata_files-checkpoint.ipynb

# %% cell 2
import csv


metadata_input_filename = 'CMIP5_pr.csv'

output_metadata_filename = 'CMIP5_day_pr_md.csv'

rows = []
with open(metadata_input_filename) as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        #newrow = row[0].split(',')[1:]
        #.replace('"','')
        #finalrow = newrow.split(',')[1:]
        newrow = row[1:4]+['day']+row[5:]
        finalrow = []
        for elt in newrow:
            finalrow.append(elt.replace('"',''))
        print finalrow
        rows.append(finalrow)
        #rows.append(finalrow)
        #if 'DATA_REF_SYNTAX' in newrow:
        #    finalrow.append('panels')
        #    rows.append(finalrow)

# %% cell 3
with open(output_metadata_filename, 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for row in rows:
        spamwriter.writerow(row)

# %% cell 5
import csv


metadata_input_filename = 'SPI6_md_CMIP6.csv'

output_metadata_filename = 'CMIP6_day_pr_md.csv'

rows = []
with open(metadata_input_filename) as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        #newrow = row[0].split(',')[1:]
        #.replace('"','')
        #finalrow = newrow.split(',')[1:]
        newrow = row[1:4]+['day']+row[5:]
        finalrow = []
        for elt in newrow:
            finalrow.append(elt.replace('"',''))
        print finalrow
        rows.append(finalrow)

# %% cell 6
with open(output_metadata_filename, 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for row in rows:
        spamwriter.writerow(row)

# %% cell 8
AR6regions_by_CORDEX_domain = dict(
    AUS = ['NAU','CAU','EAU','SAU','NZ'],
    SEA = ['SEA'],
    WAS = ['ARP','SAS','WCA'],#,'TIB'],
    EAS = ['TIB','ECA','EAS'],#'SAS'
    CAM = ['NSA','SCA','CAR'],
    SAM = ['NWS','NSA','SAM','NES','SWS','SES','SSA'],
    NAM = ['NWN','NEN','WNA','CNA','ENA','NCA'],#,'GAP'],
    #EUR = ['MED','WCE','NEU'],
    AFR = ['WAF','SAH','CAF','WSAF','ESAF','MDG','SEAF','NEAF','ARP']
)


for CORDEX_domain in AR6regions_by_CORDEX_domain:
    metadata_input_filename = 'CORDEX-'+CORDEX_domain+'_spi6.csv'
    output_metadata_filename = 'CORDEX-'+CORDEX_domain+'_day_pr_md.csv'

    rows = []
    with open(metadata_input_filename) as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            newrow = row[1:]
            #.replace('"','')
            #finalrow = newrow.split(',')[1:]
            finalrow = []
            for elt in newrow:
                finalrow.append(elt.replace('"',''))
            if 'DATA_REF_SYNTAX' in finalrow:
                finalrow.append('PANELS')
            else:
                finalrow = finalrow + AR6regions_by_CORDEX_domain[CORDEX_domain]
            print finalrow
            rows.append(finalrow)
            
    with open(output_metadata_filename, 'w') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in rows:
            spamwriter.writerow(row)

# %% cell 10
metadata_input_filename = 'CORDEX-EUR11_day_pr_md.txt'
output_metadata_filename = 'CORDEX-EUR_day_pr_md.csv'

rows = []
test = open(metadata_input_filename,'r')
for wline in test.readlines():
    tmp = wline.replace(' ','').replace('\n','').replace('.',';').split(';')
    if 'DATA_REF_SYNTAX' in tmp:
        tmp.append('PANELS')
        ttmp = tmp
    else:
        ttmp = ['.'.join(tmp[0:7])] + tmp[8:] + ['NEU','WCE','MED']
    rows.append( ttmp )
rows

# %% cell 11
with open(output_metadata_filename, 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for row in rows:
        spamwriter.writerow(row)
