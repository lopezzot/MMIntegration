from datetime import datetime as dt
from datetime import timedelta as td
import sys
import os
import tools
from ROOT import TFile, TDatime, TDirectory, gSystem, TTree
import glob
import numpy as np
import search
import copy
import classes
from array import array
import efficiency
#---------------------------------------------------------------------------------
def createsummaryplots(path=None, folder=None):
    if path == None:
        house = raw_input("Data in bb5 or Gif? ")
        folder = raw_input("Insert folder to study: ")
        user = raw_input("Who is it? (type Lorenzo, Natalia or bb5) ")
        if user == "Lorenzo":
            path = "/Users/lorenzo/Data_"+str(house)+"/"+folder+"/HV/"#Changed folder: files in Data_bb5 were in DataBB5 2/5/2019
        elif user == "Natalia":
            path = "/home/est/Escritorio/CERN/Data_"+str(house)+"/"+folder+"/HV/"
        elif user == "bb5":
            path = "bb5 path"
        else:
            print "Name not found"

    ID = folder[0:18]
    timeslot = folder[19:len(folder)]
    #rootfile = TFile("/Users/lorenzo/Desktop/MMresults/"+folder+".root","RECREATE")
    rootfile = TFile(folder+".root","RECREATE") #create root file in same directory as pdf
    dir_L1 = rootfile.mkdir("Layer1/")
    dir_L2 = rootfile.mkdir("Layer2/")
    dir_L3 = rootfile.mkdir("Layer3/")
    dir_L4 = rootfile.mkdir("Layer4/")
    dir_summary = rootfile.mkdir("Summary/")

    global directories
    directories = {"L1":dir_L1,"L2":dir_L2,"L3":dir_L3,"L4":dir_L4}
    chambertype = folder[0:3]
    defaultlayersSM1 = ["L1L1","L1R1","L1L2","L1R2","L1L3","L1R3","L1L4","L1R4","L1L5","L1R5","L2L1","L2R1","L2L2","L2R2","L2L3","L2R3","L2L4","L2R4","L2L5","L2R5","L3L1","L3R1","L3L2","L3R2","L3L3","L3R3","L3L4","L3R4","L3L5","L3R5","L4L1","L4R1","L4L2","L4R2","L4L3","L4R3","L4L4","L4R4","L4L5","L4R5"]
    defaultlayersSM2 = ["L1L6","L1R6","L1L7","L1R7","L1L8","L1R8","L2L6","L2R6","L2L7","L2R7","L2L8","L2R8","L3L6","L3R6","L3L7","L3R7","L3L8","L3R8","L4L6","L4R6","L4L7","L4R7","L4L8","L4R8"]

    if chambertype == "SM1":
        defaultlayers = defaultlayersSM1
    if chambertype == "SM2":
        defaultlayers = defaultlayersSM2
    if chambertype == "LM1":
        defaultlayers = defaultlayersSM1
    if chambertype == "LM2":
        defaultlayers = defaultlayersSM2

    #for summary plots
    spikenames = []
    sectorscurrents = []
    sectorsvoltages = []
    meancurrents = []
    meanvoltages = []
    newspikeseconds = []
    graphscurrent = []

    for dat_file in glob.iglob(path+'*.dat'):
        print "Analyzing: "+dat_file[len(path):len(dat_file)]+" \n"
        filename = dat_file[len(path):len(dat_file)-4]
        layer = filename[5:7]
        rootdirectory = directories[layer]
        graphcurrent, spikeslayer, duration, sectorsvoltage, meanvoltage, sectorscurrent, meancurrent, spikeseconds = createplot(dat_file, dat_file[len(path):len(dat_file)-4])

        if spikeseconds != None:
        	newspikeseconds = newspikeseconds + spikeseconds
        if spikeslayer != None:
        	spikenames = spikenames + spikeslayer
        if duration != None:
        	deltatime = duration
        if sectorscurrent != None:
        	sectorscurrents.append(sectorscurrent)
        if meancurrent != None:
        	meancurrents.append(meancurrent)
        if sectorsvoltage != None:
        	sectorsvoltages.append(sectorsvoltage)
        if meanvoltage != None:
        	meanvoltages.append(meanvoltage)
        if graphcurrent != None:
        	graphscurrent.append(graphcurrent)

    #tools.write_roothistogram(newspikeseconds, "Spike time distribution", "t (s)", "Entries", dir_summary)
    tools.write_rootgraph(range(len(meancurrents)),meancurrents,"i "+str(round(float(deltatime)/float(3600),2))+" hours","sector","i", sectorscurrents, dir_summary)
    tools.write_rootgraph(range(len(meanvoltages)),meanvoltages,"HV "+str(round(float(deltatime)/float(3600),2))+" hours","sector","v",sectorsvoltages, dir_summary)
    tools.write_spikeroothistogram(spikenames, "spikes", "spikes/min", dir_summary, deltatime)

    vectorspikes = [x[5:len(x)] for x in spikenames]
    spikerate = []
    spikelayers = list(set(vectorspikes))
    for i in spikelayers:
    	spikerate.append(vectorspikes.count(i))

    for sector in sectorsvoltages:
    	if sector not in spikelayers:
    		spikelayers.append(sector)
    		spikerate.append(0)

    orderedspikerate = []
    for sector in sectorsvoltages:
    	orderedspikerate.append(spikerate[spikelayers.index(sector)])

    orderedspikerate = [float(x/float((deltatime/60.))) for x in orderedspikerate]

    orderedsectorsvoltages = []
    orderedsmeanvoltages = []
    ordered_orderedspikerate = []
    ordered_graphscurrent = []


    for layer in defaultlayers: #put in order voltages
        index = sectorsvoltages.index(layer)
        orderedsectorsvoltages.append(sectorsvoltages[index])
        orderedsmeanvoltages.append(meanvoltages[index])
        ordered_orderedspikerate.append(orderedspikerate[index])

    graph_current_names = []
    for graph in graphscurrent:
    	graph_current_names.append(graph.name)
    for layer in defaultlayers:
    	index = graph_current_names.index(layer)
    	ordered_graphscurrent.append(graphscurrent[index])

    for counter, graph in enumerate(ordered_graphscurrent):                       #+" "+str(int(orderedsmeanvoltages[counter]))#
    	tools.write_orderedrootdategraph(graph.rootdates, graph.newvalues, graph.filename+" "+str(int(orderedsmeanvoltages[counter])), "time (s)", graph.filename[0], rootdirectory)

    #create trees for current values
    for counter, graph in enumerate(ordered_graphscurrent):
    	tree = TTree(ordered_graphscurrent[counter].filename, "tree")
    	newvalue = array( 'f', [ 0 ] )
    	branch = tree.Branch(ordered_graphscurrent[counter].filename, newvalue, "newvalue/F")
    	for i in range(len(graph.newvalues)):
    		newvalue[0] = ordered_graphscurrent[counter].newvalues[i]
    		tree.Fill()
    	tree.Write()

    eff, layers_eff, total_eff = efficiency.efficiency_values(orderedsmeanvoltages, chambertype)

    return orderedsectorsvoltages, orderedsmeanvoltages, ordered_orderedspikerate, ID, timeslot, deltatime, eff, layers_eff, total_eff
    #----------------------------------------------------------------------------------------

    #----------------------------------------------------------------------------------------
def createplot(file, filename):

    layer = filename[5:7]
    rootdirectory = directories[layer] #to check


    times = [x.split(' 	 ')[0] for x in open(file,"r").readlines()]
    if len(times) == 1:
    	print "Exception -----> Only one data in "+str(filename)+".dat \n"
    	return None, None, None, None, None, None, None, None
    if not times:
    	print "Exception -----> File empty: "+str(filename)+".dat \n"
    	return None, None, None, None, None, None, None, None

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

    #Identify drops
    valuesdeltas = np.diff(newvalues)
    valuesdeltas = [0]+valuesdeltas

    sectorscurrent = None
    sectorsvoltage = None
    meancurrent = None
    nospike_meancurrent = None
    meanvoltage = None
    notrips_meanvoltage = None

    if "i" in filename: #it's a current file
    	#search.findrisingedges(valuesdeltas, dates)
    	#search.findfallingedges(valuesdeltas, dates)

    	sectorscurrent = filename[5:9]
    	meancurrent = np.mean(newvalues)

    	#remove spikes in current files
    	copynewvalues = copy.copy(newvalues) #need to copy it to pass to function below
    	nospike_newvalues = search.removespikes(valuesdeltas, copynewvalues)
    	nospike_meancurrent = np.mean(nospike_newvalues) #used to have real baseline of the current
    																									#or meancurrent
    	spikecounter, filename, spikedates, spikeseconds, spikenames = search.findspikes_50na(newvalues, meancurrent, dates, newtimes, filename)
    	#spikecounter, filename, spikedates, spikeseconds, spikenames = search.findspikes(valuesdeltas, dates, newtimes, filename) #old one

    	if "D" in filename:
    		sectorscurrent = None
    		nospike_meancurrent = None

    if "v" in filename: #it's a voltage file
    	sectorsvoltage = filename[5:9]
    	meanvoltage = np.mean(newvalues)

    	copynewvalues = copy.copy(newvalues)
    	notrips_newvalues = search.removetrips(valuesdeltas, copynewvalues)
    	notrips_meanvoltage = np.mean(notrips_newvalues)

    	if "D" in filename:
    		sectorsvoltage = None
    		notrips_meanvoltage = None

    #tools.write_roothistogram(newvalues, filename, filename[0], "Entries", rootdirectory) #if want additional histograms
    tools.write_rootdategraph(rootdates, newvalues, filename, "time (s)", filename[0], rootdirectory)
    currentgraph = classes.currentgraph(filename[5:9], rootdates, newvalues, filename, "time (s)", filename[0], rootdirectory)

    #create trees for voltages branch
    if "v" in filename:
    	tree = TTree(filename, "tree")
    	newvalue = array( 'f', [ 0 ] )
    	branch = tree.Branch(filename, newvalue, "newvalue/F")
    	for i in range(len(newvalues)):
    		newvalue[0] = newvalues[i]
    		tree.Fill()
    	tree.Write()

    duration = len(newtimes) #total seconds from start to stop

    if "i" not in filename or "D" in filename:
    	spikenames = None
    	duration = None
    	spikeseconds = None
    	currentgraph = None

    return currentgraph, spikenames, duration, sectorsvoltage, notrips_meanvoltage, sectorscurrent, nospike_meancurrent, spikeseconds
    #----------------------------------------------------------------------------------------

    #createsummaryplots()
