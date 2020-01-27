import os
import MMPlots
import MMPlots_attenuation
import MMPlotsDW

todo = raw_input("MMPlots, MMPlots_attenuation, pdf or DoubleWedgepdf, DWData? ")

if todo == "pdf":
	ask = raw_input("BB5, GIF or both, dwdata? ")
	if ask == "both":
		os.system("python produce_pdf.py")
	if ask == "BB5":
		os.system("python produce_pdf_bb5.py")
	if ask == "GIF":
		os.system("python produce_pdf_gif.py")
	if ask == "dwdata":
		os.system("python produce_pdf_dwdata.py")

if todo == "DoubleWedgepdf":
	os.system("python produce_pdf_dw.py")

if todo == "MMPlots":
	MMPlots.createsummaryplots()

if todo == "MMPlots_attenuation":
	MMPlots_attenuation.createsummaryplot_attenuation()

if todo == "DWData":
	MMPlotsDW.createsummaryplots()

os.system("rm -rf /Users/lorenzo/cernbox/work/Git-to-Mac/MMAnalysis/MMIntegration/GIF*")
os.system("rm -rf /Users/lorenzo/cernbox/work/Git-to-Mac/MMAnalysis/MMIntegration/Overimposed*")
os.system("rm -rf /Users/lorenzo/cernbox/work/Git-to-Mac/MMAnalysis/MMIntegration/iMon*")
os.system("rm -rf /Users/lorenzo/cernbox/work/Git-to-Mac/MMAnalysis/MMIntegration/BB5*")