from datetime import datetime as dt
from datetime import timedelta as td
import sys
import os
import tools
from ROOT import TFile, TDatime, TDirectory, gSystem, TTree
import glob
import numpy as np
import search
import copy
import classes
from fpdf import FPDF
from pylatex import Document, Figure
from array import array

#----------------------------------------------------------------------------
def createsummaryplot_attenuation():
	'''function to collect info from GIF file'''

	house = raw_input("Data in Gif? ") #insert BB5 of GIF file path
	global folder
	folder = raw_input("Insert folder to study: ") #insert folder with bartch ID

	chambertype = folder[0:3]
	defaultlayersSM1 = ["L1L1","L1R1","L1L2","L1R2","L1L3","L1R3","L1L4","L1R4","L1L5","L1R5","L2L1","L2R1","L2L2","L2R2","L2L3","L2R3","L2L4","L2R4","L2L5","L2R5","L3L1","L3R1","L3L2","L3R2","L3L3","L3R3","L3L4","L3R4","L3L5","L3R5","L4L1","L4R1","L4L2","L4R2","L4L3","L4R3","L4L4","L4R4","L4L5","L4R5"]
	defaultlayersSM2 = ["L1L6","L1R6","L1L7","L1R7","L1L8","L1R8","L2L6","L2R6","L2L7","L2R7","L2L8","L2R8","L3L6","L3R6","L3L7","L3R7","L3L8","L3R8","L4L6","L4R6","L4L7","L4R7","L4L8","L4R8"]

	if chambertype == "SM1":
		defaultlayers = defaultlayersSM1
	if chambertype == "SM2":
		defaultlayers = defaultlayersSM2
	if chambertype == "LM1":
		defaultlayers = defaultlayersSM1
	if chambertype == "LM2":
		defaultlayers = defaultlayersSM2
		
	ID = folder[0:18] #batch ID
	timeslot = folder[19:len(folder)] #time slot from folder name

	path = "/Users/lorenzo/Data"+str(house)+"/"+folder+"/HV/"
	gifpath = "/Users/lorenzo/Data"+str(house)+"/"+folder+"/GIF/"
	giffile = gifpath+"EffectiveAttenuation.dat" 
	
	global sourcefile
	sourcefile = gifpath+"Source.dat"

	rootfile = TFile(folder+".root","RECREATE")
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
	graphs_atten = []
	graphs_linearity = []

	for dat_file in glob.iglob(path+'*.dat'):
		print "Analyzing: "+dat_file[len(path):len(dat_file)]+" \n" #print file under analysis
		filename = dat_file[len(path):len(dat_file)-4]
		graph_atten, graph_linearity, spikeslayer, spikeduration, duration, sectorsvoltage, meanvoltage, sectorscurrent, meancurrent, spikeseconds = createplot(giffile, dat_file, dat_file[len(path):len(dat_file)-4])
		
		if spikeseconds != None:
			newspikeseconds = newspikeseconds + spikeseconds
		if spikeslayer != None:
			spikenames = spikenames + spikeslayer
		if duration != None:
			deltatime = duration
		if spikeduration != None:
			spikesduration = spikeduration
		if sectorscurrent != None:
			sectorscurrents.append(sectorscurrent)
		if meancurrent != None:
			meancurrents.append(meancurrent)
		if sectorsvoltage != None:
			sectorsvoltages.append(sectorsvoltage)
		if meanvoltage != None:
			meanvoltages.append(meanvoltage)
		if graph_atten != None:
			graphs_atten.append(graph_atten)
		if graph_linearity != None:
			graphs_linearity.append(graph_linearity)

	#create summary plots 
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

	orderedspikerate = [float(x/float((spikesduration/60.))) for x in orderedspikerate]

	orderedsectorsvoltages = []
	orderedsmeanvoltages = []
	ordered_orderedspikerate = []
	ordered_graphsatten = []
	ordered_graphslinearity = []

	for layer in defaultlayers:
		index = sectorsvoltages.index(layer)
		orderedsectorsvoltages.append(sectorsvoltages[index])
		orderedsmeanvoltages.append(meanvoltages[index])
		ordered_orderedspikerate.append(orderedspikerate[index])
	
	graph_atten_names = []
	for graph in graphs_atten:
		graph_atten_names.append(graph.name)
	for layer in defaultlayers:
		index = graph_atten_names.index(layer)
		ordered_graphsatten.append(graphs_atten[index])

	graph_linearity_names = []
	for graph in graphs_linearity:
		graph_linearity_names.append(graph.name)
	for layer in defaultlayers:
		index = graph_linearity_names.index(layer)
		ordered_graphslinearity.append(graphs_linearity[index])

	for counter, graph in enumerate(ordered_graphsatten):	                                                           #+" "+str(int(orderedsmeanvoltages[counter]))# 
		tools.write_rootdategraph_plusatten(graph.new_rootdates, graph.newvalues, graph.atten_newvalues, graph.filename+" "+str(int(orderedsmeanvoltages[counter])), "time (s)", filename[0], dir_summary) #plot graph current + source 
	
	for counter, graph in enumerate(ordered_graphslinearity):
		print graph.name	                                              #+" "+str(int(orderedsmeanvoltages[counter]))#
		tools.write_attenuationrootgraph(graph.setattenvalues, graph.normalizedsetmeancurrents, graph.filename+" "+str(int(orderedsmeanvoltages[counter])), "1/attenuation", "i", dir_summary)

	return orderedsectorsvoltages, orderedsmeanvoltages, ordered_orderedspikerate, ID, timeslot, deltatime
#----------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------
def createplot(giffile, file, filename):
	'''create graph of current of voltage, find spikes and linearity plots from GIF'''
	if "D" in filename:
		return None, None, None, None, None, None, None, None, None, None
	layer = filename[5:7] #get layer       
	rootdirectory = directories[layer] #set root file directory

	sectorforarea = filename[8:9]
	chambertype = folder[0:3] #SM1 or SM2 LM1 or LM2
	
	areasSM1 = {"1":(30.0+52.)*(45.2/4.), "2":(52.+70.2)*(43.5/4.), "3":(43.5+75.6)*(43.5/4.), "4":(75.6+104.)*(43.5/4.), "5":(104.+114.9)*(43.5/4.)}
	areasSM2 = {"6":(166.4+150.5)*(135./6.), "7":(150.5+130.3)*(135./6.), "8":(130.3+117.1)*(135./6.)}

	if chambertype == "SM1":
		areas=areasSM1
	elif chambertype == "SM2":
		areas=areasSM2
	elif chambertype == "LM1":
		areas=areasSM1
	elif chambertype == "LM2":
		areas=areasSM2
	else:
		print "areas not found"
	area = areas[sectorforarea]
	
	times = [x.split(' 	 ')[0] for x in open(file,"r").readlines()]
	if len(times) == 1:        
		print "Exception -----> Only one data in "+str(filename)+".dat \n" #handle exception of empty files (should not be the case after daq fixing)
		return None, None, None, None, None, None, None, None, None
	if not times:
		print "Exception -----> File empty: "+str(filename)+".dat \n"
		return None, None, None, None, None, None, None, None, None

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
	#end of creating vectors for times, dates, values (current or voltage)

	sectorscurrent = None #default values
	sectorsvoltage = None
	meancurrent = None
	nospike_meancurrent = None #to have current not affected by spikes
	meanvoltage = None
	notrips_meanvoltage = None

	duration = len(newtimes) #total seconds from start to stop

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
			atten_newvalues[counter] = 0.0  #put attenuation to 0 il source is off, i will later remove zeros

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

		#if want to check sync, first 50 seconds
		#for counter in range(0,50):
		#	print dates[counter],newvalues[counter],atten_dates[counter],atten_newvalues[counter]

	#end data from gif file--------------------------------------

		new_rootdates = [TDatime(x.year, x.month, x.day, x.hour, x.minute, x.second) for x in dates] #rootdates with updated dates

		
	#start analysis, i'm in "i" not drift files	
		sectorscurrent = filename[5:9] #sector name
		meancurrent = np.mean(newvalues) #mean of current value
		
		#Identify drops
		valuesdeltas = np.diff(newvalues)
		valuesdeltas = [0]+valuesdeltas #differences in currents of voltages

		#remove spikes in current files
		copynewvalues = copy.copy(newvalues) #need to copy it to pass to function below
		nospike_newvalues = search.removespikes_atgif(valuesdeltas, copynewvalues, atten_newvalues) #remove spikes when source on at gif current files
		#for i in range(3):
		#	nospike_newvalues = search.removespikes_atgif([0]+np.diff(nospike_newvalues), nospike_newvalues, atten_values) #two times to actually remove spikes
		#nospike_newvalues = search.removespikes_atgif([0]+np.diff(nospike_newvalues), nospike_newvalues, atten_values) #two times to actually remove spikes
		#nospike_newvalues = search.removespikes_atgif([0]+np.diff(nospike_newvalues), nospike_newvalues, atten_values) #two times to actually remove spikes
		#nospike_newvalues = search.removespikes_atgif([0]+np.diff(nospike_newvalues), nospike_newvalues, atten_values) #two times to actually remove spikes
		nospike_meancurrent = np.mean(nospike_newvalues) #used to have real baseline of the current under fixed flux
		
		setattenvalues = set(atten_newvalues) 
		setattenvalues = [x for x in setattenvalues if float(x) != 0.] #remove 0
		setattenvalues.sort(reverse=True) #from min to max
		setmeancurrents = []
		normalizedsetmeancurrents = []

		#print len(newvalues), len(atten_newvalues)
		currentatzero = [x for counter, x in enumerate(newvalues[0:len(atten_newvalues)]) if atten_newvalues[counter] == 0.] #current when source is off  
		currentatzero = np.mean(currentatzero) #current mean when source is off

		for setattenuation in setattenvalues: #using nospike_newvalues here to not count spikes
			startindex = atten_newvalues.index(setattenuation) #first second at a given attenuation
			lastindex = len(atten_newvalues)-atten_newvalues[::-1].index(setattenuation)-1 #last second at a given attenuation
			middle = (lastindex-startindex)/2
			found = [x for x in nospike_newvalues[lastindex-60:lastindex]] 
			setmeancurrents.append(float(np.mean(found))) 
			normalizedsetmeancurrents.append(float(np.mean(found))/area)
			#this way gave problem as underestimates the current values
			#found = [x for counter, x in enumerate(nospike_newvalues[0:len(atten_newvalues)]) if atten_newvalues[counter] == setattenuation]
			#setmeancurrents.append(float(np.mean(found)))

		#if want to remove offset
		'''
		for counter in range(len(setmeancurrents)):
			setmeancurrents[counter] = setmeancurrents[counter] - currentatzero #remove offset
		'''

		for counter, setattenvalue in enumerate(setattenvalues):
			print setattenvalue, setmeancurrents[counter] #to check linearity of sectors
		
		setattenvalues = [float(x)**(-1) for x in setattenvalues] #perform 1/attenfactor
		#tools.write_attenuationrootgraph(setattenvalues, normalizedsetmeancurrents, filename, "1/attenuation", "i", dir_summary)
		graphlinearity = classes.attenuationrootgraph(filename[5:9], setattenvalues, normalizedsetmeancurrents, filename, "1/attenuation", "i", dir_summary)
		#find spikes -> new part to use threshold over plateu at given attenuation filter without spikes
		spikecounter, filename, spikedates, spikeseconds, spikenames, spikeduration = search.findspikes_atgif(newvalues, atten_newvalues, setmeancurrents, setattenvalues, dates, newtimes, filename)

	if "i" in filename and "D" in filename:
		sectorscurrent = None
		nospike_meancurrent = None

	if "v" in filename: #it's a voltage file
		sectorsvoltage = filename[5:9]
		meanvoltage = np.mean(newvalues)

		#Identify drops
		valuesdeltas = np.diff(newvalues)
		valuesdeltas = [0]+valuesdeltas #differences in currents of voltages

		copynewvalues = copy.copy(newvalues)
		notrips_newvalues = search.removetrips(valuesdeltas, copynewvalues)
		notrips_meanvoltage = np.mean(notrips_newvalues)

		if "D" in filename:
			sectorsvoltage = None
			notrips_meanvoltage = None

	if "i" not in filename or "D" in filename:
		spikenames = None
		duration = None
		spikeseconds = None
		spikeduration = None

	#write layer graphs
	#tools.write_roothistogram(newvalues, filename, filename[0], "Entries", rootdirectory) #if you want additional histograms
	
	if "i" in filename and "D" not in filename:
		#tools.write_rootdategraph_fromgif(rootdates, nospike_newvalues, filename, "time (s)", filename[0], rootdirectory) #plot graphs	
		#tools.write_rootdategraph_plusatten(new_rootdates, newvalues, atten_newvalues, filename, "time (s)", filename[0], rootdirectory) #plot graph current + source 
		graph_atten = classes.rootdategraph_plusatten(filename[5:9], new_rootdates, newvalues, atten_newvalues, filename, "time (s)", filename[0], rootdirectory)											     #or nospike_newvalues
		tools.write_rootdategraph_fromgif(rootdates, newvalues, filename, "time (s)", filename[0], rootdirectory)
	else:		
		tools.write_rootdategraph_fromgif(rootdates, newvalues, filename, "time (s)", filename[0], rootdirectory) #plot graphs	
		graph_atten = None
		graphlinearity = None

	#tools.write_rootdategraph_fromgif(rootdates, newvalues, filename, "time (s)", filename[0], rootdirectory) #plot graphs	
	
	if "D" not in filename:
		#create trees
		if "i" in filename:
			tree = TTree(filename, "tree")
			newvalue = array( 'f', [ 0 ] )
			branch = tree.Branch(filename, newvalue, "newvalue/F")
			
			treesource = TTree(filename+"_source", "tree")
			atten = array('f', [0])
			branch = treesource.Branch(filename, atten, "atten/F")
			for i in range(len(newvalues)):	
				newvalue[0] = newvalues[i]
				tree.Fill()
				atten[0] = atten_newvalues[i]
				treesource.Fill()
			tree.Write()
			treesource.Write()
		if "v" in filename:
			tree = TTree(filename, "tree")
			newvalue = array( 'f', [ 0 ] )
			branch = tree.Branch(filename, newvalue, "newvalue/F")
			for i in range(len(newvalues)):	
				newvalue[0] = newvalues[i]
				tree.Fill()
			tree.Write()
			
	return graph_atten, graphlinearity, spikenames, spikeduration, duration, sectorsvoltage, notrips_meanvoltage, sectorscurrent, nospike_meancurrent, spikeseconds
#----------------------------------------------------------------------------------------
#createsummaryplots_attenuation()
'''	
	if "i" in filename: #it's a current file
		#search.findrisingedges(valuesdeltas, dates)
		#search.findfallingedges(valuesdeltas, dates)
		
		sectorscurrent = filename[5:9]
		meancurrent = np.mean(newvalues)
		
		#remove spikes in current files
		copynewvalues = copy.copy(newvalues) #need to copy it to pass to function below
		nospike_newvalues = search.removespikes_atgif(valuesdeltas, copynewvalues)
		#nospike_newvalues = search.removespikes_atgif(np.diff(nospike_newvalues), nospike_newvalues) #two times to actually remove spikes
		#nospike_newvalues = search.removespikes_atgif(np.diff(nospike_newvalues), nospike_newvalues) #two times to actually remove spikes
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
'''
	