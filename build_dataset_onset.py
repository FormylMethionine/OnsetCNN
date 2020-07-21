import os
import json
from parser import parse


def filter(song):
    ret = {}
    ret["#MUSIC"] = song["#MUSIC"]
    ret["#OFFSET"] = song["#OFFSET"]
    charts = song["#NOTES"]
    charts.sort(key=lambda x: x[3], reverse=True)
    ret["#NOTES"] = charts[0][4:]
    ret["#BPMS"] = parse_bpm(song["#BPMS"], ret["#NOTES"])
    return ret


def parse_bpm(bpm, song):
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
    time = float(song["#OFFSET"])
    beat = 0
    bpm = song["#BPMS"][beat]
    ret = []
    for measure in song["#NOTES"]:
        i = 0
        while i < 4:
            for note in measure[int(0.25*i*len(measure)):int(0.25*(i+1)*len(measure))]:
                if somme(note) != 0:
                    ret.append(time)
                time += 4/(bpm*len(measure)) * 60 * 1000
            beat += 1
            bpm = song["#BPMS"][beat%356]
            i += 1
    return ret


if __name__ == "__main__":
    path = "dataset_ddr/stepcharts/Imagination Forest.sm"
    test = filter(parse(path))
    print(test)
    bpm = test["#BPMS"]
    print(bpm)
    print(bpm[16])
    print(len(bpm), len(test["#NOTES"])*4)
    print(onsets(test))
    print(len(onsets(test)))
