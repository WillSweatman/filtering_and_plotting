import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from random import uniform
from typing import Callable

# my own custom classes/objects
from custom_colours import *

class PlotTab:
    def __init__(self, parent=None, function:Callable=None):
        if isinstance(parent, ttk.Notebook):
            self.plot_tab = tk.Frame(parent)
            parent.add(self.plot_tab, text='Plot')
        elif isinstance(parent, tk.Frame):
            self.plot_tab = parent

        self.plot_frame = tk.Frame(self.plot_tab)
        self.plot_frame.pack(expand=True)

        if function==None:
            self.plotExampleData()
            return

        function(self.plot_frame)

        

    def plotExampleData(self):
        
        # destroy anything plot-related within 1000 miles of the tkinter window
        plt.close()
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        # generate random data
        num = 100
        min, max = 0, 1
        x = [uniform(min, max) for _ in range(num)]
        y = [uniform(min, max) for _ in range(num)]
        z = [uniform(min, max) for _ in range(num)]

        # plot example data
        fig, ax = plt.subplots()
        scatter = ax.scatter(x, y, c=z, vmin=min, vmax=max, cmap="viridis")
        ax.set_title("Example Plot")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        cbar = fig.colorbar(scatter)
        cbar.set_label("z")
        plt.tight_layout()

        # display the plot in the plot frame
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()