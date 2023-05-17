import tkinter as tk
from tkinter import ttk


class ReorderableListbox(ttk.Frame):
    def __init__(self, master, items):
        super().__init__(master)
        
        # Create the Treeview widget and add columns
        self.treeview = ttk.Treeview(self, columns=["c1","c2","c3"], selectmode="browse")
        # shrink width of iid column to 0
        self.treeview.column("#0", minwidth=0, width=0)
        # set column headings
        self.treeview.heading("0", text="iid")
        self.treeview.heading("c1", text="Variable")
        self.treeview.heading("c2", text="Operation")
        self.treeview.heading("c3", text="Value")
        
        # Create the Scrollbar widget and associate it with the Treeview
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=scrollbar.set)
        
        # Add the items to the Treeview
        for i, item in enumerate(items):
            self.treeview.insert("", "end", text="", iid=str(i))

        
        # Pack the widgets into the frame
        self.treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind events to enable drag-and-drop reordering of items
        self.treeview.bind("<Button-1>", self.on_select)
        self.treeview.bind("<B1-Motion>", self.on_drag)
        self.treeview.bind("<ButtonRelease-1>", self.on_release)
        self.dragged_iid = None
    
    def on_select(self, event):
        iid = self.treeview.identify_row(event.y)
        if iid != "":
            self.dragged_iid = iid
       
    def on_drag(self, event):
        if self.dragged_iid != None:
            new_index = self.treeview.index(self.treeview.identify_row(event.y))
            if new_index != "":
                self.treeview.move(self.dragged_iid, "", new_index)

    def on_release(self, event):
        self.dragged_iid = None

    def addItem(self, new_item):
        self.treeview.insert("", "end", text=len(self.treeview.get_children()),
                             values=new_item)

    def getFilterOrder(self):
        return [self.treeview.item(iid)['values'] for iid in self.treeview.get_children()]
    
    def combineFilters(self):
        self.final_filters = []
        

