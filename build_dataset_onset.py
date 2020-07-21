import os
import json
from parser import parse


def filter(song):
    print("filtering...")
    ret = {}
    ret["#MUSIC"] = song["#MUSIC"]
    ret["#OFFSET"] = song["#OFFSET"]
    charts = song["#NOTES"]
    charts.sort(key=lambda x: x[3], reverse=True)
    i = 0
    while True:
        if type(charts[0][i]) == list:
            break
        i += 1
    ret["#NOTES"] = charts[0][i:]
    ret["#BPMS"] = parse_bpm(song["#BPMS"], ret["#NOTES"])
    return ret


def parse_bpm(bpm, song):
    print("parsing bpms...")
    bpm = bpm.split(',')
    for i in bpm:
        bpm[bpm.index(i)] = i.split('=')
    ret = []
    j = 0
    for i in range(0, len(bpm)):
        if i < len(bpm)-1:
            while j < int(bpm[i+1][0].split('.')[0]):
                ret.append(float(bpm[i][1]))
                j += 1
        else:
            while j < len(song)*4:
                print(j)
                ret.append(float(bpm[i][1]))
                j += 1
    return ret


def somme(note):
    ret = 0
    for char in note:
        ret += int(char)
    return ret


def onsets(song):
    print("converting to timestamps...")
    time = float(song["#OFFSET"])
    beat = 0
    ret = []
    for mes in song["#NOTES"]:
        i = 0
        while i < 4:
            bpm = song["#BPMS"][beat]
            for note in mes[int(0.25*i*len(mes)):int(0.25*(i+1)*len(mes))]:
                if somme(note) != 0:
                    ret.append(time)
                time += 4/(bpm*len(mes))*60*1000
            beat += 1
            i += 1
    return ret


if __name__ == "__main__":
    #path = "dataset_ddr/stepcharts/Imagination Forest.sm"
    #path = "dataset_ddr/stepcharts/Anti the Holic.sm"
    path = "dataset_ddr/stepcharts/Through the Fire and Flames.sm"
    test = filter(parse(path))
    print(test)
    bpm = test["#BPMS"]
    print(bpm)
    print(bpm[16])
    print(len(bpm), len(test["#NOTES"])*4)
    print(onsets(test))
    print(len(onsets(test)))
