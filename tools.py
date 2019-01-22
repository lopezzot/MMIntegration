from ROOT import TH1F, gStyle, gPad, TGraph, TCanvas
import numpy as np
from array import array

def draw_roothistogram(vector, histogramtitle, xtitle, ytitle, histogramname):
	"""Function to perform ROOT histograms"""

	if xtitle == "i":
		xtitle = xtitle+" (uA)"


	if xtitle == "v":
		xtitle = xtitle+" (V)"

	rms = 0
	
	#Set ROOT histograms
	TH1Hist = TH1F(histogramtitle,"",int(300*abs((np.min(vector)-np.mean(vector))-(np.max(vector)+np.mean(vector)))),np.min(vector)-np.mean(vector), np.max(vector)+np.mean(vector))

	#Fill histograms in for loop
	for entry in range(len(vector)):
		TH1Hist.Fill(vector[entry])

	#Draw + DrawOptions histograms	
	c = TCanvas()	
	Style = gStyle
	Style.SetLineWidth(1) #TH1Hist
	Style.SetOptStat(1) #Show statistics
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
		arrayx.append(x)

	for y in vectory:
		arrayy.append(y)

	print type(arrayy)

	if ytitle == "i":
		ytitle = ytitle+" (mA)"

	if ytitle == "v":
		ytitle = ytitle+" (V)"

	#How many graph points
	n = len(vectorx)

	MyTGraph = TGraph(n, arrayx, arrayy)
	
	#Draw + DrawOptions
	c = TCanvas()
	Style = gStyle
	Style.SetPadLeftMargin(2.0)
	XAxis = MyTGraph.GetXaxis() #TGraphfasthescin
	MyTGraph.SetMarkerColor(4)
	MyTGraph.SetMarkerStyle(1)
	MyTGraph.SetMarkerSize(1)
	MyTGraph.SetTitle(graphtitle)
	XAxis.SetTitle(xtitle)
	YAxis = MyTGraph.GetYaxis()
	YAxis.SetTitleOffset(1)
	YAxis.SetTitle(ytitle)
	MyTGraph.Write(graphname)
	#MyTGraph.Draw("AP")
	#gPad.SaveAs(graphname)
	#gPad.Close()
	






