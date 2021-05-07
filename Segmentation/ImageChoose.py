# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk
from os import listdir, getcwd
from os.path import isfile, join, basename, dirname
from PIL import Image, ImageTk

# Constant variable definition
WINDOW_HEIGHT           = 800           # The height of the main window
WINDOW_WIDTH            = 600           # The width of the main window
RESIZED_IMG_SIZE_WIDTH  = 500           # Resized image width
RESIZED_IMG_SIZE_HEIGHT = 500           # Resized image height
ACCEPTED_EXTENSIONS     = ('jpg', 'jpeg', 'tif', 'tiff', 'png')     # Accepted file extensions

# Global
results = []

class ImageSelect(Toplevel):
    """
    Class for object of root main app type of tkinter app
    """
    
    def __init__(self, path, currWantedFiles):
        """
        Initialization function for main root window
        
        Parameters:
            self - current object
            
        Return:
            None
        """
        
        super(ImageSelect, self).__init__()
        
        # Global results list
        global results
        
        # Set results files defaultly to recived list
        results = currWantedFiles
        
        # list of wanted files and unwanted files
        self.lstWantedFiles = currWantedFiles
        self.lstUnwantedFiles = []
        
        # Disable resize of the window
        self.resizable(False, False)
        
        # Set title for the window
        self.title("Image Select")
        self.minsize(WINDOW_HEIGHT, WINDOW_WIDTH)
        
        self.filesFrame = Frame(self)
        self.filesFrame.grid(row = 0, column = 0)
        
        # List of wanted files
        # Creating Listbox of files
        self.lbWantedFiles = Listbox(self.filesFrame, height=int(WINDOW_HEIGHT / 20))
        
        # Creating the scroll side bar in order to accept 
        # scrolling if lot files exists
        self.lbWantedFilesSbar = Scrollbar(self.filesFrame)
        
        # Attaching Listbox to Scrollbar Since we need to have
        # a vertical scroll we use yscrollcommand
        self.lbWantedFiles.config(yscrollcommand=self.lbWantedFilesSbar.set)
        
        # setting scrollbar command parameter  
        # to listbox.yview method its yview because 
        # we need to have a vertical view 
        self.lbWantedFilesSbar.config(command=self.lbWantedFiles.yview)
        
        # Place the listbox at the left most side of the window and then
        # Place the sidebar
        self.lbWantedFiles.grid(column = 0, row = 0, sticky='nsew')
        self.lbWantedFilesSbar.grid(column = 1, row = 0, sticky='nsew')
        
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
        
        # List of files unwanted files
        # Creating Listbox of files
        self.lbUnwantedFiles = Listbox(self.filesFrame, height=int(WINDOW_HEIGHT / 20))
        
        # Creating the scroll side bar in order to accept 
        # scrolling if lot files exists
        self.lbUnwantedFilesSbar = Scrollbar(self.filesFrame)
        
        # Attaching Listbox to Scrollbar Since we need to have
        # a vertical scroll we use yscrollcommand
        self.lbUnwantedFiles.config(yscrollcommand=self.lbUnwantedFilesSbar.set)
        
        # setting scrollbar command parameter  
        # to listbox.yview method its yview because 
        # we need to have a vertical view 
        self.lbUnwantedFilesSbar.config(command=self.lbUnwantedFiles.yview)
        
        # Place the listbox at the left most side of the window and then
        # Place the sidebar
        self.lbUnwantedFiles.grid(column = 3, row = 0, sticky='nsew')
        self.lbUnwantedFilesSbar.grid(column = 4, row = 0, sticky='nsew')
        
        # Load images in path
        self.loadImagesInPath(path)
        
        # -------------
        
        # Bind double click on image to show preview
        self.lbWantedFiles.bind('<Double-1>', lambda event: self.imagePreview(event, self.lbWantedFiles, path))
        self.lbUnwantedFiles.bind('<Double-1>', lambda event: self.imagePreview(event, self.lbUnwantedFiles, path))
        
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
        
        # Open all the images in the directory
        for image in lstOnlyFilesInDir:    
            # Check to which list import the file
            if (image in self.lstWantedFiles):
                self.lbWantedFiles.insert(END, image)
                self.lstWantedFiles.append(image)
            else:
                self.lbUnwantedFiles.insert(END, image)
                self.lstUnwantedFiles.append(image)
                
    
    def removeFiles(self):
        """
        The function removes selected files from list
        
        Parameters:
            self - the object
        
        Return:
            None
        """
        
        try:
            # Get the name of the current selected file
            currFile = self.lbWantedFiles.get(self.lbWantedFiles.curselection())
            
            # Delete the file from the left list - wanted files
            self.lbWantedFiles.delete(self.lbWantedFiles.curselection())
            
            # Add the file to the right list - deleted files
            self.lbUnwantedFiles.insert(END,currFile)
        except TclError as te:
            messagebox.showerror(title="Error", message="File was not selected!")
        
    def addFiles(self):
        """
        The function reopen images that was removed into the list.
        
        Parameters:
            self - the object
        
        Return:
            None
        """
        
        try:
            # Get the name of the current selected file
            currFile = self.lbUnwantedFiles.get(self.lbUnwantedFiles.curselection())
            
            # Delete the file from the right list - deleted files
            self.lbUnwantedFiles.delete(self.lbUnwantedFiles.curselection())
            
            # Add the file to the left list - wanted files
            self.lbWantedFiles.insert(END,currFile)
        except TclError as te:
            messagebox.showerror(title="Error", message="File was not selected!")
            
    def saveOptions(self):
        """
        The function saves the selected files and returns to main screen
        
        Parameters:
            self - the object
        
        Return:
            None
        """
        
        # Global results list
        global results
        
        # Save the wanted items into results list
        results = list(self.lbWantedFiles.get(0, END))
        
        # Close the menu
        self.destroy()
        
    def imagePreview(self, event, currListBox, path):
        """
        The function shows image preview for the selected image
        
        Parameters:
            self        - the object
            event       - event of mouse clicked
            currListBox - current list of files
            path        - path of the folder of files
        
        Return:
            None
        """
        
        # Get index of current slection in the lisbox
        cs = currListBox.curselection() 
        
        # Get the list of all items in the lisbox
        all_items = currListBox.get(0, 'end')
        
        # Check if files exists in the listbox of files
        if (len(all_items) == 0):
            # Prints error message - no file selected
            messagebox.showerror(title="Error", message="No file was selected!")
        else:
            # Save the current selected line in attribute
            currSelectedFile = currListBox.get(cs[0])
            
            # Create canvas for image
            self.imgCanvas = Canvas(self, width = RESIZED_IMG_SIZE_WIDTH, height = RESIZED_IMG_SIZE_HEIGHT)
            
            # Place the image canvas in the correct location in the window
            self.imgCanvas.grid(column = 5, row = 0, padx=120, sticky='n', columnspan=100, pady = 50)
            
            self.img = Image.open(path + "/" + currSelectedFile)
            resized = self.img.resize((RESIZED_IMG_SIZE_WIDTH, RESIZED_IMG_SIZE_HEIGHT), Image.ANTIALIAS)
            
            # Prepare the image for preview
            self.imgOnCanvas = ImageTk.PhotoImage(resized)
            
            # put image on canvas pic's upper left corner (NW) on the canvas
            self.imgCanvas.create_image((0,0), image=self.imgOnCanvas, anchor=NW)
