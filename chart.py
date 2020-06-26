import numpy as np


class chart:

    def __init__(self, path):
        self.keys = ["#TITLE",
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
        keymap = {}
        for key in self.keys:
            keymap[key] = ""
        with open(path, "r") as f:
            for line in f:
                line = line.split(":")
                if line[0] in keymap:
                    keymap[line[0]] = line[1][:len(line[1])-2].strip()
        print(keymap)
