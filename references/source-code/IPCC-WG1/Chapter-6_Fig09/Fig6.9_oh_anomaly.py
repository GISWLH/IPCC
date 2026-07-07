# |-------------------------------------------------------------------------------|
# |  #-*- coding:utf-8 -*-
# |  __author__      = "Alcide Zhao"
# |	 __copyright__   = "Copyright 2021, The AerChemMIP Project"
# |  __maintainer__  = "Alcide Zhao"
# |	 __email__       = "alcide.zhao@reading.ac.uk"
# |	 __status__      = "Production"
# |	 __reference__   = "Stevenson et al. (2020): Trends in global tropospheric 
# |						hydroxyl radical and methane lifetime since 1850 from 
# |						AerChemMIP, Atmos. Chem. Phys.
# |						https://doi.org/10.5194/acp-20-12905-2020, 2020. "
# |	 
# |  This script produces the OH anomoly plots for IPCC AR6. 
# |	 It was written using Python2.7, but should also wotk with Python 3
# |	 Inputs:
# |    	All data are under the ./data folder
# |  Output:
# |    	The plot named 'OHAnomoly_1850-2014_IPCC_AR6.png' saved under working 
# |     directory
# |  Use:
# |     change to the working directory and execute 
# |			python oh_anomoly.py	
# |-------------------------------------------------------------------------------|


import numpy as np
import netCDF4 as nc4
import matplotlib.pyplot as plt
import csv,json 

plt.switch_backend('agg')

#######################      Reading data      ####################

def get_Montzka2011_oh():
	"""
	readout 1997-2007 monthly mean OH in percent relative to the 1998-2007 period
	process into annual mean
	"""
	def get_CSV_att(file,x, y):
		with open(file, 'rb') as csvfile:
			reader = csv.DictReader(csvfile)
			field_name = reader.fieldnames
			value=[];Time=[]
			for row in reader:
				Time.append(float(row[x]))
				value.append(float(row[y]))
		return Time,value
	
	file_path ='./data/Montzkaetal.2011.csv'
	Time,value = get_CSV_att(file=file_path,x='Time', y="OH")
	year= range(1997,2008)
	AnnualOH = np.empty((11))
	for iyear in year:
		AnnualOH[iyear-1997] = 100*np.nanmean(value[(iyear-1997)*12:(iyear-1997+1)*12])
	return year, AnnualOH

def get_Righlby_oh():
	"""
	readout 1980-2014 annual mean OH in percent relative to the 1998-2007 period
	"""
	def get_CSV_att(file,x, y1,y2):
		with open(file, 'rb') as csvfile:
			reader = csv.DictReader(csvfile)
			field_name = reader.fieldnames
			NOAA=[];Time=[];AGAGE=[];
			for row in reader:
				Time.append(float(row[x]))
				NOAA.append(float(row[y1]))
				AGAGE.append(float(row[y2]))
		NOAA=np.array(NOAA);NOAA[NOAA<-1000]=np.nan
		return Time,NOAA,AGAGE
	
	file_path ='./data/Rigby.2017.csv'
	Time,NOAA,AGAGE = get_CSV_att(file=file_path,x='years', y1="NOAA_50_percentile",y2="AGAGE_50_percentile")
	Time,NOAA_16,AGAGE_16 = get_CSV_att(file=file_path,x='years', y1="NOAA_16_percentile",y2="AGAGE_16_percentile")
	Time,NOAA_84,AGAGE_84 = get_CSV_att(file=file_path,x='years', y1="NOAA_84_percentile",y2="AGAGE_84_percentile")
	return Time,NOAA,AGAGE,NOAA_16,AGAGE_16,NOAA_84,AGAGE_84

def get_Turner_oh_2017():
	"""
	readout 1980-2015 annual mean OH in percent relative to the 1998-2007 period
	txt format
	"""
	file_name= './data/Turner.2017.txt'
	f=open(file_name,"r")
	comment=f.readline()
	comment=f.readline()
	lines=f.readlines()
	time=[];OH=[]
	for x in lines:
		time.append(round(float(x.split(',')[0])/100,0))
		OH.append(float(x.split(',')[4]))
	f.close()
	return time, OH

def get_Nicely_oh_2018():
	"""
	readout 1980-2015 annual mean OH in percent relative to the 1998-2007 period
	txt format
	"""
	file_name= './data/Nicely.2018.dat'
	f=open(file_name,"r")
	for i in range(5):
		comment=f.readline()
	lines=f.readlines()
	time=[];OH=[]
	for x in lines:
		time.append(float(x[0:4]))
		OH.append(float(x[-7:]))
	f.close()
	return time, OH

def get_naus_oh_2019():
	oh=np.array([-2.7674,-2.2955,-1.2479,-2.7231,-2.2045,0.3966,0.7375,1.1533,-0.3119,0.9276,1.6796,0.6734,-0.456,-1.625,-0.8399,-0.4611,0.1752,2.3085,3.764,2.8767,0.2397])
	return range(1994,2015),oh

def get_Patra_oh_2021():
	oh=np.array([-1.3105,-0.6539,-0.8650,-0.7590,0.8343,1.4527,1.2656,-0.6990,0.5380,0.5467,-0.0412,-1.4689,-1.6691,-0.7917,-1.7498,-0.2360,0.4298,2.3246,0.0298,0.2119,-0.2055])
	return range(1995,2016),oh

def get_UKESM_OH():
	"""
	UKESM 3-member simulaitons for 1850-201
	original units molec/cm3
	"""
	file_name= './data/UKESM1-0-ll_1850-2014.asc'
	f=open(file_name,"r")
	for i in range(2):
		comment=f.readline()
	lines=f.readlines()
	Time=[];OH1=[];OH2=[];OH3=[];
	for x in lines:
		Time.append(float(x.split()[0]))
		OH1.append(float(x.split()[1]))
		OH2.append(float(x.split()[2]))
		OH3.append(float(x.split()[3]))
	f.close()
	OH= np.empty((3,len(OH1)))
	OH1=np.array(OH1);OH2=np.array(OH2);OH3=np.array(OH3);
	OH[0,:]=100*(OH1-np.nanmean(OH1[146:156]))/np.nanmean(OH1[146:156])
	OH[1,:]=100*(OH2-np.nanmean(OH2[146:156]))/np.nanmean(OH2[146:156])
	OH[2,:]=100*(OH3-np.nanmean(OH3[146:156]))/np.nanmean(OH3[146:156])
	# plt.plot(OH[0,:]);plt.show()
	return Time,OH

def get_WACCM_OH():
	with open('./data/CESM2_WACCM_1850-2014.json') as json_file:
		annual_mean = np.array(json.load(json_file))
	return range(1850,2015),annual_mean

def get_GFDL_OH():
	file_name= './data/GFDL-ESM4_1850-2014.txt'
	f=open(file_name,"r")
	for i in range(2):
		comment=f.readline()
	lines=f.readlines()
	Time=[];OH=[]
	for x in lines:
		Time.append(round(float(x.split(',')[0]),0))
		OH.append(float(x.split(',')[1]))
	f.close()
	OH=100*(OH-np.nanmean(OH[147:157]))/np.nanmean(OH[147:157])
	# plt.plot(OH);plt.show()
	return Time,OH


#######################      Plot data for IPCC      ####################

def main():
	# Read model data
	Time_WACCM,OH_WACCM= get_WACCM_OH()
	Time_UKESM,OH_UKESM=get_UKESM_OH()
	Time_GFDL,OH_GFDL=get_GFDL_OH()
	# Read obs/retrievals
	time_turner, OH_turne=get_Turner_oh_2017()	
	Time_Montzka, OH_Montzka = get_Montzka2011_oh()
	Time_Nicely, OH_Nicely = get_Nicely_oh_2018()
	time_naus,oh_naus = get_naus_oh_2019();
	time_Patra,oh_Patra = get_Patra_oh_2021();
	Time_Righlby, NOAA_Righlbyy,AGAGE_Righlby,NOAA_16,AGAGE_16,NOAA_84,AGAGE_84 = get_Righlby_oh()	
	# Fill NOAA_Righlbyy with AGAGE_Righlby for the first 16 years where there is no data, this is 
	# for later averaging out NOAA and the AGAGE data
	NOAA_Righlbyy[0:16]=AGAGE_Righlby[0:16];NOAA_16[0:16]=AGAGE_16[0:16];NOAA_84[0:16]=AGAGE_84[0:16]; 

	fig = plt.figure(facecolor='White',figsize=[22/2.54,18/2.54]);pad= 5;
	ax = plt.subplot2grid((2, 4), (0, 0),colspan=4); ax.grid(True,ls=':')
	# add plot title, sub-title and axes labels
	ax.annotate('Time evolution of global annual mean tropospheric OH anomaly',xy=(.5,1.05), 
		xytext=(0, pad),xycoords='axes fraction', textcoords='offset points',
		ha='center', va='baseline',rotation='horizontal',fontsize=11,fontname="Arial")
	ax.annotate('a) 1850-2014',xy=(.01,.03), xytext=(0, pad),
		xycoords='axes fraction', textcoords='offset points',
		ha='left', va='baseline',rotation='horizontal',fontsize=11,fontname="Arial")	
	ax.annotate('% OH anomaly with respect to mean 1998-2007',xy=(-0.07,-0.1), xytext=(0, pad),
		xycoords='axes fraction', textcoords='offset points',
	 	ha='center', va='center',rotation='vertical',fontsize=11,fontname="Arial")       
	ax.set_xlim([1850,2014]);ax.set_xticks(range(1850,2015,10));
	ax.set_xticklabels(range(1850,2015,10),fontsize=11,fontname="Arial")
	ax.set_ylim([-16,16]);ax.set_yticks(range(-16,17,4));ax.set_yticklabels(range(-16,17,4),
		fontsize=11,fontname="Arial")
	
	# draw the zoon in arrow
	ax.annotate('', xy=[0.30,0.46], xytext=[1980,-16], xycoords='figure fraction', 
		textcoords='data', arrowprops=dict(arrowstyle= '->, head_width=.3,head_length=.8',color='k'))
	ax.annotate('', xy=[0.97,0.45], xytext=[2014,-16], xycoords='figure fraction', 
		textcoords='data', arrowprops=dict(arrowstyle= '-> ,head_width=.3,head_length=.8',color='k'))
	# draw model data
	ax.plot(Time_GFDL,OH_GFDL,color='b',lw=2,label='GFDL-ESM4')
	ax.plot(Time_WACCM,np.nanmean(OH_WACCM,axis=0),color='r',lw=2,label='CESM2-WACCM')
	ax.fill_between(Time_WACCM, y1 =np.nanmin(OH_WACCM,axis=0), y2=np.nanmax(OH_WACCM,axis=0),
		color='r',lw=0,alpha=0.3)
	ax.plot(Time_UKESM,np.nanmean(OH_UKESM,axis=0),color='g',lw=2,label='UKESM1-0-LL')
	ax.fill_between(Time_UKESM, y1 =np.nanmin(OH_UKESM,axis=0), y2=np.nanmax(OH_UKESM,axis=0),
		color='g',lw=0,alpha=0.3)	
	## Multimodel mean
	MULTIMODEL = np.empty((7,165)); MULTIMODEL[:]=np.nan; MULTIMODEL[0,:]=OH_GFDL;
	MULTIMODEL[1:4,0:164]=OH_UKESM;MULTIMODEL[4:7,:]=OH_WACCM;
	MMM= np.nanmean(MULTIMODEL,axis=0);
	ax.plot(range(1850,2015),MMM,color='k',lw=4,label='Multi-model mean')
	# add legends
	legend = ax.legend(shadow=False,ncol=4,loc ='upper left',handlelength=0,columnspacing=1.5,
		labelspacing=1.2,prop={'family':"Arial","size":11})	
	legend.get_frame().set_facecolor('none');legend.get_frame().set_edgecolor('none');
	legend.get_frame().set_alpha(1)
	for line, text in zip(legend.get_lines(), legend.get_texts()):
		text.set_color(line.get_color())	
	# The zoomed-in plot to compare between multi-model mean and retrievals
	ax2 = plt.subplot2grid((2, 4), (1, 1),colspan=3); ax2.grid(True,ls=':')
	ax2.annotate('b) 1980-2014',xy=(.01,.03), xytext=(0, pad),
		xycoords='axes fraction', textcoords='offset points',
		ha='left', va='baseline',rotation='horizontal',fontsize=11,fontname="Arial")
	ax2.set_xlim(1980, 2014);ax2.set_xticks(range(1980,2014,5));
	ax2.set_xticklabels(range(1980,2014,5),fontsize=11,fontname="Arial")
	ax2.set_ylim([-16,16]);ax2.set_yticks(range(-16,17,4));
	ax2.set_yticklabels(range(-16,17,4),fontsize=11,fontname="Arial")
	# plot retrievals and MMM
	ax2.fill_between(Time_Righlby, y1 =(AGAGE_16+NOAA_16)/2, y2=(AGAGE_84+NOAA_84)/2,
		color='orange',lw=0,alpha=0.4)
	ax2.plot(Time_Righlby,(NOAA_Righlbyy+AGAGE_Righlby)/2,color='orange',lw=2, label='Rigby (2017)')
	ax2.plot(Time_Montzka,OH_Montzka,color='m',lw=2,label='Montzka (2011)')
	ax2.plot(time_turner,OH_turne,color='cyan',lw=2,label='Turner (2017)')
	ax2.plot(Time_Nicely,OH_Nicely,color='lime',lw=2,label='Nicely (2018)')
	ax2.plot(time_naus,oh_naus,color='grey',lw=2, label='Naus (2019)')
	ax2.plot(time_Patra,oh_Patra,color='deepskyblue',lw=2, label='Patra (2021)')
	ax2.plot(range(1850,2015),MMM,color='k',lw=4)

	legend = ax2.legend(shadow=False,ncol=1,loc='center left',handlelength=0,columnspacing=1.3,
		labelspacing=1.5,prop={'family':"Arial","size":11},bbox_to_anchor=(-0.4, 0., 0.3, 1))	
	legend.get_frame().set_facecolor('none');legend.get_frame().set_edgecolor('none');
	legend.get_frame().set_alpha(1)
	for line, text in zip(legend.get_lines(), legend.get_texts()):
		text.set_color(line.get_color())

	plt.subplots_adjust(left=0.08, bottom=0.05, right=0.97, top=0.93, wspace=0.1, hspace=0.2);
	plt.savefig('OHAnomoly_1850-2014_IPCC_AR6.png', format='png', dpi=1000)
	return True

if __name__ == "__main__":
    main()
