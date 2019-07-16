from ROOT import TMath
import math
def get_efficiency(x):

# sigmoid
    p0 = 96.7336
    p1 = 0.0626969
    p2 = 521.418
    efficiency = (p0/(1+ math.exp(-p1*(x-p2))))

#pol9
    # p0 = 8.4947*pow(10,-8)
    # p1 = -3.33873
    # p2 = 0.00179341
    # p3 = 9.1305*pow(10,-6)
    # p4 = 1.54081*pow(10,-8)
    # p5 = 1.0672*pow(10,-11)
    # p6 = -2.86486*pow(10,-14)
    # p7 = -1.51173*pow(10,-16)
    # p8 = -1.52798*pow(10,-20)
    # p9 = 2.4595*pow(10,-22)
    #
    # efficiency = p0 + p1*x + p2*pow(x,2) + p3*pow(x,3) +p4*pow(x,4) + p5*pow(x,5) +p6*pow(x,6)+ p7*pow(x,7) + p8*pow(x,8) +p9*pow(x,9)
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

def main():
    get_efficiency(0)
    get_efficiency(520)
    get_efficiency(530)
    get_efficiency(540)
    get_efficiency(550)
    get_efficiency(560)
    get_efficiency(570)
    get_efficiency(580)
    get_efficiency(590)
    get_efficiency(600)

if __name__ == '__main__':
    main()
