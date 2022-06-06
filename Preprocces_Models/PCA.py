__author__ = 'Tapsas Apostolos', 'Valiakos Apostolos'
from tkinter import *
from tkinter import ttk
import numpy as np
import webbrowser
from tkinter import messagebox as tkMessageBox
import pandas as pd
from pandastable import Table
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class pca:
    def __init__(self,df):
        self.df = df
        self.names = list(df.columns.values)
        # We define this variable because there are two cases, in one case user select not characteristic and in other user selects a characteristic
        # usually this characteristic contains datasets class. If we worked with self.names variable we had to put None variable inside
        # thus, we had to pop this variable with aim to show eigenvalues and eigenvalues. Thats create problem because every time user 
        # press the buttons the functions will pop self.names values creating bugs. 
        self.characteristics    = list(df.columns.values)
        self.master_isdestroed  = 0
        self.master_isdestroed1 = 0
        self.master_isdestroed2 = 0
        
        # Define Main Window and set Title
        self.root = Tk()
        self.root.geometry("800x250")
        self.root.configure(background='#5c94c5')
        self.root.title("Principal Components Analysis")
        
        # Insert a Data Item to Avoid Problems
        self.characteristics.insert(0, "None")
        self.characteristics.insert(0, self.characteristics[0])
        
        self.v = StringVar(self.root)
        self.v.set(self.characteristics[0]) # set default value first characteristic name

        # Define Frames
        # Top frame         
        top_f = Frame(self.root, background='white')
        top_f.pack(side=TOP)

        # Bottom Frame
        bottom = Frame(self.root,background='#ff4d4d')
        bottom.pack(side = BOTTOM)

        # Define Text 
        Label(top_f, font = ('times new roman', 12), text = 'Please select below the class characteristic if exists:', background = 'white').pack(side = LEFT)
        
        # Define Select List
        ttk.OptionMenu(top_f, self.v, *self.characteristics).pack(side = LEFT) 
        
        # Define Buttons
        self.eigenvals_btn = ttk.Button( top_f, text = "Eigevalues",  command = self.eigenvals)
        self.eigenvals_btn.pack(side = LEFT)
        self.eigenvals_btn.state(["disabled"])

        self.eigenvecs_btn = ttk.Button( top_f, text = "Eigevectors", command = self.eigenvecs)
        self.eigenvecs_btn.pack(side = LEFT)
        self.eigenvecs_btn.state(["disabled"])
        
        ttk.Button( bottom, text="Apply", command = self.pca).pack( side = LEFT )

        ttk.Button( bottom, text="Close",  command = self.close_program).pack( side = LEFT)
        
        self.root.bind('<Escape>', lambda e: self.close_program)
        self.root.protocol("WM_DELETE_WINDOW", self.close_program)
        
        self.root.mainloop()


    def pca(self):
        self.eigenvals_btn.state(["!disabled"])
        self.eigenvecs_btn.state(["!disabled"])
        class_val = self.v.get()

        #remove class values if exists
        if class_val != 'None':
            self.names.remove(class_val)
            self.df = self.df.drop([class_val], axis = 1)
        
        # handle missing values
        self.df = self.df.dropna()

        # handle dummy variables
        self.df = pd.get_dummies(self.df)

        #calculate covariance matrix
        cov = np.cov(self.df.T)
        
        #calculate eigenvector and eigenvalues
        self.eigenval, self.eigenvec = np.linalg.eig(cov)        

        vals, vec = np.linalg.eig(cov) 

        self.posin = []
        self.posout = []
        for i in range(0,len(self.names)):
            p = np.argmax(vals)
            if vals[p] > 1:
                self.posin.append(p)
            else:
                self.posout.append(p)
            vals[p]= - 1

    def kaiser(self):
        webbrowser.open('https://www.researchgate.net/publication/299539108_An_Empirical_Kaiser_Criterion')

    def eigenvals(self):
        #unlist charactaristics name
        self.master = Tk()
        self.master.configure(background = '#5c94c5')
        self.master.title("Normality Test Stats")
        self.master.geometry('800x500') 
        self.fra = Frame(self.master)
        self.fra.pack(fill = BOTH, expand = 1)
        self.master_isdestroed = 1
      
        df2 = pd.DataFrame([self.eigenval], columns = self.names)
        
        self.pt = Table(self.fra, dataframe = df2)
        self.pt.columncolors['mycol'] = 'white'
        self.cl = ttk.Button(self.master, text = 'Close', command = self.master_destroed).pack(side = RIGHT)
        self.cl = ttk.Button(self.master, text = 'PCA Outcome', command = self.info).pack(side = RIGHT)
        self.cl = ttk.Button(self.master, text = 'Eigenvalues Variations', command = self.eigenvals_variations).pack(side = RIGHT)
        self.pt.show()
        self.pt.redraw()

        self.master.bind('<Escape>', lambda e: self.close_program)
        self.master.protocol("WM_DELETE_WINDOW", self.close_program)
        self.master.mainloop()

    def eigenvals_variations(self):
        #unlist charactaristics name
        self.master2 = Tk()
        self.master2.configure(background = '#5c94c5')
        self.master2.title("PCA eigen vectors")
        self.fra = Frame(self.master2)
        self.fra.pack(fill = BOTH, expand = 1)
        self.master_isdestroed2 = 1

        # Define Figure
        fig = Figure(figsize = (10, 6), dpi = 100)
        self.upplot = fig.add_subplot(111)
        self.ax =self.upplot 
        
        # Create Blank Figure and Put X and Y Labels Names and Title
        self.ax.set_title("Eigenvalues Variations")
        y_pos = np.arange(len(self.names))
        self.ax.bar(y_pos, self.eigenval * 10, align = 'center', alpha = 0.5)
        self.ax.set_xlabel(" ".join((map(str, self.names))))
        self.ax.set_ylabel('Eigen Value')

        # Create Blank Canva on Root Window and put Figure on it.
        self.canvas = FigureCanvasTkAgg(fig, self.master2)
        self.canvas.get_tk_widget().configure(background = 'dodgerblue',  highlightcolor = '#ff4d4d', highlightbackground = '#ff4d4d')
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side = BOTTOM, fill = BOTH, expand = True)

        toolbar = NavigationToolbar2Tk(self.canvas, self.master2)
        toolbar.update()
        self.canvas._tkcanvas.pack(side = TOP, fill = BOTH, expand = True)
        self.canvas.draw()

        self.master2.bind('<Escape>', lambda e: self.master_destroed2)
        self.master2.protocol("WM_DELETE_WINDOW", self.master_destroed2)

    def info(self):
        tkMessageBox.showinfo("PCA","According to kaiser criterion characteristics with eigenvalues <0 should be deleted from dataset.")


    def eigenvecs(self):
        pcs = []
        for i in range(0,len(self.names)):
            pcs.append('PC ' + str(i + 1))

        #unlist charactaristics name
        self.master1 = Tk()
        self.master1.configure(background = '#5c94c5')
        self.master1.title("PCA eigen vectors")
        self.fra = Frame(self.master1)
        self.fra.pack(fill = BOTH,expand = 1)
        self.master_isdestroed1 = 1

        # Define Figure
        fig = Figure(figsize = (10, 6), dpi = 100)
        self.upplot = fig.add_subplot(111)
        
        # Create Blank Figure and Put X and Y Labels Names and Title
        self.ax =self.upplot
        self.ax.clear()
        self.ax.set_xticks(np.arange(len(pcs)))
        self.ax.set_yticks(np.arange(len(self.names)))
        self.ax.set_xticklabels(pcs)
        self.ax.set_yticklabels(self.names)              
        im = self.ax.imshow(self.eigenvec, cmap = 'binary', interpolation = 'nearest', aspect = 'auto')
        for i in range(len(self.names)):
            for j in range(len(pcs)):
                text = self.ax.text(j, i, '%.3f' % self.eigenvec[i, j], ha = "center", va = "center", color = "r")
        fig.colorbar(im, orientation = 'vertical')

        # Create Blank Canva on Root Window and put Figure on it.
        self.canvas = FigureCanvasTkAgg(fig, self.master1)
        self.canvas.get_tk_widget().configure(background = 'dodgerblue',  highlightcolor = '#ff4d4d', highlightbackground = '#ff4d4d')
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side = BOTTOM, fill = BOTH, expand = True)

        toolbar = NavigationToolbar2Tk(self.canvas, self.master1)
        toolbar.update()
        self.canvas._tkcanvas.pack(side = TOP, fill = BOTH, expand = True)
        self.canvas.draw()
        
        self.master1.bind('<Escape>', lambda e: self.master_destroed1)
        self.master1.protocol("WM_DELETE_WINDOW", self.master_destroed1)

    def close_program(self):
        #Checking if child window self.master is active and if it is shows the message to close it first.
        # Note: we use double ifs because we want to avoid the self.master.winfo_exists() == 1 check. 
        # Because when master is destoyed program can not fint self.master window and a bug created.  
        # In order to fix this bug we defined a master destroed function with aim to destroy master and
        # update a flag value named master_destroed.   
        if self.master_isdestroed2 == 1 : 
            if self.master2.winfo_exists() == 1: 
                tkMessageBox.showinfo("Important Info","Eigenvalues Window is Open Please Close it First")
        if self.master_isdestroed == 1 : 
            if self.master.winfo_exists() == 1: 
                tkMessageBox.showinfo("Important Info","Eigenvalues Window is Open Please Close it First")
        elif self.master_isdestroed1 == 1 : 
            if self.master1.winfo_exists() == 1: 
                tkMessageBox.showinfo("Important Info","Eigenvectors Window is Open Please Close it First")
        else:
            self.root.destroy()
    
    def master_destroed(self):
        # Check if eigenvalues variation child window is open
        if self.master_isdestroed2 == 0:
            self.master_isdestroed = 0
            self.master.destroy()
        else:
            tkMessageBox.showinfo("Important Info","Eigenvalues Variation Window is Open Please Close it First")

    
    def master_destroed1(self):
        self.master_isdestroed1 = 0
        self.master1.destroy()
        
    def master_destroed2(self):
        self.master_isdestroed2 = 0
        self.master2.destroy()

    def get(self):
        # Transpose Data
        return self.df.dot(self.eigenvec)
        

 
   
  


    

        

        
  
        
        

    
        

        





