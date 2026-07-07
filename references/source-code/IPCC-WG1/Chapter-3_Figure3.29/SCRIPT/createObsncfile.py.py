import csv
import string
import cdms2, cdtime
import numpy

BASE_TIME_UNITS = 'days since 1850-1-1'

with open("../OBS/AR6_FGD_AssessmentTimeseriesThSL.csv", 'r') as f:
    ThSL = list(csv.reader(f, delimiter=";"))



tlist = []
ThSL_list = []
ThSL_1sigma_list = []

for i in range(2, len(ThSL)):
    #
    strList = string.split(ThSL[i][0], ',')
    #
    # First column is year
    #
    year = float(strList[0])
    ThSL_full_depth = float(strList[-2])
    ThSL_full_depth_1sigma = float(strList[-1])
    #
    #print year, ThSL_full_depth, ThSL_full_depth_1sigma
    #
    months = 12 * (year - int(year))
    #
    rel = cdtime.reltime(months, 'months since ' + str(int(year)) + '-1-1')
    #
    tval = rel.tocomp().torel(BASE_TIME_UNITS).value
    #
    tlist.append(tval)
    #
    ThSL_list.append(ThSL_full_depth)
    ThSL_1sigma_list.append(ThSL_full_depth_1sigma)
    #
# end of for i in range(2, len(ThSL)):

ThSL = numpy.array(ThSL_list)
ThSL_1sigma = numpy.array(ThSL_1sigma_list)
taxis = cdms2.createAxis(numpy.array(tlist))
taxis.designateTime()
taxis.units = BASE_TIME_UNITS

ThSL = cdms2.createVariable(ThSL, axes=[taxis], id='ThSL')
ThSL.units = 'mm'
ThSL.long_name = 'Changes in full-depth global thermal expansion (mm) relative to the 1971 average.'
ThSL.comment1 = 'Source: AR6 FGD assessment timeseries ThSL.csv from Matt Palmet'

ThSL_1sigma = cdms2.createVariable(ThSL_1sigma, axes=[taxis], id='ThSL_1sigma')
ThSL_1sigma.units = 'mm'
ThSL_1sigma.long_name = 'Full-depth Uncertainty (1-sigma)'
ThSL_1sigma.comment1 = 'Source: AR6 FGD assessment timeseries ThSL.csv from Mat Palmer'


fout = cdms2.open('../OBS/ThSL_Observed_AR6_FGD_Assessment_Timeseries.nc', 'w')
fout.write(ThSL)
fout.write(ThSL_1sigma)
fout.close()


