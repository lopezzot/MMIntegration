threshold = 565
def get_threshold(hvs): # get hospital lines voltages values
    values = [[],[],[],[]]
    hl1 = []
    hl2 = []
    div = []
    print hvs[0]
    for i, chamber in enumerate(hvs):
        for sector in chamber:
            if sector < threshold:
                values[i].append(sector)
        values[i].sort()
        div.append(values[i][int(len(values[i])/2)-1])
        hl1.append(int(values[i][0]))
        hl2.append(int(values[i][int(len(values[i])/2)]))
    return div, hl1, hl2

def get_sectors_hv(hvs):
    div, hl1, hl2 = get_threshold(hvs)
    final_values = []
    final_hv = []
    for i, chamber in enumerate(hvs):
        for sector in chamber:
            if sector < threshold:
                if sector > div[i]:
                    final_values.append(hl2[i])
                else:
                    final_values.append(hl1[i])
            else:
                final_values.append(570)
        final_hv.append(final_values)
        final_values = []
    return final_hv, hl1, hl2

def main():
    hv1 = [570.23, 570.22, 550.02, 570.01 ,520.07, 530.25, 550.57, 570.85, 560.96, 570.05]
    hv2 = [570, 570, 570, 570 ,550, 570, 560, 570, 570, 540]
    hv3 = [570, 530, 520, 570 ,520, 540, 550, 520, 530, 550]
    hv4 = [540, 570, 570, 570 ,520, 565, 570, 570, 570, 570]

    hvs = [hv1, hv2, hv3, hv4]
    result, hl1, hl2 = get_sectors_hv(hvs)
    print result[0]
    print hl1[0]
    print hl2[0]
    print "-----------------------\n"
    print result[1]
    print hl1[1]
    print hl2[1]
    print "-----------------------\n"
    print result[2]
    print hl1[2]
    print hl2[2]
    print "-----------------------\n"
    print result[3]
    print hl1[3]
    print hl2[3]
    print "-----------------------\n"
    print len(result[1])

if __name__ == '__main__':
    main()
