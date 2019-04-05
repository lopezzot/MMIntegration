import os
import MMPlots
import MMPlots_attenuation

todo = raw_input("MMPlots, MMPlots_attenuation or pdf? ")

if todo == "pdf":
	os.system("python produce_pdf.py")

if todo == "MMPlots":
	MMPlots.createsummaryplots()

if todo == "MMPlots_attenuation":
	MMPlots_attenuation.createsummaryplot_attenuation()

os.system("rm -rf /Users/lorenzo/cernbox/work/Git-to-Mac/MMAnalysis/MMIntegration/GIF*")
os.system("rm -rf /Users/lorenzo/cernbox/work/Git-to-Mac/MMAnalysis/MMIntegration/iMon*")
os.system("rm -rf /Users/lorenzo/cernbox/work/Git-to-Mac/MMAnalysis/MMIntegration/BB5*")