__author__ = 'Tapsas Apostolos', 'Valiakos Apostolos'
import time
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as tkMessageBox
from tkinter import ttk
from tkinter.ttk import Progressbar
import numpy as np
import pandas as pd
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from pandastable import Table
from sklearn.cluster import KMeans


class K_Means:
    def __init__(self,df):
        self.centroids = "Positions of Centroids: "
        self.df = df
        self.d =  df
        self.names = list(df.columns.values)
        self.dim = 0
       
        self.root = Tk()
        self.root.geometry("800x500")
        self.root.configure(background = '#5c94c5')
        self.root.title("K Means Clustering")
        
            
        self.names.insert(0, self.names[0])

        #ToDo thinks on top site of canvas
        self.top_f = Frame(self.root, background='white')
        self.top_f.pack(side = BOTTOM)
        
        #ToDo text on right site of canvas
        right_f = Frame(self.root, background = '#ff4d4d')
        right_f.pack(side = RIGHT)

        self.l1 = Label(right_f, font = ('times new roman', 12), text = "Model Statistics", bg = '#ff4d4d')
        self.l1.pack()
            
        self.l2 = Label(right_f, font = ('times new roman', 12), text = "", background = '#ff4d4d')
        self.l2.pack()

        self.pred = ttk.Button(right_f, text = 'Show Model Statistics', command = self.st)
        self.pred.pack()
        self.pred.state(["disabled"])

        self.style = ttk.Style()
        self.style.configure('TButton', background = 'dodgerblue')

        top_f = Frame(self.root,background = 'white')
        top_f.pack(side = TOP)

        self.plot_btn = ttk.Button(self.top_f, text = 'K Means Clustering', command = self.clu)
        self.plot_btn.pack(side = LEFT, ipady = 5, ipadx = 5)

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

    def clu(self):
        self.plot_btn.state(["disabled"])
        self.close.state(["disabled"])
        
        self.master = Tk()
        self.master.title("K Means")
        self.master.protocol('WM_DELETE_WINDOW', self.cl)

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
        self.el = ttk.Button(self.master, text = 'Elbow Method', command = self.elb) 
        self.el.grid(row = 4, column = 0, sticky = W, pady = 4, ipady = 2, ipadx = 4)
        ttk.Button(self.master, text = 'Show', command = self.vizu).grid(row = 4, column = 1, sticky = W, pady = 4, ipady = 2, ipadx = 4)
        ttk.Button(self.master, text = 'Quit', command = self.cl).grid(row = 4, column = 2, sticky = W, pady = 4, ipady = 2, ipadx = 4)

        mainloop()
        
    def vizu(self):
        self.close.state(["!disabled"])
        self.plot_btn.state(["!disabled"])

        # handle dummy variables
        self.df = pd.get_dummies(self.df)

        self.X = self.df.values
        
        # Fitting the K-means model to the dataset 
        kmeans = KMeans(n_clusters = int(self.v1.get()), init = 'k-means++')
        kmeans.fit(self.X)
        self.kmeans = kmeans
        self.yk = kmeans.predict(self.X)

        # Get centroids
        self.cent = kmeans.cluster_centers_
        
        self.ax.clear()
        self.ax.title.set_text("Clusters of Dataset")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.scatter(self.X[:, 0], self.X[:, 1], c = self.yk , s = 50, cmap = 'rainbow',  label = 'Values')
        self.ax.scatter(self.cent[:, 0], self.cent[:, 1], c = 'black', s = 100, alpha = 0.5, label = 'Centroids')
        self.ax.legend(loc = "upper left")
        self.canvas.draw()
        self.cl()


    def elb(self):
        self.ax.clear()
        wcss = []
        val=0
        n = len(self.df.values)
        if n > 11:
            n = 11
        
        for i in range (1, n):
            kmeans = KMeans(n_clusters = i, init = 'k-means++')
            kmeans.fit(self.df.values)
            wcss.append(kmeans.inertia_)
            self.bar['value'] = val
            val = val + 30
            self.master.update_idletasks()
            time.sleep(1)
        
        self.ax.plot(wcss, label = 'WCSS Line')
        self.ax.title.set_text("The Elbow Method")
        self.ax.set_xlabel("Number of Clusters")
        self.ax.set_ylabel("WCSS")
        self.canvas.draw()

    def cl(self):
        self.close.state(["!disabled"])
        self.plot_btn.state(["!disabled"])
        self.pred.state(["!disabled"])
        self.master.destroy()
    
    def st(self):
        self.master = Tk()
        self.master.configure(background = '#5c94c5')
        self.master.title("Model Stats")
        self.master.geometry('800x500') 
        self.fra = Frame(self.master)
        self.fra.pack(fill = BOTH, expand = 1)
        names = []

        names.append("Centroids")
        names.append("X")
        names.append("Y")

        centroids = []
        for i in range (0, int(self.v1.get())):
            i + 1
            centroids.append("Centroid " + str(i + 1))
        centroids = np.array(centroids)
        a = np.array(self.cent[:, [0, 1]])
        a = np.column_stack((centroids, a))
        a = a.reshape(int(self.v1.get()), -1) 
        df2 = pd.DataFrame(a,columns = names)
        self.pt = Table(self.fra, dataframe = df2)
        self.pt.columncolors['mycol'] = 'white'
        self.cl = ttk.Button(self.master, text = 'Close', command = self.master.destroy).pack(side = RIGHT)
        self.cl = ttk.Button(self.master, text = 'Predict', command = self.predict).pack(side = RIGHT)
        self.pt.show()
        self.pt.redraw()
        self.master.mainloop()
    
    def predict(self):
        data = []
        self.root = Tk()
        self.root.withdraw()
        self.filename = fd.askopenfilename(title="Select file", filetypes = (("all Files", "*.xlsx"),))
        if not self.filename:
            tkMessageBox.showinfo("Info", "The procedure was canceled.")
            self.root.destroy()
        else:
            data = pd.read_excel(self.filename)
            tkMessageBox.showinfo("Import", "Data Imported Successfully.")
            self.root.destroy()

        self.pred_sample = data
        self.ax.scatter(self.pred_sample.values[:,0], self.pred_sample.values[:,1], c = 'green' , s = 100, cmap = 'rainbow', label = 'Your Value')

        self.canvas.draw()

        self.m = Tk()
        self.m.configure(background = '#5c94c5')
        self.m.title("Data Viewer")
        self.m.geometry('800x500') 
        f = Frame(self.m)
        f.pack(fill = BOTH, expand = 1)
        pred_data = self.kmeans.predict(data)
        pred_data = pd.DataFrame(pred_data)
        data['class'] = pred_data[0].values

        names = []
        for col in data.columns:
            names.append(col)

        df2 = pd.DataFrame(data, columns = names)
        self.pt = Table(f, dataframe = df2)
        self.pt.columncolors['mycol'] = 'white'
        self.c = ttk.Button(self.m, text = 'Close', command = self.m.destroy).pack()
        self.pt.show()
        self.pt.redraw()
        self.m.mainloop()
