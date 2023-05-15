from gui_window import *

# Create the main application window
root = tk.Tk()
root.title("Main Window")

# Create an instance of the custom window class
my_window = MyWindow(root)

# Start the main event loop
root.mainloop()

print("**End**")