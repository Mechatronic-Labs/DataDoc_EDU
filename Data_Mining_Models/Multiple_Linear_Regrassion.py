__author__ = 'Tapsas Apostolos', 'Valiakos Apostolos'
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as tkMessageBox
from tkinter import ttk
import numpy as np
import pandas as pd
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from pandastable import Table
from scipy.stats import t
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
    
class Multiple_Linear_Regrassion:
    def __init__(self, df, instruction):
        self.df = df
        self.d  = df
        self.names = list(df.columns.values)
        self.master_isdestroed  = 0
        self.master_isdestroed2 = 0
        self.statsBut = False  
        self.selectGraph = False
        self.dim = 0
        self.root = Tk()
        self.root.geometry("800x500")
        self.root.configure(background = '#5c94c5')
        self.root.title("Multiple Linear Regression")
           
        self.names.insert(0, self.names[0])

        self.top_f = Frame(self.root,background = 'white')
        self.top_f.pack(side = BOTTOM)

        right_f = Frame(self.root,background = '#ff4d4d')
        right_f.pack(side = RIGHT)

        self.l1 = Label(right_f, font = ('times new roman', 12), text = "Model Statistics", bg = '#ff4d4d')
        self.l1.pack()
        
        self.l2 = Label(right_f, font = ('times new roman', 12), text = "", background = '#ff4d4d')
        self.l2.pack()
        
        self.pred = ttk.Button(right_f, text = 'Show model Statistics', command = self.st)
        self.pred.pack()
        self.pred.state(["disabled"])

        self.style = ttk.Style()
        self.style.configure('TButton', background = 'dodgerblue')

        top_f = Frame(self.root, background = 'white')
        top_f.pack(side = TOP)

        self.plot_btn = ttk.Button(self.top_f, text = 'Create Multiple Linear Regression Model', command = self.reg)
        self.plot_btn.pack(side = LEFT, ipady = 5, ipadx = 5)

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
        self.canvas.get_tk_widget().configure(background = 'dodgerblue', highlightcolor = '#ff4d4d' ,highlightbackground = '#ff4d4d')
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side = BOTTOM, fill = BOTH, expand = True)

        toolbar = NavigationToolbar2Tk(self.canvas, self.root)
        toolbar.update()
        self.canvas._tkcanvas.pack(side = TOP, fill = BOTH, expand = True)

        self.root.bind('<Escape>', lambda e: self.close_program)
        self.root.protocol("WM_DELETE_WINDOW", self.close_program)

        mainloop()

    def reg(self):
        self.master_isdestroed = 1
        self.selectGraph = True
        self.plot_btn.state(["disabled"])
        self.close.state(["disabled"])
        
        self.master = Tk()
        self.master.title("Multiple Linear Regresion")
        self.master.geometry("300x100")

        self.master.configure(background = 'white')

        self.v = StringVar(self.master)
        self.v.set(self.names[0]) # default value

        Label(self.master, font = ('times new roman', 10), text = "Select Independent Value:", bg = '#ffffff').grid(row = 0, column = 0)
        ttk.OptionMenu(self.master, self.v, *self.names).grid(row = 0, column = 1, ipady = 5, ipadx = 5)

        ttk.Button(self.master, text = 'Show', command = self.vizu).grid(row = 4, column = 0, sticky = W, pady = 4, ipady = 2, ipadx = 4)
        ttk.Button(self.master, text = 'Quit', command = self.master_destroed).grid(row = 4, column = 1, sticky = W, pady = 4, ipady = 2, ipadx = 4)
        self.master.bind('<Escape>', lambda e: self.master_destroed)
        self.master.protocol("WM_DELETE_WINDOW", self.master_destroed)
        mainloop()
        
    def vizu(self):
        self.master_isdestroed = 1
        self.selectGraph = True
        self.close.state(["!disabled"])
        self.pred.state(["!disabled"])
        self.plot_btn.state(["!disabled"])
        # self.master.destroy()
        self.master_destroed()
             
        # Getting the independent value from the user 
        independent_value = self.v.get()
        self.df = self.d

        # Creating the indepentent and paired values 
        y = (self.df[independent_value].values)
        self.df = self.df.drop([independent_value], axis = 1)
        
        # handle dummy variables
        self.df = pd.get_dummies(self.df)
        
        X = self.df.values
       
        # Spitting the dataset into the Train and Test set
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size = 0.25)
        
        # Fitting the Simple Linear Regression model to the train set 
        self.reg = LinearRegression()
        self.reg.fit(self.X_train, self.y_train)

        # Predict the Test set results
        self.y_pred = self.reg.predict(self.X_test)
        self.y_pred_train = self.reg.predict(self.X_train) 

        self.labels = list(self.d.columns.values)
        self.labels.remove(self.v.get())
        self.ax.clear()
        self.ax.title.set_text("Simple Linear Regression")
        formula = ''
        for i in range(len(self.reg.coef_)):
            formula = formula + str('%.3f' % self.reg.coef_[i]) + ' * ' + str(self.names[i])  
        self.ax.plot([0],  [0] , label= 'y = ' + formula)
        self.ax.legend(loc = "upper left")
        self.canvas.draw()
    
    def st(self):
        self.master = Tk()
        self.master_isdestroed = 1
        self.master.configure(background = '#5c94c5')
        self.master.title("Model Stats")
        self.master.geometry('800x500') 
        self.fra = Frame(self.master)
        self.master_isdestroed = 1
        self.fra.pack(fill = BOTH, expand = 1)

        names = ['r^2']
        y_predicted = self.reg.predict(self.X_test)
        r2 = r2_score(self.y_test, y_predicted)
        table = [r2]
        a = np.array(table)
        df2 = pd.DataFrame(a)
        df2.columns = names
        self.pt = Table(self.fra, dataframe = df2)
        self.pt.columncolors['mycol'] = 'white'
        self.cl = ttk.Button(self.master, text = 'Close', command = self.master_destroed).pack(side = RIGHT)
        self.cl = ttk.Button(self.master, text = 'Predict', command = self.predict).pack(side = RIGHT)
        self.master.bind('<Escape>', lambda e: self.master_destroed)
        self.master.protocol("WM_DELETE_WINDOW", self.master_destroed)
        self.pt.show()
        self.pt.redraw()
        self.master.mainloop()

   
    def predict(self):
        data = []
        self.root1 = Tk()
        self.root1.withdraw()
        self.master_isdestroed2 = 1
        self.filename = fd.askopenfilename(title = "Select file", filetypes = (("all Files", "*.xlsx"),))
        if not self.filename:
            tkMessageBox.showinfo("Info", "The procedure was canceled.")
            self.root1.destroy()
        else:
            data = pd.read_excel(self.filename)
            tkMessageBox.showinfo("Import", "Data Imported Successfully.")    
            self.root1.destroy()
            
        self.master_pred = Tk()
        self.master_pred.configure(background = '#5c94c5')
        self.master_pred.title("Data Viewer")
        self.master_pred.geometry('800x500') 
        f = Frame(self.master_pred)
        f.pack(fill = BOTH, expand = 1)
        pred_data = self.reg.predict(data)
        pred_data = pd.DataFrame(pred_data)
        data[self.names[0]] = pred_data[0].values
        data = pd.DataFrame(data, columns = self.names)
        df2 = pd.DataFrame(data)
        df2 = df2.iloc[: , 1:]
        self.pt = Table(f, dataframe = df2)
        self.pt.columncolors['mycol'] = 'white'
        self.c = ttk.Button(self.master_pred, text = 'Close', command = self.master_destroed).pack()
        self.master_pred.bind('<Escape>', lambda e: self.master_destroed)
        self.master_pred.protocol("WM_DELETE_WINDOW", self.master_destroed)
        self.pt.show()
        self.pt.redraw()
        self.master_pred.mainloop() 

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
        # self.enableButtons()
    
    def master_destroed(self):
        # self.master_isdestroed = 0
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
