__author__ = 'Tapsas Apostolos', 'Valiakos Apostolos'
from tkinter import *
from tkinter import Tk
from General import tkHyperlinkManager
import webbrowser

class About:
    def __init__(self):
        self.root = Tk()
        self.root.title('About Datadoc')
        self.root.geometry('600x300')
        self.text = Text(self.root)
        hyperlink = tkHyperlinkManager.HyperlinkManager(self.text)
        self.text.insert(INSERT, "Mechatronic Labs's",hyperlink.add(self.about_us))
        self.text.insert(INSERT, " Datadoc software platform offers advanced\nstatistical analysis a vast library of machine-learning algorithms,\nimage procesing")
        self.text.insert(INSERT, "integration with bigdata and seamless\ndeployment into applications. Its ease of use\nflexibility andscalability make Datadoc accessible,")
        self.text.insert(INSERT, "to users\nwith all skill levels and outfitsprojects of all sizes\nand complexity to help you and your organization find new opportunities,\nimprove efficiency and minimize risk.")
        self.text.configure(state='disabled')
        self.text.pack()
        self.root.mainloop()

    def about_us(self):
        webbrowser.open('https://www.linkedin.com/groups/14038040/')
        

