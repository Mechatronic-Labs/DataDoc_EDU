__author__ = 'Tapsas Apostolos', 'Valiakos Apostolos'
from pydoc import text
from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np
from scipy import stats
from General import tooltipmanager as tlm
from scipy.stats import chi2
from scipy.stats import chi2_contingency
from scipy.stats import chisquare
from scipy.stats import fisher_exact
import pandas as pd
from pandastable import Table
from tkinter import messagebox as tkMessageBox


class chisquare2:
    def __init__(self,df):
        self.df = df
        self.d = df.to_numpy()
        self.names = list(df.columns.values)
        self.master_isdestroed = 0
        
        # Define Main Window and set Title
        self.root = Tk()
        self.root.geometry("800x500")
        self.root.configure(background = '#5c94c5')
        self.root.title('Pearson Chisquare Test')

        # Define Frames  
        # Rigth Frame
        right_f = Frame(self.root,background = '#ff4d4d')
        right_f.pack(side = RIGHT)

        # Bottom Frame
        bottom = Frame(self.root, background = '#ff4d4d')
        bottom.pack(side = BOTTOM)
        
        # Top Frame
        top_f = Frame(self.root, background = 'white')
        top_f.pack(side = TOP)
        
        self.style = ttk.Style()
        self.style.configure('TButton', background = 'dodgerblue')

        # Define Show Results Button and put it on right Frame
        self.show_res = ttk.Button(right_f, text = 'Show Results', command = self.results_table)
        self.show_res.pack(side = LEFT)
        self.show_res.state(["disabled"])
       
        # Define Apply Button and put it on Buttom Frame
        self.bar_plt_b  =  ttk.Button(bottom, text = "Apply", command = self.chi)
        self.bar_plt_b.pack(side = LEFT)
        self.skl45 = tlm.createToolTip(self.bar_plt_b, "Apply paired t-test and Visualize t-value and t-critical value on a normal distributed histogram")
        
        # Define Close Button and put it on Buttom Frame
        ttk.Button(bottom, text = 'Close', command = self.close_program).pack(side = LEFT)
        
        # Define Figure
        fig = Figure(figsize = (10, 6), dpi = 100)
        self.upplot = fig.add_subplot(111)
        
        # Create Blank Figure and Put X and Y Labels Names and Title
        self.a = self.upplot
        self.a.clear()
        self.upplot.title.set_text("Chisquare - Distribution")
        self.upplot.set_xlabel("Value")
        self.upplot.set_ylabel("Density")

        # Create and Plot chisquare Distripution
        self.chidist = chi2(df = len(self.d), loc = 0, scale = 1)
        self.x = np.linspace(self.chidist.ppf(0.0001), self.chidist.ppf(0.9999), 100)
        self.y = self.chidist.pdf(self.x) 
        self.a.plot(self.x, self.y)

        # Create Blank Canva on Root Window and put Figure on it.
        self.canvas = FigureCanvasTkAgg(fig, self.root)
        self.canvas.get_tk_widget().configure(background = 'dodgerblue',  highlightcolor = '#ff4d4d', highlightbackground = '#ff4d4d')
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side = BOTTOM, fill = BOTH, expand = True)


        toolbar = NavigationToolbar2Tk(self.canvas, self.root)
        toolbar.update()
        self.canvas._tkcanvas.pack(side = TOP, fill = BOTH, expand = True)

        self.root.bind('<Escape>', lambda e: self.close_program)
        self.root.protocol("WM_DELETE_WINDOW", self.close_program)
        mainloop()

    def chi(self):
        self.show_res.state(["!disabled"])
        odds ,pp = stats.fisher_exact(self.d)
        self.xval, p_val, n, ex = chi2_contingency(self.d)
        self.xval, p = chisquare(f_obs = self.d, f_exp = ex)
        
        # calculate critical value
        cv  = chi2.ppf(1.0 - 0.05,  n)
        cv1 = chi2.ppf(1.0 - 0.025, n)
        cv2 = chi2.ppf(1.0 - 0.01,  n)

        self.df.n = n
        self.crit_val = cv
        self.chi_val = self.xval[0] + self.xval[1] 
        self.p_val = p_val
        self.odds = odds
        self.se = np.sqrt( (1 / self.d[0][1]) + (1 / self.d[0][0]) + (1 / self.d[1][1]) + (1 / self.d[1][0]) )
        
        # calculate ci
        low = np.log(odds) - (1.96 * self.se)
        up  = np.log(odds) + (1.96 * self.se)
        e = 2.718281
        ci = [e**low, e**up]
        self.ci = "["+str("%.3f" % ci[0])+", "+str("%.3f" % ci[1]) +"]"
        
        if self.chi_val<0:
            cv = cv * (-1)

        self.a.clear()
        self.upplot.title.set_text("Chisquare Distribution")
        self.upplot.set_xlabel("value")
        self.upplot.set_ylabel("Density")

        self.a.plot(self.x, self.y)
        self.a.plot(self.chi_val, self.chidist.pdf(self.chi_val), 'ro', label = 'Value')
        self.a.plot(cv,  self.chidist.pdf(cv),  'ko', label='0.05% Critical Value')
        self.a.plot(cv1, self.chidist.pdf(cv1), 'bo', label='0.025% Critical Value')
        self.a.plot(cv2, self.chidist.pdf(cv2), 'yo', label='0.01% Critical Value')
        legend1 = self.a.legend(loc = "upper right")
        self.a.add_artist(legend1)
        self.canvas.draw()
        
    def results_table(self):
        self.master = Tk()
        self.master.configure(background = '#5c94c5')
        self.master.title("Pearson Chi Test Stats")
        self.master.geometry('800x500') 
        self.fra = Frame(self.master)
        self.fra.pack(fill = BOTH, expand = 1)
        self.master_isdestroed = 1
        df2 = pd.DataFrame([[self.chi_val, self.p_val, self.df.n, self.crit_val, self.odds, self.se, self.ci]], 
                            columns = ["X Value","P Value", "df", "95% Point", "Odds", "SE", "CI"])
        
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
        if (self.p_val < 0.05):
            text = "According to Pearson chi test, sets have significant difference (because p_value = {}) < 0.05)\n" \
            "Thus, data have unequal means.\nImportant, if CI includes 1 we can not reject null hypothesis,"          \
            "hence, we can not say that sets have significant difference."
            tkMessageBox.showinfo("Pearson Chi Test", text.format("%.3f" % self.p_val))
        else:
            text = "According to Pearson chi test, sets not have significant difference (because p_value = {} >= 0.05)" \
            "Thus, data have equal means."
            tkMessageBox.showinfo("Pearson Chi Test", text.format("%.3f" % self.p_val))

    
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

        





