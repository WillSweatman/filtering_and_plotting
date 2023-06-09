import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from random import uniform
from typing import Callable

# my own custom classes/objects
from custom_colours import *

class PlotTab:
    def __init__(self, updateOptionsListFunction:Callable, instance=0, parent=None, function:Callable=None):
        
        # called when a tab is closed
        self.updateList = updateOptionsListFunction

        # where is this tab being placed
        if isinstance(parent, ttk.Notebook):
            self.plot_notebook = parent
            self.plot_tab = tk.Frame(parent)
            parent.add(self.plot_tab, text="Plot "+str(instance))
        elif isinstance(parent, tk.Frame):
            self.plot_notebook = parent.nametowidget(parent.winfo_parent())
            self.plot_tab = parent

        # close tab button at top of tab frame
        self.close_button = tk.Button(self.plot_tab, text="Close Tab", command=self.closeTab,
                                      bg=danger, fg=black)
        self.close_button.pack(anchor=tk.NE)

        # plot frame within tab
        self.plot_frame = tk.Frame(self.plot_tab)
        self.plot_frame.pack(expand=True)

        # use function, or plot example
        self.checkForFunction(function)
        
    def checkForFunction(self, function):
        # plot example data if nothing given
        if function==None:
            self.plotExampleData()
            return

        # if not, call the plotting function with the new plot frame
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

    def updateTab(self, function:Callable=None):
        # destroy all widgets in the plot frame
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        # note that the close button is in plot_tab, not plot_frame,
        # so it doesnt need to be recreated, it continues to exist

        # use function, or plot example
        self.checkForFunction(function)

    def closeTab(self):
        # find id of tab, get notebook to remove it
        index = self.plot_notebook.index(self.plot_tab)
        self.plot_notebook.forget(index)
        self.updateList()