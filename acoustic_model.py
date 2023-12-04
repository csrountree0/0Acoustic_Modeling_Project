# will contain the math and logic behind the project
from os import path
from pydub import AudioSegment
from pydub.playback import play
class Model:
    def __init__(self):
        pass

    #convert to wav
    def convertToWav(self, path):
        sound = AudioSegment.from_mp3(path)
        sound.export("temp.wav", format="wav")
