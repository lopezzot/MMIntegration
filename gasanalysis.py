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
twentyfourhlayers = ["L1L8"]
onehourlayers = ["L3L6"]
goodlayers = ["L1L6", "L1R6", "L2L6", "L2R6", "L2R7", "L3L6", "L3R6", "L3L7", "L3R7", "L4L6", "L4L7", "L4R7"] #L1L8 for a PCB type 8 example
goodlayers2 = ["L1R6", "L2L6", "L2R6", "L3L6", "L3R6", "L3L7", "L3R7", "L4L7", "L4R7"]
layersnosource = ["L1L6", "L1R6", "L2L6", "L2R6", "L3L6", "L3R6", "L2R7", "L3L7", "L3R7", "L4L7", "L4R7", "L1L8", "L2L8", "L3L8", "L3R8", "L4L8"]
layersnosource = ["L1L8", "L1R8", "L2L8", "L2R8", "L3L8", "L4R8"]
layersnosource2 = ["L1L8", "L2L8", "L3L8"]

#sectors used in last weeks of february
# [L1L6, L1R6, L1L7, L1L8, L2L6, L2R6, L2R7, L3L6, L3R6, L3L7, L3R7, L3R8, L4L6, L4R6, L4L7, L4R7]

rootfile = TFile("out.root", "RECREATE")

rootfilezoom = TFile("outzoom.root", "RECREATE")

rootfilespikes = TFile("outspikes.root", "RECREATE")

rootfilenosource = TFile("outnosource.root", "RECREATE")

rootfilelinearity = TFile("outlinearity.root", "RECREATE")

rootfilegain = TFile("outgain.root", "RECREATE")

rootfile1h = TFile("out1h.root", "RECREATE")

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

	rootfilezoom.cd()
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
	MyTGraph.SetName(graphtitle)
	MyTGraph.SetTitle(filename)
	YAxis = MyTGraph.GetYaxis()
	YAxis.SetRangeUser(-0.2, 0.2) #-0.2, 0.2
	MyTGraph.Draw("AL")
	c.SaveAs("gaszoom/"+str(filename)+".pdf")
	MyTGraph.Write()

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

def write_rootgraphlinearity(vectorx, vectory, errorvectory, errorvectorx, graphtitle):
	"""Function to perform ROOT graph"""

	rootfilelinearity.cd()

	arrayx = array('d')
	arrayy = array('d')
	arrayerrory = array('d')
	'''
	for e in errorvectory:
		if e < 0.5:
			arrayerrory.append(e)
			if e < 0.2:
				arrayerrory.append(0.2)
		else:
			arrayerrory.append(0.5)
	'''
	for e in errorvectory:
		arrayerrory.append(0.2)

	for x in vectorx:
		arrayx.append(x)

	for y in vectory:
		arrayy.append(y)
		
	#How many graph points
	n = len(vectorx)

	zeros = array('d')
	for i in errorvectorx:
		zeros.append(i/(12.**0.5))

	MyTGraph = TGraphErrors(n, arrayx, arrayy, zeros, arrayerrory)
	
	c = TCanvas()
	Style = gStyle
	Style.SetPadLeftMargin(2.0)
	YAxis = MyTGraph.GetYaxis()
	YAxis.SetRangeUser(-1.5, 15.) #-0.2, 29.
	XAxis = MyTGraph.GetXaxis() #TGraphfasthescin
	XAxis.SetLimits(-1.5,30.0) #0.,50.
	#XAxis.SetLabelOffset(0.025)
	XAxis.SetTitle("Rate (kHz/cm^{2})")
	#MyTGraph.GetXaxis().SetNdivisions(910)
	MyTGraph.SetMarkerStyle(20)
	MyTGraph.SetMarkerSize(0.6)
	MyTGraph.GetYaxis().SetTitle("Current (uA)")
	MyTGraph.GetYaxis().SetTitleOffset(1.)
	#MyTGraph.GetYaxis().SetTitleColor(2)
	MyTGraph.SetLineColor(1)
	MyTGraph.SetLineWidth(1)
	MyTGraph.SetMarkerColor(1)
		
	if "937" in graphtitle:
		MyTGraph.SetMarkerColor(3)
		MyTGraph.SetLineColor(3)
		
	if "iso" in graphtitle:
		MyTGraph.SetMarkerColor(2)
		MyTGraph.SetLineColor(2)	

	if "8020" in graphtitle:
		MyTGraph.SetMarkerColor(4)
		MyTGraph.SetLineColor(4)	

	MyTGraph.SetName(graphtitle)
	MyTGraph.SetTitle(graphtitle)
	f = TF1("f","pol1", 0.0, 25.0)
	f = TF1("f", '[1]*TMath::Log([2]*x+1.)+[3]', 0.0,25.0)
	f.SetParLimits(3,0.0,10.)
	f.SetParLimits(2,0.5,3.)
	f.SetParLimits(1,0.5,20.)
	MyTGraph.Fit(f, "R")
	MyTGraph.GetFunction("f").SetLineWidth(1)
	f2 = TF1("f2","pol1", 0.0, 4.0)
	#f2 = TF1("f2", '[1]*TMath::Log([2]*x+1.)+[3]', 0.84,42.1)
	#f2.SetParLimits(3,0.0,10.)
	#f2.SetParLimits(2,0.5,3.)
	#f2.SetParLimits(1,0.5,20.)
	MyTGraph.Fit(f2, "R")
	MyTGraph.Fit(f, "R")
	#MyTGraph.GetFunction("f2").SetLineColor(1)
	MyTGraph.Draw("AP")
	a = f2.GetParameter(1)
	b = f2.GetParameter(0)
	f3 = TF1("f3", '[0]*x+[1]', 0.0, 25.0)
	f3.SetParameter(0,a)
	f3.SetParameter(1,b)
	f3.SetLineStyle(3)
	f3.SetLineWidth(1)
	f3.SetLineColor(1)
	f3.Draw("same")
	f3.SetName(graphtitle)
	f3.Write()
	c.SaveAs("gaslinearity/"+str(graphtitle)+".pdf")
	MyTGraph.SetName(graphtitle)
	MyTGraph.SetTitle(graphtitle)
	MyTGraph.Write()
	
def write_summaryspikes(vectorx, vectory, graphtitle, filenae):
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

def write_summaryhv(vectorx, vectory, errorvalues, graphtitle, filename):
	"""Function to perform ROOT graph"""
	arrayx = array('d')
	arrayy = array('d')
	arrayy1 = array('d')
	arrayerror = array('d')
	arrayzeros = array('d')

	for x in vectorx:
		arrayx.append(x)

	for y in vectory:
		arrayy.append(y)
	
	for e in errorvalues:
		if e>2.0:
			e=1.5
		arrayerror.append(e)
		arrayzeros.append(0.)	

	#How many graph points
	n = len(vectorx)

	MyTGraph = TGraphErrors(n, arrayx, arrayy, arrayzeros, arrayerror)
	
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
	YAxis.SetRangeUser(-10.0, 50.)
	YAxis.SetTitle("Current (uA)")
	XAxis = MyTGraph.GetXaxis()
	XAxis.SetLimits(420., 690.)
	XAxis.SetTitle("Amplification Voltage (V)")
	XAxis.SetTitleOffset(1.2)
	MyTGraph.SetMarkerStyle(20)
	MyTGraph.SetMarkerSize(1.5)

	if "ARCO28020" in graphtitle and "10.0" in graphtitle:
		MyTGraph.SetMarkerColor(4) #9 color
		MyTGraph.SetLineColor(4)
		#f = TF1("f", "TMath::Exp([2]*x+[3])+[4]", 560., 670.) #old 10.0 reached 700V
		f = TF1("f", "TMath::Exp([0]*x+[1])", 560., 670.) 
		MyTGraph.Fit(f, "R","",570.,620.)
		MyTGraph.GetFunction("f").SetLineColor(4)
		MyTGraph.GetFunction("f").SetLineWidth(1)
		MyTGraph.GetFunction("f").SetRange(560.,670.)
		for counter, x in enumerate(arrayx):
			func = MyTGraph.GetFunction("f")
			y1 = func.Eval(x)
			arrayy1.append(arrayy[counter]/y1)
		MyTGraph2 = TGraph(len(arrayx)-2,arrayx[2:],arrayy1[2:])
		MyTGraph2.SetMarkerColor(4) #9 color
		MyTGraph2.SetLineColor(4)
		
	
	if "ARCO28020" in graphtitle and "2.2" in graphtitle:
		MyTGraph.SetMarkerColor(4)
		MyTGraph.SetLineColor(4)
		#f = TF1("f", "TMath::Exp([2]*x+[3])+[4]", 560., 670.)
		f = TF1("f", "TMath::Exp([0]*x+[1])", 560., 670.) 
		MyTGraph.Fit(f, "R","",570.,620.)
		MyTGraph.GetFunction("f").SetLineColor(4)
		MyTGraph.GetFunction("f").SetLineWidth(1)
		MyTGraph.GetFunction("f").SetRange(560.,670.)
		for counter, x in enumerate(arrayx):
			func = MyTGraph.GetFunction("f")
			y1 = func.Eval(x)
			arrayy1.append(arrayy[counter]/y1)
		MyTGraph2 = TGraph(len(arrayx)-2,arrayx[2:],arrayy1[2:])
		MyTGraph2.SetMarkerColor(4) #9 color
		MyTGraph2.SetLineColor(4)

	if "ARCO28020" in graphtitle and "4.6" in graphtitle:
		MyTGraph.SetMarkerColor(4) #7 color
		MyTGraph.SetLineColor(4)
		#f = TF1("f", "TMath::Exp([2]*x+[3])+[4]", 560., 670.)
		f = TF1("f", "TMath::Exp([0]*x+[1])", 560., 670.)
		MyTGraph.Fit(f, "R","",570.,620.)
		MyTGraph.GetFunction("f").SetLineColor(4)
		MyTGraph.GetFunction("f").SetLineWidth(1)
		MyTGraph.GetFunction("f").SetRange(560.,670.)
		for counter, x in enumerate(arrayx):
			func = MyTGraph.GetFunction("f")
			y1 = func.Eval(x)
			arrayy1.append(arrayy[counter]/y1)
		MyTGraph2 = TGraph(len(arrayx)-2,arrayx[2:],arrayy1[2:])
		MyTGraph2.SetMarkerColor(4) #9 color
		MyTGraph2.SetLineColor(4)
	
	if "ARCO28020" in graphtitle and "46" in graphtitle:
		MyTGraph.SetMarkerColor(4) #38 color
		MyTGraph.SetLineColor(4)
		#f = TF1("f", "TMath::Exp([2]*x+[3])+[4]", 600., 670.)
		f = TF1("f", "TMath::Exp([0]*x+[1])", 600., 670.)
		MyTGraph.Fit(f, "R","",600.,630.)
		MyTGraph.GetFunction("f").SetLineColor(4)
		MyTGraph.GetFunction("f").SetLineWidth(1)
		MyTGraph.GetFunction("f").SetRange(600.,670.)
	
	if "ARCO28020" in graphtitle and "100" in graphtitle:
		MyTGraph.SetMarkerColor(39)
		MyTGraph.SetLineColor(39)
		#f = TF1("f", "TMath::Exp([2]*x+[3])+[4]", 600., 670.)
		f = TF1("f", "TMath::Exp([0]*x+[1])", 660., 670.)
		if "L4L6" in filename:
			f = TF1("f", "TMath::Exp([2]*x+[3])+[4]", 660., 670.)
		#MyTGraph.Fit(f, "R")
		#MyTGraph.GetFunction("f").SetLineColor(39)

	if "ARCO2937" in graphtitle and "10.0" in graphtitle:
		MyTGraph.SetMarkerColor(3) #color 8
		MyTGraph.SetLineColor(3)
		#f = TF1("f", "TMath::Exp([2]*x+[3])+[4]", 490., 590.)
		f = TF1("f", "TMath::Exp([0]*x+[1])", 490., 590.)
		#if "L1L6" in graphtitle or "L3R6" in graphtitle or "L3L6" in graphtitle:
			#f = TF1("f", "[1]*TMath::Exp([2]*x+[3])+[4]", 490., 590.)
		if "L3R6" not in graphtitle and "L3L6" not in graphtitle:
			MyTGraph.Fit(f, "R","",500.,540.)
			if "L1L6" in graphtitle:
				MyTGraph.Fit(f,"R","",510.,540.)
			MyTGraph.GetFunction("f").SetLineColor(3)
			MyTGraph.GetFunction("f").SetRange(490.,590.)
			MyTGraph.GetFunction("f").SetLineWidth(1)
			for counter, x in enumerate(arrayx):
				func = MyTGraph.GetFunction("f")
				y1 = func.Eval(x)
				arrayy1.append(arrayy[counter]/y1)
			MyTGraph2 = TGraph(len(arrayx)-2,arrayx[2:],arrayy1[2:])
			MyTGraph2.SetMarkerColor(3) #9 color
			MyTGraph2.SetLineColor(3)
	
	if "ARCO2937" in graphtitle and "2.2" in graphtitle:
		MyTGraph.SetMarkerColor(3)
		MyTGraph.SetLineColor(3)
		#f = TF1("f", "TMath::Exp([2]*x+[3])+[4]", 490., 590.)
		f = TF1("f", "TMath::Exp([0]*x+[1])", 490., 590.)
		MyTGraph.Fit(f, "R","",500.,540.)
		MyTGraph.GetFunction("f").SetLineColor(3)
		MyTGraph.GetFunction("f").SetLineWidth(1)
		MyTGraph.GetFunction("f").SetRange(490.,590.)
		for counter, x in enumerate(arrayx):
			func = MyTGraph.GetFunction("f")
			y1 = func.Eval(x)
			arrayy1.append(arrayy[counter]/y1)
		MyTGraph2 = TGraph(len(arrayx)-2,arrayx[2:],arrayy1[2:])
		MyTGraph2.SetMarkerColor(3) #9 color
		MyTGraph2.SetLineColor(3)

	if "ARCO2937" in graphtitle and "4.6" in graphtitle:
		MyTGraph.SetMarkerColor(3) #color 29
		MyTGraph.SetLineColor(3)
		#f = TF1("f", "TMath::Exp([2]*x+[3])+[4]", 490., 590.)
		f = TF1("f", "TMath::Exp([0]*x+[1])", 490., 590.)
		MyTGraph.Fit(f, "R","",500.,540.)
		MyTGraph.GetFunction("f").SetLineColor(3)
		MyTGraph.GetFunction("f").SetLineWidth(1)
		MyTGraph.GetFunction("f").SetRange(490.,590.)
		for counter, x in enumerate(arrayx):
			func = MyTGraph.GetFunction("f")
			y1 = func.Eval(x)
			arrayy1.append(arrayy[counter]/y1)
		MyTGraph2 = TGraph(len(arrayx)-2,arrayx[2:],arrayy1[2:])
		MyTGraph2.SetMarkerColor(3) #9 color
		MyTGraph2.SetLineColor(3)

	if "ARCO2937" in graphtitle and "100" in graphtitle:
		MyTGraph.SetMarkerColor(30)
		MyTGraph.SetLineColor(30)
		#f = TF1("f", "[1]*TMath::Exp([2]*x+[3])+[4]", 520., 580.)
		f = TF1("f", "TMath::Exp([0]*x+[1])", 520., 580.)
		if "L3L7" not in graphtitle:
			MyTGraph.Fit(f,"R")
			MyTGraph.GetFunction("f").SetLineColor(30)
			
	if "ARCO2937" in graphtitle and "1000" in graphtitle:
		MyTGraph.SetMarkerColor(32)
		MyTGraph.SetLineColor(32)

	if "ARCO2937" in graphtitle and "46" in graphtitle:
		MyTGraph.SetMarkerColor(3) #color 32
		MyTGraph.SetLineColor(3)
		#f = TF1("f", "[1]*TMath::Exp([2]*x+[3])+[4]", 520., 590.)
		f = TF1("f", "TMath::Exp([0]*x+[1])", 520., 590.)
		MyTGraph.Fit(f,"R","",520.,540.)
		MyTGraph.GetFunction("f").SetLineColor(3)
		MyTGraph.GetFunction("f").SetLineWidth(1)
		MyTGraph.GetFunction("f").SetRange(520.,590.)

	if "ISOBUTANE" in graphtitle and "2.2" in graphtitle:
		MyTGraph.SetMarkerColor(2)
		MyTGraph.SetLineColor(2)	
		#f = TF1("f", "[1]*TMath::Exp([2]*x+[3])+[4]", 440., 540.)
		f = TF1("f", "TMath::Exp([0]*x+[1])", 440., 540.)
		if "L1L6" in filename or "L2R7" in filename:					
			#f = TF1("f", "TMath::Exp([2]*x+[3])+[4]", 440., 540.)
			f = TF1("f", "TMath::Exp([0]*x+[1])", 440., 540.)
		#f.SetParLimits(3,0.0,10.)
		MyTGraph.Fit(f, "R","",450.,490.)
		MyTGraph.GetFunction("f").SetLineColor(2)
		MyTGraph.GetFunction("f").SetLineWidth(1)
		MyTGraph.GetFunction("f").SetRange(440.,540.)
		for counter, x in enumerate(arrayx):
			func = MyTGraph.GetFunction("f")
			y1 = func.Eval(x)
			arrayy1.append(arrayy[counter]/y1)
		MyTGraph2 = TGraph(len(arrayx)-2,arrayx[2:],arrayy1[2:])
		MyTGraph2.SetMarkerColor(2) #9 color
		MyTGraph2.SetLineColor(2)

	if "ISOBUTANE" in graphtitle and "4.6" in graphtitle:
		MyTGraph.SetMarkerColor(2) #color 45
		MyTGraph.SetLineColor(2)	
		#f = TF1("f", "[1]*TMath::Exp([2]*x+[3])+[4]", 440., 540.)
		f = TF1("f", "TMath::Exp([0]*x+[1])", 440., 540.)
		#f.SetParLimits(3,0.0,10.)
		MyTGraph.Fit(f, "R","",450.,490.)
		MyTGraph.GetFunction("f").SetLineColor(2)
		MyTGraph.GetFunction("f").SetLineWidth(1)
		MyTGraph.GetFunction("f").SetRange(440.,540.)
		for counter, x in enumerate(arrayx):
			func = MyTGraph.GetFunction("f")
			y1 = func.Eval(x)
			arrayy1.append(arrayy[counter]/y1)
		MyTGraph2 = TGraph(len(arrayx)-2,arrayx[2:],arrayy1[2:])
		MyTGraph2.SetMarkerColor(2) #9 color
		MyTGraph2.SetLineColor(2)

	if "ISOBUTANE" in graphtitle and "10.0" in graphtitle:
		MyTGraph.SetMarkerColor(2) #color 46
		MyTGraph.SetLineColor(2)
		#f = TF1("f", "[1]*TMath::Exp([2]*x+[3])+[4]", 440., 540.)
		f = TF1("f", "TMath::Exp([0]*x+[1])", 440., 540.)
		if "L1L6" in graphtitle:
			#f = TF1("f", "[1]*TMath::Exp([2]*x+[3])+[4]", 450., 540.)
			f = TF1("f", "TMath::Exp([0]*x+[1])", 450., 540.)
		if "L1R6" in graphtitle:
			#f = TF1("f", "[1]*TMath::Exp([2]*x+[3])+[4]", 450., 540.)
			f = TF1("f", "TMath::Exp([0]*x+[1])", 450., 540.)
		if "L2L6" not in graphtitle:
			MyTGraph.Fit(f, "R","",450,490.)
			MyTGraph.GetFunction("f").SetLineColor(2)
			MyTGraph.GetFunction("f").SetLineWidth(1)			
			MyTGraph.GetFunction("f").SetRange(440.,540.)
			for counter, x in enumerate(arrayx):
				func = MyTGraph.GetFunction("f")
				y1 = func.Eval(x)
				arrayy1.append(arrayy[counter]/y1)
			MyTGraph2 = TGraph(len(arrayx)-2,arrayx[2:],arrayy1[2:])
			MyTGraph2.SetMarkerColor(2) #9 color
			MyTGraph2.SetLineColor(2)

	if "ISOBUTANE" in graphtitle and "100" in graphtitle:
		MyTGraph.SetMarkerColor(50)
		MyTGraph.SetLineColor(50)
		#f = TF1("f", "[1]*TMath::Exp([2]*x+[3])+[4]", 500., 540.)
		f = TF1("f", "TMath::Exp([0]*x+[1])", 500., 540.)
		MyTGraph.Fit(f, "R")
		MyTGraph.GetFunction("f").SetLineColor(50)		
		MyTGraph.GetFunction("f").SetLineWidth(1)

	if "ISOBUTANE" in graphtitle and "46" in graphtitle:
		MyTGraph.SetMarkerColor(2) #color 49
		MyTGraph.SetLineColor(2)
		#f = TF1("f", "[1]*TMath::Exp([2]*x+[3])+[4]", 470., 540.)
		f = TF1("f", "TMath::Exp([0]*x+[1])", 470., 540.)
		if "L1R6" in graphtitle:
			#f = TF1("f", "[1]*TMath::Exp([2]*x+[3])+[4]", 470., 540.)
			f = TF1("f", "TMath::Exp([0]*x+[1])", 470., 540.)
		MyTGraph.Fit(f, "R","",470.,500.)
		MyTGraph.GetFunction("f").SetLineColor(2)
		MyTGraph.GetFunction("f").SetLineWidth(1)
		MyTGraph.GetFunction("f").SetRange(470.,540.)

	rootfile.cd()
	MyTGraph.SetName(graphtitle)
	MyTGraph.SetTitle(filename)
	MyTGraph.Write()
	if "MyTGraph2" in locals():
		YAxis = MyTGraph2.GetYaxis()
		YAxis.SetRangeUser(0.5, 1.2)
		YAxis.SetTitle("Ratio")
		XAxis = MyTGraph2.GetXaxis()
		XAxis.SetLimits(420., 690.)
		XAxis.SetTitle("Amplification Voltage (V)")
		XAxis.SetTitleOffset(1.2)
		MyTGraph2.SetMarkerStyle(20)
		MyTGraph2.SetMarkerSize(1.5)
		MyTGraph2.SetName(graphtitle+"_ratio")
		MyTGraph2.SetTitle(filename+"_ratio")
		MyTGraph2.Write()

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

def process1h(file, file2, filename, gastype):
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

	#print dates2[0:10]
	#print newvalues2[0:10]
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
	
	MyHisto = TH1F("1hhisto-"+str(gastype)+"-"+str(filename), "1hhisto-"+str(gastype)+"-"+str(filename), int(90), -0.1, 0.8)
	MyHistoDiff = TH1F("1hhisto-diff"+str(gastype)+"-"+str(filename), "1hhisto-"+str(gastype)+"-"+str(filename), int(40), -0.2, 0.2)
	
	if "520-iso" in gastype:
		newvalues2 = [int(math.ceil(x * 100.0)) for x in newvalues2]
		#print newvalues2
		t = 15*[c for counter, c in enumerate(newvalues) if newvalues2[counter] == int(520)]
		t_diff = np.diff(t)
		for entry in t:
			#print "520ISO"+str(entry)
			if abs(entry-np.mean(t))<0.004:
				MyHisto.Fill(entry)
		for entry in t_diff:
			MyHistoDiff.Fill(entry)

	if "937" in gastype:
		newvalues_diff = np.diff(newvalues[120:])
		for entry in newvalues[120:]:
			MyHisto.Fill(entry)
		for entry in newvalues_diff:
			MyHistoDiff.Fill(entry)

	if "937" not in gastype and "520-iso" not in gastype:
		newvalues_diff = np.diff(newvalues)
		for entry in newvalues:
			MyHisto.Fill(entry)
		for entry in newvalues_diff:
			MyHistoDiff.Fill(entry)

	rootfile1h.cd()
	integral = MyHisto.Integral()
	MyHisto.Scale(1./integral)
	integral_diff = MyHistoDiff.Integral()
	MyHistoDiff.Scale(1./integral_diff)
	MyHisto.GetYaxis().SetRangeUser(0.0004,0.8)
	MyHisto.Write()
	MyHistoDiff.Write()

def process24h(file, file2, filename, gastype):
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

	#print dates2[0:10]
	#print newvalues2[0:10]
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
	
	MyHisto = TH1F("24hhisto-"+str(gastype)+"-"+str(filename), "24hhisto-"+str(gastype)+"-"+str(filename), int(180), 11., 20.)
	#MyHistoDiff = TH1F("1hhisto-diff"+str(gastype)+"-"+str(filename), "1hhisto-"+str(gastype)+"-"+str(filename), int(100), -0.1, 0.8)
	
	#if "937" in gastype:
		#newvalues = 8*newvalues[120:len(newvalues)-240]

	if "937" in gastype:
		newvalues = newvalues[60*150:len(newvalues)-120]
		newvalues = [x+4.0 for x in newvalues]

	if "8020" in gastype:
		newvalues = newvalues[len(newvalues)/2+(60*60*2):len(newvalues)-120]
		
	for entry in newvalues[60*150:len(newvalues)-120]:
		integral = MyHisto.Integral()
		MyHisto.Fill(entry)
	MyHisto.Scale(1./integral)

	rootfile1h.cd()
	MyHisto.Write()
	#MyHistoDiff.Write()

def processsaturation(file, file2, filename, gastype):
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

	#print dates[0:10]
	#print newvalues[0:10]
	#print dates2[0:10]
	#print newvalues2[0:10]
	
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
	
	filtervalues = [0.0, 10.0, 6.9, 4.6, 2.2, 1.0]
	ivalues = []
	ivalueserror = []

	if "937" in gastype:
		filtervalues = [0.0, 100.0, 46.0, 22.0, 10.0, 4.6, 2.2] #not inclyding filter 1.0

	if "iso" in gastype:
		filtervalues = [0.0, 100.0, 46.0, 22.0, 10.0, 4.6, 2.2] #not inclyding filter 1.0

	if "8020" in gastype:
		filtervalues = [0.0, 100.0, 46.0, 22.0, 10.0, 4.6, 2.2] #not inclyding filter 1.0

	if "L3L7iso-520" in filename or "L3L8iso-520" in filename:
		filtervalues = [0.0, 100.0, 46.0, 22.0, 10.0, 4.6, 2.2] #not inclyding filter 1.0

	for x in filtervalues:	
		f = np.mean([c for counter, c in enumerate(newvalues) if newvalues2[counter] == x])
		e = np.std([c for counter, c in enumerate(newvalues) if newvalues2[counter] == x])
		n = float(len([c for counter, c in enumerate(newvalues) if newvalues2[counter] == x]))
		error = e
		ivalues.append(f)
		ivalueserror.append(error)
		
	
	filtervalues = [1./x for x in filtervalues[1:]]
	if "L1L6" in filename:
		filtervalues = [0.85, 1.7, 3.3, 6.7, 12.7, 23.6] #L1L6
		filtererrors = [0.2, 0.43, 0.8, 1.7, 3.2, 6.0] #L1L6
	if "L3R7" in filename:
		filtervalues = [0.70, 1.5, 3.0, 5.9, 11.4, 21.7] #L3R7
		filtererrors = [0.2, 0.4, 0.7, 1.5, 2.9, 5.5] #L3R7

	#filtervalues = [0.0]+filtervalues
	ivalues = ivalues[1:]
	ivalueserror = ivalueserror[1:]
	#print ivalueserror
	#common part
	write_rootgraphlinearity(filtervalues, ivalues, ivalueserror, filtererrors, filename)


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
	
	if "_2.2" in filename: 			
		newvalues2 = newvalues2[4*60:len(newvalues2)-7*60]
		newvalues = newvalues[4*60:len(newvalues)-7*60] 	

	newvalues2 = [int(math.ceil(x / 10.0)) * 10 for x in newvalues2]

	if "_att2.2" in filename:
		hvvalues = [560, 570, 580, 590, 600, 610, 620, 630, 640, 650, 660, 670] #can go up to 700 V down to 550
	#if "_att10.0" in filename: #for old 10.0
		#hvvalues = [550, 560, 570, 580, 590, 600, 610, 620, 630, 640, 650, 690, 700]
		#if "L1L6" in filename:
		#	hvvalues = [550, 560, 570, 580, 590, 600, 610, 620, 630, 640, 650, 690]
	if "_att10.0" in filename:
		hvvalues = [560, 570, 580, 590, 600, 610, 620, 630, 640, 650, 660, 670] #can go down to 550
	if "_att100" in filename:
		hvvalues = [600, 610, 620, 630, 640, 660, 670] #can go up to 690
	if "_att100" in filename and "L3L6" in filename:
		hvvalues = [600, 620, 630, 640, 660, 670] #can go up to 690
	if "_att100" in filename and "L4L6" in filename:
		hvvalues = [660, 670] #can go up to 690
	if "_att46" in filename:
		hvvalues = [600, 610, 620, 630, 640, 650, 660, 670] #can go up to 700
	if "_att46" in filename and ("L4L7" in filename or "L4R7" in filename):
		hvvalues = [600, 610, 620, 630, 640, 650, 660, 670] #can go up to 700

	if "_att4.6" in filename:
		hvvalues = [560, 570, 580, 590, 600, 610, 620, 630, 640, 650, 660, 670] #can go down to 550

	ivalues = []
	hvvaluescheck = []
	errorvalues = []

	for x in hvvalues:	
		f = np.mean([c for counter, c in enumerate(newvalues) if newvalues2[counter] == x])
		error = 3.0*np.std([c for counter, c in enumerate(newvalues) if newvalues2[counter] == x]) 
		if math.isnan(f) == False:
			ivalues.append(f)
			hvvaluescheck.append(x)
			errorvalues.append(error)

	write_summaryhv(hvvaluescheck, ivalues, errorvalues, "ARCO28020 - "+str(filename), filename)
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

	if "_att2.2" in filename:
		hvvalues = [440, 450, 460, 470, 480, 490, 500, 510, 520, 530, 540] #can go up to 570 and down to 420

	if "_att100" in filename and "_att1000" not in filename:
		hvvalues = [500, 510, 520, 530, 540] #can go up to 560

	#if "_att1000" in filename:
		#hvvalues = [530, 540, 550, 560]

	if "_att46" in filename:
		hvvalues = [470, 480, 490, 500, 510, 520, 530, 540] #can go up to 550 down to 440
		if "L1R6" in filename:
			hvvalues = [470, 480, 490, 500, 510, 520, 530, 540] #can go down to 440

	if "_att10.0" in filename:
		hvvalues = [440, 450, 460, 470, 480, 490, 500, 510, 520, 530, 540] #can go up to 560 down to 430
		if "L1L6" in filename:
			hvvalues = [450, 460, 470, 480, 490, 500, 510, 520, 530, 540] #can go up to 560
		if "L2R7" in filename:
			hvvalues = [450, 460, 470, 480, 490, 500, 510, 520, 530, 540] #can go up to 570

	if "_att4.6" in filename:
		hvvalues = [440,450,460,470,480,490,500,510,520,530,540] #can go down to 430
		if "L2R7" in filename:
			hvvalues = [440,450,460,470,480,490,500,510,520,530] #can go down to 430

	ivalues = []
	hvvaluescheck = []
	errorvalues = []
	for x in hvvalues:	
		f = np.mean([c for counter, c in enumerate(newvalues) if newvalues2[counter] == x])
		e = 3.0*np.std([c for counter, c in enumerate(newvalues) if newvalues2[counter] == x])
		if math.isnan(f) == False:
			ivalues.append(f)
			errorvalues.append(e)
			hvvaluescheck.append(x)

	print hvvaluescheck, ivalues
	write_summaryhv(hvvaluescheck, ivalues, errorvalues, "ISOBUTANE - "+str(filename), filename)
	return hvvaluescheck, ivalues
	
def processisobutanenosource(file, file2, filename):
	#for summary no source
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

	if "46" in filename:
		hvvalues = [520, 530, 540, 550, 560, 570, 580, 590] #can go down to 510

	if "4.6" in filename:
		hvvalues = [490, 500, 510, 520, 530, 540, 550, 560, 570, 580, 590]

	ivalues = []
	hvvaluescheck = []
	errorvalues = []

	for x in hvvalues:	
		f = np.mean([c for counter, c in enumerate(newvalues) if newvalues2[counter] == x])
		error = 3.0*np.std([c for counter, c in enumerate(newvalues) if newvalues2[counter] == x])
		if filename == "L2R7_att100" and x == 580:
			p = [c for counter, c in enumerate(newvalues) if newvalues2[counter] == x]
			f = np.mean(p[:len(p)-7*60]) #remove last 7 minutes
			error = 3.0*np.std(p[:len(p)-7*60])
		if math.isnan(f) == False:
			ivalues.append(f)
			hvvaluescheck.append(x)
			errorvalues.append(error)

	write_summaryhv(hvvaluescheck, ivalues, errorvalues, "ARCO2937 - "+str(filename), filename)
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


'''
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
	#processisobutane(file1, file2, filename)
	processisobutanenosource(file1, file2, filename)
	
	#ARCO2 93-7 NO SOURCE
	if filename not in ["L1R8", "L2R8", "L4R8"]:
		file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_16_13_03_51_TO_2019_12_16_14_00_09/HV/iMon_"+str(L)+".dat"
		file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_16_13_03_51_TO_2019_12_16_14_00_09/HV/vMon_"+str(L)+".dat"
		processARCO2937nosource(file1, file2, filename)
'''
goodlayers = ["L3R7"]
for L in goodlayers:
	print "HV summary: "+str(L)
	filename = L

	#ARCO2 80-20 source at 2.2
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_10_15_08_22_TO_2019_12_10_18_18_04/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_10_15_08_22_TO_2019_12_10_18_18_04/HV/vMon_"+str(L)+".dat"
	processARCO28020(file1, file2, filename+"_att2.2")
	#processARCO28020spikes(file1, file2, filename)

	#ARCO2 80-20 source at 4.6
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_29_12_30_20_TO_2020_02_29_13_23_06/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_29_12_30_20_TO_2020_02_29_13_23_06/HV/vMon_"+str(L)+".dat"
	processARCO28020(file1, file2, filename+"_att4.6")
	#processARCO28020spikes(file1, file2, filename)

	#ARCO2 80-20 source at 10.0 - old
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_18_09_08_00_TO_2019_12_18_10_13_44/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_18_09_08_00_TO_2019_12_18_10_13_44/HV/vMon_"+str(L)+".dat"
	#processARCO28020(file1, file2, filename+"_att10.0")
	#processARCO28020spikes(file1, file2, filename)

	#ARCO2 80-20 source at 10.0 - 2
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_29_13_25_41_TO_2020_02_29_14_18_17/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_29_13_25_41_TO_2020_02_29_14_18_17/HV/vMon_"+str(L)+".dat"
	processARCO28020(file1, file2, filename+"_att10.0")
	#processARCO28020spikes(file1, file2, filename)

	#ARCO2 80-20 source at 46.0
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_23_16_22_34_TO_2020_01_23_17_41_42/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_23_16_22_34_TO_2020_01_23_17_41_42/HV/vMon_"+str(L)+".dat"
	processARCO28020(file1, file2, filename+"_att46")
	
	#ARCO2 80-20 source at 100.0
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_23_14_33_22_TO_2020_01_23_16_03_01/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_23_14_33_22_TO_2020_01_23_16_03_01/HV/vMon_"+str(L)+".dat"
	#processARCO28020(file1, file2, filename+"_att100")

	#ISOBUTANE source at 2.2
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_12_11_37_30_TO_2019_12_12_13_04_08/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_12_11_37_30_TO_2019_12_12_13_04_08/HV/vMon_"+str(L)+".dat"
	processisobutane(file1, file2, filename+"_att2.2")
	#processisobutanespikes(file1, file2, filename)

	#ISOBUTANE source at 4.6
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_07_09_57_19_TO_2020_02_07_11_08_17/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_07_09_57_19_TO_2020_02_07_11_08_17/HV/vMon_"+str(L)+".dat"
	if L != "L3L7":
		processisobutane(file1, file2, filename+"_att4.6")

	#ISOBUTANE source at 10.0 - old
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_13_09_56_53_TO_2019_12_13_11_09_06/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_13_09_56_53_TO_2019_12_13_11_09_06/HV/vMon_"+str(L)+".dat"
	#processisobutane(file1, file2, filename+"_att10")
	
	#ISOBUTANE source at 10.0 - 2
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_30_12_17_51_TO_2020_01_30_13_29_25/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_30_12_17_51_TO_2020_01_30_13_29_25/HV/vMon_"+str(L)+".dat"
	processisobutane(file1, file2, filename+"_att10.0")

	#ISOBUTANE source at 46.0
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_30_11_01_01_TO_2020_01_30_12_06_58/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_30_11_01_01_TO_2020_01_30_12_06_58/HV/vMon_"+str(L)+".dat"
	processisobutane(file1, file2, filename+"_att46")
	
	#ISOBUTANE source at 100.0
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_16_17_50_38_TO_2020_01_16_19_14_20/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_16_17_50_38_TO_2020_01_16_19_14_20/HV/vMon_"+str(L)+".dat"
	#processisobutane(file1, file2, filename+"_att100")

	#ISOBUTANE source at 1000.0
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_16_16_21_19_TO_2020_01_16_17_40_30/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_16_16_21_19_TO_2020_01_16_17_40_30/HV/vMon_"+str(L)+".dat"
	#processisobutane(file1, file2, filename+"_att1000")

	#ARCO2 93-7 SOURCE AT 2.2
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_16_14_02_40_TO_2019_12_16_17_13_09/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_16_14_02_40_TO_2019_12_16_17_13_09/HV/vMon_"+str(L)+".dat"
	#processARCO2937spikes(file1, file2, filename)
	hvvalues, ivalues_2p2 = processARCO2937(file1, file2, filename+"_att2.2")
	if filename == "L3R7":
		rate = 21.7
		error = 6.0
		ivalues_2p2 = [x/rate for x in ivalues_2p2]

	#ARCO2 93-7 SOURCE AT 4.6
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_18_10_33_46_TO_2020_02_18_11_44_48/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_18_10_33_46_TO_2020_02_18_11_44_48/HV/vMon_"+str(L)+".dat"
	hvvalues, ivalues_4p6 = processARCO2937(file1, file2, filename+"_att4.6")
	if filename == "L3R7":
		rate = 11.4
		error = 3.2
		ivalues_4p6 = [x/rate for x in ivalues_4p6]

	#ARCO2 93-7 SOURCE AT 10.0
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_16_17_14_32_TO_2019_12_16_18_10_58/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_16_17_14_32_TO_2019_12_16_18_10_58/HV/vMon_"+str(L)+".dat"
	hvvalues, ivalues_10p0 = processARCO2937(file1, file2, filename+"_att10.0")
	if filename == "L3R7":
		rate = 5.9
		error = 1.7
		ivalues_10p0 = [x/rate for x in ivalues_10p0]

	if filename == "L3R7":
		array520 = array('d')
		array570 = array('d')
		array590 = array('d')
		for counter, x in enumerate(hvvalues):
			if x == 520:
				print "aoooooooooooooooo"
				array520.append(ivalues_10p0[counter])
				array520.append(ivalues_4p6[counter])
				array520.append(ivalues_2p2[counter])
			if x == 570:
				print "aoooooooooooooooo"
				array570.append(ivalues_10p0[counter])
				array570.append(ivalues_4p6[counter])
				array570.append(ivalues_2p2[counter])
			if x == 590:
				print "aoooooooooooooooo"
				array590.append(ivalues_10p0[counter])
				array590.append(ivalues_4p6[counter])
				array590.append(ivalues_2p2[counter])
		print "ciaooooooo", array520, array570, array590
		NewTGraph520 = TGraph(3, array('d',[5.9,11.4,21.7]),array520)
		NewTGraph520.SetTitle("ARCO2937_L3R7_520")
		NewTGraph520.SetName("ARCO2937_L3R7_520")
		NewTGraph520.SetMarkerStyle(20)
		NewTGraph520.SetMarkerSize(1.5)
		NewTGraph570 = TGraph(3, array('d',[5.9,11.4,21.7]),array570)
		NewTGraph570.SetTitle("ARCO2937_L3R7_570")
		NewTGraph570.SetName("ARCO2937_L3R7_570")
		NewTGraph570.SetMarkerStyle(20)
		NewTGraph570.SetMarkerSize(1.5)
		NewTGraph590 = TGraph(3, array('d',[5.9,11.4,21.7]),array590)
		NewTGraph590.SetTitle("ARCO2937_L3R7_590")
		NewTGraph590.SetName("ARCO2937_L3R7_590")
		NewTGraph590.SetMarkerStyle(20)
		NewTGraph590.SetMarkerSize(1.5)
		rootfile.cd()
		NewTGraph520.Write()
		NewTGraph570.Write()
		NewTGraph590.Write()

	#ARCO2 93-7 SOURCE AT 46.0
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_27_19_09_15_TO_2020_01_27_20_05_08/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_27_19_09_15_TO_2020_01_27_20_05_08/HV/vMon_"+str(L)+".dat"
	processARCO2937(file1, file2, filename+"_att46")

	#ARCO2 93-7 SOURCE AT 100.0
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_14_20_19_29_TO_2020_01_14_21_15_35/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_14_20_19_29_TO_2020_01_14_21_15_35/HV/vMon_"+str(L)+".dat"
	#processARCO2937(file1, file2, filename+"_att100")

	#ARCO2 93-7 SOURCE AT 1000.0
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_14_21_18_13_TO_2020_01_14_22_14_11/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_14_21_18_13_TO_2020_01_14_22_14_11/HV/vMon_"+str(L)+".dat"
	#processARCO2937(file1, file2, filename+"_att1000")
'''
for L in layers:
	print "Create plots for: "+str(L)

	#ARCO2 80-20 no source
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_10_12_56_27_TO_2019_12_10_15_07_18/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_10_12_56_27_TO_2019_12_10_15_07_18/HV/vMon_"+str(L)+".dat"
	#ARCO2 80-20 source at 2.2
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_10_15_08_22_TO_2019_12_10_18_18_04/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_10_15_08_22_TO_2019_12_10_18_18_04/HV/vMon_"+str(L)+".dat"
	#ARCO2 80-20 source at 4.6
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_29_12_30_20_TO_2020_02_29_13_23_06/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_29_12_30_20_TO_2020_02_29_13_23_06/HV/vMon_"+str(L)+".dat"
	#ARCO2 80-20 source at 10.0 - old
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_18_09_08_00_TO_2019_12_18_10_13_44/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_18_09_08_00_TO_2019_12_18_10_13_44/HV/vMon_"+str(L)+".dat"
	#ARCO2 80-20 source at 10.0 - 2
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_29_13_25_41_TO_2020_02_29_14_18_17/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_29_13_25_41_TO_2020_02_29_14_18_17/HV/vMon_"+str(L)+".dat"
	#ARCO2 80-20 source at 46.0
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_23_16_22_34_TO_2020_01_23_17_41_42/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_23_16_22_34_TO_2020_01_23_17_41_42/HV/vMon_"+str(L)+".dat"
	#ARCO2 80-20 source at 100.0
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_23_14_33_22_TO_2020_01_23_16_03_01/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_23_14_33_22_TO_2020_01_23_16_03_01/HV/vMon_"+str(L)+".dat"
	#------->SPECIAL RUNS
	#ARCO2 80-20 1 h source off HV=WP+20V = 665 V
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_24_14_43_27_TO_2020_02_24_15_44_15/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_24_14_43_27_TO_2020_02_24_15_44_15/HV/vMon_"+str(L)+".dat"
	#ARCO2 80-20 1 h source off HV=WP 645 V
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_26_11_37_08_TO_2020_02_26_12_37_51/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_26_11_37_08_TO_2020_02_26_12_37_51/HV/vMon_"+str(L)+".dat"
	#ARCO2 80-20 24 hours (23 h) scan at att 1.0 HV=WP-20 = 625 V
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_24_15_50_31_TO_2020_02_25_15_29_45/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_24_15_50_31_TO_2020_02_25_15_29_45/HV/vMon_"+str(L)+".dat"

	#ISOBUTANE no source
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_12_09_43_04_TO_2019_12_12_11_04_25/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_12_09_43_04_TO_2019_12_12_11_04_25/HV/vMon_"+str(L)+".dat"
	#ISOBUTANE no source - 2
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_31_13_15_03_TO_2020_01_31_13_53_26/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_31_13_15_03_TO_2020_01_31_13_53_26/HV/vMon_"+str(L)+".dat"
	#ISOBUTANE source at 2.2
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_12_11_37_30_TO_2019_12_12_13_04_08/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_12_11_37_30_TO_2019_12_12_13_04_08/HV/vMon_"+str(L)+".dat"
	#ISOBUTANE source at 4.6
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_31_14_42_09_TO_2020_01_31_15_41_29/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_31_14_42_09_TO_2020_01_31_15_41_29/HV/vMon_"+str(L)+".dat"
	#ISOBUTANE source at 10.0
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_13_09_56_53_TO_2019_12_13_11_09_06/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_13_09_56_53_TO_2019_12_13_11_09_06/HV/vMon_"+str(L)+".dat"
	#ISOBUTANE source at 10.0 - 2
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_30_12_17_51_TO_2020_01_30_13_29_25/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_30_12_17_51_TO_2020_01_30_13_29_25/HV/vMon_"+str(L)+".dat"
	#ISOBUTANE source at 10.0 - 3
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_31_13_53_45_TO_2020_01_31_14_38_34/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_31_13_53_45_TO_2020_01_31_14_38_34/HV/vMon_"+str(L)+".dat"	
	#ISOBUTANE source at 46.0
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_30_11_01_01_TO_2020_01_30_12_06_58/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_30_11_01_01_TO_2020_01_30_12_06_58/HV/vMon_"+str(L)+".dat"
	#ISOBUTANE source at 100.0
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_16_17_50_38_TO_2020_01_16_19_14_20/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_16_17_50_38_TO_2020_01_16_19_14_20/HV/vMon_"+str(L)+".dat"
	#ISOBUTANE source at 1000.0
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_16_16_21_19_TO_2020_01_16_17_40_30/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_16_16_21_19_TO_2020_01_16_17_40_30/HV/vMon_"+str(L)+".dat"
	#------>SPECIAL RUNS
	#ISOBUTANE long run at 500 V att 1.0
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_01_17_06_33_TO_2020_02_02_13_58_33/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_01_17_06_33_TO_2020_02_02_13_58_33/HV/vMon_"+str(L)+".dat"
	#ISOBUTANE 1 hour source off at 540 V
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_05_11_32_56_TO_2020_02_05_12_34_56/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_05_11_32_56_TO_2020_02_05_12_34_56/HV/vMon_"+str(L)+".dat"
	#ISOBUTANE long term scan from 420V to 520V at filter 4.6
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_07_09_57_19_TO_2020_02_07_11_08_17/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_07_09_57_19_TO_2020_02_07_11_08_17/HV/vMon_"+str(L)+".dat"

	#ARCO2 93-7 NO SOURCE
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_16_13_03_51_TO_2019_12_16_14_00_09/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_16_13_03_51_TO_2019_12_16_14_00_09/HV/vMon_"+str(L)+".dat"
	#ARCO2 93-7 SOURCE AT 2.2
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_16_14_02_40_TO_2019_12_16_17_13_09/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_16_14_02_40_TO_2019_12_16_17_13_09/HV/vMon_"+str(L)+".dat"
	#ARCO2 93-7 SOURCE AT 4.6
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_18_10_33_46_TO_2020_02_18_11_44_48/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_18_10_33_46_TO_2020_02_18_11_44_48/HV/vMon_"+str(L)+".dat"
	#ARCO2 93-7 SOURCE AT 10.0
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_16_17_14_32_TO_2019_12_16_18_10_58/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2019_12_16_17_14_32_TO_2019_12_16_18_10_58/HV/vMon_"+str(L)+".dat"
	#ARCO2 93-7 SOURCE AT 46.0
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_27_19_09_15_TO_2020_01_27_20_05_08/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_27_19_09_15_TO_2020_01_27_20_05_08/HV/vMon_"+str(L)+".dat"	
	#ARCO2 93-7 SOURCE AT 100.0
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_14_20_19_29_TO_2020_01_14_21_15_35/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_14_20_19_29_TO_2020_01_14_21_15_35/HV/vMon_"+str(L)+".dat"
	#ARCO2 93-7 SOURCE AT 1000.0
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_14_21_18_13_TO_2020_01_14_22_14_11/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_14_21_18_13_TO_2020_01_14_22_14_11/HV/vMon_"+str(L)+".dat"
	#----->SPECIAL RUN
	#ARCO2 93-7 source off scan at 570 V
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_12_12_37_01_TO_2020_02_12_15_10_47/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_12_12_37_01_TO_2020_02_12_15_10_47/HV/vMon_"+str(L)+".dat"
	#ARCO2 93-7 source off scan at 590 V
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_14_09_29_33_TO_2020_02_14_10_32_00/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_14_09_29_33_TO_2020_02_14_10_32_00/HV/vMon_"+str(L)+".dat"
	#ARCO2 93-7 source on att 1.0 scan at 550 V 24 hours -> TO BE CHECKED CURRENTS ARE TOO LOW POSSIBLE CONTAMINATION WITH ARCO28020
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_21_13_12_47_TO_2020_02_22_13_51_46//HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_21_13_12_47_TO_2020_02_22_13_51_46//HV/vMon_"+str(L)+".dat"
	#ARCO2 93-7 source on att 1.0 hv = 570 V -> TO CHECK ARCO2 937 WAS FLUSHING INSIDE THE CHAMBER
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_03_04_00_53_55_TO_2020_03_04_10_00_30/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_03_04_00_53_55_TO_2020_03_04_10_00_30/HV/vMon_"+str(L)+".dat"
	#ARCO2 93-7 source off scan at 570 V 1 h
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_03_04_10_39_48_TO_2020_03_04_11_36_57/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_03_04_10_39_48_TO_2020_03_04_11_36_57/HV/vMon_"+str(L)+".dat"
	#ARCO2 93-7 source off scan at 590 V 1 h
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_03_04_11_38_17_TO_2020_03_04_12_30_04/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_03_04_11_38_17_TO_2020_03_04_12_30_04/HV/vMon_"+str(L)+".dat"
	#ARCO2 93-7 source on filter 1 scan at 550 V -> only 2.5 hours of good data then trip due to main frame power cut
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_03_05_09_13_58_TO_2020_03_05_11_54_00/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_03_05_09_13_58_TO_2020_03_05_11_54_00/HV/vMon_"+str(L)+".dat"
	#ARCO2 93-7 source on filter 1 scan at 550 V -> only 2.5 hours, not checked, data still to be produced in case needed
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_03_05_11_54_24_TO_2020_03_05_14_34_52/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_03_05_11_54_24_TO_2020_03_05_14_34_52/HV/vMon_"+str(L)+".dat"

	filename = L
	#createplot(file1, file2, filename)
'''
'''
for L in layers:
	print "Create plots for: "+str(L)
	filename = L

	#ARCO2 80-20 - old, deprecated
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_24_10_22_02_TO_2020_01_24_12_10_00/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_24_10_22_02_TO_2020_01_24_12_10_00/GIF/EffectiveAttenuation.dat"
	#processsaturation(file1, file2, filename, "8020")
	
	#ARCO2 80-20 at 645 V
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_24_12_50_11_TO_2020_02_24_14_40_07/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_24_12_50_11_TO_2020_02_24_14_40_07/GIF/EffectiveAttenuation.dat"
	processsaturation(file1, file2, filename+"8020-645", "8020")
	createplot(file1, file2, filename)

	#ARCO2 80-20 at 625 V
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_29_10_41_04_TO_2020_02_29_12_27_40/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_29_10_41_04_TO_2020_02_29_12_27_40/GIF/EffectiveAttenuation.dat"
	processsaturation(file1, file2, filename+"8020-625", "8020")
	#createplot(file1, file2, filename)

	#ARCO2 93-7 at 570V
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_28_10_41_02_TO_2020_01_28_12_38_20/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_28_10_41_02_TO_2020_01_28_12_38_20/GIF/EffectiveAttenuation.dat"	
	processsaturation(file1, file2, filename+"937-570", "937")
	#createplot(file1, file2, filename)

	#ARCO2 93-7 at 550V
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_28_17_24_13_TO_2020_01_28_19_23_20/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_28_17_24_13_TO_2020_01_28_19_23_20/GIF/EffectiveAttenuation.dat"	
	processsaturation(file1, file2, filename+"937-550", "937")
	#createplot(file1, file2, filename)

	#ISOBUTANE at 500V
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_04_14_56_40_TO_2020_02_04_16_48_41/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_04_14_56_40_TO_2020_02_04_16_48_41/GIF/EffectiveAttenuation.dat"	
	processsaturation(file1, file2, filename+"iso-500", "iso")
	#createplot(file1, file2, filename)

	#ISOBUTANE at 520V
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_06_11_09_50_TO_2020_02_06_13_18_41/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_06_11_09_50_TO_2020_02_06_13_18_41/GIF/EffectiveAttenuation.dat"	
	processsaturation(file1, file2, filename+"iso-520", "iso")
	#createplot(file1, file2, filename)
'''
'''
for L in onehourlayers:
	#1h source off data analysis
	filename = L

	#ARCO2 80-20 1 h source off HV=WP+20V = 665 V
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_24_14_43_27_TO_2020_02_24_15_44_15/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_24_14_43_27_TO_2020_02_24_15_44_15/HV/vMon_"+str(L)+".dat"
	process1h(file1, file2, filename, "665-8020")
	#createplot(file1, file2, filename)
	#ARCO2 80-20 1 h source off HV=WP 645 V
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_26_11_37_08_TO_2020_02_26_12_37_51/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_26_11_37_08_TO_2020_02_26_12_37_51/HV/vMon_"+str(L)+".dat"
	process1h(file1, file2, filename, "645-8020")
	#createplot(file1, file2, filename)
	
	#ISOBUTANE 1 h source off at 520
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_31_13_15_03_TO_2020_01_31_13_53_26/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_01_31_13_15_03_TO_2020_01_31_13_53_26/HV/vMon_"+str(L)+".dat"
	process1h(file1, file2, filename, "520-iso")
	#createplot(file1, file2, filename)
	#ISOBUTANE 1 hour source off at 540 V
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_05_11_32_56_TO_2020_02_05_12_34_56/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_05_11_32_56_TO_2020_02_05_12_34_56/HV/vMon_"+str(L)+".dat"
	process1h(file1, file2, filename, "540-iso")
	#createplot(file1, file2, filename)
	
	#ARCO2 93-7 source off scan at 570 V
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_03_04_10_39_48_TO_2020_03_04_11_36_57/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_03_04_10_39_48_TO_2020_03_04_11_36_57/HV/vMon_"+str(L)+".dat"
	process1h(file1, file2, filename, "570-937")
	#createplot(file1, file2, filename)
	#ARCO2 93-7 source off scan at 590 V
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_03_04_11_38_17_TO_2020_03_04_12_30_04/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_03_04_11_38_17_TO_2020_03_04_12_30_04/HV/vMon_"+str(L)+".dat"
	process1h(file1, file2, filename, "590-937")
	#createplot(file1, file2, filename)
'''
'''	
for L in twentyfourhlayers:
	#long scan source on
	filename = L
	print L

	#ARCO2 80-20 24 hours (23 h) scan at att 1.0 HV=WP-20 = 625 V
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_24_15_50_31_TO_2020_02_25_15_29_45/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_24_15_50_31_TO_2020_02_25_15_29_45/HV/vMon_"+str(L)+".dat"
	process24h(file1, file2, filename, "625-8020")

	#ISOBUTANE long run at 500 V att 1.0
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_01_17_06_33_TO_2020_02_02_13_58_33/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_01_17_06_33_TO_2020_02_02_13_58_33/HV/vMon_"+str(L)+".dat"
	process24h(file1, file2, filename, "500-iso")

	#ARCO2 93-7 2.5 hourse at 550V att 1.0
	#file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_03_05_09_13_58_TO_2020_03_05_11_54_00/HV/iMon_"+str(L)+".dat"
	#file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_03_05_09_13_58_TO_2020_03_05_11_54_00/HV/vMon_"+str(L)+".dat"
	#process24h(file1, file2, filename, "550-937")

	#ARCO2 93-7 2.5 hourse at 550V att 1.0
	file1 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_21_13_12_47_TO_2020_02_22_13_51_46/HV/iMon_"+str(L)+".dat"
	file2 = "/Users/lorenzo/DataGif/LM2_20MNMMML200007_FROM_2020_02_21_13_12_47_TO_2020_02_22_13_51_46/HV/vMon_"+str(L)+".dat"
	process24h(file1, file2, filename, "550-937")
'''