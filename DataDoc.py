#
# DataDoc application 
#
__author__      = "Apostolos Tapsas", "Apostolos Valiakos"
__copyright__   = "Copyright 2019, Apostolos Tapsas", "Apostolos Valiakos"
__license__     = "Heartbit"
__version__     = "1.0.5"
__email__       = "Apostolos Tapsas", "Apostolos Valiakos"
__status__      = "Production"

# 7113 lines of code and so on 

# Importing Libraries
from tkinter import *
import tkinter
from tkinter import ttk
from PIL import ImageTk
from tkinter import messagebox as tkMessageBox
from tkinter.colorchooser import askcolor
import webbrowser
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


from General import tkHyperlinkManager as thlm
from General import tooltipmanager as tlm
from General import Data_Statistics as ds
from General import bugrep as brep

from Preprocces_Models import Missvals as pr


from Statistic_Tests import normtest as an
from Statistic_Tests import F_test as ft


from Preprocces_Models import PCA as pca
from Preprocces_Models import Kernel_PCA as kpca



from IO import Import_data as im_data
from IO import View_Data as vd
from IO import Dummy_Data as Dumd

# Paremetric tests import
from Parametric_Tests import Independent_t_test as itt
from Parametric_Tests import Independent_z_test as izt
from Parametric_Tests import Paired_t_test as ptt


# Nonparemetric tests import
from Non_Parametric_Tests import Wilcoxon as wlcx
from Non_Parametric_Tests import Mann_Whitney_Wilcoxon as MWwlcx
from Non_Parametric_Tests import Chisqueare as chi2
from Non_Parametric_Tests import One_Sample_Kolmogorov_Smirnov as OSKS


# Visualization Imports
from Data_Visualization import Box_Plot as BP
from Data_Visualization import Pie_Chart as PCH
from Data_Visualization import Scatter_Plot as SP
from Data_Visualization import Line_Graph as LN
from Data_Visualization import Histogram as HS


# Regression  and Cassification Imports
from Data_Mining_Models import Simple_Linear_Regrassion as SLR
from Data_Mining_Models import Multiple_Linear_Regrassion as MLR
from Data_Mining_Models import Support_Vectors as SVM
from Data_Mining_Models import Decision_Tree as DT
from Data_Mining_Models import Random_Forest as RF
from Data_Mining_Models import K_Means as KM
from Data_Mining_Models import Hierarchical_Clustering as HC
from Data_Mining_Models import Logistic_Regrassion as LR
from Data_Mining_Models import K_Nearest_Neighbor as KNN
from Data_Mining_Models import Naive_Bayes as NBY

from General import about
from General import key_list

import matplotlib.image as mpimg
from General import splash 



class DataDoc:
    def __init__(self):
        # Splash Screen
        self.root = Tk()
        self.root.overrideredirect(True)
        app = splash.SplashScreen(self.root)
        self.root.after(9010, self.root.destroy)
        self.root.mainloop()

        # Define Dataset
        self.Dataset=[]
        
        # Define theme
        self.sel_theme = 'basic'

        # Create application Gui
        self.app = Tk(className = 'DataDoc')
        self.app.title("DataDoc 1.0")
        self.app.geometry("940x540")
        #self.app.attributes('-fullscreen', True)
        #self.app.resizable(0,0)
        icon_img = PhotoImage(file='icons/logo.PNG')
        self.app.tk.call('wm', 'iconphoto', self.app._w, icon_img)
        self.bg_color  = 'white'
        self.tab_color = '#5c94c5'
        
        # Put First and Second frames background color
        self.style = ttk.Style(self.app)
        self.style.configure('lefttab.TNotebook', tabposition ='wn', background = self.tab_color)
        self.style.configure('new.TFrame', background=self.bg_color)
        
        # Fit the selection buttons on application's right site 
        self.note = ttk.Notebook(self.app, style='lefttab.TNotebook')

        # Create the two buttons will fit in the right site
        self.tab1 = ttk.Frame(self.note, style='new.TFrame')
        self.tab5 = ttk.Frame(self.note, style='new.TFrame')
        self.tab4 = ttk.Frame(self.note, style='new.TFrame')
        self.tab2 = ttk.Frame(self.note, style='new.TFrame')
        self.tab3 = ttk.Frame(self.note, style='new.TFrame')
        self.tab6 = ttk.Frame(self.note, style='new.TFrame')
        
        # Put them images (tabs images)
        self.home_image       = PhotoImage(file = "icons/home.png")
        self.ass_image        = PhotoImage(file = "icons/p_ass.png")
        self.image_pros_image = PhotoImage(file = "icons/imege_pross.png")
        self.nntab_image      = PhotoImage(file = "icons/p_neuralnets.png")
        self.bug_image        = PhotoImage(file = "icons/p_bug.png")
        self.ter_image        = PhotoImage(file = "icons/p_vis.png")
        self.info_image       = PhotoImage(file = "icons/p_info.png")
        self.term_image       = PhotoImage(file = "icons/install.png")
       
        # Pack them also tabs view order
        self.note.add(self.tab1, text = "Data",   image = self.home_image)
        self.note.add(self.tab5, text = "View",   image = self.ter_image)
        self.note.add(self.tab4, text = "Neural", image = self.nntab_image)
        self.note.add(self.tab2, text = "Rules" , image = self.ass_image)
        #self.note.add(self.tab3, text = "I", image = self.image_pros_image)
        #self.note.add(self.tab6, text = "About DataDoc", image = self.info_image)
        self.note.pack(fill=BOTH, expand=True, side='right')

        # Pack buttons to the left side
        self.bug  = ttk.Button(self.note,text='Doc', image = self.bug_image, command = self.repbug)
        self.bug.pack(side=BOTTOM, anchor=W) 

        #Create  Menu
        self.menu = Menu(self.app)
        self.app.config(menu=self.menu)
        self.submenu2=Menu(self.menu)


        # Preprocces Menu
        #========================================================================================
        self.preprocces_menu = Menu(self.menu)
        self.miss_val_menu   = Menu(self.menu)
        self.pca_menu        = Menu(self.menu)

        self.miss_val_image      = PhotoImage(file = "icons/p_missing_value1.png")
        self.del_miss_val_image  = PhotoImage(file = "icons/p_missing_cor1.png")
        self.mean_miss_val_image = PhotoImage(file = "icons/p_missing_cor2.png")

        # Put tab in root
        self.menu.add_cascade(label="Preprocces", menu=self.preprocces_menu)

        # First menu of Preprocces tab
        self.preprocces_menu.add_cascade(label="Missing Values Manager", image = self.miss_val_image, menu = self.miss_val_menu)

        # Sub menus of First menu of Preprocces tab
        self.miss_val_menu.add_command(label="Delete Missing Values", image = self.del_miss_val_image, command = self.del_miss_vals)
        self.miss_val_menu.add_command(label="Replace Missing Values With Mean",image = self.mean_miss_val_image, command = self.rep_means)
        self.stat_proc_image = PhotoImage(file = "icons/p_stat_pro.png")

        self.pca_image = PhotoImage(file = "icons/p_pca.png")
        self.kpca_image = PhotoImage(file = "icons/p_kpca.png")

        # Second menu of Preprocces tab
        self.preprocces_menu.add_cascade(label="Statistical Procedures",image = self.stat_proc_image, menu = self.pca_menu)


        # Sub menus of Second menu of Preprocces tab
        self.pca_menu.add_command(label="Principal Component Analysis", image = self.pca_image, command = self.prica)
        self.pca_menu.add_command(label="Kernel Principal Component Analysis", image = self.kpca_image, command = self.kprica)


        # Analyze
        #========================================================================================
        # Define images for Analyze menu
        self.ds        = PhotoImage(file = "icons/p_da.png")
        self.normality = PhotoImage(file = "icons/p_nor_test.png")
        self.f_test    = PhotoImage(file = "icons/p_f_test.png")
        self.chi_test  = PhotoImage(file = "icons/p_chisquare.png")


        self.filemenu = Menu(self.menu)
        self.menu.add_cascade(label="Analyze", menu=self.submenu2)
        self.submenu2.add_cascade(label="Descriptive Statistics",image=self.ds, menu = self.filemenu)
        self.filemenu.add_command(label="Normality Test", image=self.normality, command = self.norm_test)
        self.filemenu.add_command(label="F Test", image=self.f_test, command = self.ftest)
        self.filemenu = Menu(self.menu)
        

        #Compare Means
        #========================================================================================
        #Define images for Compare Means menu
        self.cm  = PhotoImage(file = "icons/p_cm.png")
        self.tt1 = PhotoImage(file = "icons/p_i_t_t.png")
        self.tt2 = PhotoImage(file = "icons/p_p_t_t.png")
        self.tt3 = PhotoImage(file = "icons/p_i_t_z.png")


        self.submenu2.add_cascade(label="Compare Means",image = self.cm ,menu = self.filemenu)
        self.filemenu.add_command(label="Independent Sample t-test", image = self.tt1, command=self.in_t_test)
        self.filemenu.add_command(label="Independent Sample z-test", image = self.tt3, command=self.in_z_test)
        self.filemenu.add_command(label="Paired Sample t-test", image = self.tt2, command=self.p_t_test)
        self.filemenu = Menu(self.menu)

        #Non parametric Tests
        #========================================================================================
        #Define images for Non parametric Tests
        self.nparam        = PhotoImage(file = "icons/dstats.png")
        self.paired_wl     = PhotoImage(file = "icons/p_wil.png")
        self.indepe_wl     = PhotoImage(file = "icons/p_inwil.png")


        self.submenu2.add_cascade(label="Non Parametric Tests", image = self.nparam, menu = self.filemenu)
        self.filemenu.add_command(label="Chisquare Test", image = self.chi_test, command = self.chi)
        self.filemenu.add_command(label="Paired Sample Wilcoxon test", image = self.paired_wl, command = self.Wilcox)
        self.filemenu.add_command(label="Independent Sample Mann_Whitney_Wilcoxon", image = self.indepe_wl, command = self.Mann_Whitney_Wilcoxon)
        self.filemenu = Menu(self.menu)


        # Regression Menu
        #========================================================================================
        # Create the Menus
        self.regression_menu = Menu(self.menu)
        self.linear_menu     = Menu(self.menu)
        self.svm_menu        = Menu(self.menu)
        self.dt_menu         = Menu(self.menu)

        # Put tab in root
        self.menu.add_cascade(label = "Regression", menu = self.regression_menu)
        self.reg = PhotoImage(file = "icons/p_linear.png")

        # First menu of Preprocces tab
        self.regression_menu.add_cascade(label = "Linear Models", image = self.reg, menu = self.linear_menu)
        self.lr= PhotoImage(file = "icons/p_linear_reg.png")
        self.mr= PhotoImage(file = "icons/p_mul_reg.png")

        # Sub menus of First menu of Preprocces tab
        self.linear_menu.add_command(label="Simple Linear Regression", image = self.lr, command = self.slr)
        self.linear_menu.add_command(label="Multivariate Regression",  image = self.mr, command = self.mlr)
        self.svm_reg = PhotoImage(file = "icons/p_svm_rec.png")
        self.svm_mod = PhotoImage(file = "icons/p_svm_mod.png")

        # Second menu of Preprocces tab
        self.regression_menu.add_cascade(label="Support Vector Model", image = self.svm_mod, menu = self.svm_menu)

        # Sub menus of Second menu of Preprocces tab
        self.svm_menu.add_command(label="Support Vector Regression", image = self.svm_reg, command = self.svr)
        self.d_tree_mod = PhotoImage(file = "icons/p_dtree_mod.png")
        self.d_tree_reg = PhotoImage(file = "icons/p_dtree_reg.png")
        self.rand_for   = PhotoImage(file = "icons/p_rf.png")

        # 3rd menu of Preprocces tab
        self.regression_menu.add_cascade(label="Decision tree models", image = self.d_tree_mod, menu = self.dt_menu)

        # Sub menus of 3rd menu of Preprocces tab
        self.dt_menu.add_command(label="Decision Tree Regression", image = self.d_tree_reg, command = self.dt_r)
        self.dt_menu.add_command(label="Random Forest Regression", image = self.rand_for, command = self.rf_r)


        # Classification Menu
        #=========================================================================================
        self.classification_menu = Menu(self.menu)
        self.c_linear_menu       = Menu(self.menu)
        self.c_svm_menu          = Menu(self.menu)
        self.c_dt_menu           = Menu(self.menu)
        self.bayes               = Menu(self.menu)
        self.knn_menu            = Menu(self.menu)

        # Put tab in root
        self.menu.add_cascade(label = "Classification", menu = self.classification_menu)

        # First menu of Preprocces tab
        self.classification_menu.add_cascade(label = "Linear Models", image = self.reg, menu = self.c_linear_menu)
        self.log_reg = PhotoImage(file = "icons/p_logistic_reg.png")

        # Sub menus of First menu of Preprocces tab
        self.c_linear_menu.add_command(label = "Logistic Regression", image = self.log_reg, command = self.logreg)

        self.svm                 = PhotoImage(file = "icons/p_svm.png")
        self.svm_class           = PhotoImage(file = "icons/p_svm_class.png")
        self.rand_for_c          = PhotoImage(file = "icons/p_rf_c.png")
        self.d_tree_c            = PhotoImage(file = "icons/p_dtree_c.png")
        self.naive               = PhotoImage(file = "icons/p_nb.png")
        self.bayes_c             = PhotoImage(file = "icons/p_nb_c.png")
        self.knn_c               = PhotoImage(file = "icons/p_knn.png")
        self.vector_quantization = PhotoImage(file = "icons/p_v.png")

        self.classification_menu.add_cascade(label = "Vector Quantization", image= self.vector_quantization, menu = self.knn_menu)

        # Sub menus of Second menu of Preprocces tab
        self.knn_menu.add_command(label = "KNN", image=self.knn_c ,command=self.knn)
        
        # Second menu of Preprocces tab
        self.classification_menu.add_cascade(label = "Support Vector Model", image = self.svm, menu = self.c_svm_menu)


        # Sub menus of Second menu of Preprocces tab
        self.c_svm_menu.add_command(label = "Support Vector Classifier", image = self.svm_class, command = self.svc)


        # 3rd menu of Preprocces tab
        self.classification_menu.add_cascade(label = "Decision tree models", image = self.d_tree_mod, menu = self.c_dt_menu)


        # Sub menus of 3rd menu of Preprocces tab
        self.c_dt_menu.add_command(label = "Decision Tree Classifier", image = self.d_tree_c, command = self.dt_c)
        self.c_dt_menu.add_command(label = "Random Forest Classifier", image = self.rand_for_c, command = self.rf_c)

        # Bayes Menu
        self.classification_menu.add_cascade(label = "Bayes Model",image = self.bayes_c, menu = self.bayes)
        self.bayes.add_command(label = "Naive Bayes",              image = self.naive,   command = self.nb)


        # Clusstering Menu
        #==========================================================================================
        self.kmeans_image   = PhotoImage(file = "icons/p_kmeans.png")
        self.hierart_image  = PhotoImage(file = "icons/p_hp.png")

        self.clustering_menu = Menu(self.menu)
        self.kmeans_menu     = Menu(self.menu)

        # Put tab in root
        self.menu.add_cascade(label = "Clustering", menu = self.clustering_menu)

        # First menu of Preprocces tab
        self.clustering_menu.add_cascade(label = "Vector Quantization",image = self.vector_quantization, menu = self.kmeans_menu)

        # Sub menus of 3rd menu of Preprocces tab
        self.kmeans_menu.add_command(label = "Hierarchical clustering", image = self.hierart_image, command = self.hc)
        self.kmeans_menu.add_command(label = "K-Means",                 image = self.kmeans_image,  command = self.km)
        

        # Settings Menu
        #==========================================================================================
        self.settings_menu = Menu(self.menu)
        self.menu.add_cascade(label = "Settings", menu = self.settings_menu)
        
       
        # Themes Menu
        #==========================================================================================
        self.themes_menu = Menu(self.menu)
        self.settings_menu.add_cascade(label = "Themes", menu = self.themes_menu)
        self.themes_menu.add_command  (label = "Basic",  command = '')
    
       
        # Help Menu
        #==========================================================================================
        self.about_menu = Menu(self.menu)
        self.info_menu  = Menu(self.menu)
        
        self.menu.add_cascade(label = 'Help', menu = self.about_menu)
        self.about_menu.add_command(label = 'Keyboard Shortcuts List',   command = self.key_list)
        self.about_menu.add_cascade(label = 'Info',                      menu = self.info_menu)
        self.info_menu.add_command (label = 'Dummy Variables Handling', command = self.dummy_values_handling_info)
        self.info_menu.add_command (label = 'Missing Values Handling',  command = self.missing_values_handling_info)
        self.info_menu.add_command (label = 'About Datadoc',            command = self.abt)
        

        # First Tab Buttons
        #==========================================================================================
        self.imdb = PhotoImage(file = "icons/imdb.png")
        self.scp  = PhotoImage(file = "icons/scaplot.png")
        self.abt  = PhotoImage(file = "icons/sti2.png")
        self.shd  = PhotoImage(file = "icons/p_ds.png")
        self.vie  = PhotoImage(file = "icons/p_view.png")        
        
        # To work with createToolTip class you should create the buttons as below
        self.import_data_button1 = ttk.Button(self.tab1, text = 'S', image = self.imdb, command = self.import_dataset)
        self.import_data_button1.grid(row = 1, column = 0)
        self.sk_tip = tlm.createToolTip(self.import_data_button1, 'Import a dataset from .xlsx or .xls files.')

        self.import_data_button2 = ttk.Button(self.tab1, text = 'S', image = self.shd , command = self.data_stats)
        self.import_data_button2.grid(row = 1, column = 1)
        self.sk_tip = tlm.createToolTip(self.import_data_button2, 'Show Data Statistics')


        self.import_data_button3 = ttk.Button(self.tab1, text = 'S', image = self.vie, command = self.view)
        self.import_data_button3.grid(row = 1, column = 2)
        self.skl2 = tlm.createToolTip(self.import_data_button3, "View dataset.")
        
        # Neural nets  Tab Buttons
        #==========================================================================================        
        self.NLP_ico = PhotoImage(file = "icons/p_NN.png")
        self.CNN_ico = PhotoImage(file = "icons/p_NN1.png")
        self.MLP_ico = PhotoImage(file = "icons/p_NN2.png")

        self.nn_btn   = ttk.Button(self.tab4, text = 'S', image = self.MLP_ico, command = self.show_app)
        self.nn_btn.grid(row = 1,column = 0)
        self.nn_tip = tlm.createToolTip(self.nn_btn, "Build Neural Net")

        self.cnn_btn   = ttk.Button(self.tab4, text = 'S', image = self.CNN_ico, command = self.show_app)
        self.cnn_btn.grid(row = 1,column = 1)
        self.cnn_tip = tlm.createToolTip(self.cnn_btn, "Build a Convolutional Neural Network")
        
        self.nlp_btn   = ttk.Button(self.tab4, text = 'S', image = self.NLP_ico, command = self.show_app)
        self.nlp_btn.grid(row=2,column=0)
        self.nlp_tip = tlm.createToolTip(self.nlp_btn, "Build NLP Neural Network")

        # Association Rules  Tab Buttons
        #==========================================================================================
        #S = ttk.Label(self.tab2, text= "External Modules Installation", background="white",font = "Times", anchor='nw').grid(row=0,column=0)
        self.apriori_pic = PhotoImage(file = "icons/p_appriori.png")
        self.apriori_btn   = ttk.Button(self.tab2,image=self.apriori_pic, text='S', command = self.show_app)
        self.apriori_btn.grid(row = 1, column = 0)
        self.apriori_tip = tlm.createToolTip(self.apriori_btn, 'a priori')


        self.eclat_pic = PhotoImage(file = "icons/p_eclat.png")
        self.eclat_btn = ttk.Button(self.tab2, image = self.eclat_pic,text='S', command = self.show_app)
        self.eclat_btn.grid(row = 1, column = 1)
        self.eclat_tip = tlm.createToolTip(self.eclat_btn, 'eclat')

        self.fp_pic = PhotoImage(file = "icons/p_fp.png")
        self.fp_btn = ttk.Button(self.tab2,image = self.fp_pic, text ='S', command = self.show_app)
        self.fp_btn.grid(row = 2, column = 0)
        self.fp_tip = tlm.createToolTip(self.fp_btn, 'fp')
        

        # Vizualize Tab Buttons
        #==========================================================================================
        #Create Button images
        self.hist_pic = PhotoImage(file = "icons/p_hist.png")
        self.box_pic  = PhotoImage(file = "icons/p_box_btn.png")
        self.pie_pic  = PhotoImage(file = "icons/p_pie.png")
        self.sc_pic   = PhotoImage(file = "icons/scaplot.png")
        self.line_pic = PhotoImage(file = "icons/p_line_graph.png")
        self.bar_pic  = PhotoImage(file = "icons/p_bar.png")

        #Histogram
        self.hist_btn   = ttk.Button(self.tab5, text = 'S', image = self.hist_pic, command = self.hist_graph)
        self.hist_btn.grid(row = 1, column = 0)
        self.hist_tip = tlm.createToolTip(self.hist_btn, "Show dataset's histogram and statistics of selected characteristics, such as standard deviation, mean, median, etc.")


        #Boxplot
        self.box_btn = ttk.Button(self.tab5, text='S', image = self.box_pic, command = self.box_graph)
        self.box_btn.grid(row = 1, column = 1)
        self.box_tip = tlm.createToolTip(self.box_btn, "Show dataset's box plot and statistics of selected characteristics, such as standard deviation, mean, median, etc.")

        #Piechart 
        self.pie_btn = ttk.Button(self.tab5, text='S', image = self.pie_pic, command = self.pie_chart)
        self.pie_btn.grid(row = 1, column = 2)
        self.pie_tip = tlm.createToolTip(self.pie_btn, "Show dataset's pie chart and statistics of selected characteristics, such as standard deviation, mean, median, etc.")

        #Scatter plot 
        self.sc_btn  = ttk.Button(self.tab5, text='S', image=self.sc_pic, command = self.plot_data)
        self.sc_btn.grid(row = 2,column = 0)
        self.sc_btn_tip  = tlm.createToolTip(self.sc_btn, "Show dataset's scater plot illustation.\nIf dataset dimensions is over 3 then the tool automatically will apply PCA to dataset with aim to create a 3d scatter plot.")

        #Line plot
        self.line_btn = ttk.Button(self.tab5, text='S', image = self.line_pic, command = self.line_graph)
        self.line_btn.grid(row = 2, column = 1)
        self.line_tip = tlm.createToolTip(self.line_btn, "Show dataset's lineplot and statistics of selected characteristics, such as standard deviation, mean, median, etc.")
        

        S = ttk.Label(self.tab3, text = "Image Processing", background = "white", font = "Times").grid(row = 0, column = 0)

        text = Text(self.tab6)
        text.grid(row = 0, column = 0)
        self.hyperlink = thlm.HyperlinkManager(text)
        text.insert(INSERT, "The Heartbit",self.hyperlink.add(self.about_us))
        text.insert(INSERT, " Datadoc software platform offers advanced statistical analysis, a vast library of machine-learning algorithms, image procesing")
        text.insert(INSERT, " integration with bigdata and seamless deployment into applications. Its ease of use, flexibility and scalability make Datadoc accessible,")
        text.insert(INSERT, " to users with all skill levels and outfits projects of all sizes and complexity to help you and your organization find new opportunities, improve efficiency and minimize risk.")
        text.configure(state='disabled')



        # create keysortcuts
        self.app.bind('<i>', self.import_dataset)
        self.app.bind('<k>', self.kprica)
        self.app.bind('<p>', self.prica)
        self.app.bind('<s>', self.data_stats)
        self.app.bind('<v>', self.view)
        self.app.bind('<Alt-B>', self.nb)
        self.app.bind('<Alt-D>', self.dt_c)
        self.app.bind('<Alt-I>', self.logreg)
        self.app.bind('<Alt-K>', self.knn)
        self.app.bind('<Alt-R>', self.rf_c)
        self.app.bind('<Alt-V>', self.svc)
        self.app.bind('<Control-D>', self.dt_r)
        self.app.bind('<Control-H>', self.hc)
        self.app.bind('<Control-K>', self.km)
        self.app.bind('<Control-M>', self.mlr)
        self.app.bind('<Control-R>', self.rf_r)
        self.app.bind('<Control-S>', self.slr)
        self.app.bind('<Control-V>', self.svr)
        self.app.bind('<Control-b>', self.box_graph)
        self.app.bind('<Control-c>', self.chi)
        self.app.bind('<Control-d>', self.del_miss_vals)
        self.app.bind('<Control-f>', self.ftest)
        self.app.bind('<Control-h>', self.hist_graph)
        self.app.bind('<Control-l>', self.line_graph)
        self.app.bind('<Control-n>', self.norm_test)
        self.app.bind('<Control-p>', self.pie_chart)
        self.app.bind('<Control-r>', self.rep_means)
        self.app.bind('<Control-s>', self.plot_data)
        self.app.bind('<Alt-p>', self.on_closing)
        self.app.bind('<Escape>', self.on_closing)
        
        #Set fullscreen key
        self.app.bind('<f>', lambda event: self.app.attributes("-fullscreen", not self.app.attributes("-fullscreen")))

        self.app.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.app.mainloop()
    
    def on_closing(self, event=None):
        if tkMessageBox.askokcancel("Quit", "Do you want to quit DataDoc?"):
            self.app.destroy()
    
    def key_list(self):
        print (key_list.keys_list())

    def about_us(self):
        webbrowser.open('https://heartbit.gr')
    
    def basic_theme(self,event=None):

        self.sel_theme = 'basic'                                              
        self.style.configure('new.TFrame', background='white')
        self.style.configure('lefttab.TNotebook', tabposition='wn', background='#5c94c5')

        # change tab images
        self.home_image = PhotoImage(file = "icons/home.png")
        
        self.note.tab(self.tab1,image=self.home_image)
        #self.note.tab(self.tab1,image='')

        self.vis_image = PhotoImage(file = "icons/p_vis.png")
        self.note.tab(self.tab5,image=self.vis_image)
        #self.note.tab(self.tab5,image='')

        # first tab button update
        self.imdb = PhotoImage(file = "icons/imdb.png")
        self.import_data_button1.configure(image=self.imdb)

        self.shd  = PhotoImage(file = "icons/p_ds.png")
        self.import_data_button2.configure(image=self.shd)

        self.vie  = PhotoImage(file = "icons/p_view.png")
        self.import_data_button3.configure(image=self.vie)

        self.svi  = PhotoImage(file = "icons/saved.png")
        self.import_data_button4.configure(image=self.svi)


        # second tab button update
        self.hist_pic = PhotoImage(file = "icons/p_hist.png")
        self.hist_btn.configure(image=self.hist_pic)

        
        self.box_pic = PhotoImage(file = "icons/p_box_btn.png")
        self.box_btn.configure(image=self.box_pic)

        self.pie_pic = PhotoImage(file = "icons/p_pie.png")
        self.pie_btn.configure(image=self.pie_pic)

        self.sc_pic = PhotoImage(file = "icons/scaplot.png")
        self.sc_btn.configure(image=self.sc_pic)

        self.line_pic = PhotoImage(file = "icons/p_line_graph.png")
        self.line_btn.configure(image=self.line_pic)

        self.bar_pic = PhotoImage(file = "icons/p_bar.png")
        self.bar_btn.configure(image=self.bar_pic )


        # Bug image
        self.bug_image = PhotoImage(file = "icons/p_bug.png")
        self.bug_image.configure(image = self.bug_image)

        self.packages_image = PhotoImage(file = "icons/install.png")
        self.exe.configure(image = self.packages_image)
    
    def show_app(self,event=None):
        tkMessageBox.showinfo("Info","This Module is Under Construction")
    
    def missing_values_handling_info(self, event=None):
        tkMessageBox.showinfo("Missing Values Handling Info","DataDoc allows user to handle missing values with 2 ways. First, it gives them the option to delete missing values, deleting the whole sample. This technique may be harmfull for the Dataset because it reduces the length of it, or even erase it. The second way is to replace the missing values with the mean of the characteristic of the column that the missing value was detected(in extreme values case). Even though this is a safer technique for the dataset, it produces values to it which some times is undesirable. In case which user do not selects any of ways descriped DataDoc automaticaly deletes missing values where an action is selected (i.e. Data Statistics, Parametric and non tests or model creation etc.).")
    
    def dummy_values_handling_info(self, event=None):
        tkMessageBox.showinfo("Dummy Values Handling Info","DataDoc handles dummy variables automatically after informing user that Dataset has them. When an action selected (i.e. Data Statistics, Parametric and non tests or model creation etc.) DataDoc automatically will transform possible dummy variables to new collumns with zeroes and ones. Value of one (1) represents the possition which the string values was insite before the transormation. User must be careful with aim to avoid dummy variable trap.")
     
    def import_dataset(self,event=None):
        # Load dataset 
        if len(self.Dataset)==0:
            self.Dataset = im_data.import_data().load_data()
            if self.Dataset.isnull().any().any():
                tkMessageBox.showinfo("Important Info","Dataset Has Missing Values That Maybe Create Problems During Data Analysis. We Propose To Delete or Replace Them via Preprocess Menu. For more information about how Datadoc Handles missing values go to help>info>Missing Values Handling.")
            # Check if Dataset has Dummy Variables
            # It is not necessary to pass entire dataset
            Dumd.Check_if_dummyd_exists(self.Dataset.head())
        else:
            # Load new Dataset case 
            if tkMessageBox.askokcancel("Important Message", "Do you want to load new Dataset?"):
                self.Dataset = im_data.import_data().load_data()
                if self.Dataset.isnull().any().any():
                    tkMessageBox.showinfo("Important Info","Dataset Has Missing Values That Maybe Create Problems During Data Analysis. We Propose To Delete or Replace Them via Preprocess Menu. For more information about how Datadoc Handles missing values go to help>info>Missing Values Handling")
                # Check if Dataset has Dummy Variables
                # It is not necessary to pass entire dataset
                Dumd.Check_if_dummyd_exists(self.Dataset.head())
    
    def view(self,event=None):
        if len(self.Dataset)==0:
            tkMessageBox.showinfo("Error","Dataset matrix is empty please import dataset")
        else:
            vd.Data_viewer(self.Dataset)
               
    def data_stats(self,event=None):
        if len(self.Dataset)==0:
            tkMessageBox.showinfo("Error","Dataset matrix is empty please import dataset")

        else:
            ds.Data_Statistics(self.Dataset)

    def plot_data(self,event=None):
        if len(self.Dataset)==0:
            tkMessageBox.showinfo("Error","Dataset matrix is empty please import dataset")

        else:
            SP.Scatter_Plot(self.Dataset)

    def del_miss_vals(self,event=None):
        if len(self.Dataset)==0:
            tkMessageBox.showinfo("Error","Dataset matrix is empty please import dataset")

        else:
            self.Dataset = pr.Preprocessing().del_missing_vals(self.Dataset)

    def rep_means(self,event=None):
        if len(self.Dataset)==0:
            tkMessageBox.showinfo("Error","Dataset matrix is empty please import dataset")

        else:
            self.Dataset = pr.Preprocessing().rep_miss_vals_with_mean_val(self.Dataset)
            tkMessageBox.showinfo("Info","Missing Values Are Replaced With Mean Values")

    def docs(self):
        webbrowser.open("https://heartbit.gr/datadoc-documentation/")

    def norm_test(self,event=None):
         if len(self.Dataset)==0:
            tkMessageBox.showinfo("Error","Dataset matrix is empty please import dataset")

         else:
             an.Analyze(self.Dataset)

    def ftest(self,event=None):
         if len(self.Dataset)==0:
            tkMessageBox.showinfo("Error","Dataset matrix is empty please import dataset")

         else:
             ft.f_test(self.Dataset)

    def chi(self,event=None):
        if len(self.Dataset)==0:
            tkMessageBox.showinfo("Error","Dataset matrix is empty please import dataset")

        else:
             chi2.chisquare2(self.Dataset)

    def in_t_test(self):
        if len(self.Dataset)==0:
            tkMessageBox.showinfo("Error","Dataset matrix is empty please import dataset")

        else:
            itt.t_test(self.Dataset)

    
    def in_z_test(self):
        if len(self.Dataset)==0:
            tkMessageBox.showinfo("Error","Dataset matrix is empty please import dataset")

        else:
            izt.z_test(self.Dataset)


    def p_t_test(self):
        if len(self.Dataset)==0:
            tkMessageBox.showinfo("Error","Dataset matrix is empty please import dataset")

        else:
            ptt.t_test(self.Dataset)


    def Wilcox(self):
        if len(self.Dataset)==0:
            tkMessageBox.showinfo("Error","Dataset matrix is empty please import dataset")

        else:
            wlcx.Wilcoxon_Test(self.Dataset)

    
    def Mann_Whitney_Wilcoxon(self):
        if len(self.Dataset)==0:
            tkMessageBox.showinfo("Error","Dataset matrix is empty please import dataset")

        else:
            MWwlcx.Mann_Whitney_Wilcoxon(self.Dataset)


    
    # Data Visualization    
    def pie_chart(self,event=None):
         if len(self.Dataset)==0:
            tkMessageBox.showinfo("Error","Dataset matrix is empty please import dataset")

         else:
             PCH.Pie_Chart(self.Dataset)

    def line_graph(self,event=None):
         if len(self.Dataset)==0:
            tkMessageBox.showinfo("Error","Dataset matrix is empty please import dataset")

         else:
             LN.Line_Graph(self.Dataset)

    def box_graph(self,event=None):
         if len(self.Dataset)==0:
            tkMessageBox.showinfo("Error","Dataset matrix is empty please import dataset")

         else:
             BP.Box_Plot(self.Dataset,self.sel_theme)


    def hist_graph(self,event=None):
         if len(self.Dataset)==0:
            tkMessageBox.showinfo("Error","Dataset matrix is empty please import dataset")

         else:
             HS.Histogram(self.Dataset)


    def in_sklearn(self):
        os.system("pip install -U scikit-learn")
        tkMessageBox.showinfo("Install","Scikit Learn Installed Successfully.")

    #PCA
    def prica(self,event=None):
        if len(self.Dataset)==0:
            tkMessageBox.showinfo("Error","Dataset matrix is empty please import dataset")

        else:
            pca.pca(self.Dataset)
            
    def kprica(self,event=None):
        if len(self.Dataset)==0:
            tkMessageBox.showinfo("Error","Dataset matrix is empty please import dataset")

        else:
            kpca.Kernel_PCA(self.Dataset)


    # Regression
    def slr(self,event=None):
        if len(self.Dataset)==0:
            tkMessageBox.showinfo("Error","Dataset matrix is empty please import dataset")

        else:
            SLR.Simple_Linear_Regrassion(self.Dataset,'r')

    def mlr(self,event=None):
         if len(self.Dataset)==0:
            tkMessageBox.showinfo("Error","Dataset matrix is empty please import dataset")

         else:
             MLR.Multiple_Linear_Regrassion(self.Dataset,'r')

    def svr(self,event=None):
         if len(self.Dataset)==0:
            tkMessageBox.showinfo("Error","Dataset matrix is empty please import dataset")

         else:
             SVM.Support_Vectors(self.Dataset,'r')
    def dt_r(self,event=None):
        if len(self.Dataset)==0:
            tkMessageBox.showinfo("Error","Dataset matrix is empty please import dataset")

        else:
            DT.Decision_trees(self.Dataset,'r') 

    def rf_r(self,event=None):
        if len(self.Dataset)==0:
            tkMessageBox.showinfo("Error","Dataset matrix is empty please import dataset")

        else:
            RF.Random_Forest(self.Dataset,'r')

    def km(self,event=None):
        if len(self.Dataset)==0:
            tkMessageBox.showinfo("Error","Dataset matrix is empty please import dataset")

        else:
            KM.K_Means(self.Dataset)

    def hc(self,event=None):
        if len(self.Dataset)==0:
            tkMessageBox.showinfo("Error","Dataset matrix is empty please import dataset")

        else:
            HC.Hierarchical_clustering(self.Dataset)


    #Classification
    def logreg(self,event=None):
        if len(self.Dataset)==0:
            tkMessageBox.showinfo("Error","Dataset matrix is empty please import dataset")

        else:
            LR.Logistic_Regrassion(self.Dataset)

    def dt_c(self,event=None):
        if len(self.Dataset)==0:
            tkMessageBox.showinfo("Error","Dataset matrix is empty please import dataset")

        else:
            DT.Decision_trees(self.Dataset,'c')

    def rf_c(self,event=None):
        if len(self.Dataset)==0:
            tkMessageBox.showinfo("Error","Dataset matrix is empty please import dataset")

        else:
            RF.Random_Forest(self.Dataset,'c')

    def svc(self,event=None):
         if len(self.Dataset)==0:
            tkMessageBox.showinfo("Error","Dataset matrix is empty please import dataset")
         else:
             SVM.Support_Vectors(self.Dataset,'c')

    def knn(self,event=None):
         if len(self.Dataset)==0:
            tkMessageBox.showinfo("Error","Dataset matrix is empty please import dataset")
         else:
             KNN.K_Nearest_Neighbor(self.Dataset)

    def nb(self,event=None):
         if len(self.Dataset)==0:
            tkMessageBox.showinfo("Error","Dataset matrix is empty please import dataset")
         else:
             NBY.Naive_Bayes(self.Dataset)

    def repbug(self):
        brep.Bug_Report() 

    def abt(self):
        about.About()

DataDoc()