def read(filename):
    f = open(filename, "r")
    hv = []
    spike = []
    for data in f:
        hv.append(data[5:8])
        spike.append(data[9:10])
    print spike
    print hv
    return hv, spike

def main():
    read("LM1_M3_Saclay_CS.dat")

if __name__ == '__main__':
    main()
