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

class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("Python Tkinter Dialog Widget")
        self.minsize(640, 400)

        self.labelFrame = ttk.LabelFrame(self, text = "Open File")
        self.labelFrame.grid(column = 0, row = 1, padx = 20, pady = 20)

        self.button()


    def button(self):
        self.button = ttk.Button(self.labelFrame, text = "Browse A File",command = self.fileDialog)
        self.button.grid(column = 1, row = 1)

    
    def on_image_click(event=None):
        # `command=` calls function without argument
        # `bind` calls function with one argument
        print("image clicked")

    def fileDialog(self):
  
        # Browse for directory of images
        self.path = filedialog.askdirectory()
        
        # Print label with directory location under the button
        self.label = ttk.Label(self.labelFrame, text = "")
        self.label.grid(column = 1, row = 2)
        self.label.configure(text = self.path)
        
        # Load all files in directory to array - without directories
        onlyfiles = [f for f in listdir(self.path) if isfile(join(self.path, f))]
        
        # set location of the image preview
        row = 4
        col = 0
        
        # Open all the images in the directory
        for image in onlyfiles:    
            try:
                img = Image.open(self.path + "/"+ image)
                img = img.resize((100, 100), Image.ANTIALIAS)
                photo = ImageTk.PhotoImage(img)
                self.label2 = Label(image=photo)
                self.label2.image = photo 
                self.label2.grid(column=col, row=row)
                self.label2.configure(text = image)
                self.label3 = Label()
                self.label3.grid(column = col + 1, row = row)
                self.label3.configure(text = image)
                row = row + 1
            except IOError:
                print("Not an image!")

root = Root()
root.mainloop()