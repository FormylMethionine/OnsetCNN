from time import perf_counter


def metadata(path):
    keys = {"#TITLE",
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
            "#KEYSOUNDS"}
    ret = {}
    with open(path, "r") as f:
        for line in f:
            line = line.split(":")
            if line[0] in keys:
                ret[line[0]] = line[1][:len(line[1])-2].strip()
    print(ret)
    return ret


def maps(path):
    ret = []
    f = open(path, "r")
    line = f.readline()
    chart = []
    while line != "":
        while line != "#NOTES:\n":
            line = f.readline()
        for i in range(1, 7):
            chart.append(line[:len(line)-1])
            line = f.readline()
        while line != "" and line != "\n" and line[0] != ';':
            to_add = []
            while line != "" and \
                    line != "\n" and \
                    line[0] != ',' and \
                    line[0] != ';':
                to_add.append(line[:len(line)-1])
                line = f.readline()
            chart.append(to_add)
            to_add = []
            line = f.readline()
        ret.append(chart)
        chart = []
        line = f.readline()
    f.close()
    return ret


def parse(path):
    ret = metadata(path)
    ret["#NOTES"] = maps(path)
    return ret


if __name__ == "__main__":
    path = "Songs/Vocaloid Project Pad Pack/Anti the Holic/Anti the Holic.sm"
    #path = "Anti the Holic.sm"
    t_start = perf_counter()
    dic = parse(path)
    t_end = perf_counter()
    t = t_end - t_start
    print(dic)
    print("elapsed time:", t)
