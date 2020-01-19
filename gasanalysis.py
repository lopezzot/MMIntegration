from datetime import datetime as dt
from datetime import timedelta as td
import sys
import os
import tools
from ROOT import *
import glob
import numpy as np
import search
import copy
import classes
from array import array
import efficiency
import math

layers = ["L1L6", "L1R6", "L2L6", "L2R6", "L3L6", "L3R6", "L4L6", "L4R6", "L1L7", "L1R7", "L2L7", "L2R7", "L3L7", "L3R7", "L4L7", "L4R7", "L1L8", "L1R8", "L2L8", "L2R8", "L3L8", "L3R8", "L4L8", "L4R8"]
goodlayers = ["L1R6", "L2L6", "L2R6", "L2R7", "L3L6", "L3R6", "L3L7", "L3R7", "L4L6", "L4L7", "L4R7"]
goodlayers2 = ["L1R6", "L2L6", "L2R6", "L3L6", "L3R6", "L3L7", "L3R7", "L4L7", "L4R7"]
layersnosource = ["L1L6", "L1R6", "L2L6", "L2R6", "L3L6", "L3R6", "L2R7", "L3L7", "L3R7", "L4L7", "L4R7", "L1L8", "L2L8", "L3L8", "L3R8", "L4L8"]
layersnosource = ["L1L8", "L1R8", "L2L8", "L2R8", "L3L8", "L4R8"]
layersnosource2 = ["L1L8", "L2L8", "L3L8"]

rootfile = TFile("out.root", "RECREATE")

rootfilespikes = TFile("outspikes.root", "RECREATE")

rootfilenosource = TFile("outnosource.root", "RECREATE")

rootfilegain = TFile("outgain.root", "RECREATE")

def write_rootdategraph(vectorx, vectory, vectorx2, vectory2, graphtitle):
	"""Function to perform ROOT graph"""
	arrayx = array('d')
	arrayy = array('d')

	for x in vectorx:
		arrayx.append(x.Convert())

	for y in vectory:
		arrayy.append(y)
		
	#How many graph points
	n = len(vectorx)

	arrayx2 = array('d')
	arrayy2 = array('d')

	for x in vectorx2:
		arrayx2.append(x.Convert())

	for y in vectory2:
		arrayy2.append(y)
		
	#How many graph points
	n2 = len(vectorx2)
	
	MyTGraph = TGraph(n, arrayx, arrayy)
	MyTGraph2 = TGraph(n2, arrayx2, arrayy2)
	
	#Draw + DrawOptions
	c = TCanvas()
	pad1 = TPad("pad1","",0,0,1,1)
	pad2 = TPad("pad2","",0,0,1,1)
	pad2.SetFillStyle(4000)
	pad2.SetFrameFillStyle(0)

	Style = gStyle
	Style.SetPadLeftMargin(2.0)
	YAxis = MyTGraph.GetYaxis()
	YAxis.SetRangeUser(-1, 40.)
	XAxis = MyTGraph.GetXaxis() #TGraphfasthescin
	XAxis.SetTimeDisplay(1)
	XAxis.SetTimeFormat("%H:%M")
	XAxis.SetLabelOffset(0.025)
	MyTGraph.GetXaxis().SetNdivisions(910)
	MyTGraph.SetMarkerStyle(1)
	MyTGraph.SetMarkerSize(1)
	MyTGraph.GetYaxis().SetTitle("Current (uA)")
	MyTGraph.GetYaxis().SetTitleOffset(1.)
	MyTGraph.GetYaxis().SetTitleColor(2)
	MyTGraph.SetLineColorAlpha(2, 0.5)
	MyTGraph.SetLineWidth(1)
	MyTGraph.SetTitle(filename)

	XAxis2 = MyTGraph2.GetXaxis() #TGraphfasthescin
	XAxis2.SetTimeDisplay(1)
	XAxis2.SetTimeFormat("%H:%M")
	XAxis2.SetLabelOffset(0.025)
	MyTGraph2.SetMarkerStyle(1)
	MyTGraph2.SetMarkerSize(1)
	MyTGraph2.SetLineColor(4)
	MyTGraph2.GetXaxis().SetLabelSize(0)
	MyTGraph2.GetXaxis().SetNdivisions(910)
	MyTGraph2.GetYaxis().SetTitle("HV/100 (V)")
	MyTGraph2.GetYaxis().SetTitleOffset(1.)
	MyTGraph2.GetYaxis().SetTitleColor(4)
	MyTGraph2.SetTitle("")
	
	pad1.Draw()
	pad1.cd()
	MyTGraph.Draw("AL")

	pad2.Draw()
	pad2.cd()
	MyTGraph2.Draw("ALY+")
	c.SaveAs("gastest/"+str(filename)+".pdf")
	gPad.Close()

def write_summaryspikes(vectorx, vectory, graphtitle, filename):
	"""Function to perform ROOT graph"""
	arrayx = array('d')
	arrayy = array('d')

	for x in vectorx:
		arrayx.append(x)

	for y in vectory:
		arrayy.append(y)
		
	#How many graph points
	n = len(vectorx)

	MyTGraph = TGraph(n, arrayx, arrayy)
	
	'''
	#Draw + DrawOptions
	c = TCanvas()
	c.SetLogy()
	Style = gStyle
	Style.SetPadLeftMargin(2.0)
	YAxis = MyTGraph2.GetYaxis()
	YAxis.SetRangeUser(-1, 40.)
	XAxis = MyTGraph2.GetXaxis() #TGraphfasthescin
	XAxis.SetLabelOffset(0.025)
	MyTGraph2.GetXaxis().SetTitle("HV (V)")
	MyTGraph2.GetXaxis().SetTitleOffset(1.4)
	MyTGraph2.SetMarkerStyle(1)
	MyTGraph2.SetMarkerSize(1)
	MyTGraph2.GetYaxis().SetTitle("Current (uA)")
	MyTGraph2.GetYaxis().SetTitleOffset(1.)
	MyTGraph2.SetLineColorAlpha(1, 1.0)
	MyTGraph2.SetLineWidth(1)
	MyTGraph2.SetTitle(filename)
	rootfile.cd()
	'''
	YAxis = MyTGraph.GetYaxis()
	YAxis.SetRangeUser(-1, 10.)
	if "L2L6" in filename:
		YAxis.SetRangeUser(-1, 30.)
	YAxis.SetTitle("Spikes / min")
	XAxis = MyTGraph.GetXaxis()
	XAxis.SetLimits(-120., +80.)
	XAxis.SetTitle("Amplification Voltage (V)")
	XAxis.SetTitleOffset(1.2)
	MyTGraph.SetMarkerStyle(20)
	MyTGraph.SetMarkerSize(1)

	if "ARCO28020" in graphtitle and "10" in graphtitle:
		MyTGraph.SetMarkerColor(9)
		MyTGraph.SetLineColor(9)
		MyTGraph.SetMarkerStyle(24)

	if "ARCO28020" in graphtitle and "10" not in graphtitle:
		MyTGraph.SetMarkerColor(4)
		MyTGraph.SetLineColor(4)
		MyTGraph.SetMarkerStyle(24)

	if "ARCO2937" in graphtitle and "10" in graphtitle:
		MyTGraph.SetMarkerColor(8)
		MyTGraph.SetLineColor(8)
		MyTGraph.SetMarkerStyle(25)
		MyTGraph.SetMarkerStyle(25)

	if "ARCO2937" in graphtitle and "10" not in graphtitle:
		MyTGraph.SetMarkerColor(3)
		MyTGraph.SetLineColor(3)
		MyTGraph.SetMarkerStyle(25)

	if "ISOBUTANE" in graphtitle and "10" not in graphtitle:
		MyTGraph.SetMarkerColor(2)
		MyTGraph.SetLineColor(2)
		MyTGraph.SetMarkerStyle(26)

	if "ISOBUTANE" in graphtitle and "10" in graphtitle:
		MyTGraph.SetMarkerColor(6)
		MyTGraph.SetLineColor(6)
		MyTGraph.SetMarkerStyle(26)


	rootfilespikes.cd()
	MyTGraph.SetName(graphtitle)
	MyTGraph.SetTitle(filename)
	MyTGraph.Write()

def write_summaryhv(vectorx, vectory, graphtitle, filename):
	"""Function to perform ROOT graph"""
	arrayx = array('d')
	arrayy = array('d')

	for x in vectorx:
		arrayx.append(x)

	for y in vectory:
		arrayy.append(y)
		
	#How many graph points
	n = len(vectorx)

	MyTGraph = TGraph(n, arrayx, arrayy)
	
	'''
	#Draw + DrawOptions
	c = TCanvas()
	c.SetLogy()
	Style = gStyle
	Style.SetPadLeftMargin(2.0)
	YAxis = MyTGraph2.GetYaxis()
	YAxis.SetRangeUser(-1, 40.)
	XAxis = MyTGraph2.GetXaxis() #TGraphfasthescin
	XAxis.SetLabelOffset(0.025)
	MyTGraph2.GetXaxis().SetTitle("HV (V)")
	MyTGraph2.GetXaxis().SetTitleOffset(1.4)
	MyTGraph2.SetMarkerStyle(1)
	MyTGraph2.SetMarkerSize(1)
	MyTGraph2.GetYaxis().SetTitle("Current (uA)")
	MyTGraph2.GetYaxis().SetTitleOffset(1.)
	MyTGraph2.SetLineColorAlpha(1, 1.0)
	MyTGraph2.SetLineWidth(1)
	MyTGraph2.SetTitle(filename)
	rootfile.cd()
	'''
	YAxis = MyTGraph.GetYaxis()
	YAxis.SetRangeUser(-10., 100.)
	YAxis.SetTitle("Current (uA)")
	XAxis = MyTGraph.GetXaxis()
	XAxis.SetLimits(400., 740.)
	XAxis.SetTitle("Amplification Voltage (V)")
	XAxis.SetTitleOffset(1.2)
	MyTGraph.SetMarkerStyle(20)
	MyTGraph.SetMarkerSize(0.7)

	if "ARCO28020" in graphtitle and "10" in graphtitle:
		MyTGraph.SetMarkerColor(9)
		MyTGraph.SetLineColor(9)

	if "ARCO28020" in graphtitle and "10" not in graphtitle:
		MyTGraph.SetMarkerColor(4)
		MyTGraph.SetLineColor(4)

	if "ARCO2937" in graphtitle and "10" in graphtitle:
		MyTGraph.SetMarkerColor(8)
		MyTGraph.SetLineColor(8)

	if "ARCO2937" in graphtitle and "10" not in graphtitle:
		MyTGraph.SetMarkerColor(3)
		MyTGraph.SetLineColor(3)

	if "ARCO2937" in graphtitle and "100" in graphtitle:
		MyTGraph.SetMarkerColor(30)
		MyTGraph.SetLineColor(30)

	if "ARCO2937" in graphtitle and "1000" in graphtitle:
		MyTGraph.SetMarkerColor(32)
		MyTGraph.SetLineColor(32)

	if "ISOBUTANE" in graphtitle and "10" not in graphtitle:
		MyTGraph.SetMarkerColor(2)
		MyTGraph.SetLineColor(2)		
		f = TF1("f", "[Baseline]+exp([Constant]+[Slope]*x)", 420., 520.)
		MyTGraph.Fit(f, "R")

	if "ISOBUTANE" in graphtitle and "10" in graphtitle:
		MyTGraph.SetMarkerColor(46)
		MyTGraph.SetLineColor(46)
		f = TF1("f", "[Baseline]+exp([Constant]+[Slope]*x)", 440., 520.)
		MyTGraph.Fit(f, "R")

	if "ISOBUTANE" in graphtitle and "100" in graphtitle:
		MyTGraph.SetMarkerColor(50)
		MyTGraph.SetLineColor(50)
		f = TF1("f", "[Baseline]+exp([Constant]+[Slope]*x)", 500., 560.)
		MyTGraph.Fit(f, "R")

	if "ISOBUTANE" in graphtitle and "1000" in graphtitle:
		MyTGraph.SetMarkerColor(49)
		MyTGraph.SetLineColor(49)

	rootfile.cd()
	MyTGraph.SetName(graphtitle)
	MyTGraph.SetTitle(filename)
	MyTGraph.Write()

def write_summarygain(vectorx, vectory, graphtitle, filename):
	"""Function to perform ROOT graph"""
	arrayx = array('d')
	arrayy = array('d')

	for x in vectorx:
		arrayx.append(x)

	for y in vectory:
		arrayy.append(y)
		
	#How many graph points
	n = len(vectorx)

	MyTGraph = TGraph(n, arrayx, arrayy)
	
	YAxis = MyTGraph.GetYaxis()
	YAxis.SetRangeUser(0., 15.)
	YAxis.SetTitle("Current ratio")
	XAxis = MyTGraph.GetXaxis()
	XAxis.SetLimits(400., 740.)
	XAxis.SetTitle("Amplification Voltage (V)")
	XAxis.SetTitleOffset(1.2)
	MyTGraph.SetMarkerStyle(20)
	MyTGraph.SetMarkerSize(1)

	if "ARCO28020" in graphtitle and "10" in graphtitle:
		MyTGraph.SetMarkerColor(9)
		MyTGraph.SetLineColor(9)

	if "ARCO28020" in graphtitle and "10" not in graphtitle:
		MyTGraph.SetMarkerColor(4)
		MyTGraph.SetLineColor(4)

	if "ARCO2937" in graphtitle and "10" in graphtitle:
		MyTGraph.SetMarkerColor(8)
		MyTGraph.SetLineColor(8)

	if "ARCO2937" in graphtitle and "10" not in graphtitle:
		MyTGraph.SetMarkerColor(3)
		MyTGraph.SetLineColor(3)

	if "ISOBUTANE" in graphtitle and "10" not in graphtitle:
		MyTGraph.SetMarkerColor(2)
		MyTGraph.SetLineColor(2)

	if "ISOBUTANE" in graphtitle and "10" in graphtitle:
		MyTGraph.SetMarkerColor(46)
		MyTGraph.SetLineColor(46)


	rootfilegain.cd()
	MyTGraph.SetName(graphtitle)
	MyTGraph.SetTitle(filename)
	MyTGraph.Write()

def write_summarynosource(vectorx, vectory, graphtitle, filename):
	"""Function to perform ROOT graph"""
	arrayx = array('d')
	arrayy = array('d')

	for x in vectorx:
		arrayx.append(x)

	for y in vectory:
		arrayy.append(y)
		
	#How many graph points
	n = len(vectorx)

	MyTGraph = TGraph(n, arrayx, arrayy)
	
	'''
	#Draw + DrawOptions
	c = TCanvas()
	c.SetLogy()
	Style = gStyle
	Style.SetPadLeftMargin(2.0)
	YAxis = MyTGraph2.GetYaxis()
	YAxis.SetRangeUser(-1, 40.)
	XAxis = MyTGraph2.GetXaxis() #TGraphfasthescin
	XAxis.SetLabelOffset(0.025)
	MyTGraph2.GetXaxis().SetTitle("HV (V)")
	MyTGraph2.GetXaxis().SetTitleOffset(1.4)
	MyTGraph2.SetMarkerStyle(1)
	MyTGraph2.SetMarkerSize(1)
	MyTGraph2.GetYaxis().SetTitle("Current (uA)")
	MyTGraph2.GetYaxis().SetTitleOffset(1.)
	MyTGraph2.SetLineColorAlpha(1, 1.0)
	MyTGraph2.SetLineWidth(1)
	MyTGraph2.SetTitle(filename)
	rootfile.cd()
	'''
	YAxis = MyTGraph.GetYaxis()
	YAxis.SetRangeUser(-4, 45.)
	YAxis.SetTitle("Current (uA)")
	XAxis = MyTGraph.GetXaxis()
	XAxis.SetLimits(-100., 60.)
	XAxis.SetTitle("Amplification Voltage (V)")
	XAxis.SetTitleOffset(1.2)
	MyTGraph.SetMarkerStyle(20)
	MyTGraph.SetMarkerSize(1.0)

	if "ARCO28020" in graphtitle and "10" in graphtitle:
		MyTGraph.SetMarkerColor(9)
		MyTGraph.SetLineColor(9)

	if "ARCO28020" in graphtitle and "10" not in graphtitle:
		MyTGraph.SetMarkerColor(4)
		MyTGraph.SetLineColor(4)

	if "ARCO2937" in graphtitle and "10" in graphtitle:
		MyTGraph.SetMarkerColor(8)
		MyTGraph.SetLineColor(8)

	if "ARCO2937" in graphtitle and "10" not in graphtitle:
		MyTGraph.SetMarkerColor(3)
		MyTGraph.SetLineColor(3)

	if "ISOBUTANE" in graphtitle and "10" not in graphtitle:
		MyTGraph.SetMarkerColor(2)
		MyTGraph.SetLineColor(2)

	if "ISOBUTANE" in graphtitle and "10" in graphtitle:
		MyTGraph.SetMarkerColor(6)
		MyTGraph.SetLineColor(6)


	rootfilenosource.cd()
	MyTGraph.SetName(graphtitle)
	MyTGraph.SetTitle(filename)
	MyTGraph.Write()

def createplot(file, file2, filename):
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
	#print times
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

	#part file2
	times2 = [x[0:19] for x in open(file2,"r").readlines()]
	if len(times2) == 1:
		print "Exception -----> Only one data in "+str(filename)+".dat \n"
		return None
	if not times2:
		print "Exception -----> File empty: "+str(filename)+".dat \n"
		return None
	
	#part file2
	times2 = [x.replace(':',' ') for x in times2]
	times2 = [x.replace('/',' ') for x in times2]
	times2 = [x.replace('_',' ') for x in times2]
	
	times2 = [dt.strptime(x, '%m %d %Y %H %M %S') for x in times2]
	starttime2 = times2[0]
	dates2 = [starttime2]
	times2 = [int((x-starttime2).total_seconds()) for x in times2]
	values2 = [float(x[21:28]) for x in open(file2,"r").readlines()]
	print values2
	#print values2
	newtimes2 = range(times2[len(times2)-1])
	newvalues2 = [None]*len(newtimes2) 

	for counter, value in enumerate(newvalues2):
		if counter in times2:
			newvalues2[counter] = values2[times2.index(counter)]
		else:
			newvalues2[counter] = newvalues2[counter-1]

	for counter in range(len(newtimes2)-1):
		dates2.append(dates2[counter]+td(seconds=1))

	print dates2[0:10]
	print newvalues2[0:10]
	rootdates2 = [TDatime(x.year, x.month, x.day, x.hour, x.minute, x.second) for x in dates2]
	newvalues2 = [x/100. for x in newvalues2]
	
	if rootdates[0] not in rootdates2:
		for counter, i in enumerate(rootdates):
			if i in rootdates2:
				startrootdate = counter
				break
		rootdates = rootdates[startrootdate:]
		newvalues = newvalues[startrootdate:]

	if len(rootdates) > len(rootdates2):
		rootdates = rootdates[:len(rootdates2)]
		newvalues = newvalues[:len(newvalues2)]
	else:
		rootdates2 = rootdates2[:len(rootdates)]
		newvalues2 = newvalues2[:len(newvalues)]
	
	#common part
	write_rootdategraph(rootdates, newvalues, rootdates2, newvalues2, filename)

def processARCO28020(file, file2, filename):
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
	#print times
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
	#part file2
	times2 = [x[0:19] for x in open(file2,"r").readlines()]
	if len(times2) == 1:
		print "Exception -----> Only one data in "+str(filename)+".dat \n"
		return None
	if not times2:
		print "Exception -----> File empty: "+str(filename)+".dat \n"
		return None	
	#part file2
	times2 = [x.replace(':',' ') for x in times2]
	times2 = [x.replace('/',' ') for x in times2]
	times2 = [x.replace('_',' ') for x in times2]
	
	times2 = [dt.strptime(x, '%m %d %Y %H %M %S') for x in times2]	
	starttime2 = times2[0]
	dates2 = [starttime2]	
	times2 = [int((x-starttime2).total_seconds()) for x in times2]	
	values2 = [float(x[21:28]) for x in open(file2,"r").readlines()]
	
	newtimes2 = range(times2[len(times2)-1])
	newvalues2 = [None]*len(newtimes2)	
	for counter, value in enumerate(newvalues2):
		if counter in times2:
			newvalues2[counter] = values2[times2.index(counter)]
		else:
			newvalues2[counter] = newvalues2[counter-1]	
	for counter in range(len(newtimes2)-1):
		dates2.append(dates2[counter]+td(seconds=1))	
	rootdates2 = [TDatime(x.year, x.month, x.day, x.hour, x.minute, x.second) for x in dates2]
	
	if rootdates[0] not in rootdates2:
		for counter, i in enumerate(rootdates):
			if i in rootdates2:
				startrootdate = counter
				break
		rootdates = rootdates[startrootdate:]
		newvalues = newvalues[startrootdate:]	
	if len(rootdates) > len(rootdates2):
		rootdates = rootdates[:len(rootdates2)]
		newvalues = newvalues[:len(newvalues2)]
	else:
		rootdates2 = rootdates2[:len(rootdates)]
		newvalues2 = newvalues2[:len(newvalues)]
	
	if "_att10" not in filename: 			
		newvalues2 = newvalues2[4*60:len(newvalues2)-7*60]
		newvalues = newvalues[4*60:len(newvalues)-7*60] 	

	newvalues2 = [int(math.ceil(x / 10.0)) * 10 for x in newvalues2]
	hvvalues = [550, 560, 570, 580, 590, 600, 610, 620, 630, 640, 650, 660, 670, 680, 690, 700]
	if "_att10" in filename:
		hvvalues = [550, 560, 570, 580, 590, 600, 610, 620, 630, 640, 650, 690, 700]
	ivalues = []
	hvvaluescheck = []
	for x in hvvalues:	
		f = np.mean([c for counter, c in enumerate(newvalues) if newvalues2[counter] == x])
		if math.isnan(f) == False:
			ivalues.append(f)
			hvvaluescheck.append(x)

	write_summaryhv(hvvaluescheck, ivalues, "ARCO28020 - "+str(filename), filename)
	return hvvaluescheck, ivalues

def processARCO28020nosource(file, file2, filename):
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
	#print times
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
	#part file2
	times2 = [x[0:19] for x in open(file2,"r").readlines()]
	if len(times2) == 1:
		print "Exception -----> Only one data in "+str(filename)+".dat \n"
		return None
	if not times2:
		print "Exception -----> File empty: "+str(filename)+".dat \n"
		return None	
	#part file2
	times2 = [x.replace(':',' ') for x in times2]
	times2 = [x.replace('/',' ') for x in times2]
	times2 = [x.replace('_',' ') for x in times2]
	
	times2 = [dt.strptime(x, '%m %d %Y %H %M %S') for x in times2]	
	starttime2 = times2[0]
	dates2 = [starttime2]	
	times2 = [int((x-starttime2).total_seconds()) for x in times2]	
	values2 = [float(x[21:28]) for x in open(file2,"r").readlines()]
	
	#print values2
	newtimes2 = range(times2[len(times2)-1])
	newvalues2 = [None]*len(newtimes2)	
	for counter, value in enumerate(newvalues2):
		if counter in times2:
			newvalues2[counter] = values2[times2.index(counter)]
		else:
			newvalues2[counter] = newvalues2[counter-1]	
	for counter in range(len(newtimes2)-1):
		dates2.append(dates2[counter]+td(seconds=1))	
	rootdates2 = [TDatime(x.year, x.month, x.day, x.hour, x.minute, x.second) for x in dates2]
	
	if rootdates[0] not in rootdates2:
		for counter, i in enumerate(rootdates):
			if i in rootdates2:
				startrootdate = counter
				break
		rootdates = rootdates[startrootdate:]
		newvalues = newvalues[startrootdate:]	
	if len(rootdates) > len(rootdates2):
		rootdates = rootdates[:len(rootdates2)]
		newvalues = newvalues[:len(newvalues2)]
	else:
		rootdates2 = rootdates2[:len(rootdates)]
		newvalues2 = newvalues2[:len(newvalues)]
	
	newvalues2 = newvalues2[4*60:len(newvalues2)-7*60]
	newvalues = newvalues[4*60:len(newvalues)-7*60] 	
	newvalues2 = [int(math.ceil(x / 10.0)) * 10 for x in newvalues2]
	hvvalues = [550, 560, 570, 580, 590, 600, 610, 620, 630, 640, 650, 660, 670, 680]
	if "L2L8" in filename or "L2R8" in filename or "L4R8" in filename:
		hvvalues = [550, 560, 570, 580, 590, 600, 610, 620, 630, 640, 650, 660, 670]
	
	ivalues = []
	hvvaluescheck = []
	for x in hvvalues:	
		f = np.mean([c for counter, c in enumerate(newvalues) if newvalues2[counter] == x])
		if math.isnan(f) == False:
			ivalues.append(f)
			hvvaluescheck.append(x)

	print hvvaluescheck, ivalues
	hvvaluescheck = [x-645 for x in hvvaluescheck]
	write_summarynosource(hvvaluescheck, ivalues, "ARCO28020 - "+str(filename), filename)

def processARCO28020spikes(file, file2, filename):
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
	#print times
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
	#part file2
	times2 = [x[0:19] for x in open(file2,"r").readlines()]
	if len(times2) == 1:
		print "Exception -----> Only one data in "+str(filename)+".dat \n"
		return None
	if not times2:
		print "Exception -----> File empty: "+str(filename)+".dat \n"
		return None	
	#part file2
	times2 = [x.replace(':',' ') for x in times2]
	times2 = [x.replace('/',' ') for x in times2]
	times2 = [x.replace('_',' ') for x in times2]
	
	times2 = [dt.strptime(x, '%m %d %Y %H %M %S') for x in times2]	
	starttime2 = times2[0]
	dates2 = [starttime2]	
	times2 = [int((x-starttime2).total_seconds()) for x in times2]	
	values2 = [float(x[21:28]) for x in open(file2,"r").readlines()]
	
	#print values2
	newtimes2 = range(times2[len(times2)-1])
	newvalues2 = [None]*len(newtimes2)	
	for counter, value in enumerate(newvalues2):
		if counter in times2:
			newvalues2[counter] = values2[times2.index(counter)]
		else:
			newvalues2[counter] = newvalues2[counter-1]	
	for counter in range(len(newtimes2)-1):
		dates2.append(dates2[counter]+td(seconds=1))	
	rootdates2 = [TDatime(x.year, x.month, x.day, x.hour, x.minute, x.second) for x in dates2]
	
	if rootdates[0] not in rootdates2:
		for counter, i in enumerate(rootdates):
			if i in rootdates2:
				startrootdate = counter
				break
		rootdates = rootdates[startrootdate:]
		newvalues = newvalues[startrootdate:]	
	if len(rootdates) > len(rootdates2):
		rootdates = rootdates[:len(rootdates2)]
		newvalues = newvalues[:len(newvalues2)]
	else:
		rootdates2 = rootdates2[:len(rootdates)]
		newvalues2 = newvalues2[:len(newvalues)]
	
	newvalues2 = newvalues2[4*60:len(newvalues2)-7*60]
	newvalues = newvalues[4*60:len(newvalues)-7*60] 	
	newvalues2 = [int(math.ceil(x / 10.0)) * 10 for x in newvalues2]
	hvvalues = [550, 560, 570, 580, 590, 600, 610, 620, 630, 640, 650, 660, 670, 680, 690, 700]
	spikesvalues = []
	hvvaluescheck = []
	for x in hvvalues:	
		subset = [c for counter, c in enumerate(newvalues) if newvalues2[counter] == x]
		if len(subset) > 0:
			subset = subset[10:] #to exclude charging up effects
			f = np.mean(subset)
			counterspikes = 0
			for d in subset:
				if d > f + 0.2:
					counterspikes = counterspikes+1
			counterspikes = counterspikes/(float(len(subset))/60.)
			if math.isnan(f) == False:
				spikesvalues.append(counterspikes)
				hvvaluescheck.append(x)

	print hvvaluescheck, spikesvalues
	hvvaluescheck = [x-640 for x in hvvaluescheck]
	write_summaryspikes(hvvaluescheck, spikesvalues, "ARCO28020 - "+str(filename), filename)

def processisobutane(file, file2, filename):
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
	#print times
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
	#part file2
	times2 = [x[0:19] for x in open(file2,"r").readlines()]
	if len(times2) == 1:
		print "Exception -----> Only one data in "+str(filename)+".dat \n"
		return None
	if not times2:
		print "Exception -----> File empty: "+str(filename)+".dat \n"
		return None	
	#part file2
	times2 = [x.replace(':',' ') for x in times2]
	times2 = [x.replace('/',' ') for x in times2]
	times2 = [x.replace('_',' ') for x in times2]
	
	times2 = [dt.strptime(x, '%m %d %Y %H %M %S') for x in times2]	
	starttime2 = times2[0]
	dates2 = [starttime2]	
	times2 = [int((x-starttime2).total_seconds()) for x in times2]	
	values2 = [float(x[21:28]) for x in open(file2,"r").readlines()]
	
	#print values2
	newtimes2 = range(times2[len(times2)-1])
	newvalues2 = [None]*len(newtimes2)	
	for counter, value in enumerate(newvalues2):
		if counter in times2:
			newvalues2[counter] = values2[times2.index(counter)]
		else:
			newvalues2[counter] = newvalues2[counter-1]	
	for counter in range(len(newtimes2)-1):
		dates2.append(dates2[counter]+td(seconds=1))	
	rootdates2 = [TDatime(x.year, x.month, x.day, x.hour, x.minute, x.second) for x in dates2]
	
	if rootdates[0] not in rootdates2:
		for counter, i in enumerate(rootdates):
			if i in rootdates2:
				startrootdate = counter
				break
		rootdates = rootdates[startrootdate:]
		newvalues = newvalues[startrootdate:]	
	if len(rootdates) > len(rootdates2):
		rootdates = rootdates[:len(rootdates2)]
		newvalues = newvalues[:len(newvalues2)]
	else:
		rootdates2 = rootdates2[:len(rootdates)]
		newvalues2 = newvalues2[:len(newvalues)]
	
	#newvalues2 = newvalues2[4*60:len(newvalues2)-7*60]
	#newvalues = newvalues[4*60:len(newvalues)-7*60] 	
	if filename == "L4L6_att10":
		newvalues2 = newvalues2[:len(newvalues2)-10*60]
		newvalues = newvalues[4*60:len(newvalues)-10*60] 	
	
	newvalues2 = [int(math.ceil(x / 10.0)) * 10 for x in newvalues2]
	hvvalues = [420, 430, 440, 450, 460, 470, 480, 490, 500, 510, 520, 530, 540, 550, 560, 570]
	if filename == "L2R7_att10":
		hvvalues = [450, 460, 470, 480, 490, 500, 510, 520, 530, 540, 550, 560, 570]

	if "_att100" in filename and "_att1000" not in filename:
		hvvalues = [500, 510, 520, 530, 540, 550, 560]

	if "_att1000" in filename:
		hvvalues = [530, 540, 550, 560]

	ivalues = []
	hvvaluescheck = []
	for x in hvvalues:	
		f = np.mean([c for counter, c in enumerate(newvalues) if newvalues2[counter] == x])
		if math.isnan(f) == False:
			ivalues.append(f)
			hvvaluescheck.append(x)

	print hvvaluescheck, ivalues
	write_summaryhv(hvvaluescheck, ivalues, "ISOBUTANE - "+str(filename), filename)
	return hvvaluescheck, ivalues

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
	#print times
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
	#part file2
	times2 = [x[0:19] for x in open(file2,"r").readlines()]
	if len(times2) == 1:
		print "Exception -----> Only one data in "+str(filename)+".dat \n"
		return None
	if not times2:
		print "Exception -----> File empty: "+str(filename)+".dat \n"
		return None	
	#part file2
	times2 = [x.replace(':',' ') for x in times2]
	times2 = [x.replace('/',' ') for x in times2]
	times2 = [x.replace('_',' ') for x in times2]
	
	times2 = [dt.strptime(x, '%m %d %Y %H %M %S') for x in times2]	
	starttime2 = times2[0]
	dates2 = [starttime2]	
	times2 = [int((x-starttime2).total_seconds()) for x in times2]	
	values2 = [float(x[21:28]) for x in open(file2,"r").readlines()]
	
	#print values2
	newtimes2 = range(times2[len(times2)-1])
	newvalues2 = [None]*len(newtimes2)	
	for counter, value in enumerate(newvalues2):
		if counter in times2:
			newvalues2[counter] = values2[times2.index(counter)]
		else:
			newvalues2[counter] = newvalues2[counter-1]	
	for counter in range(len(newtimes2)-1):
		dates2.append(dates2[counter]+td(seconds=1))	
	rootdates2 = [TDatime(x.year, x.month, x.day, x.hour, x.minute, x.second) for x in dates2]
	
	if rootdates[0] not in rootdates2:
		for counter, i in enumerate(rootdates):
			if i in rootdates2:
				startrootdate = counter
				break
		rootdates = rootdates[startrootdate:]
		newvalues = newvalues[startrootdate:]	
	if len(rootdates) > len(rootdates2):
		rootdates = rootdates[:len(rootdates2)]
		newvalues = newvalues[:len(newvalues2)]
	else:
		rootdates2 = rootdates2[:len(rootdates)]
		newvalues2 = newvalues2[:len(newvalues)]
	
	#newvalues2 = newvalues2[4*60:len(newvalues2)-7*60]
	#newvalues = newvalues[4*60:len(newvalues)-7*60] 	
	if filename == "L4L6_att10":
		newvalues2 = newvalues2[:len(newvalues2)-10*60]
		newvalues = newvalues[4*60:len(newvalues)-10*60] 	
	
	newvalues2 = [int(math.ceil(x / 10.0)) * 10 for x in newvalues2]
	hvvalues = [420, 430, 440, 450, 460, 470, 480, 490, 500, 510, 520, 530, 540, 550, 560, 570]
	ivalues = []
	hvvaluescheck = []
	for x in hvvalues:	
		f = np.mean([c for counter, c in enumerate(newvalues) if newvalues2[counter] == x])
		if math.isnan(f) == False:
			ivalues.append(f)
			hvvaluescheck.append(x)

	print hvvaluescheck, ivalues
	hvvaluescheck = [x-520 for x in hvvaluescheck]
	write_summarynosource(hvvaluescheck, ivalues, "ISOBUTANE - "+str(filename), filename)

def processisobutanespikes(file, file2, filename):
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
	#print times
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
	#part file2
	times2 = [x[0:19] for x in open(file2,"r").readlines()]
	if len(times2) == 1:
		print "Exception -----> Only one data in "+str(filename)+".dat \n"
		return None
	if not times2:
		print "Exception -----> File empty: "+str(filename)+".dat \n"
		return None	
	#part file2
	times2 = [x.replace(':',' ') for x in times2]
	times2 = [x.replace('/',' ') for x in times2]
	times2 = [x.replace('_',' ') for x in times2]
	
	times2 = [dt.strptime(x, '%m %d %Y %H %M %S') for x in times2]	
	starttime2 = times2[0]
	dates2 = [starttime2]	
	times2 = [int((x-starttime2).total_seconds()) for x in times2]	
	values2 = [float(x[21:28]) for x in open(file2,"r").readlines()]
	
	#print values2
	newtimes2 = range(times2[len(times2)-1])
	newvalues2 = [None]*len(newtimes2)	
	for counter, value in enumerate(newvalues2):
		if counter in times2:
			newvalues2[counter] = values2[times2.index(counter)]
		else:
			newvalues2[counter] = newvalues2[counter-1]	
	for counter in range(len(newtimes2)-1):
		dates2.append(dates2[counter]+td(seconds=1))	
	rootdates2 = [TDatime(x.year, x.month, x.day, x.hour, x.minute, x.second) for x in dates2]
	
	if rootdates[0] not in rootdates2:
		for counter, i in enumerate(rootdates):
			if i in rootdates2:
				startrootdate = counter
				break
		rootdates = rootdates[startrootdate:]
		newvalues = newvalues[startrootdate:]	
	if len(rootdates) > len(rootdates2):
		rootdates = rootdates[:len(rootdates2)]
		newvalues = newvalues[:len(newvalues2)]
	else:
		rootdates2 = rootdates2[:len(rootdates)]
		newvalues2 = newvalues2[:len(newvalues)]
	
	#newvalues2 = newvalues2[4*60:len(newvalues2)-7*60]
	#newvalues = newvalues[4*60:len(newvalues)-7*60] 	
	if filename == "L4L6_att10":
		newvalues2 = newvalues2[:len(newvalues2)-10*60]
		newvalues = newvalues[4*60:len(newvalues)-10*60] 	
	
	newvalues2 = [int(math.ceil(x / 10.0)) * 10 for x in newvalues2]
	hvvalues = [420, 430, 440, 450, 460, 470, 480, 490, 500, 510, 520, 530, 540, 550, 560, 570]
	spikesvalues = []
	hvvaluescheck = []
	for x in hvvalues:	
		subset = [c for counter, c in enumerate(newvalues) if newvalues2[counter] == x]
		if len(subset) > 0:
			subset = subset[10:]
			f = np.mean(subset)
			counterspikes = 0
			for d in subset:
				if d > f + 0.2:
					counterspikes = counterspikes+1
			counterspikes = counterspikes/(float(len(subset))/60.)
			if math.isnan(f) == False:
				if x < 445:
					counterspikes = 0.0
				spikesvalues.append(counterspikes)
				hvvaluescheck.append(x)


	print hvvaluescheck, spikesvalues
	hvvaluescheck = [x-520 for x in hvvaluescheck]
	write_summaryspikes(hvvaluescheck, spikesvalues, "ISOBUTANE - "+str(filename), filename)

def processARCO2937(file, file2, filename):
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
	#print times
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
	#part file2
	times2 = [x[0:19] for x in open(file2,"r").readlines()]
	if len(times2) == 1:
		print "Exception -----> Only one data in "+str(filename)+".dat \n"
		return None
	if not times2:
		print "Exception -----> File empty: "+str(filename)+".dat \n"
		return None	
	#part file2
	times2 = [x.replace(':',' ') for x in times2]
	times2 = [x.replace('/',' ') for x in times2]
	times2 = [x.replace('_',' ') for x in times2]
	
	times2 = [dt.strptime(x, '%m %d %Y %H %M %S') for x in times2]	
	starttime2 = times2[0]
	dates2 = [starttime2]	
	times2 = [int((x-starttime2).total_seconds()) for x in times2]	
	values2 = [float(x[21:28]) for x in open(file2,"r").readlines()]
	
	#print values2
	newtimes2 = range(times2[len(times2)-1])
	newvalues2 = [None]*len(newtimes2)	
	for counter, value in enumerate(newvalues2):
		if counter in times2:
			newvalues2[counter] = values2[times2.index(counter)]
		else:
			newvalues2[counter] = newvalues2[counter-1]	
	for counter in range(len(newtimes2)-1):
		dates2.append(dates2[counter]+td(seconds=1))	
	rootdates2 = [TDatime(x.year, x.month, x.day, x.hour, x.minute, x.second) for x in dates2]
	
	if rootdates[0] not in rootdates2:
		for counter, i in enumerate(rootdates):
			if i in rootdates2:
				startrootdate = counter
				break
		rootdates = rootdates[startrootdate:]
		newvalues = newvalues[startrootdate:]	
	if len(rootdates) > len(rootdates2):
		rootdates = rootdates[:len(rootdates2)]
		newvalues = newvalues[:len(newvalues2)]
	else:
		rootdates2 = rootdates2[:len(rootdates)]
		newvalues2 = newvalues2[:len(newvalues)]
	
	#newvalues2 = newvalues2[4*60:len(newvalues2)-7*60]
	#newvalues = newvalues[4*60:len(newvalues)-7*60] 	
	newvalues2 = [int(math.ceil(x / 10.0)) * 10 for x in newvalues2]
	hvvalues = [490, 500, 510, 520, 530, 540, 550, 560, 570, 580, 590]

	if "100" in filename and "1000" not in filename:
		hvvalues = [520, 530, 540, 550, 560, 570, 580]

	if "1000" in filename:
		hvvalues = [490, 500, 510, 520, 530, 540, 550, 560, 570, 580, 590, 600]

	ivalues = []
	hvvaluescheck = []
	for x in hvvalues:	
		f = np.mean([c for counter, c in enumerate(newvalues) if newvalues2[counter] == x])
		if filename == "L2R7_att100" and x == 580:
			p = [c for counter, c in enumerate(newvalues) if newvalues2[counter] == x]
			f = np.mean(p[:len(p)-7*60]) #remove last 7 minutes
		if math.isnan(f) == False:
			ivalues.append(f)
			hvvaluescheck.append(x)

	write_summaryhv(hvvaluescheck, ivalues, "ARCO2937 - "+str(filename), filename)
	return hvvaluescheck, ivalues

def processARCO2937nosource(file, file2, filename):
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
	#print times
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
	#part file2
	times2 = [x[0:19] for x in open(file2,"r").readlines()]
	if len(times2) == 1:
		print "Exception -----> Only one data in "+str(filename)+".dat \n"
		return None
	if not times2:
		print "Exception -----> File empty: "+str(filename)+".dat \n"
		return None	
	#part file2
	times2 = [x.replace(':',' ') for x in times2]
	times2 = [x.replace('/',' ') for x in times2]
	times2 = [x.replace('_',' ') for x in times2]
	
	times2 = [dt.strptime(x, '%m %d %Y %H %M %S') for x in times2]	
	starttime2 = times2[0]
	dates2 = [starttime2]	
	times2 = [int((x-starttime2).total_seconds()) for x in times2]	
	values2 = [float(x[21:28]) for x in open(file2,"r").readlines()]
	
	#print values2
	newtimes2 = range(times2[len(times2)-1])
	newvalues2 = [None]*len(newtimes2)	
	for counter, value in enumerate(newvalues2):
		if counter in times2:
			newvalues2[counter] = values2[times2.index(counter)]
		else:
			newvalues2[counter] = newvalues2[counter-1]	
	for counter in range(len(newtimes2)-1):
		dates2.append(dates2[counter]+td(seconds=1))	
	rootdates2 = [TDatime(x.year, x.month, x.day, x.hour, x.minute, x.second) for x in dates2]
	
	if rootdates[0] not in rootdates2:
		for counter, i in enumerate(rootdates):
			if i in rootdates2:
				startrootdate = counter
				break
		rootdates = rootdates[startrootdate:]
		newvalues = newvalues[startrootdate:]	
	if len(rootdates) > len(rootdates2):
		rootdates = rootdates[:len(rootdates2)]
		newvalues = newvalues[:len(newvalues2)]
	else:
		rootdates2 = rootdates2[:len(rootdates)]
		newvalues2 = newvalues2[:len(newvalues)]
	
	#newvalues2 = newvalues2[4*60:len(newvalues2)-7*60]
	#newvalues = newvalues[4*60:len(newvalues)-7*60] 	
	newvalues2 = [int(math.ceil(x / 10.0)) * 10 for x in newvalues2]
	hvvalues = [490, 500, 510, 520, 530, 540, 550, 560, 570, 580, 590]
	ivalues = []
	hvvaluescheck = []
	for x in hvvalues:	
		f = np.mean([c for counter, c in enumerate(newvalues) if newvalues2[counter] == x])
		if math.isnan(f) == False:
			ivalues.append(f)
			hvvaluescheck.append(x)

	print hvvaluescheck, ivalues
	hvvaluescheck = [x-570 for x in hvvaluescheck]
	write_summarynosource(hvvaluescheck, ivalues, "ARCO2937 - "+str(filename), filename)

def processARCO2937spikes(file, file2, filename):
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
	#print times
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
	#part file2
	times2 = [x[0:19] for x in open(file2,"r").readlines()]
	if len(times2) == 1:
		print "Exception -----> Only one data in "+str(filename)+".dat \n"
		return None
	if not times2:
		print "Exception -----> File empty: "+str(filename)+".dat \n"
		return None	
	#part file2
	times2 = [x.replace(':',' ') for x in times2]
	times2 = [x.replace('/',' ') for x in times2]
	times2 = [x.replace('_',' ') for x in times2]
	
	times2 = [dt.strptime(x, '%m %d %Y %H %M %S') for x in times2]	
	starttime2 = times2[0]
	dates2 = [starttime2]	
	times2 = [int((x-starttime2).total_seconds()) for x in times2]	
	values2 = [float(x[21:28]) for x in open(file2,"r").readlines()]
	
	#print values2
	newtimes2 = range(times2[len(times2)-1])
	newvalues2 = [None]*len(newtimes2)	
	for counter, value in enumerate(newvalues2):
		if counter in times2:
			newvalues2[counter] = values2[times2.index(counter)]
		else:
			newvalues2[counter] = newvalues2[counter-1]	
	for counter in range(len(newtimes2)-1):
		dates2.append(dates2[counter]+td(seconds=1))	
	rootdates2 = [TDatime(x.year, x.month, x.day, x.hour, x.minute, x.second) for x in dates2]
	
	if rootdates[0] not in rootdates2:
		for counter, i in enumerate(rootdates):
			if i in rootdates2:
				startrootdate = counter
				break
		rootdates = rootdates[startrootdate:]
		newvalues = newvalues[startrootdate:]	
	if len(rootdates) > len(rootdates2):
		rootdates = rootdates[:len(rootdates2)]
		newvalues = newvalues[:len(newvalues2)]
	else:
		rootdates2 = rootdates2[:len(rootdates)]
		newvalues2 = newvalues2[:len(newvalues)]
	
	#newvalues2 = newvalues2[4*60:len(newvalues2)-7*60]
	#newvalues = newvalues[4*60:len(newvalues)-7*60] 	
	newvalues2 = [int(math.ceil(x / 10.0)) * 10 for x in newvalues2]
	hvvalues = [490, 500, 510, 520, 530, 540, 550, 560, 570, 580, 590]
	spikesvalues = []
	hvvaluescheck = []
	for x in hvvalues:	
		subset = [c for counter, c in enumerate(newvalues) if newvalues2[counter] == x]
		if len(subset) > 0:
			subset = subset[10:]
			f = np.mean(subset)
			counterspikes = 0
			for d in subset:
				if d > f + 0.2:
					counterspikes = counterspikes+1
			counterspikes = counterspikes/(float(len(subset))/60.)
			if math.isnan(f) == False:
				spikesvalues.append(counterspikes)
				hvvaluescheck.append(x)

	print hvvaluescheck, spikesvalues
	hvvaluescheck = [x-570 for x in hvvaluescheck]
	write_summaryspikes(hvvaluescheck, spikesvalues, "ARCO2937 - "+str(filename), filename)


for L in goodlayers:
	print "Gain summary: "+str(L)
	filename = L
	
	#ARCO2 80-20 source at 2.2
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_10_15_08_22_TO_2019_12_10_18_18_04/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_10_15_08_22_TO_2019_12_10_18_18_04/HV/vMon_"+str(L)+".dat"
	hvvaluescheck, ivalues = processARCO28020(file1, file2, filename)
   
	#ARCO2 80-20 source at 10.0
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_18_09_08_00_TO_2019_12_18_10_13_44/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_18_09_08_00_TO_2019_12_18_10_13_44/HV/vMon_"+str(L)+".dat"
	hvvaluescheck2, ivalues2 = processARCO28020(file1, file2, filename+"_att10")
	hvvaluescheck = hvvaluescheck[0:11]+hvvaluescheck[14:16]
	ivalues = ivalues[0:11]+ivalues[14:16]
	gain = []
	hvgain = []
	for counter, x in enumerate(hvvaluescheck):
		hvgain.append(x)
		gain.append(ivalues[counter]/ivalues2[counter])
	print "ARCO28020:"
	print ivalues, ivalues2
	write_summarygain(hvgain, gain, "ARCO28020_"+str(filename), filename)
	
	#ISOBUTANE source at 2.2
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_12_11_37_30_TO_2019_12_12_13_04_08/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_12_11_37_30_TO_2019_12_12_13_04_08/HV/vMon_"+str(L)+".dat"
	hvvaluescheck, ivalues = processisobutane(file1, file2, filename)
   
	#ISOBUTANE source at 10.0
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_13_09_56_53_TO_2019_12_13_11_09_06/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_13_09_56_53_TO_2019_12_13_11_09_06/HV/vMon_"+str(L)+".dat"
	hvvaluescheck2, ivalues2 = processisobutane(file1, file2, filename+"_att10")
	hvvaluescheck = hvvaluescheck[2:11]
	ivalues = ivalues[2:11]
	gain = []
	hvgain = []
	for counter, x in enumerate(hvvaluescheck2):
		hvgain.append(x)
		gain.append(ivalues[counter]/ivalues2[counter])
	write_summarygain(hvgain, gain, "ISOBUTANE_"+str(filename), filename)
	
	#ISOBUTANE source at 100.0
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_16_17_50_38_TO_2020_01_16_19_14_20/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_16_17_50_38_TO_2020_01_16_19_14_20/HV/vMon_"+str(L)+".dat"
	hvvaluescheck3, ivalues3 = processisobutane(file1, file2, filename+"_att100")
	hvvaluescheck3 = hvvaluescheck3[:3]
	ivalues3 = ivalues3[:3]
	gain = []
	hvgain = []
	ivalues2 = ivalues2[6:]
	hvvaluescheck2 = hvvaluescheck2[6:]
	for counter, x in enumerate(hvvaluescheck3):
		hvgain.append(x)
		gain.append(ivalues2[counter]/ivalues3[counter])
	write_summarygain(hvgain, gain, "ISOBUTANE_"+str(filename)+"_2", filename+"_2")
	
	#ARCO2 93-7 SOURCE AT 2.2
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_16_14_02_40_TO_2019_12_16_17_13_09/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_16_14_02_40_TO_2019_12_16_17_13_09/HV/vMon_"+str(L)+".dat"
	hvvaluescheck, ivalues = processARCO2937(file1, file2, filename)
   
	#ARCO2 93-7 SOURCE AT 10.0
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_16_17_14_32_TO_2019_12_16_18_10_58/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_16_17_14_32_TO_2019_12_16_18_10_58/HV/vMon_"+str(L)+".dat"
	hvvaluescheck2, ivalues2 = processARCO2937(file1, file2, filename+"_att10")
	gain = []
	hvgain = []
	for counter, x in enumerate(hvvaluescheck2):
		hvgain.append(x)
		gain.append(ivalues[counter]/ivalues2[counter])
	write_summarygain(hvgain, gain, "ARCO2937_"+str(filename), filename)

	#ARCO2937 source at 100.0
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_14_20_19_29_TO_2020_01_14_21_15_35/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_14_20_19_29_TO_2020_01_14_21_15_35/HV/vMon_"+str(L)+".dat"
	hvvaluescheck3, ivalues3 = processARCO2937(file1, file2, filename+"_att100")
	gain = []
	hvgain = []
	ivalues2 = ivalues2[3:11]
	hvvaluescheck2 = hvvaluescheck2[3:11]
	for counter, x in enumerate(hvvaluescheck3):
		hvgain.append(x)
		gain.append(ivalues2[counter]/ivalues3[counter])
	write_summarygain(hvgain, gain, "ARCO2037_"+str(filename)+"_2", filename+"_2")
	
'''
for L in layersnosource2:
	print "Current no source "+str(L)
	filename = L

	#ARCO2 80-20 no source
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_10_12_56_27_TO_2019_12_10_15_07_18/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_10_12_56_27_TO_2019_12_10_15_07_18/HV/vMon_"+str(L)+".dat"
	processARCO28020nosource(file1, file2, filename)

	#ISOBUTANE no source
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_12_09_43_04_TO_2019_12_12_11_04_25/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_12_09_43_04_TO_2019_12_12_11_04_25/HV/vMon_"+str(L)+".dat"
	processisobutanenosource(file1, file2, filename)
	
	#ARCO2 93-7 NO SOURCE
	if filename not in ["L1R8", "L2R8", "L4R8"]:
		file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_16_13_03_51_TO_2019_12_16_14_00_09/HV/iMon_"+str(L)+".dat"
		file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_16_13_03_51_TO_2019_12_16_14_00_09/HV/vMon_"+str(L)+".dat"
		processARCO2937nosource(file1, file2, filename)
'''
'''
for L in goodlayers:
	print "HV summary: "+str(L)
	filename = L

	#ARCO2 80-20 source at 2.2
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_10_15_08_22_TO_2019_12_10_18_18_04/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_10_15_08_22_TO_2019_12_10_18_18_04/HV/vMon_"+str(L)+".dat"
	#processARCO28020(file1, file2, filename)
	#processARCO28020spikes(file1, file2, filename)

	#ARCO2 80-20 source at 10.0
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_18_09_08_00_TO_2019_12_18_10_13_44/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_18_09_08_00_TO_2019_12_18_10_13_44/HV/vMon_"+str(L)+".dat"
	#processARCO28020(file1, file2, filename+"_att10")
	#processARCO28020spikes(file1, file2, filename)

	#ISOBUTANE source at 2.2
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_12_11_37_30_TO_2019_12_12_13_04_08/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_12_11_37_30_TO_2019_12_12_13_04_08/HV/vMon_"+str(L)+".dat"
	processisobutane(file1, file2, filename)
	#processisobutanespikes(file1, file2, filename)

	#ISOBUTANE source at 10.0
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_13_09_56_53_TO_2019_12_13_11_09_06/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_13_09_56_53_TO_2019_12_13_11_09_06/HV/vMon_"+str(L)+".dat"
	processisobutane(file1, file2, filename+"_att10")
	
	#ISOBUTANE source at 100.0
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_16_17_50_38_TO_2020_01_16_19_14_20/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_16_17_50_38_TO_2020_01_16_19_14_20/HV/vMon_"+str(L)+".dat"
	processisobutane(file1, file2, filename+"_att100")

	#ISOBUTANE source at 1000.0
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_16_16_21_19_TO_2020_01_16_17_40_30/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_16_16_21_19_TO_2020_01_16_17_40_30/HV/vMon_"+str(L)+".dat"
	#processisobutane(file1, file2, filename+"_att1000")

	#ARCO2 93-7 SOURCE AT 2.2
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_16_14_02_40_TO_2019_12_16_17_13_09/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_16_14_02_40_TO_2019_12_16_17_13_09/HV/vMon_"+str(L)+".dat"
	#processARCO2937(file1, file2, filename)
	#processARCO2937spikes(file1, file2, filename)

	#ARCO2 93-7 SOURCE AT 10.0
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_16_17_14_32_TO_2019_12_16_18_10_58/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_16_17_14_32_TO_2019_12_16_18_10_58/HV/vMon_"+str(L)+".dat"
	processARCO2937(file1, file2, filename+"_att10")

	#ARCO2 93-7 SOURCE AT 100.0
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_14_20_19_29_TO_2020_01_14_21_15_35/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_14_20_19_29_TO_2020_01_14_21_15_35/HV/vMon_"+str(L)+".dat"
	processARCO2937(file1, file2, filename+"_att100")

	#ARCO2 93-7 SOURCE AT 1000.0
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_14_21_18_13_TO_2020_01_14_22_14_11/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_14_21_18_13_TO_2020_01_14_22_14_11/HV/vMon_"+str(L)+".dat"
	#processARCO2937(file1, file2, filename+"_att1000")
'''

'''
for L in layers:
	print "Create plots for: "+str(L)

	#ARCO2 80-20 no source
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_10_12_56_27_TO_2019_12_10_15_07_18/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_10_12_56_27_TO_2019_12_10_15_07_18/HV/vMon_"+str(L)+".dat"
	#ARCO2 80-20 source at 2.2
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_10_15_08_22_TO_2019_12_10_18_18_04/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_10_15_08_22_TO_2019_12_10_18_18_04/HV/vMon_"+str(L)+".dat"
	#ARCO2 80-20 source at 10.0
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_18_09_08_00_TO_2019_12_18_10_13_44/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_18_09_08_00_TO_2019_12_18_10_13_44/HV/vMon_"+str(L)+".dat"

	#ISOBUTANE no source
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_12_09_43_04_TO_2019_12_12_11_04_25/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_12_09_43_04_TO_2019_12_12_11_04_25/HV/vMon_"+str(L)+".dat"
	#ISOBUTANE source at 2.2
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_12_11_37_30_TO_2019_12_12_13_04_08/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_12_11_37_30_TO_2019_12_12_13_04_08/HV/vMon_"+str(L)+".dat"
	#ISOBUTANE source at 10.0
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_13_09_56_53_TO_2019_12_13_11_09_06/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_13_09_56_53_TO_2019_12_13_11_09_06/HV/vMon_"+str(L)+".dat"
	#ISOBUTANE source at 100.0
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_16_17_50_38_TO_2020_01_16_19_14_20/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_16_17_50_38_TO_2020_01_16_19_14_20/HV/vMon_"+str(L)+".dat"
	#ISOBUTANE source at 1000.0
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_16_16_21_19_TO_2020_01_16_17_40_30/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_16_16_21_19_TO_2020_01_16_17_40_30/HV/vMon_"+str(L)+".dat"

	#ARCO2 93-7 NO SOURCE
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_16_13_03_51_TO_2019_12_16_14_00_09/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_16_13_03_51_TO_2019_12_16_14_00_09/HV/vMon_"+str(L)+".dat"
	#ARCO2 93-7 SOURCE AT 2.2
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_16_14_02_40_TO_2019_12_16_17_13_09/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_16_14_02_40_TO_2019_12_16_17_13_09/HV/vMon_"+str(L)+".dat"
	#ARCO2 93-7 SOURCE AT 10.0
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_16_17_14_32_TO_2019_12_16_18_10_58/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_16_17_14_32_TO_2019_12_16_18_10_58/HV/vMon_"+str(L)+".dat"
	#ARCO2 93-7 SOURCE AT 100.0
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_14_20_19_29_TO_2020_01_14_21_15_35/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_14_20_19_29_TO_2020_01_14_21_15_35/HV/vMon_"+str(L)+".dat"
	#ARCO2 93-7 SOURCE AT 1000.0
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_14_21_18_13_TO_2020_01_14_22_14_11/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_14_21_18_13_TO_2020_01_14_22_14_11/HV/vMon_"+str(L)+".dat"

	filename = L
	createplot(file1, file2, filename)
'''