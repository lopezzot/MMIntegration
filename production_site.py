def read(filename):
    f = open(filename, "r")
    hv = []
    spike = []
    position = []
    for data in f:
        for i in range(len(data)):
            if data[i:i+1] == '\t':
                position.append(i)
            if data[i:i+1] == '\n':
                position.append(i)
        hv.append(data[5:position[1]])
        spike.append(data[position[1]+1:position[2]])
        position = []
    return hv, spike

def main():
    read("LM1_M3_Saclay_CS.dat")

if __name__ == '__main__':
    main()
