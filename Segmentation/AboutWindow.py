# import tkinter module 
from tkinter import * 
from tkinter.ttk import *
from tkinter import LabelFrame, Button, Label

# Constant variable definition
IMAGE_PATH = "images\SCE.png"
WINDOWGEOMETRY = "+450+250"
class AboutW(Toplevel):


    def __init__(self):
        super(AboutW, self).__init__()
        self.geometry(WINDOWGEOMETRY)
        
        # creating main tkinter window/toplevel    
        # first level
        self.leftFirstLevel = LabelFrame(self, relief='raised')
        self.rightFirstLevel = LabelFrame(self, relief='raised')
        self.leftFirstLevel.grid(row = 0, column = 0,columnspan = 1, sticky = W, padx = 10) 
        self.rightFirstLevel.grid(row = 0, column = 1,rowspan = 3, sticky = W, padx = 10)
        img = PhotoImage(file = IMAGE_PATH) 
        img1 = img.subsample(1, 1)
        self.title=Label(self.leftFirstLevel, text = "Segmentation of computer tomography \n(CT) image sequence for lower back vertebrae.\n © 2020 - 2021",font=("Aharoni", 25)).grid(row = 0, column = 0)
        self.sceImage=Label(self.rightFirstLevel, image = img1)#.grid(row = 1, column = 1, columnspan = 2, rowspan = 2, ipadx = 5, ipady = 5) 
        self.sceImage.grid(row = 1, column = 1,columnspan = 1, rowspan = 1, ipadx = 4, ipady = 4)
        self.sceImage.photo_ref =img1
        
        # second level
        self.leftThirdLevel = LabelFrame(self, relief='flat')
        self.leftThirdLevel.grid(row = 1, column = 0, sticky = W, padx = 10) 
        
        # left side
        self.leftOfleftThirdLevel=LabelFrame(self.leftThirdLevel,relief='raised')
        self.leftOfleftThirdLevel.grid(row = 0, column = 0)
        self.developers=Label(self.leftOfleftThirdLevel, justify="left",text = "Created by: ",font=("Aharoni", 15)).grid(row = 0, column = 0)
        # midle side
        self.middleOfleftThirdLevel=LabelFrame(self.leftThirdLevel,relief='raised')
        self.middleOfleftThirdLevel.grid(row = 0, column = 1,padx = 50)
        self.nameOfDevelopers=Label(self.middleOfleftThirdLevel, text = "Aviel Roistacher - avirois@gmail.com",font=("Aharoni", 14)).grid(row = 0, column = 0)
        self.nameOfDevelopers=Label(self.middleOfleftThirdLevel, text = "Genady Kogan - rgkogan@gmail.com",font=("Aharoni", 14)).grid(row = 1, column = 0)
        # right side
        self.rightOfleftThirdLevel=LabelFrame(self.leftThirdLevel,relief='raised')
        self.rightOfleftThirdLevel.grid(row = 0, column = 2,padx = 10)
        
        # third level
        self.leftSecondLevel = LabelFrame(self, relief='flat')
        self.leftSecondLevel.grid(row = 2, column = 0, sticky = W,padx = 10) 
        
        # left side
        self.leftOfleftSecondLevel= LabelFrame(self.leftSecondLevel, relief='raised')
        self.leftOfleftSecondLevel.grid(row = 0, column = 0, sticky = W, pady = 2) 
        self.academicAdviser=Label(self.leftOfleftSecondLevel, justify="left",text = "Academic Adviser: ",font=("Aharoni", 15)).grid(row = 0, column = 0)
        
        # right side
        self.rightOfleftSecondLevel= LabelFrame(self.leftSecondLevel, relief='raised')
        self.rightOfleftSecondLevel.grid(row = 0, column = 1, sticky = W, padx = 50) 
        self.nameOfAcademicAdviser=Label(self.rightOfleftSecondLevel, text = "Dr. Irina Rabaev",font=("Aharoni", 14)).grid(row = 0, column = 0)
        
        # fourth level
        self.rightFourthLevel = LabelFrame(self, relief='flat')
        self.rightFourthLevel.grid(row = 4, column = 1, sticky = W, padx = 10)
        self.closelButton = Button (self.rightFourthLevel, text="Close", width = 46, fg='red',command=self.destroy)
        self.closelButton.grid(row = 0, column = 1,pady = 5)
        
        
        
        
    
        
        
        
        
        
        
        