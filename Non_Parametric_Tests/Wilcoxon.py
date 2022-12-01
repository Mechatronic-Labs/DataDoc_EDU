__author__ = 'Tapsas Apostolos', 'Valiakos Apostolos'
from scipy.stats import wilcoxon
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as tkMessageBox
import pandas as pd
from General import tooltipmanager as tlm
from pandastable import Table
import numpy as np


class Wilcoxon_Test:
    def __init__(self,df):
        self.df = df
        self.names = list(df.columns.values)
        self.master_isdestroed = 0
        
        # Define Main Window and set Title
        self.root = Tk()
        self.root.geometry("800x250")
        self.root.configure(background = '#5c94c5')
        self.root.title("Paired Wilcoxon Test")

        self.v = StringVar(self.root)
        self.v1 = StringVar(self.root)

        # Insert a Data Item to Avoid Problems
        self.names.insert(0, self.names[0])
        
        self.v = StringVar(self.root)
        self.v.set(self.names[0]) # set default value first characteristic name

        self.v1 = StringVar(self.root)
        self.v1.set(self.names[1]) # set default value second characteristic name

        # Define Frames
        # Top frame         
        top_f = Frame(self.root, background = 'white')
        top_f.pack(side=TOP)

        # Bottom Frame
        bottom = Frame(self.root,background = '#ff4d4d')
        bottom.pack(side = BOTTOM)
        
        #Define Select list on Top Frame
        Label(top_f, font = ('times new roman', 12), text = 'Select the characteristic for paired wilcoxon test:', background='white').pack(side = LEFT)

        ttk.OptionMenu(top_f, self.v,  *self.names).pack(side = LEFT)
        ttk.OptionMenu(top_f, self.v1, *self.names).pack(side = LEFT)

        # Define Apply Button and put it on Buttom Frame
        self.bar_plt_b  =  ttk.Button(bottom, text = "Apply", command = self.wt)
        self.bar_plt_b.pack(side = LEFT)
        self.skl45 = tlm.createToolTip(self.bar_plt_b, "Apply paired wilcoxon test")
        
        # Define Show Results Button and put it on right Frame
        self.show_res = ttk.Button(bottom, text = 'Show Results', command = self.results_table)
        self.show_res.pack(side = LEFT)
        self.show_res.state(["disabled"])

        # Define Close Button and put it on Buttom Frame
        ttk.Button(bottom, text = 'Close', command = self.master_destroed).pack(side = LEFT)

        self.root.bind('<Escape>', lambda e: self.master_destroed)
        self.root.protocol("WM_DELETE_WINDOW", self.master_destroed)
        self.root.mainloop()
    

    def wt(self):
        self.w = 0
        self.p = 0
        self.show_res.state(["!disabled"])
        val, val2 = self.v.get(), self.v1.get()
        if val.isdigit():
            val=int(val)
            x = self.df[val].values[~np.isnan(self.df[val].values)]
        else:
            x = self.df[val].values[~np.isnan(self.df[val].values)]

        if val2.isdigit():
            val2=int(val2)
            y = self.df[val2].values[~np.isnan(self.df[val2].values)]
        else:
            y = self.df[val2].values[~np.isnan(self.df[val2].values)]
        self.w, self.p = wilcoxon(x, y, zero_method = "wilcox")
       

    def results_table(self):
        self.master = Tk()
        self.master.configure(background = '#5c94c5')
        self.master.title("Wilcoxon Paired Test Stats")
        self.master.geometry('800x500') 
        self.fra = Frame(self.master)
        self.fra.pack(fill = BOTH, expand = 1)
        self.master_isdestroed = 1
        df2 = pd.DataFrame([[self.w, self.p, ]], columns = ["W Value", "P Value"])
        
        self.pt = Table(self.fra, dataframe = df2)
        self.pt.columncolors['mycol'] = 'white'
        self.cl = ttk.Button(self.master, text = 'Close', command = self.master_destroed).pack(side = RIGHT)
        self.cl = ttk.Button(self.master, text = 'Test Outcome', command = self.info).pack(side = RIGHT)
        self.pt.show()
        self.pt.redraw()

        self.master.bind('<Escape>', lambda e: self.close_program)
        self.master.protocol("WM_DELETE_WINDOW", self.close_program)
        self.master.mainloop()
        
    
    def info(self):
        if (self.p < 0.05):
            text = "According to wilcoxon test the data have significant difference (because p_value = {} < 0.05)."
            tkMessageBox.showinfo("Wilcoxon Test", text.format("%.3f" % self.p))
        else:
            text = "According to wilcoxon test the data did not have significant difference (because p_value = {} >= 0.05)."
            tkMessageBox.showinfo("Wilcoon Test", text.format("%.3f" % self.p))


    
    def close_program(self):
        #Checking if child window self.master is active and if it is shows the message to close it first.
        # Note: we use double ifs because we want to avoid the self.master.winfo_exists() == 1 check. 
        # Because when master is destoyed program can not fint self.master window and a bug created.  
        # In order to fix this bug we defined a master destroed function with aim to destroy master and
        # update a flag value named master_destroed.   
        if self.master_isdestroed == 1: 
            if self.master.winfo_exists() == 1: 
                tkMessageBox.showinfo("Important Info","Wilcoxon Test Stats Window is Open Please Close it First.")
        else:
            self.root.destroy()
    
    def master_destroed(self):
        self.master_isdestroed = 0
        self.master.destroy()