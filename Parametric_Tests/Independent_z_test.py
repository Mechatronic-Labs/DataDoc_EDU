__author__ = 'Tapsas Apostolos', 'Valiakos Apostolos'
from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np
from General import tooltipmanager as tlm
from scipy.stats import norm
from tkinter import messagebox as tkMessageBox
from statsmodels.stats import weightstats as stests
import pandas as pd
from pandastable import Table


class z_test:
    def __init__(self,df):
        self.df = df
        self.d = df.to_numpy()
        self.names = list(df.columns.values)
        self.master_isdestroed = 0

        # Define Main Window and set Title
        self.root = Tk()
        self.root.geometry("800x500")
        self.root.configure(background='#5c94c5')
        self.root.title('Independent T Test')

        # Insert a Data Item to Avoid Problems
        self.names.insert(0, self.names[0])

        self.v = StringVar(self.root)
        self.v.set(self.names[0]) # set default value first characteristic name

        self.v1 = StringVar(self.root)
        self.v1.set(self.names[1]) # set default value second characteristic name

        # Define Frames  
        # Rigth Frame
        right_f = Frame(self.root,background = '#ff4d4d')
        right_f.pack(side = RIGHT)

        # Bottom Frame
        bottom = Frame(self.root,background = '#ff4d4d')
        bottom.pack(side = BOTTOM)
        
        # Top Frame
        top_f = Frame(self.root,background = 'white')
        top_f.pack(side = TOP)

        self.style = ttk.Style()
        self.style.configure('TButton', background='dodgerblue')

        # Define Show Results Button and put it on right Frame
        self.show_res = ttk.Button(right_f, text='Show Results', command=self.results_table)
        self.show_res.pack(side = LEFT)
        self.show_res.state(["disabled"])
      
        # Define Select list on Top Frame
        self.l9 = Label(top_f,font=('times new roman',12),text='Select the characteristic for independent z-test:',background='white')
        self.l9.pack(side = LEFT)
        
        ttk.OptionMenu(top_f, self.v,  *self.names).pack(side = LEFT)
        ttk.OptionMenu(top_f, self.v1, *self.names).pack(side = LEFT)

        # Define Apply Button and put it on Buttom Frame
        self.bar_plt_b  =  ttk.Button(bottom, text = "Apply", command = self.independent)
        self.bar_plt_b.pack(side = LEFT)
        self.skl45 = tlm.createToolTip(self.bar_plt_b, "Apply paired z-test and Visualize z-value and z-critical value on a normal distributed histogram")
        
        # Define Close Button and put it on Buttom Frame
        self.close = ttk.Button(bottom, text = 'Close', command = self.close_program)
        self.close.pack(side = LEFT)
        
        # Define Figure 
        fig = Figure(figsize = (10, 6), dpi = 100)
        self.upplot = fig.add_subplot(111)
    
        # Create Blank Figure and Put X and Y Labels Names and Title
        self.a = self.upplot
        self.a.clear()
        self.upplot.title.set_text("Normal-Distribution")
        self.upplot.set_xlabel("z_value")
        self.upplot.set_ylabel("Density")
        
        # Create and Plot t Distripution
        self.zdistribution = norm(0, 1)
        self.x = np.linspace(self.zdistribution.ppf(0.0001), self.zdistribution.ppf(0.9999), 100)
        self.y = self.zdistribution.pdf(self.x) 
        self.a.plot(self.x, self.y)
        
        # Create Blank Canva on Root Window and put Figure on it.
        self.canvas = FigureCanvasTkAgg(fig, self.root)
        self.canvas.get_tk_widget().configure(background = 'dodgerblue',  highlightcolor = '#ff4d4d', highlightbackground = '#ff4d4d')
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side = BOTTOM, fill = BOTH, expand = True)

        toolbar = NavigationToolbar2Tk(self.canvas, self.root)
        toolbar.update()
        self.canvas._tkcanvas.pack(side = TOP, fill = BOTH, expand = True)

        self.root.bind('<Escape>', self.close_program)
        self.root.protocol("WM_DELETE_WINDOW", self.close_program)
        mainloop()

    def independent(self):
        self.show_res.state(["!disabled"])
        val, val2 = self.v.get(), self.v1.get()
        if val.isdigit():
            val=int(val)
            data1 = self.df[val].values[~np.isnan(self.df[val].values)]
        else:
            data1 = self.df[val].values[~np.isnan(self.df[val].values)]
        if val2.isdigit():
            val2=int(val2)
            data2 = self.df[val2].values[~np.isnan(self.df[val2].values)]
        else:
            data2 = self.df[val2].values[~np.isnan(self.df[val2].values)]

        #check if variance is equal
        # calculate n degrees of freadom
        # Delta Degrees of Freedom: the divisor used in the calculation is N - ddof, where N represents the number of elements. By default, ddof is zero.
        # The mean is normally calculated as x.sum() / N, where N = len(x). If, however, ddof is specified, the divisor N - ddof is used instead.
        # In standard statistical practice, ddof=1 provides an unbiased estimator of the variance of a hypothetical infinite population.
        # ddof=0 provides a maximum likelihood estimate of the variance for normally distributed variables.
        # Statistical libraries like numpy use the variance n for what they call var or variance and the standard deviation.

        #calculate standard error of the mean
        mean_dif = data1 - data2 
        self.mean_dif = np.mean(mean_dif)
        self.se = np.std(mean_dif, ddof=1) / np.sqrt(np.size(mean_dif))

        # calculate n degrees of freadom
        n = len(data1) + len(data2) - 2

        # calculate critical value
        cv  = norm.ppf(1.0 - 0.05 )
        cv1 = norm.ppf(1.0 - 0.025)
        cv2 = norm.ppf(1.0 - 0.01 )

        self.df.n = str(len(self.d[:,0])) + ' + ' + str(len(self.d[:,1]))+'(-2)'+ '=' + str(n)
        self.crit_val = cv1

        # calculate t and p values
        z, p = stests.ztest(data1, data2)
            
        # calculate ci
        low = self.mean_dif - (cv1 * self.mean_dif)
        up  = self.mean_dif + (cv1 * self.mean_dif)
        ci = [low, up]
        self.z_val = z
        self.p_val = p
        self.ci = "["+str("%.3f" % ci[0])+", "+str("%.3f" % ci[1]) +"]"
        
        if z<0:
            z = z * (-1)
                
        self.a.clear()
        self.upplot.title.set_text("Norm-Distribution")
        self.upplot.set_xlabel("z_value")
        self.upplot.set_ylabel("Density")

        self.zdistribution = norm(self.mean_dif, 1)
        self.x = np.linspace(self.zdistribution.ppf(0.0001), self.zdistribution.ppf(0.9999), 100)
        self.y = self.zdistribution.pdf(self.x) 

        self.a.plot(self.x,self.y)
        self.a.plot(cv,  self.zdistribution.pdf(cv),'ko',  label = '0.05% Critical Value')
        self.a.plot(cv1, self.zdistribution.pdf(cv1),'bo', label = '0.025% Critical Value')
        self.a.plot(cv2, self.zdistribution.pdf(cv2),'yo', label = '0.01% Critical Value')
        self.a.plot(z,   self.zdistribution.pdf(z), 'ro',  label = 'z_value')
        legend1 = self.a.legend(loc = "upper right")
        self.a.add_artist(legend1)
        self.canvas.draw()

    def results_table(self):
        self.master = Tk()
        self.master.configure(background='#5c94c5')
        self.master.title("Z Test Stats")
        self.master.geometry('800x500') 
        self.fra = Frame(self.master)
        self.fra.pack(fill = BOTH, expand = 1)
        self.master_isdestroed = 1

        df2 = pd.DataFrame([[self.z_val, self.p_val, self.df.n, self.crit_val, self.mean_dif, self.se, self.ci]], 
                            columns = ["Z Value", "P Value", "df", "95% Point", "mean dif", "std err", "CI"])
        
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
        if (self.p_val<0.05):
            text = "According to z test the data have significant difference between means (because p_value = {} < 0.05)\n" \
            "Thus, data have unequal means.\nImportant, if CI includes 0 we can not reject null hypothesis,"                \
            "hence, we can not say that data have unequal means."
            tkMessageBox.showinfo("z Test", text.format("%.3f" % self.p_val))
        else:
            text = "According to z test the data not have significant difference between means (because p_value = {} >= 0.05)\n" \
            "Thus the data have equal means." 
            tkMessageBox.showinfo("z Test", text.format("%.3f" % self.p_val))

    def close_program(self):
        #Checking if child window self.master is active and if it is shows the message to close it first.
        # Note: we use double ifs because we want to avoid the self.master.winfo_exists() == 1 check. 
        # Because when master is destoyed program can not fint self.master window and a bug created.  
        # In order to fix this bug we defined a master destroed function with aim to destroy master and
        # update a flag value named master_destroed.   
        if self.master_isdestroed == 1: 
            if self.master.winfo_exists() == 1: 
                tkMessageBox.showinfo("Important Info","Z Test Stats Window is Open Please Close it First.")
        else:
            self.root.destroy()
    
    def master_destroed(self):
        self.master_isdestroed = 0
        self.master.destroy()
   
        

    
        

        





