# -*- coding: utf-8 -*-

try:
    from datetime import datetime
    from tkinter import *
    from tkinter import ttk
    from tkinter import filedialog
    from tkinter import messagebox
    from PIL import Image, ImageTk
    from os import listdir, getcwd
    from os.path import isfile, join, basename, dirname
    from tkinter import Menu
    import Segmentation as seg
    import Paint as pnt 
    import Notebook as no
    import AboutWindow as ab
    import ConvertDicom as cd
    import webbrowser
    import gc
    import time
except ImportError as impError:
    with open('./Logs/Imports.log', 'a') as import_log_file:
        import_log_file.write("Date - " + str(datetime.now().strftime("%d/%m/%Y %H:%M:%S")) + "\n" + str(impError) + "\n")
    sys.exit()  

# Constant variable definition
WINDOW_HEIGHT           = 800           # The height of the main window
WINDOW_WIDTH            = 600           # The width of the main window
DEFAULT_THRESHOLD       = 0.6           # Default threshold value
DEFAULT_MIN_SIZE        = 1000          # Default min size of object for segmentation
DEFAULT_AREA_SIZE       = 5000          # Default area threshold for segmentation
DEFAULT_MAX_SIZE        = 50000         # Default max size of object for segmentation
THRESHOLD_RESOLUTION    = 0.0005        # Increment resolution for threshold
ZOOM_IN_SCALE           = 1.1           # Zoom in scale size
ZOOM_OUT_SCALE          = 0.9           # Zoom out scale size
MIN_DISPLAY_SIZE_WIDTH  = 400           # Minimum size in pixel of displayed image of width
MIN_DISPLAY_SIZE_HEIGHT = 400           # Minimum size in pixel of displayed image of height
SEGMENT_FUNC_INDX       = 0             # Index for segmentation function in the list inside dictionary of files
THRESHOLD_INDX          = 1             # Index for threshold in the list inside dictionary of files
MIN_SIZE_INDX           = 2             # Index for min size in the list inside dictionary of files
AREA_SIZE_INDX          = 3             # Index for area size in the list inside dictionary of files
MAX_SIZE_INDX           = 4             # Index for max size in the list inside dictionary of files
PROGRESS_BAR_LENGTH     = 300           # Length of progressbar window
PROGRESS_BAR_WIDTH      = 50            # Width of progressbar window
PROGRESS_BAR_PERCENTAGE = 100.0         # Percent of progress bar set to 100
PROGRESS_BAR_INIT       = 0             # value for reseting progress bar to progress Zero
PROGRAM_PATH            = getcwd()      # Get path of the py files
DOCUMENTATION_FILE      = PROGRAM_PATH + '/Documentation/GKAR.pdf'  # Get documentation file path
ACCEPTED_EXTENSIONS     = ('jpg', 'jpeg', 'tif', 'tiff', 'png')     # Accepted file extensions
TESTED_IMGS_COLOR       = "SpringGreen3" # The color for images that segmentation already tested by user

# Code segment

class Root(Tk):
    
    """
    Class for object of root main app type of tkinter app
    """
    
    def __init__(self):
        """
        Initialization function for main root window
        
        Parameters:
            self - current object
            
        Return:
            None
        """
        
        super(Root, self).__init__()
        
        # Set title for the window
        self.title("Bone Segmentation")
        
        # Set size of the window
        self.minsize(WINDOW_HEIGHT, WINDOW_WIDTH)
        
        # Create upper menu using the function
        self.upperMenu()
        
        # Create image select panel using the function
        self.imageSelectPanel()
        
        # Disable resize of the window
        self.resizable(False, False)   
       
    def upperMenu(self):
        """
        The function creates the upper menu in the main app
        
        Parameters:
            self - the object
        
        Return:
            None
        """
        
        # Create the upper menu
        self.menu = Menu(self)

        # ==================  File Menu
        
        # Create file button for the upper menu
        fileMenu = Menu(self.menu, tearoff=False)
        
        # Add the file menu to the upper menu
        self.menu.add_cascade(label='File', menu=fileMenu)
        self.config(menu=self.menu)
        
        # Add button for choosing directory of files
        fileMenu.add_command(label='Open Directory', command = self.fileDialog)
        
        # Add separator for the exit button
        fileMenu.add_separator()
        
        # Add button for perform segmentation on all images in list
        fileMenu.add_command(label='Perform segmentation', command = self.performSegmentation)
        
        # Add separator for the exit button
        fileMenu.add_separator()
        
        # Add exit button to File menu
        fileMenu.add_command(label='Exit', command = self.programExit, accelerator="Ctrl+Q")
        self.bind_all("<Control-q>", self.programExit)
        
        # ==================  Help Menu
        
        # Create help menu button for upper menu
        helpMenu = Menu(self.menu, tearoff=False)
        
        # Add the Help menu to the upper menu
        self.menu.add_cascade(label='Help', menu=helpMenu)
        self.config(menu=self.menu)
       
        helpMenu.add_command(label='Notebook', command = self.notebook)
        
        # Add separator for the Notebook button
        helpMenu.add_separator()
        
        
        helpMenu.add_command(label='About', command = self.about)
        
        # Add separator for the Documentation button
        helpMenu.add_separator()
         
        # Add Documentation button to Help menu
        helpMenu.add_command(label='Documentation', command = self.documentation)
        
    def programExit(self, event=None):
        """
        The function closes the program
        
        Parameters:
            self    - the object
            event   - event of button clicked if exists or None if empty
        
        Return:
            None
        """
        
        # Close the main program
        self.destroy()
    
    def imageSelectPanel(self):
        """
        The function creates the image selection panel
        
        Parameters:
            self - the object
        
        Return:
            None
        """
        
        # Creating Listbox of files
        self.lbFiles = Listbox(self, height=int(WINDOW_HEIGHT / 20))
        
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
       
    def openImage(self, event): 
        """
        The fucntion opens the image according to the selection in the listbox of images
        
        Parameters:
            self    - the object
            event   - mouse click image location
        
        Return:
            None
        """
        
        # Get index of current slection in the lisbox
        cs = self.lbFiles.curselection() 
        
        # Get the list of all items in the lisbox
        all_items = self.lbFiles.get(0, 'end')
        
        # Check if files exists in the listbox of files
        if (len(all_items) == 0):
            # Prints error message - no file selected
            messagebox.showerror(title="Error", message="No file was selected!")
        else:
            # Save the current selected line in attribute
            self.currentSelectedLine = cs[0]
            
            # Load the image by the current selected index
            self.loadImageByIndx(self.currentSelectedLine, all_items)
    
    def nextImage(self):
        """
        The function moves to the next image in the list of files if exists
        
        Parameters:
            self    - the object
        
        Return:
            None
        """
        
        # Get the list of all files in listbox
        all_items = self.lbFiles.get(0, 'end')
        
        # Check if exists next image
        if (self.currentSelectedLine + 1 != len(all_items)):
            # Move to the next image
            self.currentSelectedLine += 1
            
            # Clear current selected item
            self.lbFiles.selection_clear(0, 'end')
            
            # Select the next item
            self.lbFiles.select_set(self.currentSelectedLine)
            
            # Load the image by the current selected index
            self.loadImageByIndx(self.currentSelectedLine, all_items)
    
    def prevImage(self):
        """
        The function moves to the previous image in the list of files if exists
        
        Parameters:
            self    - the object
        
        Return:
            None
        """
        
        # Get the list of all files in listbox
        all_items = self.lbFiles.get(0, 'end')
        
        # Check if exists previous image
        if (self.currentSelectedLine - 1 >= 0):
            # Move to the next image
            self.currentSelectedLine -= 1
            
            # Clear current selected item
            self.lbFiles.selection_clear(0, 'end')
            
            # Select the prev item
            self.lbFiles.select_set(self.currentSelectedLine)
            
            # Load the image by the current selected index
            self.loadImageByIndx(self.currentSelectedLine, all_items)
      
    def loadImageByIndx(self, zImgIndx, all_items):
        """
        The function opens the image and all parameters, and buttons according to the index
        
        Parameters:
            self        - the object
            zImgIndx    - the index of the current image in files list
            all_items   - the list of all items in the listbox of files 
        
        Return:
            None
        """
        
        # Set the current file with path
        self.currentFile = all_items[zImgIndx]
        
        try:
            # Mark the image as already selected
            self.lbFiles.itemconfig(zImgIndx, bg=TESTED_IMGS_COLOR)
            
            # Create frame for image
            self.frameImage = Frame(self)
            self.frameImage.grid(column = 2, row = 0, sticky='nsew')
            
            # Create canvas for image
            self.imgCanvas = Canvas(self.frameImage, width = 500, height = 500)
            
            # Place the image canvas in the correct location in the window
            self.imgCanvas.grid(column = 0, row = 0, padx=120, sticky='n', columnspan=100)
            
            # Prepare the image with first segmentation
            self.img = self.dictFilesSegment[self.currentFile][SEGMENT_FUNC_INDX]()
            self.img = self.img.resize((MIN_DISPLAY_SIZE_WIDTH, MIN_DISPLAY_SIZE_HEIGHT), Image.ANTIALIAS)
            
            # Put photo as attribute in order to prevent garbage collection
            self.photo = ImageTk.PhotoImage(self.img)
            
            # put image on canvas pic's upper left corner (NW) on the canvas
            self.imgCanvas.create_image((0,0), image=self.photo, anchor=NW)
            
            # Configure scroll area for image
            self.imgCanvas.configure(scrollregion = self.imgCanvas.bbox("all"))
            
            # Define variablies to hold data in silders and spinboxes
            varThreshold = DoubleVar(value = 0.)
            varMinSize = IntVar(value = 0)
            varMaxSize = DoubleVar(value = 0)
            varAreaThreshold = IntVar(value = 0)
            
            # Add sliders for segmentation options:
            self.thresholdLbl = Label(self.frameImage, text="Threshold:").grid(row=1,padx=20, sticky=W)
            self.threshold = Scale(self.frameImage, showvalue=0, from_=0, to=1, resolution = THRESHOLD_RESOLUTION, orient=HORIZONTAL, variable=varThreshold)
            self.threshold.set(self.dictFilesSegment[self.currentFile][THRESHOLD_INDX])
            self.threshold.grid(row = 1, column = 1, sticky='w')
            
            # Add textbox for threshold
            self.tbThreshold = Spinbox(self.frameImage, textvariable=varThreshold, wrap=True, width=10, from_=0, to=1, increment = THRESHOLD_RESOLUTION)
            self.tbThreshold.grid(row = 1, column = 2,rowspan=1, sticky='WE')
            
            # Add sliders for min size threshold:
            self.minSizeLbl = Label(self.frameImage, text="Min Size:").grid(row=2,padx=20, sticky=W)
            self.minSizeVal = Scale(self.frameImage, showvalue=0, from_=0, to=10000, orient=HORIZONTAL, variable=varMinSize)
            self.minSizeVal.set(self.dictFilesSegment[self.currentFile][MIN_SIZE_INDX])
            self.minSizeVal.grid(row = 2, column = 1, sticky='w')
            
            # Add textbox for min size
            self.tbMinSize = Spinbox(self.frameImage, textvariable=varMinSize, wrap=True, width=10, from_=0, to=10000)
            self.tbMinSize.grid(row = 2, column = 2,rowspan=1, sticky='WE')
            
            # Add sliders for max size threshold:
            self.maxSizeLbl = Label(self.frameImage, text="Max Size:").grid(row=3,padx=20, sticky=W)
            self.maxSizeVal = Scale(self.frameImage, showvalue=0, from_=0, to=100000, orient=HORIZONTAL, variable=varMaxSize)
            self.maxSizeVal.set(self.dictFilesSegment[self.currentFile][MAX_SIZE_INDX])
            self.maxSizeVal.grid(row = 3, column = 1, sticky='w')
            
            # Add textbox for max size
            self.tbMaxSize = Spinbox(self.frameImage, textvariable=varMaxSize, wrap=True, width=10, from_=0, to=100000)
            self.tbMaxSize.grid(row = 3, column = 2,rowspan=1, sticky='WE')
            
            # Add sliders for area threshold:
            self.areaValLbl = Label(self.frameImage, text="Area Treshold:").grid(row=4, padx=20, sticky=W)
            self.areaVal = Scale(self.frameImage, showvalue=0, from_=0, to=10000, orient=HORIZONTAL, variable=varAreaThreshold)
            self.areaVal.set(self.dictFilesSegment[self.currentFile][AREA_SIZE_INDX])
            self.areaVal.grid(row = 4, column = 1, sticky='w')
            
            # Add textbox for area threshold
            self.tbAreaThreshold = Spinbox(self.frameImage, textvariable=varAreaThreshold, wrap=True, width=10, from_=0, to=10000)
            self.tbAreaThreshold.grid(row = 4, column = 2,rowspan=1, sticky='WE')
            
            # Get number of rows in the image frame
            nFrameRows = self.frameImage.grid_size()[1]
            
            # Set the row for buttons
            nButtonsRow = nFrameRows
            
            # Add button for segmentation Preview
            self.btnSegmentPreview = ttk.Button(self.frameImage, text="Preview", command=self.previewSegmentation)
            self.btnSegmentPreview.config(width=20)
            self.btnSegmentPreview.grid(column = 1, row = nButtonsRow, sticky='sw')
            
            # Add button for clear segmentation values
            self.btnSegmentPreview = ttk.Button(self.frameImage, text="Reset Thresholds", command=self.resetThresholds)
            self.btnSegmentPreview.config(width=20)
            self.btnSegmentPreview.grid(column = 2, row = nButtonsRow, sticky='sw')
            
            # Add button for image segmentation save
            self.btnSegmentPreview = ttk.Button(self.frameImage, text="Save", command=self.singleImageSegmentation)
            self.btnSegmentPreview.config(width=20)
            self.btnSegmentPreview.grid(column = 3, row = nButtonsRow, sticky='sw')
            
            # Add button for image edit
            self.btnSegmentPreview = ttk.Button(self.frameImage, text="Edit", command=self.editImage)
            self.btnSegmentPreview.config(width=20)
            self.btnSegmentPreview.grid(column = 4, row = nButtonsRow, sticky='sw')
            
            # Add button for next image
            self.btnNextImage = ttk.Button(self.frameImage, text="Next >", command=self.nextImage)
            self.btnNextImage.config(width=20)
            self.btnNextImage.grid(column = 5, row = nButtonsRow, sticky='sw')
            
            # Check if the current image is the last image then block the next button
            if (self.currentSelectedLine == len(all_items) - 1):
                # Disable the next button
                self.btnNextImage.config(state=DISABLED)
            
            # Add button for previous image
            self.btnPrevImage = ttk.Button(self.frameImage, text="< Prev", command=self.prevImage)
            self.btnPrevImage.config(width=20)
            self.btnPrevImage.grid(column = 0, row = nButtonsRow, sticky='sw')
            
            # Check if the current image is the first image then block the prev button
            if (self.currentSelectedLine <= 0):
                # Disable the prev button
                self.btnPrevImage.config(state=DISABLED)
            
            # Scroll image using mouse wheel
            self.imgCanvas.bind("<MouseWheel>",self.zoomer)
            
            # Move using mouse click
            self.imgCanvas.bind("<ButtonPress-1>", self.move_start)
            self.imgCanvas.bind("<B1-Motion>", self.move_move)
            
        except IOError:
            print(IOError.message)
            
    def zoomer(self, event):
        """
        The function performs zoom-in or zoom-out according to the event of mouse wheel moving
        
        Parameters:
            self    - the object
            event   - mouse wheel event
        
        Return:
            None
        """
        
        # Get image current size
        width, height = self.img.size
        
        # If moved the mouse wheel forward
        if (event.delta > 0):
            # Resize the image bythe zoom in scale value
            self.img = self.img.resize((int(width * ZOOM_IN_SCALE), int(height * ZOOM_IN_SCALE)), Image.ANTIALIAS)
            
        # If moved the mouse wheel backward
        elif (event.delta < 0):
            # Check if the size after resize will be less than minimum image size
            if ((int(width * ZOOM_OUT_SCALE) > MIN_DISPLAY_SIZE_WIDTH) and 
                (int(height * ZOOM_OUT_SCALE) > MIN_DISPLAY_SIZE_HEIGHT)):
    
                # Resize the image bythe zoom out scale value
                self.img = self.img.resize((int(width * ZOOM_OUT_SCALE), int(height * ZOOM_OUT_SCALE)), Image.ANTIALIAS)
        
        # Put photo as attribute in order to prevent garbage collection
        self.photo = ImageTk.PhotoImage(self.img)
        
        # Clear canvas before zoom
        self.imgCanvas.delete("all")
        
        # put image on canvas pic's upper left corner (NW) on the canvas
        self.imgCanvas.create_image((0,0), image=self.photo, anchor=NW)
        
        # Configure canvas to be scrollabale
        self.imgCanvas.configure(scrollregion = self.imgCanvas.bbox("all"))

    def move_start(self, event):
        """
        The function allows mouse moving on the preview image in the canvas
        
        Parameters:
            self    - the object
            event   - mouse move event
        
        Return:
            None
        """
        
        self.imgCanvas.scan_mark(event.x, event.y)
    
    def move_move(self, event):
        """
        The function allows image drag on the preview image in the canvas
        
        Parameters:
            self    - the object
            event   - mouse drag event
        
        Return:
            None
        """
        
        self.imgCanvas.scan_dragto(event.x, event.y, gain=1)
    
    def previewSegmentation(self):
        """
        The function runs the preview image segmentation on the current chosen image with the selected parameters (or default).
        The function shows the preview result on the screen.
        
        Parameters:
            self    - the object
        
        Return:
            None
        """
        
        # Get parameters for the image
        currentFile = self.path + '/' + self.currentFile
        threshold = self.threshold.get()
        minSizeVal = self.minSizeVal.get()
        areaVal = self.areaVal.get()
        maxSizeVal = self.maxSizeVal.get()
        
        # Save image shape before segmentation in order to save the scale
        width, height = self.img.size
        
        try:
            # Prepare list with configuration for image
            lstConfigImg = [seg.imageConfigSegment(currentFile, threshold, minSizeVal, areaVal, maxSizeVal), threshold, minSizeVal, areaVal, maxSizeVal]
            
            # Save the parameters for the image
            self.dictFilesSegment[self.currentFile] = lstConfigImg
            
            # Perform the segmentation after changing values
            self.img = self.dictFilesSegment[self.currentFile][SEGMENT_FUNC_INDX]()
            self.img = self.img.resize((width, height), Image.ANTIALIAS)
            self.photo = ImageTk.PhotoImage(self.img)
            
            # put image on canvas pic's upper left corner (NW) on the canvas
            self.imgCanvas.create_image((0,0), image=self.photo, anchor=NW)
            
        except ValueError:
            messagebox.showerror(title="Error", message="Wrong threshold values selected!")

        
    def resetThresholds(self):
        """
        The function reset the thresholds to default values
        
        Parameters:
            self - the object
        
        Return:
            None
        """
        
        # Reset values for thresholds
        self.threshold.set(DEFAULT_THRESHOLD)
        self.minSizeVal.set(DEFAULT_MIN_SIZE)
        self.areaVal.set(DEFAULT_AREA_SIZE)
        self.maxSizeVal.set(DEFAULT_MAX_SIZE)
        
    def loadImagesInPath(self):
        """
        The function loads all the images in the selected path.
        Only images of acceptable types will be loaded (acceptable types are types in ACCEPTED_EXTENSIONS).
        If the directory contains DICOM files, the files will be converted to PNG.
        
        Parameters:
            self - the object
        
        Return:
            None
        """
        
        # Create empty dictionary for files
        self.dictFilesSegment = {}
        
        # get all the dicom files from the current directory
        dcmFiles = list(filter(lambda file: file.endswith('.dcm'), listdir(self.path)))
        
        # Check if exist at least one dicom files in the directory
        if (len(dcmFiles) != 0):
            # Convert the dicom files to png
            cd.convertDCM(self.path)
        
        # Load all files in directory to array - without directories
        onlyfiles = [f for f in listdir(self.path) if isfile(join(self.path, f)) and f.lower().endswith(ACCEPTED_EXTENSIONS)]
        
        # Define image index
        nImgIndex = 0
        
        # Open all the images in the directory
        for image in onlyfiles:    
            self.lbFiles.insert(nImgIndex,image)
            
            # Save images into dictionary in order to perform segmentation
            self.dictFilesSegment[image] = [seg.imageConfigSegment(self.path + '/' + image), DEFAULT_THRESHOLD, DEFAULT_MIN_SIZE, DEFAULT_AREA_SIZE, DEFAULT_MAX_SIZE]
            
            # Increment the index
            nImgIndex = nImgIndex + 1
    
    def editImage(self):
        """
        The function runs the editor on the current selected image.
        If the image was saved after the edit then the function loads it to the main app,
        and performs the preview of the segementation on the new edited image.
        
        Parameters:
            self - the object
        
        Return:
            None
        """
        
        # Start the paint application on the selected image
        paintWindow = pnt.PaintApp(self.currentFile, self.path)
        paintWindow.show()
        
        # Prevent garbage collector cleaning the memory and closing the window
        pnt.paintApp.exec_()
        
        # Check if saved as image
        if (pnt.savedAsImageFlag):
            # Check if the file has different name and need to be added to list
            if (pnt.savedAsPath == pnt.SAVED_SAME_PATH_DIFF_NAME):
                # Add the new file to the file list
                self.lbFiles.insert(self.lbFiles.size(), pnt.savedAsFileName)
            # Same path and same name
            elif (pnt.savedAsPath == pnt.SAVED_SAME_PATH_AND_NAME):
                # Reload the image
                self.previewSegmentation()
        # Check if image saved (simple save and not saveas)
        elif (pnt.savedImageFlag):
            # Reload the image
            self.previewSegmentation()
        
    def notebook(self):
        """
        The function runs the notebook application in order to write memo pages.
        
        Parameters:
            self - the object
        
        Return:
            None
        """
        
        noteP = no.Note()
        noteP.show()
        
    def about(self):
        """
        The function opens the about window.
        
        Parameters:
            self - the object
        
        Return:
            None
        """
        
        aboutW = ab.AboutW()
        aboutW.show()
        
        # Prevent garbage collector cleaning the memory and closing the window
        mainloop()
    
    # Open Documentaion file
    def documentation(self):
        """
        The function opens the PDF documentation page.
        
        Parameters:
            self - the object
        
        Return:
            None
        """
        
        # Open the documentation page from the program path
        webbrowser.open(DOCUMENTATION_FILE, new=2)     
       
    def fileDialog(self):
        """
        The function opens the file dialog in order to get the images directory from the user.
        
        Parameters:
            self - the object
        
        Return:
            None
        """

        # Browse for directory of images
        self.path = filedialog.askdirectory()
        
        # Check if path was selected open all images in path
        if self.path != '':
            self.lbFiles.delete(0,'end')
            
            # Load all the images in the current selected path into the listbox
            self.loadImagesInPath()
            
    def performSegmentation(self):
        """
        The function performs the segmentation on all the images in the listbox according to the chosen parameters.
        If there is no images in the path the function will raise error message, otherwise the function will ask a path and name
        to save the result files.
        The function will build Two result files <selected_name>_contour.txt for contour coordinates,
        and <selected_name>_grayscale.txt for grayscale coordinates.
        The function will show progress bar for the whole segmentation.
        
        Parameters:
            self - the object
        
        Return:
            None
        """
        
        # Get the number of pictures to perform segmentation
        picNum = self.lbFiles.size()
        
        # Check if no images in list to perform segmentation
        if (picNum == 0):
            messagebox.showerror(title="Error", message="No images was selected to perform segmentation!")
        # Exists at least One image to segmentation
        else:
            # Select the path and name of the result files
            fullpath = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=(("Text", "*.txt"),("All Files", "*.*")))
            
            # Check if selected wrong path
            if (not fullpath):
                # Wrong path selected
                messagebox.showerror(title="Error", message="Wrong path selected!")
                
                return 0
            # Correct path selected
            else:
                # Get filename and path from fullpath
                filename = basename(fullpath)
                filepath = dirname(fullpath)
                
                #start progress bar
                popup = Toplevel()
                
                # Set size of popup window
                popup.geometry(str(PROGRESS_BAR_LENGTH) + "x" + str(PROGRESS_BAR_WIDTH))
                
                # Disable buttons for popup
                popup.resizable(0,0)
                
                # Set progress bar window label as segmentation
                labelText = StringVar()
                Label(popup, textvariable=labelText).grid(row=0,column=0)
                
                # Initialize progress to Zero
                progress = PROGRESS_BAR_INIT
                
                # Create the progress bar widget
                progress_var = DoubleVar()
                progress_bar = ttk.Progressbar(popup, variable=progress_var, maximum=PROGRESS_BAR_PERCENTAGE, length=PROGRESS_BAR_LENGTH)
                progress_bar.grid(row=1, column=0, sticky="NESW")
                
                # Define progress step as 100 divide by number of images
                progress_step = float(PROGRESS_BAR_PERCENTAGE / (picNum))
                
                # Set pictures counter
                picCounter = 0
                
                # Run over the images and perform the segmentation
                for curFile in self.dictFilesSegment:
                    
                    # Update the percentage of segmentation with percision of 2 digits after float point
                    labelText.set(str(format((picCounter * progress_step), '.2f')) + "%")
                    
                    # Update progress bar popup window
                    popup.update()
                    
                    # Wait for the result of segmentation
                    #time.sleep(1)
                    self.dictFilesSegment[curFile][SEGMENT_FUNC_INDX](1,filepath,filename, picCounter)
                    
                    # Increment the progress
                    progress += progress_step
                    
                    # Set the current progress
                    progress_var.set(progress)
                    
                    # Increment picture counter
                    picCounter += 1
                 
                # Destroy the popup windows as the segmentation ended
                popup.destroy()
                
        return 0
                
    def singleImageSegmentation(self):
        """
        The function performs the segmentation for single selected image.
        The function will ask a path and name to save the result files.
        The function will build Two result files <selected_name>_contour.txt for contour coordinates,
        and <selected_name>_grayscale.txt for grayscale coordinates.
        The function will show message when the segmentation completed.
        
        Parameters:
            self - the object
        
        Return:
            None
        """
        
        
        # Select the path and name of the result files
        fullpath = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=(("Text", "*.txt"),("All Files", "*.*")))
        
        # Check if selected wrong path
        if (not fullpath):
            # Wrong path selected
            messagebox.showerror(title="Error", message="Wrong path selected!")
            
            return 0
        # Correct path selected
        else:
            # Get filename and path from fullpath
            filename = basename(fullpath)
            filepath = dirname(fullpath)
            
            # Perform segmentation and save to file
            self.dictFilesSegment[self.currentFile][SEGMENT_FUNC_INDX](1,filepath,filename, 0)
            
            # Show message about successful segmentation
            messagebox.showinfo(title="Segmentation completed!", message="Segmentation of " + self.currentFile + " completed!")

# Check if we are running the module from the main scope
if __name__ == "__main__":
    # Execute only if run from the main file and not as import
    
    # Run the main GUI
    root = Root()
    root.mainloop()
