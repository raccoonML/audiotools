import librosa
import numpy as np
import audio
from hparams import hparams

"""
This helps implement a user interface for a vocoder.
Currently this is Griffin-Lim but can be extended to different vocoders.

Required elements for the vocoder UI are:
self.sample_rate
self.source_action
self.vocode_action
"""

class Voicebox_Project:
    def __init__(self):
        # Property needed for voicebox
        self.sample_rate = hparams.sample_rate

        # Initialization for project
        self.source_spec = None

    """
    The following action methods are called by Voicebox on button press
    Source: [Load] --> source_action
    Vocode: [Vocode] --> vocode_action
    """

    def source_action(self, wav):
        # The vocoder toolbox also vocodes the spectrogram with Griffin-Lim for comparison.
        # Inputs: wav (from voicebox)
        # Outputs: spec, wav_GL, spec_GL (to voicebox)
        self.source_spec = audio.melspectrogram(wav)
        wav_GL = audio.inv_mel_spectrogram(self.source_spec)
        spec_GL = audio.melspectrogram(wav_GL)
        return self.source_spec.T, wav_GL, spec_GL.T

    def vocode_action(self):
        # For this sample vocoder project, we will use Griffin-Lim as the vocoder.
        # Other projects will substitute an actual neural vocoder.
        # Inputs: None
        # Outputs: wav, spec (to voicebox)
        
        wav = audio.inv_mel_spectrogram(self.source_spec)
        spec = audio.melspectrogram(wav)
        return wav, spec.T
