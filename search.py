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

def findspikes(valuesdeltas, dates, filename):
	spikedates = []
	spikecounter = 0
	spikenames = []
	for counter, x in enumerate(valuesdeltas):
		if x > 0.4:
			print "---> one spike at "+str(dates[counter])
			spikecounter = spikecounter + 1
			spikedates.append(dates[counter])
			spikenames.append(filename)
	return spikecounter, filename, spikedates, spikenames