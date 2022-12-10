__author__ = 'Tapsas Apostolos', 'Valiakos Apostolos'
from tkinter import messagebox as tkMessageBox
from tkinter import *

class Check_if_dummyd_exists:
    def __init__(self, df):
        self.df = df
        self.has_dummy = False

        # Take first row of dataframe
        self.checkdata = list(df.iloc[1].values)
        
        # Take datatype for every row's element
        self.types_trace = []

        # Create a mask whitch true values are str types
        [self.types_trace.append(type(self.checkdata[i]).__name__ == 'str') for i in range(0, len(self.checkdata))]
        
        # Use the mask to keep only characteristic names with str data 
        self.names = list(df.columns.values[self.types_trace])
        
        if len(self.names) > 0:
            self.has_dummy = True
            tkMessageBox.showinfo("Importand info","Your Dataframe has dummy variables. For more information about how Datadoc Handles dummy variables go to help>info>Dummy Variables Handling.")
        
    def has_dummy(self):
        return self.has_dummy
            