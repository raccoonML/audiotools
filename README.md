# audiotools

This is a minimal audio library to generate and invert mel spectrograms for neural voice projects. The purpose is to provide an audio processing pipeline that is easy to inspect and extend.

## Setup

There is no setup required to use audiotools. Add the provided [audio.py](https://github.com/raccoonML/audiotools/blob/main/audio.py) to your project. It is intended to be a drop-in replacement for the audio.py in the popular [Rayhane-Mamah/Tacotron2](https://github.com/Rayhane-mamah/Tacotron-2) and [CorentinJ/Real-Time-Voice-Cloning](https://github.com/CorentinJ/Real-Time-Voice-Cloning) repos.

## Usage

A hyperparameters object containing the audio processing settings is a required input in each function call. An example `hparams.py` is provided for testing purposes. You can also reference the above projects for hparams files that will also work with this repo.

Note: The spectrogram shape used in this library is (n_mel_channels, n_frames). This is done for compatibility with the repos mentioned above. When using audiotools with other repos, you may need to transpose the spectrogram inputs and outputs to have the correct shape.

### Load an audio file
```
import audio
from hparams import hparams
wav = audio.load_wav("path/to/audio_file.wav", hparams)
```

### Make a mel spectrogram
```
spec = audio.melspectrogram(wav, hparams)
```

### Vocode the mel spectrogram with Griffin-Lim to recover an audio waveform
```
wav_out = audio.inv_mel_spectrogram(spec, hparams)
```

## Demo

To use the Voicebox interface to visualize spectrograms and test Griffin-Lim, set up a Python virtual environment and install the requirements.
```
pip install --upgrade pip
pip install -r requirements.txt
```

Then launch the user interface with:
```
python run_voicebox.py
```
