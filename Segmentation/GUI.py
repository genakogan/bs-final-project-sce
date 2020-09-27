# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 17:29:23 2020

@author: Aviel-PC
"""

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
from os import listdir
from os.path import isfile, join
from tkinter import Menu
import Segmentation as seg

class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("Python Tkinter Dialog Widget")
        self.minsize(640, 400)

        #self.labelFrame = ttk.LabelFrame(self, text = "Open File")
        #self.labelFrame.grid(column = 0, row = 1, padx = 20, pady = 20)
        #self.labelFrame.pack()
        
        self.upperMenu()
        self.imageSelectPanel()
        
        # Disable resize of the window
        self.resizable(False, False)
        
    def upperMenu(self):
        # Create the upper menu
        self.menu = Menu(self)
        
        # Create file button for the upper menu
        fileMenu = Menu(self.menu, tearoff=False)
        
        # Add button for choosing directory of files
        fileMenu.add_command(label='Open Directory', command = self.fileDialog)
        
        # Add separator for the exit button
        fileMenu.add_separator()
        
        # Add exit button to File menu
        fileMenu.add_command(label='Exit', command = self.programExit)
        
        # Add the file menu to the upper menu
        self.menu.add_cascade(label='File', menu=fileMenu)
        self.config(menu=self.menu)
    
    def programExit(self):
        self.destroy()
        
    def imageSelectPanel(self):
        # Creating Listbox of files
        self.lbFiles = Listbox(self, height=40)
        
        # Creating the scroll side bar in order to accept 
        # scrolling if lot files exists
        self.lbFilesSbar = Scrollbar(self)
        
        # Attaching Listbox to Scrollbar Since we need to have
        # a vertical scroll we use yscrollcommand
        self.lbFiles.config(yscrollcommand=self.lbFilesSbar.set)
        
        # setting scrollbar command parameter  
        # to listbox.yview method its yview because 
        # we need to have a vertical view 
        self.lbFilesSbar.config(command=self.lbFiles.yview)
        
        # Place the listbox at the left most side of the window and then
        # Place the sidebar
        self.lbFiles.grid(column = 0, row = 0, sticky='nsew')
        self.lbFilesSbar.grid(column = 1, row = 0, sticky='nsew')
           
        # Binding double click with left mouse 
        # button with go function 
        self.lbFiles.bind('<Double-1>', self.openImage)
        
    def openImage(self,event): 
        cs = self.lbFiles.curselection() 
        all_items = self.lbFiles.get(0, 'end')
        currentFile = all_items[cs[0]]
        
        try:
            # Create frame for image
            self.frameImage = Frame(self)
            self.frameImage.grid(column = 2, row = 0, sticky='nsew')
            
             # Create frame for sliders
            self.frameSliders = Frame(self)
            self.frameSliders.grid(column = 2, row = 1, sticky='nsew')
            
            #img = Image.open(self.path + "/"+ currentFile)
            # Perform first segmentation preview
            img = seg.imageConfigSegment(currentFile)()
            img = img.resize((400, 400), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(img)
            self.imgPreview = Label(self.frameImage, image=photo)
            self.imgPreview.image = photo 
            self.imgPreview.grid(column = 0, row = 0, padx=120, sticky='n', columnspan=100)
            
            # Add sliders for segmentation options:
            self.thresholdLbl = Label(self.frameImage, text="Threshold:").grid(row=1,padx=20, sticky=W)
            self.threshold = Scale(self.frameImage, from_=0, to=1000, orient=HORIZONTAL)
            self.threshold.set(1)
            self.threshold.grid(row = 1, column = 1, sticky='w')
            
            # Add sliders for segmentation options:
            self.thresholdLbl1 = Label(self.frameImage, text="Min Size:").grid(row=2,padx=20, sticky=W)
            self.threshold1 = Scale(self.frameImage, from_=0, to=1000, orient=HORIZONTAL)
            self.threshold1.set(2)
            self.threshold1.grid(row = 2, column = 1, sticky='w')
            
            # Add sliders for segmentation options:
            self.thresholdLbl2 = Label(self.frameImage, text="Area Treshold:").grid(row=3, padx=20, sticky=W)
            self.threshold2 = Scale(self.frameImage, from_=0, to=1000, orient=HORIZONTAL)
            self.threshold2.set(3)
            self.threshold2.grid(row = 3, column = 1, sticky='w')
            
            # Add button for segmentation Preview
            self.btnSegmentPreview = ttk.Button(self.frameImage, text="Preview", command='')
            self.btnSegmentPreview.config(width=20)
            self.btnSegmentPreview.grid(column = 20, row = 4, sticky='w')
            
            #self.btnSegmentPreview.lift()
            
        except IOError:
            print("Not an image!")


    def loadImagesInPath(self):
    
        # Load all files in directory to array - without directories
        onlyfiles = [f for f in listdir(self.path) if isfile(join(self.path, f))]
        
        nImgIndex = 0
        
        # Open all the images in the directory
        for image in onlyfiles:    
            self.lbFiles.insert(nImgIndex,image)
            nImgIndex = nImgIndex + 1
            
    
    def fileDialog(self):

        # Browse for directory of images
        self.path = filedialog.askdirectory()
        
        # Check if path was selected open all images in path
        if self.path != '':
            self.lbFiles.delete(0,'end')
            self.loadImagesInPath()

root = Root()
root.mainloop()