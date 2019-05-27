from datetime import datetime as dt
from datetime import timedelta as td
import sys
import os
import tools
from ROOT import TFile, TDatime, TDirectory, gSystem, TTree, gROOT, TH1, TH1F, gStyle, gPad, TGraph, TCanvas, TDatime, TMultiGraph, TLine, TLatex, TGaxis, TPad
import glob
import numpy as np
import search
import copy
import classes
from array import array

def write_rootdategraph(vectorx, vectory, graphtitle, xtitle, ytitle):
	"""Function to perform ROOT graph"""

	arrayx = array('d')
	arrayy = array('d')

	for x in vectorx:
		arrayx.append(x.Convert())

	for y in vectory:
		arrayy.append(y)

	if ytitle == "i":
		ytitle = ytitle+" (uA)"
		color = 2
		offset = 1.
		minimum = -1
		maximum = int(np.max(vectory)+1.5)
		if maximum > 10:
			maximum = int(10)

	if ytitle == "v":
		ytitle = ytitle+" (V)"
		color = 4
		offset = 0.9
		minimum = 0
		maximum = 600
		
	#How many graph points
	n = len(vectorx)

	MyTGraph = TGraph(n, arrayx, arrayy)
	MyTGraph.SetName(graphtitle)
	
	#Draw + DrawOptions
	c = TCanvas()
	Style = gStyle
	Style.SetPadLeftMargin(2.0)
	XAxis = MyTGraph.GetXaxis() #TGraphfasthescin
	XAxis.SetTimeDisplay(1)
	XAxis.SetTimeFormat("#splitline{%d/%m}{%H:%M:%S}")
	XAxis.SetLabelOffset(0.025)
	MyTGraph.SetMarkerColor(color)
	MyTGraph.SetMarkerStyle(1)
	MyTGraph.SetMarkerSize(1)
	MyTGraph.SetLineColor(color)
	MyTGraph.SetTitle(graphtitle)
	#XAxis.SetTitle(xtitle)
	YAxis = MyTGraph.GetYaxis()
	YAxis.SetTitleOffset(offset)
	YAxis.SetTitleOffset(offset)
	YAxis.SetTitle(ytitle)
	MyTGraph.GetHistogram().SetMinimum(minimum)
	MyTGraph.GetHistogram().SetMaximum(maximum)
	#MyTGraph.Draw("APL")
	#rootdirectory.WriteTObject(MyTGraph)
	MyTGraph.Write()
	#MyTGraph.Draw("APL")
	#if "D" not in graphtitle:
	#	gPad.SaveAs("BB5-"+graphtitle[0:9]+".pdf")
	#gPad.Close()


def createplot(file, filename):
	
	times = [x.split(' 	 ')[0] for x in open(file,"r").readlines()]
	if len(times) == 1:
		print "Exception -----> Only one data in "+str(filename)+".dat \n"
		return None
	if not times:
		print "Exception -----> File empty: "+str(filename)+".dat \n"
		return None
		
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

	write_rootdategraph(rootdates, newvalues, filename, "time (s)", filename[0])

	return None

path = raw_input("Insert path to folder: ")
folder = raw_input("Insert folder to study: ")
rootoutputfile = TFile(folder+".root","RECREATE")
path = path+"/"+folder+"/HV/"

for dat_file in glob.iglob(path+'*.dat'):
	print "Analyzing: "+dat_file[len(path):len(dat_file)]+" \n"
	filename = dat_file[len(path):len(dat_file)-4]
	createplot(dat_file, filename)