__author__ = 'Tapsas Apostolos', 'Valiakos Apostolos'
from math import e
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from tkinter import *
from tkinter import messagebox as tkMessageBox
from tkinter import ttk
from pandastable import Table
import numpy as np
from scipy.stats.stats import chisquare
from General import tooltipmanager as tlm
from scipy import stats
import pandas as pd


# Produse f distribution dataset
dfnum = 2 # between group degrees of freedom
dfden = 48 # within groups degrees of freedom
fdist_dataset = np.random.f(dfnum, dfden, 100)

# Produse mormal distribution dataset
mu, sigma = 0, 0.1 # mean and standard deviation
normaldist_dataset = np.random.normal(mu, sigma, 100)

# Produse chi square distribution dataset
chisquaredist_dataset = np.random.chisquare(2, 100)

# Produse poison square distribution dataset
poisondist_dataset = np.random.poisson(5, 100)

# Produse student t distribution dataset
tdist_dataset = np.random.standard_t(10, size=100)


d = {'Norm': normaldist_dataset, 'chi': chisquaredist_dataset, 'f' : fdist_dataset, 'Poison': poisondist_dataset, 'Student t':tdist_dataset}
df = pd.DataFrame(data = d)


class One_Sample_Kolmogorov_Smirnov_test:
    def __init__(self,df):
        self.df = df
        self.names = list(df.columns.values)
        
        # Define Main Window and set Title
        self.root = Tk()
        self.root.geometry("680x100")
        self.root.title("One Shample Kolmogorov Smirnov Test")

        self.names.insert(0, self.names[0])

        self.v = StringVar(self.root)
        self.v.set(self.names[0]) # set default value first characteristic name

        # Define Distibution options
        self.distibutions = {'----------':'norm', 'Normal Distibution':'norm', 'T Distibution': 't', 'Chi Square Distibution': 'chi2', 'F Distibution':'f', 
                             'Poisson Distibution':'poisson'}


        self.v1 = StringVar(self.root)
        self.v1.set(self.distibutions['Normal Distibution']) # set default value first characteristic distribution

        # Define Text 
        self.text = Label(self.root, font=('times new roman', 12), text='Please select the characteristic and distribution for KS test:',background='white')
        self.text.grid(row = 1, column = 0)

        # Define Select List
        w = ttk.OptionMenu(self.root, self.v,  *self.names).grid(row = 1, column = 1) 
        w = ttk.OptionMenu(self.root, self.v1, *self.distibutions.keys()).grid(row = 1, column = 2) 
        
        # Define Buttons
        ttk.Button( self.root, text="Select", command = self.ks_test).grid(row = 3, column = 0)
        ttk.Button( self.root, text="Close",  command = self.root.destroy).grid(row = 3, column = 1)
        
        self.root.bind('<Escape>', lambda e: self.root.destroy())
        self.root.mainloop()
    
    def ks_test(self):
        self.val = self.v.get()
        if self.val.isdigit():
            val=int(self.val)
            data = self.df[self.val].values[~np.isnan(self.df[self.val].values)]
        else:
            data = self.df[self.val].values[~np.isnan(self.df[self.val].values)]
        self.closed = 1
        # execute KS acording distibution selected
        if self.distibutions[self.v1.get()] == 'norm':
            s, self.p = stats.kstest(data, self.distibutions[self.v1.get()])
        if self.distibutions[self.v1.get()] == 'f':
            s, self.p = stats.kstest(data, self.distibutions[self.v1.get()], (len(data) - 1, len(data) - 1,) )
        elif self.distibutions[self.v1.get()] == 'poisson':
            s, self.p = stats.kstest(data, self.distibutions[self.v1.get()], (np.mean(data) ,) )
        elif self.distibutions[self.v1.get()] == 'chi2':
            s, self.p = stats.kstest(data, self.distibutions[self.v1.get()], (len(data) - 1 ,) )
        else:
            s, self.p = stats.kstest(data, self.distibutions[self.v1.get()], (len(data) - 1 ,))
        
        self.master = Tk()
        self.master.configure(background='#5c94c5')
        self.master.title("One Shample Kolmogorov Smirnov Test Results")
        self.master.geometry('800x500') 
        self.fra = Frame(self.master)
        self.fra.pack(fill=BOTH,expand=1)
        df2 = pd.DataFrame([[s, self.p]], columns = ["KS", "KS p-val"])
        #Debuf Print
        #print(df2)
        self.pt = Table(self.fra, dataframe = df2)
        self.pt.columncolors['mycol'] = 'white'
        self.cl = ttk.Button(self.master, text='Close', command = self.master.destroy).pack(side = RIGHT)
        self.cl = ttk.Button(self.master, text='Test Outcome', command = self.info).pack(side = RIGHT)
        self.pt.show()
        self.pt.redraw()
        self.master.mainloop()

    def info (self):
        if self.p > 0.05:
            tkMessageBox.showinfo("Kolmogorov-Smirnov Test","According to Kolmogorov-Smirnov test the "+ str(self.val)+" characteristic follows "+self.v1.get()+" because p("+str("%.5f" % self.p)+")>0.05.")
        else:
            tkMessageBox.showinfo("Kolmogorov-Smirnov Test","According to Kolmogorov-Smirnov test the "+ str(self.val)+" characteristic does not follows "+self.v1.get()+" because p("+str("%.5f" % self.p)+")>0.05.")
    

#One_Sample_Kolmogorov_Smirnov_test(df)
        
