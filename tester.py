import sys
from parser import parse
from build_dataset_onset import filter, onsets

path = sys.argv[1]
print(path)
song = parse(path)
song = filter(song)
print(song)
song = onsets(song)
