__author__ = 'Tapsas Apostolos', 'Valiakos Apostolos'
from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

class Pie_Chart:
    def __init__(self,df):
        self.df = df
        self.d=df.to_numpy()
        self.names = list(df.columns.values)
        self.dim = 0   
        
        self.root = Tk()
        self.root.geometry("800x500")
        self.root.configure(background = '#5c94c5')
        self.root.title("Pie Chart Creator")

        self.names.insert(0, self.names[0])

        self.top_f = Frame(self.root,background = 'white')
        self.top_f.pack(side = BOTTOM)
        
        right_f = Frame(self.root, background = '#ff4d4d')
        right_f.pack(side = RIGHT)

        self.l1 = Label(right_f, font = ('times new roman', 12), text = "Dataset Statistics", bg='#ff4d4d')
        self.l1.pack()
        
        self.l2 = Label(right_f, font = ('times new roman', 12), text = "", background = '#ff4d4d')
        self.l2.pack()

        self.style = ttk.Style()
        self.style.configure('TButton', background = 'dodgerblue')

        top_f = Frame(self.root,background = 'white')
        top_f.pack(side = TOP)
        
        self.plot_btn = ttk.Button(self.top_f, text = 'Create Pie Chart', command = self.create_pie_graph)
        self.plot_btn.pack(side = LEFT, ipady = 5, ipadx = 5)

        self.close = ttk.Button(self.top_f, text='Close', command = self.root.destroy)
        self.close.pack(side = LEFT, ipady = 5, ipadx = 5)

        left_f = Frame(self.root,background = "white")
        left_f.pack(side = LEFT)
        
        self.f = Figure(figsize = (10, 6), dpi = 100)
        self.ax = self.f.add_subplot(111)
        self.ax.clear()        
        self.ax.title.set_text("Pie Chart")
        self.ax.set_xlabel(" ? ")
        self.ax.set_ylabel(" ? ")

        self.canvas = FigureCanvasTkAgg(self.f, self.root)
        self.canvas.get_tk_widget().configure(background = 'dodgerblue',  highlightcolor = '#ff4d4d', highlightbackground = '#ff4d4d')
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side = BOTTOM, fill = BOTH, expand = True)

        toolbar = NavigationToolbar2Tk(self.canvas, self.root)
        toolbar.update()
        self.canvas._tkcanvas.pack(side = TOP, fill = BOTH, expand = True)
        self.root.bind('<Escape>', lambda e: self.root.destroy())
        mainloop()

    def create_pie_graph(self):       
        size = []
        for i in range(0,len(self.names) - 1):
            size.append(len(self.df.values[:, i]))
        self.ax.clear()
        self.ax.title.set_text("Pie Chart")
        self.ax.set_xlabel("")
        self.ax.set_ylabel("")
        patches = self.ax.pie(size, labels = self.df.columns.values, autopct = '%1.1f%%', shadow = True, startangle = 90)        
        self.ax.axis('equal')
        self.canvas.draw()
        
        

  

        





