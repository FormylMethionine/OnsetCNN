import essentia.standard
import essentia
import numpy as np


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
