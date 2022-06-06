__author__ = 'Tapsas Apostolos', 'Valiakos Apostolos'
import os
import time
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as tkMessageBox
from tkinter import ttk
from tkinter.ttk import Progressbar
from pandastable import Table
import pandas as pd
import scipy.cluster.hierarchy as sch
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from sklearn.cluster import AgglomerativeClustering


class Hierarchical_clustering:

    def __init__(self,df):
        self.df = df
        self.d =  df 
        self.master_isdestroed = 0
        self.master_isdestroed2 = 0
        self.statsBut = False  
        self.selectGraph = False
        self.names = list(df.columns.values)
        self.dim = 0
       
        self.root = Tk()
        self.root.geometry("800x500")
        self.root.configure(background = '#5c94c5')
        self.root.title("Hierarchical Clustering")
        self.root.bind('<Escape>', lambda e: self.close_program)
        self.root.protocol("WM_DELETE_WINDOW", self.close_program)
            
        self.names.insert(0, self.names[0])

        self.top_f = Frame(self.root, background = 'white')
        self.top_f.pack(side = BOTTOM)

        right_f = Frame(self.root, background = '#ff4d4d')
        right_f.pack(side = RIGHT)

        self.l1 = Label(right_f, font = ('times new roman', 12), text = "Model Statistics", bg = '#ff4d4d')
        self.l1.pack()
        
        self.l2 = Label(right_f,font=('times new roman',12), text = "", background = '#ff4d4d')
        self.l2.pack()

        self.style = ttk.Style()
        self.style.configure('TButton', background = 'dodgerblue')

        top_f = Frame(self.root,background = 'white')
        top_f.pack(side = TOP)

        self.plot_btn = ttk.Button(self.top_f, text = 'Hierarchical Clustering', command = self.clu)
        self.plot_btn.pack(side = LEFT, ipady = 5, ipadx = 5)

        self.pred = ttk.Button(right_f, text = 'Show model Statistics', command = self.st)
        self.pred.pack(side = BOTTOM)
        self.pred.state(["disabled"])

        self.close = ttk.Button(self.top_f, text = 'Close', command = self.close_program)
        self.close.pack(side = LEFT, ipady = 5, ipadx = 5)

        left_f = Frame(self.root, background = "white")
        left_f.pack(side = LEFT)
        
        self.f = Figure(figsize = (10, 6), dpi = 100)
        self.ax = self.f.add_subplot(111)
        self.ax.clear()

        self.ax.title.set_text("Illustration")
        self.ax.set_xlabel(" ? ")
        self.ax.set_ylabel(" ? ")

        self.canvas = FigureCanvasTkAgg(self.f, self.root)
        self.canvas.get_tk_widget().configure(background = 'dodgerblue',  highlightcolor = '#ff4d4d', highlightbackground = '#ff4d4d')
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side = BOTTOM, fill = BOTH, expand = True)

        toolbar = NavigationToolbar2Tk(self.canvas, self.root)
        toolbar.update()
        self.canvas._tkcanvas.pack(side = TOP, fill = BOTH, expand = True)

        mainloop()

    def clu(self):
        self.plot_btn.state(["disabled"])
        self.close.state(["disabled"])
        self.master_isdestroed = 1
        self.statsBut = True
        self.selectGraph = True
        
        self.master = Tk()
        self.master.title("Hierarchical")
        self.master.configure(background = 'white')

        self.v1 = StringVar(self.master)
        self.v1.set(len(self.df.values)) # default value

        Label(self.master, font = ('times new roman', 10), text = "Give The Number of Clusters.", bg = '#ffffff').grid(row = 0, column = 0)
        self.option1 = ttk.Entry(self.master, textvariable = self.v1, width = 10)
        self.option1.grid(row = 0, column = 1)
        
        style = ttk.Style()
        style.configure("red.Horizontal.TProgressbar", foreground = 'red', background = '#03b6fc')
        self.bar = Progressbar(self.master, length = 220, style = 'red.Horizontal.TProgressbar')
        self.bar.grid(column = 0, row = 2)
        
        self.el = ttk.Button(self.master, text = 'Create Dendrogram',command = self.el) 
        self.el.grid(row = 4, column = 0, sticky = W, pady = 4, ipady = 2, ipadx = 4)
        ttk.Button(self.master, text = 'Show', command = self.vizu).grid(row = 4, column = 1, sticky = W, pady = 4, ipady = 2, ipadx = 4)
        ttk.Button(self.master, text = 'Quit', command = self.master_destroed).grid(row = 4, column = 2, sticky = W, pady = 4, ipady = 2, ipadx = 4)
        
        self.master.bind('<Escape>', lambda e: self.master_destroed)
        self.master.protocol("WM_DELETE_WINDOW", self.master_destroed)
        
        mainloop()
        
    def vizu(self):        
        self.close.state(["!disabled"])
        self.plot_btn.state(["!disabled"])
        self.pred.state(["!disabled"])

        # handle dummy variables
        self.df = pd.get_dummies(self.df)

        self.statsBut = True

        # Fitting the Heratical model model to the dataset 
        hc = AgglomerativeClustering(n_clusters = int(self.v1.get()), affinity = 'euclidean', linkage = 'ward')
        self.yk = hc.fit_predict(self.df.values)
        self.model = hc    
        self.ax.clear()
        self.ax.title.set_text("Clusters of Dataset")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.scatter(self.df.values[:,0], self.df.values[:,1], c = self.yk , s=50, cmap = 'rainbow', label = 'Values')
        self.ax.legend(loc = "upper left")
        self.canvas.draw()


    def el(self):
        self.ax.clear()
        self.ax.title.set_text("Dendrogram")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        val = 0

        # Show dendrogram
        for i in range(0, 5):
            self.bar['value'] = val
            self.master.update_idletasks()
            val= val + 25
            time.sleep(1)
        den = sch.dendrogram(sch.linkage(self.df.values, method = 'ward'), ax = self.ax)
        self.canvas.draw()
    
    def st(self):
        data = []
        self.master_isdestroed = 1
        self.selectGraph = True
        self.root1 = Tk()
        self.root1.withdraw()
        self.filename = fd.askopenfilename(title = "Select file", filetypes = (("all Files", "*.xlsx"),))
        if not self.filename:
            tkMessageBox.showinfo("Info", "The procedure was canceled.")
            self.root1.destroy()
        else:
            try:
                data = pd.read_excel(self.filename)
                tkMessageBox.showinfo("Import", "Data Imported Successfully.")
                self.root1.destroy()
            except ImportError as io:
                self.tkMessageBox.showerror("ImportError", io)
                self.MsgBox = tkMessageBox.askquestion('Install Missing Modules', 'Do you want to install xlrd', icon = 'warning')
                if self.MsgBox == 'yes':
                    os.system("pip install xlrd")
                    tkMessageBox.showinfo("Install", "Your Module Installed Successfully. Now you can import datasets.")
                    self.root1.destroy() 
                else:
                    tkMessageBox.showinfo("Install", "You must Install Missing Modules.")
                    self.root1.destroy()
        self.pred_sample = data
        self.ax.scatter(self.pred_sample.values[:,0], self.pred_sample.values[:,1], c = 'black', marker = "X", s = 80, cmap = 'rainbow', label = 'Your Value')

        self.canvas.draw()

        self.master = Tk()
        self.master.configure(background = '#5c94c5')
        self.master.title("Data Viewer")
        self.master.geometry('800x500') 
        f = Frame(self.master)
        f.pack(fill = BOTH, expand = 1)
        self.pt = Table(f, dataframe = data)
        self.pt.columncolors['mycol'] = 'white'
        self.c = ttk.Button(self.master, text = 'Close', command = self.master_destroed).pack()
        self.master.bind('<Escape>', lambda e: self.master_destroed)
        self.master.protocol("WM_DELETE_WINDOW", self.master_destroed)
        self.pt.show()
        self.pt.redraw()
        self.master.mainloop()

    def enableButtons(self):
        self.plot_btn.state(["!disabled"])
        self.close.state(["!disabled"])
        if(self.statsBut):
            self.pred.state(["!disabled"])

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
        if(self.selectGraph):
            self.selectGraph = False
            self.enableButtons()
        if self.master_isdestroed2 == 1:
            if self.master_pred.winfo_exists() == 1:
                self.master_pred.destroy()
                self.master_isdestroed2 = 0
        else:
            self.master_isdestroed = 0
            self.master.destroy()