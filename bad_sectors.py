threshold = 565
def get_threshold(hvs):
    values = []
    for chamber in hvs:
        for sector in chamber:
            if sector < threshold:
                values.append(sector)
    values.sort()
    print "len values"
    print len(values)
    div = values[int(len(values)/2)-1]
    hl1 = round(values[0],2)
    hl2 = round(values[int(len(values)/2)],2)
    return div, hl1, hl2

def get_sectors_hv(hvs):
    div, hl1, hl2  = get_threshold(hvs)
    final_values = []
    final_hvs = []
    print "div"
    print div
    print "hl1"
    print hl1
    print "hl2"
    print hl2
    i=0
    for chamber in hvs:
        for sector in chamber:
            if sector < threshold:
                if sector > div:
                    final_values.append(hl2)
                else:
                    final_values.append(hl1)
            else:
                final_values.append(570)
        final_hvs.append(final_values)
        final_values = []
    return final_hvs, hl1, hl2

def main():
    hv1 = [570.23, 570.22, 550.02, 570.01 ,520.07, 530.25, 550.57, 570.85, 560.96, 570.05]
    hv2 = [570, 570, 570, 570 ,550, 570, 560, 570, 570, 540]
    hv3 = [570, 530, 520, 570 ,520, 540, 550, 520, 530, 550]
    hv4 = [540, 570, 570, 570 ,520, 560, 570, 550, 560, 570]

    hvs = [hv1, hv2, hv3, hv4]
    result = get_sectors_hv(hvs)
    print result[0]
    print "-----------------------\n"
    print result[1]
    print "-----------------------\n"
    print result[2]
    print "-----------------------\n"
    print result[3]
    print "-----------------------\n"
    print len(result[1])

if __name__ == '__main__':
    main()
