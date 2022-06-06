__author__ = 'Tapsas Apostolos', 'Valiakos Apostolos'
from tkinter import *
from tkinter import ttk
from sklearn.decomposition import KernelPCA
import pandas as pd

class Kernel_PCA():
    def __init__(self,df):
        self.df = df
        self.names = list(df.columns.values)

        # Define Main Window and set Title
        self.root = Tk()
        self.root.geometry("800x250")
        self.root.configure(background = '#5c94c5')
        self.root.title("Kernel Principal Components Analysis")
        
        # Define kernels options
        self.kel = ["Linear" , "Poly" , "Rbf" , "Sigmoid" , "Cosine"]
        self.v1 = StringVar(self.root)
        self.kel.insert(0, self.kel[0])
        self.v1.set(self.kel[0]) # default value

        # Define frames
        # Top frame         
        top_f = Frame(self.root, background = 'white')
        top_f.pack( side=TOP ) 
        
        # Bottom Frame
        bottom = Frame(self.root,background = '#ff4d4d')
        bottom.pack( side = BOTTOM )

        # Define Kernel option and put it on top frame
        Label(top_f, font = ('times new roman', 10), text = "Select Kernel", bg = '#ffffff').pack(side = LEFT)

        # Define select list
        ttk.OptionMenu(top_f, self.v1, *self.kel).pack(side = LEFT)

        # Define Apply Button and put it on buttom Frame
        ttk.Button(bottom, text = 'Apply', command = self.kpca).pack(side = LEFT)

        # Define close Button and put it on buttom Frame
        ttk.Button(bottom, text = 'Close', command = self.root.destroy).pack(side = LEFT)
        
        self.root.bind('<Escape>', lambda e: self.root.destroy())
        #self.root.protocol("WM_DELETE_WINDOW", self.close_program)
        
        self.root.mainloop()
    
    # Function Applying PCA
    def kpca(self):
        # Getting the independent value from the user 
        ker = self.v1.get().lower()

        # handle missing values
        self.df = self.df.dropna()

        # handle dummy variables
        self.df = pd.get_dummies(self.df)

        self.X = self.df.values

        #Fitting to the Dataset
        self.kpca = KernelPCA(kernel = ker)

        self.X = self.kpca.fit_transform(self.X)
    
    def get(self):
        return self.X
    
        
       

        
        




