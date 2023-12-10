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

    # create the initial window
    def initgui(self):
        # create window and title it Acoustic Modeling
        # self.root = tk.Tk()
        self.root.deiconify()
        self.root.title("Acoustic Modeling")
        self.root.geometry("200x100")
        # create button for loading file which is implemented in acoustic_controller.py

        self.loadfilebtn.pack(pady=20)

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

        self.RTgraphbtn = tk.Button(self.root, text="Low", command=self.controller.nextPlot)
        self.RTgraphbtn.pack(padx=5, in_=btn_Frame, side=tk.LEFT)

        # combining plots into single plot
        combinebtn = tk.Button(self.root, text="Combine Plots", command=self.controller.combinePlots)
        combinebtn.pack(padx=5, in_=btn_Frame, side=tk.LEFT)

    def displayWaveform(self, model):
        # remove load file button
        self.loadfilebtn.destroy()
        # add new buttons
        self.addbtns()
        # resize window
        self.root.geometry("600x600")
        # add figure of waveform to figures
        self.figures.append(Figure(figsize=(6, 5), dpi=100))
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
        toolbar = NavigationToolbar2Tk(self.canvas, self.root)
        toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP)

    def clearPrevPlot(self):
        # clear the canvas, so we can update it with another graph
        self.canvas.get_tk_widget().destroy()

    def genRT60plots(self, type):
        self.figures.append(Figure(figsize=(6, 5), dpi=100))
        plot1 = self.figures[type+1].add_subplot(111)
        plot1.plot(self.controller.model.t, self.controller.model.dBdata[type])
        plot1.set_xlabel("Time [s]")
        plot1.set_ylabel("Intensity dB")
        title_str= ""
        if type == 0:
            title_str = "Low"
        elif type == 1:
            title_str = "Mid"
        elif type == 2:
            title_str = "High"
        plot1.set_title("RT60 for " + title_str)
        iom = self.controller.model.maxValueIndex[type]
        ioml5 = self.controller.model.RT60Stuff[type][0]
        ioml25 = self.controller.model.RT60Stuff[type][1]
        plot1.plot(self.controller.model.t[iom],self.controller.model.dBdata[type][iom],'go')
        plot1.plot(self.controller.model.t[ioml5],self.controller.model.dBdata[type][ioml5],'yo')
        plot1.plot(self.controller.model.t[ioml25],self.controller.model.dBdata[type][ioml25],'ro')

    def drawNextCanvas(self,type):
        self.canvas = FigureCanvasTkAgg(self.figures[type], master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP)