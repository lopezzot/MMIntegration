from ROOT import gROOT, TH1, TH1F, gStyle, gPad, TGraph, TCanvas, TDatime, TMultiGraph, TLine
import numpy as np
from array import array

def write_roothistogram(vector, histogramtitle, xtitle, ytitle, rootdirectory):
	"""Function to perform ROOT histograms"""

	if xtitle == "i":
		xtitle = xtitle+" (uA)"
		nbin = 100

	if xtitle == "v":
		xtitle = xtitle+" (V)"
		nbin = 20

	rms = 0
	
	#Set ROOT histograms
	TH1Hist = TH1F(histogramtitle,"",int(nbin),np.min(vector)-1.5*abs(np.max(vector)-np.min(vector)), np.max(vector)+1.5*(np.max(vector)-np.min(vector)))
	
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
	mean = TH1Hist.GetMean()
	rms = TH1Hist.GetRMS()
	Entries = TH1Hist.GetEntries()
	rootdirectory.WriteTObject(TH1Hist)
	#TH1Hist.Write(histogramname)
	#gPad.SaveAs(histogramname)
	#gPad.Close()

def write_spikeroothistogram(vectorspikes, histogramtitle, ytitle, rootdirectory, deltatime):
	"""Function to perform ROOT histograms"""

	#Set ROOT histograms
	TH1Hist = TH1F(histogramtitle,"",3,0,3)
	
	vectorspikes = [x[5:len(x)] for x in vectorspikes]
	
	#Fill histograms in for loop
	for entry in range(len(vectorspikes)):
		TH1Hist.Fill(vectorspikes[entry],1./(deltatime/60))
		
	#Draw + DrawOptions histograms	
	c = TCanvas()	
	Style = gStyle
	Style.SetLineWidth(1) #TH1Hist
	Style.SetOptStat(0) #Show statistics
	gROOT.ForceStyle()
	TH1Hist.SetCanExtend(TH1.kAllAxes)
	TH1Hist.SetFillColor(38)
	TH1Hist.LabelsDeflate()
	TH1Hist.SetMinimum(0)
	TH1Hist.SetMaximum(2)
	YAxis = TH1Hist.GetYaxis()
	YAxis.SetTitle(ytitle)
	TH1Hist.Draw("histo")
	rootdirectory.WriteTObject(TH1Hist)
	#TH1Hist.Write(histogramname)
	#gPad.SaveAs(histogramname)
	#gPad.Close()


def write_rootgraph(vectorx, vectory, graphtitle, xtitle, ytitle, rootdirectory):
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

	if ytitle == "v":
		ytitle = ytitle+" (V)"
		color = 4
		offset = 0.9
		minimum = 400
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
	MyTGraph.Draw("APL")
	rootdirectory.WriteTObject(MyTGraph)
	#MyTGraph.Write(graphname)
	#MyTGraph.Draw("AP")
	#gPad.SaveAs(graphname)
	gPad.Close()