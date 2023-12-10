# make the program appealing to the user, things the
# user can interact with that will be implemented in controller
import tkinter as tk
from acoustic_controller import Controller
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt
import numpy as np


class View:
    def __init__(self):
        self.controller = Controller(self)
        # window
        self.root = tk.Tk()
        self.root.withdraw()
        # load file button
        self.loadfilebtn = tk.Button(self.root, text="Load Audio File", command=self.controller.LoadFile)
        self.figures = []
        self.canvas = None
        # button for moving through RT60 graphs
        self.RTgraphbtn = None

    # create the initial window with load file button
    def initgui(self):
        # create window and title it Acoustic Modeling
        # self.root = tk.Tk()
        self.root.deiconify()
        self.root.title("Acoustic Modeling")
        self.root.geometry("200x100")
        self.root.protocol("WM_DELETE_WINDOW", self.endProgram)
        # create button for loading file which is implemented in acoustic_controller.py

        self.loadfilebtn.pack(pady=20)

    def endProgram(self):
        exit(0)

    def run(self):
        # start gui
        self.root.mainloop()

    # for using message boxes to let the user know something
    def msgbox(self, type, title, message, icon):
        # create types to hold some of the different types of message boxes
        types = {
            1: messagebox.askokcancel,
            2: messagebox.askyesno,
        }

        # if the type we want is in types then use it and display the message
        # box and return result, so we can use it if we need to
        if type in types:
            r = types[type](
                title=title,
                message=message,
                icon=icon,
            )
            return r

    def addbtns(self):
        # for additional buttons
        # frame to contain the buttons on top of screen
        btn_Frame = tk.Frame(self.root)
        btn_Frame.pack(side=tk.TOP, pady=20)

        # going back to waveform
        waveformbtn = tk.Button(self.root, text="Waveform", command=self.controller.Waveform)
        waveformbtn.pack(padx=5, in_=btn_Frame, side=tk.LEFT)


        self.RTgraphbtn = tk.Button(self.root, text="Low", command=self.controller.nextPlot)
        self.RTgraphbtn.pack(padx=5, in_=btn_Frame, side=tk.LEFT)

        # combining plots into single plot
        combinebtn = tk.Button(self.root, text="Combine Plots", command=self.controller.combinePlots)
        combinebtn.pack(padx=5, in_=btn_Frame, side=tk.LEFT)

        # amp vs freq plot to show the highest amp
        avsfbtn = tk.Button(self.root, text="Amp vs freq", command=self.controller.avsfPlot)
        avsfbtn.pack(padx=5, in_=btn_Frame, side=tk.LEFT)

        # RT60 avg reduced by .5
        RTlbl = tk.Label(self.root, text="Difference: " + str(round(self.controller.model.RTdiff, 3)) + " seconds")
        RTlbl.pack(side=tk.BOTTOM)
        # highest resonance freq
        min_l = min(len(self.controller.model.freqs), len(self.controller.model.data))
        max_amp = np.argmax(self.controller.model.data[:min_l])
        reslbl = tk.Label(self.root, text="Frequency with highest amplitude: " + str(
            round(self.controller.model.freqs[max_amp], 2)) + " hz")
        reslbl.pack(side=tk.BOTTOM)

        # time value for wav
        lenlbl = tk.Label(self.root,
                          text="Time of wav file: " + str(round(self.controller.model.t[-1], 2)) + " seconds")
        lenlbl.pack(side=tk.BOTTOM)


    def displayWaveform(self, model):
        # remove load file button
        self.loadfilebtn.destroy()
        # add new buttons
        if self.controller.model.numChannels == 1:
            self.addbtns()
            # resize window
            self.root.geometry("675x625")
        else:
            self.root.geometry("600x500")

        # add figure of waveform to figures
        self.figures.append(Figure(figsize=(7, 5), dpi=100))
        # do all the plotting
        time = np.linspace(0., model.data.shape[0] / model.samplerate, model.data.shape[0])
        plot1 = self.figures[0].add_subplot(111)
        if model.numChannels == 2:
            plot1.plot(time, model.data[:, 0], label="Left channel")
            plot1.plot(time, model.data[:, 1], label="Right channel")
        else:
            plot1.plot(time, model.data, label="Audio")
        plot1.legend()
        plot1.set_xlabel("Time [s]")
        plot1.set_ylabel("Amplitude")
        plot1.set_title("Waveform of " + model.file_name)

        # set canvas as a TkAgg obj, so we can put it in tkinter window
        self.canvas = FigureCanvasTkAgg(self.figures[0], master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP)

        # causing too many issues
        #toolbar = NavigationToolbar2Tk(self.canvas, self.root)
        #toolbar.update()
        #self.canvas.get_tk_widget().pack(side=tk.TOP)

        # labels for displaying text




    def clearPrevPlot(self):
        # clear the canvas, so we can update it with another graph
        self.canvas.get_tk_widget().destroy()

    def genRT60plots(self, type):
        self.figures.append(Figure(figsize=(7, 5), dpi=100))
        plot1 = self.figures[type + 1].add_subplot(111)
        title_str = ""
        if type == 0:
            title_str = "Low"
            plot1.plot(self.controller.model.t, self.controller.model.dBdata[type], label="Low", color='blue')
        elif type == 1:
            title_str = "Mid"
            plot1.plot(self.controller.model.t, self.controller.model.dBdata[type], label="Mid", color='purple')
        elif type == 2:
            title_str = "High"
            plot1.plot(self.controller.model.t, self.controller.model.dBdata[type], label="High", color='pink')

        plot1.set_xlabel("Time [s]")
        plot1.set_ylabel("Intensity [dB]")
        plot1.set_title("RT60 for " + title_str)
        iom = self.controller.model.maxValueIndex[type]
        ioml5 = self.controller.model.RT60Stuff[type][0]
        ioml25 = self.controller.model.RT60Stuff[type][1]
        plot1.plot(self.controller.model.t[iom], self.controller.model.dBdata[type][iom], 'go')
        plot1.plot(self.controller.model.t[ioml5], self.controller.model.dBdata[type][ioml5], 'yo')
        plot1.plot(self.controller.model.t[ioml25], self.controller.model.dBdata[type][ioml25], 'ro')

    def combinedPlot(self):
        self.figures.append(Figure(figsize=(7, 5), dpi=100))
        combined_plot = self.figures[-1].add_subplot(111)

        for i in range(1, 4):
            figure = self.figures[i]

            for ax in figure.get_axes():
                line = ax.lines[0]
                combined_plot.plot(line.get_xdata(), line.get_ydata(), label=ax.get_title(), color=line.get_color())

        combined_plot.set_xlabel("Time [s]")
        combined_plot.set_ylabel("Intensity [dB]")
        combined_plot.set_title("Combined Waveforms")

        combined_plot.legend()

    def amp_vs_freq(self):
        min_l = min(len(self.controller.model.freqs),len(self.controller.model.data))
        self.figures.append(Figure(figsize=(7, 5), dpi=100))
        avfplot = self.figures[-1].add_subplot(111)
        avfplot.plot(self.controller.model.freqs[:min_l],self.controller.model.data[:min_l])
        avfplot.set_xlabel("Frequency [Hz]")
        avfplot.set_ylabel("Amplitude")
        avfplot.set_title("Amplitude vs Frequency")
        # max amplitude index
        max_amp = np.argmax(self.controller.model.data[:min_l])
        avfplot.plot(self.controller.model.freqs[max_amp], self.controller.model.data[max_amp],'go')

    def drawNextCanvas(self, type):
        self.clearPrevPlot()
        self.canvas = FigureCanvasTkAgg(self.figures[type], master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP)

