__author__ = 'Tapsas Apostolos', 'Valiakos Apostolos'
from scipy import stats
import scipy.stats as stats
from tkinter import *
from tkinter import Tk
from tkinter import messagebox as tkMessageBox
import pandas as pd
from tkinter import ttk
from pandastable import Table
from sympy import Le


class Analyze:
    def __init__(self,df):
        self.df = df
        self.names = list(df.columns.values)
        self.master_isdestroed = 0
        
        # Define Main Window and set Title
        self.root = Tk()
        self.root.geometry("800x250")
        self.root.configure(background = '#5c94c5')
        self.root.title("Normality Test")
        
        # Insert a Data Item to Avoid Problems
        self.names.insert(0, self.names[0])
        
        self.v = StringVar(self.root)
        self.v.set(self.names[0]) # set default value first characteristic name

        # Define frames
        # Top frame         
        top_f = Frame(self.root, background = 'white')
        top_f.pack( side = TOP )
        
        # Bottom Frame
        bottom = Frame(self.root,background = '#ff4d4d')
        bottom.pack( side = BOTTOM )

        # Define Text 
        Label(top_f, font=('times new roman', 12), text = 'Please select below the characteristic for normality test:', background = 'white').pack(side = LEFT)
        
        # Define Select List
        ttk.OptionMenu(top_f, self.v, *self.names).pack(side = LEFT)

        # Define Buttons
        ttk.Button(bottom, text="Apply", command=self.normtest).pack(side = LEFT)

        ttk.Button(bottom, text="Close", command=self.close_program).pack(side = LEFT)
        
        self.root.bind('<Escape>', lambda e: self.close_program)
        self.root.protocol("WM_DELETE_WINDOW", self.close_program)
        
        self.root.mainloop()
        
    def normtest(self):
        val = self.v.get()
        if val.isdigit():
            val=int(val)
            data = self.df[val]
        else:
            data = self.df[val].values 
        
        #Apply Shapiro-Wilk Test
        [shapiro_stat, shapiro_pvalue] = stats.shapiro(data)

        #Apply Kolmogorov-Smirnov Test
        [ks_stat, ks_pvalue] = stats.kstest(data, 'norm')

        self.master = Tk()
        self.master.configure(background = '#5c94c5')
        self.master.title("Normality Test Stats")
        self.master.geometry('800x500') 
        self.fra = Frame(self.master)
        self.fra.pack(fill = BOTH, expand = 1)
        self.master_isdestroed = 1
        df2 = pd.DataFrame([[shapiro_stat, shapiro_pvalue, ks_stat, ks_pvalue]], columns = ["Shapiro", "Shapito p-val", "KS", "KS p-val"])
        
        #Debuf Print
        #print(df2)
        self.pt = Table(self.fra, dataframe = df2)
        self.pt.columncolors['mycol'] = 'white'
        self.cl = ttk.Button(self.master, text = 'Close', command = self.master_destroed).pack(side = RIGHT)
        self.cl = ttk.Button(self.master, text = 'Test Outcome', command = self.info).pack(side = RIGHT)
        self.pt.show()
        self.pt.redraw()

        self.master.bind('<Escape>', lambda e: self.master_destroed)
        self.master.protocol("WM_DELETE_WINDOW", self.master_destroed)
        self.master.mainloop()

    def info (self):
        val = self.v.get()
        
        # handle missing values
        self.df = self.df.dropna()

        # handle dummy variables
        self.df = pd.get_dummies(self.df)

        if val.isdigit():
            val = int(val)
            data = self.df[val]
        else:
            data = self.df[val].values
          
        #Checking for Dataset length and applies the corresponding normality test
        if len(data) < 50:
            [stat, pvalue] = stats.shapiro(data)
            if pvalue > 0.05:
                text = "According to Shapiro-Wilk test(because df = {} <50) the {} characteristic follows normal distribution because p({}) > 0.05."
                tkMessageBox.showinfo("Normality Test", text.format(len(data), val, "%.3f" % pvalue)) 
            else:
                text = "According to Shapiro-Wilk test(because df = {} <50) the {} characteristic does not follows normal distribution because p({}) < 0.05."
                tkMessageBox.showinfo("Normality Test", text.format(len(data), val, pvalue))
        else:
            [stat, pvalue] = stats.kstest(data, 'norm')
            if pvalue > 0.05:
                text = "According to Kolmogorov-Smirnov test(because df = {} > 50) the {} characteristic follows normal distribution because p({}) > 0.05."
                tkMessageBox.showinfo("Normality Test", text.format(len(data), val, "%.3f" % pvalue))
            else:
                text = "According to Kolmogorov-Smirnov test(because df = {} > 50) the {} characteristic does not follows normal distribution because p({}) > 0.05."
                tkMessageBox.showinfo("Normality Test", text.format(len(data), val, "%.3f" % pvalue))

    def close_program(self):
        #Checking if child window self.master is active and if it is shows the message to close it first.
        # Note: we use double ifs because we want to avoid the self.master.winfo_exists() == 1 check. 
        # Because when master is destoyed program can not fint self.master window and a bug created.  
        # In order to fix this bug we defined a master destroed function with aim to destroy master and
        # update a flag value named master_destroed.   
        if self.master_isdestroed == 1: 
            if self.master.winfo_exists() == 1: 
                tkMessageBox.showinfo("Important Info", "Normality Test Stats Window is Open Please Close it First.")
        else:
            self.root.destroy()
    
    def master_destroed(self):
        self.master_isdestroed = 0
        self.master.destroy()

        
          





    




