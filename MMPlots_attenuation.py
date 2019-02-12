from datetime import datetime as dt
from datetime import timedelta as td
import sys
import os
import tools
from ROOT import TFile, TDatime, TDirectory, gSystem
import glob
import numpy as np
import search

folder = raw_input("Insert folder to study: ")

path = "/Users/lorenzo/DataGif/"+folder+"/HV/"
gifpath = "/Users/lorenzo/DataGif/"+folder+"/GIF/"
giffile = gifpath+"gifData.dat"

rootfile = TFile("/Users/lorenzo/Desktop/MMresults/"+folder+".root","RECREATE")
dir_L1 = rootfile.mkdir("Layer1/")
dir_L2 = rootfile.mkdir("Layer2/")
dir_L3 = rootfile.mkdir("Layer3/")
dir_L4 = rootfile.mkdir("Layer4/")
dir_summary = rootfile.mkdir("Summary/")

directories = {"L1":dir_L1,"L2":dir_L2,"L3":dir_L3,"L4":dir_L4}

#for summary plots
spikenames = []
sectorscurrents = []
sectorsvoltages = []
meancurrents = []
meanvoltages = []
newspikeseconds = []
#----------------------------------------------------------------------------------------
def createplot(giffile, file, filename):

	layer = filename[5:7]
	rootdirectory = directories[layer] #to check

	times = [x.split(' 	 ')[0] for x in open(file,"r").readlines()]
	if len(times) == 1:
		print "Exception -----> Only one data in "+str(filename)+".dat \n"
		return None, None, None, None, None, None, None
	if not times:
		print "Exception -----> File empty: "+str(filename)+".dat \n"
		return None, None, None, None, None, None, None

	times = [x.replace(':',' ') for x in times]
	times = [x.replace('/',' ') for x in times]
	times = [x.replace('_',' ') for x in times]
	times = [dt.strptime(x, '%m %d %Y %H %M %S') for x in times]

	starttime = times[0]
	dates = [starttime]

	times = [int((x-starttime).total_seconds()) for x in times]

	values = [float(x.split(' 	 ')[1]) for x in open(file,"r").readlines()]

	newtimes = range(times[len(times)-1])
	newvalues = [None]*len(newtimes)

	for counter, value in enumerate(newvalues):
		if counter in times:
			newvalues[counter] = values[times.index(counter)]
		else:
			newvalues[counter] = newvalues[counter-1]

	for counter in range(len(newtimes)-1):
		dates.append(dates[counter]+td(seconds=1))

	rootdates = [TDatime(x.year, x.month, x.day, x.hour, x.minute, x.second) for x in dates]

	#Identify drops
	valuesdeltas = np.diff(newvalues)
	valuesdeltas = [0]+valuesdeltas

	sectorscurrent = None
	sectorsvoltage = None
	meancurrent = None
	nospike_meancurrent = None #to have current not affected by spikes
	meanvoltage = None
	
	if "i" in filename: #it's a current file
		search.findrisingedges(valuesdeltas, dates)
		search.findfallingedges(valuesdeltas, dates)
		spikecounter, filename, spikedates, spikeseconds, spikenames = search.findspikes(valuesdeltas, dates, newtimes, filename)

		sectorscurrent = filename[5:9]
		meancurrent = np.mean(newvalues)

		#remove spikes
		nospike_newvalues = search.removespikes(valuesdeltas, newvalues)
		nospike_meancurrent = np.mean(nospike_newvalues)

	if "v" in filename: #it's a voltage file
		sectorsvoltage = filename[5:9]
		meanvoltage = np.mean(newvalues)

	#data from gif file (for attenuation)------------------------
	atten = [x.split(' 	 ') for x in open(giffile,"r").readlines()[1:]] #read attenutation factor exept first line (header)
	atten = [x for x in atten if len(x) == 11]
	atten_times = [x[0] for x in atten]
	atten_values = [x[5] for x in atten]
	
	atten_times = [x.replace(':',' ') for x in atten_times]
	atten_times = [x.replace('/',' ') for x in atten_times]
	atten_times = [x.replace('_',' ') for x in atten_times]
	atten_times = [dt.strptime(x, '%d %m %Y %H %M %S') for x in atten_times]

	atten_starttime = atten_times[0] 
	atten_dates = [atten_starttime]

	atten_times = [int((x-atten_starttime).total_seconds()) for x in atten_times]
	
	atten_newtimes = range(atten_times[len(atten_times)-1])
	atten_newvalues = [None]*len(atten_newtimes)

	for atten_counter, atten_value in enumerate(atten_newvalues):
		if atten_counter in atten_times:
			atten_newvalues[atten_counter] = atten_values[atten_times.index(atten_counter)]
		else:
			atten_newvalues[atten_counter] = atten_newvalues[atten_counter-1]

	for counter in range(len(atten_newtimes)-1):
		atten_dates.append(atten_dates[counter]+td(seconds=1))

	#completed date array and attenuation array from GIF 
	#now important to match starting time with data from chamber
	#not done for drift
	if "i" in filename and "D" not in filename:
		
		syncindex = atten_dates.index(dates[10])
		dates = dates[10:]
		atten_dates = atten_dates[syncindex:]
		if len(atten_dates) > len(dates):
			atten_dates = atten_dates[0:len(dates)]
			atten_newvalues = atten_newvalues[0:len(newvalues)] #attenuation values sync to i values 
		elif len(atten_dates) < len(dates):
			dates = dates[0:len(atten_dates)]
			newvalues = newvalues[0:len(atten_newvalues)] #syn complete

		setattenvalues = set(atten_newvalues) 
		setattenvalues = [x for x in setattenvalues if float(x) != 0.]
		setmeancurrents = []

		for setattenuation in setattenvalues:
			found = [x for counter, x in enumerate(newvalues) if atten_newvalues[counter] == setattenuation]
			setmeancurrents.append(float(np.mean(found)))

		setattenvalues = [float(x)**(-1) for x in setattenvalues]
		tools.write_attenuationrootgraph(setattenvalues[2:], setmeancurrents[2:], filename+"_attenuation", "1/attenuation", "i", dir_summary)
	#end data from gif file--------------------------------------

	#write layer graphs
	#tools.write_roothistogram(newvalues, filename, filename[0], "Entries", rootdirectory) #if you want additional histograms
	tools.write_rootdategraph(rootdates, newvalues, filename, "time (s)", filename[0], rootdirectory)
	
	duration = len(newtimes) #total seconds from start to stop

	if "i" not in filename or "D" in filename:
		spikenames = None
		duration = None
		spikeseconds = None

	return spikenames, duration, sectorsvoltage, meanvoltage, sectorscurrent, nospike_meancurrent, spikeseconds
#----------------------------------------------------------------------------------------

for dat_file in glob.iglob(path+'*.dat'):
	print "Analyzing: "+dat_file[len(path):len(dat_file)]+" \n"
	spikeslayer, duration, sectorsvoltage, meanvoltage, sectorscurrent, meancurrent, spikeseconds = createplot(giffile, dat_file, dat_file[len(path):len(dat_file)-4])
	
	if spikeseconds != None:
		newspikeseconds = newspikeseconds + spikeseconds
	if spikeslayer != None:
		spikenames = spikenames + spikeslayer
	if duration != None:
		deltatime = duration
	if sectorscurrent != None:
		sectorscurrents.append(sectorscurrent)
	if meancurrent != None:
		meancurrents.append(meancurrent)
	if sectorsvoltage != None:
		sectorsvoltages.append(sectorsvoltage)
	if meanvoltage != None:
		meanvoltages.append(meanvoltage)

tools.write_roothistogram(newspikeseconds, "Spike time distribution", "t (s)", "Entries", dir_summary)
tools.write_rootgraph(range(len(meancurrents)),meancurrents,"i "+str(round(float(deltatime)/float(3600),2))+" hours","sector","i", sectorscurrents, dir_summary)
tools.write_rootgraph(range(len(meanvoltages)),meanvoltages,"HV "+str(round(float(deltatime)/float(3600),2))+" hours","sector","v",sectorsvoltages, dir_summary)
tools.write_spikeroothistogram(spikenames, "spikes", "spikes/min", dir_summary, deltatime)
