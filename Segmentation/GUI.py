# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 17:29:23 2020

@author: Aviel-PC
"""

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
from os import listdir
from os.path import isfile, join
from tkinter import Menu
import Segmentation as seg
import Paint as pnt

# Constant variable definition
DEFAULT_THRESHOLD = 0.6
DEFAULT_MIN_SIZE = 1000
DEFAULT_AREA_SIZE = 1000

# Code segment

class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("Python Tkinter Dialog Widget")
        self.minsize(800, 600)

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
        self.currentFile = all_items[cs[0]]
        
        try:
            # Create frame for image
            self.frameImage = Frame(self)
            self.frameImage.grid(column = 2, row = 0, sticky='nsew')
            
             # Create frame for sliders
            self.frameSliders = Frame(self)
            self.frameSliders.grid(column = 2, row = 1, sticky='nsew')
            
            # Create canvas for image
            self.imgCanvas = Canvas(self.frameImage, width = 500, height = 500)
            
            # Configure scroll area for image
            self.imgCanvas.configure(scrollregion=(0,0,1000,1000))
            self.imgCanvas.grid(column = 0, row = 0, padx=120, sticky='n', columnspan=100)

            
            # Prepare the image with first segmentation
            img = seg.imageConfigSegment(self.currentFile)()
            img = img.resize((400, 400), Image.ANTIALIAS)
            
            # Put photo as attribute in order to prevent garbage collection
            self.photo = ImageTk.PhotoImage(img)
            
            # put image on canvas pic's upper left corner (NW) on the canvas
            self.imgCanvas.create_image((0,0), image=self.photo, anchor=NW)
            
            # Add sliders for segmentation options:
            self.thresholdLbl = Label(self.frameImage, text="Threshold:").grid(row=1,padx=20, sticky=W)
            self.threshold = Scale(self.frameImage, from_=0, to=1, resolution = 0.005, orient=HORIZONTAL)
            self.threshold.set(DEFAULT_THRESHOLD)
            self.threshold.grid(row = 1, column = 1, sticky='w')
            
            # Add sliders for min size threshold:
            self.minSizeLbl = Label(self.frameImage, text="Min Size:").grid(row=2,padx=20, sticky=W)
            self.minSizeVal = Scale(self.frameImage, from_=0, to=10000, orient=HORIZONTAL)
            self.minSizeVal.set(DEFAULT_MIN_SIZE)
            self.minSizeVal.grid(row = 2, column = 1, sticky='w')
            
            # Add sliders for area threshold:
            self.areaValLbl = Label(self.frameImage, text="Area Treshold:").grid(row=3, padx=20, sticky=W)
            self.areaVal = Scale(self.frameImage, from_=0, to=10000, orient=HORIZONTAL)
            self.areaVal.set(DEFAULT_AREA_SIZE)
            self.areaVal.grid(row = 3, column = 1, sticky='w')
            
            # Add button for segmentation Preview
            self.btnSegmentPreview = ttk.Button(self.frameImage, text="Preview", command=self.previewSegmentation)
            self.btnSegmentPreview.config(width=20)
            self.btnSegmentPreview.grid(column = 1, row = 4, sticky='w')
            
            # Add button for clear segmentation values
            self.btnSegmentPreview = ttk.Button(self.frameImage, text="Reset Thresholds", command=self.resetThresholds)
            self.btnSegmentPreview.config(width=20)
            self.btnSegmentPreview.grid(column = 2, row = 4, sticky='w')
            
            # Add button for image edit
            self.btnSegmentPreview = ttk.Button(self.frameImage, text="Edit", command=self.editImage)
            self.btnSegmentPreview.config(width=20)
            self.btnSegmentPreview.grid(column = 3, row = 4, sticky='w')
            
            # Scroll image using mouse wheel
            self.imgCanvas.bind("<MouseWheel>",self.zoomer)
            
            # Move using mouse click
            self.imgCanvas.bind("<ButtonPress-1>", self.move_start)
            self.imgCanvas.bind("<B1-Motion>", self.move_move)
            
            #self.btnSegmentPreview.lift()
            
        except IOError:
            #print("Not an image!")
            print(IOError.message)
            
    def zoomer(self, event):
        if (event.delta > 0):
            self.imgCanvas.scale("all", event.x, event.y, 1.1, 1.1)
        elif (event.delta < 0):
            self.imgCanvas.scale("all", event.x, event.y, 0.5, 0.5)
        self.imgCanvas.configure(scrollregion = self.imgCanvas.bbox("all"))

    # mouse move
    def move_start(self, event):
        self.imgCanvas.scan_mark(event.x, event.y)
        
    def move_move(self, event):
        self.imgCanvas.scan_dragto(event.x, event.y, gain=1)
        
    def previewSegmentation(self):
        # Get parameters for the image
        currentFile = self.currentFile
        threshold = self.threshold.get()
        minSizeVal = self.minSizeVal.get()
        areaVal = self.areaVal.get()
        
        try:
            # Perform the segmentation after changing values
            img = seg.imageConfigSegment(currentFile, threshold, minSizeVal, areaVal)()
            img = img.resize((400, 400), Image.ANTIALIAS)
            self.photo = ImageTk.PhotoImage(img)
            #self.imgPreview = Label(self.frameImage, image=photo)
            #self.imgPreview.image = photo 
            #self.imgPreview.grid(column = 0, row = 0, padx=120, sticky='n', columnspan=100)
            
            # put image on canvas pic's upper left corner (NW) on the canvas
            self.imgCanvas.create_image((0,0), image=self.photo, anchor=NW)
        except ValueError:
            messagebox.showerror(title="Error", message="Wrong threshold values selected!")

        
    def resetThresholds(self):
        # Reset values for thresholds
        self.threshold.set(DEFAULT_THRESHOLD)
        self.minSizeVal.set(DEFAULT_MIN_SIZE)
        self.areaVal.set(DEFAULT_AREA_SIZE)
        
    def loadImagesInPath(self):
    
        # Load all files in directory to array - without directories
        onlyfiles = [f for f in listdir(self.path) if isfile(join(self.path, f))]
        
        nImgIndex = 0
        
        # Open all the images in the directory
        for image in onlyfiles:    
            self.lbFiles.insert(nImgIndex,image)
            nImgIndex = nImgIndex + 1
    
    # Function for button edit image
    def editImage(self):
        window = pnt.Window(self.currentFile)
        window.show() 
        mainloop()
        
    def fileDialog(self):

        # Browse for directory of images
        self.path = filedialog.askdirectory()
        
        # Check if path was selected open all images in path
        if self.path != '':
            self.lbFiles.delete(0,'end')
            self.loadImagesInPath()

root = Root()
root.mainloop()