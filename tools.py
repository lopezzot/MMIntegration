from ROOT import TH1F, gStyle, gPad, TGraph, TCanvas, TDatime
import numpy as np
from array import array

def draw_roothistogram(vector, histogramtitle, xtitle, ytitle, histogramname):
	"""Function to perform ROOT histograms"""

	if xtitle == "i":
		xtitle = xtitle+" (uA)"
		nbin = 100

	if xtitle == "v":
		xtitle = xtitle+" (V)"
		nbin = 20

	rms = 0
	
	#Set ROOT histograms
	TH1Hist = TH1F(histogramtitle,"",int(nbin),np.min(vector)-abs(np.min(vector)-np.mean(vector)), np.max(vector)+abs(np.max(vector)-np.mean(vector)))
	
	#Fill histograms in for loop
	for entry in range(len(vector)):
		TH1Hist.Fill(vector[entry])

	#Draw + DrawOptions histograms	
	c = TCanvas()	
	Style = gStyle
	Style.SetLineWidth(1) #TH1Hist
	Style.SetOptStat(1) #Show statistics
	if xtitle == "i":
		TH1Hist.SetMarkerColor(kRed)
	elif xtitle == "v":
		TH1Hist.SetMarkerColor(kBlue)
	XAxis = TH1Hist.GetXaxis()
	XAxis.SetTitle(xtitle)
	YAxis = TH1Hist.GetYaxis()
	YAxis.SetTitle(ytitle)
	TH1Hist.Draw()
	mean = TH1Hist.GetMean()
	rms = TH1Hist.GetRMS()
	Entries = TH1Hist.GetEntries()
	TH1Hist.Write(histogramname)
	#gPad.SaveAs(histogramname)
	#gPad.Close()

def draw_rootgraph(vectorx, vectory, graphtitle, xtitle, ytitle, graphname):
	"""Function to perform ROOT graph"""

	arrayx = array('d')
	arrayy = array('d')

	for x in vectorx:
		arrayx.append(x.Convert())

	for y in vectory:
		arrayy.append(y)

	print len(arrayx), len(arrayy)
	print arrayx

	if ytitle == "i":
		ytitle = ytitle+" (uA)"
		color = 2
		offset = 1.

	if ytitle == "v":
		ytitle = ytitle+" (V)"
		color = 3
		offset = 0.5

	#How many graph points
	n = len(vectorx)

	MyTGraph = TGraph(n, arrayx, arrayy)
	
	#Draw + DrawOptions
	c = TCanvas()
	Style = gStyle
	Style.SetPadLeftMargin(2.0)
	XAxis = MyTGraph.GetXaxis() #TGraphfasthescin
	XAxis.SetTimeDisplay(1)
 	XAxis.SetTimeFormat("#splitline{%H/%M}{%d:%m}")
 	Xaxis.SetLabelOffset(0.025)
	MyTGraph.SetMarkerColor(color)
	MyTGraph.SetMarkerStyle(1)
	MyTGraph.SetMarkerSize(1)
	MyTGraph.SetTitle(graphtitle)
	#XAxis.SetTitle(xtitle)
	YAxis = MyTGraph.GetYaxis()
	YAxis.SetTitleOffset(offset)
	YAxis.SetTitleOffset(offset)
	YAxis.SetTitle(ytitle)
	MyTGraph.Write(graphname)
	#MyTGraph.Draw("AP")
	#gPad.SaveAs(graphname)
	#gPad.Close()
	






