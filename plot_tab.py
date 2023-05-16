import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from random import uniform
from typing import Union

# my own custom classes/objects
from custom_colours import *

class PlotTab:
    def __init__(self, parent=None, function_defined=False) -> Union[tk.Frame, None]:
        
        if type(parent)==ttk.Notebook:
            self.plot_tab = tk.Frame(parent)
            parent.add(self.plot_tab, text='Plot')

        elif type(parent)==tk.Frame:
            self.plot_tab = parent

        else:
            tk.messagebox.showerror("Error", "Specified parent needed to plot")
            return None


        self.plot_frame = tk.Frame(self.plot_tab)
        self.plot_frame.pack(expand=True)

        # return prepped frame ready for plotting
        if function_defined:
            return self.plot_frame
        
        # else plot the random data
        self.plotExampleData()

        return

    def plotExampleData(self):
        
        # destroy anything plot-related within 1000 miles of the tkinter window
        plt.close()
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        # generate random data
        x = [uniform(0, 5) for _ in range(5)]
        y = [uniform(0, 5) for _ in range(5)]

        # plot example data
        fig, ax = plt.subplots()
        ax.scatter(x, y)
        ax.set_title("Example Plot")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        plt.tight_layout()

        # display the plot in the plot frame
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()