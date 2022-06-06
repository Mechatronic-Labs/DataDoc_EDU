__author__ = 'Tapsas Apostolos', 'Valiakos Apostolos'
import numpy as np
import warnings
warnings.simplefilter(action='ignore', category = FutureWarning)
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from scipy import stats
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as tkMessageBox
from tabulate import tabulate
from pandastable import Table
from mpl_toolkits import mplot3d

import pandas as pd

class Histogram:
      def __init__(self,df):
        # Save Dataframe and separate values and columns
        self.df = df
        self.d=df.to_numpy()
        self.names = list(df.columns.values)
        self.statsBut = False
        self.showedTable = False
        self.timesPressed = 0
        self.showButtonPressed =False
        self.master_isdestroed = 0
        self.selectGraph = False

        self.oldDim = 0
        self.dim = 0
        # Create Window 
        self.root = Tk()
        self.root.geometry("800x500")
        self.root.configure(background = '#5c94c5')
        self.root.title("Histogram Creator")

        self.names.insert(0, self.names[0])

        # Initialize Frames
        self.top_f = Frame(self.root, background = 'white')
        self.top_f.pack(side = BOTTOM)

        right_f = Frame(self.root, background = '#ff4d4d')
        right_f.pack(side = RIGHT)

        top_f = Frame(self.root, background = 'white')
        top_f.pack(side = TOP)

        left_f = Frame(self.root, background = "white")
        left_f.pack(side = LEFT)

        # Initialize labels and buttons
        self.l1 = Label(right_f, font = ('times new roman', 12), text = "Dataset Statistics", bg = '#ff4d4d')
        self.l1.pack()

        self.pred = ttk.Button(right_f, text = 'Show Characteristic statistics', command = self.st)
        self.pred.pack(side = BOTTOM)
        self.pred.state(["disabled"])
        
        self.l2 = Label(right_f, font = ('times new roman', 12), text = "",background = '#ff4d4d')
        self.l2.pack()

        self.style = ttk.Style()
        self.style.configure('TButton', background = 'dodgerblue')

        self.plot_btn = ttk.Button(self.top_f, text = 'Create One Characteristic Histogram', command = self.create_hist_graph)
        self.plot_btn.pack(side = LEFT, ipady = 5, ipadx = 5)

        self.plot_btn1 = ttk.Button(self.top_f, text = 'Create Two Characteristics Histogram', command = self.create_2d_line_graph)
        self.plot_btn1.pack(side = LEFT, ipady = 5, ipadx = 5)

        self.close = ttk.Button(self.top_f, text = 'Close', command = self.close_program)
        self.close.pack(side = LEFT, ipady = 5, ipadx = 5)

        # Create figure clear canvas and set titles        
        self.f = Figure(figsize = (10, 6), dpi = 100)
        self.ax = self.f.add_subplot(111)
        self.ax.clear()
        self.ax.title.set_text("Histogram")
        self.ax.set_xlabel(" ? ")
        self.ax.set_ylabel(" ? ")

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

      def create_hist_graph(self):
        # Set this as the first option
        self.oldDim = self.dim
        self.dim = 1
        self.selectGraph = True
        # Disable Buttons
        self.plot_btn.state(["disabled"])
        self.plot_btn1.state(["disabled"])
        self.close.state(["disabled"])
        self.pred.state(["disabled"])

        # Create window
        self.master = Tk()
        self.master.title("Create Histogram")
        self.master.geometry('700x200')

        self.master.configure(background = 'white')
                       
        self.master.protocol('WM_DELETE_WINDOW', self.master_destroed)  # root is your root window
        self.master.bind('<Escape>', lambda e: self.master_destroed)

        self.v = StringVar(self.master)
        self.v.set(self.names[0]) # default value

        self.v1 = StringVar(self.master)
        self.v1.set(self.names[0]) # default value
        # Set options For colors
        self.colors = {'blue': 'b','green': 'g','red':'r','cyan':'c','magenta':'m','yellow':'y','black':'k','white':'w'}

        self.col = StringVar(self.master)
        self.col.set('blue') # default value
            
        # Place Buttons and options
        Label(self.master, font = ('times new roman', 10), text = "Select first attribute:", bg = '#ffffff').grid(row = 0, column = 0)
        ttk.OptionMenu(self.master, self.v, *self.names).grid(row = 0, column = 1, ipady = 5, ipadx = 5)

        Label(self.master, font = ('times new roman', 10), text = "Select color:", bg = '#ffffff').grid(row = 1, column = 0)
        ttk.OptionMenu(self.master, self.col, *self.colors.keys()).grid(row = 1, column = 1, ipady = 5, ipadx = 5)
            
        ttk.Button(self.master, text = 'Show', command = self.show).grid(row = 3, column = 0, sticky = W, pady = 4, ipady = 2, ipadx = 4)
        ttk.Button(self.master, text = 'Quit', command = self.master_destroed).grid(row = 3, column = 1, sticky = W, pady = 4, ipady = 2, ipadx = 4)
            
        mainloop()


      def create_2d_line_graph(self):
        # Set this as the second option
        self.oldDim = self.dim
        self.dim = 2
        self.selectGraph = True
        # Disable Buttons
        self.plot_btn.state(["disabled"])
        self.pred.state(["disabled"])
        self.plot_btn1.state(["disabled"])
        self.close.state(["disabled"])
        # Create window
        self.master = Tk()
        self.master.title("Create Histogram")
        self.master.geometry('700x200')
        self.master.configure(background = 'white')

                   
        self.master.protocol('WM_DELETE_WINDOW', self.master_destroed)  # root is your root window
        self.master.bind('<Escape>', lambda e: self.master_destroed)

        self.v = StringVar(self.master)
        self.v.set(self.names[0]) # default value

        self.v1 = StringVar(self.master)
        self.v1.set(self.names[0]) # default value

        # Set options for Colors
        self.colors = {'blue': 'b','green': 'g','red':'r','cyan':'c','magenta':'m','yellow':'y','black':'k','white':'w'}

        self.des = StringVar(self.master)
        self.des.set('circle marker') # default value

        self.col = StringVar(self.master)
        self.col.set('blue') # default value

        self.col1 = StringVar(self.master)
        self.col1.set('red') # default value

        self.des1 = StringVar(self.master)
        self.des1.set('circle marker') # default value

        # Place Buttons and Labels
        Label(self.master,font=('times new roman',10),text="Select first attribute:",bg='#ffffff').grid(row=0,column=0)
        ttk.OptionMenu(self.master, self.v, *self.names).grid(row=0, column=1,ipady=5, ipadx=5)

        Label(self.master,font=('times new roman',10),text="Select second attribute:",bg='#ffffff').grid(row=0,column=2)
        ttk.OptionMenu(self.master, self.v1, *self.names).grid(row=0, column=3,ipady=5, ipadx=5)

        Label(self.master,font=('times new roman',10),text="First Histogram:",bg='#ffffff').grid(row=1,column=0)

        Label(self.master,font=('times new roman',10),text="Select color:",bg='#ffffff').grid(row=2,column=0)
        ttk.OptionMenu(self.master, self.col, *self.colors.keys()).grid(row=2, column=1,ipady=5, ipadx=5)
 
        Label(self.master,font=('times new roman',10),text="Second Histogram:",bg='#ffffff').grid(row=1,column=2)

        Label(self.master,font=('times new roman',10),text="Select color:",bg='#ffffff').grid(row=2,column=2)
        ttk.OptionMenu(self.master, self.col1, *self.colors.keys()).grid(row=2, column=3,ipady=5, ipadx=5)
            
        ttk.Button(self.master,text='Show', command=self.show).grid(row=5,column=0,sticky=W,pady=4,ipady=2, ipadx=4)
        ttk.Button(self.master,text='Quit', command=self.master_destroed).grid(row=5,column=1,sticky=W,pady=4,ipady=2, ipadx=4)

        mainloop()

            
      def cl(self):
        # Enable Buttons
        self.close.state(["!disabled"])
        self.plot_btn.state(["!disabled"])
        self.plot_btn1.state(["!disabled"])
        if(self.showButtonPressed):
            self.pred.state(["!disabled"])
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
        # if users selects the first option
        if self.dim == 1:
            val = self.v.get()
            val1 = self.v1.get()
            if val.isdigit():
                val = int(val)
                x = self.df[val].values[~np.isnan(self.df[val].values)]
            else:
                x = self.df[val].values[~np.isnan(self.df[val].values)]
        # Clear canvas and place titles
                self.ax.clear()
                self.f.clf()
                self.ax = self.f.add_subplot(111)
                self.ax.title.set_text("Histogram")
                self.ax.set_xlabel(val)
                self.ax.set_ylabel('Probability') 
                self.ax.hist(x,facecolor = self.colors[self.col.get()])
                  
                legend1 = self.ax.legend(loc="upper left")
                self.canvas.draw()

                k = np.std(x)/np.mean(x)
        # Place results in table
                self.table = [["df ",len(x)],["Standard Error",str("%.2f" % stats.sem(x))],
                           ["Minimum",str("%.2f" % np.min(x))],["Maximum",str("%.2f" % np.max(x))],
                           ["Mean",str("%.2f" % np.mean(x))],["Median",str("%.2f" % np.median(x))],
                           ["Standard Dev ",str("%.2f" % np.std(x))],["CV",str("%.2f" % k)]]

                tabulate.PRESERVE_WHITESPACE = True
                # self.l1.configure(text = "Statisics")
                # self.l2.configure(text = tabulate(self.table, headers=["Characteristic",val,val1],tablefmt="gidhub",colalign=("center",)))
        # In case user selects the second option
        else:
            val = self.v.get()
            val1 = self.v1.get()
            if val.isdigit():
                val = int(val)
                x = self.df[val].values[~np.isnan(self.df[val].values)]
            else:
                x = self.df[val].values[~np.isnan(self.df[val].values)]
                if val1.isdigit():
                    val1 = int(val1)
                    y = self.df[val1].values[~np.isnan(self.df[val1].values)]
                else:
                    y = self.df[val1].values[~np.isnan(self.df[val1].values)]

        # Clear canvas and place titles
                self.ax.clear()
                self.f.clf()
                self.ax = self.f.add_subplot(111)
                self.ax.title.set_text("Histogram")
                self.ax.set_xlabel('')
                self.ax.set_ylabel('Propability')
                self.ax.hist(x,color = self.colors[self.col.get()] , label = val)
                self.ax.hist(y,color = self.colors[self.col1.get()] , label = val1)

                legend1 = self.ax.legend(loc="upper left")
                self.canvas.draw()

                k = np.std(x) / np.mean(x)
                kk = np.std(y) / np.mean(y)

        # Place results in table
                self.table = [["df ",len(x),len(y)],["Standard Error",str("%.2f" % stats.sem(x)),str("%.2f" % stats.sem(y))],
                           ["Minimum",str("%.2f" % np.min(x)),str("%.2f" % np.min(y))],["Maximum",str("%.2f" % np.max(x)),str("%.2f" % np.max(y))],
                           ["Mean",str("%.2f" % np.mean(x)),str("%.2f" % np.mean(y))],["Median",str("%.2f" % np.median(x)),str("%.2f" % np.median(y))],
                           ["Standard Dev ",str("%.2f" % np.std(x)),str("%.2f" % np.std(y))],["CV",str("%.2f" % k),str("%.2f" % kk)]]

                tabulate.PRESERVE_WHITESPACE = True
                # self.l1.configure(text = "Statisics")
                # self.l2.configure(text = tabulate(self.table, headers=["Characteristic",val,val1],tablefmt="gidhub",colalign=("center",)))

      def st(self):
        # Create window for model statistics
        self.master_isdestroed = 1
        self.master = Tk()
        self.master.configure(background='#5c94c5')
        self.master.title("Model Stats")
        self.master.geometry('800x500') 
        self.fra = Frame(self.master)
        self.fra.pack(fill = BOTH, expand = 1)
        # Create appropriate window for each user option
        if(self.statsBut or self.timesPressed == 0):
            if(self.timesPressed == 0):
                if(self.dim == 1):
                    self.namesForCol = ['Characteristic', self.v.get()]
                elif(self.dim == 2):
                    self.namesForCol = ['Characteristic', self.v.get(), self.v1.get()]
                else:
                    if(self.dim == 1):
                        self.namesForCol = ['Characteristic', self.v.get()]
                    elif(self.dim == 2):
                        self.namesForCol = ['Characteristic', self.v.get(), self.v1.get()]
            if(self.showedTable or self.timesPressed == 0 ): 
                    df2 = pd.DataFrame(self.table, columns =  self.namesForCol)
                    self.pt = Table(self.fra, dataframe=df2)
        else:
            df2 = pd.DataFrame(self.table)
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
                tkMessageBox.showinfo("Important Info","Child Window is Open Please Close it First.")
        else:
            self.root.destroy()

      def master_destroed(self):
        self.master_isdestroed = 0
        if(self.selectGraph):
            self.selectGraph = False
            self.enableButtons()
        self.master.destroy()                          
# Histogram(df)
