def metadata(path):
    keys = ["#TITLE",
            "#SUBTITLE",
            "#ARTIST",
            "#TITLETRANSLIT",
            "#ARTISTTRANSLIT",
            "#GENRE",
            "#CREDIT",
            "#BANNER",
            "#BACKGROUND",
            "#LYRICSPATH",
            "#CDTITLE",
            "#MUSIC",
            "#OFFSET",
            "#SAMPLESTART",
            "#SAMPLELENGTH",
            "#SELECTABLE",
            "#DISPLAYBPM",
            "#BPMS",
            "#STOPS",
            "#BGCHANGES",
            "#KEYSOUNDS"]
    ret = {}
    for key in keys:
        ret[key] = ""
        with open(path, "r") as f:
            for line in f:
                line = line.split(":")
                if line[0] in ret:
                    ret[line[0]] = line[1][:len(line[1])-2].strip()
    return ret


def maps(path):
    ret = []
    i = -1
    with open(path, "r") as f:
        for line in f:
            if "#NOTES" in line:
                i += 1
                ret.append([])
            if i >= 0:
                ret[i].append(line[:len(line)-1])
    for chart in ret:
        print(clean(chart))
        chart = clean(chart)

    return ret


def clean(chart):
    ret = chart.copy()
    to_remove = ["#NOTES:", '', ';']
    for i in to_remove:
        ret.remove(i)
        for i in ret:
            if i[0:2] == "//":
                ret.remove(i)
        #to_add = []
        #for i in ret:
            #to_add.append(i)
            #ret.remove(i)
            #if i == ',' or ret.index(i) == 4:
                #ret.append(to_add[:len(to_add)-1])
                #to_add = []
    return ret


def parse(path):
    ret = metadata(path)
    ret["#NOTES"] = maps(path)
    return ret


if __name__ == "__main__":
    path = "Songs/Vocaloid Project Pad Pack/Anti the Holic/Anti the Holic.sm"
    print(parse(path))
