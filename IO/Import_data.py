__author__ = 'Tapsas Apostolos', 'Valiakos Apostolos'
from tkinter import filedialog as fd
from tkinter import *
import pandas as pd
from tkinter import messagebox as tkMessageBox
import os

class import_data(object):
    def load_data(self):
        self.data=[]
        self.root=Tk()
        self.root.withdraw()
        self.filename = fd.askopenfilename(title = "Select file",filetypes = (("all Files","*.xlsx"),))
        if not self.filename:
            tkMessageBox.showinfo("Info","The procedure was canceled.")
            self.root.destroy()
            return pd.DataFrame()
        else:
            try:
                self.data = pd.read_excel(self.filename)
                tkMessageBox.showinfo("Import","Data Imported Successfully.")    
                self.root.destroy()
                return self.data
            except ImportError as io:
                self.tkMessageBox.showerror("ImportError",io)
                self.MsgBox = tkMessageBox.askquestion ('Install Missing Moduls','Do you want to install openpyxl',icon = 'warning')
                if self.MsgBox == 'yes':
                    os.system("pip3 install openpyxl")
                    tkMessageBox.showinfo("Install","Your Module Installed Successfully. Now you can import datasets.")
                    self.root.destroy()
                    return pd.DataFrame()
                else:
                    tkMessageBox.showinfo("Install","You must Install Missing Modules.") 
                    self.root.destroy()
                    return pd.DataFrame()
        
   
    
    


   
    
    




   
