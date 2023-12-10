# gui implementation such as buttons etc
from tkinter import filedialog
from acoustic_model import Model


class Controller:
    def __init__(self, view):
        self.view = view
        self.model = Model()
        self.trackGraph = 0


    def LoadFile(self):
        # store the path to the file and open file explorer for user to select a file to analyze
        file_path = filedialog.askopenfilename(title="Select a File(must be audio file)", filetypes=[("All Files", "*.*")])

        # get file type to see if its mp3 or wav
        file_type = file_path[file_path.rfind(".") + 1:]
        if file_type.lower() != "mp3" and file_type.lower() != "wav":
            self.view.msgbox(1, 'warning', 'Please enter a mp3 or wav file.', 'warning')
        else:
            if file_type == "mp3":
                self.model.convertToWav(file_path)
            else:
                # place file in dir so we can use it
                self.model.placeFileInDir(file_path)
                if self.model.numChannels != 1:
                    if self.view.msgbox(2, "Warning", "Multi-Channel data detected, you will only be able to view the  waveform, Wish to continue?",'warning') == False:
                        exit(0)
                    else:
                        self.model.file_name = file_path[file_path.rfind("/") + 1:]
                        # if entered correctly then we can display the initial plot
                        self.model.readWav()
                        # Display waveform
                        self.view.displayWaveform(self.model)
                else:
                    self.model.file_name = file_path[file_path.rfind("/") + 1:]
                    # if entered correctly then we can display the initial plot
                    self.model.readWav()
                    # Display waveform
                    self.view.displayWaveform(self.model)
                    # Generate the plot for low frequency
                    self.view.genRT60plots(0)
                    # Generate the plot for mid-frequency
                    self.view.genRT60plots(1)
                    # Generate the plot for high frequency
                    self.view.genRT60plots(2)
                    # Generate combined plot
                    self.view.combinedPlot()
                    # generate plot for amp vs frequency
                    self.view.amp_vs_freq()

    def combinePlots(self):
        self.view.drawNextCanvas(4)

    def avsfPlot(self):
        self.view.drawNextCanvas(5)

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

        self.view.drawNextCanvas(self.trackGraph)

    def Waveform(self):
        self.view.drawNextCanvas(0)

