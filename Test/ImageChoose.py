# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk
from os import listdir, getcwd
from os.path import isfile, join, basename, dirname

# Constant variable definition
WINDOW_HEIGHT           = 800           # The height of the main window
WINDOW_WIDTH            = 600           # The width of the main window
ACCEPTED_EXTENSIONS     = ('jpg', 'jpeg', 'tif', 'tiff', 'png')     # Accepted file extensions

# Global
results = []

class ImageSelect(Tk):
    """
    Class for object of root main app type of tkinter app
    """
    
    def __init__(self, path):
        """
        Initialization function for main root window
        
        Parameters:
            self - current object
            
        Return:
            None
        """
        
        super(ImageSelect, self).__init__()
        
        # list of wanted files and unwanted files
        self.lstWantedFiles = []
        self.lstUnwantedFiles = []
        
        # Set title for the window
        self.title("Image Select")
        self.minsize(WINDOW_HEIGHT, WINDOW_WIDTH)
        
        self.filesFrame = Frame(self)
        self.filesFrame.grid(row = 0, column = 0)
        
        # List of files
        # Creating Listbox of files
        self.lbFiles1 = Listbox(self.filesFrame, height=int(WINDOW_HEIGHT / 20))
        
        # Creating the scroll side bar in order to accept 
        # scrolling if lot files exists
        self.lbFilesSbar1 = Scrollbar(self.filesFrame)
        
        # Attaching Listbox to Scrollbar Since we need to have
        # a vertical scroll we use yscrollcommand
        self.lbFiles1.config(yscrollcommand=self.lbFilesSbar1.set)
        
        # setting scrollbar command parameter  
        # to listbox.yview method its yview because 
        # we need to have a vertical view 
        self.lbFilesSbar1.config(command=self.lbFiles1.yview)
        
        # Place the listbox at the left most side of the window and then
        # Place the sidebar
        self.lbFiles1.grid(column = 0, row = 0, sticky='nsew')
        self.lbFilesSbar1.grid(column = 1, row = 0, sticky='nsew')
        
        self.lbFiles2 = Listbox(self.filesFrame, height=int(WINDOW_HEIGHT / 20))
        
        #-------------------
        
        # Create frame for image
        self.frameButtons = Frame(self.filesFrame)
        self.frameButtons.grid(column = 2, row = 0, sticky='nsew')
        
        # Add button for move files
        self.btnMoveRight = ttk.Button(self.frameButtons, text=">>", command=self.removeFiles)
        self.btnMoveRight.config(width=20)
        self.btnMoveRight.grid(column = 0, row = 0, pady = (int(WINDOW_HEIGHT / 4), 10))
        
        # Add button for move files
        self.btnSave = ttk.Button(self.frameButtons, text="Save", command=self.saveOptions)
        self.btnSave.config(width=20)
        self.btnSave.grid(column = 0, row = 1, pady = 10)
        
        # Add button for move files
        self.btnMoveLeft = ttk.Button(self.frameButtons, text="<<", command=self.addFiles)
        self.btnMoveLeft.config(width=20)
        self.btnMoveLeft.grid(column = 0, row = 2, pady = 10)
        
        
        #-------------------
        
        # Creating the scroll side bar in order to accept 
        # scrolling if lot files exists
        self.lbFilesSbar2 = Scrollbar(self.filesFrame)
        
        # Attaching Listbox to Scrollbar Since we need to have
        # a vertical scroll we use yscrollcommand
        self.lbFiles2.config(yscrollcommand=self.lbFilesSbar2.set)
        
        # setting scrollbar command parameter  
        # to listbox.yview method its yview because 
        # we need to have a vertical view 
        self.lbFilesSbar2.config(command=self.lbFiles2.yview)
        
        # Place the listbox at the left most side of the window and then
        # Place the sidebar
        self.lbFiles2.grid(column = 3, row = 0, sticky='nsew')
        self.lbFilesSbar2.grid(column = 4, row = 0, sticky='nsew')
        
        # Load images in path
        self.loadImagesInPath(path)
        
        # -------------

        
    def loadImagesInPath(self, path):
        """
        The function loads all the images in the selected path.
        
        Parameters:
            self - the object
        
        Return:
            None
        """
        
        # Load all files in directory to array - without directories
        lstOnlyFilesInDir = [f for f in listdir(path) if isfile(join(path, f)) and f.lower().endswith(ACCEPTED_EXTENSIONS)]
        
        # Define image index
        nImgIndex = 0
        
        # Open all the images in the directory
        for image in lstOnlyFilesInDir:    
            self.lbFiles1.insert(nImgIndex,image)
            self.lstWantedFiles.append(image)
    
    def removeFiles(self):
        try:
            # Get the name of the current selected file
            currFile = self.lbFiles1.get(self.lbFiles1.curselection())
            
            # Delete the file from the left list - wanted files
            self.lbFiles1.delete(self.lbFiles1.curselection())
            
            # Add the file to the right list - deleted files
            self.lbFiles2.insert(END,currFile)
        except TclError as te:
            messagebox.showerror(title="Error", message="File was not selected!")
        
    def addFiles(self):
        try:
            # Get the name of the current selected file
            currFile = self.lbFiles2.get(self.lbFiles2.curselection())
            
            # Delete the file from the right list - deleted files
            self.lbFiles2.delete(self.lbFiles2.curselection())
            
            # Add the file to the left list - wanted files
            self.lbFiles1.insert(END,currFile)
        except TclError as te:
            messagebox.showerror(title="Error", message="File was not selected!")
            
    def saveOptions(self):
        # Global results list
        global results
        
        # Save the wanted items into results list
        results = list(self.lbFiles1.get(0, END))
        
        # Close the menu
        self.destroy()
            
# Run the main GUI
root = ImageSelect("C:\\Users\\Aviel-PC\\לימודים\\Project\\CT images\\spineimage\\SpineCTAnonExample\\SpineCTAnonExample\\test5")
root.mainloop()

print(results)
