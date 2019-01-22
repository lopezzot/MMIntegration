from datetime import datetime as dt
from datetime import timedelta as td
import sys
import os
import tools
from ROOT import TFile, TDatime
import glob

folder = raw_input("Insert folder to study: ")
path = "../Export/"+folder+"/" 
#
#path1 = "SM1_FROM_2018_11_16_10_00_00_TO_2018_11_16_13_51_59/"
#path2 = "Export/"+path1+"/"
#name = raw_input("Insert filename: ")

rootfile = TFile(folder+".root","RECREATE")

#----------------------------------------------------------------------------------------
def createplot(file, filename):

	times = [x.split(' 	 ')[0] for x in open(file,"r").readlines()]
	times = [x.replace(':',' ') for x in times]
	times = [x.replace('/',' ') for x in times]
	times = [x.replace('_',' ') for x in times]
	times = [dt.strptime(x, '%m %d %Y %H %M %S') for x in times]
	starttime = times[0]
	times = [int((x-starttime).total_seconds()) for x in times]
	
	values = [float(x.split(' 	 ')[1]) for x in open(file,"r").readlines()]

	newtimes = range(times[len(times)-1])
	newvalues = [None]*len(newtimes)

	for counter, value in enumerate(newvalues):
		if counter in times:
			newvalues[counter] = values[times.index(counter)]
		else:
			newvalues[counter] = newvalues[counter-1]

	tools.draw_roothistogram(newvalues, filename, filename[0], "Entries",filename)
	tools.draw_rootgraph(newtimes, newvalues, filename, "time (s)", filename[0], filename)
#----------------------------------------------------------------------------------------
'''
for dat_file in glob.iglob(path+'*.dat'):
	if dat_file[len(path):len(dat_file)] != "iMon_L4D.dat":
		print "Analyzing: "+dat_file[len(path):len(dat_file)]+" \n"
		createplot(dat_file, dat_file[len(path):len(dat_file)])
'''	
#createplot("Export/SM1_FROM_2018_11_16_10_00_00_TO_2018_11_16_13_51_59/"+name, name)
