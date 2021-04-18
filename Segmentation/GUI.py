# -*- coding: utf-8 -*-

try:
    from datetime import datetime
    from tkinter import *
    from tkinter import ttk
    from tkinter import filedialog
    from tkinter import messagebox
    from PIL import Image, ImageTk
    from os import listdir, getcwd, mkdir
    from os.path import isfile, join, basename, dirname
    from tkinter import Menu
    from pathlib import Path
    import Segmentation as seg
    import Paint as pnt 
    import Notebook as no
    import AboutWindow as ab
    import ConvertDicom as cd
    import ImageChoose as ic
    import AboutWindow as aw
    import PixelSpacingChoose as psc
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
MIN_DISPLAY_SIZE_WIDTH  = 500           # Minimum size in pixel of displayed image of width
MIN_DISPLAY_SIZE_HEIGHT = 500           # Minimum size in pixel of displayed image of height
SEGMENT_FUNC_INDX       = 0             # Index for segmentation function in the list inside dictionary of files
THRESHOLD_INDX          = 1             # Index for threshold in the list inside dictionary of files
MIN_SIZE_INDX           = 2             # Index for min size in the list inside dictionary of files
AREA_SIZE_INDX          = 3             # Index for area size in the list inside dictionary of files
MAX_SIZE_INDX           = 4             # Index for max size in the list inside dictionary of files
CONFIGURED_INDX         = 5             # Index for flag if the image configured or default values saved
PROGRESS_BAR_LENGTH     = 300           # Length of progressbar window
PROGRESS_BAR_WIDTH      = 50            # Width of progressbar window
PROGRESS_BAR_PERCENTAGE = 100.0         # Percent of progress bar set to 100
PROGRESS_BAR_INIT       = 0             # value for reseting progress bar to progress Zero
IMG_NOT_OPEN_FLAG       = 0             # Flag if user didn't open image yet
IMG_ALREADY_OPEN_FLAG   = 1             # Flag if user already opend image
SEGMENTATION_SUCCESS    = 0             # Flag indicates segmentation successfully done
SEGMENTATION_ERROR      = 1             # Flag indicates failed to perofrm segmentation
PROGRAM_PATH            = getcwd()      # Get path of the py files
DOCUMENTATION_FILE      = PROGRAM_PATH + '/Documentation/DOCU.pdf'  # Get documentation file path
DEMO_VIDEO_URL          = "https://youtu.be/d84Q1buXCMw"            # The link of demo video
STATE_DIRECTORY_NAME    = '/Saved_state'                            # Path to state files
DICT_STATE_FNAME        = "dict_state.txt"                          # Name of dictionary file
TESTED_STATE_FNAME      = "tested_files_state.txt"                  # Name of tested files file
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
        self.title("Easy Bone Segmentation - SCE")
        
        # Set icon for the application
        icon = PhotoImage(file=PROGRAM_PATH + "/images/icon.png")
        self.iconphoto(False, icon)
        
        # Set size of the window
        self.minsize(WINDOW_HEIGHT, WINDOW_WIDTH)
        
        # Create upper menu using the function
        self.upperMenu()
        
        # Create image select panel using the function
        self.imageSelectPanel()
        
        # Disable resize of the window
        self.resizable(False, False)
        
        # Set flag for already chosen image
        self.imgAlreadyOpen = IMG_NOT_OPEN_FLAG
        
        # Set default threshold currently set for application
        self.default_threshold = DEFAULT_THRESHOLD
        self.default_area_size = DEFAULT_AREA_SIZE
        self.default_min_size = DEFAULT_MIN_SIZE
        self.default_max_size = DEFAULT_MAX_SIZE
        
        # List to store the names of tested files
        self.lstTestedFiles = []
       
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
        self.fileMenu = Menu(self.menu, tearoff=False)
        
        # Add the file menu to the upper menu
        self.menu.add_cascade(label='File', menu=self.fileMenu)
        self.config(menu=self.menu)
        
        # Add button for choosing directory of files
        self.fileMenu.add_command(label='Open Directory', command = self.fileDialog)
        
        # Add separator for the exit button
        self.fileMenu.add_separator()
        
        # Add button for perform segmentation on all images in list
        self.fileMenu.add_command(label='Perform segmentation', command = self.performSegmentation)
        
        # Add separator for the exit button
        self.fileMenu.add_separator()
        
        # Add button for save the state of configurations
        self.fileMenu.add_command(label='Save state', state = DISABLED, command = self.saveConfigState)
        
        # Add button for load the state of configurations
        self.fileMenu.add_command(label='Load state', state = DISABLED, command = self.loadConfigState)
        
        # Add separator for the exit button
        self.fileMenu.add_separator()
        
        # Add exit button to File menu
        self.fileMenu.add_command(label='Exit', command = self.programExit, accelerator="Ctrl+Q")
        self.bind_all("<Control-q>", self.programExit)
        
         # ==================  Edit Menu
        
        # Create edit button for the upper menu
        self.editMenu = Menu(self.menu, tearoff=False)
        
        # Add the edit menu to the upper menu
        self.menu.add_cascade(label='Edit', menu=self.editMenu)
        self.config(menu=self.menu)
        
        # Add button for sort ascending
        self.editMenu.add_command(label='Sort Ascending', state = DISABLED, command = self.sortAsc)
        
        # Add button for sort descending
        self.editMenu.add_command(label='Sort Descending', state = DISABLED, command = self.sortDesc)
        
        # Add separator for the Documentation button
        self.editMenu.add_separator()
        
        # Add button for save current values to default thresholds
        self.editMenu.add_command(label='Set Default Thresholds', state = DISABLED, command = self.setNewDefault)
        
        # Add button for reset the default thresholds to program default
        self.editMenu.add_command(label='Reset Default Thresholds', state = DISABLED, command = self.resetDefaultValues)
        
        # Add separator for the Documentation button
        self.editMenu.add_separator()
        
        # Add button for set thresholds on images below
        self.editMenu.add_command(label='Set Thresholds Below', state = DISABLED, command = self.setBelowThresholds)
        
        # Add separator for the Documentation button
        self.editMenu.add_separator()
        
        # Add button for set spacing for current segmentation
        self.editMenu.add_command(label='Set Spacing Values', state = DISABLED, command = self.setSpacingValues)
        
        # Add separator for the Documentation button
        self.editMenu.add_separator()
        
        # Add button for save current values to default thresholds
        self.editMenu.add_command(label='Remove Image', state = DISABLED, command = self.delSingleFile)
        
        # Add button for reset the default thresholds to program default
        self.editMenu.add_command(label='Reopen Image', state = DISABLED, command = self.reopenImage)
        
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
        
        # Add separator for the Documentation button
        helpMenu.add_separator()
        
        # Add Demo video button to Help menu
        helpMenu.add_command(label='Demo', command = lambda: webbrowser.open(DEMO_VIDEO_URL, new=2))
        
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
        
        # Check if already image opend then 
        if(self.imgAlreadyOpen == IMG_ALREADY_OPEN_FLAG):
            # Image already exists then destroy the frame to create new one for new image
            self.frameImage.destroy()
               
        # Set the current file with path
        self.currentFile = all_items[zImgIndx]
        
        try:
            # Mark the image as already selected
            self.lbFiles.itemconfig(zImgIndx, bg=TESTED_IMGS_COLOR)
            
            # Add the image index to list of tested files
            self.lstTestedFiles.append(self.currentFile)
            
            # Create frame for image
            self.frameImage = Frame(self)
            self.frameImage.grid(column = 2, row = 0, sticky='nsew')
            
            # Create canvas for image
            self.imgCanvas = Canvas(self.frameImage, width = MIN_DISPLAY_SIZE_WIDTH, height = MIN_DISPLAY_SIZE_HEIGHT)
            
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
            
            # Define variable to hold boolean value for checkbutton
            bLockParams = self.dictFilesSegment[self.currentFile][CONFIGURED_INDX]
            self.varLockedParams = BooleanVar(value=bLockParams)
            
            # Define variablies to hold data in silders and spinboxes
            varThreshold = DoubleVar(value = 0.)
            varMinSize = IntVar(value = 0)
            varMaxSize = DoubleVar(value = 0)
            varAreaThreshold = IntVar(value = 0)
            
            # Add checkbutton to set image as configured or able to reset
            self.cbLockParams = Checkbutton(self.frameImage, text = 'Lock params', variable=self.varLockedParams, command=self.lockParams)
            self.cbLockParams.grid(row = 0, column = 5, sticky = 'WE')
            
            # Check if need to select because image locked
            if (bLockParams):
                self.cbLockParams.select()
            # Need deselect because the image is not locked
            else:
                self.cbLockParams.deselect()
            
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
            
            # -------- Buttons first line --------
            
            # Add button for previous image
            self.btnPrevImage = ttk.Button(self.frameImage, text="< Prev", command=self.prevImage)
            self.btnPrevImage.config(width=20)
            self.btnPrevImage.grid(column = 0, row = nButtonsRow, sticky='sw')
            
            # Check if the current image is the first image then block the prev button
            if (self.currentSelectedLine <= 0):
                # Disable the prev button
                self.btnPrevImage.config(state=DISABLED)
            
            # Add button for segmentation Preview
            self.btnSegmentPreview = ttk.Button(self.frameImage, text="Preview", command=self.previewSegmentation)
            self.btnSegmentPreview.config(width=20)
            self.btnSegmentPreview.grid(column = 1, row = nButtonsRow, sticky='sw')
            
            # Add button for clear segmentation values
            self.btnResetToDefault = ttk.Button(self.frameImage, text="Reset Thresholds", command=self.resetThresholds)
            self.btnResetToDefault.config(width=20)
            self.btnResetToDefault.grid(column = 2, row = nButtonsRow, sticky='sw')
            
            # Add button for image segmentation save
            self.btnSingleSegment = ttk.Button(self.frameImage, text="Save", command=self.singleImageSegmentation)
            self.btnSingleSegment.config(width=20)
            self.btnSingleSegment.grid(column = 3, row = nButtonsRow, sticky='sw')
            
            # Add button for image edit
            self.btnImgEdit = ttk.Button(self.frameImage, text="Edit", command=self.editImage)
            self.btnImgEdit.config(width=20)
            self.btnImgEdit.grid(column = 4, row = nButtonsRow, sticky='sw')
            
            # Add button for next image
            self.btnNextImage = ttk.Button(self.frameImage, text="Next >", command=self.nextImage)
            self.btnNextImage.config(width=20)
            self.btnNextImage.grid(column = 5, row = nButtonsRow, sticky='sw')
            
            # Check if the current image is the last image then block the next button
            if (self.currentSelectedLine == len(all_items) - 1):
                # Disable the next button
                self.btnNextImage.config(state=DISABLED)
            
            # -------- Evenets buttons ---------
            
            # Scroll image using mouse wheel
            self.imgCanvas.bind("<MouseWheel>",self.zoomer)
            
            # Move using mouse click
            self.imgCanvas.bind("<ButtonPress-1>", self.move_start)
            self.imgCanvas.bind("<B1-Motion>", self.move_move)
            
            # Open edit menu buttons if successfully opend image
            self.editMenu.entryconfig("Set Default Thresholds", state=NORMAL)
            self.editMenu.entryconfig("Reset Default Thresholds", state=NORMAL)
            self.editMenu.entryconfig("Remove Image", state=NORMAL)
            self.editMenu.entryconfig("Set Thresholds Below", state=NORMAL)
            
            # Set image open flag as true
            self.imgAlreadyOpen = IMG_ALREADY_OPEN_FLAG
                        
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
            lstConfigImg = [seg.imageConfigSegment(currentFile, threshold, minSizeVal, areaVal, maxSizeVal), threshold, minSizeVal, areaVal, maxSizeVal, True]
            
            # Save the parameters for the image
            self.dictFilesSegment[self.currentFile] = lstConfigImg
            
            # Perform the segmentation after changing values
            self.img = self.dictFilesSegment[self.currentFile][SEGMENT_FUNC_INDX]()
            self.img = self.img.resize((width, height), Image.ANTIALIAS)
            self.photo = ImageTk.PhotoImage(self.img)
            
            # put image on canvas pic's upper left corner (NW) on the canvas
            self.imgCanvas.create_image((0,0), image=self.photo, anchor=NW)
            
            # Set image as locked parameters change
            self.cbLockParams.select()
            
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
        self.threshold.set(self.default_threshold)
        self.minSizeVal.set(self.default_min_size)
        self.areaVal.set(self.default_area_size)
        self.maxSizeVal.set(self.default_max_size)
        
    def lockImageDependentButtons(self, stateButtons):
        """
        The function change the state of image dependent buttons according to the state in stateButtons parameter
        
        Parameters:
            self         - the object
            stateButtons - the new state of buttons
        
        Return:
            None
        """
        # Set the state according to images in directory to all buttons that depend on images
        self.editMenu.entryconfig("Sort Ascending", state = stateButtons)
        self.editMenu.entryconfig("Sort Descending", state = stateButtons)
        self.editMenu.entryconfig("Reopen Image", state = stateButtons)
        self.fileMenu.entryconfig("Save state", state = stateButtons)
        self.fileMenu.entryconfig("Load state", state = stateButtons)
        self.editMenu.entryconfig("Set Spacing Values", state = stateButtons)
        
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
        
        # State of buttons that depends on images in folder
        stateButtons = DISABLED
        
        # Create empty dictionary for files
        self.dictFilesSegment = {}
        
        # get all the dicom files from the current directory
        dcmFiles = list(filter(lambda file: file.endswith('.dcm'), listdir(self.path)))
        
        # Check if exist at least one dicom files in the directory
        if (len(dcmFiles) != 0):
            # Convert the dicom files to png
            cd.convertDCM(self.path)
        
        # Load all files in directory to array - without directories
        self.lstOnlyWantedFilesInDir = [f for f in listdir(self.path) if isfile(join(self.path, f)) and f.lower().endswith(ACCEPTED_EXTENSIONS)]
        
        # Define image index
        nImgIndex = 0
        
        # Open all the images in the directory
        for image in self.lstOnlyWantedFilesInDir:    
            self.lbFiles.insert(nImgIndex,image)
            
            # Save images into dictionary in order to perform segmentation
            self.dictFilesSegment[image] = [seg.imageConfigSegment(self.path + '/' + image), self.default_threshold, self.default_min_size, self.default_area_size, self.default_max_size, False]
            
            # Increment the index
            nImgIndex = nImgIndex + 1
        
        # Check if images exists in the directory then change state of buttons
        if (nImgIndex != 0):
            stateButtons = NORMAL
            
        # Set the state of buttons if images exists in directory or not
        self.lockImageDependentButtons(stateButtons)
    
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
        
        # Make the main screen invisible
        self.withdraw()
        
        # Start the paint application on the selected image
        paintWindow = pnt.PaintApp(self.currentFile, self.path)
        paintWindow.showMaximized()
        
        # Prevent garbage collector cleaning the memory and closing the window
        pnt.paintApp.exec_()
        
        # Check if saved as image
        if (pnt.savedAsImageFlag):
            # Check if the file has different name and need to be added to list
            if (pnt.savedAsPath == pnt.SAVED_SAME_PATH_DIFF_NAME):
                # Add the new file to the file list
                self.lbFiles.insert(self.lbFiles.size(), pnt.savedAsFileName)
                
                # Add the image into dictionary in order to perform segmentation
                self.dictFilesSegment[pnt.savedAsFileName] = [seg.imageConfigSegment(self.path + '/' + pnt.savedAsFileName), self.default_threshold, self.default_min_size, self.default_area_size, self.default_max_size, False]
                
                # Add the file to wanted files list
                self.lstOnlyWantedFilesInDir.append(pnt.savedAsFileName)
                
            # Same path and same name
            elif (pnt.savedAsPath == pnt.SAVED_SAME_PATH_AND_NAME):
                # Reload the image
                self.previewSegmentation()
        # Check if image saved (simple save and not saveas)
        elif (pnt.savedImageFlag):
            # Reload the image
            self.previewSegmentation()
        
        # Return the main screen be visible
        self.deiconify()
        
    def notebook(self):
        """
        The function runs the notebook application in order to write memo pages.
        
        Parameters:
            self - the object
        
        Return:
            None
        """
        
        # Make the main screen invisible
        self.withdraw()
        
        # Create notebook instance
        noteP = no.Note()
        
        # Show the notebook
        noteP.show()
        
        # Prevent garbage collector cleaning the memory and closing the window
        no.noteApp.exec_()
        
        # Return the main screen be visible
        self.deiconify()
        
    def about(self):
        """
        The function opens the about window.
        
        Parameters:
            self - the object
        
        Return:
            None
        """
        """
        aboutW = ab.AboutW()
        aboutW.show()
        
        # Prevent garbage collector cleaning the memory and closing the window
        mainloop()
        """
        # Open the about screen
        AboutWin = aw.AboutW()
        
        # Set the about window on always top
        AboutWin.grab_set_global()
    
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
            
            # Check if already image opend then clean the image frame
            self.cleanImageFrame()
            
            # Reset the spacing values per directory
            seg.pixel_to_mm_val_configured = seg.PIXEL_TO_MM_VAL_DEFAULT
            
            # Clear the list of files that already tested
            self.lstTestedFiles = []
    
    def cleanImageFrame(self):
        """
        The function cleans the image frame with buttons and closes the buttons that depends on image.
        
        Parameters:
            self - the object
        
        Return:
            None
        """
        
        # Check if already image opend then 
        if(self.imgAlreadyOpen == IMG_ALREADY_OPEN_FLAG):
            # Image already exists then destroy the frame to create new one for new image
            self.frameImage.destroy()
            
            # As image not selected disable all the buttons that use open image panel
            self.editMenu.entryconfig("Set Default Thresholds", state=DISABLED)
            self.editMenu.entryconfig("Reset Default Thresholds", state=DISABLED)
            self.editMenu.entryconfig("Remove Image", state=DISABLED)
            self.editMenu.entryconfig("Set Thresholds Below", state=DISABLED)
            
        # Change image already opend to not opend image
        self.imgAlreadyOpen = IMG_NOT_OPEN_FLAG
    
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
                
                return (SEGMENTATION_ERROR)
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
                    
                    # Perform segmentatuion
                    nSegStat = self.dictFilesSegment[curFile][SEGMENT_FUNC_INDX](1,filepath,filename, picCounter)
                    
                    # Check if segmentation failed on current image
                    if nSegStat == seg.SAVE_FAILED:
                        # Raise error message
                        messagebox.showerror(title="Error", message="Segmentation error due to incorrect parameters on image " + str(curFile) + "!")
                        
                        # Destroy the popup windows as the segmentation ended
                        popup.destroy()
                        
                        return (SEGMENTATION_ERROR)
                    
                    
                    # Increment the progress
                    progress += progress_step
                    
                    # Set the current progress
                    progress_var.set(progress)
                    
                    # Increment picture counter
                    picCounter += 1
                 
                # Destroy the popup windows as the segmentation ended
                popup.destroy()
                
        return (SEGMENTATION_SUCCESS)
                
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
            
            return (SEGMENTATION_ERROR)
        
        # Correct path selected
        else:
            # Get filename and path from fullpath
            filename = basename(fullpath)
            filepath = dirname(fullpath)
            
            # Perform segmentation and save to file
            nSegStat = self.dictFilesSegment[self.currentFile][SEGMENT_FUNC_INDX](1,filepath,filename, 0)
            
            # Check if segmentation failed on current image
            if nSegStat == seg.SAVE_FAILED:
                # Raise error message
                messagebox.showerror(title="Error", message="Segmentation error due to incorrect parameters on image " + str(self.currentFile) + "!")
                
                return (SEGMENTATION_ERROR)
            
            # Show message about successful segmentation
            messagebox.showinfo(title="Segmentation completed!", message="Segmentation of " + self.currentFile + " completed!")
            
            return (SEGMENTATION_SUCCESS)
    
    def setNewValuesForImages(self):
        """
        The function runs over all the files in the directory and if the image is not configured by the user,
        then the program resets the parameters to the new parameters.
        
        Parameters:
            None
        
        Return:
            None
        """
        
        # Run over all the images in path to set the new defualt if not already changed value
        for image in self.dictFilesSegment:
            # Check if values not yet changed by the user changed
            if (self.dictFilesSegment[image][CONFIGURED_INDX] == False):
                # Change images into values in order to perform segmentation
                self.dictFilesSegment[image] = [seg.imageConfigSegment(self.path + '/' + image, self.default_threshold, self.default_min_size, self.default_area_size, self.default_max_size), self.default_threshold, self.default_min_size, self.default_area_size, self.default_max_size, False]
    
    def setNewDefault(self):
        """
        The function sets the new values as default values
        
        Parameters:
            self - the object
        
        Return:
            None
        """
        
        # Check if user really want to set new default
        MsgBox = messagebox.askquestion('Change Default Values','Are you sure you want to change the default thresholds?',icon = 'question')
        
        # Check if yes selected by the user
        if MsgBox == 'yes':
            # Set new default values
            self.default_threshold = self.threshold.get()
            self.default_area_size = self.areaVal.get()
            self.default_min_size = self.minSizeVal.get()
            self.default_max_size = self.maxSizeVal.get()
            
            # Set the new default value for all images that not configured by the user
            self.setNewValuesForImages()
    
    def resetDefaultValues(self):
        """
        The function resets the default values to the program default
        
        Parameters:
            self - the object
        
        Return:
            None
        """
        
        # Check if user really want to reset default values
        MsgBox = messagebox.askquestion('Change Default Values','Are you sure you want to reset back to the default thresholds?',icon = 'question')
        
        # Check if yes selected by the user
        if MsgBox == 'yes':
            # Set new default values
            self.default_threshold = DEFAULT_THRESHOLD
            self.default_area_size = DEFAULT_AREA_SIZE
            self.default_min_size = DEFAULT_MIN_SIZE
            self.default_max_size = DEFAULT_MAX_SIZE
            
            # Set the new default value for all images that not configured by the user
            self.setNewValuesForImages()
            
    def setBelowThresholds(self):
        """
        The function sets the current selected thresholds on all images 
        below the current image and only if the image is not locked.
        If the image already locked then bypass the current image and move to next one.
        
        Parameters:
            self - the object
        
        Return:
            None
        """
        
        # Get values of parameters sliders
        threshold = self.threshold.get()
        minSizeVal = self.minSizeVal.get()
        areaVal = self.areaVal.get()
        maxSizeVal = self.maxSizeVal.get()
        
        # Find the index of current file
        nImgIndex = self.lbFiles.get(0, END).index(self.currentFile)
        
        # Check if the current image is the last image
        if (len(self.lbFiles.get(nImgIndex + 1, END)) == 0):
            messagebox.showwarning('Warning','You are on last image therefore there are no more images below!', icon = 'warning')
        # Current image is not last image
        else:
            # Check if user really want to set new default
            MsgBox = messagebox.askquestion('Change thresholds of images below','Are you sure you want to change the thresholds of images below the current image?',icon = 'question')
            
            # Check if yes selected by the user
            if (MsgBox == 'yes'):
                # Move on all images below the current image
                for image in self.lbFiles.get(nImgIndex + 1, END):
                    # Check if image already locked
                    if (self.dictFilesSegment[image][CONFIGURED_INDX] == False):
                        # Change images into values in order to perform segmentation
                        self.dictFilesSegment[image] = [seg.imageConfigSegment(self.path + '/' + image, threshold, minSizeVal, areaVal, maxSizeVal), threshold, minSizeVal, areaVal, maxSizeVal, False]
    
    def sortAsc(self):
        """
        The function sorts the listbox of files in ascending order.
        
        Parameters:
            self - the object
        
        Return:
            None
        """
        self.sortFiles()
        
    def sortDesc(self):
        """
        The function sorts the listbox of files in descending order.
        
        Parameters:
            self - the object
        
        Return:
            None
        """
        self.sortFiles(True)
    
    def sortFiles(self, bReverse=False):
        """
        The function sorts the listbox of files in selected order and saves the color of tested files.
        
        Parameters:
            self - the object
        
        Return:
            None
        """
        
        # sort the file list
        self.lstOnlyWantedFilesInDir.sort(reverse=bReverse)
        
        # Clean current listbox
        self.lbFiles.delete(0,END)
        
        # Define image index
        nImgIndex = 0
        
        # Open all the images in the directory
        for image in self.lstOnlyWantedFilesInDir:    
            self.lbFiles.insert(nImgIndex,image)
            
            # Check if image already tested to mark it green
            if (image in self.lstTestedFiles):
                # Mark the image as already selected
                self.lbFiles.itemconfig(nImgIndex, bg=TESTED_IMGS_COLOR)
            
            # Increment the index
            nImgIndex = nImgIndex + 1
    
    def lockParams(self):
        """
        The function changes the lock argument of the file according to the checkbox.
        
        Parameters:
            self - the object
        
        Return:
            None
        """
        
        # Change the lock argument for the current file
        self.dictFilesSegment[self.currentFile][CONFIGURED_INDX] = self.varLockedParams.get()
        
    def reopenImage(self):
        """
        The function opens new screen that allows to user to add or remove images from segmentation.
        
        Parameters:
            self - the object
        
        Return:
            None
        """
        
        # Make the main screen invisible
        self.withdraw()
        
        # Open the image selection screen
        ImgChoose = ic.ImageSelect(self.path, list(self.lbFiles.get(0,END)))
        
        # Wait till the image selection screen being destroyed
        self.wait_window(ImgChoose)
        
        # Return the main screen be visible
        self.deiconify()
        
        # Update list of images
        self.updateImageList()
    
    def updateImageList(self):
        """
        The function updates the listbox of files according to the selection to add or remove files from the list.
        If the file exists in wanted but not in results then remove it from list (selected to remove).
        If the file does not exist in wanted but in reslts then add it to list (selected to import).
        The function sorts the list in ascending order.
        
        Parameters:
            self - the object
        
        Return:
            None
        """
        
        # State of buttons that depends on images in folder
        stateButtons = DISABLED

        # Filter images to reload
        lstReloadImages = list(filter(lambda img: img not in self.lstOnlyWantedFilesInDir and img in ic.results, ic.results))
        
        # Filter images to remove
        lstRemoveImages = list(filter(lambda img: img in self.lstOnlyWantedFilesInDir and img not in ic.results, self.lstOnlyWantedFilesInDir))
        
        # Remove images from the list
        for image in lstRemoveImages:
            # Remove the selected files
            self.removeSingleFile(image)
        
        # Add images into the list
        for image in lstReloadImages:
            # Add the file to the list of files
            self.lbFiles.insert(END, image)
            
            # Add the current image into dictionary of configurations
            self.dictFilesSegment[image] = [seg.imageConfigSegment(self.path + '/' + image, self.default_threshold, self.default_min_size, self.default_area_size, self.default_max_size), self.default_threshold, self.default_min_size, self.default_area_size, self.default_max_size, False]
            
            # Add the file to wanted files list
            self.lstOnlyWantedFilesInDir.append(image)
        
        # Check if images exists
        if (self.lbFiles.size() != 0):
            stateButtons = NORMAL
            
            # Sort the images list in ascending order
            self.sortAsc()
        
        # Set the state of buttons if images exists in directory or not
        self.lockImageDependentButtons(stateButtons)
        
    def removeSingleFile(self, fileName):
        """
        The function removes the selected file from the files list
        
        Parameters:
            self     - the object
            filename - (str) the name of the file to remove
        
        Return:
            None
        """
        
        # Remove the file from dictionary
        del self.dictFilesSegment[fileName]
        
        # Check if file already tested
        if (fileName in self.lstTestedFiles):
            
            # Remove the file from tested files
            self.lstTestedFiles.remove(fileName)
        
        # Remove the file from wanted files list
        self.lstOnlyWantedFilesInDir.remove(fileName)
        
        # Remove the file from listbox
        nIndxFile = self.lbFiles.get(0, END).index(fileName)
        self.lbFiles.delete(nIndxFile)
        
    def delSingleFile(self):
        """
        The function performs remove of single file from list using removeSingleFile function.
        The function cleans the image frame.
        
        Parameters:
            self - the object
        
        Return:
            None
        """
        
        # Remove the single selected file
        self.removeSingleFile(self.currentFile)
        
        # Check if already image opend then clean the frame
        self.cleanImageFrame()
        
    def saveConfigState(self):
        """
        The function saves the configuration of images into results files in Save_state directory.
        The function saves both the dictionary of configurations and list of already tested files.
        
        Parameters:
            self - the object
        
        Return:
            None
        """
        
        # Create new directory for state files
        strStatePath = self.path + STATE_DIRECTORY_NAME
        
        # Check if directory already exists and save the state into boolean variable
        boolDirExists = Path(strStatePath).exists()
        
        # Check if state directory already exists if not create
        if (not boolDirExists):
            mkdir(strStatePath)
            
        # Write the dictionary of file configurations into file
        with open(strStatePath + "/" + DICT_STATE_FNAME, "w") as outDictState:
           outDictState.write(self.buildDictString())
           
        # Write the names of tested files into file
        with open(strStatePath + "/" + TESTED_STATE_FNAME, "w") as outTestedState:
           outTestedState.write(self.buildTestedFilesString())
           
    def buildDictString(self):
        """
        The function builds string with the configuration dictionary.
        
        Parameters:
            self - the object
        
        Return:
            None
        """
        
        # Result string
        strRes = ""
        
        # Run over the files in the dictionary
        for file in self.dictFilesSegment:
            strRes = strRes + file + "," \
                    + str(self.dictFilesSegment[file][THRESHOLD_INDX]) + "," \
                    + str(self.dictFilesSegment[file][MIN_SIZE_INDX]) + "," \
                    + str(self.dictFilesSegment[file][AREA_SIZE_INDX]) + "," \
                    + str(self.dictFilesSegment[file][MAX_SIZE_INDX]) + "," \
                    + str(self.dictFilesSegment[file][CONFIGURED_INDX]) + "\n"
            
        return (strRes)
    
    def buildTestedFilesString(self):
        """
        The function builds string with the filenames of tested files.
        
        Parameters:
            self - the object
        
        Return:
            None
        """
        
        # Result string
        strRes = ""
        
        # Run over the tested list
        for file in self.lstTestedFiles:
            strRes = strRes + file + "\n"
            
        return (strRes)
    
    def loadConfigState(self):
        """
        The function loads the saved state from files back into the system.
        If the file exists then the function loads configurations, otherwise,
        the current configurations remain.
        
        Parameters:
            self - the object
        
        Return:
            None
        """
        
        # Create new directory for state files
        strStatePath = self.path + STATE_DIRECTORY_NAME
        
        # List of images that saved
        lstSavedImages = []
        
        # Load the dictionary state into temporary dictionary for test
        with open(strStatePath + "/" + DICT_STATE_FNAME) as inDictState:
            # Run over the lines in file
            for line in inDictState:
                
                # Read the line and split it to list
                lstLine = line.split(",")
               
                # Define the path to the current file
                strFilePath = self.path + '/' + lstLine[0]
               
                # Check if the image exists in the path
                if ((Path(strFilePath).exists())):
                    
                    # Save the configurations for file into variables
                    fName = lstLine[0]
                    fThreshold = float(lstLine[1])
                    fMinSize = int(lstLine[2])
                    fAreaThreshold = int(lstLine[3])
                    fMaxSize = int(lstLine[4])
                    fConfigFlag = bool(lstLine[5])
                                               
                    # The file exists then recover the configuration
                    self.dictFilesSegment[fName] = [seg.imageConfigSegment(self.path + '/' + fName, fThreshold, fMinSize, fAreaThreshold, fMaxSize), fThreshold, fMinSize, fAreaThreshold, fMaxSize, fConfigFlag]
                    
                    # Add the image to saved images list 
                    lstSavedImages.append(lstLine[0])
        
        # Load the already tested files from file
        with open(strStatePath + "/" + TESTED_STATE_FNAME) as inTestedState:
            # Run over the lines in file
            for line in inTestedState:
                
                # Get the file name
                filename = line.rstrip("\n")
                
                # Define the path to the current file
                strFilePath = self.path + '/' + filename
                
                # Check if the image exists in the path
                if ((Path(strFilePath).exists())):
                
                    # Add the file to tested list
                    self.lstTestedFiles.append(filename)
                    
                    # Find the index of current file
                    nImgIndex = self.lbFiles.get(0, END).index(filename)
                    
                    # Mark the image as already selected
                    self.lbFiles.itemconfig(nImgIndex, bg=TESTED_IMGS_COLOR)
                    
        # Check all items in list that was not saved in save state option and remove them
        for image in list(self.dictFilesSegment.keys()):
            # Check if image was not saved as part of save state
            if image not in lstSavedImages:
                # Remove the image from the list
                self.removeSingleFile(image)
                
    def setSpacingValues(self):
        """
        The function opens new screen that allows user to change spacing parameters.
        
        Parameters:
            self - the object
        
        Return:
            None
        """
        
        # Make the main screen invisible
        self.withdraw()
        
        # Open the image selection screen
        SpacingChoose = psc.PixelSpaceChoose(seg.pixel_to_mm_val_configured)
        
        # Wait till the image selection screen being destroyed
        self.wait_window(SpacingChoose)
        
        # Return the main screen be visible
        self.deiconify()
        
        # Set the result list to segmentation algorithm
        seg.pixel_to_mm_val_configured = psc.results
        
# Check if we are running the module from the main scope
if __name__ == "__main__":
    # Execute only if run from the main file and not as import
    
    # Run the main GUI
    root = Root()
    root.mainloop()
