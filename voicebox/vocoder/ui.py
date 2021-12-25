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

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from pathlib import Path
import sounddevice as sd
import soundfile as sf
import numpy as np
import sys
from warnings import filterwarnings, warn
filterwarnings("ignore")


class UI(QDialog):
    def draw_spec(self, spec, which):
        if which == "source":
            spec_ax = self.source_ax
        elif which == "GL":
            spec_ax = self.GL_ax
        else:
            spec_ax = self.vocoded_ax

        # Draw the spectrogram
        spec_ax.clear()
        if spec is not None:
            im = spec_ax.imshow(np.flip(spec.T, axis=0), aspect="auto", interpolation="none")
    
        spec_ax.set_xticks([])
        spec_ax.set_yticks([])
        spec_ax.figure.canvas.draw()

    def save_audio_file(self, wav, sample_rate):        
        dialog = QFileDialog()
        dialog.setDefaultSuffix(".wav")
        fpath, _ = dialog.getSaveFileName(
            parent=self,
            caption="Select a path to save the audio file",
            filter="Audio Files (*.flac *.wav)"
        )
        if fpath:
            #Default format is wav
            if Path(fpath).suffix == "":
                fpath += ".wav"
            sf.write(fpath, wav, sample_rate)

    def play(self, wav, sample_rate):
        try:
            sd.stop()
            sd.play(wav, sample_rate)
        except Exception as e:
            print(e)
            self.log("Error in audio playback. Try selecting a different audio output device.")
            self.log("Your device must be connected before you start the toolbox.")
        
    def stop(self):
        sd.stop()

    def browse_file(self):
        fpath = QFileDialog().getOpenFileName(
            parent=self,
            caption="Select an audio file",
            filter="Audio Files (*.mp3 *.flac *.wav *.m4a)"
        )
        return Path(fpath[0]) if fpath[0] != "" else ""
    
    def log(self, msg):
        pass

    def reset_interface(self):
        self.draw_spec(None, "source")
        self.draw_spec(None, "GL")
        self.draw_spec(None, "vocoded")

    def __init__(self, window_title):
        ## Initialize the application
        self.app = QApplication(sys.argv)
        super().__init__(None)
        self.setWindowTitle(window_title)
        
        ## Main layouts
        # Root
        root_layout = QGridLayout()
        self.setLayout(root_layout)
        
        # Source Controls
        source_cont_layout = QGridLayout()
        root_layout.addLayout(source_cont_layout, 0, 0, 1, 1)
        
        source_cont_layout.addWidget(QLabel("Source"), 0, 0)
        self.source_load_button = QPushButton("Load")
        source_cont_layout.addWidget(self.source_load_button, 1, 0)
        self.source_play_button = QPushButton("Play")
        source_cont_layout.addWidget(self.source_play_button, 1, 1)

        # Source Spectrogram
        source_spec_layout = QVBoxLayout()
        root_layout.addLayout(source_spec_layout, 1, 0, 1, 5)
        
        source_spec_layout.addStretch()
        fig, self.source_ax = plt.subplots(1, 1, figsize=(10, 2.25), facecolor="#F0F0F0")
        source_spec_layout.addWidget(FigureCanvas(fig))

        # GL Controls
        GL_cont_layout = QGridLayout()
        root_layout.addLayout(GL_cont_layout, 6, 0, 1, 1)
        
        GL_cont_layout.addWidget(QLabel("Griffin-Lim"), 0, 0)
        self.GL_play_button = QPushButton("Play")
        GL_cont_layout.addWidget(self.GL_play_button, 1, 0)
        self.GL_save_button = QPushButton("Save")
        GL_cont_layout.addWidget(self.GL_save_button, 1, 1)

        # Griffin-Lim Spectrogram
        GL_spec_layout = QVBoxLayout()
        root_layout.addLayout(GL_spec_layout, 7, 0, 1, 5)
        
        GL_spec_layout.addStretch()
        fig, self.GL_ax = plt.subplots(1, 1, figsize=(10, 2.25), facecolor="#F0F0F0")
        GL_spec_layout.addWidget(FigureCanvas(fig))

        # Vocoded Controls
        vocoded_cont_layout = QGridLayout()
        root_layout.addLayout(vocoded_cont_layout, 8, 0, 1, 1)
        
        vocoded_cont_layout.addWidget(QLabel("Vocoded"), 0, 0)
        self.vocoded_vocode_button = QPushButton("Vocode")
        vocoded_cont_layout.addWidget(self.vocoded_vocode_button, 1, 0)
        self.vocoded_play_button = QPushButton("Play")
        vocoded_cont_layout.addWidget(self.vocoded_play_button, 1, 2)
        self.vocoded_save_button = QPushButton("Save")
        vocoded_cont_layout.addWidget(self.vocoded_save_button, 1, 3)

        # Vocoded Spectrogram
        vocoded_spec_layout = QVBoxLayout()
        root_layout.addLayout(vocoded_spec_layout, 9, 0, 1, 5)
        
        vocoded_spec_layout.addStretch()
        fig, self.vocoded_ax = plt.subplots(1, 1, figsize=(10, 2.25), facecolor="#F0F0F0")
        vocoded_spec_layout.addWidget(FigureCanvas(fig))

        # Set attributes for spectrogram plots
        for ax in [self.source_ax, self.GL_ax, self.vocoded_ax]:
            ax.set_facecolor("#F0F0F0")
            for side in ["top", "right", "bottom", "left"]:
                ax.spines[side].set_visible(False)
        
        ## Set the size of the window and of the elements
        max_size = QDesktopWidget().availableGeometry(self).size() * 0.8
        self.resize(max_size)
        
        ## Finalize the display
        self.reset_interface()
        self.show()

    def start(self):
        self.app.exec_()
