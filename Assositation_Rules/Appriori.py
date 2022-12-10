
__author__ = 'Tapsas Apostolos', 'Valiakos Apostolos'
from tkinter import *
from tkinter import messagebox as tkMessageBox
from tkinter import ttk
import numpy as np
#from apyori import apriori
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from General import tooltipmanager as tlm
from pandastable import Table
import pandas as pd

class appriori:
    def __init__(self,df):
        self.df = df
        self.d = df.to_numpy()
        self.names = list(df.columns.values)
        self.master_isdestroed = 0
        
        # Define Main Window and set Title
        self.root = Tk()
        self.root.geometry("800x500")
        self.root.configure(background='#5c94c5')
        self.root.title('Appriori')
        
        # Insert a Data Item to Avoid Problems
        self.names.insert(0, self.names[0])

        self.v = StringVar(self.root)
        self.v.set(self.names[0]) # set default value first characteristic name

        self.v1 = StringVar(self.root)
        self.v1.set(self.names[1]) # set default value second characteristic name

        # Define Frames  
        # Rigth Frame
        right_f = Frame(self.root,background='#ff4d4d')
        right_f.pack(side=RIGHT)
        
        # Bottom Frame
        bottom = Frame(self.root,background='#ff4d4d')
        bottom.pack(side=BOTTOM)
        
        # Top Frame
        top_f = Frame(self.root,background='white')
        top_f.pack(side=TOP)
        
        # Define Style
        self.style = ttk.Style()
        self.style.configure('TButton', background='dodgerblue')
        
        # Define Show Results Button and put it on right Frame
        self.show_res = ttk.Button(right_f, text='Show Results', command = self.results_table)
        self.show_res.pack(side=LEFT)
        self.show_res.state(["disabled"])
        
        # Define Select list on Top Frame
        self.l9 = Label(top_f,font=('times new roman',12),text='Select the characteristic for independent f-test:',background='white')
        self.l9.pack(side=LEFT)

        # Define First Value Choise
        ttk.OptionMenu(top_f, self.v, *self.names).pack(side=LEFT)
        
        # Define Second Value Choise
        ttk.OptionMenu(top_f, self.v1, *self.names).pack(side=LEFT)
        
        # Define Apply Button and put it on Buttom Frame
        self.bar_plt_b  =  ttk.Button(bottom, text="Apply", command=self.appr)
        self.bar_plt_b.pack(side=LEFT)
        self.skl45 = tlm.createToolTip(self.bar_plt_b, "Apply f-test and Visualize f-value and f-critical value on a f distributed histogram")

        # Define Close Button and put it on Buttom Frame
        self.close = ttk.Button(bottom, text='Close',command=self.close_program)
        self.close.pack(side=LEFT)
        
        # Define Figure
        fig = Figure(figsize=(10,6), dpi=100)
        self.upplot = fig.add_subplot(111)
        
        # Create Blank Figure and Put X and Y Labels Names and Title
        self.a =self.upplot
        self.a.clear()
        self.upplot.title.set_text("f - Distribution")
        self.upplot.set_xlabel("Value")
        self.upplot.set_ylabel("Density")

        # Create and Plot f Distripution 
        self.fdistribution = f(len(self.df[self.names[0]])-1, len(self.names[1])-1)
        self.x = np.linspace(self.fdistribution.ppf(0.0001), self.fdistribution.ppf(0.9999), 100)
        self.y = self.fdistribution.pdf(self.x) 
        self.a.plot(self.x,self.y)

        # Create Blank Canva on Root Window and put Figure on it.
        self.canvas = FigureCanvasTkAgg(fig, self.root)
        self.canvas.get_tk_widget().configure(background='dodgerblue',  highlightcolor='#ff4d4d', highlightbackground='#ff4d4d')
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(self.canvas, self.root)
        toolbar.update()
        self.canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)

        self.root.bind('<Escape>', lambda e: self.close_program)
        self.root.protocol("WM_DELETE_WINDOW", self.close_program)
        mainloop()


    def appr(self):
        self.show_res.state(["!disabled"])
        val, val2 = self.v.get(), self.v1.get()
        
        
        legend1 = self.a.legend(loc="upper right")
        self.a.add_artist(legend1)
        self.canvas.draw()


    def results_table(self):
        self.master = Tk()
        self.master.configure(background='#5c94c5')
        self.master.title("F Test Stats")
        self.master.geometry('800x500') 
        self.fra = Frame(self.master)
        self.fra.pack(fill=BOTH,expand=1)
        self.master_isdestroed = 1
        
        ##df2 = pd.DataFrame([[self.f_val, self.p_value, self.cv1]], columns = ["F Value", "P Value", "95% Point"])
        
        
        self.pt = Table(self.fra, dataframe = df2)
        self.pt.columncolors['mycol'] = 'white'
        self.cl = ttk.Button(self.master, text='Close', command = self.master_destroed).pack(side = RIGHT)
        self.cl = ttk.Button(self.master, text='Test Outcome', command = self.info).pack(side = RIGHT)
        self.pt.show()
        self.pt.redraw()
        
        self.master.bind('<Escape>', lambda e: self.master_destroed)
        self.master.protocol("WM_DELETE_WINDOW", self.master_destroed)
        self.master.mainloop()

    def info(self):
        if (self.p_value<0.05):
            text = "According to f test the data have significant difference between variance (because p_value = {})\nThus the data have unequal variance." 
            tkMessageBox.showinfo("F Test", text.format("%.3f" % self.p_value))
        else:
            text = "According to f test the data not have significant difference between variance (because p_value = {})\nThus the data have unequal variance."
            tkMessageBox.showinfo("F Test", text.format("%.3f" % self.p_value))

    def close_program(self):
        #Checking if child window self.master is active and if it is shows the message to close it first.
        # Note: we use double ifs because we want to avoid the self.master.winfo_exists() == 1 check. 
        # Because when master is destoyed program can not fint self.master window and a bug created.  
        # In order to fix this bug we defined a master destroed function with aim to destroy master and
        # update a flag value named master_destroed.   
        if self.master_isdestroed == 1: 
            if self.master.winfo_exists() == 1: 
                tkMessageBox.showinfo("Important Info","F Test Stats Window is Open Please Close it First.")
        else:
            self.root.destroy()
    
    def master_destroed(self):
        self.master_isdestroed = 0
        self.master.destroy()

