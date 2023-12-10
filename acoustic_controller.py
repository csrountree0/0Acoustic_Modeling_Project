# gui implementation such as buttons etc
from tkinter import filedialog
from acoustic_model import Model


class Controller:
    def __init__(self, view):
        self.view = view
        self.model = Model()
        self.trackGraph =0


    def LoadFile(self):
        # store the path to the file and open file explorer for user to select a file to analyze
        file_path = filedialog.askopenfilename(title="Select a File(must be audio file)", filetypes=[("All Files", "*.*")])

        # get file type to see if its mp3 or wav
        file_type = file_path[file_path.rfind(".") + 1:]
        if file_type.lower() != "mp3" and file_type.lower() != "wav":
            self.view.msgbox(1, 'Error', 'Please enter a mp3 or wav file.', 'error')
        else:
            if file_type == "mp3":
                self.model.convertToWav(file_path)
            else:
                # place file in dir so we can use it
                self.model.placeFileInDir(file_path)
            self.model.file_name = file_path[file_path.rfind("/") + 1:]
            # if entered correctly then we can display the initial plot
            self.model.readWav()
            self.view.displayWaveform(self.model)
            self.view.genRT60plots(0)
            self.view.genRT60plots(1)
            self.view.genRT60plots(2)
    def combinePlots(self):
        pass

    # for button to move through different RT graphs
    def nextPlot(self):
        # 0 is amplitude plot
        # 1 is low plot
        # 2 is mid plot
        # 3 is high plot
        self.trackGraph += 1
        if self.trackGraph == 4:
            self.trackGraph = 1
        if self.trackGraph == 1:
            self.view.RTgraphbtn.config(text="Mid")
        elif self.trackGraph == 2:
            self.view.RTgraphbtn.config(text="High")
        elif self.trackGraph == 3:
            self.view.RTgraphbtn.config(text="Low")

        self.view.clearPrevPlot()
        self.view.drawNextCanvas(self.trackGraph)


