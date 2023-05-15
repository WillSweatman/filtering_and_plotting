import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

def getHeaders(header_row):
    headers = []
    #print("index  header_label")

    index = 0
    for label in header_row:
        headers.append(label)
        """
        # everything below is concerning formatting the print output
        pten = 0 # power of ten of index
        if index > 0:
            pten = math.floor(math.log10(index))
        # " "*(3-pten) accounts for max excel columns of order 10^4 (5 digits)
        print(" "*(3-pten),index,"",label)
        """
        index += 1

    return headers

def printData(array):
    print(array)

def transposeData(array):
    transposed_list = []
    transposed_types = []

    for i in range(len(array[0])):
        type_found = False
        transposed_row = []
        for row in array:
            try:
                value = float(row[i])
                if value.is_integer() and not isinstance(value, int):
                    transposed_row.append(int(value))
                    if not type_found:
                        transposed_types.append("int")
                        type_found = True
                else:
                    transposed_row.append(value)
                    if not type_found: 
                        transposed_types.append(["int", "flt"])
                        type_found = True
            except ValueError:
                if not isinstance(row[i], (str)):
                    transposed_row.append(None)
                    if not type_found: 
                        transposed_types.append("unknown")
                        type_found = True
                else:
                    transposed_row.append(row[i])
                    if not type_found:
                        if row[i].lower() in ["true", "false"]:
                            transposed_types.append("bool")
                        else:
                            transposed_types.append("str")
                        type_found = True

        transposed_list.append(transposed_row)

    #return transposed lists of type and value
    return transposed_list, transposed_types

def openCSV():
    file_path = os.path.dirname(__file__) + "\\citibike-stations.csv"

    headers_list = []
    data = []

    with open(file_path, newline='') as csvfile:
        #print("csv opened")
        spamreader = csv.reader(csvfile, delimiter=',')
        header_present = True
        for row in spamreader:
            if header_present:
                headers_list = getHeaders(row)
                header_present = False
                continue

            data.append(row)


    #print(len(data),"rows from csv loaded")
    t_data, types = transposeData(data)
    return t_data, types, headers_list

def on_closing(self):
        
        # Get a list of all the figure numbers
        fig_total = plt.get_fignums()
        #print("Graphs created:",len(fig_total))

        # Loop over the figure numbers and close each figure
        for fig_num in fig_total:
            fig = plt.figure(fig_num)
            plt.close(fig)

        # Close main window
        self.master.destroy()