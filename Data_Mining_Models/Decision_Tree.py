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
from sklearn import preprocessing, tree
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import StandardScaler
from tabulate import tabulate
from sklearn.metrics import r2_score
    
class Decision_trees():
    def __init__(self,df,instruction):
        self.instruction = instruction
        self.df = df
        self.d =  df
        self.master_isdestroed = 0 
        self.master_isdestroed2 = 0
        self.statsBut = False
        self.names = list(df.columns.values)

        self.dim = 0
    
        self.root = Tk()
        self.root.geometry("800x500")
        self.root.configure(background = '#5c94c5')
        self.root.bind('<Escape>', lambda e: self.close_program)
        self.root.protocol("WM_DELETE_WINDOW", self.close_program)
            
        self.names.insert(0, self.names[0])

        self.top_f = Frame(self.root, background = 'white')
        self.top_f.pack(side = BOTTOM)

        right_f = Frame(self.root, background = '#ff4d4d')
        right_f.pack(side = RIGHT)

        self.l1 = Label(right_f, font = ('times new roman', 12), text = "Model Statistics", bg = '#ff4d4d')
        self.l1.pack()
        
        self.l2 = Label(right_f, font = ('times new roman', 12), text = "", background = '#ff4d4d')
        self.l2.pack()

        self.style = ttk.Style()
        self.style.configure('TButton', background = 'dodgerblue')

        top_f = Frame(self.root, background = 'white')
        top_f.pack(side = TOP)

        if instruction == 'r':
            self.root.title("Decision Tree Regression")
            self.plot_btn = ttk.Button(self.top_f, text = 'Create Decision Tree Regression Model', command = self.reg)
            self.plot_btn.pack(side = LEFT, ipady = 5, ipadx = 5)
            self.pred_btn = ttk.Button(right_f, text = 'Show Model Statistics', command = self.st)
            self.pred_btn.pack(side = BOTTOM)
            self.pred_btn.state(["disabled"])
        else:
            self.root.title("Decision Tree Classification")
            self.plot_btn = ttk.Button(self.top_f, text = 'Create Decision Tree Classification Model', command = self.clas)
            self.plot_btn.pack(side = LEFT,ipady = 5, ipadx = 5)
            self.mod_stats = ttk.Button(right_f, text = 'Show Model Statistics', command = self.st)
            self.mod_stats.pack(side = BOTTOM)
            self.mod_stats.state(["disabled"])
                    
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

        self.root.bind('<Escape>', lambda e: self.root.destroy())
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)
          
        mainloop()

    def reg(self):
        self.plot_btn.state(["disabled"])
        self.close.state(["disabled"])
        self.selectGraph = True
        self.master_isdestroed = 1
        
        self.master = Tk()
        self.master.title("Decision Tree Regresion")
        self.master.configure(background = 'white')

        self.v = StringVar(self.master)
        self.v.set(self.names[0]) # default value

        Label(self.master,font=('times new roman', 10), text = "Select Independent Value:", bg = '#ffffff').grid(row = 0, column = 0)
        ttk.OptionMenu(self.master, self.v, *self.names).grid(row = 0, column = 1, ipady = 5, ipadx = 5)

        ttk.Button(self.master, text = 'Show', command = self.vizu_reg).grid(row = 4, column = 0, sticky = W, pady = 4, ipady = 2, ipadx = 4)
        ttk.Button(self.master, text = 'Quit', command = self.master_destroed).grid(row = 4, column = 1, sticky = W, pady = 4, ipady = 2, ipadx = 4)
        
        self.master.bind('<Escape>', lambda e: self.master_destroed)
        self.master.protocol("WM_DELETE_WINDOW", self.master_destroed)
        
        mainloop()
        
    def vizu_reg(self):
        self.master_destroed()
        self.pred_btn.state(["!disabled"])
        self.close.state(["!disabled"])
        self.plot_btn.state(["!disabled"])
        self.selectGraph = True
        self.master_isdestroed = 1

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
        
        # Feature Scaling
        sc_X = StandardScaler()
        sc_y = StandardScaler()
        self.X_train = sc_X.fit_transform(self.X_train)
        self.y_train = self.y_train.reshape(-1, 1)
        self.y_train = sc_y.fit_transform(self.y_train)

        #Fitting to the Dataset
        self.reg = tree.DecisionTreeRegressor()
        self.reg.fit(self.X_train, self.y_train)

        # Predict the Test set results
        self.y_pred = self.reg.predict(self.X_test)
        self.y_pred_train = self.reg.predict(self.X_train) 

        self.labels = list(self.d.columns.values)
        self.labels.remove(self.v.get())
        self.ax.clear()
        self.ax.title.set_text("Decision Tree Regression")
        self.ax.set_xlabel(self.labels[0])
        self.ax.set_ylabel(self.v.get())
        X_grid = np.arange(min(self.X_train), max(self.X_train), 0.1)
        X_grid = X_grid.reshape(len(X_grid),1)
        self.ax.plot(X_grid, self.reg.predict(X_grid), label = 'Decision Tree Regression Line')
        self.ax.plot(self.X_train, self.y_train, 'ro', label = 'Values')
        self.ax.legend(loc = "upper left")
        self.canvas.draw()

    def clas(self):
        self.selectGraph = True
        self.master_isdestroed = 1
        self.plot_btn.state(["disabled"])
        self.close.state(["disabled"])
        self.master = Tk()
        self.master.title("Decision Tree Classification")
        self.master.configure(background = 'white')
        self.v = StringVar(self.master)
        self.v.set(self.names[0]) # default value
        self.creteria = ['gini', 'entropy']
        self.v1 = StringVar(self.master)
        self.creteria.insert(0, self.creteria[0])
        self.v1.set(self.creteria[0]) # default value
        Label(self.master, font = ('times new roman', 10), text = "Select Independent Value:", bg = '#ffffff').grid(row = 0, column = 0)
        ttk.OptionMenu(self.master, self.v, *self.names).grid(row = 0, column = 1, ipady = 5, ipadx = 5)
        Label(self.master, font = ('times new roman', 10), text = "Select Creteria:", bg = '#ffffff').grid(row = 0, column = 2)
        ttk.OptionMenu(self.master, self.v1, *self.creteria).grid(row = 0, column = 3, ipady = 5, ipadx = 5)
        ttk.Button(self.master, text = 'Show', command = self.vizu_clas).grid(row = 4, column = 0, sticky = W, pady = 4, ipady = 2, ipadx = 4)
        ttk.Button(self.master, text = 'Quit', command = self.master_destroed).grid(row = 4, column = 1, sticky = W, pady = 4, ipady = 2, ipadx = 4)
        self.master.bind('<Escape>', lambda e: self.master_destroed)
        self.master.protocol("WM_DELETE_WINDOW", self.master_destroed)
        mainloop()

    def vizu_clas(self):
        self.df = self.d
        self.selectGraph = True
        self.master_isdestroed = 1
        self.close.state(["!disabled"])
        self.plot_btn.state(["!disabled"])

        # Getting the independent value from the user 
        independent_value = self.v.get()
        cret_value = self.v1.get()
    
        # Creating the indepentent and paired values 
        y = self.df[independent_value].values
        m = list(dict.fromkeys(y))
        self.p_val = list(np.arange(1, len(m) + 1))
        self.p_val = map(str, self.p_val)
        if type(y[0]) == str:
                self.p_val = y
                le = preprocessing.LabelEncoder()
                y = le.fit_transform(y)

        self.df = self.df.drop([independent_value], axis = 1)

        # handle dummy variables
        self.df = pd.get_dummies(self.df)
        
        self.X = self.df.values

        # Spitting the dataset into the Train and Test set
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, y, test_size = 0.25)

        # Fitting the Simple Linear Regression model to the train set 
        self.clas = tree.DecisionTreeClassifier(criterion = cret_value)
        
        try:
            self.clas.fit(self.X_train, self.y_train)
        except ValueError as VE:
            tkMessageBox.showerror("Value Error",VE)

        # Predict the Test set results
        self.y_pred = self.clas.predict(self.X_train)
        self.y_pred_train = self.clas.predict(self.X_train)  

        # Confusion matrix
        self.con_mat = confusion_matrix(self.y_train, self.y_pred)

        # Cross Validation        
        scores = cross_val_score(self.clas, self.X_train, self.y_train,cv = 10)
                
        # Define output
        table = [["Model Mean Accuracy", str('%.2f' % (self.clas.score(self.X_train,self.y_train) * 100) + '%')], 
                ["Cross Validation Score", str('%.2f' % (np.mean(scores) * 100) + '%')]]
        
        tabulate.PRESERVE_WHITESPACE = True
        self.l1.configure(text = "Statisics")
        self.acc = ['%.2f' % (self.clas.score(self.X_train, self.y_train) * 100) + '%']
        self.cvs = ['%.2f' % (np.mean(scores) * 100) + '%' ]
         
        self.ax.clear()
        self.f.clf()
        self.ax = self.f.add_subplot(111)
        self.ax.title.set_text("Confusion Matrix")
        im = self.ax.matshow(self.con_mat, cmap = 'cool', interpolation = 'nearest', aspect = 'auto')
        self.f.colorbar(im, orientation = 'vertical')
        thresh = np.max(self.con_mat) / 2.
        for i in range(self.con_mat.shape[0]):
            for j in range(self.con_mat.shape[1]):
                self.ax.text(j, i, format(self.con_mat[i, j], '.0f'), ha = "center", va = "center", color = "white" if self.con_mat[i, j] > thresh else "black")

        self.ax.set_xticklabels([''] + list(self.p_val))
        self.ax.set_yticklabels([''] + list(self.p_val))
        self.canvas.draw()
        self.mod_stats.state(["!disabled"])


    def predict(self):
        data = []
        self.root1 = Tk()
        self.master_isdestroed2 = 1
        self.root1.withdraw()
        self.filename = fd.askopenfilename(title = "Select file", filetypes = (("all Files", "*.xlsx"),))
        if not self.filename:
            tkMessageBox.showinfo("Info", "The procedure was canceled.")
            self.root1.destroy()
        else:
            self.names = []
            data = pd.read_excel(self.filename)
            tkMessageBox.showinfo("Import", "Data Imported Successfully.")    
            self.root1.destroy()
            for col in data.columns:
                self.names.append(col)
        
        # if data loaded
        self.master_pred = Tk()
        self.master_pred.configure(background = '#5c94c5')
        self.master_pred.title("Data Viewer")
        self.master_pred.geometry('800x500') 
        f = Frame(self.master_pred)
        f.pack(fill = BOTH, expand = 1)
        if self.instruction == 'r' :
            pred_data = self.reg.predict(data)
        else:
            pred_data = self.clas.predict(data)
        pred_data = pd.DataFrame(pred_data)
        data = pd.DataFrame(data, columns = self.names)
        data[self.v.get()] = pred_data[0].values
        df2 = pd.DataFrame(data)
        self.pt = Table(f, dataframe = df2)
        self.pt.columncolors['mycol'] = 'white'
        self.c = ttk.Button(self.master_pred, text = 'Close', command = self.master_destroed).pack()
        self.master_pred.bind('<Escape>', lambda e: self.master_destroed)
        self.master_pred.protocol("WM_DELETE_WINDOW", self.master_destroed)
        self.pt.show()
        self.pt.redraw()
        self.master_pred.mainloop()

    def st(self):
        self.pred_btn.state(["!disabled"])
        self.master = Tk()
        self.master_isdestroed = 1
        self.master.configure(background='#5c94c5')
        self.master.title("Model Stats")
        self.master.geometry('800x500') 
        self.fra = Frame(self.master)
        self.fra.pack(fill = BOTH, expand = 1)
        if(self.instruction != 'r'):
            names = ["Model Mean Accuracy","Cross Validation Score"]
            df2 = pd.DataFrame(list(zip(self.acc, self.cvs)), columns = names)
            self.pt = Table(self.fra, dataframe = df2)
        else:
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
        self.pt.show()
        self.pt.redraw()
        self.master.bind('<Escape>', lambda e: self.master_destroed)
        self.master.protocol("WM_DELETE_WINDOW", self.master_destroed)
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