from ROOT import TMath
import math
def get_efficiency(x):
#    all values
    # p0 = -4135.1
    # p1 = 14.5086
    # p2 = -0.0124388
    # efficiency = p0 + p1*x + p2*x*x
# no 0
#    p0 = -4147.79
#    p1 = 14.5572
#    p2 = -0.0124852


# histogram
#    p0 = -4167.17
#    p1 = 14.6275
#    p2 = -0.0125488

    # if x == 0:
    #     efficiency = 0
    # elif x >= 580:
    #     efficiency = 95
    # else:
    #     efficiency = p0 + p1*x + p2*x*x
    # print efficiency

# sigmoid
    p0 = 96.7336
    p1 = 0.0626969
    p2 = 521.418
    efficiency = (p0/(1+ math.exp(-p1*(x-p2))))

# pol2

    # p0 = -0.121066
    # p1 = -0.283292
    # p2 = 0.000763684
    # efficiency = p0 + p1*x + p2*x*x

#    pol 5
    # p0 = -0.00206796
    # p1 = -2.133
    # p2 = 0.00200703
    # p3 = 9.83116*math.pow(10,-6)
    # p4 = 5.88458*math.pow(10,-9)
    # p5 = -2.04183*math.pow(10,-11)

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

#    efficiency = p0 + p1*x + p2*x*x + p3*x*x*x +p4*x*x*x*x + p5*x*x*x*x*x +p6*x*x*x*x*x*x+ p7*x*x*x*x*x*x*x + p8*x*x*x*x*x*x*x*x +p9*x*x*x*x*x*x*x*x*x
    print efficiency
    return efficiency

def get_mean_efficiency(values):
    total = 0
    for i in range(len(values)):
        total = total + get_efficiency(values[i])
    efficiency = total/len(values)
    return efficiency

def efficiency_values(values):   # get efficiency per sector, per layer and the whole chamber
    efficiency = []
    layers_efficiency = []
    for i in range(len(values)):
        print "HV"
        print values[i]
        print "efficiency"
        efficiency.append(get_efficiency(values[i]))

    total_efficiency = get_mean_efficiency(values)

    for x in range(len(values)/10):
        layers_efficiency.append(get_mean_efficiency(values[x*10:x*10+10]))

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
