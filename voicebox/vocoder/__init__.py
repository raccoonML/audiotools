# raccoonML audio tools.
# MIT License
# Copyright (c) 2021 raccoonML (https://patreon.com/raccoonML)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software") to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR ANY OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from voicebox.vocoder.ui import UI
import librosa
import sys
import traceback

"""
Voicebox Vocoder Interface

Your project needs to provide the following interfaces to use this Voicebox UI.

voice_obj.sample_rate          # Sample rate in Hz
voice_obj.source_action(wav)   # Class method to handle a loaded source wav, returns: spec, wav_GL, spec_GL
                               #   where _GL designates Griffin-Lim. Voicebox ignores _GL variables if None
voice_obj.vocode_action()      # Class method to perform vocoding, returns: wav, spec
"""

class Voicebox:
    def __init__(self, voice_obj, window_title=""):
        # Prevent errors from crashing the window
        sys.excepthook = self.excepthook

        # Process inputs
        self.voice_obj = voice_obj

        if len(window_title) == 0:
            window_title = "Voicebox"

        # Initialize variables
        self.source_wav = None
        self.GL_wav = None
        self.vocoded_wav = None
        self.fpath = None

        # Initialize the events and the interface
        self.ui = UI(window_title)
        self.setup_events()
        self.update_buttons()
        self.ui.start()

    def excepthook(self, exc_type, exc_value, exc_tb):
        traceback.print_exception(exc_type, exc_value, exc_tb)
        self.ui.log("Exception: %s" % exc_value)
        
    def setup_events(self):
        ## Source
        # Load
        func = lambda: self.load_from_browser(self.ui.browse_file(), "source")
        self.ui.source_load_button.clicked.connect(func)
        # Play
        func = lambda: self.play("source") 
        self.ui.source_play_button.clicked.connect(func)

        ## GL
        # Play
        func = lambda: self.play("GL") 
        self.ui.GL_play_button.clicked.connect(func)
        # Save As
        func = lambda: self.save("GL")
        self.ui.GL_save_button.clicked.connect(func)

        ## Vocoded
        # Vocode
        func = lambda: self.vocode()
        self.ui.vocoded_vocode_button.clicked.connect(func)
        # Play
        func = lambda: self.play("vocoded") 
        self.ui.vocoded_play_button.clicked.connect(func)
        # Save As
        func = lambda: self.save("vocoded")
        self.ui.vocoded_save_button.clicked.connect(func)

    def get_wav(self, wavtype):
        if wavtype == "source":
            return self.source_wav
        elif wavtype == "GL":
            return self.GL_wav
        else:
            return self.vocoded_wav

    def play(self, wavtype):
        self.ui.play(self.get_wav(wavtype), self.voice_obj.sample_rate)
        
    def save(self, wavtype):
        self.ui.save_audio_file(self.get_wav(wavtype), self.voice_obj.sample_rate)

    def load_from_browser(self, fpath, wavtype):
        if fpath == "":
            return 

        # Load wav at the project's sample rate
        wav, _ = librosa.load(str(fpath), self.voice_obj.sample_rate)

        # Provide voice object with the wav
        if wavtype == "source":
            self.source_wav = wav
            spec, self.GL_wav, spec_GL = self.voice_obj.source_action(wav)

        # Draw the spectrogram
        if spec is not None:
            self.draw_spec(spec, wavtype)
        if spec_GL is not None:
            self.draw_spec(spec_GL, "GL")

        self.update_buttons()

    def vocode(self):
        # Call the vocoding process
        self.vocoded_wav, spec = self.voice_obj.vocode_action()
        # Draw the spectrogram
        if spec is not None:
            self.draw_spec(spec, "vocoded")

        self.update_buttons()

    def draw_spec(self, spec, wavtype):
        # Draw spec
        self.ui.draw_spec(spec, wavtype)

    def update_buttons(self):
        # Always allow loading of source
        self.ui.source_load_button.setDisabled(False)

        # Enable play/save buttons if wav exists
        if self.source_wav is None:
            self.ui.source_play_button.setDisabled(True)
        else:
            self.ui.source_play_button.setDisabled(False)
            
        if self.GL_wav is None:
            self.ui.GL_play_button.setDisabled(True)
            self.ui.GL_save_button.setDisabled(True)
        else:
            self.ui.GL_play_button.setDisabled(False)
            self.ui.GL_save_button.setDisabled(False)

        if self.vocoded_wav is None:
            self.ui.vocoded_play_button.setDisabled(True)
            self.ui.vocoded_save_button.setDisabled(True)
        else:
            self.ui.vocoded_play_button.setDisabled(False)
            self.ui.vocoded_save_button.setDisabled(False)

        # Enable vocode button when source exists
        if self.source_wav is None:
            self.ui.vocoded_vocode_button.setDisabled(True)
        else:
            self.ui.vocoded_vocode_button.setDisabled(False)
