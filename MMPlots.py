from datetime import datetime as dt
from datetime import timedelta as td
import sys
import os
import tools
from ROOT import TFile, TDatime
import glob
import numpy as np
import search

folder = raw_input("Insert folder to study: ")
path = "../Export/"+folder+"/" 

rootfile = TFile(folder+".root","RECREATE")

#----------------------------------------------------------------------------------------
def createplot(file, filename):

	times = [x.split(' 	 ')[0] for x in open(file,"r").readlines()]
	if len(times) == 1:
		print "Only one data in "+str(filename)+".dat \n"
		return
	if not times:
		print "File empty: "+str(filename)+".dat \n"
		return

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
		#search.findrisingedges(valuesdeltas, dates)
		#search.findfallingedges(valuesdeltas, dates)
		spikedates = search.findspikes(valuesdeltas, dates)

	tools.write_roothistogram(newvalues, filename, filename[0], "Entries",filename)
	tools.write_rootgraph(rootdates, newvalues, filename, "time (s)", filename[0], filename)
#----------------------------------------------------------------------------------------

for dat_file in glob.iglob(path+'*.dat'):
	print "Analyzing: "+dat_file[len(path):len(dat_file)]+" \n"
	createplot(dat_file, dat_file[len(path):len(dat_file)-4])

#createplot("Export/SM1_FROM_2018_11_16_10_00_00_TO_2018_11_16_13_51_59/"+name, name)
