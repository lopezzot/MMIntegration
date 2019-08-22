threshold = 565
def get_threshold(hvs): # get hospital lines voltages values
    values = [[],[],[],[]]
    hl1 = []
    hl2 = []
    div = []
    for i, chamber in enumerate(hvs):
        for sector in chamber:
            if sector < threshold:
                values[i].append(sector)
        values[i].sort()
        if len(values[i]) != 0:
            div.append(values[i][int(len(values[i])/2)-1])
            hl1.append(int(values[i][0]))
            hl2.append(int(values[i][int(len(values[i])/2)]))
        else:
            div.append(0)
            hl1.append(0)
            hl2.append(0)
    return div, hl1, hl2
#---------------------------------------------------------------------
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
