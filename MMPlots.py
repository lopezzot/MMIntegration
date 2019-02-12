from datetime import datetime as dt
from datetime import timedelta as td
import sys
import os
import tools
from ROOT import TFile, TDatime, TDirectory, gSystem
import glob
import numpy as np
import search
import copy

house = raw_input("Data in BB5 or Gif? ")
folder = raw_input("Insert folder to study: ")

path = "/Users/lorenzo/Data"+str(house)+"/"+folder+"/HV/"
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
def createplot(file, filename):

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
	nospike_meancurrent = None
	meanvoltage = None
	notrips_meanvoltage = None
	
	if "i" in filename: #it's a current file
		#search.findrisingedges(valuesdeltas, dates)
		#search.findfallingedges(valuesdeltas, dates)
		
		sectorscurrent = filename[5:9]
		meancurrent = np.mean(newvalues)

		#remove spikes in current files
		copynewvalues = copy.copy(newvalues) #need to copy it to pass to function below
		nospike_newvalues = search.removespikes(valuesdeltas, copynewvalues)
		nospike_meancurrent = np.mean(nospike_newvalues) #used to have real baseline of the current
																										#or meancurrent
		spikecounter, filename, spikedates, spikeseconds, spikenames = search.findspikes_50na(newvalues, nospike_meancurrent, dates, newtimes, filename)
		#spikecounter, filename, spikedates, spikeseconds, spikenames = search.findspikes(valuesdeltas, dates, newtimes, filename) #old one
		
		if "D" in filename:
			sectorscurrent = None
			nospike_meancurrent = None

	if "v" in filename: #it's a voltage file
		sectorsvoltage = filename[5:9]
		meanvoltage = np.mean(newvalues)

		copynewvalues = copy.copy(newvalues)
		notrips_newvalues = search.removetrips(valuesdeltas, copynewvalues)
		notrips_meanvoltage = np.mean(notrips_newvalues)

		if "D" in filename:
			sectorsvoltage = None
			notrips_meanvoltage = None

	#tools.write_roothistogram(newvalues, filename, filename[0], "Entries", rootdirectory) #if want additional histograms
	tools.write_rootdategraph(rootdates, newvalues, filename, "time (s)", filename[0], rootdirectory)
	
	duration = len(newtimes) #total seconds from start to stop

	if "i" not in filename or "D" in filename:
		spikenames = None
		duration = None
		spikeseconds = None

	return spikenames, duration, sectorsvoltage, notrips_meanvoltage, sectorscurrent, nospike_meancurrent, spikeseconds
#----------------------------------------------------------------------------------------

for dat_file in glob.iglob(path+'*.dat'):
	print "Analyzing: "+dat_file[len(path):len(dat_file)]+" \n"
	spikeslayer, duration, sectorsvoltage, meanvoltage, sectorscurrent, meancurrent, spikeseconds = createplot(dat_file, dat_file[len(path):len(dat_file)-4])
	
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

#tools.write_roothistogram(newspikeseconds, "Spike time distribution", "t (s)", "Entries", dir_summary)
tools.write_rootgraph(range(len(meancurrents)),meancurrents,"i "+str(round(float(deltatime)/float(3600),2))+" hours","sector","i", sectorscurrents, dir_summary)
tools.write_rootgraph(range(len(meanvoltages)),meanvoltages,"HV "+str(round(float(deltatime)/float(3600),2))+" hours","sector","v",sectorsvoltages, dir_summary)
tools.write_spikeroothistogram(spikenames, "spikes", "spikes/min", dir_summary, deltatime)
