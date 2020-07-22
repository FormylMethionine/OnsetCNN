import os
import json
from parser import parse


def filter(song):
    print("filtering...")
    ret = {}
    ret["#MUSIC"] = song["#MUSIC"]
    ret["#OFFSET"] = song["#OFFSET"]
    charts = song["#NOTES"]
    charts.sort(key=lambda x: int(x[3]), reverse=True)
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
    ret = {}
    ret["#MUSIC"] = song["#MUSIC"]
    ons = []
    for mes in song["#NOTES"]:
        i = 0
        while i < 4:
            bpm = song["#BPMS"][beat]
            for note in mes[int(0.25*i*len(mes)):int(0.25*(i+1)*len(mes))]:
                if somme(note) != 0:
                    ons.append(time)
                time += 4/(bpm*len(mes))*60*1000
            beat += 1
            i += 1
    ret["#ONSETS"] = ons
    return ret


def build_dataset():
    dataset = []
    for f in os.listdir("./dataset_ddr/stepcharts"):
        print("Converting '" + f + "'")
        f = "./dataset_ddr/stepcharts/" + f
        song = parse(f)
        song = filter(song)
        song = onsets(song)
        dataset.append(song)
        print("\n")
    with open("dataset_onset_ddr.json", "w") as f:
        f.write(json.dumps(dataset))


if __name__ == "__main__":
    build_dataset()
