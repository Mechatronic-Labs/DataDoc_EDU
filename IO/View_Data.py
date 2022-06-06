__author__ = 'Tapsas Apostolos', 'Valiakos Apostolos'
from tkinter import *
from pandastable import Table
from tkinter import ttk

class Data_viewer:
    def __init__(self,df):
        self.df = df
        self.root = Tk(className = 'Data Viewer')
        self.root.configure(background='#5c94c5')
        self.root.title("Data Viewer")
    
        self.f = Frame(self.root)
        self.f.pack(fill=BOTH,expand=1)
        self.pt = Table(self.f, dataframe = self.df)
        self.pt.columncolors['mycol'] = 'white'
        self.close = ttk.Button(self.root, text='Close', command = self.root.destroy).pack()
        self.pt.show()
        self.pt.redraw()
        
        #Set fullscreen key
        self.root.bind('<f>', lambda event: self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen")))
        self.root.bind('<Escape>', lambda e: self.root.destroy())
        self.root.mainloop()

