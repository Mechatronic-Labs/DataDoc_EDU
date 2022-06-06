__author__ = 'Tapsas Apostolos', 'Valiakos Apostolos'
import numpy as np
from mpl_toolkits import mplot3d
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from scipy import stats
from tkinter import *
from tkinter import messagebox as tkMessageBox
from tkinter import ttk
from tabulate import tabulate
from pandastable import Table
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
import pandas as pd

class Scatter_Plot:
    def __init__(self,df):
        # Save Dataframe, values and columns in variables
        self.df = df
        self.df = self.df.dropna()
        self.d = df.to_numpy()
        self.names = list(df.columns.values)
        self.statsBut = False
        self.showedTable = False
        self.timesPressed = 0
        self.showButtonPressed = False
        self.master_isdestroed = 0
        self.selectGraph = False
        self.oldDim = 0
        self.dim = 0

        # Create window
        self.root = Tk()
        self.root.geometry("800x500")
        self.root.configure(background = '#5c94c5')
        self.root.title("Scatter Plot Creator")

        self.names.insert(0, self.names[0])

        # Initialize Frames
        self.top_f = Frame(self.root, background = 'white')
        self.top_f.pack(side = BOTTOM)

        right_f = Frame(self.root,background = '#ff4d4d')     
        right_f.pack(side = RIGHT)
        
        left_f = Frame(self.root,background = "white")
        left_f.pack(side = LEFT)
        
        # initialize Labels and buttons
        self.l1 = Label(right_f, font = ('times new roman', 12), text = "Dataset Statistics", bg = '#ff4d4d')
        self.l1.pack()

        self.pred = ttk.Button(right_f, text = 'Show Characteristics statistics', command = self.st)
        self.pred.pack(side = BOTTOM)
        self.pred.state(["disabled"])
        
        
        self.l2 = Label(right_f, font = ('times new roman', 12), text = "", background = '#ff4d4d')
        self.l2.pack()

        self.style = ttk.Style()
        self.style.configure('TButton', background = 'dodgerblue')

        top_f = Frame(self.root,background = 'white')
        top_f.pack(side = TOP)
       
        self.plot_btn = ttk.Button(self.top_f, text = 'Create Two Dimensions Scatter Plot', command = self.create_2d_plot)
        self.plot_btn.pack(side = LEFT, ipady = 5, ipadx = 5)

        self.plot_btn1 = ttk.Button(self.top_f, text='Create Three Dimensions Scatter Plot',command = self.create_3d_plot)
        self.plot_btn1.pack(side = LEFT, ipady = 5, ipadx = 5)

        self.close = ttk.Button(self.top_f, text = 'Close', command = self.close_program)
        self.close.pack(side = LEFT, ipady = 5, ipadx = 5)

        # Create subplot and set Titles in axes
        self.f = Figure(figsize = (10, 6), dpi = 100)
        self.ax = self.f.add_subplot(111)
        self.ax.clear()        
        self.ax.title.set_text("Scatter Plot")
        self.ax.set_xlabel(" ? ")
        self.ax.set_ylabel(" ? ")

        # Draw in Canvas
        self.canvas = FigureCanvasTkAgg(self.f, self.root)
        self.canvas.get_tk_widget().configure(background = 'dodgerblue',  highlightcolor = '#ff4d4d', highlightbackground = '#ff4d4d')
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side = BOTTOM, fill = BOTH, expand = True)

        toolbar = NavigationToolbar2Tk(self.canvas, self.root)
        toolbar.update()
        self.canvas._tkcanvas.pack(side = TOP, fill = BOTH, expand = True)
        self.root.bind('<Escape>', lambda e: self.close_program)
        self.root.protocol("WM_DELETE_WINDOW", self.close_program)
        mainloop()

    def create_2d_plot(self):
        # Set this as the first option
        self.oldDim = self.dim
        self.dim = 1
        self.selectGraph = True
        # Disable buttons
        self.plot_btn.state(["disabled"])
        self.plot_btn1.state(["disabled"])
        self.pred.state(["disabled"])
        self.close.state(["disabled"])
        # Create Window
        self.master = Tk()
        self.master.title("Create 2D Scater Plot")
        self.master.geometry('700x200')
        self.master.configure(background = 'white')

                      
        self.master.protocol('WM_DELETE_WINDOW', self.master_destroed)  # root is your root window
        self.master.bind('<Escape>', lambda e: self.master_destroed)

        self.v = StringVar(self.master)
        self.v.set(self.names[0]) # default value

        self.v1 = StringVar(self.master)
        self.v1.set(self.names[0]) # default value

        # Set options for colors
        self.colors = {'blue': 'b','green': 'g','red':'r','cyan':'c','magenta':'m','yellow':'y','black':'k','white':'w'}

        self.descriptions = {'circle marker' : 'o','solid line style' : '-', 'dashed line style' : '--','dash-dot line style' : '-.','dotted line style' : ':', 'point marker' : '.',
                            'pixel marker' : ',','triangle_down marker' :'v','triangle_up marker':'^','triangle_left marker':'<','triangle_right marker':'>','tri_down marker':'1',
                            'tri_up marker':'2','tri_left marker':'3','tri_right marker':'4','square marker':'s','pentagon marker':'p','star marker':'*','hexagon1 marker':'h',
                            'hexagon2 marker':'H','plus marker':'+','x marker':'x','diamond marker':'D','thin_diamond marker':'d','vline marker':'|','hline marker':'_'}

        self.des = StringVar(self.master)
        self.des.set('circle marker') # default value

        self.col = StringVar(self.master)
        self.col.set('blue') # default value

        # Place labels and buttons
        Label(self.master, font = ('times new roman', 10), text = "Select first attribute:", bg = '#ffffff').grid(row = 0, column = 0)
        ttk.OptionMenu(self.master, self.v, *self.names).grid(row = 0, column = 1, ipady = 5, ipadx = 5)

        Label(self.master, font = ('times new roman', 10), text = "Select secont attribute:", bg ='#ffffff').grid(row = 0, column = 2)
        ttk.OptionMenu(self.master, self.v1, *self.names).grid(row = 0, column =3, ipady = 5, ipadx = 5)

        Label(self.master, font = ('times new roman', 10), text = "Select color:", bg = '#ffffff').grid(row = 1, column = 0)
        ttk.OptionMenu(self.master, self.col, *self.colors.keys()).grid(row = 1, column = 1, ipady = 5, ipadx = 5)

        Label(self.master, font = ('times new roman', 10), text = "Select description:",bg='#ffffff').grid(row = 1, column = 2)
        ttk.OptionMenu(self.master, self.des, *self.descriptions.keys()).grid(row = 1, column = 3, ipady = 5, ipadx = 5)

        ttk.Button(self.master, text='Show', command = self.show).grid(row = 3, column = 0, sticky = W, pady = 4, ipady = 2, ipadx = 4)
        ttk.Button(self.master, text='Quit', command = self.master_destroed).grid(row = 3, column = 1, sticky = W, pady = 4, ipady = 2, ipadx = 4)

        mainloop()


    def create_3d_plot(self):
        # Set this as the Second option
        self.oldDim = self.dim
        self.dim = 2
        self.selectGraph = True
      
        # Disable Buttons
        self.plot_btn.state(["disabled"])
        self.pred.state(["disabled"])
        self.plot_btn1.state(["disabled"])
        self.close.state(["disabled"])

        # Create Window
        self.master = Tk()
        self.master.title("Create 3D Scater Plot")
        self.master.geometry('700x200')
            
        self.master.protocol('WM_DELETE_WINDOW', self.master_destroed)  # root is your root window
        self.master.bind('<Escape>', lambda e: self.master_destroed)

        self.master.configure(background='white')

        self.v = StringVar(self.master)
        self.v.set(self.names[0]) # default value

        self.v1 = StringVar(self.master)
        self.v1.set(self.names[0]) # default value

        self.v2 = StringVar(self.master)
        self.v2.set(self.names[0]) # default value

        # Set options for colors and markers
        self.colors = {'blue': 'b','green': 'g','red':'r','cyan':'c','magenta':'m','yellow':'y','black':'k','white':'w'}

        self.descriptions = {'circle marker' : 'o','solid line style' : '-', 'dashed line style' : '--','dash-dot line style' : '-.','dotted line style' : ':', 'point marker' : '.',
                            'pixel marker' : ',','triangle_down marker' :'v','triangle_up marker':'^','triangle_left marker':'<','triangle_right marker':'>','tri_down marker':'1',
                            'tri_up marker':'2','tri_left marker':'3','tri_right marker':'4','square marker':'s','pentagon marker':'p','star marker':'*','hexagon1 marker':'h',
                            'hexagon2 marker':'H','plus marker':'+','x marker':'x','diamond marker':'D','thin_diamond marker':'d','vline marker':'|','hline marker':'_'}

        self.des = StringVar(self.master)
        self.des.set('circle marker') # default value

        self.col = StringVar(self.master)
        self.col.set('blue') # default value


        # Place Labels and Buttons
        Label(self.master, font = ('times new roman', 10), text = "Select first attribute:", bg = '#ffffff').grid(row = 0, column = 0)
        ttk.OptionMenu(self.master, self.v, *self.names).grid(row = 0, column = 1, ipady = 5, ipadx = 5)

        Label(self.master, font = ('times new roman', 10), text = "Select secont attribute:", bg = '#ffffff').grid(row = 0, column = 2)
        ttk.OptionMenu(self.master, self.v1, *self.names).grid(row=0, column = 3, ipady = 5, ipadx = 5)

        Label(self.master, font = ('times new roman', 10), text = "Select third attribute:", bg = '#ffffff').grid(row = 0, column = 4)
        ttk.OptionMenu(self.master, self.v2, *self.names).grid(row = 0, column = 5, ipady = 5, ipadx = 5)

        Label(self.master, font = ('times new roman', 10), text = "Select color:", bg = '#ffffff').grid(row = 1, column = 0)
        ttk.OptionMenu(self.master, self.col, *self.colors.keys()).grid(row = 1, column = 1, ipady = 5, ipadx = 5)

        Label(self.master, font = ('times new roman', 10), text = "Select description:", bg = '#ffffff').grid(row = 1, column = 2)
        ttk.OptionMenu(self.master, self.des, *self.descriptions.keys()).grid(row = 1, column = 3, ipady = 5, ipadx = 5)

        ttk.Button(self.master, text = 'Show', command = self.show).grid(row = 3, column = 0, sticky = W, pady = 4, ipady = 2, ipadx = 4)
        ttk.Button(self.master, text = 'Quit', command = self.master_destroed).grid(row = 3, column = 1, sticky = W, pady = 4, ipady = 2, ipadx = 4)

        mainloop()

            
    def cl(self):
        # Enable Buttons
        self.close.state(["!disabled"])
        self.plot_btn.state(["!disabled"])
        if(self.showButtonPressed):
            self.pred.state(["!disabled"])
        self.plot_btn1.state(["!disabled"])
        self.master.destroy()
        self.dim = self.oldDim

            
    def show(self):
        self.showButtonPressed = True
        self.statsBut = True
        # Destroy parent Window
        self.master.destroy()
        # Enable Buttons
        self.plot_btn.state(["!disabled"])
        self.pred.state(["!disabled"])
        self.plot_btn1.state(["!disabled"])
        self.close.state(["!disabled"]) 
        self.p = self.colors[self.col.get()] + self.descriptions[self.des.get()]
        # In Case of user selects the first option
        if self.dim == 1:                  
            val = self.v.get()
            val1 = self.v1.get()
            if val.isdigit():
                val = int(val)
                x = self.df[val]
            else:
                x = self.df[val].values
            if val1.isdigit():
                val1 = int(val1)
                y = self.df[val1]
            else:
                y = self.df[val1].values
        # Clear canvas and set titles
                self.ax.clear()
                self.f.clf()
                self.ax = self.f.add_subplot(111)
                self.ax.title.set_text("2D Scatter Plot")
                self.ax.set_xlabel(str(val))
                self.ax.set_ylabel(str(val1))
                self.ax.plot(x,y,self.p)
                self.canvas.draw()

                k  = np.std(x) / np.mean(x)
                kk = np.std(y) / np.mean(y)
        # Set results on table
                self.table = [["df ",len(x),len(y)],["Standard Error",str("%.2f" % stats.sem(x)),str("%.2f" % stats.sem(y))],
                        ["Minimum",str("%.2f" % np.min(x)),str("%.2f" % np.min(y))],["Maximum",str("%.2f" % np.max(x)),str("%.2f" % np.max(y))],
                        ["Mean",str("%.2f" % np.mean(x)),str("%.2f" % np.mean(y))],["Median",str("%.2f" % np.median(x)),str("%.2f" % np.median(y))],
                        ["Standard Dev ",str("%.2f" % np.std(x)),str("%.2f" % np.std(y))],["CV",str("%.2f" % k),str("%.2f" % kk)]]

                tabulate.PRESERVE_WHITESPACE = True
              
        # in case of user selects the second option
        else:
            # Save user options in variables
            val  = self.v.get()
            val1 = self.v1.get()
            val2 = self.v2.get()
            if val.isdigit():
                val = int(val)
                x = self.df[val]
            else:
                x = self.df[val].values
            if val1.isdigit():
                val1 = int(val1)
                y = self.df[val1]
            else:
                y = self.df[val1].values
            if val2.isdigit():
                val2 = int(val2)
                z = self.df[val2]
            else:
                z = self.df[val2].values

        # Clear Canvas and set titles and then draw
            self.ax.clear()
            self.f.clf()
            self.ax = self.f.add_subplot(111, projection = "3d")
            self.ax.title.set_text("3D Scatter Plot")
            self.ax.set_xlabel(str(val))
            self.ax.set_ylabel(str(val1))
            self.ax.set_zlabel(str(val2))
            self.ax.plot3D(x, y, z, self.p)
            self.canvas.draw()

            k   = np.std(x) / np.mean(x)
            kk  = np.std(y) / np.mean(y)
            kkk = np.std(y) / np.mean(z)

        # Save Results in table
            self.table = [["df ",len(x),len(y),len(z)],["Standard Error",str("%.2f" % stats.sem(x)),str("%.2f" % stats.sem(y)),str("%.2f" % stats.sem(z))],
                        ["Minimum",str("%.2f" % np.min(x)),str("%.2f" % np.min(y)),str("%.2f" % np.min(z))],["Maximum",str("%.2f" % np.max(x)),str("%.2f" % np.max(y)),str("%.2f" % np.max(z))],
                        ["Mean",str("%.2f" % np.mean(x)),str("%.2f" % np.mean(y)),str("%.2f" % np.mean(z))],["Median",str("%.2f" % np.median(x)),str("%.2f" % np.median(y)),str("%.2f" % np.median(z))],
                        ["Standard Dev ",str("%.2f" % np.std(x)),str("%.2f" % np.std(y)),str("%.2f" % np.std(z))],["CV",str("%.2f" % k),str("%.2f" % kk),str("%.2f" % kkk)]]

            tabulate.PRESERVE_WHITESPACE = True
                 
    def st(self):
        # Create window For Statistics
        self.master = Tk()
        self.master_isdestroed = 1
        self.master.configure(background='#5c94c5')
        self.master.title("Model Stats")
        self.master.geometry('800x500') 
        self.fra = Frame(self.master)
        self.fra.pack(fill = BOTH, expand = 1)
        
        # Create columns depending on users' option
        if(self.statsBut or self.timesPressed == 0):
            if(self.timesPressed == 0):
                if(self.dim == 1):
                    self.namesForCol = ['Characteristic', self.v.get(), self.v1.get()]
                elif(self.dim == 2):
                    self.namesForCol = ['Characteristic', self.v.get(), self.v1.get(), self.v2.get()]
                else:
                    if(self.dim == 1):
                        self.namesForCol = ['Characteristic', self.v.get(), self.v1.get()]
                    elif(self.dim == 2):
                        self.namesForCol = ['Characteristic', self.v.get(), self.v1.get(), self.v2.get()]
            if(self.showedTable or self.timesPressed == 0 ):
                 df2 = pd.DataFrame(self.table, columns =  self.namesForCol)
                 self.pt = Table(self.fra, dataframe=df2)
            else:
                self.pt = Table(self.fra)
            
        self.pt.columncolors['mycol'] = 'white'
        ttk.Button(self.master, text='Close', command = self.master_destroed).pack(side = RIGHT)
        self.master.bind('<Escape>', lambda e: self.master_destroed)
        self.master.protocol("WM_DELETE_WINDOW", self.master_destroed)
        self.pt.show()
        self.pt.redraw()
        self.showedTable = True
        self.timesPressed = self.timesPressed + 1
            
    def enableButtons(self):
            self.plot_btn.state(["!disabled"])
            self.plot_btn1.state(["!disabled"])
            self.close.state(["!disabled"])
            if(self.statsBut):
                self.pred.state(["!disabled"])
            self.dim = self.oldDim        

    def close_program(self):
        #Checking if child window self.master is active and if it is shows the message to close it first.
        # Note: we use double ifs because we want to avoid the self.master.winfo_exists() == 1 check. 
        # Because when master is destoyed program can not fint self.master window and a bug created.  
        # In order to fix this bug we defined a master destroed function with aim to destroy master and
        # update a flag value named master_destroed.   
        if self.master_isdestroed == 1: 
            if self.master.winfo_exists() == 1: 
                tkMessageBox.showinfo("Important Info", "Child Window is Open Please Close it First.")
        else:
            self.root.destroy()

    def master_destroed(self):
        self.master_isdestroed = 0
        if(self.selectGraph):
            self.selectGraph = False
            self.enableButtons()
        self.master.destroy() 