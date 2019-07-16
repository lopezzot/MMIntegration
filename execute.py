import os
import MMPlots
import MMPlots_attenuation

todo = raw_input("MMPlots, MMPlots_attenuation, pdf or DoubleWedgepdf? ")

if todo == "pdf":
	ask = raw_input("BB5, GIF or both? ")
	if ask == "both":
		os.system("python produce_pdf.py")
	if ask == "BB5":
		os.system("python produce_pdf_bb5.py")
	if ask == "GIF":
		os.system("python produce_pdf_gif.py")

if todo == "DoubleWedgepdf":
	os.system("python produce_pdf_dw.py")

if todo == "MMPlots":
	MMPlots.createsummaryplots()

if todo == "MMPlots_attenuation":
	MMPlots_attenuation.createsummaryplot_attenuation()

os.system("rm -rf /Users/lorenzo/cernbox/work/Git-to-Mac/MMAnalysis/MMIntegration/GIF*")
os.system("rm -rf /Users/lorenzo/cernbox/work/Git-to-Mac/MMAnalysis/MMIntegration/iMon*")
os.system("rm -rf /Users/lorenzo/cernbox/work/Git-to-Mac/MMAnalysis/MMIntegration/BB5*")