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
from sklearn import preprocessing
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from tabulate import tabulate


class K_Nearest_Neighbor:
    def __init__(self,df):
        self.df = df
        self.d  = df
        self.names = list(df.columns.values)

        self.root = Tk()
        self.root.geometry("800x500")
        self.root.configure(background = '#5c94c5')
        self.root.title("K Nearest Neighbor")
       
            
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

        top_f = Frame(self.root,background = 'white')
        top_f.pack(side = TOP)

        self.plot_btn = ttk.Button(self.top_f, text = 'Create K Nearest Neighbor Model', command = self.clas)
        self.plot_btn.pack(side = LEFT, ipady = 5, ipadx = 5)

        self.pred = ttk.Button(right_f, text = 'Show Model Statistics', command = self.st)
        self.pred.pack(side = BOTTOM)
        self.pred.state(["disabled"])
                    
        self.close = ttk.Button(self.top_f, text = 'Close', command = self.root.destroy)
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

    def clas(self):
        self.plot_btn.state(["disabled"])
        self.close.state(["disabled"])
        
        self.master = Tk()
        self.master.title("K Nearest Neighbor")
        self.master.protocol('WM_DELETE_WINDOW', self.cl)
        self.master.configure(background = 'white')

        self.v = StringVar(self.master)
        self.v.set(self.names[0]) # default value

        self.v1 = StringVar(self.master)
        self.v1.set(5) # default value

        self.dis = ['Euclidean Distance', 'Manhattan Distance']
        self.dis.insert(0, self.dis[0])
        
        self.v2 = StringVar(self.master)
        self.v2.set(self.dis[0]) # default value

        Label(self.master, font = ('times new roman', 10), text = "Select Independent Value:", bg = '#ffffff').grid(row = 0, column = 0)
        ttk.OptionMenu(self.master, self.v, *self.names).grid(row = 0, column = 1, ipady = 5, ipadx = 5)

        Label(self.master, font = ('times new roman', 10), text = "Select Distance Metric:", bg = '#ffffff').grid(row = 0, column = 2)
        ttk.OptionMenu(self.master, self.v2, *self.dis).grid(row = 0, column = 3, ipady = 5, ipadx = 5)

        Label(self.master, font = ('times new roman', 10), text = "Give The Number of Neighbours.", bg = '#ffffff').grid(row = 1, column = 0)
        ttk.Entry(self.master, textvariable = self.v1, width = 10).grid(row = 1, column = 1)

        ttk.Button(self.master, text = 'Show', command = self.vizu).grid(row = 4, column = 0, sticky = W, pady = 4, ipady = 2, ipadx = 4)
        ttk.Button(self.master, text = 'Quit', command = self.cl).grid(row = 4, column = 1, sticky = W, pady = 4, ipady = 2, ipadx = 4)

        mainloop()
        
    def vizu(self):
        self.df = self.d
        self.plot_btn.state(["disabled"])
        self.close.state(["disabled"])  
        self.pred.state(["!disabled"])

        # Getting the independent value from the user 
        independent_value = self.v.get()

        # Getting Solver
        num_of_nei = int(self.v1.get())

        dis = 1
        if self.v2.get() == 'Euclidean Distance':
            dis = 2
        
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
        
        X = self.df.values

        # Spitting the dataset into the Train and Test set
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size = 0.25)

        # Fitting the Simple Linear Regression model to the train set 
        self.model = KNeighborsClassifier(n_neighbors = num_of_nei, metric = 'minkowski', p = dis)
        
        try:
            self.model.fit(self.X_train, self.y_train)
        except ValueError as VE:
            tkMessageBox.showerror("Value Error", VE)

        # Predict the Test set results
        self.y_pred = self.model.predict(self.X_train)
        self.y_pred_train = self.model.predict(self.X_train)  

        # Confusion matrix
        self.con_mat = confusion_matrix(self.y_train, self.y_pred)

        self.acc = accuracy_score(self.y_pred, self.y_pred_train)
        
        scores = cross_val_score(self.model, self.X_train, self.y_train, cv = 10)
       
        table = [["Model Mean Accuracy",str('%.2f' % (self.model.score(self.X_train, self.y_train) * 100) + '%')],
                ["Cross Validation Score",str('%.2f' % (np.mean(scores) * 100) + '%')]]
        
        self.acc  = ['%.2f' % (self.model.score(self.X_train, self.y_train) * 100) + '%']
        self.cvs  = ['%.2f' % (np.mean(scores) * 100) + '%']
        self.bias = ['%.3f' % 1]
        
        tabulate.PRESERVE_WHITESPACE = True
        self.l1.configure(text = "Statisics")

        self.ax.clear()
        self.f.clf()
        self.ax = self.f.add_subplot(111)
        self.ax.title.set_text("Confusion Matrix")
        im = self.ax.matshow(self.con_mat, cmap = 'cool', interpolation = 'nearest', aspect = 'auto')
        self.f.colorbar(im, orientation = 'vertical')
        thresh = np.max(self.con_mat) / 2.
        for i in range(self.con_mat.shape[0]):
            for j in range(self.con_mat.shape[1]):
                self.ax.text(j, i, format(self.con_mat[i, j], '.0f'), ha = "center", va="center", color = "white" if self.con_mat[i, j] > thresh else "black")

        self.ax.set_xticklabels([''] + list(self.p_val))
        self.ax.set_yticklabels([''] + list(self.p_val))
        self.canvas.draw()
        self.pred.state(["!disabled"])

    def predict(self):
        data = []
        self.root = Tk()
        self.root.withdraw()
        self.filename = fd.askopenfilename(title = "Select file", filetypes = (("all Files","*.xlsx"),))
        if not self.filename:
            tkMessageBox.showinfo("Info","The procedure was canceled.")
            self.root.destroy()
        else:
            self.names = []
            data = pd.read_excel(self.filename)
            tkMessageBox.showinfo("Import", "Data Imported Successfully.")
            for col in data.columns:
                self.names.append(col)
            self.root.destroy()
            
        self.m = Tk()
        self.m.configure(background = '#5c94c5')
        self.m.title("Data Viewer")
        self.m.geometry('800x500') 

        f = Frame(self.m)
        f.pack(fill = BOTH, expand = 1)
        
        data = np.array(data)
        pred_data = self.model.predict(data)
        pred_data = pd.DataFrame(pred_data)
        data = pd.DataFrame(data, columns = self.names)
        data['class'] = pred_data[0].values
        df2 = pd.DataFrame(data)
        self.pt = Table(f, dataframe = df2)
        self.pt.columncolors['mycol'] = 'white'
        self.c = ttk.Button(self.m, text = 'Close', command = self.m.destroy).pack()
        self.pt.show()
        self.pt.redraw()
        self.m.mainloop()
        
    def cl(self):
        self.close.state(["!disabled"])
        self.plot_btn.state(["!disabled"])
        self.master.destroy()
    
    def st(self):
        self.master = Tk()
        self.master.configure(background = '#5c94c5')
        self.master.title("Model Stats")
        self.master.geometry('800x500') 
        self.fra = Frame(self.master)
        self.fra.pack(fill = BOTH, expand = 1)
        names = ["Model Mean Accuracy", "Bias Added"]
        # names = ["Model Mean Accuracy"]
        values = [self.acc, self.bias]
        print(values)
        df2 = pd.DataFrame(list(zip(self.acc, self.bias)), columns = names)
        self.pt = Table(self.fra, dataframe=df2)
        self.pt.columncolors['mycol'] = 'white'
        self.cl = ttk.Button(self.master, text = 'Close', command = self.master.destroy).pack(side = RIGHT)
        self.cl = ttk.Button(self.master, text = 'Predict', command = self.predict).pack(side = RIGHT)
        self.pt.show()
        self.pt.redraw()
        self.master.mainloop()
