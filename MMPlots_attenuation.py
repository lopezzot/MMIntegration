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
from fpdf import FPDF
from pylatex import Document, Figure


#----------------------------------------------------------------------------
def createsummaryplot_attenuation():
	house = raw_input("Data in Gif? ")
	folder = raw_input("Insert folder to study: ")

	ID = folder[0:18]
	timeslot = folder[19:len(folder)]

	path = "/Users/lorenzo/Data"+str(house)+"/"+folder+"/HV/"
	gifpath = "/Users/lorenzo/Data"+str(house)+"/"+folder+"/GIF/"
	giffile = gifpath+"EffectiveAttenuation.dat"
	
	global sourcefile
	sourcefile = gifpath+"Source.dat"

	rootfile = TFile("/Users/lorenzo/Desktop/MMresults/"+folder+".root","RECREATE")
	dir_L1 = rootfile.mkdir("Layer1/")
	dir_L2 = rootfile.mkdir("Layer2/")
	dir_L3 = rootfile.mkdir("Layer3/")
	dir_L4 = rootfile.mkdir("Layer4/")

	global dir_summary
	dir_summary = rootfile.mkdir("Summary/")

	global directories
	directories = {"L1":dir_L1,"L2":dir_L2,"L3":dir_L3,"L4":dir_L4}

	#for summary plots
	spikenames = []
	sectorscurrents = []
	sectorsvoltages = []
	meancurrents = []
	meanvoltages = []
	newspikeseconds = []

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

	vectorspikes = [x[5:len(x)] for x in spikenames]
	spikerate = []
	spikelayers = list(set(vectorspikes))
	for i in spikelayers:
		spikerate.append(vectorspikes.count(i))

	for sector in sectorsvoltages:
		if sector not in spikelayers:
			spikelayers.append(sector)
			spikerate.append(0)

	orderedspikerate = []
	for sector in sectorsvoltages:
		orderedspikerate.append(spikerate[spikelayers.index(sector)])

	orderedspikerate = [float(x/float((deltatime/60.))) for x in orderedspikerate]

	return sectorsvoltages, meanvoltages, orderedspikerate, ID, timeslot, deltatime
#----------------------------------------------------------------------------------------

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
	notrips_meanvoltage = None
	
	if "i" in filename: #it's a current file
		#search.findrisingedges(valuesdeltas, dates)
		#search.findfallingedges(valuesdeltas, dates)
		
		sectorscurrent = filename[5:9]
		meancurrent = np.mean(newvalues)
		
		#remove spikes in current files
		copynewvalues = copy.copy(newvalues) #need to copy it to pass to function below
		nospike_newvalues = search.removespikes_atgif(valuesdeltas, copynewvalues)
		nospike_newvalues = search.removespikes_atgif(np.diff(nospike_newvalues), nospike_newvalues) #two times to actually remove spikes
		nospike_newvalues = search.removespikes_atgif(np.diff(nospike_newvalues), nospike_newvalues) #two times to actually remove spikes
		nospike_meancurrent = np.mean(nospike_newvalues) #used to have real baseline of the current
		
		#TO BE CHECKED WICH ONE WE WANT
		#spikecounter, filename, spikedates, spikeseconds, spikenames = search.findspikes_50na(newvalues, nospike_meancurrent, dates, newtimes, filename)
		#spikecounter, filename, spikedates, spikeseconds, spikenames = search.findspikes(valuesdeltas, dates, newtimes, filename)

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

	#write layer graphs
	#tools.write_roothistogram(newvalues, filename, filename[0], "Entries", rootdirectory) #if you want additional histograms
	tools.write_rootdategraph_fromgif(rootdates, newvalues, filename, "time (s)", filename[0], rootdirectory)	

	duration = len(newtimes) #total seconds from start to stop

	if "i" not in filename or "D" in filename:
		spikenames = None
		duration = None
		spikeseconds = None

	#data from gif file (for attenuation)------------------------
	atten = [x.split(' 	 ') for x in open(giffile,"r").readlines()[1:]] #read attenutation factor exept first line (header)
	#atten = [x for x in atten if len(x) == 11] #used before change in daq
	atten_times = [x[0] for x in atten]
	atten_values = [float(x[1]) for x in atten]

	atten_times = [x.replace(':',' ') for x in atten_times]
	atten_times = [x.replace('/',' ') for x in atten_times]
	atten_times = [x.replace('_',' ') for x in atten_times]
	atten_times = [dt.strptime(x, '%m %d %Y %H %M %S') for x in atten_times]

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
		atten_dates.append(atten_dates[counter]+td(seconds=1)) #end of creating arrays atten values and times
	
	source = [x.split(' 	 ') for x in open(sourcefile,"r").readlines()[1:]] #read attenutation factor exept first line (header)
	#atten = [x for x in atten if len(x) == 11] #used before change in daq
	source_times = [x[0] for x in source]
	source_values = [float(x[1]) for x in source] #0.0 off 1.0 on
	
	source_times = [x.replace(':',' ') for x in source_times]
	source_times = [x.replace('/',' ') for x in source_times]
	source_times = [x.replace('_',' ') for x in source_times]
	source_times = [dt.strptime(x, '%m %d %Y %H %M %S') for x in source_times]

	source_starttime = source_times[0] 
	source_dates = [source_starttime]

	source_times = [int((x-source_starttime).total_seconds()) for x in source_times]
	
	source_newtimes = range(source_times[len(source_times)-1])
	source_newvalues = [None]*len(source_newtimes)

	for source_counter, source_value in enumerate(source_newvalues):
		if source_counter in source_times:
			source_newvalues[source_counter] = source_values[source_times.index(source_counter)]
		else:
			source_newvalues[source_counter] = source_newvalues[source_counter-1]

	for counter in range(len(source_newtimes)-1):
		source_dates.append(source_dates[counter]+td(seconds=1)) #end of creating arrays source values and times
	
	#now important to match starting time of source file and atten file
	if "i" in filename and "D" not in filename:
		
		if source_dates[10] in atten_dates:
			syncindex = atten_dates.index(source_dates[10])
			source_dates = source_dates[10:]
		else:
			syncindex = atten_dates.index(source_dates[50])
			source_dates = source_dates[50:]
		atten_dates = atten_dates[syncindex:]
		if len(atten_dates) > len(source_dates):
			atten_dates = atten_dates[0:len(source_dates)]
			atten_newvalues = atten_newvalues[0:len(source_newvalues)] #attenuation values sync to i values 
		elif len(atten_dates) < len(source_dates):
			source_dates = source_dates[0:len(atten_dates)]
			source_newvalues = source_newvalues[0:len(atten_newvalues)] #syn complete

		#for counter in range(0,50):
		#	print source_dates[counter],source_newvalues[counter],atten_dates[counter],atten_newvalues[counter]

	for counter, atten_newvalue in enumerate(atten_newvalues):
		if source_newvalues[counter] == 0.0:
			atten_newvalues[counter] = 0.0 #put attenuation to 0 il source is of, i will later remove zeros

	#completed date array and attenuation array from GIF 
	#now important to match starting time with data from chamber
	#not done for drift
	
	if "i" in filename and "D" not in filename:
		
		if dates[10] in atten_dates:
			syncindex = atten_dates.index(dates[10])
			dates = dates[10:]
		else:
			syncindex = atten_dates.index(dates[100]) #mettere 100 e provare!
			dates = dates[100:]
		atten_dates = atten_dates[syncindex:]
		if len(atten_dates) > len(dates):
			atten_dates = atten_dates[0:len(dates)]
			atten_newvalues = atten_newvalues[0:len(newvalues)] #attenuation values sync to i values 
		elif len(atten_dates) < len(dates):
			dates = dates[0:len(atten_dates)]
			newvalues = newvalues[0:len(atten_newvalues)] #syn complete!

		#if want to check sync
		#for counter in range(0,50):
			#print dates[counter],newvalues[counter],atten_dates[counter],atten_newvalues[counter]
	
		setattenvalues = set(atten_newvalues) 
		setattenvalues = [x for x in setattenvalues if float(x) != 0.] #remove 0
		setattenvalues.sort(reverse=True) #from min to max
		setmeancurrents = []

		#print len(newvalues), len(atten_newvalues)
		currentatzero = [x for counter, x in enumerate(newvalues[0:len(atten_newvalues)]) if atten_newvalues[counter] == 0.] #current when source is off  
		currentatzero = np.mean(currentatzero)

		for setattenuation in setattenvalues: #using nospike_newvalues here to not count spikes
			startindex = atten_newvalues.index(setattenuation)
			lastindex = len(atten_newvalues)-atten_newvalues[::-1].index(setattenuation)-1
			found = [x for x in nospike_newvalues[startindex+60*3:startindex+60*3+180]] 
			setmeancurrents.append(float(np.mean(found)))
			#this way gave problem as underestimates the current values
			#found = [x for counter, x in enumerate(nospike_newvalues[0:len(atten_newvalues)]) if atten_newvalues[counter] == setattenuation]
			#setmeancurrents.append(float(np.mean(found)))

		for counter in range(len(setmeancurrents)):
			setmeancurrents[counter] = setmeancurrents[counter] #- currentatzero #remove offset

		for counter, setattenvalue in enumerate(setattenvalues):
			print setattenvalue, setmeancurrents[counter]
		
		setattenvalues = [float(x)**(-1) for x in setattenvalues]
		tools.write_attenuationrootgraph(setattenvalues, setmeancurrents, filename, "1/attenuation", "i", dir_summary)

		#now write graphs current and voltages + find spikes
		if "i" in filename: #it's a current file
		
			#find spikes -> new part to find threshold over plateu at fiven attenuation filter without spikes
			spikecounter, filename, spikedates, spikeseconds, spikenames = search.findspikes_atgif(newvalues, atten_newvalues, setmeancurrents, setattenvalues, dates, newtimes, filename)

			if "D" in filename:
				sectorscurrent = None
				nospike_meancurrent = None

	#end data from gif file--------------------------------------
	
	return spikenames, duration, sectorsvoltage, notrips_meanvoltage, sectorscurrent, nospike_meancurrent, spikeseconds
#----------------------------------------------------------------------------------------
#createsummaryplots_attenuation()

	