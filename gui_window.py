import custom_funcs
import filtering
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# custom scripts
from plot_tab import PlotTab

class MainWindow(tk.Tk):
    def __init__(self):
        # Set up window
        super().__init__()
        self.title("My Window")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(side=tk.TOP, fill='both', expand=True)
        self.tab1 = tk.Frame(self.notebook)
        self.notebook.add(self.tab1, text='Data and Filtering')
        
        # Open data and save it
        self.data, self.types, self.headers_list = custom_funcs.openCSV()

        self.data_filtered = self.data
        
        """Data Entry"""

        # Add a label to the window
        data_label = tk.Label(self.tab1, text="Pick Data", font=('Arial', 22))
        data_label.pack(padx=20, pady=20)

        # Add a Frame to hold the Combobox widgets
        data_frame = tk.Frame(self.tab1)
        data_frame.pack()

        # Add a Combobox widget for x data
        self.combo_var_x = tk.StringVar()
        self.combo_x = ttk.Combobox(data_frame, textvariable = self.combo_var_x,
                                    state="readonly", exportselection=False)
        self.combo_x.set("X data")
        self.combo_x.pack(side = tk.LEFT, padx=20, pady=20)

        # Add a Combobox widget for y data
        self.combo_var_y = tk.StringVar()
        self.combo_y = ttk.Combobox(data_frame, textvariable = self.combo_var_y,
                                    state="readonly", exportselection=False)
        self.combo_y.set("Y data")
        self.combo_y.pack(side = tk.LEFT, padx=20, pady=20)

        # Add a Combobox widget for colour data
        self.combo_var_c = tk.StringVar()
        self.combo_c = ttk.Combobox(data_frame, textvariable = self.combo_var_c,
                                    state="readonly", exportselection=False)
        self.combo_c.set("Colour data")
        self.combo_c.pack(side = tk.LEFT, padx=20, pady=20)
        
        # Populate the Combobox with data
        self.populateCombo(self.combo_x)
        self.populateCombo(self.combo_y)
        self.populateCombo(self.combo_c)

        """Filtering"""

        #self.findDataTypes()
        
        self.filter_frame = tk.Frame(self.tab1)
        self.filter_frame.pack(pady=10)

        self.filter_box = filtering.FilterBox(self.filter_frame, self.headers_list, self.types)




        """Plotting"""
        self.plot_instance = 0

        # button to plot the data
        self.plot_button = tk.Button(self.tab1, text="Plot New", command=self.plotData)
        self.plot_button.pack()

        # update plot frame
        self.update_frame = tk.Frame(self.tab1)

        # toggle frame visibility based on the presence of any plot frames
        self.toggleFrameVisibility(self.update_frame, len(self.notebook.tabs()) <= 1)

         # some helpful text
        self.or_label = tk.Label(self.update_frame, text="OR Update Existing")
        self.or_label.pack()

        # variable to store the selected option
        self.tab_options = tk.StringVar(self)

        # define options
        self.options = [self.notebook.tab(tab)['text'] for tab in self.notebook.tabs()]

        # default value for the dropdown
        self.tab_options.set("Select an option")

        #dropdown to select plot frame to update
        self.tabs_dropdown = tk.OptionMenu(self.update_frame, self.tab_options, *self.options)
        self.tabs_dropdown.pack()

        # button to update plot with changes
        self.plot_button = tk.Button(self.update_frame, text="Update", command=self.plotData)
        self.plot_button.pack()

    def toggleFrameVisibility(self, frame:tk.Frame, condition:bool):
        if condition:
            frame.pack_forget()
        else:
            frame.pack()

    def on_closing(self):
        
        # Get a list of all the figure numbers
        fig_total = plt.get_fignums()
        #print("Graphs created:",len(fig_total))

        # Loop over the figure numbers and close each figure
        for fig_num in fig_total:
            fig = plt.figure(fig_num)
            plt.close(fig)

        # Close main window
        self.destroy()

    def populateCombo(self, combo):
        # This line allows all data, not just int/float
        #combo['values'] = self.headers_list

        # Call the function to get the data and set it as the values for the Combobox
        valid_headers = []
        for header in self.headers_list:
            # error here if the first element in a row passes, but another doesnt
            data_type = type(self.data[self.headers_list.index(header)][0])
            if data_type == int or data_type == float:
                valid_headers.append(header)

        combo['values'] = valid_headers

    def applyFilters(self):

        # reset data to originl, ready to apply filters
        self.data_filtered = []
        for i in range(len(self.data)):
            self.data_filtered.append([])

        # get filters
        current_filters = self.filter_box.getFilterList()
        # indices we will scrap (not display)
        scrapped_indices = []

        # apply filters
        for fil in current_filters:
            check_value = self.filter_box.getEntryType(fil[2])[1]
            for idx, point in enumerate(self.data[self.headers_list.index(fil[0])]):
                if "=" in fil[1]:
                    if point != check_value:
                        scrapped_indices.append(idx)
                elif "<" in fil[1]:
                    if point >= check_value:
                        scrapped_indices.append(idx)
                elif ">" in fil[1]:
                    if point <= check_value:
                        scrapped_indices.append(idx)
                elif "ϵ" in fil[1]:
                    if check_value not in point:
                        scrapped_indices.append(idx)


        for idx in range(len(self.data[0])):
            if idx not in scrapped_indices:
                for col in range(len(self.data)):
                    self.data_filtered[col].append(self.data[col][idx])

    def plotData(self):
        
        self.plot_instance += 1

        if self.combo_var_x.get() == "X data" or self.combo_var_y.get() == "Y data":
            tk.messagebox.showerror("Error", "Missing X and/or Y data, example used instead")
            PlotTab(self.updateTabOptions, self.plot_instance, self.notebook)
        else:
            PlotTab(self.updateTabOptions, self.plot_instance, self.notebook, self.plotFiltered)

        # add new tab to tab options list
        self.updateTabOptions()

        # select new tab
        last_tab_index = self.notebook.index("end") - 1
        self.notebook.select(last_tab_index) 
        
    def updateTabOptions(self):
        # toggle frame visibility based on the presence of any plot frames
        self.toggleFrameVisibility(self.update_frame, len(self.notebook.tabs()) <= 1)

        # update tab options
        self.options = [self.notebook.tab(tab)['text'] for tab in self.notebook.tabs()[1:]]

        self.tabs_dropdown["menu"].delete(0, "end")
        for option in self.options:
            self.tabs_dropdown["menu"].add_command(label=option, command=tk._setit(self.tab_options, option))

    def updatePlot(self):
        pass
    
    def plotFiltered(self, plot_frame):
    
        self.applyFilters()

        # Get the x and y data from the combo boxes
        x_choice = self.combo_var_x.get()
        y_choice = self.combo_var_y.get()
        c_choice = self.combo_var_c.get()
        

        self.x_index = self.headers_list.index(x_choice)
        self.y_index = self.headers_list.index(y_choice)
        

        data_to_plot_x = self.data_filtered[self.x_index]
        data_to_plot_y = self.data_filtered[self.y_index]
        
        fig, ax = plt.subplots()
        if c_choice == "Colour data":
            im = ax.scatter(data_to_plot_x, data_to_plot_y, marker = 'x')
        else:
            self.c_index = self.headers_list.index(c_choice)
            data_to_plot_c = self.data_filtered[self.c_index]
            im = ax.scatter(data_to_plot_x, data_to_plot_y, marker = 'x',
                        c = data_to_plot_c, cmap = 'viridis')
            cbar = fig.colorbar(im)
            cbar.ax.set_ylabel(c_choice.capitalize().replace('_', ' '), rotation=0, labelpad=15)

        ax.set_title('Scatter Plot '+str(len(plt.get_fignums())))
        ax.set_xlabel(x_choice.capitalize().replace('_', ' '))
        ax.set_ylabel(y_choice.capitalize().replace('_', ' '))

        ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

        # Clear the plot frame
        plt.close()
        for widget in plot_frame.winfo_children():
            widget.destroy()

        # Display the plot in the plot frame
        canvas = FigureCanvasTkAgg(fig, plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def findDataTypes(self):
        for i in range(len(self.data)):
            print(i, self.data[i][0])





if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()

    print("**End**")