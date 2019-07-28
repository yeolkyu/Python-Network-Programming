import sys
from tkinter import *

class BasicClass:
    def __init__(self):
        root = Tk()
        button = Button(root, text = "Press to quit", command=self.quit)
        button.pack()
        
    def quit(self):
        print("Leaving now...")
        sys.exit()
        
BasicClass()
mainloop()
