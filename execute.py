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

