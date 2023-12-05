# will contain the math and logic behind the project
from os import path
from pydub import AudioSegment
from pydub.playback import play
from scipy.io import wavfile
import scipy.io
class Model:
    def __init__(self):
        self.numChannels = 0
        self.data = 0
        self.samplerate = 0


    #convert to wav
    def convertToWav(self, path):
        sound = AudioSegment.from_mp3(path)
        sound.export("temp.wav", format="wav", tags={})
        self.num_channels()

    # exports the selected file
    # to the directory of the modules
    def placeFileInDir(self, path):
        sound = AudioSegment.from_file(path)
        sound.export("temp.wav", format="wav", tags={})
        self.num_channels()

    # store number of channels in attribute
    def num_channels(self):
        sound = AudioSegment.from_file("temp.wav")
        self.numChannels = sound.channels

    def readWav(self):
       self.samplerate, self.data = wavfile.read("temp.wav")