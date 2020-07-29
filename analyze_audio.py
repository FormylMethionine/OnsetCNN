import matplotlib.colors as clr
import matplotlib.pyplot as plt
import essentia.standard
import essentia
import numpy as np
import scipy.signal


def stft(path):

    windows = np.array([23, 46, 93])*1e-2
    samplerate = 44100
    loader = essentia.standard.MonoLoader(filename=path)
    data = loader()
    m = samplerate*windows
    ret = []
    for i in m:
        f, t, STFT = scipy.signal.stft(data,
                                       fs=samplerate,
                                       nperseg=samplerate*1e-2,
                                       nfft=i)
        ret.append([f, t, STFT])
    return ret


def analyze(path):
    samplerate = 44100
    loader = essentia.standard.MonoLoader(filename=path, sampleRate=samplerate)
    audiodata = loader()
    nffts = [1024, 2048, 4096]
    ret = []
    for nfft in nffts:
        win = essentia.standard.Windowing(size=nfft, type='hann')
        spec = essentia.standard.Spectrum(size=nfft)
        mel = essentia.standard.MelBands(inputSize=(nfft//2)+1,
                                         numberBands=80,
                                         lowFrequencyBound=27.5,
                                         highFrequencyBound=16000,
                                         sampleRate=samplerate)
        feats = []
        for frame in essentia.standard.FrameGenerator(audiodata, nfft, 512):
            frame_feats = mel(spec(win(frame)))
            feats.append(frame_feats)
        ret.append(feats)
    ret = np.transpose(np.stack(ret), (1, 2, 0))
    ret = np.log(ret + 1e-16)
    return ret



if __name__ == "__main__":
    path = './dataset_ddr/audiofiles/Anti the Holic.ogg'
    test = analyze(path)
    print(test)
    #data = stft(path)[1]
    #loader = MonoLoader(filename=path)
    #data = loader()
    #samplerate = 44100
    #data = data.sum(axis=1) / 2
    #m = floor(samplerate*9.3e-2)
    # f, t, STFT = scipy.signal.stft(data,
    #                               fs=samplerate,
    #                               nperseg=1e-2*samplerate,
    #                               nfft=samplerate*9.3e-2)
    #data[2] = np.abs(data[2])
    #plt.pcolormesh(data[1], data[0], data[2], norm=clr.LogNorm(), shading='nearest')
    #plt.show()
