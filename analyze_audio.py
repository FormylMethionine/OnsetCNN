import essentia as es
import scipy.signal
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

if __name__ == "__main__":
    path = "./dataset_ddr/audiofiles/Anti the Holic.ogg"
    data, samplerate = sf.read(path)
    #samplerate, data = scipy.io.wavfile.read(path)
    print(data)
    f, t, Zxx = scipy.signal.stft(data, fs=samplerate)
    print(t)
    print(np.abs(Zxx)[0])
    print(np.shape(np.abs(Zxx)))
    plt.pcolormesh(t, f, np.abs(Zxx))
    plt.show()
