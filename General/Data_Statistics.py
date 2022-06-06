__author__ = 'Tapsas Apostolos', 'Valiakos Apostolos'
from tkinter import *
from tkinter import ttk
import numpy as np
from scipy import stats
from pandastable import Table
import pandas as pd

class Data_Statistics:
    def __init__(self,df):
        self.df = df
        
        # Delete all Missing Values
        self.df = self.df.dropna()

        # handle dummy variables
        self.df = pd.get_dummies(self.df)
        
        d = self.df.to_numpy()
        self.names = list(self.df.columns.values)
        self.root = Tk()
        self.root.configure(background='#5c94c5')
        self.root.title("Data Viewer")
        self.root.geometry('800x500') 
        self.f = Frame(self.root)
        self.f.pack(fill=BOTH,expand=1)

        names = ['df','SE',"Minimum","Maximum",'Mean','Median','Std','CV']    
        table = []
        for i in range(0,len(self.names)):
            x=d[:,i]
            table.append(len(x))
            table.append(float("%.2f" % stats.sem(x)))
            table.append(float("%.2f" % np.min(x)))
            table.append(float("%.2f" % np.max(x)))
            table.append(float("%.2f" % np.mean(x)))
            table.append(float("%.2f" % np.median(x)))
            table.append(float("%.2f" % np.std(x)))
            table.append(float("%.2f" % (np.std(x)/np.mean(x)*100)))

        a = np.array(table)
        a = a.reshape(len(self.names), 8) 
        df2 = pd.DataFrame(a,columns = names)
        df2.insert(0,'Attribute',self.names)
        self.pt = Table(self.f, dataframe=df2)
        self.pt.columncolors['mycol'] = 'white'
        self.close = ttk.Button(self.root, text='Close', command = self.root.destroy).pack()
        self.pt.show()
        self.pt.redraw()
        self.root.bind('<Escape>', lambda e: self.root.destroy())
        self.root.mainloop()
        
    
       
        
        
        







