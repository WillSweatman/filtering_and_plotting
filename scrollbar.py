import tkinter as tk
from tkinter import ttk


class ReorderableListbox(ttk.Frame):
    def __init__(self, master, items):
        super().__init__(master)
        
        # Create the Treeview widget and add columns
        self.treeview = ttk.Treeview(self, columns=["c1","c2","c3"], selectmode="browse")
        self.treeview.column("#0", width=0)
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
        # Remember the ID of the item that was clicked
        item_id = self.treeview.identify_row(event.y)
        if item_id != "":
            self.dragged_iid = item_id
    
    def on_drag(self, event):
        # Reorder the items as the mouse is dragged
        if self.dragged_iid is not None:
            new_index = self.treeview.index(self.treeview.identify_row(event.y))
            if new_index != "":
                self.treeview.move(self.dragged_iid, "", new_index)
    
    def on_release(self, event):
        # Save the new order of the items
        self.dragged_iid = None
        new_order = [self.treeview.item(iid)['text'] for iid in self.treeview.get_children()]
        #print(new_order)  # replace with your own code to save the new order

    def addItem(self, new_item):
        self.treeview.insert("", "end", values=new_item)

    def getFilterOrder(self):
        return [self.treeview.item(iid)['values'] for iid in self.treeview.get_children()]

