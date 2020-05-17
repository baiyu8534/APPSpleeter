import audio.ffmpeg as ffmpeg
import numpy as np
import librosa
from librosa.core import stft, istft
from scipy.signal.windows import hann

import os

from multiprocessing import Pool

def _stft(data, inverse=False, length=None):
    """
    Single entrypoint for both stft and istft. This computes stft and istft with librosa on stereo data. The two
    channels are processed separately and are concatenated together in the result. The expected input formats are:
    (n_samples, 2) for stft and (T, F, 2) for istft.
    :param data: np.array with either the waveform or the complex spectrogram depending on the parameter inverse
    :param inverse: should a stft or an istft be computed.
    :return: Stereo data as numpy array for the transform. The channels are stored in the last dimension
    """
    assert not (inverse and length is None)
    data = np.asfortranarray(data)
    N = 4096
    H = 1024
    win = hann(N, sym=False)
    fstft = istft if inverse else stft
    win_len_arg = {"win_length": None, "length": length} if inverse else {"n_fft": N}
    n_channels = data.shape[-1]
    out = []
    for c in range(n_channels):
        d = data[:, :, c].T if inverse else data[:, c]
        s = fstft(d, hop_length=H, window=win, center=False, **win_len_arg)
        s = np.expand_dims(s.T, 2 - inverse)
        out.append(s)
    if len(out) == 1:
        return out[0]
    return np.concatenate(out, axis=2 - inverse)


def save_to_file(
        sources,
        codec='wav', audio_adapter=ffmpeg.FFMPEGProcessAudioAdapter(),
        bitrate='128k', synchronous=True):
    """ export dictionary of sources to files.

    :param sources:             Dictionary of sources to be exported. The
                                keys are the name of the instruments, and
                                the values are Nx2 numpy arrays containing
                                the corresponding intrument waveform, as
                                returned by the separate method
    :param audio_descriptor:    Describe song to separate, used by audio
                                adapter to retrieve and load audio data,
                                in case of file based audio adapter, such
                                descriptor would be a file path.
    :param destination:         Target directory to write output to.
    :param filename_format:     (Optional) Filename format.
    :param codec:               (Optional) Export codec.
    :param audio_adapter:       (Optional) Audio adapter to use for I/O.
    :param bitrate:             (Optional) Export bitrate.
    :param synchronous:         (Optional) True is should by synchronous.

    """

    # filename = "chengdu.mp3"
    pool = Pool()
    tasks = []
    for instrument, data in sources.items():
        path = "./out/"+instrument + "." + codec

        if pool:
            task = pool.apply_async(audio_adapter.save, (
                path,
                data,
                44100,
                codec,
                bitrate))
            tasks.append(task)
        else:
            audio_adapter.save(path, data, 44100, codec, bitrate)
    if synchronous and pool:
        while len(tasks) > 0:
            task = tasks.pop()
            task.get()
            task.wait(timeout=200)



def get_transfrom_data(music_path):
    audio_adapter = ffmpeg.FFMPEGProcessAudioAdapter()
    offset = 0
    duration = 600.
    codec = 'wav'
    bitrate = '128k'
    filename_format = '{filename}/{instrument}.{codec}'
    synchronous = False

    waveform, sample_rate = audio_adapter.load(
        music_path,
        offset=offset,
        duration=duration,
        sample_rate=44100)

    stft = _stft(waveform)
    if stft.shape[-1] == 1:
        stft = np.concatenate([stft, stft], axis=-1)
    elif stft.shape[-1] > 2:
        stft = stft[:, :2]

    # print(waveform)
    print(stft)
    return stft