from ROOT import TMath
import math
def get_efficiency(x):

# sigmoid
    p0 = 96.7336
    p1 = 0.0626969
    p2 = 521.418
    efficiency = (p0/(1+ math.exp(-p1*(x-p2))))
    return efficiency

def get_mean_efficiency(values):
    total = 0
    for i in range(len(values)):
        total = total + get_efficiency(values[i])
    efficiency = total/len(values)
    return efficiency

def efficiency_values(values, type):   # get efficiency per sector, per layer and the whole chamber
    efficiency = []
    layers_efficiency = []
    for i in range(len(values)):
        efficiency.append(get_efficiency(values[i]))
    total_efficiency = get_mean_efficiency(values)
    if type == "SM1" or type == "SM2":
        for x in range(len(values)/10):
            layers_efficiency.append(get_mean_efficiency(values[x*10:x*10+10]))
    else:
        for x in range(len(values)/6):
            layers_efficiency.append(get_mean_efficiency(values[x*6:x*6+6]))

    return efficiency, layers_efficiency, total_efficiency
