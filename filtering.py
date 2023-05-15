import tkinter as tk
from tkinter import ttk
import scrollbar

class FilterBox(ttk.Frame):
    def __init__(self, master, headers_list, types):
        super().__init__(master)

        tk.Label(master, text='Filtering', font=('Arial', 22)).pack(side=tk.TOP)

        # Create the top frame and add some widgets to it
        self.top_frame = tk.Frame(master, height=100, width=200)
        self.top_frame.pack(side=tk.TOP)

        tk.Label(self.top_frame, text='Filters', font=('Arial', 16))

        # Create the first dropdown menu
        self.options = [types, headers_list]

        # for i, (type, header) in enumerate(zip(self.options[0], self.options[1])):
        #     print(f"Pair {i}: {type}, {header}")


        
        self.var1 = tk.StringVar(self.top_frame)
        self.var1.set("Variable")
        self.var1.trace('w', self.dropdown1_selected) # add trace to call function when dropdown1 is selected
        self.dropdown1 = tk.OptionMenu(self.top_frame, self.var1, *self.options[1])
        self.dropdown1.pack(side=tk.LEFT)

        # Create the second dropdown menu
        self.options2 = [["int, flt, str, bool", "int, flt",
                    "int, flt", "str"], 
                    ["Equals (=)", "Less than (<)", "More than (>)", "Contains (ϵ)"]]
        self.var2 = tk.StringVar(self.top_frame)
        self.var2.set("Operator")
        self.dropdown2 = tk.OptionMenu(self.top_frame, self.var2, 'select variable first!')
        self.dropdown2.pack(side=tk.LEFT)

        # Create the entry widget
        self.entry = tk.Entry(self.top_frame)
        self.entry.pack(side=tk.LEFT)

        # Create the button
        self.button = tk.Button(self.top_frame, text="Submit", command=self.print_array)
        self.button.pack(side=tk.LEFT)

        # Create error label
        self.error_label = tk.Label(self.top_frame)
        self.error_label.pack(side=tk.LEFT)

        # Create the bottom frame and add some widgets to it
        self.bottom_frame = tk.Frame(master, height=100, width=200)
        self.bottom_frame.pack(side=tk.TOP)

        self.reorderable_listbox = scrollbar.ReorderableListbox(self.bottom_frame, [])
        self.reorderable_listbox.pack(side=tk.TOP, expand=True)

    def getOptionsType(self, options, option):
        return options[0][options[1].index(option)]

    def allowedOptions(self, type_var, options):
        allowed_options = []
        for i, op_list in enumerate(options[0]):
            if type(type_var) == list:
                for type_elem in type_var:
                    if type_elem in op_list:
                        if options[1][i] not in allowed_options:
                            allowed_options.append(options[1][i])
            else:
                if type_var in op_list:
                        allowed_options.append(options[1][i])

        return allowed_options

    def is_type(self, x, t):
        try:
            t(x)
            return True
        except:
            return False

    def getEntryType(self, entry):
        if self.is_type(entry, int):
            return "int", int(entry)
        elif self.is_type(entry, float):
            return "flt", float(entry)
        elif entry.lower() in ["true", "false"]:
            return "bool", entry
        
        return "str", entry

    def print_array(self):
        arr = [str(self.var1.get()), str(self.var2.get())]
        entry_type, converted_entry = self.getEntryType(self.entry.get())
        if entry_type in self.getOptionsType(self.options, self.var1.get()):
            arr.append(converted_entry)
            self.reorderable_listbox.addItem(arr)
            self.error_label.config(text="")
        else:
            self.error_label.config(text=f"Error: Invalid type '{entry_type}' for selected filter")

    def dropdown1_selected(self, *args):
        allowed_options = self.allowedOptions(self.getOptionsType(self.options, self.var1.get()), self.options2)
        self.dropdown2['menu'].delete(0, 'end')
        for option in allowed_options:
            self.dropdown2['menu'].add_command(label=option, command=tk._setit(self.var2, option))

    def getFilterList(self):
        return self.reorderable_listbox.getFilterOrder()