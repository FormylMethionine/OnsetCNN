import os
import json
from parser import parse


def filter(song):
    ret = {}
    ret["#MUSIC"] = song["#MUSIC"]
    ret["#BPMS"] = song["#BPMS"]
    ret["#OFFSET"] = song["#OFFSET"]
    charts = song["#NOTES"]
    charts.sort(key=lambda x: x[3], reverse=True)
    ret["#NOTES"] = charts[0][4:]
    return ret


def parse_bpm(bpm, song):
    bpm = bpm.split(',')
    for i in bpm:
        bpm[bpm.index(i)] = i.split('=')
    ret = []
    print(bpm)
    j = 0
    for i in range(0, len(bpm)):
        if i < len(bpm)-1:
            while j < int(bpm[i+1][0].split('.')[0]):
                ret.append(bpm[i][1])
                j += 1
        else:
            while j < len(song)*4:
                ret.append(bpm[i][1])
                j += 1
    return ret


def onsets(song):
    return 0

if __name__ == "__main__":
    path = "dataset_ddr/stepcharts/Imagination Forest.sm"
    test = filter(parse(path))
    print(test)
    bpm = parse_bpm(test["#BPMS"], test["#NOTES"])
    print(test["#NOTES"])
    print(bpm[16])
    print(len(bpm), len(test["#NOTES"])*4)
