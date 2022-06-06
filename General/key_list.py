__author__ = 'Tapsas Apostolos', 'Valiakos Apostolos'
from tkinter import *
from tkinter import Tk

class keys_list:
    def __init__(self):
        self.root = Tk()
        self.root.title('Keyboard Shortcuts List')
        #self.root.geometry('600x400')
        w = Canvas(self.root, width=200, height=100)
        w.pack()
        self.text = Text(w)
        scrollbar_tk = Scrollbar(w,orient="vertical")
        scrollbar_tk.pack(side=RIGHT, fill=BOTH)
        self.text.insert(END, "e = Save Data"+"\n")
        self.text.insert(END, "i = Import Data"+"\n")
        self.text.insert(END, "k = Apply Kernel PCA"+"\n")
        self.text.insert(END, "p = Apply PCA"+"\n")
        self.text.insert(END, "s = View Data Statistics"+"\n")
        self.text.insert(END, "t = Open DataDoc Terminal (F5 to run the code)"+"\n")
        self.text.insert(END, "v = View Data"+"\n")
        self.text.insert(END, "ALT + B = Apply Naive Bayes"+"\n")
        self.text.insert(END, "ALT + D = Apply Decision Tree Classification"+"\n")
        self.text.insert(END, "ALT + I = Apply Logistic Regression"+"\n")
        self.text.insert(END, "ALT + K = Apply KNN Classification"+"\n")
        self.text.insert(END, "ALT + R = Apply Random Forest Classification"+"\n")
        self.text.insert(END, "ALT + V = Apply SVM Classification"+"\n")
        self.text.insert(END, "CTRL + D = Apply Decision Tree Regression"+"\n")
        self.text.insert(END, "CTRL + H = Apply Hierarchical Clustering"+"\n")
        self.text.insert(END, "CTRL + K = Apply K-Means"+"\n")
        self.text.insert(END, "CTRL + M = Apply Multivariate Regression"+"\n")
        self.text.insert(END, "CTRL + R = Apply Random Forest Regression"+"\n")
        self.text.insert(END, "CTRL + S = Apply Linear Regression"+"\n")
        self.text.insert(END, "CTRL + V = Apply SVM Regression"+"\n")
        self.text.insert(END, "CTRL + b = Create Box Plot"+"\n")
        self.text.insert(END, "CTRL + c = Apply Chi Square Test"+"\n")
        self.text.insert(END, "CTRL + d = Delete Missing Values"+"\n")
        self.text.insert(END, "CTRL + f = Apply F Test"+"\n")   
        self.text.insert(END, "CTRL + h = Create Histogram"+"\n")
        self.text.insert(END, "CTRL + l = Create Line Plot"+"\n")
        self.text.insert(END, "CTRL + n = Apply Normality Test"+"\n")
        self.text.insert(END, "CTRL + p = Create Pie Chart"+"\n")
        self.text.insert(END, "CTRL + r = Replace Missing Values"+"\n")
        self.text.insert(END, "CTRL + s = Create Scatter Plot"+"\n") 
        self.text.configure(state='disabled')
        self.text.pack()
        scrollbar_tk.config(command=self.text.yview)
        self.root.mainloop()


     

