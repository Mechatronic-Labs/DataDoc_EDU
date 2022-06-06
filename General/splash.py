__author__ = 'Tapsas Apostolos', 'Valiakos Apostolos'
from tkinter import *
from PIL import Image

class SplashScreen:
    def __init__(self, parent):
        self.parent = parent
 
        self.aturSplash()
        self.aturWindow()
 
    def aturSplash(self):
        # import image menggunakan Pillow
        self.gambar = Image.open("icons/intro_image.png")
        self.imgSplash = PhotoImage(file = "icons/intro_image.png")
 
    def aturWindow(self):
        # ambil ukuran dari file image
        lebar, tinggi = self.gambar.size
 
        setengahLebar = (self.parent.winfo_screenwidth()-lebar)//2
        setengahTinggi = (self.parent.winfo_screenheight()-tinggi)//2
 
        # atur posisi window di tengah-tengah layar
        self.parent.geometry("%ix%i+%i+%i" %(lebar, tinggi,
                                             setengahLebar,setengahTinggi))
 
        # atur Image via Komponen Label
        Label(self.parent, image=self.imgSplash).pack()
         

