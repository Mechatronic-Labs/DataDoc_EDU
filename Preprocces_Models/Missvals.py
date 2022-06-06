__author__ = 'Tapsas Apostolos', 'Valiakos Apostolos'
from tkinter import messagebox as tkMessageBox

class Preprocessing:
    def del_missing_vals(self,df):
        self.df = df
        self.df = self.df.dropna()
        if self.df.empty:
            tkMessageBox.showinfo("Info","The Dataset is empty please chose another action to clear your dataset")
            return df
        else:
            tkMessageBox.showinfo("Info","Missing Valuse Are Deleted")
            return self.df
    def rep_miss_vals_with_mean_val(self,df):
        df = df.fillna(df.mean())
        return df





