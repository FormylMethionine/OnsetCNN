import os
import json
import pickle as pkl
from analyze_audio import analyze
from parser import parse


def filter(metadata, charts):
    #print("filtering...")
    ret = []
    #ret["#MUSIC"] = song["#MUSIC"]
    #ret["#OFFSET"] = song["#OFFSET"]
    #charts = song["#NOTES"]
    charts.sort(key=lambda x: int(x[3]), reverse=True)
    i = 0
    while True:
        if type(charts[0][i]) == list:
            break
        i += 1
    ret = charts[0][i:]
    bpm = parse_bpm(ret, metadata["#BPMS"])
    return ret, bpm


def parse_bpm(chart, bpm):
    #print("parsing bpms...")
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
            while j < len(chart)*4:
                ret.append(float(bpm[i][1]))
                j += 1
    return ret


def somme(note):
    ret = 0
    for char in note:
        ret += int(char)
    return ret


def onsets(metadata, chart, bpm):
    #print("converting to timestamps...")
    time = float(metadata["#OFFSET"])
    beat = 0
    ret = []
    audiodata = analyze("./dataset_ddr/audiofiles/"+metadata["#MUSIC"])
    ons = []
    for mes in chart:
        i = 0
        while i < 4:
            bpmtmp = abs(bpm[beat])
            for note in mes[int(0.25*i*len(mes)):int(0.25*(i+1)*len(mes))]:
                if somme(note) != 0:
                    ons.append(time)
                time += 4/(bpmtmp*len(mes))*60*1000
            beat += 1
            i += 1
    ret = ons
    return ret, audiodata


def build_dataset():
    n = 0
    for f in os.listdir("./dataset_ddr/stepcharts"):
        print("Converting '" + f + "'")
        path = "./dataset_ddr/stepcharts/" + f
        metadata, chart = parse(path)
        chart, bpm = filter(metadata, chart)
        chart, audio = onsets(metadata, chart, bpm)
        with open(f+'.json', 'w') as fi:
            fi.write(json.dumps(chart))
        with open(f+'.metadata', 'w') as fi:
            fi.write(json.dumps(metadata))
        with open(f+'.pkl', 'wb') as fi:
            fi.write(pkl.dumps(audio))
        n += 1
        #print("\n")
    print(n, "files converted")


if __name__ == "__main__":
    build_dataset()
