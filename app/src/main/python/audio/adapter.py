#!/usr/bin/env python
# coding: utf8

""" AudioAdapter class defintion. """

from abc import ABC, abstractmethod

# pylint: disable=import-error
import numpy as np

# from tensorflow.contrib.signal import stft, hann_window
# pylint: enable=import-error

# from .. import SpleeterError
# from ..utils.logging import get_logger

__email__ = 'research@deezer.com'
__author__ = 'Deezer Research'
__license__ = 'MIT License'


class AudioAdapter(ABC):
    """ An abstract class for manipulating audio signal. """

    # Default audio adapter singleton instance.
    DEFAULT = None

    @abstractmethod
    def load(
            self, audio_descriptor, offset, duration,
            sample_rate, dtype=np.float32):
        """ Loads the audio file denoted by the given audio descriptor
        and returns it data as a waveform. Aims to be implemented
        by client.

        :param audio_descriptor:    Describe song to load, in case of file
                                    based audio adapter, such descriptor would
                                    be a file path.
        :param offset:              Start offset to load from in seconds.
        :param duration:            Duration to load in seconds.
        :param sample_rate:         Sample rate to load audio with.
        :param dtype:               Numpy data type to use, default to float32.
        :returns:                   Loaded data as (wf, sample_rate) tuple.
        """
        pass


    @abstractmethod
    def save(
            self, path, data, sample_rate,
            codec=None, bitrate=None):
        """ Save the given audio data to the file denoted by
        the given path.

        :param path: Path of the audio file to save data in.
        :param data: Waveform data to write.
        :param sample_rate: Sample rate to write file in.
        :param codec: (Optional) Writing codec to use.
        :param bitrate: (Optional) Bitrate of the written audio file.
        """
        pass


def get_default_audio_adapter():
    """ Builds and returns a default audio adapter instance.

    :returns: An audio adapter instance.
    """
    if AudioAdapter.DEFAULT is None:
        from .ffmpeg import FFMPEGProcessAudioAdapter
        AudioAdapter.DEFAULT = FFMPEGProcessAudioAdapter()
    return AudioAdapter.DEFAULT


