import numpy as np

def findrisingedges(valuesdeltas, dates):
	mycounterrising = 0
	for counter, x in enumerate(valuesdeltas):
		if np.sum(valuesdeltas[counter:counter+30]) > 0.035 and counter-mycounterrising>120:
			if np.sum(valuesdeltas[counter+10:counter+30+10]) > 0.035:
				mycounterrising = counter
				print "---> one rising edge at "+str(dates[counter])
				return dates[counter]

def findfallingedges(valuesdeltas, dates):
	mycounterfalling = 0
	for counter, x in enumerate(valuesdeltas):
		if np.sum(valuesdeltas[counter:counter+30]) < -0.035 and counter-mycounterfalling>120:
			if np.sum(valuesdeltas[counter+10:counter+30+10]) < -0.035:
				mycounterfalling = counter
				print "---> one falling edge at "+str(dates[counter])
				return dates[counter]

def findspikes(valuesdeltas, dates, seconds, filename):
	spikedates = []
	spikecounter = 0
	spikenames = []
	spikeseconds = []
	for counter, x in enumerate(valuesdeltas):
		if x > 0.4: #uA was at 0.4
			print "---> one spike at "+str(dates[counter])
			spikecounter = spikecounter + 1
			spikedates.append(dates[counter])
			spikeseconds.append(seconds[counter])
			spikenames.append(filename)
	return spikecounter, filename, spikedates, spikeseconds, spikenames

def removespikes(valuesdeltas, valueshv):
	for counter, x in enumerate(valuesdeltas):
		if x > 0.4: #nA
			for i in range(counter,counter+20): ##to remove spikes in current graphs from bb5
				if i == len(valueshv) -1:
					break
				valueshv[i] = valueshv[i-1]
	return valueshv

def removespikes_atgif(valuesdeltas, valueshv): #to remove spikes in current graphs from gif
	for counter, x in enumerate(valuesdeltas):
		if x > 0.4: #nA
			for i in range(counter,counter+30):
				if i == len(valueshv) -1:
					break
				valueshv[i] = valueshv[i-1]
	return valueshv


def removetrips(valuesdeltas, valueshv):
	for counter, x in enumerate(valuesdeltas):
		if abs(x) > 5: #5V
			for i in range(counter,counter+60*20):
				if i == len(valueshv) -1:
					break
				valueshv[i] = valueshv[i-1]
	return valueshv

def findspikes_50na(newvalues, mean_nospike, dates, seconds, filename):
	
	treshold = 0.050 #uA
	spikedates = []
	spikecounter = 0 #not used anymore
	spikenames = []
	spikeseconds = []
	setcounter = 0
	#print filename, mean_nospike
	for counter, x in enumerate(newvalues):
		if x > treshold+mean_nospike: #50 nA + mean without spikes
			#print "---> one spike at "+str(dates[counter])
			'''
			if seconds[counter] > setcounter + 3:
				spikecounter = spikecounter + 1
				spikedates.append(dates[counter])
				spikeseconds.append(seconds[counter])
				spikenames.append(filename)
				setcounter = seconds[counter]
			'''
			spikecounter = spikecounter + 1
			spikedates.append(dates[counter])
			spikeseconds.append(seconds[counter])
			spikenames.append(filename)
	return spikecounter, filename, spikedates, spikeseconds, spikenames

def findspikes_atgif(currentvalues, attenuation, meancurrent, setattenuation, dates, seconds, filename):
	''' to count spikes with current graphs from GIF'''

	treshold = 0.4 #uA
	spikedates = []
	spikecounter = 0
	spikenames = []
	spikeseconds = []
	for counter, x in enumerate(currentvalues[0:len(attenuation)]):
		if attenuation[counter] != 0.:
			currentatattenuation = meancurrent[setattenuation.index(float(attenuation[counter])**-1)]
			if x > currentatattenuation+treshold:
				spikecounter = spikecounter+1
				spikedates.append(dates[counter])
				spikeseconds.append(seconds[counter])
				spikenames.append(filename)

	return spikecounter, filename, spikedates, spikeseconds, spikenames


















