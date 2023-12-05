# make the program appealing to the user, things the
# user can interact with that will be implemented in controller
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np


class View:
    def __init__(self, controller):
        self.controller = controller
        self.root = None
        self.loadfilebtn = None

    # create the inital window
    def initgui(self):
        # create window and title it Acoustic Modeling
        self.root = tk.Tk()
        self.root.title("Acoustic Modeling")
        self.root.geometry("200x100")

        # create button for loading file which is implemented in acoustic_controller.py
        self.loadfilebtn = tk.Button(self.root, text="Load Audio File", command=self.controller.LoadFile)
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

    def displayWaveform(self, model):
        time = np.linspace(0., model.data.shape[0] / model.samplerate, model.data.shape[0])
        if model.numChannels == 2:
            plt.plot(time, model.data[:, 0], label="Left channel")
            plt.plot(time, model.data[:, 1], label="Right channel")
        else:
            plt.plot(time, model.data, label="Audio")
        plt.legend()
        plt.xlabel("Time [s]")
        plt.ylabel("Amplitude")
        plt.show()
