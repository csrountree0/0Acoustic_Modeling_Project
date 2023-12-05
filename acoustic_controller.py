# gui implementation such as buttons etc
from acoustic_view import View
from tkinter import filedialog
from acoustic_model import Model


class Controller:
    def __init__(self):
        self.view = View(self)
        self.model = Model()
    def LoadFile(self):
        # store the path to the file and open file explorer for user to select a file to analyze
        file_path = filedialog.askopenfilename(title="Select a File(must be audio file)",
                                               filetypes=[("All Files", "*.*")])

        # get file type to see if its mp3 or wav
        file_type = file_path[file_path.rfind(".") + 1:]

        if file_type != "mp3" and file_type != "wav":
            self.view.msgbox(1, 'Error', 'Please enter a mp3 or wav file.', 'error')
        else:
            if file_type == "mp3":
                self.model.convertToWav(file_path)
            else:
                # place file in dir so we can use it
                self.model.placeFileInDir(file_path)

        # if entered correctly then we can display the inital plot
        self.model.readWav()
        self.view.displayWaveform(self.model)