# will contain the math and logic behind the project
from os import path
from pydub import AudioSegment
from pydub.playback import play
from scipy.io import wavfile
from scipy.fft import fft
import scipy.io
import numpy as np
import matplotlib.pyplot as plt


class Model:
    def __init__(self):
        # count how many channels there are
        self.numChannels = 0
        # store data read from wav
        self.data = 0
        # store samplerate
        self.samplerate = 0
        # store name of file
        self.file_name = ""
        # hold spectrum, frequencies, time, and image
        self.spectrum=None
        self.freqs=None
        self.t=None
        self.im =None
        # hold dB data go from low, mid, high
        self.dBdata = []
        # index of max value
        self.maxValueIndex = []
        # RT60 holds index for 5, 25 and RT60 time
        self.RT60Stuff = []
        # RT60 avg -0.5
        self.RTdiff = 0
    # convert to wav
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
        if self.numChannels == 1:
            self.spectrum, self.freqs, self.t, self.im = plt.specgram(self.data, Fs=self.samplerate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
            self.frequency_check(250)
            self.frequency_check(1000)
            self.frequency_check(5000)
            self.calculateRT60(0)
            self.calculateRT60(1)
            self.calculateRT60(2)
            self.calcDiff()

    def find_target_freq(self, target):
        # finds first occurrence of a target frequency
        # 250 for low
        # 1000 for mid
        # 50000 for high
        for x in self.freqs:
            if x > target:
                break
        return x

    def frequency_check(self, target):
        # get data in db from specific frequency for RT60 calculation
        target_freq = self.find_target_freq(target)
        # find the index of the first occurrence of target_freq
        # which is stored in a tuple that holds an array of indices
        index_of_freq = np.where(self.freqs == target_freq)[0][0]
        # get the data for respective frequency
        data_for_freq = self.spectrum[index_of_freq]
        # convert to dB
        data_in_db_fun = 10 * np.log10(data_for_freq)
        # add it to the list of data
        self.dBdata.append(data_in_db_fun)

    # since the exact value might not exist for
    # -5 or -25 we get the closest value
    def find_nearest_value(self, a, v):
        a = np.asarray(a)
        idx = (np.abs(a-v)).argmin()
        return a[idx]

    def calculateRT60(self, type):
        # get index of max value
        self.maxValueIndex.append(np.argmax(self.dBdata[type]))
        # from max onward for low mid and high
        sliced_array = self.dBdata[type][self.maxValueIndex[-1]:]
        # calculate max -5
        vml5 = self.dBdata[type][self.maxValueIndex[type]] - 5
        # find nearest value of max -5dB
        vml5 = self.find_nearest_value(sliced_array, vml5)
        # find index in non sliced array
        iml5 = np.where(self.dBdata[type] == vml5)
        # repeat for -25
        vml25 = self.dBdata[type][self.maxValueIndex[type]] -25
        vml25 = self.find_nearest_value(sliced_array, vml25)
        iml25 = np.where(self.dBdata[type] == vml25)
        # get rt20
        rt20 = (self.t[iml5] - self.t[iml25])[0]
        # place indexes and RT60 in list
        self.RT60Stuff.append([iml5, iml25, abs(rt20*3)])

    def calcDiff(self):
        self.RTdiff = (self.RT60Stuff[0][2] +self.RT60Stuff[1][2]+self.RT60Stuff[2][2] / 3) - 0.5