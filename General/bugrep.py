__author__ = 'Tapsas Apostolos', 'Valiakos Apostolos'
from tkinter import *
from tkinter import Tk
from General import tkHyperlinkManager
import webbrowser

class Bug_Report:
    def __init__(self):
        self.root = Tk()
        self.root.title('Bug Report')
        self.root.geometry('600x300')
        self.text = Text(self.root)
        hyperlink = tkHyperlinkManager.HyperlinkManager(self.text)
        self.text.insert(INSERT, "Bug Detected?\nIn this case you can mail us ")
        self.text.insert(END, "Here", hyperlink.add(self.email))
        self.text.insert(END, " or open an issue at ")
        self.text.insert(END, "Github", hyperlink.add(self.open_issue))
        self.text.insert(END, ".")
        self.text.configure(state='disabled')
        self.text.pack()
        self.root.mainloop()
        
    def email(self):
        #webbrowser.open('https://mailto:mechatroniclabs@gmail.com')
        webbrowser.open("mailto:?to=mechatroniclabs@gmail.com&subject=BugReport", new=1)

    def open_issue(self):
        webbrowser.open('https://github.com/Mechatronic-Labs/DataDoc/issues')
        

