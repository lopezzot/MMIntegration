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
rootfile = TFile("/Users/lorenzo/Desktop/MMresults/"+folder+".root","RECREATE")
dir_L1 = rootfile.mkdir("Layer1/")
dir_L2 = rootfile.mkdir("Layer2/")
dir_L3 = rootfile.mkdir("Layer3/")
dir_L4 = rootfile.mkdir("Layer4/")
dir_summary = rootfile.mkdir("Summary/")
directories = {"L1":dir_L1,"L2":dir_L2,"L3":dir_L3,"L4":dir_L4}

spikenames = []
#----------------------------------------------------------------------------------------
def createplot(file, filename):

	layer = filename[5:7]
	rootdirectory = directories[layer] #to check

	times = [x.split(' 	 ')[0] for x in open(file,"r").readlines()]
	if len(times) == 1:
		print "Exception -----> Only one data in "+str(filename)+".dat \n"
		return None, None
	if not times:
		print "Exception -----> File empty: "+str(filename)+".dat \n"
		return None, None

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
	
	if "i" in filename: #it's a current file
		search.findrisingedges(valuesdeltas, dates)
		search.findfallingedges(valuesdeltas, dates)
		spikecounter, filename, spikedates, spikenames = search.findspikes(valuesdeltas, dates, filename)

	tools.write_roothistogram(newvalues, filename, filename[0], "Entries", rootdirectory)
	tools.write_rootgraph(rootdates, newvalues, filename, "time (s)", filename[0], rootdirectory)

	duration = len(newtimes) #total seconds from start to stop

	if "i" not in filename:
		spikenames = None
		duration = None

	return spikenames, duration
#----------------------------------------------------------------------------------------

for dat_file in glob.iglob(path+'*.dat'):
	print "Analyzing: "+dat_file[len(path):len(dat_file)]+" \n"
	spikeslayer, duration = createplot(dat_file, dat_file[len(path):len(dat_file)-4])
	if spikeslayer != None:
		spikenames = spikenames + spikeslayer
	if duration != None:
		deltatime = duration

tools.write_spikeroothistogram(spikenames, "spikes", "spikes/min", dir_summary, deltatime)


